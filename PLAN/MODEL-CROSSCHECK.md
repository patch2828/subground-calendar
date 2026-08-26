# MODEL CROSS-CHECK — independent arithmetic (2026-08-26)

Computed by Claude in code, separately from `04-MONEY.md`, so the money model has ground truth to be checked against. **All fill rates and all costs for unbooked shows are ESTIMATES and are labeled as such.** The Gold Rush line uses only real numbers from `FACTS.md`.

## 1. The Gold Rush figures reconcile exactly

```
sellout ticket net   100 x $13.33 + 1200 x $17.78  = $22,669
+ vendors $450 + merch $290                        = $23,409   <- FACTS.md says $23,409  MATCH
- realistic costs $9,779                           = $13,630   <- FACTS.md says ~$13,630 MATCH
breakeven check      100 EB + 475 GA               = $9,778 vs costs $9,779
                                                   -> 575 tickets CONFIRMED to the dollar
```

The fact base is internally consistent. Nothing in the Sept 10 model needs revisiting.

## 2. Six-month net, three scenarios

Shotgun's ~11% is applied to every ticket line. Icehouse is held at a flat −$2,500 and is never allowed to show profit, per Ryan's binding 8/22 correction.

| Show | Cap | CONSERVATIVE | TARGET | SELLOUT |
|---|---:|---:|---:|---:|
| 01 Gold Rush · Sep 10 | 1,300 | $761 | $3,626 | $13,656 |
| 02 Icehouse · Sep 18/19 | — | −$2,500 | −$2,500 | −$2,500 |
| 03 **HALLOWEEN · Oct 31** | 1,000 | $8,162 | $14,852 | $23,215 |
| 04 Combine × NR · Nov 6 | 1,000 | $4,258 | $9,988 | $18,582 |
| 05 TH3 N3TW0RK · Dec 12 | 600 | $1,999 | $4,415 | $7,435 |
| 06 **NYE · Dec 31** | 1,000 | $9,120 | $17,883 | $26,265 |
| 07 January · Jan 23 | 1,000 | $3,990 | $9,720 | $18,315 |
| 08 February · Feb 13 | 1,000 | $5,289 | $11,375 | $19,895 |
| 09 **DRIVE-IN · Feb 20** | 2,500 | $8,759 | $25,394 | $54,505 |
| **Ticketed subtotal** | | **$39,837** | **$94,753** | **$179,368** |
| Light House Thursdays ×6 | | $5,400 | $5,400 | $5,400 |
| Sponsors | | $0 | $10,000 | $20,000 |
| **SIX-MONTH NET** | | **$45,237** | **$110,153** | **$204,768** |

| Scenario | Lands at | Against the $100K target |
|---|---:|---|
| CONSERVATIVE (~50% fill) | $45,237 | **short by $54,763** |
| **TARGET (~70% fill)** | **$110,153** | **clears it by $10,153** |
| SELLOUT | $204,768 | clears it by $104,768 |

## 3. What this actually says

**$100K is reachable and it is not comfortable.** It requires TARGET, not CONSERVATIVE — roughly **70% fill across nine shows**. That is not an arbitrary number: it is exactly Pipeline Law 3's threshold ("break even on tickets alone at 70% sold"). The law was written as a floor for safety. To hit $100K it has to become the *expected case*, on every single date, for six months straight.

**Three lines carry the number.**
- **Drive-In = 23% of target.** One show, a quarter of the year. If it does not happen, target drops to about $85K and the year misses.
- **Halloween + NYE together = $32,735 at target**, ~30%. Both are single dates that cannot be moved or rescheduled.
- **Sponsors = 9% of target and are currently at $0.** No pitch deck, no outreach, no prospect list. This is the only layer where the entire amount is upside rather than execution risk.

**The conservative case is not a failure case.** $45,237 net in six months, self-funded, from a promoter who had $0 cash in August, is a real business. It just is not $100K. Saying so now is worth more than discovering it in February.

## 4. The honest risk on this model

- Costs for shows 03 through 09 are ESTIMATES. The only hard venue number in hand is Fillmore's **Thursday** rate ($3,500/5hr all-in); **the Friday and Saturday rates are unknown** and Halloween is a Saturday. If a weekend buyout runs materially above the Thursday rate, shows 03, 04, 07 and 08 all move together in the wrong direction.
- The Drive-In has **no contact logged anywhere**. It carries a quarter of the target and nobody has spoken to the venue. That is the single largest unmanaged risk in the plan.
- Fill rates are assumed, not observed. The only fill rate ever actually measured is SIGNAL 001, and the current live show is at 2 tickets sold with 15 days to go — which is a conversion problem that was diagnosed and fixed on 8/25, not a demand problem, but it is not yet re-proven.
- Merch income assumes the inventory leak gets fixed. At today's ~$440 of sellable stock the merch column is capped and most of it evaporates.

## 5. Reproduce it

The arithmetic is deliberately simple so it can be re-run and argued with: ticket net = qty × face × 0.89, vendor and merch income scale with fill, costs are fixed per show. Change the fill assumptions and the answer changes; that is the point.
