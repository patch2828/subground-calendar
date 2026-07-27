#!/usr/bin/env python3
"""
RESOURCE GUARD — desktop watchdog for resource hogs.

Samples every running process, groups them by app, and shows a live colorful
donut + bar readout of what is eating the most CPU / memory / disk right now.
When something starts stealing (over threshold, sustained), a window pops to
the front of the desktop naming the offender, and one button slows it down.

Throttling is real, reversible, and OS-level:
  EASE OFF  low priority
  SLOW      lowest priority + half the cores
  HEAVY     lowest priority + a quarter of the cores
  CHOKE     lowest priority + one core + suspend/resume duty cycling

Everything applied is remembered and restored on RESTORE, on quit, and on crash.

Run:
    python resource_guard.py            # the window
    python resource_guard.py --once     # one text snapshot, no GUI
"""

from __future__ import annotations

import argparse
import atexit
import json
import math
import os
import platform
import signal
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

try:
    import psutil
except ImportError:  # pragma: no cover - environment guard
    sys.exit(
        "RESOURCE GUARD needs psutil.\n"
        "  Windows:  py -m pip install psutil\n"
        "  macOS/Linux:  python3 -m pip install psutil"
    )

APP_NAME = "RESOURCE GUARD"
CONFIG_PATH = Path.home() / ".resource-guard.json"
IS_WINDOWS = platform.system() == "Windows"
IS_MACOS = platform.system() == "Darwin"

# ---------------------------------------------------------------- palette ----
# Same colors as the SubGround calendar page.
BG = "#0b0a12"
PANEL = "#15121f"
PANEL2 = "#1c1830"
LINE = "#2a2440"
INK = "#f4f1fb"
MUTED = "#a79fc4"
DIM = "#6f688c"
PURPLE = "#8b5cf6"
PURPLE2 = "#a78bfa"
ORANGE = "#ff8c42"
HOT = "#ff5470"
GREEN = "#3ddc84"
GOLD = "#ffd15c"
CYAN = "#22d3ee"
PINK = "#f472b6"

SERIES = [HOT, ORANGE, GOLD, GREEN, CYAN, PURPLE2, PINK, "#4cc9f0"]

# ------------------------------------------------------------- throttling ----
EASE, SLOW, HEAVY, CHOKE = 1, 2, 3, 4

LEVELS = {
    EASE: {
        "name": "EASE OFF",
        "color": GREEN,
        "cores": 0.75,
        "duty": None,
        "blurb": "low priority, keeps all cores",
    },
    SLOW: {
        "name": "SLOW",
        "color": GOLD,
        "cores": 0.5,
        "duty": None,
        "blurb": "lowest priority, half the cores",
    },
    HEAVY: {
        "name": "HEAVY",
        "color": ORANGE,
        "cores": 0.25,
        "duty": None,
        "blurb": "lowest priority, a quarter of the cores",
    },
    CHOKE: {
        "name": "CHOKE",
        "color": HOT,
        "cores": 0.0,  # single core
        "duty": (0.06, 0.14),  # run 60ms, pause 140ms
        "blurb": "one core + pulsed pauses — hard stop, may stutter the app",
    },
}

# Processes that keep the machine alive. Never touched, in any mode.
PROTECTED = {
    # Windows
    "system", "system idle process", "registry", "memory compression", "smss",
    "csrss", "wininit", "winlogon", "services", "lsass", "svchost", "dwm",
    "audiodg", "fontdrvhost", "explorer", "ctfmon", "sihost", "taskhostw",
    "searchindexer", "securityhealthservice", "msmpeng", "wudfhost",
    # macOS
    "kernel_task", "launchd", "windowserver", "loginwindow", "coreaudiod",
    "hidd", "systemuiserver", "dock", "finder",
    # Linux
    "systemd", "init", "kthreadd", "dbus-daemon", "xorg", "wayland", "gnome-shell",
    "pulseaudio", "pipewire",
}

METRICS = [
    ("cpu", "CPU", "%"),
    ("mem", "MEMORY", "%"),
    ("disk", "DISK", "MB/s"),
]

DEFAULTS = {
    "interval": 1.5,
    "auto_manage": True,
    "auto_level": SLOW,
    "cpu_threshold": 35.0,   # % of total machine CPU
    "mem_threshold": 25.0,   # % of total RAM
    "disk_threshold": 40.0,  # MB/s
    "strikes": 4,            # consecutive samples over the line before acting
    "always_on_top": False,
    "allowlist": [],         # app keys never auto-managed
}


def load_config() -> dict:
    cfg = dict(DEFAULTS)
    try:
        if CONFIG_PATH.exists():
            saved = json.loads(CONFIG_PATH.read_text())
            for k, v in saved.items():
                if k in cfg and isinstance(v, type(cfg[k])):
                    cfg[k] = v
    except Exception:
        pass
    return cfg


def save_config(cfg: dict) -> None:
    try:
        CONFIG_PATH.write_text(json.dumps(cfg, indent=2))
    except Exception:
        pass


# ------------------------------------------------------------- sampling -----
@dataclass
class Entity:
    """One app — every process sharing a name, summed together."""

    key: str
    label: str
    pids: list = field(default_factory=list)
    cpu: float = 0.0        # % of the whole machine
    mem_mb: float = 0.0
    mem_pct: float = 0.0
    disk: float = 0.0       # MB/s read+write
    user: str = ""

    def value(self, metric: str) -> float:
        return {"cpu": self.cpu, "mem": self.mem_pct, "disk": self.disk}[metric]

    def readout(self, metric: str) -> str:
        if metric == "cpu":
            return f"{self.cpu:.1f}%"
        if metric == "mem":
            return f"{self.mem_mb / 1024:.2f} GB"
        return f"{self.disk:.1f} MB/s"

    @property
    def protected(self) -> bool:
        return self.key in PROTECTED


class Sampler:
    """Walks the process table and returns apps sorted by a metric."""

    def __init__(self) -> None:
        self.ncpu = psutil.cpu_count(logical=True) or 1
        self.total_mem = psutil.virtual_memory().total
        self._procs: dict[int, psutil.Process] = {}
        self._io: dict[int, tuple[int, float]] = {}
        self.last_pid_stats: dict[int, tuple[float, float, float]] = {}
        self._self_pids = {os.getpid()}
        try:
            self._self_pids.add(os.getppid())
        except Exception:
            pass
        self.prime()

    def prime(self) -> None:
        """First cpu_percent() call per process always returns 0.0 — burn it."""
        for proc in psutil.process_iter():
            try:
                proc.cpu_percent(None)
                self._procs[proc.pid] = proc
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def _disk_rate(self, proc: psutil.Process, now: float) -> float:
        try:
            io = proc.io_counters()
        except (psutil.AccessDenied, psutil.NoSuchProcess, AttributeError):
            return 0.0
        total = io.read_bytes + io.write_bytes
        prev = self._io.get(proc.pid)
        self._io[proc.pid] = (total, now)
        if not prev:
            return 0.0
        prev_total, prev_ts = prev
        dt = now - prev_ts
        if dt <= 0 or total < prev_total:
            return 0.0
        return (total - prev_total) / dt / (1024 * 1024)

    def sample(self) -> list[Entity]:
        now = time.monotonic()
        alive: set[int] = set()
        apps: dict[str, Entity] = {}
        per_pid: dict[int, tuple[float, float, float]] = {}

        for proc in psutil.process_iter(["pid", "name", "username"]):
            pid = proc.pid
            if pid in self._self_pids or pid <= 0:
                continue
            alive.add(pid)
            cached = self._procs.get(pid)
            if cached is None:
                self._procs[pid] = proc
                try:
                    proc.cpu_percent(None)  # prime the new arrival
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
                continue
            try:
                raw_name = cached.name()
                cpu = cached.cpu_percent(None) / self.ncpu
                rss = cached.memory_info().rss
                disk = self._disk_rate(cached, now)
                try:
                    user = cached.username()
                except (psutil.AccessDenied, KeyError):
                    user = ""
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

            per_pid[pid] = (cpu, rss / (1024 * 1024), disk)
            key = raw_name.lower().removesuffix(".exe")
            app = apps.get(key)
            if app is None:
                app = Entity(key=key, label=raw_name.removesuffix(".exe"), user=user)
                apps[key] = app
            app.pids.append(pid)
            app.cpu += cpu
            app.mem_mb += rss / (1024 * 1024)
            app.disk += disk

        for dead in set(self._procs) - alive:
            self._procs.pop(dead, None)
            self._io.pop(dead, None)

        self.last_pid_stats = per_pid
        total_mb = self.total_mem / (1024 * 1024)
        for app in apps.values():
            app.mem_pct = app.mem_mb / total_mb * 100.0
            app.cpu = min(app.cpu, 100.0)

        return list(apps.values())

    @staticmethod
    def top(entities: list[Entity], metric: str, n: int = 8) -> list[Entity]:
        ranked = sorted(entities, key=lambda e: e.value(metric), reverse=True)
        return [e for e in ranked[:n] if e.value(metric) > 0.05]


# ----------------------------------------------------------- chat meters ----
# One live meter per chat window — a Claude desktop window, or a browser window
# sitting on a chat tab. Window titles are what make per-chat granularity
# possible; where the OS won't hand them over we fall back to per-process.
CHAT_HINTS = ("claude", "chatgpt", "openai", "gemini", "copilot", "perplexity", "grok")
CHAT_PROC_HINTS = ("claude", "chatgpt", "chrome", "msedge", "brave", "firefox")


@dataclass
class ChatWindow:
    pid: int
    title: str
    cpu: float = 0.0      # % of the whole machine, i.e. per-second load
    mem_mb: float = 0.0
    disk: float = 0.0

    @property
    def short(self) -> str:
        t = self.title.strip()
        for junk in (" — Claude", " - Claude", " | Claude", " — Google Chrome",
                     " - Google Chrome", " and 1 more page", " — Mozilla Firefox"):
            t = t.replace(junk, "")
        t = t.strip() or f"pid {self.pid}"
        return t if len(t) <= 34 else t[:33] + "…"


def _windows_titles() -> list[tuple[int, str]]:
    """(pid, title) for every visible top-level window. Windows only."""
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.WinDLL("user32", use_last_error=True)
    found: list[tuple[int, str]] = []

    WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

    def cb(hwnd, _lparam):
        if not user32.IsWindowVisible(hwnd):
            return True
        length = user32.GetWindowTextLengthW(hwnd)
        if length <= 0:
            return True
        buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buf, length + 1)
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        found.append((int(pid.value), buf.value))
        return True

    user32.EnumWindows(WNDENUMPROC(cb), 0)
    return found


def _linux_titles() -> list[tuple[int, str]]:
    """(pid, title) via wmctrl, if it happens to be installed."""
    import shutil as _sh
    import subprocess

    if not _sh.which("wmctrl"):
        return []
    try:
        out = subprocess.run(["wmctrl", "-lp"], capture_output=True, text=True,
                             timeout=3).stdout
    except Exception:
        return []
    rows = []
    for line in out.splitlines():
        parts = line.split(None, 4)
        if len(parts) < 5:
            continue
        try:
            rows.append((int(parts[2]), parts[4]))
        except ValueError:
            continue
    return rows


def list_chat_windows(sampler: Sampler) -> list[ChatWindow]:
    """Every open chat window, newest usage attached."""
    titles: list[tuple[int, str]] = []
    try:
        if IS_WINDOWS:
            titles = _windows_titles()
        elif not IS_MACOS:
            titles = _linux_titles()
    except Exception:
        titles = []

    stats = sampler.last_pid_stats
    chats: dict[int, ChatWindow] = {}

    for pid, title in titles:
        low = title.lower()
        if not any(h in low for h in CHAT_HINTS):
            continue
        if pid not in stats:
            continue
        cpu, mem, disk = stats[pid]
        w = chats.get(pid)
        if w is None:
            chats[pid] = ChatWindow(pid, title, cpu, mem, disk)
        elif len(title) > len(w.title):
            w.title = title

    if chats:
        return sorted(chats.values(), key=lambda w: w.cpu, reverse=True)

    # Fallback: no window titles available — meter the chat app's processes.
    for proc in psutil.process_iter(["pid", "name"]):
        name = (proc.info["name"] or "").lower().removesuffix(".exe")
        if not any(h in name for h in CHAT_PROC_HINTS):
            continue
        pid = proc.info["pid"]
        if pid not in stats:
            continue
        cpu, mem, disk = stats[pid]
        chats[pid] = ChatWindow(pid, f"{proc.info['name']} · pid {pid}", cpu, mem, disk)

    return sorted(chats.values(), key=lambda w: w.cpu, reverse=True)


# ------------------------------------------------------------ throttling ----
class Throttler:
    """Applies and fully reverses OS-level slowdowns."""

    def __init__(self) -> None:
        self.ncpu = psutil.cpu_count(logical=True) or 1
        self.original: dict[int, dict] = {}   # pid -> {nice, affinity}
        self.applied: dict[str, int] = {}     # app key -> level
        self.app_pids: dict[str, list[int]] = {}
        self._choked: set[int] = set()
        self._lock = threading.Lock()
        self._duty_stop = threading.Event()
        self._duty_thread: threading.Thread | None = None
        atexit.register(self.restore_all)

    # -- priority helpers ----------------------------------------------------
    def _low_nice(self, level: int):
        if IS_WINDOWS:
            if level == EASE:
                return psutil.BELOW_NORMAL_PRIORITY_CLASS
            return psutil.IDLE_PRIORITY_CLASS
        return 10 if level == EASE else 19

    def _core_mask(self, level: int) -> list[int] | None:
        share = LEVELS[level]["cores"]
        keep = 1 if share == 0 else max(1, int(round(self.ncpu * share)))
        if keep >= self.ncpu:
            return None
        return list(range(keep))

    # -- public --------------------------------------------------------------
    def apply(self, key: str, pids: list[int], level: int) -> tuple[int, list[str]]:
        """Throttle every pid of an app. Returns (count_ok, errors)."""
        if key in PROTECTED:
            return 0, [f"{key} is a system process — refusing to touch it"]

        ok, errors = 0, []
        mask = self._core_mask(level)
        nice = self._low_nice(level)

        for pid in pids:
            try:
                proc = psutil.Process(pid)
                with self._lock:
                    if pid not in self.original:
                        snap = {"nice": None, "affinity": None}
                        try:
                            snap["nice"] = proc.nice()
                        except Exception:
                            pass
                        try:
                            snap["affinity"] = proc.cpu_affinity()
                        except Exception:
                            pass
                        self.original[pid] = snap
                try:
                    proc.nice(nice)
                except Exception as exc:
                    errors.append(f"pid {pid}: priority — {exc.__class__.__name__}")
                if mask is not None:
                    try:
                        proc.cpu_affinity(mask)
                    except Exception:
                        pass  # unsupported on macOS; priority still applied
                ok += 1
            except psutil.NoSuchProcess:
                continue
            except psutil.AccessDenied:
                errors.append(f"pid {pid}: access denied — run as admin to throttle it")
            except Exception as exc:
                errors.append(f"pid {pid}: {exc.__class__.__name__}")

        if ok:
            with self._lock:
                self.applied[key] = level
                self.app_pids[key] = list(pids)
                if LEVELS[level]["duty"]:
                    self._choked.update(pids)
                else:
                    self._choked.difference_update(pids)
            self._sync_duty(level)
        return ok, errors

    def restore(self, key: str) -> int:
        with self._lock:
            pids = self.app_pids.pop(key, [])
            self.applied.pop(key, None)
            self._choked.difference_update(pids)
        return self._restore_pids(pids)

    def restore_all(self) -> int:
        with self._lock:
            pids = sorted(self.original)
            self.applied.clear()
            self.app_pids.clear()
            self._choked.clear()
        self._duty_stop.set()
        return self._restore_pids(pids)

    def _restore_pids(self, pids: list[int]) -> int:
        restored = 0
        for pid in pids:
            with self._lock:
                snap = self.original.pop(pid, None)
            if snap is None:
                continue
            try:
                proc = psutil.Process(pid)
                try:
                    proc.resume()  # undo any duty-cycle pause
                except Exception:
                    pass
                if snap["nice"] is not None:
                    try:
                        proc.nice(snap["nice"])
                    except Exception:
                        pass
                if snap["affinity"]:
                    try:
                        proc.cpu_affinity(snap["affinity"])
                    except Exception:
                        pass
                restored += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return restored

    # -- duty cycling --------------------------------------------------------
    def _sync_duty(self, level: int) -> None:
        if not self._choked:
            self._duty_stop.set()
            return
        if self._duty_thread and self._duty_thread.is_alive():
            return
        self._duty_stop = threading.Event()
        on, off = LEVELS[CHOKE]["duty"]
        self._duty_thread = threading.Thread(
            target=self._duty_loop, args=(on, off), daemon=True, name="rg-duty"
        )
        self._duty_thread.start()

    def _duty_loop(self, on: float, off: float) -> None:
        try:
            while not self._duty_stop.is_set():
                with self._lock:
                    pids = list(self._choked)
                if not pids:
                    break
                for pid in pids:
                    try:
                        psutil.Process(pid).suspend()
                    except Exception:
                        continue
                self._duty_stop.wait(off)
                for pid in pids:
                    try:
                        psutil.Process(pid).resume()
                    except Exception:
                        continue
                self._duty_stop.wait(on)
        finally:
            # never leave anything frozen
            with self._lock:
                pids = list(self._choked)
            for pid in pids:
                try:
                    psutil.Process(pid).resume()
                except Exception:
                    continue


# ---------------------------------------------------------------- colors ----
def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def mix(fg: str, bg: str, t: float) -> str:
    """t=1 -> fg, t=0 -> bg."""
    fr, fg_, fb = _hex_to_rgb(fg)
    br, bg_, bb = _hex_to_rgb(bg)
    r = round(br + (fr - br) * t)
    g = round(bg_ + (fg_ - bg_) * t)
    b = round(bb + (fb - bb) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


# ------------------------------------------------------------------- CLI ----
def unfreeze_all() -> int:
    """Safety valve: resume anything left suspended (e.g. if CHOKE was
    interrupted by a hard kill that no handler can catch)."""
    freed = 0
    for proc in psutil.process_iter(["pid", "name", "status"]):
        try:
            if proc.info["status"] != psutil.STATUS_STOPPED:
                continue
            proc.resume()
            print(f"  resumed {proc.info['name']} (pid {proc.info['pid']})")
            freed += 1
        except Exception:
            continue
    print(f"{freed} process(es) resumed." if freed else "Nothing was frozen.")
    return 0


def run_once(top_n: int, interval: float) -> int:
    sampler = Sampler()
    print(f"{APP_NAME} — sampling {interval:.1f}s ...")
    time.sleep(interval)
    entities = sampler.sample()
    vm = psutil.virtual_memory()
    print(
        f"\nmachine: {sampler.ncpu} cores | CPU {psutil.cpu_percent():.0f}% | "
        f"RAM {vm.percent:.0f}% of {vm.total / 1024**3:.0f} GB\n"
    )
    for metric, title, _ in METRICS:
        print(f"  {title}")
        rows = Sampler.top(entities, metric, top_n)
        if not rows:
            print("    (nothing measurable)")
        for i, e in enumerate(rows, 1):
            flag = "  [system]" if e.protected else ""
            print(
                f"    {i}. {e.label[:28]:<28} {e.readout(metric):>10}"
                f"  x{len(e.pids)} proc{flag}"
            )
        print()
    return 0


# ------------------------------------------------------------------- GUI ----
def run_gui(cfg: dict, meters_only: bool = False) -> int:
    import tkinter as tk
    from tkinter import font as tkfont

    try:
        root = tk.Tk()
    except Exception as exc:
        print(f"No desktop display available ({exc}). Try: python resource_guard.py --once")
        return 1

    sampler = Sampler()
    throttler = Throttler()

    # ---- fonts ----
    families = set(tkfont.families(root))
    def pick(*names: str) -> str:
        for n in names:
            if n in families:
                return n
        return "TkDefaultFont"

    UI = pick("Segoe UI", "Inter", "Helvetica Neue", "DejaVu Sans", "Arial")
    MONO = pick("Consolas", "Menlo", "DejaVu Sans Mono", "Courier New")

    F_TITLE = (UI, 20, "bold")
    F_EYE = (UI, 9, "bold")
    F_H = (UI, 11, "bold")
    F_BODY = (UI, 10)
    F_SMALL = (UI, 9)
    F_BIG = (UI, 34, "bold")
    F_MONO = (MONO, 9)

    # ---- state ----
    state = {
        "metric": "cpu",
        "entities": [],
        "rows": [],
        "selected": None,     # app key
        "level": cfg["auto_level"],
        "phase": 0.0,
        "strikes": {},        # key -> consecutive samples over the line
        "alerted": {},        # key -> monotonic ts of last popup
        "alert_win": None,
        "meter_win": None,
        "meter_canvas": None,
        "chat_rows": [],      # ChatWindow list, refreshed every tick
        "chat_hist": {},      # chat key -> per-second history
        "meters_only": meters_only,
    }

    root.title(APP_NAME)
    root.configure(bg=BG)
    root.geometry("1060x736")
    root.minsize(940, 660)

    def threshold_for(metric: str) -> float:
        return cfg[{"cpu": "cpu_threshold", "mem": "mem_threshold", "disk": "disk_threshold"}[metric]]

    # ------------------------------------------------------------ widgets ---
    def panel(parent, **kw):
        return tk.Frame(parent, bg=PANEL, highlightbackground=LINE,
                        highlightthickness=1, **kw)

    header = tk.Frame(root, bg=BG)
    header.pack(fill="x", padx=18, pady=(16, 6))

    tk.Label(header, text="👁  RESOURCE", font=F_TITLE, fg=INK, bg=BG).pack(side="left")
    tk.Label(header, text="GUARD", font=F_TITLE, fg=ORANGE, bg=BG).pack(side="left", padx=(6, 0))
    tk.Label(header, text="  WHO'S STEALING RIGHT NOW", font=F_EYE, fg=PURPLE2, bg=BG).pack(
        side="left", padx=(14, 0), pady=(8, 0)
    )

    sys_label = tk.Label(header, text="", font=F_SMALL, fg=MUTED, bg=BG, justify="right")
    sys_label.pack(side="right")

    # metric tabs
    tabs = tk.Frame(root, bg=BG)
    tabs.pack(fill="x", padx=18, pady=(2, 10))
    tab_buttons: dict[str, tk.Label] = {}

    def set_metric(m: str):
        state["metric"] = m
        for key, btn in tab_buttons.items():
            on = key == m
            btn.configure(
                fg=BG if on else MUTED,
                bg=ORANGE if on else PANEL2,
            )
        refresh_ui()

    for metric, title, _unit in METRICS:
        b = tk.Label(tabs, text=f"  {title}  ", font=F_H, fg=MUTED, bg=PANEL2,
                     padx=12, pady=6, cursor="hand2")
        b.pack(side="left", padx=(0, 8))
        b.bind("<Button-1>", lambda _e, m=metric: set_metric(m))
        tab_buttons[metric] = b

    hint = tk.Label(tabs, text="click any bar to pick a target", font=F_SMALL,
                    fg=DIM, bg=BG)
    hint.pack(side="left", padx=(10, 0))

    meters_btn = tk.Label(tabs, text="  ◧  CHAT METERS  ", font=F_H, fg=BG,
                          bg=PURPLE2, padx=6, pady=6, cursor="hand2")
    meters_btn.pack(side="right")
    meters_btn.bind("<Button-1>", lambda _e: open_meters())

    # main body: donut | bars
    body = tk.Frame(root, bg=BG)
    body.pack(fill="both", expand=True, padx=18)

    donut_wrap = panel(body)
    donut_wrap.pack(side="left", fill="both", padx=(0, 12))
    donut = tk.Canvas(donut_wrap, width=372, height=372, bg=PANEL,
                      highlightthickness=0)
    donut.pack(padx=10, pady=10)

    bars_wrap = panel(body)
    bars_wrap.pack(side="left", fill="both", expand=True)
    bars = tk.Canvas(bars_wrap, bg=PANEL, highlightthickness=0, height=372)
    bars.pack(fill="both", expand=True, padx=10, pady=10)

    # controls
    controls = panel(root)
    controls.pack(fill="x", padx=18, pady=(12, 0))

    crow1 = tk.Frame(controls, bg=PANEL)
    crow1.pack(fill="x", padx=12, pady=(10, 4))

    tk.Label(crow1, text="THROTTLE STRENGTH", font=F_EYE, fg=PURPLE2, bg=PANEL).pack(
        side="left", padx=(0, 10)
    )

    level_buttons: dict[int, tk.Label] = {}

    def set_level(lv: int):
        state["level"] = lv
        cfg["auto_level"] = lv if lv != CHOKE else HEAVY  # never auto-choke
        for key, btn in level_buttons.items():
            on = key == lv
            btn.configure(bg=LEVELS[key]["color"] if on else PANEL2,
                          fg=BG if on else MUTED)
        blurb.configure(text=LEVELS[lv]["blurb"], fg=LEVELS[lv]["color"])

    for lv in (EASE, SLOW, HEAVY, CHOKE):
        b = tk.Label(crow1, text=f" {LEVELS[lv]['name']} ", font=F_H, fg=MUTED,
                     bg=PANEL2, padx=10, pady=5, cursor="hand2")
        b.pack(side="left", padx=(0, 6))
        b.bind("<Button-1>", lambda _e, v=lv: set_level(v))
        level_buttons[lv] = b

    crow2 = tk.Frame(controls, bg=PANEL)
    crow2.pack(fill="x", padx=12, pady=(4, 12))

    def big_button(parent, text, color, cmd, width=22):
        b = tk.Button(parent, text=text, command=cmd, font=(UI, 11, "bold"),
                      fg=BG, bg=color, activebackground=mix(color, INK, 0.75),
                      activeforeground=BG, relief="flat", bd=0, padx=10, pady=9,
                      cursor="hand2", width=width)
        return b

    slow_btn = big_button(crow2, "⏬  SLOW THIS DOWN", ORANGE, lambda: throttle_selected())
    slow_btn.pack(side="left")

    restore_btn = big_button(crow2, "↺  RESTORE", GREEN, lambda: restore_selected(), width=14)
    restore_btn.pack(side="left", padx=(8, 0))

    restore_all_btn = big_button(crow2, "↺  RESTORE EVERYTHING", PURPLE2,
                                 lambda: restore_all(), width=22)
    restore_all_btn.pack(side="left", padx=(8, 0))

    blurb = tk.Label(crow2, text="", font=F_SMALL, fg=MUTED, bg=PANEL)
    blurb.pack(side="right", padx=(12, 4))

    auto_var = tk.BooleanVar(value=cfg["auto_manage"])

    def toggle_auto():
        cfg["auto_manage"] = auto_var.get()
        log(f"auto-manage {'ON' if cfg['auto_manage'] else 'OFF'}", PURPLE2)

    auto_chk = tk.Checkbutton(
        crow1, text=" AUTO-MANAGE HOGS", variable=auto_var, command=toggle_auto,
        font=F_H, fg=GREEN, bg=PANEL, activebackground=PANEL, activeforeground=GREEN,
        selectcolor=PANEL2, highlightthickness=0, bd=0, cursor="hand2",
    )
    auto_chk.pack(side="right")

    top_var = tk.BooleanVar(value=cfg["always_on_top"])

    def toggle_top():
        cfg["always_on_top"] = top_var.get()
        root.attributes("-topmost", cfg["always_on_top"])

    tk.Checkbutton(
        crow1, text=" ALWAYS ON TOP", variable=top_var, command=toggle_top,
        font=F_SMALL, fg=MUTED, bg=PANEL, activebackground=PANEL,
        activeforeground=MUTED, selectcolor=PANEL2, highlightthickness=0, bd=0,
        cursor="hand2",
    ).pack(side="right", padx=(0, 14))

    # log
    log_wrap = panel(root)
    log_wrap.pack(fill="x", padx=18, pady=(10, 16))
    log_box = tk.Text(log_wrap, height=5, bg=PANEL, fg=MUTED, font=F_MONO,
                      relief="flat", highlightthickness=0, wrap="word",
                      padx=10, pady=8)
    log_box.pack(fill="x")
    log_box.configure(state="disabled")
    for tag, color in (("ok", GREEN), ("warn", GOLD), ("hot", HOT),
                       ("info", MUTED), ("purple", PURPLE2)):
        log_box.tag_configure(tag, foreground=color)

    _tag_for = {GREEN: "ok", GOLD: "warn", HOT: "hot", MUTED: "info", PURPLE2: "purple"}

    def log(msg: str, color: str = MUTED):
        stamp = time.strftime("%H:%M:%S")
        log_box.configure(state="normal")
        log_box.insert("1.0", f"{stamp}  {msg}\n", _tag_for.get(color, "info"))
        log_box.delete("60.0", "end")
        log_box.configure(state="disabled")

    # ------------------------------------------------------------ drawing ---
    def draw_donut():
        metric = state["metric"]
        rows = state["rows"]
        donut.delete("all")
        w = int(donut["width"])
        cx = cy = w / 2
        r_out = w / 2 - 26
        ring = 30

        # backing track
        donut.create_oval(cx - r_out, cy - r_out, cx + r_out, cy + r_out,
                          outline=mix(LINE, PANEL, 0.9), width=ring)

        # spinning tick ring — shows the sampler is alive
        state["phase"] = (state["phase"] + 2.4) % 360
        for i in range(60):
            ang = math.radians(state["phase"] + i * 6)
            r1 = r_out + 12
            r2 = r_out + (18 if i % 5 == 0 else 15)
            fade = 0.10 + 0.5 * (i / 60)
            donut.create_line(
                cx + r1 * math.cos(ang), cy - r1 * math.sin(ang),
                cx + r2 * math.cos(ang), cy - r2 * math.sin(ang),
                fill=mix(PURPLE2, PANEL, fade), width=2,
            )

        scale_total = 100.0 if metric in ("cpu", "mem") else None
        used = sum(e.value(metric) for e in rows)
        total = scale_total if scale_total else max(used, 0.0001)
        if scale_total and used > scale_total:
            total = used

        start = 90.0
        box = (cx - r_out, cy - r_out, cx + r_out, cy + r_out)
        for i, e in enumerate(rows):
            frac = e.value(metric) / total
            extent = -frac * 360.0
            if abs(extent) < 0.4:
                continue
            color = SERIES[i % len(SERIES)]
            hot = throttler.applied.get(e.key)
            # glow
            donut.create_arc(*box, start=start, extent=extent, style="arc",
                             outline=mix(color, PANEL, 0.22), width=ring + 12)
            donut.create_arc(*box, start=start, extent=extent, style="arc",
                             outline=color, width=ring if i else ring + 5)
            if hot:
                donut.create_arc(*box, start=start, extent=extent, style="arc",
                                 outline=BG, width=3)
            start += extent

        if scale_total and used < scale_total:
            donut.create_arc(*box, start=start, extent=-(scale_total - used) / total * 360.0,
                             style="arc", outline=mix(DIM, PANEL, 0.30), width=ring - 8)

        # center readout
        title = dict((m, t) for m, t, _ in METRICS)[metric]
        unit = dict((m, u) for m, _, u in METRICS)[metric]
        donut.create_text(cx, cy - 46, text=title, font=F_EYE, fill=PURPLE2)
        if rows:
            lead = rows[0]
            donut.create_text(cx, cy - 6, text=lead.readout(metric), font=F_BIG,
                              fill=SERIES[0])
            label = lead.label if len(lead.label) <= 20 else lead.label[:19] + "…"
            donut.create_text(cx, cy + 30, text=label.upper(), font=F_H, fill=INK)
            over = lead.value(metric) >= threshold_for(metric)
            donut.create_text(
                cx, cy + 52,
                text=("OVER THE LINE" if over else "within limits"),
                font=F_SMALL, fill=HOT if over else DIM,
            )
            donut.create_text(cx, cy + 74,
                              text=f"{len(lead.pids)} process{'es' if len(lead.pids) != 1 else ''}",
                              font=F_SMALL, fill=DIM)
        else:
            donut.create_text(cx, cy, text=f"idle ({unit})", font=F_H, fill=DIM)

    def draw_bars():
        metric = state["metric"]
        rows = state["rows"]
        bars.delete("all")
        w = max(bars.winfo_width(), 420)
        row_h = 42
        pad = 8
        max_val = max([e.value(metric) for e in rows], default=1.0) or 1.0
        thresh = threshold_for(metric)

        bars.create_text(14, 12, text="TOP CONSUMERS", font=F_EYE, fill=PURPLE2,
                         anchor="w")
        bars.create_text(w - 14, 12, text="click to target", font=F_SMALL,
                         fill=DIM, anchor="e")

        y = 30
        for i, e in enumerate(rows):
            color = SERIES[i % len(SERIES)]
            selected = state["selected"] == e.key
            lv = throttler.applied.get(e.key)

            if selected:
                bars.create_rectangle(6, y - 2, w - 6, y + row_h - 6,
                                      fill=PANEL2, outline=mix(color, PANEL, 0.6))

            bars.create_rectangle(14, y + 4, 22, y + 20, fill=color, outline="")
            name = e.label if len(e.label) <= 26 else e.label[:25] + "…"
            bars.create_text(32, y + 12, text=name, font=F_H, fill=INK, anchor="w")

            meta = f"{len(e.pids)}×"
            if e.protected:
                meta += "  system"
            if lv:
                meta += f"  ▼ {LEVELS[lv]['name']}"
            bars.create_text(w - 16, y + 12, text=f"{e.readout(metric)}   {meta}",
                             font=F_SMALL, fill=LEVELS[lv]["color"] if lv else MUTED,
                             anchor="e")

            # bar
            bx0, bx1 = 32, w - 16
            by = y + 26
            bars.create_rectangle(bx0, by, bx1, by + 8, fill=PANEL2, outline="")
            frac = min(e.value(metric) / max_val, 1.0)
            bw = (bx1 - bx0) * frac
            if bw > 2:
                bars.create_rectangle(bx0, by, bx0 + bw, by + 8,
                                      fill=mix(color, PANEL, 0.35), outline="")
                bars.create_rectangle(bx0, by + 2, bx0 + bw, by + 6, fill=color,
                                      outline="")
            # threshold marker
            if max_val > 0 and thresh <= max_val:
                tx = bx0 + (bx1 - bx0) * (thresh / max_val)
                bars.create_line(tx, by - 3, tx, by + 11, fill=HOT, width=1,
                                 dash=(2, 2))
            y += row_h + pad // 2

        if not rows:
            bars.create_text(w / 2, 120, text="nothing is using anything right now",
                             font=F_BODY, fill=DIM)

        bars.configure(scrollregion=(0, 0, w, y))

    def on_bars_click(event):
        rows = state["rows"]
        idx = int((event.y - 30) // (42 + 4))
        if 0 <= idx < len(rows):
            state["selected"] = rows[idx].key
            draw_bars()
            update_buttons()

    bars.bind("<Button-1>", on_bars_click)

    def selected_entity() -> Entity | None:
        key = state["selected"]
        if not key:
            return None
        for e in state["entities"]:
            if e.key == key:
                return e
        return None

    def update_buttons():
        e = selected_entity()
        if e is None:
            slow_btn.configure(text="⏬  SLOW THIS DOWN", state="disabled",
                               bg=mix(ORANGE, PANEL, 0.35))
            restore_btn.configure(state="disabled", bg=mix(GREEN, PANEL, 0.35))
            return
        short = e.label if len(e.label) <= 14 else e.label[:13] + "…"
        if e.protected:
            slow_btn.configure(text=f"🔒  {short.upper()} IS SYSTEM", state="disabled",
                               bg=mix(DIM, PANEL, 0.5))
        else:
            slow_btn.configure(text=f"⏬  SLOW {short.upper()}", state="normal", bg=ORANGE)
        on = e.key in throttler.applied
        restore_btn.configure(state="normal" if on else "disabled",
                              bg=GREEN if on else mix(GREEN, PANEL, 0.35))

    # ---------------------------------------------------------- throttling --
    def throttle_entity(e: Entity, level: int, auto: bool = False) -> None:
        ok, errors = throttler.apply(e.key, e.pids, level)
        tag = "auto" if auto else "manual"
        if ok:
            log(f"[{tag}] {e.label} → {LEVELS[level]['name']} on {ok} process(es)",
                LEVELS[level]["color"])
        for err in errors[:3]:
            log(f"  {e.label}: {err}", GOLD)
        if not ok and not errors:
            log(f"{e.label} vanished before it could be throttled", MUTED)
        update_buttons()
        draw_bars()

    def throttle_selected():
        e = selected_entity()
        if e is None:
            return
        throttle_entity(e, state["level"])

    def restore_selected():
        e = selected_entity()
        if e is None:
            return
        n = throttler.restore(e.key)
        log(f"restored {e.label} ({n} process(es)) to normal", GREEN)
        state["strikes"].pop(e.key, None)
        update_buttons()
        draw_bars()

    def restore_all():
        n = throttler.restore_all()
        state["strikes"].clear()
        log(f"restored everything — {n} process(es) back to normal", GREEN)
        update_buttons()
        draw_bars()

    # -------------------------------------------------------- alert window --
    def close_alert():
        win = state["alert_win"]
        state["alert_win"] = None
        if win is not None:
            try:
                win.destroy()
            except Exception:
                pass

    def pop_alert(e: Entity, metric: str, auto_level: int | None):
        close_alert()
        win = tk.Toplevel(root)
        state["alert_win"] = win
        win.title(f"{APP_NAME} — {e.label} is stealing")
        win.configure(bg=BG)
        w_, h_ = 560, 470
        sx = root.winfo_screenwidth() // 2 - w_ // 2
        sy = max(40, root.winfo_screenheight() // 2 - h_ // 2 - 40)
        win.geometry(f"{w_}x{h_}+{sx}+{sy}")
        win.resizable(False, False)
        win.protocol("WM_DELETE_WINDOW", close_alert)

        # bring it to the front of the desktop, then let it be normal
        win.attributes("-topmost", True)
        win.after(1200, lambda: win.winfo_exists() and win.attributes("-topmost", False))
        try:
            win.lift()
            win.focus_force()
        except Exception:
            pass

        title = dict((m, t) for m, t, _ in METRICS)[metric]
        thresh = threshold_for(metric)
        val = e.value(metric)

        tk.Label(win, text="⚠  RESOURCE THEFT", font=(UI, 10, "bold"), fg=HOT,
                 bg=BG).pack(pady=(16, 2))
        tk.Label(win, text=e.label, font=(UI, 22, "bold"), fg=INK, bg=BG).pack()
        tk.Label(
            win,
            text=f"{title} {e.readout(metric)}  ·  limit {thresh:g}"
                 f"{'%' if metric != 'disk' else ' MB/s'}  ·  {len(e.pids)} process(es)",
            font=F_SMALL, fg=MUTED, bg=BG,
        ).pack(pady=(4, 8))

        gauge = tk.Canvas(win, width=300, height=190, bg=BG, highlightthickness=0)
        gauge.pack()

        cx, cy, r = 150, 150, 108
        over = min(val / max(thresh, 0.001), 2.0)
        span = 180.0 * min(over / 2.0, 1.0)
        gauge.create_arc(cx - r, cy - r, cx + r, cy + r, start=0, extent=180,
                         style="arc", outline=mix(LINE, BG, 0.9), width=26)
        seg_colors = [GREEN, GOLD, ORANGE, HOT]
        steps = 48
        for s in range(steps):
            frac = s / steps
            if frac * 180 > span:
                break
            color = seg_colors[min(int(frac * len(seg_colors)), len(seg_colors) - 1)]
            gauge.create_arc(cx - r, cy - r, cx + r, cy + r,
                             start=180 - frac * 180 - (180 / steps),
                             extent=180 / steps + 1, style="arc",
                             outline=mix(color, BG, 0.28), width=34)
            gauge.create_arc(cx - r, cy - r, cx + r, cy + r,
                             start=180 - frac * 180 - (180 / steps),
                             extent=180 / steps + 1, style="arc",
                             outline=color, width=24)
        # tapered needle
        ang = math.radians(180 - span)
        tip = (cx + (r - 30) * math.cos(ang), cy - (r - 30) * math.sin(ang))
        side = ang + math.pi / 2
        base = 7
        gauge.create_polygon(
            cx + base * math.cos(side), cy - base * math.sin(side),
            cx - base * math.cos(side), cy + base * math.sin(side),
            tip[0], tip[1],
            fill=INK, outline="",
        )
        gauge.create_oval(cx - 11, cy - 11, cx + 11, cy + 11, fill=INK, outline="")
        gauge.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill=BG, outline="")
        gauge.create_text(cx, cy - 52, text=e.readout(metric), font=(UI, 26, "bold"),
                          fill=HOT if val >= thresh else GOLD)
        gauge.create_text(cx, cy - 24, text=f"{over * 100:.0f}% of your limit",
                          font=F_SMALL, fill=MUTED)

        if auto_level:
            tk.Label(win, text=f"auto-managed → {LEVELS[auto_level]['name']} already applied",
                     font=F_SMALL, fg=LEVELS[auto_level]["color"], bg=BG).pack(pady=(2, 0))

        btns = tk.Frame(win, bg=BG)
        btns.pack(pady=(14, 0))

        def do_slow():
            throttle_entity(e, state["level"])
            close_alert()

        def do_harder():
            harder = min(state["level"] + 1, CHOKE)
            set_level(harder)
            throttle_entity(e, harder)
            close_alert()

        def do_ignore():
            if e.key not in cfg["allowlist"]:
                cfg["allowlist"].append(e.key)
            state["strikes"].pop(e.key, None)
            log(f"{e.label} added to the leave-it-alone list", PURPLE2)
            close_alert()

        tk.Button(btns, text=f"⏬  SLOW IT DOWN  ({LEVELS[state['level']]['name']})",
                  command=do_slow, font=(UI, 12, "bold"), fg=BG, bg=ORANGE,
                  activebackground=mix(ORANGE, INK, 0.75), activeforeground=BG,
                  relief="flat", bd=0, padx=18, pady=11, cursor="hand2").pack(side="left")
        tk.Button(btns, text="⏬⏬  HARDER", command=do_harder, font=(UI, 11, "bold"),
                  fg=BG, bg=HOT, activebackground=mix(HOT, INK, 0.75),
                  activeforeground=BG, relief="flat", bd=0, padx=14, pady=11,
                  cursor="hand2").pack(side="left", padx=(8, 0))

        tail = tk.Frame(win, bg=BG)
        tail.pack(pady=(10, 0))
        tk.Button(tail, text="leave it alone", command=do_ignore, font=F_SMALL,
                  fg=MUTED, bg=PANEL2, activebackground=PANEL, activeforeground=INK,
                  relief="flat", bd=0, padx=12, pady=6, cursor="hand2").pack(side="left")
        tk.Button(tail, text="dismiss", command=close_alert, font=F_SMALL, fg=MUTED,
                  bg=PANEL2, activebackground=PANEL, activeforeground=INK,
                  relief="flat", bd=0, padx=12, pady=6, cursor="hand2").pack(
            side="left", padx=(8, 0))

    # --------------------------------------------------------- chat meters --
    METER_W = 430
    METER_ROW = 58
    SPARK = 44  # samples of history kept per chat

    def meter_color(cpu: float) -> str:
        if cpu < 8:
            return GREEN
        if cpu < 20:
            return GOLD
        if cpu < 40:
            return ORANGE
        return HOT

    def close_meters():
        win = state["meter_win"]
        state["meter_win"] = None
        state["meter_canvas"] = None
        if win is not None:
            try:
                win.destroy()
            except Exception:
                pass
        if state.get("meters_only"):
            on_close()

    def open_meters():
        if state["meter_win"] is not None:
            try:
                state["meter_win"].lift()
                return
            except Exception:
                pass
        win = tk.Toplevel(root)
        state["meter_win"] = win
        win.title("CHAT METERS")
        win.configure(bg=BG)
        win.attributes("-topmost", True)
        sx = root.winfo_screenwidth() - METER_W - 40
        win.geometry(f"{METER_W}x{METER_ROW * 4 + 96}+{max(0, sx)}+60")
        win.minsize(METER_W, 200)
        win.protocol("WM_DELETE_WINDOW", close_meters)
        cv = tk.Canvas(win, bg=BG, highlightthickness=0)
        cv.pack(fill="both", expand=True)
        state["meter_canvas"] = cv
        cv.bind("<Button-1>", on_meter_click)
        draw_meters()

    def on_meter_click(event):
        rows = state["chat_rows"]
        idx = int((event.y - 54) // METER_ROW)
        if not (0 <= idx < len(rows)):
            return
        chat = rows[idx]
        key = f"chat:{chat.pid}"
        if key in throttler.applied:
            throttler.restore(key)
            log(f"restored chat “{chat.short}” to normal", GREEN)
        else:
            ok, errors = throttler.apply(key, [chat.pid], state["level"])
            if ok:
                log(f"chat “{chat.short}” → {LEVELS[state['level']]['name']}",
                    LEVELS[state["level"]]["color"])
            for err in errors[:2]:
                log(f"  {err}", GOLD)
        draw_meters()

    def draw_meters():
        cv = state.get("meter_canvas")
        if cv is None:
            return
        rows = state["chat_rows"]
        hist = state["chat_hist"]
        cv.delete("all")
        w = max(cv.winfo_width(), METER_W)

        cv.create_text(14, 16, text="LIVE CHAT METERS", font=F_EYE, fill=PURPLE2,
                       anchor="w")
        cv.create_text(w - 14, 16, text="usage per second", font=F_SMALL, fill=DIM,
                       anchor="e")
        total = sum(c.cpu for c in rows)
        cv.create_text(14, 36, text=f"{len(rows)} open · {total:.1f}% of the machine",
                       font=F_SMALL, fill=MUTED, anchor="w")
        cv.create_line(10, 48, w - 10, 48, fill=LINE)

        y = 54
        for chat in rows:
            key = f"chat:{chat.pid}"
            lv = throttler.applied.get(key)
            color = LEVELS[lv]["color"] if lv else meter_color(chat.cpu)

            cv.create_text(14, y + 12, text=chat.short, font=F_H, fill=INK, anchor="w")
            cv.create_text(w - 62, y + 12, text=f"{chat.cpu:.1f} %/s", font=F_H,
                           fill=color, anchor="e")

            chip_x0 = w - 56
            chip = "RESET" if lv else "SLOW"
            cv.create_rectangle(chip_x0, y + 3, w - 12, y + 21,
                                fill=mix(color, BG, 0.22), outline=color)
            cv.create_text((chip_x0 + w - 12) / 2, y + 12, text=chip, font=F_SMALL,
                           fill=color)

            # the meter itself
            bx0, bx1, by = 14, w - 14, y + 26
            cv.create_rectangle(bx0, by, bx1, by + 10, fill=PANEL, outline="")
            frac = min(chat.cpu / 50.0, 1.0)  # 50% of the machine = full bar
            bw = (bx1 - bx0) * frac
            if bw > 2:
                cv.create_rectangle(bx0, by, bx0 + bw, by + 10,
                                    fill=mix(color, BG, 0.35), outline="")
                cv.create_rectangle(bx0, by + 2, bx0 + bw, by + 8, fill=color,
                                    outline="")

            # per-second history
            series = hist.get(key, [])
            if len(series) > 1:
                peak = max(max(series), 5.0)
                sx0 = bx0 + (bx1 - bx0) * 0.42   # right half only — meta text sits left
                step = (bx1 - sx0) / (SPARK - 1)
                pts = []
                for i, v in enumerate(series[-SPARK:]):
                    pts.extend((sx0 + i * step, y + 52 - (v / peak) * 14))
                cv.create_line(*pts, fill=mix(color, BG, 0.75), width=1.5,
                               smooth=True)
                cv.create_line(sx0, y + 53, bx1, y + 53, fill=mix(LINE, BG, 0.8))

            meta = f"{chat.mem_mb:.0f} MB"
            if lv:
                meta += f"   ▼ {LEVELS[lv]['name']}"
            cv.create_text(14, y + 50, text=meta, font=F_SMALL,
                           fill=color if lv else DIM, anchor="w")
            y += METER_ROW

        if not rows:
            cv.create_text(w / 2, 110,
                           text="no chat windows found yet", font=F_BODY, fill=DIM)
            cv.create_text(w / 2, 132,
                           text="open Claude and it shows up here",
                           font=F_SMALL, fill=DIM)

        cv.configure(scrollregion=(0, 0, w, y + 10))

        # grow/shrink the strip to fit however many chats are open
        win = state["meter_win"]
        wanted = max(200, 66 + METER_ROW * max(len(rows), 1))
        if win is not None and abs(win.winfo_height() - wanted) > METER_ROW / 2:
            try:
                win.geometry(f"{win.winfo_width()}x{wanted}")
            except Exception:
                pass

    def update_chats():
        try:
            rows = list_chat_windows(sampler)
        except Exception:
            rows = []
        rows = rows[:8]
        state["chat_rows"] = rows
        hist = state["chat_hist"]
        live = set()
        for chat in rows:
            key = f"chat:{chat.pid}"
            live.add(key)
            series = hist.setdefault(key, [])
            series.append(chat.cpu)
            if len(series) > SPARK:
                del series[:-SPARK]
        for gone in set(hist) - live:
            hist.pop(gone, None)
        if state["meter_win"] is not None:
            draw_meters()

    # ------------------------------------------------------------ hog scan --
    def scan_for_hogs():
        metric = state["metric"]
        now = time.monotonic()
        for e in state["entities"]:
            if e.protected or e.key in cfg["allowlist"]:
                continue
            over_any = any(
                e.value(m) >= threshold_for(m) for m, _t, _u in METRICS
            )
            if not over_any:
                state["strikes"].pop(e.key, None)
                continue
            hits = state["strikes"].get(e.key, 0) + 1
            state["strikes"][e.key] = hits
            if hits < cfg["strikes"]:
                continue
            if e.key in throttler.applied:
                continue  # already handled

            worst = max(METRICS, key=lambda m: e.value(m[0]) / max(threshold_for(m[0]), 0.001))
            worst_metric = worst[0]

            # one alert per app per 90s, however loud it gets
            if now - state["alerted"].get(e.key, 0) <= 90:
                continue
            state["alerted"][e.key] = now

            applied_level = None
            if cfg["auto_manage"]:
                applied_level = min(cfg["auto_level"], HEAVY)  # auto never chokes
                throttle_entity(e, applied_level, auto=True)
            else:
                log(f"{e.label} is over the line on {worst[1]} — {e.readout(worst_metric)}", HOT)
            pop_alert(e, worst_metric, applied_level)

    # ------------------------------------------------------------- refresh --
    def refresh_ui():
        state["rows"] = Sampler.top(state["entities"], state["metric"], 8)
        if state["selected"] is None and state["rows"]:
            state["selected"] = state["rows"][0].key
        draw_donut()
        draw_bars()
        update_buttons()

    def tick():
        try:
            state["entities"] = sampler.sample()
        except Exception as exc:
            log(f"sampler hiccup: {exc.__class__.__name__}", GOLD)
            state["entities"] = []

        vm = psutil.virtual_memory()
        managed = len(throttler.applied)
        sys_label.configure(
            text=(f"{sampler.ncpu} cores   CPU {psutil.cpu_percent():.0f}%   "
                  f"RAM {vm.percent:.0f}% of {vm.total / 1024**3:.0f} GB   "
                  f"throttled: {managed}")
        )
        refresh_ui()
        update_chats()
        scan_for_hogs()
        root.after(int(cfg["interval"] * 1000), tick)

    # ---------------------------------------------------------------- exit --
    def on_close():
        n = throttler.restore_all()
        cfg["auto_manage"] = auto_var.get()
        save_config(cfg)
        if n:
            log(f"restored {n} process(es) on exit", GREEN)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    def on_signal(signum, _frame):
        """Ctrl-C or a kill still puts every process back the way it was."""
        throttler.restore_all()
        try:
            root.destroy()
        except Exception:
            pass
        os._exit(0)

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            signal.signal(sig, on_signal)
        except Exception:
            pass

    set_metric("cpu")
    set_level(cfg["auto_level"])
    root.attributes("-topmost", cfg["always_on_top"])
    log(f"watching {sampler.ncpu} cores — thresholds: CPU {cfg['cpu_threshold']:g}%, "
        f"RAM {cfg['mem_threshold']:g}%, disk {cfg['disk_threshold']:g} MB/s", PURPLE2)
    log("nothing is throttled until you say so (or auto-manage catches a hog)", MUTED)

    if meters_only:
        root.withdraw()
        root.after(700, open_meters)
    root.after(600, tick)
    try:
        root.mainloop()
    finally:
        throttler.restore_all()
    return 0


# ------------------------------------------------------------------ main ----
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=f"{APP_NAME} — find and slow resource hogs")
    parser.add_argument("--once", action="store_true",
                        help="print one snapshot to the terminal and exit (no window)")
    parser.add_argument("--top", type=int, default=8, help="how many apps to show")
    parser.add_argument("--meters", action="store_true",
                        help="just the always-on-top per-chat usage meters")
    parser.add_argument("--unfreeze", action="store_true",
                        help="resume anything left suspended, then exit (panic button)")
    parser.add_argument("--interval", type=float, help="seconds between samples")
    parser.add_argument("--no-auto", action="store_true",
                        help="start with auto-manage off")
    parser.add_argument("--cpu", type=float, help="CPU threshold, %% of the whole machine")
    parser.add_argument("--mem", type=float, help="memory threshold, %% of total RAM")
    parser.add_argument("--disk", type=float, help="disk threshold in MB/s")
    args = parser.parse_args(argv)

    if args.unfreeze:
        return unfreeze_all()

    cfg = load_config()
    if args.interval:
        cfg["interval"] = max(0.5, args.interval)
    if args.no_auto:
        cfg["auto_manage"] = False
    if args.cpu:
        cfg["cpu_threshold"] = args.cpu
    if args.mem:
        cfg["mem_threshold"] = args.mem
    if args.disk:
        cfg["disk_threshold"] = args.disk

    if args.once:
        return run_once(args.top, cfg["interval"])
    return run_gui(cfg, meters_only=args.meters)


if __name__ == "__main__":
    sys.exit(main())
