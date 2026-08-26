# 06 — FINANCE

The money system: what is owed, what is owed to him, what rail each thing runs on, and what is quietly leaking.

**Everything in the LIVE STATE section was read from Gmail on 2026-08-26 between 19:00 and 20:00 MST.** It contradicts stored memory in two places, and that is the point of the section. **Live beats stored, always.**

**Claude never moves money.** Every line here ends with Ryan pressing the button. Claude fills fields, finds the number, names the deadline, and flags the leak.

---

## 1. LIVE STATE — read today, and it is not what the notes said

### 🔴 THE GALLIUM DEPOSIT FAILED. IT IS NOT PAID.

Stored memory says *"GALLIUM $625 DEPOSIT — SCHEDULED & CARD ACCEPTED 8/25."* **That is wrong.** Melio sent two failure notices **today**:

| When | What |
|---|---|
| 2026-08-26 12:02 MST | "Your $625.00 payment to AB Touring, LLC **has failed** due to an issue with your payment method" |
| 2026-08-26 15:24 MST | Same message again |

- **Payment ID `pymnt_90515894`** · org `org_4884078` · Invoice **#10786**
- Resolve at: `app.melio.com/pay/scheduled/pymnt_90515894?organization=org_4884078`
- **The contract deadline is Friday Aug 28. That is two days out.**
- **Richer detail from the Night Desk, read live 8/26:** the payment is now **staged in Melio against Desert Financial checking ••0400 at $0 fee — but NOT confirmed.** The account went **further negative overnight** on overdraft fees and cannot absorb a $625 debit without bouncing a third time.
- ⚠️ **AND THE DELIVERY DATE IS THE REAL PROBLEM: standard ACH delivers Aug 31 — three days AFTER the Aug 28 deadline — even once the account can send it.** Fixing the funding alone does not fix the timing.
- **So the actionable move is not financial, it is a conversation:** tell AB Touring the payment is staged and ask whether a short delay still lands inside their window. That costs nothing and is the only lever that works today.
- Mom cannot cover it and pointed to Mario. **Mario has the US Bank line (866-268-7231) and has said "I'll call when I'm ready" — the fourth time this has come up.** Ryan's own plan: $200 cash to Mario, which fixes the card and returns $200 to Desert Financial, leaving ~$150 to cover.

**This is the single most urgent money item in the business.** The headliner is signed, publicly announced, and the deposit that secures him has not landed.

### 🟢 BLADE IS PAID — first half, confirmed

Stored memory says *"NOTHING HAS BEEN PAID."* **Also wrong, and this one is good news.**

- Cash App receipt 2026-08-26 09:10 MST: **"You paid Blade V Colosimo $250 · For security"** · sender "Ryan sans"
- Blade's own invoice arrived 15:52 MST: **"Invoice 023 $250 deposit paid"**, total $500
- **Remaining: $250 day-of, Sept 10, from door money.**

### 🔴 THE CARD IS FAILING EVERYWHERE, NOT JUST AT MELIO

Six failed Anthropic charges today alone — $98.19, $49.10, $48.65, $21.17 (twice), $20.97 — alongside two that succeeded. Plus:

- **OnePay debit card DEACTIVATED** — "Payment declined, your OnePay debit card is deactivated" (8/26 11:04)
- **Cash App Card declined $5** at Zenbusiness (8/26 09:20)
- **Venmo declined Discord $14.57** again (8/25 20:30) — this has been failing daily since 8/9

**Read: there is no working card right now.** Cash App *balance* sends work (Blade went through). Card-funded rails do not.

### 🟢 KELLY MADRID REPLIED — the approval letter is in the inbox

2026-08-26 18:34 MST, thread `1a03f35d2b48a7be`, with **the approval letter and the approved site plan attached**, answering the vendor-count and 400 sq ft canopy question. Her words: table-only vendors are fine; a couple more 10x10 pop-ups are fine, however (condition continues in the attachment). **This unblocks taking vendor money.** It has been sitting unread.

### ⚠️ LIKELY PHISHING — do not click

Three near-identical **"Service Suspension Notice"** emails arrived 8/26 12:12–12:15 to `ryan@`, `dream@` and `booking@subgroundcollective.com`, from random-string senders on **`statica.sk`** (`4hx6vvtfwq@`, `qwv3dyxplp@`, `mof6nqtu5c@`). Random mailbox names, a Slovak domain, three addresses hit at once, and urgency about "automatic renewal." **Treat as phishing. Do not click, do not enter credentials.** Zoho is the real mail host; verify any real suspension at the Zoho admin directly.

---

## 2. THE RAILS — what works, what it costs, what is broken

| Rail | Fee | Status today | Use it for |
|---|---|---|---|
| **Cash App `$Ryansans`** | free P2P from balance; **3% on card sends, and most issuers code those as a cash advance** | **WORKING from balance** | Money IN. Vendor fees. Paying Blade. **Default rail while checking is negative.** |
| **Melio** (card → ACH) | **2.9%** | ⚠️ **failing** — Gallium bounced twice today | Vendors who will not take cards. Contract-compliant for AB Touring's "direct deposit." |
| **Square Tap to Pay** | **2.6% + 15¢** | account exists, no reader; Tap to Pay works on the Pixel 10 Pro XL | The merch booth. Next-business-day funding. |
| **Shotgun Banking** | ~11% taken at ticket sale | working | Ticket revenue. **Early payout: Banking → event balance → New Transfer → 4-digit emailed code → 2–3 business days.** Sell ~4 days before money is needed. |
| **Visa ••2245** | — | 🔴 **FROZEN** since 8/25 fraud hold | Nothing, until Mario calls |
| **OnePay debit** | — | 🔴 **DEACTIVATED** | Nothing |
| **Venmo (business)** | — | receiving works, **spending does not** (balance ~0) | Booth QR only |
| **Checking ••0400 (Desert Financial)** | — | 🔴 **NEGATIVE** | **Nothing.** Zelle/ACH into it gets eaten by the overdraft before it reaches the bill. |
| **Zelle** | — | **does not exist** | — |

### The card problem, stated precisely
**Visa ••2245 is in Ryan's name but on his dad's (Mario Romero) account. Limit $1,500, not $3,000. Ryan is an authorized user — he cannot request a credit-line increase, only the primary can.** About **$857** remains available and is simply locked. US Bank needs Mario on the line. Mario said he would call on 8/25 and did not.

Two fixes given, neither done:
1. **Call the number on the back of the card** — the automated line reads available credit from the card number alone, no primary-account access needed.
2. **Register an authorized-user online login** (card number + name + DOB + last-4 SSN at most issuers) so Ryan gets his own balance and alerts instead of discovering declines at a deadline.

---

## 3. WHAT IS OWED, AND WHEN

### Sept 10 — Gold Rush

| Line | Amount | Status | Due | Rail |
|---|---:|---|---|---|
| **GALLIUM deposit** | **$625** | 🔴 **FAILED TWICE TODAY** | **Fri Aug 28** | Melio `pymnt_90515894` — needs a working card |
| GALLIUM balance | $625 | not due | day-of, after performance | cash from door |
| GALLIUM hotel + ground | unknown | not booked | before Sept 10 | — |
| Blade security 1st half | $250 | ✅ **PAID 8/26** | — | Cash App |
| Blade security 2nd half | $250 | open | day-of | from door |
| **EMT ELITE deposit** | **unknown — the figure is inside `SubGround Collective Price Qt.pdf` and has never been read. Do not guess it.** | open | **locks the date** | electronic only, no checks |
| EMT balance | unknown | open | 72 hrs prior | electronic |
| Klarity Audio (sound) | **$1,400 if paid before the show, else $1,500** | open | early-pay saves $100 | Jonathan, 714-225-0547 |
| Proper Site Services | ~$2,250 verbal · trim target ~$1,855 | written quote still not received | 50% up front / 50% day-of | — |
| Wristbands (WristCo) | ~$28 for 500 ×2 colours | open | before Sept 10 | — |
| Insurance | $477 | ✅ PAID | — | — |
| TUP fee | $600 | ✅ PAID 8/11 (ACCELA-119946) | — | — |
| City licence PBL26-010893 | $47.95 | ✅ paid by Moses (receipt #3906) | — | — |
| Printify booth order | $331.98 | ✅ PAID by Ryan 8/25 (#28379886.1) | — | — |

**Cash needed in the next 72 hours: the Gallium $625 (Friday) plus the EMT deposit.** Everything else on this table is either paid or deferrable to Sept 7–10 and coverable from door money. **236 tickets covers the whole deferred pile — 18% of capacity.**

### Money owed TO him

| Source | Amount | Status |
|---|---:|---|
| Vendor fee — 0FD (@zer0fuakindrip) | $150 | locked 8/25, rail sent, unpaid. **Has 2 unread DMs from 8/26.** |
| Vendor fee — Valley Freeze | $150 | terms sent, unpaid |
| Vendor fee — greenphoenixfarm420 | $150 | never confirmed "in" |
| Ticket sales | ongoing | breakeven is **575 tickets** |

**All three vendor fees are due Sept 3** (layout lock with Peoria). **Kelly's reply today is what unblocks charging them.**

---

## 4. THE SUBSCRIPTION LEAK

Recurring charges found across this session. **Several are being paid for things that are paused, retired, or duplicated.**

| Charge | Amount | Note |
|---|---:|---|
| **Instagram ads** | **~$251/day and climbing** | $2,146.08 billed Aug 6–26. Last 6 days = $1,147.85. **At $15/ticket that is ~143 tickets just to cover ad spend.** Per-click is genuinely efficient ($0.163) so this is a *pacing* call, not a kill call — but it is the largest outflow in the business and nobody has set a cap. **Ryan's call, Claude never touches on/off.** |
| Google Workspace | ~$22/mo | started 8/17 after the trial ended. Cancel-or-keep decision is overdue. |
| Quo (A2P/SMS) | 3 separate receipts on 8/26 | Downgrade-to-Starter is already scheduled for Sept 11 (`trig_01UfkbVYYnaeosFocZGDibw`). |
| Registered Agents Inc. | annual | For Sanfilippo Holdings LLC. **Confirm it is still wanted** — a paid RA service bills every year whether used or not. |
| Discord Nitro | $14.57/mo | **Declining daily since 8/9.** Either fix the card or cancel it; a daily decline email is a subscription you are not receiving. |
| Massage Envy | $90/$180 | Declined 6+ times (8/9 through 8/23). Same call. |
| Anthropic | variable | 6 failed charges today. |

**The pattern worth naming: a card that declines does not cancel the subscription, it just fails loudly forever.** Every one of these is still accruing an obligation.

---

## 5. THE DEBT FILE

| Creditor | Amount | Position | Action |
|---|---:|---|---|
| **PRA** | $657 | No reply to the 7/27 validation request. **The 30-day window closed ~Aug 26 — that is TODAY.** | **1692g(b) cease-collection letter + CFPB complaint are now ripe.** This is the one with a live deadline. |
| **Midland** | $456 | Treat the web form as **never submitted** | Resubmit at `midlandcredit.com/response/` |
| **NCA** (Speedy Cash, acct 17881605) | $300 | Dispute acknowledged 7/28, **1692g pause in effect**; validation arrives by postal mail | **No action.** Wait. |
| **Kikoff** | $200 | **No written deletion agreement** | **DO NOT PAY.** Escalation draft staged 8/5 (thread `19fa59bf60fb78bb`), token CL632UR3LZ. |
| **Coconino** | — | Goodwill **DENIED** 7/28 (Marlene Baca, COO). The lates are real. | **NEVER dispute.** Disputing a real late is how you lose credibility on the ones that are wrong. |

---

## 6. THE STRUCTURE QUESTION — open, and it is Ryan's

**Sanfilippo Holdings LLC is ACTIVE.** AZ file #23614065, filed 2023-12-06. Registered agent: Registered Agents Inc.

But **SubGround operates as a sole-prop DBA**, and the **Melio account was opened as a sole proprietorship using an SSN, not an EIN.** That is a real fork and it has consequences for banking, liability and business credit.

Three options, all legitimate:
- **(a)** Get an EIN under Sanfilippo Holdings LLC and open the business account under it. Strongest for business credit, no new formation cost.
- **(b)** Keep SubGround as a sole-prop DBA with its own EIN.
- **(c)** File an AZ trade name for "SubGround Collective" under the existing LLC.

**This is a money and structure decision, not Claude's to assume.** Two related cleanups: the ACC record still lists an old Phoenix address (805 N 4th Ave) rather than Peoria, and the paid registered-agent service bills annually.

⚠️ **Do not attach the LLC to the A2P/10DLC registration.** It was deliberately filed sole-prop and came back approved; adding an EIN-holding entity is what causes Twilio error 30915.

---

## 7. THE RULES

1. **Show money and life money never touch.** Pipeline Law 1. Every event funds the next event's deposits.
2. **Claude never moves money.** Fills every non-financial field; Ryan types bank digits and presses Confirm. This split held on the Melio setup and Ryan accepted it — keep it on every future payment.
3. **Never type an SSN, tax ID or government ID into any field.** Route to the no-SSN path or hand it to Ryan.
4. **A payment ask without a payment destination is not an ask.** Every message requesting money carries the rail in the same message. Default: **Cash App `$Ryansans`.** Caught 8/26: three vendors all knew the $150 price, none had been told where to send it — $450 frozen on a missing line.
5. **While checking is negative, money in flight goes to Cash App, never Zelle-to-Desert-Financial.** Cash App lands in a separate balance; ACH into ••0400 gets eaten by the overdraft.
6. **Never judge ad spend by daily burn without dividing by clicks.** $251/day sounds alarming; $0.163/click is efficient. Break-even conversion is 0.92% and normal event pages run 1–3%.
7. **Verify a payment landed. Do not trust the confirmation email.** Gallium was recorded as PAID on 8/25 and failed on collect on 8/26. **Scheduled is not paid. Charged is not delivered.**

---

## 8. HOW THIS STAYS CURRENT

The daily mission trigger (`trig_017ayWRpQy1mRZKHsUWjQPci`, 8 AM MST) already runs a money step. It should, every run:

1. **Sweep Gmail for money mail in the last 24h** — receipts, declines, invoices, failure notices. Declines and failures outrank receipts.
2. **Re-verify anything marked PAID that has not cleared.** A scheduled payment is not a paid payment.
3. **Update section 1 and section 3 of this file**, commit, push.
4. **Push the deltas into the Night Desk MONEY WATCH block** (one artifact, one URL, always pass `url:`).
5. **Surface, never spend.** Name the number and the deadline; Ryan presses the button.

**What Claude cannot see:** bank balances, the Visa's available credit, cash in hand, and anything paid in cash at the door. Those are Ryan's to report, and the model is blind without them. Do not infer a balance from receipts alone.
