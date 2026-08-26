# 03 - THE PROMO ENGINE
### The system that sells the tickets. Sept 2026 to Feb 2027.

Built 2026-08-26 off `FACTS.md` and `SLATE.md`. Every number here is either quoted from FACTS.md or labeled **ESTIMATE / Claude's model** with the arithmetic shown so Ryan can check it.

**What this doc is:** the repeatable promo system for all nine shows on the slate. Read Section 0 before you spend one dollar on any of them.
**What this doc is not:** a content calendar for Gold Rush. That loop already exists and is firing. See Section 7.

**Standing rule over everything below: nothing publishes without Ryan's explicit in-session approval.** Staged with Share unclicked is the correct end state.

---

# SECTION 0 - READ THIS FIRST: THE BLACK RECTANGLE

## 0.1 What happened

| | Number | Source |
|---|---|---|
| Gold Rush ticket page visits | **5,482** | FACTS §4 |
| Tickets sold off those visits | **2** | FACTS §4 |
| Conversion rate | **0.04%** | FACTS §4 |
| Ad money spent to buy that traffic | **$897** across 5,506 clicks | FACTS §5 |
| Cost per click | **$0.163** | FACTS §5 |
| Rate the page needed to break even | **0.92%** | FACTS §5 |

The page did not underperform. It was **broken**, and nobody looked at it as a buyer.

**The cause, verified 8/25:** on Shotgun, a broken file sitting in the **Video trailer (16:9) slot renders INSTEAD of the cover image** in the public hero. Every one of those 5,482 visitors landed on a **black rectangle** where the flyer should have been. They did not bounce because the offer was wrong. They bounced because there was nothing to look at.

**What it cost, Claude's model:**
```
2 tickets recovered, assume GA net $17.78 each  =  $35.56
Ad spend against that traffic                    =  $897.00
Net on the broken window                         = -$861.44
```
ESTIMATE. Assumes both sales were GA. Shotgun nets are verified (FACTS §4); the tier split on those 2 orders is unknown.

**What it would have produced at a normal rate, Claude's model:**
```
5,506 clicks x 1.5% = 82.6 tickets
82.6 x $17.78 GA net = $1,468.65
$1,468.65 - $897 spend = +$571.65
```
ESTIMATE, same net assumption. The swing between the broken page and a working page on the same traffic is roughly **$1,433**.

## 0.2 The permanent rule

> ### THE HERO CHECK
> **1. Never leave a video in the Shotgun Video trailer (16:9) slot unless it has been verified playing on the live public page.** If there is any doubt, the slot is empty. An empty trailer slot lets the cover image render. A broken one replaces it.
> **2. Always load the public event page as a buyer, in a normal browser, logged out, on a phone and on desktop, and confirm the hero image renders, before spending a dollar on promo.**
> **3. This check runs again after every edit to the event page.** FACTS §13: Shotgun description edits can silently fail. Verify on the live page, not in the editor.

This is not a Gold Rush lesson. It is a **gate on every one of the nine shows**, and it belongs at T-60 and again at T-21 in the timeline in Section 4.

## 0.3 The four-line pre-flight, run before any paid spend on any show

Ryan or whoever is running the page ticks all four. No tick, no spend.

| # | Check | Pass condition |
|---|---|---|
| 1 | Video trailer slot | Empty, **or** verified playing on the live public page |
| 2 | Hero renders | Cover image visible logged-out, on phone **and** desktop |
| 3 | Buy flow completes | Tiers show correct price, checkout reaches payment |
| 4 | Copy is clean | No exact street address, correct roster stylization, `IfYoKYK` not the retired mark, no banned words (Section 6) |

## 0.4 The second lesson hiding inside the first

**12 promo codes are live and all 12 sit at 0 redemptions as of 8/25.** Twelve codes, 200 total uses, zero used. That is not a code problem. That is a **distribution** problem, and it is compounded by the fact that anyone who did click a code landed on the same black rectangle. Fix the page first, then push the codes (Section 5).

---

# SECTION 1 - THE FUNNEL, MEASURED

## 1.1 The four numbers that run the whole engine

| Metric | Value | Status |
|---|---|---|
| Gold Rush ticket page views | **5,500+** | Verified, FACTS §3 |
| Cost per click | **$0.163** ($897 / 5,506 clicks) | Verified, FACTS §5 |
| Break-even conversion | **0.92%** | Verified, FACTS §5 |
| Normal event page conversion | **1% to 3%** | Verified benchmark, FACTS §5 |

**Traffic is not the problem. Ryan can buy 5,500 people for under $900.** The gap between 0.92% and 1.5% is the entire business.

## 1.2 What each conversion rate is worth per day

**At $211/day** (the spend level modeled in FACTS §5). $211 / $0.163 = **1,294.5 clicks, call it 1,295**.

| Conversion | Tickets/day | Revenue at GA net $17.78 | Spend | **Net/day** | Source |
|---|---|---|---|---|---|
| 0.50% | 6.5 | $115 | $211 | **-$96** | ESTIMATE |
| **0.92% break-even** | 11.9 | $212 | $211 | **~$0** | Verified |
| 1.00% | 13.0 | $230 | $211 | **+$19** | Verified |
| 1.50% | 19.4 | $345 | $211 | **+$134** | Verified |
| 2.00% | 25.9 | $460 | $211 | **+$250** | Verified |
| 3.00% | 38.9 | $691 | $211 | **+$480** | ESTIMATE |

Arithmetic for the two ESTIMATE rows (Claude's model):
```
0.50%: 1,295 x 0.005 = 6.475 tix x $17.78 = $115.13 - $211 = -$95.87
3.00%: 1,295 x 0.030 = 38.85 tix x $17.78 = $690.75 - $211 = +$479.75
```
The four verified rows check out on the same arithmetic, which confirms the model uses **GA net $17.78**, not face value:
```
0.92%: 1,295 x 0.0092 = 11.91 x $17.78 = $211.85  ~ break-even at $211. Correct.
1.50%: 1,295 x 0.0150 = 19.43 x $17.78 = $345.38 - $211 = +$134.38 -> FACTS says +$134. Correct.
```

**At $251/day**, which is the rate the account actually ran on 8/25 and 8/26. $251 / $0.163 = **1,539.9 clicks, call it 1,540**. Every row below is **ESTIMATE / Claude's model**, same arithmetic, same $17.78 net.

| Conversion | Tickets/day | Revenue | Spend | **Net/day** |
|---|---|---|---|---|
| 0.04% (the broken page) | 0.6 | $11 | $251 | **-$240** |
| 0.50% | 7.7 | $137 | $251 | **-$114** |
| 0.92% | 14.2 | $252 | $251 | **~$0** |
| 1.00% | 15.4 | $274 | $251 | **+$23** |
| 1.50% | 23.1 | $411 | $251 | **+$160** |
| 2.00% | 30.8 | $548 | $251 | **+$297** |
| 3.00% | 46.2 | $821 | $251 | **+$570** |

**Read the top row of that table twice.** A broken page at $251/day burns roughly **$240 every single day** and returns almost nothing. That is the entire cost of skipping the four-line check in Section 0.3.

## 1.3 What a full window looks like

**Verified, FACTS §5:** at 1.5% for 16 days: **311 tickets, $5,527 revenue on $3,376 spend = +$2,151 net from ads alone.**
```
$3,376 / 16 = $211/day. $3,376 / $0.163 = 20,712 clicks.
20,712 x 1.5% = 310.7 tickets. 311 x $17.78 = $5,529 (FACTS: $5,527, rounding).
$5,527 - $3,376 = +$2,151.
```

**Gold Rush, 15 days remaining at the current $251/day. Claude's model, ESTIMATE:**
```
15 x $251 = $3,765 spend -> $3,765 / $0.163 = 23,098 clicks

  at 0.04% (broken page):  9.2 tickets x $17.78 = $164     ->  -$3,601
  at 0.92% (break-even):  212.5 tickets x $17.78 = $3,778  ->      +$13
  at 1.50%:               346.5 tickets x $17.78 = $6,161  ->   +$2,396
  at 2.00%:               462.0 tickets x $17.78 = $8,214  ->   +$4,449
```
For scale against the real target: **breakeven on Sept 10 is 575 tickets, 44% of capacity** (FACTS §7), and **236 tickets clears the entire deferred vendor pile, 18% of capacity**. A working page at 1.5% for the remaining 15 days delivers 346 tickets, which covers the deferred pile with room and gets 60% of the way to full breakeven on ads alone.

## 1.4 The standing decision

> **DO NOT CAP THE SPEND. MEASURE IT.** (FACTS §5, do not re-litigate.)
>
> - **Above 0.92%: leave it running.** Every click above break-even is profit, and the daily burn number is meaningless on its own.
> - **Below 0.5% with a page that passed the four-line check: the offer or the audience is wrong, not the spend.** Change the creative, the tier, or the targeting. Do not just cut the budget and call it discipline.
> - **Never judge ad spend by daily burn without dividing by clicks.** $251 is not a number. $251 / $0.163 = 1,540 clicks is a number.

## 1.5 The live risk that sits next to that decision

FACTS §5 flags this and this doc is not going to soften it:

- Ad account **960559416871193** billed **$2,146.08 between Aug 6 and Aug 26**.
- Daily rate climbed **$76 to $127 to $172 to $211 to $251/day** on 8/25 and 8/26.
- **Last 6 days alone = $1,147.85.**
- At $15 Early Bird face, that is **roughly 143 tickets just to cover the ad spend.**

**Someone must look at the daily cap.** "Do not cap" is a decision about not panicking at a healthy conversion rate. It is not a decision to stop looking at the account. The daily rate more than tripled in three weeks and it did that while the page was showing a black rectangle.

**Ryan clicks. Claude never touches the ad account on or off.** Claude reports the number, Ryan decides.

Also live and relevant: **Visa ••2245 froze on 8/25** after a Melio charge plus a Cash App push tripped the fraud model. **While that card is frozen the Instagram ads decline** along with the EMT deposit, Blade, and the porta potties (FACTS §10). A frozen card is a promo outage, not just a payment outage. Check it before assuming a delivery problem.

---

# SECTION 2 - THE CHANNEL MAP

## 2.1 The map, warm to cold

| Channel | Size | Temperature | Cost | Verified? |
|---|---|---|---|---|
| **SMS via (602) 962-7369** | **113 contacts** with phone numbers | **HOTTEST.** Roughly half are SIGNAL 001 buyers. People who already paid. | Per-message cost **unknown, needs Ryan to confirm in Quo**. Marginal cost of the list itself: $0, it already exists. | FACTS §6 |
| **The SIGNAL 001 450** | **~450 through the door**, only 113 reachable by phone today | **WARMEST AUDIENCE THAT EXISTS.** 100% first-time buyers, so 0% have ever bought again. | **$0** to reach the 113. The other ~337 are unreachable until numbers get captured at a door. | FACTS §3, §6 |
| **Artist audiences** (roster of 22, 16 verified handles) | Unknown per artist, needs each artist to confirm | **WARM, BORROWED.** Their fans trust them, not us. | The 25% discount, plus whatever cut Ryan sets. See Section 5. | FACTS §2, §4 |
| **TH3 N3TW0RK broadcast channel** | Member count **unknown, needs Ryan to read it in the IG app** | **WARM, OPT-IN.** People chose to be in it. | $0 | FACTS §1 |
| **IG @subground.collective organic** | **1,276 followers / 22 posts** (8/25) | **LUKEWARM.** Organic story reach is **~80 views on 1,276 followers**, about 6.3%. | $0 | FACTS §1, §5 |
| **IG paid / boosting** | Effectively unlimited | **COLD** but efficient and it is what actually drives traction. | **$0.163 per click**, verified | FACTS §5 |
| **Shotgun followers** | **9** | Cold and irrelevant at this size. | $0 | FACTS §4 |
| **Audience Republic** | **UNKNOWN. Not in FACTS.md, not anywhere in this repo.** | Unknown | Unknown | **NOT VERIFIED** |

## 2.2 The actual top-of-funnel constraint

> **Shotgun followers = 9.**

That is the number that caps organic discovery on the platform where the tickets actually live. Nine people get notified when SubGround posts an event. Every other channel has to push traffic *to* Shotgun because Shotgun will never push traffic *to* the show.

Two consequences that shape everything else in this doc:

1. **Shotgun is a checkout, not a marketing channel.** Do not wait for it to sell anything. It converts traffic you send it, and only if the hero renders.
2. **Every ticket must be driven from IG, SMS, or an artist.** There is no fourth path today. That is why Sections 3 and 5 matter more than Section 1.

**Growing the 9 is worth doing and costs nothing:** the follow button on the event page gets a mention in every day-of and day-after post. It is a slow compounding asset across nine shows. It will not save Sept 10.

## 2.3 Channel by channel, with the real limits

### SMS - the approved A2P number
- **Number: (602) 962-7369.** Approved by The Campaign Registry **8/26 at 6:55 AM**, sole-proprietor application.
- Workspace: **"SubGround-NET3WORK-IfY(o)KYK"** at **my.quo.com**.
- **The list: Shotgun Smartboard > Marketing > Contacts = 113 contacts with phone numbers.** `Export CSV` is top-right.
- **Throughput ceiling: ~1,000 segments/day** on sole-prop 10DLC. 113 recipients fits in one send with room.
  - Claude's model, ESTIMATE: at 2 segments per message, 113 x 2 = **226 segments, about 23% of the daily ceiling**. Standard SMS segmenting is 160 characters for a single-segment GSM-7 message and 153 per segment once it concatenates. **Confirm the exact segment count inside Quo before sending, do not trust this estimate on send day.**
- **Hard compliance rules (FACTS §6 and §15, these do not bend):**
  - **Consent is required.** Only message people with an existing relationship. The 113 gave their number at ticket purchase. That is the relationship.
  - **Every single message carries an opt-out line.** No exceptions, not even a one-line reminder.
  - **Honor STOP immediately and permanently.** Remove from the list, do not re-add.
  - **Never import a scraped, bought, or guessed number.** Do not text anyone who never transacted.
- **A2P craft that keeps the number alive:** no EIN required for sole prop. OTP goes to a **carrier mobile, never a VoIP number**. One sending number. **Twilio error 30915 means an EIN-holding entity got attached to a sole-prop registration, so keep Sanfilippo Holdings LLC out of it entirely.**

### IG @subground.collective
- **1,276 followers / 22 posts** as of 8/25. The old "889 / blocked on the 1,000 gate" note is dead, Ryan cleared it.
- **Organic story reach is ~80 views.** Plan accordingly: stories are for the people already in, boosting is for the people who are not.
- **Platform limits that will silently waste your time (FACTS §13):**

| Limit | What it means for promo |
|---|---|
| **IG collab invite hard cap = 5 per post** | A 9-artist lineup does not fit on one collab post. Section 5.3 has the workaround. |
| **IG DMs cap at 1,000 characters and SILENTLY refuse at the limit** | A 1,000-char artist pitch never sends and never errors. Keep DMs well under. |
| **IG web DM send is unreliable from automation** | Working route as of 8/26: `find` the Send button, `computer scroll_to` the ref, then `computer left_click` the ref. A bare ref click on an inbox row does nothing without the `scroll_to` first. |
| **IG private-API calls via javascript_tool are BLOCKED** by the action classifier | Use the DOM route. |
| **Broadcast channels are INVISIBLE to Instagram web** | See below. |
| **Cloud and scheduled sessions have NO browser** | Any IG posting step runs on-computer, never from a scheduled cloud run. |

### TH3 N3TW0RK broadcast channel
- Exists, and it is **app-only. Invisible to Instagram web.** Channel posting and appearance settings cannot be reached from a browser at all.
- **Operational meaning: every broadcast drop is a phone job Ryan does by hand.** No automation can do it, on-computer or in the cloud.
- **Member count is unknown.** Ryan reads it in the app once, and it goes in FACTS. Until then this channel cannot be sized or forecast.
- It is still the highest-intent free channel available. People opted in.

### The 12 promo codes
All **25% off**, all at **0 redemptions as of 8/25** (FACTS §4).

| Code | Uses | Belongs to | On the Sept 10 lineup? |
|---|---|---|---|
| SHARKY | 15 | Sharky, @sups2shark. **PROMOTER, never goes on lineup art.** | No, promoter |
| BASSED | 15 | @bassed.dnb | Yes, USB B2B BASSED |
| MOON | 15 | FØØL MØØN, @foolmoonbeats | Yes |
| USB | 15 | @usb.dnb | Yes, USB B2B BASSED |
| FAIRYDVST | 15 | Srija, @srija.fairydvst | Yes |
| PRADA | 15 | PRADA G, @pradagoneverything | Yes |
| CHIRENJI | 15 | @chirenji_dub | Yes |
| GALLIUM | 15 | GALLIUM, @ggalliumm | Yes, headliner |
| ONSUMMON | 15 | @onsummon | Yes |
| ANAMORPHIC | 15 | @anamorphic_music | Yes |
| BRILLIANT25 | 25 | **Owner unknown, needs Ryan to confirm** | Unknown |
| RELENTLESS25 | 25 | **Owner unknown, needs Ryan to confirm** | Unknown |

**Total capacity: 200 uses** (7 x 15 = 105, plus 25 + 25 + 15 + 15 + 15 = 95).

**What 200 redemptions would actually be worth, Claude's model, ESTIMATE:**
```
GA $20 face, 25% off = $15 buyer price.
Shotgun nets $13.33 on a $15 face (verified for Early Bird, FACTS §4).
200 x $13.33 = $2,666 net, vs 200 x $17.78 = $3,556 at full GA.
Cost of the discount if all 200 burn: $890.
```
ESTIMATE. Assumes Shotgun's take is the same ~11% of the paid price on a discounted ticket as on a full one, which is a reasonable read of the verified numbers but has **not** been tested on a real discounted order. **Worth Ryan running one $15 discounted test order** the same way Order #68759746 verified the base rates.

**Nine of these twelve codes belong to artists who are on the Sept 10 bill.** Ten if you count Sharky. Zero have been used. That is the single cheapest unclaimed revenue on the board and it needs distribution, not redesign.

### Smartboard craft, so nobody loses an hour to it
- Edit page: `smartboard.shotgun.live/events/<id>/edit`
- **The promo-code drawer renders off-screen right. Trusted clicks miss. `JS .click()` works.**
- Lineup order lives in the **Event description textarea**, and the native setter persists there.
- **Ticket-row drag-reorder and the per-row "more" menu do NOT respond to automation.** Ryan does those by hand.
- Event IDs: **pre-party 581323** (Public / On-Sale). **Afters 581336** is a retired concept. **Flip it to Private, never delete it.**

### Audience Republic
**Status: unknown.** The name does not appear in `FACTS.md` or anywhere in this repo. Nothing about it is verified: not whether an account exists, not who holds the login, not what list size is inside it, not what it costs.

**Owner of this question: Ryan.** Three things to confirm before it goes in any plan:
1. Does a SubGround Audience Republic account exist, and under which email?
2. If it does, how many contacts are in it, and do those contacts overlap the 113 in Shotgun?
3. What does it cost per month, and is it currently billing?

Until those are answered it is **not a channel**, it is a rumor, and no beat in Section 4 depends on it.

---

# SECTION 3 - THE SINGLE BIGGEST UNTAPPED ASSET

## 3.1 State it plainly

> **450 people came to SIGNAL 001 on May 16, 2026.**
> **The buyer profile shows 100% first-time buyers.**
> **Therefore zero of those 450 have ever bought a second SubGround ticket.**

It is the warmest audience that exists, it costs nothing to reach, and it has never been asked.

Supporting numbers, all verified in FACTS §3:
- SIGNAL 001, May 16 2026: **~450 people** (never say 300), 21 artists.
- Shotgun history: **$2,740 across 142 tickets = $19.30 realized net per ticket.**

## 3.2 The reachability gap, and why it is the real problem

Claude's model, ESTIMATE, arithmetic shown:
```
Through the door at SIGNAL 001:          ~450
Shotgun tickets sold:                     142
So roughly 308 came in another way (door, guest list, comp).

Phone numbers on file across ALL SubGround history:  113
Roughly half of those are SIGNAL 001 buyers (FACTS §6): ~56

Reachable by SMS out of the 450 today:  ~56 to 113, call it under 25%
Unreachable:                            ~337 to 394
```
ESTIMATE on the split. The 450, the 142, and the 113 are verified. The overlap between them is not, and nobody has counted it.

**Two conclusions fall straight out of that:**

1. **The list is smaller than the audience, and that is a capture failure, not a marketing failure.** Three hundred-odd people walked through a door SubGround built and left no way to reach them.
2. **Door capture is now a permanent day-of job on every show.** See Section 4, T-0. If Sept 10 draws even 400 people and captures 200 numbers with consent, the SMS list roughly triples in one night and every show after it gets cheaper to sell.

## 3.3 The win-back play

**Objective:** convert first-time SIGNAL 001 buyers into repeat buyers on Gold Rush, and use that same play on every show after it.

**Why it should work:** these people paid money to stand in a SubGround room and they have never been asked to do it again. Their conversion rate has no reason to look like cold traffic's 1% to 3%. It should look far better. **That is a hypothesis, not a fact. Measure it, do not assume it.**

### The four sends

Every send goes out from **(602) 962-7369**, from the Quo workspace, to the 113 exported from Shotgun Smartboard > Marketing > Contacts. **Every send carries the opt-out line.** Every send is written short because SMS is a tap, not a read.

| Send | When | Job |
|---|---|---|
| **1. The win-back** | T-14 | Name the relationship, name the show, name the price, one link |
| **2. The deadline** | T-10 | Early Bird closing is a real deadline, use it once |
| **3. The last call** | T-5 | Final push while there is still time to buy |
| **4. The thank-you + opt-in** | T+1 (day after) | Thank them, ask for the next one, feed the list |

**Do not send more than four times per show.** Sole-prop 10DLC throughput is small, carrier tolerance for a new number is smaller, and the fastest way to kill a brand new A2P registration is to look like a blast.

### The copy

All four are written to be sent to a person. No em dashes, no banned words, no exact street address.

**SEND 1 - T-14, the win-back**
```
SubGround here. You were at SIGNAL 001 in May.
Next one is Thu Sept 10 in Peoria. GALLIUM closing.
All ages, no alcohol, 1pm to 10pm.
Early Bird is $15.
Reply STOP to opt out.
```
Then paste the live public Shotgun link for event 581323 on the end. **Do not retype that URL from memory. Copy it out of the browser after the Section 0.3 hero check passes.** Claude has not seen that URL and it is not written here.

**SEND 2 - T-10, the deadline**
```
SubGround. Early Bird for Sept 10 is $15 and there are only 100 of them.
After that it is $20.
GALLIUM closes at 9.
Reply STOP to opt out.
```
Verified: **100 Early Bird at $15, 1,200 GA at $20, cap 1,300** (FACTS §3, §4). **Only send this if the Early Bird tier is genuinely still open.** If it sold out, say it sold out. FACTS §15: never claim a stat that is not real.

**SEND 3 - T-5, the last call**
```
SubGround. Thursday. Peoria. Doors 1pm, GALLIUM 9 to 10, hard out at 10.
Vendors, car show, all ages.
Last chance to grab a ticket before the day.
Reply STOP to opt out.
```

**SEND 4 - T+1, the thank-you and the ask**
```
SubGround. Thank you for being there yesterday.
Photos and video are coming this week.
You are on the list for the next one first.
Reply STOP to opt out.
```
This one is doing two jobs. It closes the loop, and it keeps the list warm through the gap to the next show so send 1 on the next show is not a cold restart.

### The consent rules, restated because this is where things go legally wrong

| Rule | Why |
|---|---|
| **Only message existing relationships** | The 113 gave their number at purchase. That is the consent basis. Nothing else qualifies. |
| **Opt-out line on every message** | FACTS §15. Not just the first one. Every one. |
| **Honor STOP immediately and permanently** | Remove from the export, do not re-add on the next show |
| **Never import scraped, bought, or guessed numbers** | It kills the A2P registration and it is the wrong way to run |
| **Identify SubGround by name in every message** | People delete unknown numbers. Being named is both compliant and better marketing. |
| **Ryan approves every send before it goes** | Standing rule, FACTS §15 |

### Door capture, the thing that makes send 1 bigger next time

Physical sign-up at the merch booth on every show, run off the Pixel 10 Pro XL that is already there for Square Tap to Pay.

The consent language on the sign-up has to be explicit and it has to be visible above where they type:

```
Text me about SubGround shows.
Message rates may apply. Reply STOP anytime.
```

Nothing else. No pre-checked box, no "by entering you agree to" buried below the fold. The whole value of the list is that the people on it want to be on it.

---

# SECTION 4 - THE PER-SHOW PROMO TIMELINE

**This is a template. It runs on any of the nine shows.** Counted backward from doors, not from announce.

## 4.1 The beats

| Beat | Asset | Channel | The job it does |
|---|---|---|---|
| **T-60** | Shotgun event page built. Hero cover image locked. **Trailer slot EMPTY unless verified playing.** Accent color chosen per FACTS §1. | Shotgun (build only, nothing public) | **Build the thing that converts before you drive anyone to it.** Run the Section 0.3 four-line check now, the first of two times. Nothing publishes at this beat. |
| **T-45** | Save-the-date. Date, city, accent, "We build the underground." **No street address.** | IG feed post 4:5 portrait + story + broadcast channel | **Plant the date.** Not selling yet. Selling here wastes the announce. Open the SMS opt-in link in the bio. |
| **T-30** | **ON SALE.** Early Bird tier live. Headliner announce with the collab tag. | IG feed collab post, story, broadcast channel, SMS is silent | **Turn attention into money.** Pipeline Law 2: presales are financing. Early Bird is the cheapest capital SubGround can raise. |
| **T-21** | Full lineup art. Correct roster stylization. **Second Section 0.3 check.** Artist codes and clip spec go out. | IG collab posts (5-cap, see 5.3), artist DMs, broadcast channel | **Turn the lineup into a distribution network.** This is the beat where the artists become the channel and the promo codes get into hands. |
| **T-14** | **ADS ON.** Boost the best-performing organic post, not a fresh cold creative. **SMS SEND 1, the win-back.** | IG paid + SMS | **Buy traffic now that there is a working page and a full lineup to land on.** Section 1.4 governs: above 0.92%, leave it running. |
| **T-10** | Early Bird closing notice. **SMS SEND 2, the deadline.** Artist clips start rotating. | IG story, SMS, artist stories | **Manufacture a real deadline.** The tier step is genuine urgency and it does not require lying. |
| **T-7** | Vendor and production reveal. Set-time tease. First artist clip posts land. | IG feed + stories, vendor cross-posts | **Widen the reason to come.** Vendors, car show, food. Not everyone comes for the headliner, and vendors keep 100% of their sales so they promote hard. |
| **T-5** | **SMS SEND 3, last call.** **Ryan requests the Shotgun early payout.** | SMS + Shotgun Banking | **Two jobs: last soft push, and get the money moving.** Early payout runs Banking > event balance > New Transfer > 4-digit emailed code > 2 to 3 business days. Requesting at T-5 puts cash in hand before doors. **Ryan does this. Claude never moves money.** |
| **T-3** | Set times published. Countdown sticker on story. | IG story + broadcast channel | **Convert the fence-sitters.** People buy when they can see which hour they want. |
| **T-2** | Know-before-you-go: parking, age policy, alcohol policy, what to bring. **Exact location drops to ticket holders only.** | Shotgun buyer email + broadcast channel + story | **Kill the friction that stops a purchase, and reward the buyers.** Location as a ticket-holder perk is a purchase reason, not just a security rule. |
| **T-1** | Final story push. Final ad check. Day-of run of show confirmed to every artist and vendor. | IG story, SMS is silent, direct DMs | **Last conversion window, and make sure the show can actually run.** Check the ad account conversion rate one more time against 0.92%. |
| **T-0, day-of** | Live stories on a rolling cadence: doors, line, first set, peak, headliner. Merch booth live. **Door number capture.** | IG stories + broadcast channel | **Sell at the door, and capture the list.** Section 3.3 says why the capture matters more than the walk-ups. |
| **T+1, day-after** | **RAW recap within 48 hours.** **SMS SEND 4.** Thank the artists and vendors by handle. **Ryan pays the next show's deposits.** | IG feed + stories, SMS, DMs, bank | **Close the loop and fire Pipeline Law 1.** Every event funds the next event's deposits. The day-after post is also the T-45 asset for the next show. |

## 4.2 The two checks that repeat, and where

**Section 0.3, the four-line hero check, runs at T-60 and again at T-21.** Twice, because the T-21 lineup art edit is exactly the kind of edit that can silently fail on Shotgun and put a broken asset back in the hero right before the money goes in.

**The conversion check runs daily from T-14 to T-0.** One number: clicks divided into tickets. Compare to 0.92%. Above it, do nothing. Below 0.5% on a verified page, change the creative or the audience, not the budget.

## 4.3 Where the money beat sits

Pipeline Law 1 says every event funds the next event's deposits. That has a hard timing consequence on this timeline:

```
T-5   Ryan requests early payout on Shotgun
      2 to 3 business days
T-1   Cash lands
T-0   Show runs, day-of cash comes in at the door and the booth
T+1   Ryan pays the NEXT show's deposits
```
FACTS §4: **sell about 4 days before the money is needed.** Requesting at T-5 is the tightest safe version of that. If a deposit is due earlier than T-1, the request has to move earlier, and the on-sale date has to move earlier with it. **On-sale dates are when the show pays its own bills** (Pipeline Law 2).

## 4.4 The T-60 date for every show on the slate

Computed in Python off the SLATE dates, not eyeballed.

| Show | Date | T-60 | T-45 | T-30 | T-21 | T-14 |
|---|---|---|---|---|---|---|
| Gold Rush Pre-Party | Thu Sep 10 2026 | Sun Jul 12 | Mon Jul 27 | Tue Aug 11 | Thu Aug 20 | Thu Aug 27 |
| Icehouse Content Night | Fri Sep 18 or Sat Sep 19 | past | past | past | Fri Aug 28 | Fri Sep 4 |
| **HALLOWEEN** | Sat Oct 31 2026 | **Tue Sep 1** | Wed Sep 16 | Thu Oct 1 | Sat Oct 10 | Sat Oct 17 |
| Combine x Northern Road | Fri Nov 6 2026 | **Mon Sep 7** | Tue Sep 22 | Wed Oct 7 | Fri Oct 16 | **Fri Oct 23 (blackout)** |
| TH3 N3TW0RK Night | Sat Dec 12 2026 | Tue Oct 13 | Wed Oct 28 | Thu Nov 12 | Sat Nov 21 | Sat Nov 28 |
| New Year's Eve | Thu Dec 31 2026 | Sun Nov 1 | Mon Nov 16 | Tue Dec 1 | Thu Dec 10 | Thu Dec 17 |
| January Headline | Sat Jan 23 2027 | Tue Nov 24 | Wed Dec 9 | Thu Dec 24 | Sat Jan 2 | Sat Jan 9 |
| February Headline | Sat Feb 13 2027 | Tue Dec 15 | Wed Dec 30 | Thu Jan 14 | **Sat Jan 23** | Sat Jan 30 |
| Drive-In Glendale 9 | Sat Feb 20 2027 | Tue Dec 22 | Wed Jan 6 | Thu Jan 21 | Sat Jan 30 | Sat Feb 6 |

### Four collisions this table exposes

1. **HALLOWEEN T-60 IS TUE SEP 1. THAT IS SIX DAYS FROM NOW.** Oct 31 2026 is a Saturday, which happens roughly once every seven years (2020, 2026, 2037), and SLATE calls it the highest-value open date of the window. **Its promo clock starts before Gold Rush even happens.** The Shotgun page has to be built during Gold Rush week, not after it. This is the single most time-sensitive line in this document.
2. **Combine T-14 lands Fri Oct 23, the first day of the HARD BLACKOUT** (Oct 23 to 25, Ryan is at F33LZ's We Are Love Friend Festival). The ads-on beat and SMS SEND 1 for Nov 6 must be **built and staged before Oct 23** and fired on a schedule, or moved to T-16 on Oct 21. Ryan will not be available to run them live.
3. **The February show's T-21 is Sat Jan 23, which IS the January show.** And the Drive-In's T-21 is Sat Jan 30, which is February's T-14. From late January onward, three promo windows overlap. Sequence the SMS sends so the 113 do not get three texts in one week, and separate the ad audiences so the two shows are not bidding against each other.
4. **January's T-30 is Thu Dec 24 and February's T-45 is Wed Dec 30.** On-sale beats landing on Christmas Eve and the day before NYE. Move them by a day or two. Nobody buys a Phoenix rave ticket on Christmas Eve.

## 4.5 Gold Rush is already inside the window, so run it compressed

**Today is 2026-08-26. Gold Rush is T-15.** The T-60, T-45, T-30, and T-21 beats are behind us. Do not pretend otherwise, and do not skip their *jobs*, just compress them.

| Beat | Date | Status and what actually happens |
|---|---|---|
| T-15 | **Wed Aug 26** | **RUN SECTION 0.3 RIGHT NOW.** The page is Public and On-Sale (event 581323) and it has been showing a black rectangle. Nothing else on this list matters until that check passes. |
| T-14 | **Thu Aug 27** | Ads on against a verified page. **SMS SEND 1**, the win-back to all 113. Artist codes and the clip spec go out to all nine lineup artists in one push. |
| T-10 | **Mon Aug 31** | Early Bird deadline push. **SMS SEND 2.** Also the last useful day to reorder merch, since FACTS §7 sets the reorder-by date at Sept 1 and stock is capped at ~$440 of sellable inventory. |
| T-7 | **Thu Sep 3** | Vendor reveal (0FD, Valley Freeze, greenphoenixfarm420 pending). **Vendor fees $450 are due today** and the Peoria layout locks. Vendors keep 100% of sales, so give them art to post. |
| T-5 | **Sat Sep 5** | **SMS SEND 3.** **Ryan requests the Shotgun early payout.** Valley Freeze is also booked separately today, so a live cross-post is free content. |
| T-3 | **Mon Sep 7** | Set times published. Countdown sticker. |
| T-2 | **Tue Sep 8** | Know-before-you-go: all ages, **no alcohol**, parking, hard stop at 10 PM. Exact address to ticket holders only. |
| T-1 | **Wed Sep 9** | Final push. Final conversion check against 0.92%. Confirm run of show to every artist and vendor. |
| T-0 | **Thu Sep 10** | Event 1 PM to 10 PM, hard stop 10 PM (city record supersedes the old 2 PM doors line). **GALLIUM 9 to 10 PM.** Rolling stories, merch booth, door capture. |
| T+1 | **Fri Sep 11** | RAW recap. **SMS SEND 4.** Thank every handle. Permit cleanup is 7 to 8 AM. **Ryan pays Icehouse and Halloween deposits out of the door money.** Melcher lead engine re-enables today. |

**The one open reach blocker on Gold Rush:** GALLIUM's team still owes a **repost plus collab-tag acceptance on @ggalliumm** for the 8/20 lineup post (instagram.com/p/DcSSydQFPmW). FACTS §7 is explicit that this is the reach blocker, **not** an art-approval blocker. Agent is **Andrew Lehr, AB Touring, andrew@abtouring.com, (814) 602-5613**, who has not replied to three emails and **prefers the phone**. FACTS §7: the next rung is the phone, not a fourth email. **Ryan makes that call.**

## 4.6 Icehouse is the exception, and it runs on a different clock

**ICEHOUSE IS NOT A REVENUE EVENT.** Ryan's binding correction, 8/22. Free event, zero ticket revenue, roughly $2.5k total cost ($2k room plus about $500 projection mapping and lasers), funded out of Sept 10 proceeds. **Do not model it as profit anywhere, including here.**

It has **no ticket funnel**, so Section 4.1 does not apply. Its promo job is inverted:

| Normal show | Icehouse |
|---|---|
| Promo sells tickets | **Promo fills 10 artist slots and about 20 heads for the shoot** |
| Output is revenue | **Output is the asset library that promotes shows 03 through 09** |
| Success = tickets sold | Success = **RAW within 48 hours, curated edit over 2 weeks** |

Format: setup and doors 7 PM, **15-minute sets back to back**, projection-mapped walls plus lasers. Lineup of 10: FOOL MOON, ONSUMMON, USB, FAIRYDUST, CHIRENJI, WAKE UP, F33LZ, EXGF5, ANAMORPHIC, PRADA G, with VELCROSHIRT in as the final spot for now.

**This is the content engine for the rest of the slate.** Every T-45 save-the-date, T-21 lineup post, and artist clip for Halloween, Combine, TH3 N3TW0RK Night, NYE, January, February, and the Drive-In can be cut from this one night. That is what makes a free show worth $2.5k. **Content first. Sponsors second. Festival third.**

Booking is still open: email sent 8/11 to **Sam, sam@openvenues.com**, 4-hour shoot roughly 7 to 11 PM, contract name Sub Ground, headcount ~20. **No artist constraint requires the 19th**, so let Sam's availability decide between Fri Sept 18 and Sat Sept 19. **The $2,000 room fee is not in hand. Nothing gets signed, committed, or promised before Sept 10 without Ryan's OK.**

---

# SECTION 5 - ARTIST AS CHANNEL

## 5.1 Why this section is worth more than the ad section

The roster is 22 artists. Sixteen have verified IG handles. Every one of them has an audience that trusts them more than it trusts a promoter's boosted post, and reaching that audience costs **nothing but a discount and a cut.**

Right now that channel is producing **zero**. Twelve codes, 200 uses, 0 redemptions.

## 5.2 The promo-code-with-a-cut structure

**The structure:** each artist gets a named code on the Shotgun ticket page. The code gives their fans **25% off**. Every redemption is attributed to that artist. The artist gets a cut of each ticket their code sells, on top of their performance fee.

**Why it works better than "please share the flyer":**
- The artist's fans get a real reason to use their link instead of just buying normally.
- Attribution is automatic, so nobody argues about who drove what.
- It pays the artist for reach, which is the thing SubGround actually needs and cannot buy at this price.
- **It fires Pipeline Law 4.** Today's artists are DREAM's department heads. Paying them for reach now is how they grow at these prices.

**The cut amount is Ryan's call and is not set anywhere in FACTS.md.** Here is the model so he can pick a number, not so Claude can pick one for him.

**Claude's model, ESTIMATE. Per GA ticket, all arithmetic shown:**
```
Full price GA:  $20 face -> $17.78 net to SubGround (verified, FACTS §4)
25% off code:   $15 face -> $13.33 net to SubGround (inferred, same ~11% Shotgun take)

The discount alone already costs:  $17.78 - $13.33 = $4.45 per ticket

Then the artist cut comes off that $13.33:
  $1 cut -> SubGround keeps $12.33   (69% of full GA)
  $2 cut -> SubGround keeps $11.33   (64%)
  $3 cut -> SubGround keeps $10.33   (58%)
  $5 cut -> SubGround keeps  $8.33   (47%)
```
ESTIMATE on the $13.33 net for a discounted ticket. Verified for a $15 Early Bird face; **not yet tested on a discounted order.** One test purchase settles it.

**The sanity check against breakeven:** Sept 10 breaks even at **575 tickets** on **$9,779** of realistic cost, which is **$17.01 of net needed per ticket at breakeven volume** ($9,779 / 575 = $17.01, Claude's arithmetic off FACTS §7). A discounted code ticket at $13.33 nets **below** that line, and with a cut on top it nets further below.

**What that means, said straight:** promo codes are a **volume and reach instrument, not a margin instrument.** They are worth it because they bring in buyers who would not have bought at all and because they buy the artist relationship. They are not worth it if they cannibalize full-price buyers who were already going to come. **Cap the uses** (which the current 15-and-25 structure already does, 200 total across 12 codes) and do not extend them once the show is selling.

**Three things Ryan should decide before the codes go out:**
1. The cut per ticket, or whether the 25% discount alone is the artist's compensation for reach.
2. Whether the cut is paid in cash on show night or added to the artist's fee.
3. Who owns BRILLIANT25 and RELENTLESS25, or whether those two should be retired.

## 5.3 The 5-collab cap, and how to work with it

**IG collab invite hard cap is 5 per post.** Verified, FACTS §13. A 9-artist lineup does not fit.

**Do not solve this by tagging in the caption.** A caption tag is a mention. A collab puts the post on the collaborator's grid and in front of their followers. Those are different products and only one of them is reach.

**The workaround: split the lineup across posts.**

For a 9-artist bill like Sept 10:

| Post | Collab slots used | Who |
|---|---|---|
| **Post 1, the headliner post** | 1 of 5 | @ggalliumm, plus up to 4 more if he accepts |
| **Post 2, the lineup post** | 5 of 5 | Five artists |
| **Post 3, the lineup post part two** | 4 of 5 | The remaining four, plus the vendor @zer0fuakindrip |

Every artist lands on somebody's collab post. Nobody gets left in a caption.

**Rules for the collab flow:**
- **Only tag verified handles.** FACTS §2 lists the 16 that are safe: @foolmoonbeats, @bassed.dnb, @srija.fairydvst, @fairytale_productionsaz, @pradagoneverything, @usb.dnb, @chirenji_dub, @anamorphic_music, @sups2shark, @mind.g4me, @allie.radd, @sp3llkvstr, @your_exgirlfriendsmusic, @psytari, @onsummon, @king_space_music. Plus @ggalliumm for the Sept 10 headliner. **No verified handle exists for Yewz, Conkusst, Spaydz, or Bandaid. Ask them, do not guess.**
- **@sups2shark is Sharky, a PROMOTER. Never on lineup art.** He can be collabbed on a promo post, never billed as an artist.
- **A collab invite is not reach until it is accepted.** Track acceptances. An unaccepted invite does nothing at all. This is exactly what is currently stalling the Sept 10 headliner post.

## 5.4 THE CLIP SPEC - the highest-leverage fix on this whole page

**The lesson, and it is worth reading twice: the fix is the SPEC you send artists, not more cropping on your end.**

Every hour spent re-cropping a landscape clip an artist sent is an hour that produces one mediocre asset. One clear spec sent once produces correct assets from every artist forever. **Fix the input, stop patching the output.**

**CHIRENJI's submission is the reference example.** Native portrait, shot and delivered at 1080x1920. That is the correct submission and it needed nothing done to it.

### The spec, exactly as it goes to artists

Send this verbatim. It is written to be sent to a person, so there are no em dashes in it and nothing in it sounds like software.

```
Sending you the clip spec so your stuff looks right and I do not have to crop it.

Shoot it vertical on your phone. Do not shoot landscape and do not send me a
screen recording.

1080 x 1920, portrait, straight off the phone.
15 to 30 seconds.
No text on it, no logo, no watermark. I add those.
Good light on your face or good light on the setup, one or the other.
Sound on. Even if we mute it, I want the option.

CHIRENJI's last one is exactly right if you want to see the target.

Send it as a file, not through a story. Stories compress it to mush.
```

### Why 1080x1920 and not 4:5

| Format | Size | Used for |
|---|---|---|
| **Portrait 9:16** | **1080 x 1920** | **Reels, stories, broadcast channel. This is what artists submit.** |
| **Portrait 4:5** | 1080 x 1350 | Feed posts. Ryan's standing IG format rule per the `ryan-source-map` skill: never square, portrait 4:5, grid-safe center. |
| Square 1:1 | 1080 x 1080 | **Never.** Standing rule. |

**A 1080x1920 native clip can be cut down to 4:5 without losing quality. A 4:5 or landscape clip cannot be expanded up to 9:16 without either bars or a destructive crop.** That is the whole reason the spec asks for the biggest correct frame. Take the tall one and cut down. Never take the wide one and stretch up.

**Grid-safe center applies to every crop-down.** If the subject is not centered in the frame, the feed crop cuts their head off.

### What to ask each artist for, per show

Three things, asked once at T-21, in one DM under 1,000 characters (FACTS §13: IG DMs silently refuse at the limit):

1. **One clip to the spec above.**
2. **Their promo code, with the cut named.**
3. **Accept the collab invite.** This is the one that actually moves reach and it is the one artists forget. Say it last so it is the thing they read before they close the app.

---

# SECTION 6 - CONTENT RULES

## 6.1 The mark and the words

| Rule | Detail |
|---|---|
| **The mark is `IfYoKYK`.** Exact casing. | "IF you, only, You Know." The old form is **retired** for all new content. Legacy instances still live on site copy, some Printify products, and printed cards. **Scope of fixing those is Ryan's call, not a promo decision.** |
| **The descriptor is "bass, underground, and frontline electronic music."** | **BANNED: "psytrance."** Never, in any copy, ever. |
| **BANNED WORD: "frequency."** | Not in captions, not in taglines, not in artist DMs, not in ad copy. If you need the idea, use a different word. |
| **Tagline in use: "We build the underground."** | |
| **Roster stylization is exact and never altered.** | FOOL MOON, EXGF5, MIND G4ME, ALLIE RADD, YEWZ, KING SPACE, VELOCES, SP3LLKVSTR, PSYTORI, THE ALCHEMIST, CONKUSST, SPAYDZ, USB, FAIRYDUST (styles herself **FɅIRYDVST**), CHIRENJI, WAKE UP, F33LZ, PRADA G, DIGITS, BANDAID, ONSUMMON, ANAMORPHIC. **F33LZ uses they/them.** |
| **Roster count is 22.** | The website still says "20+ artists." Fix owed. |
| **Never add SPECKZ.** | Standing and permanent. |
| **Never sound like AI.** | No em dashes in anything sent to a person. |

## 6.2 Color, and the correction that matters

**FACTS §1 was updated by Ryan directly on 2026-08-26 and it supersedes the old blanket no-purple rule.** Older docs and older instructions still carry "no purple on SubGround posts." **That line is stale.** Anyone working off it will produce the wrong art.

> **PER-EVENT ACCENT, FIXED CHASSIS.**
> **The chassis is the brand. The accent is the event.**
> One earned accent per event, never a rainbow.

**PURPLE IS ALLOWED on every event except one. Purple is BANNED on GOLD RUSH PRE-PARTY material only, because Gold Rush owns gold.**

And the reverse also holds: **gold is the GOLD RUSH event brand, not the SubGround house brand.** Do not put gold on other events.

**Locked accents for this slate:**

| Show | Accent |
|---|---|
| Gold Rush Pre-Party | **GOLD.** No purple, ever. |
| Icehouse | ICE / pale cyan |
| **Halloween** | **VIOLET.** The date earns it. |
| Combine x Northern Road | STEEL BLUE |
| TH3 N3TW0RK | TERMINAL GREEN |
| NYE | CHROME / platinum |
| January | COLD SLATE |
| February | CRIMSON |
| Drive-In | TEAL |

Note that **Halloween's locked accent is violet**, which is by itself proof the blanket no-purple rule is dead. Two entries in the same locked list cannot both be true.

**The chassis, which never changes on any event:**
```
ground     #08090B
panels     #101216
hairlines  #1E222A
silver     #A7ABB6
paper      #EDEFF4

Type: Archivo (display + body) + IBM Plex Mono (labels, timestamps, all data)
Marks: bracket corner marks, hairline rules
```

## 6.3 What never goes public

| Never publish | Instead |
|---|---|
| **A venue's exact street address** | City only. Teasers say "Coming Soon." **The location drops to ticket holders**, which makes it a purchase reason instead of a leak. |
| **The tunnel location, at all** | Tunnel Rave promo is **teasers only, permanently.** Not to ticket holders, not to the broadcast channel, not ever. |
| **Any capacity, headcount, or stat that is not real** | Use the proven facts: 1,300 approved capacity, GALLIUM under contract closing 9 to 10 PM, 5,500+ ticket-page views, 450 through the door at SIGNAL 001, vendors keep 100% of their sales with no cut. **Ryan refused to tell a vendor "1,200 guaranteed." Hold that line.** SIGNAL 001 is **~450**. Never say 300. Never inflate it either. |
| **Stock photos, AI images, or another promoter's crowd shots as SubGround crowd** | **Real performance photos only.** The 8x8 matte vinyl backdrop exists specifically to generate real ones (matte because gloss glares in the AZ sun and ruins photos). Icehouse exists to generate a library of them. |
| **An unverified artist handle** | Only the 16 verified handles in FACTS §2, plus @ggalliumm for Sept 10. Ask, do not guess. |
| **Sharky on lineup art** | He is a promoter. Collab him on promo posts, never bill him as an artist. |

## 6.4 The approval gate

> **Nothing publishes without Ryan's explicit in-session approval. Staged with Share unclicked is the correct end state.**

That covers IG feed posts, stories, broadcast channel drops, every SMS send, artist DMs, ad creative, and any edit to a live Shotgun page. **Claude drafts and stages. Ryan presses the button.**

Same split on money: **Claude never moves money.** Ryan requests the Shotgun payout, Ryan pays the artist cuts, Ryan pays the deposits, Ryan touches the ad account on and off.

---

# SECTION 7 - FEED THE LOOPS, DO NOT DUPLICATE THEM

**Ryan's standing preference: no chat overlapping another's duties.** Two systems doing the same job is worse than one, because now nobody knows which one is authoritative.

## 7.1 The live loops this doc feeds

| Loop | Status | How this doc relates to it |
|---|---|---|
| **"SubGround daily story push (Gold Rush to Sept 10)"** | **LIVE and firing** | **Any Gold Rush content plan FEEDS this loop, it does not duplicate it.** Section 4.5 is the beat schedule the daily push draws from. Do not create a second Gold Rush content task. Do not write a competing daily calendar. Hand this loop the assets and the beats and let it run. |
| **THE NIGHT DESK** | **LIVE.** ONE artifact, ONE permanent URL: `claude.ai/code/artifact/34d787f1-b905-4883-af42-717acaa0f336` | **NEVER create a second board. NEVER fork it.** Any session that updates it **must pass `url:` to the Artifact tool.** Refresh trigger `trig_01737a51KSMoe8LKkCvNhanU`, cron `0 4,14,21 * * *` = 7am / 2pm / 9pm MST. Promo status lands **on that board**, not on a new one. |
| **THE DREAM ladder** | Live artifact: `claude.ai/code/artifact/e4e7f869-12c7-40e1-a62b-38dc5541a83b` | Update in place via the url param. |
| **ON THE ROCKS** | Live artifact: `claude.ai/code/artifact/06070ae1-eab8-421f-a9a9-d41b8de9ab2c` | Update in place via the url param. |
| **Scout Tour Radar** | Mondays around 9 AM | Match rule: show within 90 to 360 miles **and** within 2 weeks = top priority. **No auto-pitching until a date is locked.** Radar output feeds the T-60 build decision, it does not trigger promo on its own. |
| **Nightly memory sweep** | 11:30 PM | Any promo fact learned this cycle goes here. |
| **Melcher lead engine** | **PAUSED** for Sept 10 focus | Re-enables 9/11, calendar reminder set for 9/11 9am. Not a SubGround promo channel. Do not cross the lists. |

## 7.2 The rule for anyone adding to the promo system

**Before you build a new promo automation, answer three questions:**

1. **Does a loop already do this?** The daily story push already covers Gold Rush daily content. The Night Desk already covers status. If the answer is yes, feed it.
2. **Where does its output land?** If the answer is "a new artifact," stop. It lands on the Night Desk at the existing URL.
3. **Can it actually run where it will run?** **Cloud and scheduled sessions have NO browser and NO device bridge.** Anything touching Chrome, IG, Google Messages, or local files runs on-computer. A scheduled cloud task that tries to post to Instagram will fail silently and nobody will notice for a week.

**And one scheduler rule, from FACTS §13: never use local `CronCreate` for scheduled tasks. It dies with the session.** Claude Code Remote `create_trigger` or `send_later` only.

## 7.3 Delivery limits that will silently eat a send

| Pipe | State | The gotcha |
|---|---|---|
| **Google Messages web** | **LIVE and paired**, retested 8/26 11:15 AM, about 25 threads | **The paper-plane Send button does NOT fire from automation. Enter in the compose box DOES.** |
| **IG web DM** | Unreliable from automation | Working route 8/26: `find` Send, `computer scroll_to` the ref, `computer left_click` the ref. **A bare ref click on an inbox row does nothing without the `scroll_to` first.** |
| **IG broadcast channel** | App-only | **Invisible to IG web.** Phone job, by hand, every time. |
| **Discord** | **Web is logged OUT on frontdesk Chrome.** Desktop is signed in but **NOT VIEWABLE**, screenshots return a uniform dark mask. | **Do NOT send blind into Discord.** Wrong-thread risk. Blind-read recipe that works: clipboard sentinel, ctrl+k jump, @-name Tab autocomplete, ctrl+a then ctrl+c to read, always with a nonsense-handle control test. |
| **Chrome via computer-use** | Read tier only | No clicks, no typing. Interaction goes through the claude-in-chrome extension, which can only address tabs inside its own MCP tab group. |
| **Shotgun description edits** | Can silently fail | **Verify on the live public page, never in the editor.** This is the same class of failure that produced the black rectangle. |

---

# SECTION 8 - THE CONFIRM LIST

Everything this doc needs and does not have. **No placeholders were used. These are open questions with a named owner.** Each one that gets answered goes into `FACTS.md`, not into a side note.

| # | Unknown | Owner | Why it blocks something |
|---|---|---|---|
| 1 | **Does the Gold Rush page currently pass the Section 0.3 hero check?** | Ryan | Blocks every dollar of promo spend on Sept 10. Highest priority item in this file. |
| 2 | **What is the live public Shotgun URL for event 581323?** | Ryan | Every SMS send and every ad needs it. **Copy it from the browser, do not retype it.** |
| 3 | **Audience Republic: does an account exist, under which email, how many contacts, what does it cost?** | Ryan | It is listed as a channel in the brief but appears nowhere in FACTS.md or this repo. Until answered it is not a channel. |
| 4 | **TH3 N3TW0RK broadcast channel member count** | Ryan, in the IG app (web cannot see it) | The channel cannot be sized or forecast without it. |
| 5 | **What does Quo charge per message or per month?** | Ryan, at my.quo.com | SMS is called the cheapest channel in this doc. That claim is unverified on cost. |
| 6 | **What is the artist cut per ticket on a promo code, and is it paid in cash on show night or added to the fee?** | Ryan | Section 5.2 models it but will not pick a number. |
| 7 | **Who owns BRILLIANT25 and RELENTLESS25?** | Ryan | 50 of the 200 total code uses are unattributed. |
| 8 | **Does a 25%-off $15 GA ticket really net $13.33?** | Ryan, via one test order | Section 5.2's whole margin model rests on this inference. One purchase settles it, same as Order #68759746 settled the base rates. |
| 9 | **Exact overlap between the 113 SMS contacts and the 450 who attended SIGNAL 001** | Ryan, by reading the export | Section 3.2 estimates it. The real number changes how the win-back is written. |
| 10 | **Has GALLIUM accepted the collab tag and reposted on @ggalliumm?** | Ryan, by phone to Andrew Lehr (814) 602-5613 | Named in FACTS §7 as **the** reach blocker on Sept 10. Three emails have gone unanswered. The next rung is the phone. |
| 11 | **Verified IG handles for Yewz, Conkusst, Spaydz, Bandaid** | Ryan or the artists | They cannot be collabbed or tagged until these exist. Do not guess a handle. |
| 12 | **Stylization conflicts inside FACTS.md itself** | Ryan | **FOOL MOON** (roster §2) vs **FØØL MØØN** (Sept 10 lineup §7). **FAIRYDUST** (§2, §8) vs **FɅIRYDVST** (§2 note) vs **FAIRYDVST** (§7). **F33LZ** vs **F333LZ** (both in §8). Roster stylization is exact and never altered, so these have to be resolved before they go on printed art. |
| 13 | **What is the ad account's current daily cap set to?** | Ryan, in account 960559416871193 | The rate went $76 to $251/day in three weeks while the page was broken. Section 1.5. |
| 14 | **Is Visa ••2245 unfrozen?** | Ryan, by calling the number on the back | While it is frozen the ads decline. It is a promo outage, not just a payment one. |
| 15 | **Icehouse: Fri Sept 18 or Sat Sept 19?** | Sam at sam@openvenues.com | No artist constraint requires the 19th. Sam's availability decides. Blocks the shoot call sheet. |

---

## THE WHOLE ENGINE IN NINE LINES

1. **Load the page as a buyer before you spend a dollar.** 5,482 visits and 2 sales is what skipping that costs.
2. **The trailer slot is empty unless the video is verified playing.** A broken file renders instead of the hero.
3. **Traffic is cheap at $0.163 a click. Conversion is the whole business.** 0.92% is break-even, 1% to 3% is normal.
4. **Do not cap the spend, measure it.** Above 0.92% leave it running. Below 0.5% on a verified page, change the offer, not the budget.
5. **Shotgun followers = 9.** Every ticket gets driven from IG, SMS, or an artist. There is no fourth path.
6. **450 people came in May, 100% first-time buyers, zero repeats.** That is the warmest audience in the business and it costs nothing. Text the 113, with consent and an opt-out line, and capture numbers at every door.
7. **Fix the clip spec, not the crop.** 1080x1920 native portrait, CHIRENJI's is the example. One spec beats a hundred re-crops.
8. **Halloween's promo clock starts Tue Sept 1**, six days from now, before Gold Rush even happens. Saturday Halloween comes around about every seven years.
9. **Feed the loops. Never fork the Night Desk. Ryan approves everything and Ryan moves all the money.**
