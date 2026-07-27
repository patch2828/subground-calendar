# RESOURCE GUARD

A desktop watchdog that shows what's eating your machine right now and lets you
slow it down with one button. Runs on your computer, not in the cloud.

```
Windows      double-click  run-resource-guard.bat
Chat meters  double-click  run-chat-meters.bat
Mac / Linux  ./run-resource-guard.sh
Terminal     python resource_guard.py
```

Needs Python 3.9+ and `psutil` (the launchers install psutil for you).

---

## The main window

- **Live donut** of the top 8 apps, one color each, plus how much of the machine
  is still free. Tabs switch it between **CPU**, **MEMORY** and **DISK**.
- **Top consumers** list with a bar per app, a dashed red line marking your
  limit, and the process count (Chrome's 30 processes count as one app).
- **THROTTLE STRENGTH** picks how hard the slow-down hits:

  | | what it does |
  |---|---|
  | EASE OFF | low priority, keeps all cores |
  | SLOW | lowest priority, half the cores |
  | HEAVY | lowest priority, a quarter of the cores |
  | CHOKE | one core plus pulsed pauses — hard stop, the app may stutter |

- **SLOW THIS DOWN** applies it to whatever is selected. **RESTORE** puts that
  one back. **RESTORE EVERYTHING** puts everything back.
- **AUTO-MANAGE HOGS** (on by default) throttles anything that stays over your
  limit for 4 samples in a row, by itself. Auto mode never uses CHOKE — that one
  is yours to pull.

## The pop-up

When something crosses the line, a window comes to the front of your desktop
with the offender's name, a colored gauge showing how far over your limit it is,
and four choices: **SLOW IT DOWN**, **HARDER**, **leave it alone** (never bother
you about that app again), or **dismiss**. One pop-up per app per 90 seconds.

## Chat meters

**CHAT METERS** (top-right, or `run-chat-meters.bat`) opens a narrow always-on-top
strip that sits beside your chats. One row per open chat window — Claude,
ChatGPT, Gemini, Copilot, Perplexity, Grok — each with:

- a **live colored meter** of what that chat is using per second — green under 8%
  of the machine, gold to 20%, orange to 40%, red past that
- the number itself (`2.1 %/s`), its memory, and a rolling graph of the last ~44 seconds
- a **SLOW / RESET** chip — click it to throttle that one chat and click again to
  put it back

The strip grows and shrinks as you open and close chats.

Two honest limits:

- It meters the **window**, not the tab. A browser reports one title per window,
  so five Claude tabs in one Chrome window read as one chat. Separate windows
  read separately. Windows titles come from the OS; on Linux it needs `wmctrl`,
  and on macOS it falls back to per-process metering.
- It measures **your computer's** usage — CPU, memory, disk. Claude's token and
  credit burn lives on Anthropic's side and nothing outside the app can read it,
  so no meter here can show it.

## Thresholds and settings

Defaults: CPU 35% of the machine, memory 25% of total RAM, disk 40 MB/s, 4
strikes before acting. Change them per run:

```
python resource_guard.py --cpu 50 --mem 30 --disk 80 --interval 2
python resource_guard.py --no-auto        # watch only, never act on its own
python resource_guard.py --meters         # just the chat meters
python resource_guard.py --once           # one text snapshot, no window
python resource_guard.py --unfreeze       # panic button, see below
```

Settings persist in `~/.resource-guard.json`, including the "leave it alone"
list.

## Safety

- System-critical processes (`svchost`, `dwm`, `lsass`, `explorer`, `systemd`,
  `WindowServer`, …) are refused outright, in every mode.
- Every original priority and core assignment is recorded before anything is
  changed, and restored on RESTORE, on quit, on Ctrl-C, and on kill.
- Nothing is ever killed. Throttling is reversible; closing the app un-does it.
- **CHOKE** works by suspending and resuming the process ~5 times a second. If
  RESOURCE GUARD is force-killed (Task Manager "End task", power loss) during a
  paused slice, that app can be left frozen. Fix it with:
  `python resource_guard.py --unfreeze`
- On Windows, throttling processes owned by another user or running elevated
  needs admin — right-click the .bat and "Run as administrator".

## Tested

CPU-hog processes at 100%: detected, auto-throttled to lowest priority on half
the cores; CHOKE dropped them from 100% to 15%; RESTORE and a SIGTERM kill both
returned them to normal priority, all cores, running. The window-title path for
per-chat metering is Windows API code that this Linux test machine can't
exercise — the per-process fallback is what was verified here.
