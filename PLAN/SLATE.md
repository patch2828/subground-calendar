# THE SLATE — Sept 2026 → Feb 2027 (canonical; every doc builds off this)

Locked by Claude 2026-08-26 off `FACTS.md`. Day-of-week verified twice against the Sept 10 = Thursday anchor.
**Dates marked TO BOOK are open dates Claude is proposing, not commitments. Ryan books them.**

| # | Date | Day | Show | Venue (A / fallback B) | Cap | Status |
|---|---|---|---|---|---|---|
| **01** | **Thu Sep 10** | Thu | **GOLD RUSH PRE-PARTY** | M&M lot, Peoria | 1,300 | **LOCKED · PERMITTED · ON SALE** |
| **02** | **Fri Sep 18 or Sat Sep 19** | — | **ICEHOUSE CONTENT NIGHT** | The Icehouse | ~100 | Awaiting Sam · **NOT a revenue event** |
| **03** | **Sat Oct 31** | Sat | **HALLOWEEN** | Fillmore Warehouse / Alchemist's Enclave | 1,000 | **TO BOOK — highest-value open date of the window** |
| **04** | **Fri Nov 6** | Fri | **COMBINE × NORTHERN ROAD** | Fillmore Warehouse / Alchemist's Enclave | 1,000 | Date locked w/ Corson · venue pending Friday rate |
| **05** | **Sat Dec 12** | Sat | **TH3 N3TW0RK NIGHT** (roster showcase) | 600-cap room | 600 | TO BOOK |
| **06** | **Thu Dec 31** | Thu | **NEW YEAR'S EVE** | 1,000-cap | 1,000 | TO BOOK — fattest night of the year |
| **07** | **Sat Jan 23** | Sat | **JANUARY HEADLINE** | 1,000-cap | 1,000 | TO BOOK |
| **08** | **Sat Feb 13** | Sat | **FEBRUARY HEADLINE** (Valentine's weekend) | 1,000-cap | 1,000 | TO BOOK |
| **09** | **Sat Feb 20** | Sat | **DRIVE-IN — GLENDALE 9 TAKEOVER** | Glendale 9 Drive-In | 2,500 | TO BOOK — **the $100K hinge** |

### The recurring layer (runs underneath the slate)
| Series | Cadence | Room | Purpose |
|---|---|---|---|
| **LIGHT HOUSE THURSDAYS** — Fairytail × SubGround | monthly Thursday, from Oct | Light House kava bar, ~100–150 | Cheap, fast, low-risk. Feeds the SMS list and pays small. First real Fairytail joint activation. |

### Floating adds — real pipeline items with no date yet
- **PRESCOTT — RENEGADE / Prototype** (300–500, 2-stage mini fest) — blocked on **Josh (Auxlee, Funky Forest)**. Slot it the moment he answers.
- **CHEBA HUT** — deck already delivered, window passed unlocked. Re-pitch as a Light House-style Thursday.
- **TUNNEL RAVE (Surprise AZ)** — Srija's scouting. Teasers only, **never the location**.
- **PICACHO PEAK** — pack fully built, backburner.

### Hard constraints the slate respects
- **Oct 23–25 = HARD BLACKOUT** (Ryan at F33LZ's We Are Love Friend Festival). Halloween Oct 31 clears it by six days.
- **Oct 9–11 FORM @ Arcosanti is OPTIONAL** — the calendar explicitly marks those dates FREE for shows.
- Radar, Ryan's call, no pitch built: **Whethan @ The Van Buren Sat Nov 7** (0 miles, the night after our Nov 6) and **Whethan @ Shrine LA Fri Dec 4**.

### Why these dates
- **Oct 31 is a SATURDAY.** Halloween on a Saturday happens roughly once every six or seven years. It is the single highest-demand club date of the fall and October is currently empty. Booking it is the largest single swing available in this window.
- **Nov 6 sits the night before Whethan plays The Van Buren.** Out-of-town bass crowd is already in Phoenix and already spending. The afters framing is free money.
- **Dec 31 is a Thursday with Friday Jan 1 a holiday** — people go out and stay out. Double pricing is normal on NYE and nobody blinks.
- **Feb 13 is Valentine's weekend Saturday** — couples pricing, table/2-for pricing, an easy sell.
- **Feb 20 for the Drive-In** — the outdoor window is wide open in Phoenix February, it is clear of monsoon entirely, and it lands after **seven** ticketed shows of track record (01, 03, 04, 05, 06, 07, 08 — 02 Icehouse is free) so the room can actually be filled.

---

## DATE VERIFICATION — run in code, not eyeballed (2026-08-26)

All fifteen dates below were computed with Python's calendar, not estimated:

```
Sep 10 2026 GOLD RUSH        -> Thursday
Sep 18 2026 Icehouse A       -> Friday
Sep 19 2026 Icehouse B       -> Saturday
Oct  9 2026 FORM start       -> Friday
Oct 23 2026 blackout start   -> Friday
Oct 25 2026 blackout end     -> Sunday
Oct 31 2026 HALLOWEEN        -> Saturday
Nov  6 2026 Combine/NR       -> Friday
Nov  7 2026 Whethan PHX      -> Saturday
Dec  4 2026 Whethan LA       -> Friday
Dec 12 2026 N3TWORK          -> Saturday
Dec 31 2026 NYE              -> Thursday
Jan 23 2027 Jan headline     -> Saturday
Feb 13 2027 Feb headline     -> Saturday
Feb 20 2027 DRIVE-IN         -> Saturday
```

**Countdown from 2026-08-26:** Gold Rush T-15 · Halloween T-66 · Combine T-72 · NYE T-127 · Drive-In T-178.
Six months from today lands on **Fri Feb 26 2027**, so the Feb 20 Drive-In is the last show inside the window.

### How rare the Halloween date is
Halloween falls on a Saturday in **2020, 2026, 2037** — three times in the twenty-one years 2020–2040, an average of once every seven years. This is not a normal October date and it should not be priced or promoted like one.

### CORRECTION FOUND — a canonical doc is wrong
The **Aug 21, 2026 "SubGround / Dream Project — Event Calendar" Doc** (`1b_wSnT06odmUTYz8ryDqxjX-IVf97l4LtphqcpjdKW8`) lists the Whethan LA radar hit as **"Sat Dec 4."** **Dec 4, 2026 is a FRIDAY.** Verified two independent ways. The Google Calendar event itself carries only the date, not a day name, so the error is in the Doc's prose. Worth fixing before anyone routes around it — a Friday LA date and a Saturday LA date imply different build-around windows.
