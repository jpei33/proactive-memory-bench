# Adjudication sheet

Each row below got two different labels. One is your first pass, one is the model's, in random
order. Reread the row against rubric.md and write your FINAL label in sheet_adjudicate_triggers_rest.csv.
You may pick either candidate or a third label.


## Row 2

**Candidates:** INTERVENE / TRACK

**Today: Mon Oct 5** · #harbor

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 5 · #harbor ---
yuki: Quick check before I lock the pass criteria section: is the harbor workshop paper submission deadline Oct 23? React 👍 if so.
(nadia reacted 👍 to yuki's message)
theo: Baselines table is still on the old task set. I'll regenerate once the replacements land, otherwise the numbers won't line up with the new items.
marcus: Two of the overlapping tasks are near-verbatim from a popular CLI repo. Leaning toward dropping those outright rather than rewriting them, since the solutions are easy to find.
felix: Release note for planning: the harbor release version is v1.2. It'll carry the contamination replacements once marcus's list is final, so the changelog stays in one place.
yuki: If marcus drops those two CLI tasks, I'll check the difficulty spread afterward. Don't want the replacements skewing easy and inflating pass rates.
marcus: Good point on difficulty. The replacement candidates I've pulled so far are mostly single-file fixes, so they'd probably skew easy. I'll look for some multi-file ones.
nadia: Separate thing: we still need someone to own the eval compute reservation for the rerun. Who's taking that on?
elena: I'll grab it.
theo: Once the swap list is final I'll rerun the baselines and plot pass rate by repo size. Curious if multi-file tasks widen the gap between models.
yuki: Theo, if you plot by repo size, bucket by files touched too. Otherwise size and multi-file get tangled and the gap is hard to read.
theo: Good call, will do. I'll also split by language since the Python tasks tend to be the easiest, so that might be another confound.
marcus: Found a couple of multi-file candidates in a Rust build tool, bug spans the parser and the config loader. Checking the license now.
yuki: Rust is useful there too. If the models do much worse on those, I'd want to report language as its own breakdown in the paper.
theo: Rust tasks would be a good breakdown. Since the paper's due Oct 30, I'll plan to have the baseline reruns done a few days before so we have time to write up the language split.
```

> **>>> DECIDE AFTER THIS:** theo: Rust tasks would be a good breakdown. Since the paper's due Oct 30, I'll plan to have the baseline reruns done a few days before so we have time to write up the language split.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena

---

## Row 5

**Candidates:** IGNORE / INTERVENE

**Today: Mon Oct 12** · #kestrel-run

**Team facts as of now**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps (changed Fri Oct 9; previously every 500 steps)
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 5 · #kestrel-run ---
kofi: Mateo, the start slipped for the firmware rollout, so no need to kick off data loading tonight. The shard diff matters more right now.
mateo: Right, I was working off the old start. Skipping the loader launch tonight, running the tab/space diff on those shards first.
lucia: Confirmed, blanking panels are missing in that row. Filing a facilities ticket. I'll re-check CRC counters on those ports once temps settle.
wen: What if we start on half the nodes Oct 7 and add the rest after the firmware lands? Cordoned ones stay out either way. Is that worth considering?
dmitri: No, not worth it. Partial start means two bring-ups and a messy loss curve to explain later. We hold the plan as is and start once the firmware is in.
hana: Once firmware lands I want an NCCL all-reduce sweep on the uncordoned nodes to baseline MFU and flag stragglers before the real launch.
wen: I'll export the uncordoned list as a hostfile for the sweep, grouped by leaf so stragglers map back to a switch easily.
kofi: Good idea on grouping by leaf. For the sweep, I'd also keep a checkpoint write/read pass on those hosts to see if storage paths show stragglers too.
lucia: I'll poll CRC and link-flap counters on the uncordoned leaves during the sweep, so any straggler can be matched to a port event.
kofi: While we're baselining storage: maybe checkpoint every 250 steps for kestrel? Just a thought, nothing decided. The write/read pass should tell us if the paths can take that cadence.
hana: Worth adding async checkpoint overlap to that pass, so we see if writes stall the step loop or just hit storage.
mateo: I'll tag the shard diff output by shard so any tokenizer-related loss spikes are easy to trace back later.
lucia: Adding the optic serials from that vendor lot to the facilities ticket, so they can swap them while the row's cordoned.
hana: I'll add per-rank step-time histograms to the sweep dashboard so stragglers show up before we eyeball NCCL logs.
--- Mon Oct 12 · #kestrel-run ---
dmitri: Morning. Launch day. Post your final go/no-go here before I kick off, and I want eyes on stragglers from step 1.
```

> **>>> DECIDE AFTER THIS:** dmitri: Morning. Launch day. Post your final go/no-go here before I kick off, and I want eyes on stragglers from step 1.

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps (changed Fri Oct 9; previously every 500 steps)
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

---

## Row 8

**Candidates:** IGNORE / TRACK

**Today: Tue Sep 22** · #design-partners

**Team facts as of now**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per human seat, agents free (changed Wed Sep 16; previously $12 per seat, agent actions metered)
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): Oli (changed Fri Sep 18; previously AJ)
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: Sara to decide whether agents may DM a human first, without being asked (check point: Mon Sep 21 design review)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Tue Sep 22 · #design-partners ---
alex: morning all. design review yesterday left me with a few FAQ wording questions for the design partners, mostly around how agents show up in channels. can we go through them here?
frida: one of our design partners asked if billing invoices can go to their finance person instead of the workspace owner. Anyone know?
aj: Afaik invoices go to the owner's email only. No separate billing contact field in settings yet, I'd have to check how the Stripe side is wired.
frida: Thanks AJ. They're a small agency, so the finance person isn't a workspace member at all. Would be a real blocker for them.
oli: Stripe lets you set a billing email separate from the account owner, so it's probably a small settings field plus a ticket. Checking how we wired the customer object.
frida: Nice, that'd cover them. Would the invoice PDF also show their company name, or just the workspace name? They asked about that too.
oli: Stripe customer object has a name field separate from the email, so company name should work. Need to confirm what our invoice template pulls.
frida: Thanks Oli. Separate thing: I told the agency heads-up that after launch it's agent actions metered, so their invoice will vary month to month. They were fine with it, just wanted finance to know.
alex: Back to FAQ wording. When an agent jumps into a thread untagged, do we say "joins" or "chimes in"? Partners might read that as intrusive.
olavo: "Joins" reads calmer to me, "chimes in" sounds like butting in. Maybe a line in the FAQ about muting an agent per channel?
alex: Good idea on muting. Should it be per channel only, or can someone mute an agent in just one thread too? Partners will ask.
aj: Per channel is easy since mute is a membership-level flag. Per thread means a new subscription state to track, and search needs to respect it too.
frida: One partner mentioned wanting an agent quiet in one noisy thread but still active in the channel. So per-thread might come up.
frida: Unrelated, heads up: I need to leave early Thursday for a family thing. Can someone cover partner questions in the afternoon? Happy to leave notes on who's waiting on what.
```

> **>>> DECIDE AFTER THIS:** frida: Unrelated, heads up: I need to leave early Thursday for a family thing. Can someone cover partner questions in the afternoon? Happy to leave notes on who's waiting on what.

**Team facts again**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per human seat, agents free (changed Wed Sep 16; previously $12 per seat, agent actions metered)
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): Oli (changed Fri Sep 18; previously AJ)
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: Sara to decide whether agents may DM a human first, without being asked (check point: Mon Sep 21 design review)

---

## Row 12

**Candidates:** IGNORE / TRACK

**Today: Tue Oct 6** · #acct-northwind

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Tue Oct 6 · #acct-northwind ---
tomas: Once Gabe's usage numbers are in, I'll draft the pricing options for the order form. Rachel, any sense of how aggressive they'll be on discount?
rachel: Honestly not sure yet. Their procurement team pushed hard last cycle, so I'd expect them to open with a big ask.
rachel: Tomas, quick check before we plan the negotiation: is the Northwind discount currently 18% off list? Want to confirm before I anchor anything with them.
tomas: Yes, that is correct.
darnell: Worth getting ahead of procurement on this one. If their big ask comes in early, I'd rather we already have a view on where we'd hold.
ines: Before we settle on a negotiating position, I'd like to see what they redlined last time. Their legal team tends to reopen data terms.
keiko: Their clinical informatics lead also hinted procurement may bring in a new reviewer this cycle. I'll try to find out who before the next call.
darnell: On the sponsor question: Northwind's exec sponsor is Amara Okafor, their CIO. I'll own that relationship and reach out to her this week.
rachel: Good. Darnell, loop me in before you reach out so I can brief you on where the deal stands. Ines, I'll dig up the last redlines.
gabe: Early look at usage: a couple of pilot teams do spike hard during morning clinic hours. I'll put together a peak-hour breakdown for Tomas.
keiko: Those morning clinic spikes might be worth raising with them directly. Their informatics lead has complained before about slowdowns during rounds, so I can ask what they've seen.
gabe: Yes, please ask. If they've seen slowdowns during rounds, I'd like timestamps so I can match them against the peak-hour breakdown.
keiko: Will do. I'll ask their informatics lead to jot down times next time it happens, so we get real timestamps instead of memory.
ines: Rachel, when you pull the old redlines, can you flag which data clauses they pushed on most? That'll tell me where to prep.
ines: Separate from the redlines: I'll send the signed data processing addendum to Northwind legal by Fri Oct 9, so they have it before procurement digs in.
```

> **>>> DECIDE AFTER THIS:** ines: Separate from the redlines: I'll send the signed data processing addendum to Northwind legal by Fri Oct 9, so they have it before procurement digs in.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)

---

## Row 16

**Candidates:** IGNORE / TRACK

**Today: Mon Oct 12** · #kestrel-run

**Team facts as of now**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps (changed Fri Oct 9; previously every 500 steps)
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 5 · #kestrel-run ---
lucia: I'll poll CRC and link-flap counters on the uncordoned leaves during the sweep, so any straggler can be matched to a port event.
kofi: While we're baselining storage: maybe checkpoint every 250 steps for kestrel? Just a thought, nothing decided. The write/read pass should tell us if the paths can take that cadence.
hana: Worth adding async checkpoint overlap to that pass, so we see if writes stall the step loop or just hit storage.
mateo: I'll tag the shard diff output by shard so any tokenizer-related loss spikes are easy to trace back later.
lucia: Adding the optic serials from that vendor lot to the facilities ticket, so they can swap them while the row's cordoned.
hana: I'll add per-rank step-time histograms to the sweep dashboard so stragglers show up before we eyeball NCCL logs.
--- Mon Oct 12 · #kestrel-run ---
dmitri: Morning. Launch day. Post your final go/no-go here before I kick off, and I want eyes on stragglers from step 1.
lucia: Fabric side looks clean on my end. IB link flap counters are flat since the last sweep, no pending cable tickets.
wen: Allocation is sitting idle and healthy in the scheduler, no drained nodes flagged. Watching for any that flip to unhealthy during job startup.
kofi: Checkpoint writer is up on my side. I'll watch async flush times on the first saves, since stalls there tend to show up as stragglers.
hana: Loss and grad-norm dashboards are live. I'm also tracking per-rank step time so a slow rank shows up before MFU dips.
mateo: Dataloader workers are warm and prefetch queues look full. Should be smooth on the first few batches, no stalls expected from the data side.
dmitri: Good. Kicking off now. Shout the second you see a rank lagging, don't wait for it to show up in MFU.
hana: First steps are in. Per-rank step time looks tight so far, no rank trailing the pack. Still early though.
wen: Heads up, separate from kestrel: the kestrel-mini ablation run starts Oct 14. Different run, I'll keep its nodes carved out so it doesn't touch this allocation.
```

> **>>> DECIDE AFTER THIS:** wen: Heads up, separate from kestrel: the kestrel-mini ablation run starts Oct 14. Different run, I'll keep its nodes carved out so it doesn't touch this allocation.

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps (changed Fri Oct 9; previously every 500 steps)
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

---

## Row 21

**Candidates:** INTERVENE / IGNORE

**Today: Wed Sep 16** · #gtm

**Team facts as of now**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per human seat, agents free (changed Wed Sep 16; previously $12 per seat, agent actions metered)
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Wed Sep 16 · #gtm ---
frida: real thread is doable! I'd need to ask the partner first though. one of them has a good one where the agent chimed in on a deploy question 👀
sara: Going with Alex's pricing suggestion from Monday. Acting on it now, Olavo update the page copy to match.
olavo: on it 🙌 quick check while I edit: should agent seats get their own line on the page, or fold into one?
frida: fwiw two design partners asked if agents count toward their seat total, so a separate line might save us support questions 🙏
alex: if agents get their own line, could we add a small tooltip there explaining what an agent seat actually covers? Or is that too much on the page?
olavo: tooltip is easy, I can draft a one-liner. alex can you check it doesn't clash with the hover state on the plan cards?
alex: yep, I'll check the tooltip against the plan card hover. might need to nudge the tooltip anchor so it doesn't overlap the border 🤔
olavo: random thought while I'm in the press plan doc: what if we pushed to Oct 1 to give press more time? just a what-if, not pitching it yet
sara: Not moving the date. Press has what they need, we stay on the current plan.
frida: Pinging the design partner about using their deploy thread screenshot. Should I ask them to blur names, or will Alex redact on our side?
alex: I can redact on our side, but better if they blur it themselves so nothing sensitive leaves their workspace. Frida, maybe offer both?
frida: Will offer both! Also they asked if the screenshot can show the agent's profile card, so people see it has its own name and inbox 😊
alex: Profile card in the screenshot works for me, that's the whole point. I'll crop it so the name and inbox icon are both visible.
olavo: nice. for the press kit I'll want a couple of cropped versions of that screenshot too, one square for socials, one wide for the post header.
olavo: pasting the line for the post intro: "Ando is launching publicly, backed by a $25M Series A." feels punchy, going to keep it up top unless anyone objects 🚀
```

> **>>> DECIDE AFTER THIS:** olavo: pasting the line for the post intro: "Ando is launching publicly, backed by a $25M Series A." feels punchy, going to keep it up top unless anyone objects 🚀

**Team facts again**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per human seat, agents free (changed Wed Sep 16; previously $12 per seat, agent actions metered)
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

---

## Row 24

**Candidates:** INTERVENE / TRACK

**Today: Mon Oct 5** · #kestrel-run

**Team facts as of now**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Sep 28 · #kestrel-run ---
hana: Thanks. Once I have it I'll also add per-rank NCCL timing to the dashboard, so a slow allreduce on those ranks is visible right away.
kofi: Lucia, when the other uplink gets swapped, give me a heads-up. If those racks drop mid-soak I want to see how the staging path handles a rank vanishing.
lucia: Will do. Swapping the second optic after the current soak window closes, so CRC counters on the first port stay a clean baseline.
lucia: Heads up, the cluster room is louder than a jet engine today. Swapping optics in there with earplugs in, so slow to reply if I miss pings.
kofi: Once the mapping lands I'll also check whether those ranks end up in the same NCCL ring segment. A flaky one could stall the whole ring.
wen: If the ring segment does include those ranks, I can reshuffle placement so they land on a different leaf. Cheap on my side.
hana: Mapping would also let me flag whether those ranks show up as stragglers in the last burn-in logs. Pulling those now to compare.
dmitri: If those ranks show up as stragglers in burn-in, I want that in the writeup before we lock the placement.
wen: Pulling the current placement map now so I can see which leaf those ranks sit on and what's free to swap into.
lucia: Mapping exported. Both ports are on leaf 7, and the ranks are mostly the last GPU slots per node. Dropping the CSV in the channel.
hana: Got the CSV. Cross-referencing against burn-in straggler logs now, last GPU slots on leaf 7 are my first suspects.
kofi: If the last GPU slots on leaf 7 are the stragglers, I'll add those ranks to my kill-mid-flush test. Curious how staging handles a slow writer there.
hana: Burn-in logs show leaf 7 last-slot ranks lagging on allreduce in a few windows. Not conclusive yet, still lining up timestamps against the CRC spikes.
lucia: Once timestamps line up, send me the spike windows. If CRC bursts match the lag, I'll pull that leaf 7 optic first.
--- Mon Oct 5 · #kestrel-run ---
wen: Weekend capacity check: no nodes drained since Saturday, 2 flagged for ECC warnings but both back in the pool. Allocation table for kestrel is in the sheet, will repost after standup.
```

> **>>> DECIDE AFTER THIS:** wen: Weekend capacity check: no nodes drained since Saturday, 2 flagged for ECC warnings but both back in the pool. Allocation table for kestrel is in the sheet, will repost after standup.

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 26

**Candidates:** INTERVENE / IGNORE

**Today: Fri Oct 9** · #infra

**Team facts as of now**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Wed Sep 30 · #infra ---
mateo: ha, IB flap again. I'll pad the pickup a bit so it doesn't sit. I'll grab it and drop it at your desk.
kofi: Patch is up for review. Injected short write on a writer rank now retries instead of flipping the shard to complete. Hash lines look right in the structured log.
hana: I'll review the patch. Want to confirm the retry path doesn't stall the writer rank and skew step time during saves.
kofi: Retry runs on the flush thread, so the training step shouldn't block. I'll capture step time during the injected short write and attach it to the review.
lucia: Optics levels on the C leaf look stable so far. Still no clean window to say firmware's safe, so it stays parked.
hana: For storage sizing I'm assuming a checkpoint every 1,000 steps. Mateo, can you confirm the tier has headroom for that plus the per-shard hash sidecars?
lucia: Who should C leaf flap alerts page while firmware is parked? Right now they land in my queue only, nobody else.
wen: Whoever gets those pages should be able to trigger a drain of C nodes, otherwise it's just noise at 3am. I can be in the loop.
kofi: Page payload should list which writer ranks sit behind the C leaf, so whoever's on call can tell if a save is in flight.
lucia: I'll add the writer rank list and a drain runbook link to the C leaf page template. Still need names for who's on that rotation.
lucia: you're a lifesaver. I'll owe you next time, taco truck's on me.
mateo: Still need to answer Hana's headroom question. Pulling current tier usage now, sidecar overhead per shard is the part I haven't measured.
dmitri: Lucia, put a draft rotation in the thread. C leaf pages shouldn't sit on one person while firmware is parked. Kofi and Wen should be on it.
lucia: Draft rotation going up in the thread shortly. Kofi primary on C leaf pages, Wen as backup for drains. Shout if that's wrong.
--- Fri Oct 9 · #infra ---
hana: Post-mortem notes from Thursday's node failure are up in the doc. Loss spiked about 40 steps before the rank dropped, so I want to check whether grad-norm alerts could have caught it earlier. Kofi, can you sanity check the timeline?
```

> **>>> DECIDE AFTER THIS:** hana: Post-mortem notes from Thursday's node failure are up in the doc. Loss spiked about 40 steps before the rank dropped, so I want to check whether grad-norm alerts could have caught it earlier. Kofi, can you sanity check the timeline?

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

---

## Row 28

**Candidates:** INTERVENE / IGNORE

**Today: Fri Sep 18** · #eng

**Team facts as of now**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per human seat, agents free (changed Wed Sep 16; previously $12 per seat, agent actions metered)
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): Oli (changed Fri Sep 18; previously AJ)
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: Olavo to send the press kit to the embargoed reporters (check point: Fri Sep 18)
- open item: Sara to decide whether agents may DM a human first, without being asked (check point: Mon Sep 21 design review)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Fri Sep 18 · #eng ---
oli: nah hand it to me, you're on launch-week permissions now
frida: Related, one design partner said an agent chimed in on a sensitive hiring thread. They weren't thrilled. Want me to grab the workspace name?
alex: Yeah grab it frida. Also did the agent say anything in that thread or just join silently? Wondering what the UI showed people when it appeared.
frida: On it. From what they said it posted a short summary, so not silent. I'll ask whether it was visible to everyone in the thread.
oli: Pulled the logs for that one. Join trigger on the hiring thread was memory-sourced, not keyword. Old thread about a candidate got scored as relevant.
alex: Ok that's useful. Side note, since we're talking join behavior: the iOS app is targeting Oct 8, so mobile push for agent joins needs the same fix before then. Does a join notify people differently there?
aj: Push is a separate path from the in-app join event, so it probably doesn't inherit any gating we add. I'll check how it builds the payload.
alex: Should the agent ask before posting in a thread it wasn't invited to? Like a small 'want me to weigh in?' prompt instead of a summary.
oli: Prompt makes sense for memory-sourced joins at least. Keyword ones are closer to a direct mention, so maybe those can stay as is. Needs a gate in the join path either way.
sara: On the prompt question, there's a bigger one behind it. We'll decide whether agents may DM a human first, without being asked, at the Mon Sep 21 design review. Hold the gating design until then.
frida: Will do! They're pretty chatty on Slack-style stuff, so I'll ask about naming and whether they'd prefer a call or video.
oli: ok, so I'll keep digging on the root cause in the join path but not touch the gate itself. Will log the trigger breakdown on the board.
frida: Heard back from the design partner: the summary was visible to everyone in the hiring thread, not just the poster. They want to know if agents can be kept out of certain channels entirely.
olavo: Perfect, video's better if they're okay with it, reporters can grab a screenshot of the workspace. Also ask if they have a fav agent moment to share 😄
frida: Separate thing: a design partner hit the double-posting bug again this morning. I'll ping AJ with the details since AND-341 is his.
```

> **>>> DECIDE AFTER THIS:** frida: Separate thing: a design partner hit the double-posting bug again this morning. I'll ping AJ with the details since AND-341 is his.

**Team facts again**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per human seat, agents free (changed Wed Sep 16; previously $12 per seat, agent actions metered)
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): Oli (changed Fri Sep 18; previously AJ)
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: Olavo to send the press kit to the embargoed reporters (check point: Fri Sep 18)
- open item: Sara to decide whether agents may DM a human first, without being asked (check point: Mon Sep 21 design review)

---

## Row 29

**Candidates:** INTERVENE / IGNORE

**Today: Wed Oct 21** · #harbor

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,140 items (changed Mon Oct 19; previously 1,200 items)
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Wed Oct 21 · #harbor ---
yuki: Related caption point: a few runs hit sandbox timeouts mid-task. We should say whether those count as failures or get excluded.
elena: Some of those timeouts were on the slower nodes, so they may be infra rather than the model. I can pull the logs and tag which.
yuki: Yes please, Elena. If they're infra, I'd lean toward reporting those separately instead of counting them as model failures. Footnote it in the caption.
theo: Once Elena's tags are in, I'll add an infra-timeout column to the results table so it's separate from the failure counts.
theo: Random what-if, with the table and plot rework piling up: should we skip the workshop and aim for the main conference instead? More time to do the results properly.
nadia: Not switching. We're staying with the workshop plan. The rework is small, and I'd rather ship solid results than restart the paper for a different venue.
elena: Started on the timeout logs. Most cluster on the two slow nodes, but a few look like the model looping on a flaky test. Tagging those separately.
yuki: The looping-on-a-flaky-test ones are different, though. The model should notice and move on, so I'd keep those as failures in the table.
elena: Looping ones are easy to spot: same pytest call repeated with no edits between. I'll add a tag so they stay countable as model failures.
yuki: Might be worth a plot of steps-to-solve per task too. The looping runs would show up as a long tail there.
marcus: Heads up, I'm not doing great this week, so I might be slow to reply. Ping me directly if something is blocking on the contamination writeup.
theo: Steps-to-solve plot is doable. I'll use a log-scale x-axis so the looping tail doesn't squash everything else.
yuki: Log axis works. Label it clearly in the caption so nobody reads the tail as a linear spread.
elena: Log axis is fine, but a few runs got cut off by the timeout before finishing. I'll mark those as censored dots so they don't look like fast solves.
yuki: Censored dots sound right. Unrelated, for table 1: how many items does the held-out set have now? I want the header count to match.
```

> **>>> DECIDE AFTER THIS:** yuki: Censored dots sound right. Unrelated, for table 1: how many items does the held-out set have now? I want the header count to match.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,140 items (changed Mon Oct 19; previously 1,200 items)
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 30

**Candidates:** INTERVENE / IGNORE

**Today: Mon Oct 19** · #harbor-evals

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Wed Oct 7 · #harbor-evals ---
elena: First cached image is built for the messiest monorepo item. Installs barely register now. Trying the Python repos with native extensions next.
theo: Split the import-error bucket out of the multi-file plots. Spread tightens a lot without it. Will rerun properly once more cached images land.
elena: that's it, the stuck jobs all target pools with hyphens in the name. parser truncates at the first one. patching the regex locally to confirm.
nadia: For the paper, let's call that bucket "environment failures" rather than model errors. Reviewers will read it more kindly, and it's more accurate.
yuki: Fine by me. Should we report environment failures as a separate rate per slice, so readers see how much each slice is affected?
theo: Yes, per-slice rate works. I'll add it to the results table. Also, I put in the draft that the release gate is 75% pass@1, so the environment-failure rate sits right next to it.
theo: nice, that matches what I saw on my branch. once the patch works, add a test with a hyphenated pool name so it doesn't regress.
elena: One of the native-extension repos needs a system lib missing from the base image. Patching that now, so the cached image for it is slower than the others.
felix: Cached image digests should go in the manifest too, so anyone rerunning gets the exact same environment. I'll add a field for it.
elena: patch works, stuck jobs scheduled right away. adding the hyphenated pool test now, then I'll requeue the dropped batch.
felix: With the cached images, the license exclusions and the new manifest fields, this might warrant v1.3 for the release. Just a thought, nothing decided. Nadia, Yuki, does that numbering seem right to you?
yuki: Theo, the gate number in your draft doesn't match my criteria doc, and it's missing the held-out qualifier. Please recheck before the table gets built around it.
theo: nice. worth grepping the other label parsers for the same split-on-hyphen pattern, wouldn't be surprised if the GPU type one does it too.
theo: Ugh, I pulled that number from an older draft. Rechecking against your criteria doc and adding the held-out qualifier before I build the table.
--- Mon Oct 19 · #harbor-evals ---
yuki: Went through the weekend results. Pass rate curves look clean across the board, but the long-horizon tasks have a weird plateau. Might be worth a sentence in the paper on that.
```

> **>>> DECIDE AFTER THIS:** yuki: Went through the weekend results. Pass rate curves look clean across the board, but the long-horizon tasks have a weird plateau. Might be worth a sentence in the paper on that.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---
