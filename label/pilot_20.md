# Rubric pilot: 20 decision points

For each row, read the team facts and the recent messages, then decide what an AI teammate with perfect memory should do right after the **last** message: IGNORE, TRACK or INTERVENE, plus severity 1-3 (TRACK is always 1). Use rubric.md. Fill in label/pilot_20_labels.csv.

## Row 1

**Team facts as of now**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

**Recent messages** (the last one is the decision point)

```
--- Thu Sep 10 · #eng ---
oli: Starting the launch-readiness checklist for the agent runtime. Three open items: DM permissions, the double-posting bug, memory store under load. Want status on each before standup.
aj: DM permissions: the core check is in, but I'm still tracing an edge case where an agent gets added to a group DM after it's already started.
alex: For that group DM edge case, what does the user see if the agent is added late? Does it get history or start blank? Asking for the onboarding copy.
aj: Right now it starts blank. History backfill is the part I'm tracing, since it touches the same permission check as the other DM cases.
aj: Policy for the permission check, so we're all building against the same rule: agents never read a DM unless a participant forwards it. That covers late-added agents too, so blank start is correct, no backfill.
alex: Got it, I'll write the late-add copy around a blank start. Should the agent post a short note saying it can't see earlier messages?
aj: A note works, but keep it generic. It shouldn't hint at what was said earlier, only that the agent joined late.
oli: Double-posting: repro'd it again locally. Looks like two agents both answering the same unaddressed message in a channel. Ticket's up, digging into the runtime dedupe.
frida: Fwiw one design partner hit that double reply last week, two bots answered the same question in their ops channel. They found it funny, but still.
oli: Who can take AND-341 (agent double-posts in threads)? Needs an owner before standup.
frida: hey Alex, for the design-partner lunch, any thoughts on format? Thinking casual, maybe demo corner so folks can poke at the agents 🙂
```

## Row 2

**Team facts as of now**

- kestrel pretraining run (start date): Oct 12
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

**Recent messages** (the last one is the decision point)

```
--- Mon Oct 5 · #kestrel-run ---
kofi: Bigger vocab means the embedding shard layout changes, so I want to retest resharding on restore. Does it pad to a multiple of the TP degree?
dmitri: Actually make that Oct 12, not Oct 5. Fabric firmware rollout needs another week.
wen: Then the reserved block sits idle until the new start. Release it to the pool for backfill meanwhile, or keep holding?
lucia: Rollout is staged spine first, leaves after. Still seeing occasional link flaps on the old leaf image, so NCCL busbw will wobble until then.
kofi: Slip gives me time to run the resharding restore test on the bigger vocab layout. Still need an answer on padding to the TP degree.
kofi: With start now Oct 12, I'll move the restart drill to the week before, so the resharding restore test on the new vocab layout runs on the upgraded fabric.
mateo: Cross-checked shard IDs against the spike steps. They line up with the same handful of Python-heavy shards from the dedup pass, so it's shard-specific, not code in general.
hana: Shard-specific is good news then. Might be mixed tabs and spaces from the dedup pass, not the vocab. Can you diff tokenization on those shards?
mateo: Will do. I'll diff both tokenizers on those shards and count tab vs space runs in the indented blocks.
lucia: Flaps cluster on a few leaf uplinks in one row. CRC errors climbing on those ports, so I'm suspecting optics rather than the old image alone.
wen: If it's optics, which nodes sit behind those leaf uplinks? I can cross-check them against the reserved block and the ECC-flagged ones.
lucia: I can dump the port-to-node map for that row from the fabric manager. Optics swap would mean draining whatever sits behind those leaves.
mateo: I'll kick off data loading tonight since kestrel starts today, Oct 5. The tokenizer diff on those shards can run alongside it.
lucia: Port-to-node map for that row is dumped to the sheet. CRC errors all sit on optics from the same vendor lot.
wen: Overlaying the map on the ECC-flagged nodes. Some of them sit behind those same leaves, so maybe not coincidence.
```

## Row 3

**Team facts as of now**

- kestrel pretraining run (start date): Oct 12
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

**Recent messages** (the last one is the decision point)

```
--- Mon Oct 5 · #kestrel-run ---
kofi: Slip gives me time to run the resharding restore test on the bigger vocab layout. Still need an answer on padding to the TP degree.
kofi: With start now Oct 12, I'll move the restart drill to the week before, so the resharding restore test on the new vocab layout runs on the upgraded fabric.
mateo: Cross-checked shard IDs against the spike steps. They line up with the same handful of Python-heavy shards from the dedup pass, so it's shard-specific, not code in general.
hana: Shard-specific is good news then. Might be mixed tabs and spaces from the dedup pass, not the vocab. Can you diff tokenization on those shards?
mateo: Will do. I'll diff both tokenizers on those shards and count tab vs space runs in the indented blocks.
lucia: Flaps cluster on a few leaf uplinks in one row. CRC errors climbing on those ports, so I'm suspecting optics rather than the old image alone.
wen: If it's optics, which nodes sit behind those leaf uplinks? I can cross-check them against the reserved block and the ECC-flagged ones.
lucia: I can dump the port-to-node map for that row from the fabric manager. Optics swap would mean draining whatever sits behind those leaves.
mateo: I'll kick off data loading tonight since kestrel starts today, Oct 5. The tokenizer diff on those shards can run alongside it.
lucia: Port-to-node map for that row is dumped to the sheet. CRC errors all sit on optics from the same vendor lot.
wen: Overlaying the map on the ECC-flagged nodes. Some of them sit behind those same leaves, so maybe not coincidence.
lucia: Same row could mean a shared cooling issue. I'll pull transceiver temps on those ports and compare against the ECC-flagged nodes' inlet temps.
hana: If temps line up, check DCGM for clock throttling on those nodes too. Throttled GPUs would show up as stragglers in step time.
lucia: Transceiver temps on those ports run hot compared to the rest of the row. Could be a missing blanking panel at the rack.
dmitri: We'll decide between tokenizer v3 and v4 for kestrel at the Thu Oct 8 run sync. Mateo, have the shard diff ready by then. Kofi, get the TP padding answer to the group before.
```

## Row 4

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list
- Northwind executive sponsor (person): Jon Reyes (new CTO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

**Recent messages** (the last one is the decision point)

```
--- Mon Oct 19 · #acct-northwind ---
keiko: Security lead also asked if the changelog can come as a spreadsheet instead of a PDF. Their reviewers like to filter by vendor.
ines: Spreadsheet is fine by me. I'd want a confidentiality note on the first tab, and the entries should match the addendum wording exactly.
darnell: On our side, I'm happy to ping their exec sponsor before signature if it helps close out the security packet questions.
rachel: That would help, Darnell. Keep it to the security packet and the process, nothing on terms. I'll loop you in on the thread.
keiko: Their ops lead offered to join the burst call and bring someone from the check-in app team, since that's what fires the requests.
gabe: Perfect, having the check-in app team on the call helps. I want to ask how their client retries when a request gets throttled.
keiko: I'll ask their app team whether the check-in client backs off on throttling or just retries right away. Will pass along what they say.
rachel: Let's keep the burst call about how throttling behaves, not a limits renegotiation. They're already getting 18% off list, so I don't want new asks sneaking in late.
rachel: *correction: it's 15% off list, not 18%. Tomas, please confirm against the order form so nobody quotes the wrong number to Northwind.
tomas: Understood, Rachel. I'm pulling the order form now and will post the discount exactly as it is written there.
keiko: App team replied: the check-in client retries right away with a little jitter, no real backoff. Ops lead seemed a bit sheepish about it.
gabe: Thanks, that's the key detail. Immediate retries pile onto a spike, so I'll suggest exponential backoff on their client. A small fix on their side.
keiko: Their ops lead asked if we can send a short doc on recommended backoff settings, something the app team can hand to their devs.
gabe: Happy to write it. I'll keep it to a one-pager with example backoff and jitter settings plus a short code snippet their devs can paste in.
keiko: Heads up, I have a personal matter to handle tomorrow and can't make the call. Can someone cover for me? Happy to send a quick brief tonight.
```

## Row 5

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list
- Northwind executive sponsor (person): Jon Reyes (new CTO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

**Recent messages** (the last one is the decision point)

```
--- Thu Oct 15 · #acct-northwind ---
keiko: Will do. Their admin said she'd ask around the team and get back to me. I'll flag it as soon as I hear.
keiko: Learned it on a call this morning, in passing. No read yet on whether the new CTO backs the expansion plans.
darnell: Good catch, Keiko. Does anyone on our side have a relationship with the new person yet? Might need an intro before the QBR.
gabe: Haven't met him. Their platform lead might know him though. I can ask when we sync on the integration work.
rachel: Good idea, Gabe. Also, the term pitch may need rework if the new exec hasn't bought in. Keiko, any sense of his priorities?
keiko: Not yet. Only heard he came from a different health system. I can ask their procurement lead what he cares about most.
tomas: Should I hold the multi-year model until we know whether the new exec wants that structure, or build both anyway?
darnell: Fine either way. If the back room is taken, I know a second place with a quiet corner. Less private but good food.
rachel: I'd lean toward building both, since the model is cheap. Just keep the multi-year one internal until we know where the new exec lands.
rachel: Timeline: we decide whether to offer Northwind a two-year term after the Fri Oct 16 finance review. Tomas, have both models ready for that so we're not scrambling.
keiko: Either works for me. The quiet corner might actually feel more relaxed for them. I'll pass both options along once I hear back on the dietary thing.
tomas: Understood. I'll build both models so they're ready for the review, with the volume-band language Ines asked for in each order form draft.
ines: Worth checking whether the new exec's arrival reopens any security or compliance review on their side. That could shift how they read the contract terms.
gabe: Good call, Ines. Their security team did a pretty thorough architecture review last time, so I'd expect questions on data flow again.
darnell: I'll send the QBR deck to Amara Okafor once the term section is locked. Better she sees it from me than cold.
```

## Row 6

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list
- Northwind executive sponsor (person): Jon Reyes (new CTO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

**Recent messages** (the last one is the decision point)

```
--- Mon Oct 19 · #acct-northwind ---
keiko: Their ops lead offered to join the burst call and bring someone from the check-in app team, since that's what fires the requests.
gabe: Perfect, having the check-in app team on the call helps. I want to ask how their client retries when a request gets throttled.
keiko: I'll ask their app team whether the check-in client backs off on throttling or just retries right away. Will pass along what they say.
rachel: Let's keep the burst call about how throttling behaves, not a limits renegotiation. They're already getting 18% off list, so I don't want new asks sneaking in late.
rachel: *correction: it's 15% off list, not 18%. Tomas, please confirm against the order form so nobody quotes the wrong number to Northwind.
tomas: Understood, Rachel. I'm pulling the order form now and will post the discount exactly as it is written there.
keiko: App team replied: the check-in client retries right away with a little jitter, no real backoff. Ops lead seemed a bit sheepish about it.
gabe: Thanks, that's the key detail. Immediate retries pile onto a spike, so I'll suggest exponential backoff on their client. A small fix on their side.
keiko: Their ops lead asked if we can send a short doc on recommended backoff settings, something the app team can hand to their devs.
gabe: Happy to write it. I'll keep it to a one-pager with example backoff and jitter settings plus a short code snippet their devs can paste in.
keiko: Heads up, I have a personal matter to handle tomorrow and can't make the call. Can someone cover for me? Happy to send a quick brief tonight.
rachel: I'll cover for Keiko. Keiko, in the brief just list who's attending from their side and what the ops lead is most worried about.
keiko: Thank you, Rachel. Brief coming tonight. Their ops lead's biggest worry is patients seeing error screens at the check-in kiosk during a rush.
gabe: That worry is useful. I'll frame the one-pager around keeping kiosk check-ins smooth during a rush, so their app team sees why it matters.
gabe: Quick one before we wrap: who's the exec contact at Northwind now? I want to cc them on the renewal thread when I send the one-pager.
```

## Row 7

**Team facts as of now**

- kestrel pretraining run (start date): Oct 12
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

**Recent messages** (the last one is the decision point)

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

## Row 8

**Team facts as of now**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

**Recent messages** (the last one is the decision point)

```
--- Thu Sep 10 · #eng ---
aj: No baseline yet. I have a read-heavy test script but it only simulates a handful of agents. Need to scale it up first.
oli: There's an agent-sim harness in the runtime tests that spawns fake agents with canned channel traffic. Might save you rebuilding. Check if it fits your script.
frida: Yes! Name cards are great. One partner mentioned she'd love to see an agent jump into a thread unprompted, so maybe a script for that moment 😄
aj: Thanks, I'll try the sim harness for the load test. Also, on DM permissions: I'll merge the forwarded-DM permission check by Tue Sep 15, late-add edge case included.
alex: Ooh, unprompted jump-in is the best demo. Should we seed a thread where two humans are stuck on something, so the agent has a natural reason to chime in?
frida: Related to the load test: one partner runs a ton of agents in a single workspace and said memory lookups felt laggy during their Monday standup rush.
oli: That lag report is useful. Frida, do you know if their agents were all reading the same memory entries or spread out? Changes how I'd shape the load test.
frida: Good question, not sure. I'll ask them which channels the agents were hitting during the rush and get back to you.
frida: Yes, something relatable like two people arguing over which snack order to get for the lunch 😂 agent jumps in with a tally
alex: Slightly random, but does the agent typing indicator also fire for the double replies? Would be good to know for the onboarding demo.
oli: Alex: yes, typing indicator fires per agent, so you'd see two bubbles for a double reply. Not great for a demo, I'd avoid that scenario.
alex: Haha perfect. Should I mock up the snack thread in the sandbox so the agent's reply looks natural on screen? I can draft it.
olavo: For the launch post, can I show agents joining a thread on their own? Want a clean gif, no double bubbles obviously 😅
oli: Olavo: thread-join gif is fine as long as only one agent is in the channel. Use a single-agent demo workspace.
frida: Yes please! Draft it and I'll run it past a couple of partners to see if the snack banter feels real 😊
```

## Row 9

**Team facts as of now**

- kestrel pretraining run (start date): Oct 12
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

**Recent messages** (the last one is the decision point)

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

## Row 10

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list
- Northwind executive sponsor (person): Jon Reyes (new CTO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

**Recent messages** (the last one is the decision point)

```
--- Thu Oct 15 · #acct-northwind ---
keiko: Learned it on a call this morning, in passing. No read yet on whether the new CTO backs the expansion plans.
darnell: Good catch, Keiko. Does anyone on our side have a relationship with the new person yet? Might need an intro before the QBR.
gabe: Haven't met him. Their platform lead might know him though. I can ask when we sync on the integration work.
rachel: Good idea, Gabe. Also, the term pitch may need rework if the new exec hasn't bought in. Keiko, any sense of his priorities?
keiko: Not yet. Only heard he came from a different health system. I can ask their procurement lead what he cares about most.
tomas: Should I hold the multi-year model until we know whether the new exec wants that structure, or build both anyway?
darnell: Fine either way. If the back room is taken, I know a second place with a quiet corner. Less private but good food.
rachel: I'd lean toward building both, since the model is cheap. Just keep the multi-year one internal until we know where the new exec lands.
rachel: Timeline: we decide whether to offer Northwind a two-year term after the Fri Oct 16 finance review. Tomas, have both models ready for that so we're not scrambling.
keiko: Either works for me. The quiet corner might actually feel more relaxed for them. I'll pass both options along once I hear back on the dietary thing.
tomas: Understood. I'll build both models so they're ready for the review, with the volume-band language Ines asked for in each order form draft.
ines: Worth checking whether the new exec's arrival reopens any security or compliance review on their side. That could shift how they read the contract terms.
gabe: Good call, Ines. Their security team did a pretty thorough architecture review last time, so I'd expect questions on data flow again.
darnell: I'll send the QBR deck to Amara Okafor once the term section is locked. Better she sees it from me than cold.
keiko: Their procurement lead also wants a usage breakdown by clinical department in the QBR. Gabe, can we pull that from the dashboards?
```

## Row 11

**Team facts as of now**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

**Recent messages** (the last one is the decision point)

```
--- Wed Sep 30 · #infra ---
(kofi reacted ✅ to hana's message)
lucia: Not seeing NCCL timeouts yet, just symbol errors and retrains on a couple of C uplinks. Checking cable seating before touching firmware.
kofi: Good. If those C uplinks retrain mid-save, I'd expect partial shards on the writer ranks. I'll check how the async flush handles a stalled write.
wen: Who's owning fabric incident on-call for kestrel right now? I need a name on the rota before I lock the allocation table.
mateo: lunch? thinking the taco truck by the loading dock, it's been parked there all week
lucia: I'll take it.
kofi: Also want to confirm the async flush path retries on a short write instead of silently marking the shard complete. Looking at the writer rank logs now.
lucia: Reseated one of the C uplinks, symbol errors dropped on that port. Still watching the other. Will hold firmware until counters stay clean.
kofi: Found it: on a short write the flush thread logs a warning but still flips the shard to complete. Need to patch that before we trust any save from C.
lucia: taco truck again? the line there was brutal yesterday. I'd rather do the noodle place, it's faster
hana: That's bad for resume too. If a partial shard gets marked complete, we'd only see it as a loss spike after restart. Can we add a checksum verify on load?
kofi: Yes, checksum on load makes sense. I'll write per-shard hashes at flush time and verify on resume, so a bad shard fails loudly instead of loading.
mateo: the noodle place is a 15 min walk though, and the line there moves slow when the lunch crowd from the other building shows up
hana: Hash verify adds load-time cost on resume. Worth timing it on a big shard set so restart latency doesn't balloon.
wen: @dmitri what's the kestrel start date? Need it to lock the allocation table and size the reservation window.
```

## Row 12

**Team facts as of now**

- kestrel pretraining run (start date): Oct 12
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

**Recent messages** (the last one is the decision point)

```
--- Mon Oct 5 · #kestrel-run ---
lucia: Flaps cluster on a few leaf uplinks in one row. CRC errors climbing on those ports, so I'm suspecting optics rather than the old image alone.
wen: If it's optics, which nodes sit behind those leaf uplinks? I can cross-check them against the reserved block and the ECC-flagged ones.
lucia: I can dump the port-to-node map for that row from the fabric manager. Optics swap would mean draining whatever sits behind those leaves.
mateo: I'll kick off data loading tonight since kestrel starts today, Oct 5. The tokenizer diff on those shards can run alongside it.
lucia: Port-to-node map for that row is dumped to the sheet. CRC errors all sit on optics from the same vendor lot.
wen: Overlaying the map on the ECC-flagged nodes. Some of them sit behind those same leaves, so maybe not coincidence.
lucia: Same row could mean a shared cooling issue. I'll pull transceiver temps on those ports and compare against the ECC-flagged nodes' inlet temps.
hana: If temps line up, check DCGM for clock throttling on those nodes too. Throttled GPUs would show up as stragglers in step time.
lucia: Transceiver temps on those ports run hot compared to the rest of the row. Could be a missing blanking panel at the rack.
dmitri: We'll decide between tokenizer v3 and v4 for kestrel at the Thu Oct 8 run sync. Mateo, have the shard diff ready by then. Kofi, get the TP padding answer to the group before.
wen: Cordoning the nodes behind those leaves in the scheduler now so nothing gets placed there while we sort out cooling and optics.
kofi: Mateo, the start slipped for the firmware rollout, so no need to kick off data loading tonight. The shard diff matters more right now.
mateo: Right, I was working off the old start. Skipping the loader launch tonight, running the tab/space diff on those shards first.
lucia: Confirmed, blanking panels are missing in that row. Filing a facilities ticket. I'll re-check CRC counters on those ports once temps settle.
wen: What if we start on half the nodes Oct 7 and add the rest after the firmware lands? Cordoned ones stay out either way. Is that worth considering?
```

## Row 13

**Team facts as of now**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered

**Recent messages** (the last one is the decision point)

```
--- Tue Sep 8 · #launch ---
(sara reacted 👍 to olavo's message)
oli: fyi the member list currently sorts agents below humans alphabetically. might want to pin the agent higher for new workspaces, ticket coming
alex: good catch Oli. pinning the agent up top in the member list would fit with the welcome card too, I'll sketch both together 🙂
sara: Next up: who's taking the launch waitlist email? Need one owner for it.
olavo: I'll grab it 🙌
frida: For the waitlist email, can we mention the agent shows up in the member list? That's what tripped up my design partners 😅
alex: Good idea Frida. I could make a small screenshot of the member list with the agent pinned for the email, if Olavo wants it 📸
sara: Pricing: $12 per seat. That's what goes in the launch post and the waitlist email.
aj: Does the waitlist email need to say anything about what the agent can see? A few people will ask about channel access vs private conversations.
sara: Also, agent actions get metered on top of the per-seat number. Olavo, make sure that's in both the post and the email.
aj: Still need an answer on my question about what the agent can see. People will ask, and I'd rather the email wording be exact.
olavo: Sara, can you take AJ's access question? I'd like the exact wording before I draft the email copy 🙏
alex: meanwhile I'm sketching the pricing page. $15 per seat up top, with a small note under it about agent actions being metered 💸 will drop the mock here soon
frida: One design partner asked if they can mute the agent in a single channel without removing it. Worth a line in the FAQ?
frida: Separate from the FAQ: I'll send design partners the Slack-to-Ando migration guide by Fri Sep 11, so they have time to try it before launch 🙂
```

## Row 14

**Team facts as of now**

- kestrel pretraining run (start date): Oct 12
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

**Recent messages** (the last one is the decision point)

```
--- Mon Oct 12 · #kestrel-run ---
hana: Will do, Kofi. I've tagged the first flush window in the step-time panel so I can diff it against the next save once jitter's in.
wen: Pulling per-node ECC and thermal counters across the allocation. A throttling GPU would show up as a slow rank before anything else.
lucia: Fabric is mine today. Paste the dataloader node names and flap timestamps, I'll cross-check against the leaf counters.
mateo: Pasting now. Flaps hit two of the loader nodes in the same rack, timestamps line up with the first few prefetch bursts. No retransmit errors in the dataloader logs though.
lucia: Thanks. Checking those two against the leaf port counters now. If they share a ToR, could be a bad optic or a dirty connector.
hana: Step time on the two ranks fed by those loader nodes looks flat so far. If the flaps stall prefetch, I'd expect a blip there first.
lucia: Both loader nodes sit under the same ToR. Port counters show CRC errors climbing on one of the optics. Looks like a marginal transceiver.
mateo: Makes sense. Can we swap that optic or drain those two loader nodes? Prefetch queues have headroom, so I can rebalance workers onto the others.
lucia: Swapping the optic needs a tech at the rack. I'd drain those two loader nodes first, then pull the transceiver and reseat the connector.
hana: If a crash lands mid-drain, we lose at most 500 steps of work, since checkpoints go every 500 steps. Worst case that's a few minutes of recompute at current step time. Fine to proceed with the drain.
mateo: Starting the drain on those two loader nodes now. Rebalancing dataloader workers onto the remaining hosts, will watch prefetch queue depth as it shifts.
lucia: Once the drain completes I'll send a tech to the rack for the transceiver. Keeping CRC counters on that ToR under watch in the meantime.
wen: ECC and thermal counters look clean across the allocation so far. No throttling ranks, MFU is holding steady while the loaders drain.
mateo: Drain's progressing. Prefetch queue depth on the remaining loaders is climbing a bit but still has headroom, no stalls on the consumer side.
lucia: Drain looks complete on my side. Tech is heading to the rack now; CRC counters on that ToR are still ticking up on the suspect optic.
```

## Row 15

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Gabe to load-test Northwind's workload at their full rate limit (check point: Wed Oct 14)

**Recent messages** (the last one is the decision point)

```
--- Tue Oct 6 · #acct-northwind ---
gabe: Fair warning, the QBR deck is already at like 40 slides. Pretty sure the nurse manager's quote is getting its own slide at this point.
rachel: Gabe, cut it to a handful of slides. Execs skim. Keep the nurse manager quote and the usage trend, drop the rest to appendix.
gabe: Will do. I'll keep the usage trend to one clean chart and move the per-team breakdown to the appendix.
tomas: Once Gabe's peak-hour view is in, I'll model a couple of pricing scenarios. Keiko, any sense yet whether they're comparing us against another vendor?
keiko: Not sure yet. Their informatics lead mentioned procurement asked about other vendors' demos, but nothing concrete. I'll try to learn more on the next call.
darnell: If another vendor is in the mix, I'd like to know before I reach out. Keiko, anything on who's demoing would help.
keiko: Will push on it. I'll ask casually which vendors came through, maybe through their informatics lead since she's friendly with us.
keiko: Also, on the procurement side: I hinted at 20% off list to their procurement lead on our last call, just to set expectations. She didn't push back. Tomas, that should fit your pricing scenarios.
darnell: Gabe, once the QBR deck is trimmed, send me the exec summary version. I want to preview it before the sponsor meeting.
gabe: Sure, Darnell. I'll write the exec summary around adoption and the burst patterns, keep the technical detail light.
tomas: Keiko, please hold off on floating any discount figures with procurement until my scenarios are done. Nothing is approved on my side yet.
keiko: Understood, Tomas. I'll stay off numbers with procurement until your scenarios are ready. Sorry, that was getting ahead of the process.
rachel: Thanks for owning that, Keiko. Tomas, ping me when the scenarios are drafted so I can sanity-check against where procurement's head is.
tomas: Will do, Rachel. I'll draft a conservative and a stretch scenario, and note which assumptions depend on Gabe's burst data.
--- Mon Oct 12 · #acct-northwind ---
darnell: Weekly pipeline note: Northwind is still our biggest renewal this quarter. Their finance team is pushing back on the discount, so let's get aligned before anything goes back to them. Rachel, where are we on the order form draft?
```

## Row 16

**Team facts as of now**

- public launch (date): Sep 24
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per human seat, agents free
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): Oli
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: Olavo to send the press kit to the embargoed reporters (check point: Fri Sep 18)

**Recent messages** (the last one is the decision point)

```
--- Fri Sep 18 · #eng ---
aj: Is it the join heuristic firing on keyword match, or is it the memory store surfacing old threads as relevant? Those look the same from outside.
frida: Yes, I think two of them would be up for it! One is a small design agency that loves the agent memory stuff. Let me ask them today.
aj: fwiw I'm still on AND-341, the double-posting thing, so I'll get to the join logic soon. Might be related though, double posts could be two triggers firing at once.
oli: Good question aj. Logs show join events with a trigger field, checking now which ones are keyword vs memory-sourced. Double posts might share a trigger id too.
olavo: Awesome! The agency one sounds perfect, reporters love a creative-team angle. Can you ask if they're okay being named in the piece?
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
```

## Row 17

**Team facts as of now**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

**Recent messages** (the last one is the decision point)

```
--- Wed Sep 30 · #infra ---
lucia: Firmware rollout on the IB leaf switches is staged but not pushed. Seeing a few flapping links on rack group C that I want to look at first.
```

## Row 18

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30

**Recent messages** (the last one is the decision point)

```
--- Tue Oct 6 · #acct-northwind ---
rachel: Kicking off the Northwind renewal thread. Want one place for timeline, pricing, sponsor, and paperwork. Keiko, any early signals from their side?
keiko: Yes, a couple. Their clinical informatics lead mentioned on our last call that usage has grown a lot since the pilot teams went live. Sounds happy overall.
gabe: Good sign. Growth like that usually means we should check their rate limit headroom before we talk renewal. Want me to pull usage trends?
rachel: Yes please, Gabe. Timeline note for everyone: the Northwind renewal signature deadline is Oct 30. Working back from that for pricing, legal review, and sponsor sign-off.
gabe: On it. I'll also check whether any of their pilot teams are bursting at peak hours, since that's usually where throttling shows up first.
tomas: Once Gabe's usage numbers are in, I'll draft the pricing options for the order form. Rachel, any sense of how aggressive they'll be on discount?
rachel: Honestly not sure yet. Their procurement team pushed hard last cycle, so I'd expect them to open with a big ask.
rachel: Tomas, quick check before we plan the negotiation: is the Northwind discount currently 18% off list? Want to confirm before I anchor anything with them.
tomas: Yes, that is correct.
```

## Row 19

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Gabe to load-test Northwind's workload at their full rate limit (check point: Wed Oct 14)

**Recent messages** (the last one is the decision point)

```
--- Thu Oct 8 · #acct-northwind-eng ---
rachel: Yes, saw it. Ouch. Makes me wonder if Northwind's team has backoff with jitter on their side. Worth a quick check with them?
gabe: Good point. I'll ask their ops lead for de-identified sample forms so we can compare the smaller model without touching real patient records.
ines: Also, that applies to all endpoints, batch included, so the same coverage holds if they move the form-filling there.
keiko: Great, I'll ask their ops lead for the de-identified forms and mention the stagger idea when I send the snippet.
gabe: Also spotted their retry loop has no max attempts, so one stuck request can hang an entire intake session. I'll add a cap to the snippet.
keiko: Their ops lead will love the cap. Last week she said a frozen intake session meant staff fell back to paper forms.
gabe: Also worth adding a client-side timeout so a hung call fails fast instead of sitting there. I'll put that in the snippet too.
gabe: Good call. Last time I looked at their integration, they had a fixed 1s retry with no jitter. Could be worth a gentle nudge.
keiko: Perfect. Their ops lead also mentioned the assistant gives no feedback while waiting, so staff just stare at a blank screen. Any UX tip there?
gabe: Streaming responses plus a "working on it" spinner fixes most of that. Separately, I'll load-test Northwind's workload at their full rate limit and have results by Wed Oct 14.
keiko: Streaming plus a spinner is an easy sell. Their ops lead said staff just want to know it's alive, not faster.
rachel: Yeah, a fixed interval with no jitter is exactly how those pile up. Could you put together a short backoff snippet I can send Keiko?
rachel: Good. I'll frame this in the renewal conversation as proactive tuning, not a capacity problem. Keeps the upsell door open.
keiko: Their ops lead also asked whether the assistant can flag when a form comes back with missing fields instead of silently moving on.
keiko: Gabe, can the assistant flag missing fields? If it misfires they'll want to debug, and logs will be available since Northwind is on standard 30-day retention. I'll tell their ops lead.
```

## Row 20

**Team facts as of now**

- kestrel pretraining run (start date): Oct 12
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

**Recent messages** (the last one is the decision point)

```
--- Mon Sep 28 · #kestrel-run ---
kofi: If the last GPU slots on leaf 7 are the stragglers, I'll add those ranks to my kill-mid-flush test. Curious how staging handles a slow writer there.
hana: Burn-in logs show leaf 7 last-slot ranks lagging on allreduce in a few windows. Not conclusive yet, still lining up timestamps against the CRC spikes.
lucia: Once timestamps line up, send me the spike windows. If CRC bursts match the lag, I'll pull that leaf 7 optic first.
--- Mon Oct 5 · #kestrel-run ---
wen: Weekend capacity check: no nodes drained since Saturday, 2 flagged for ECC warnings but both back in the pool. Allocation table for kestrel is in the sheet, will repost after standup.
hana: Tokenizer question again: the 100k vocab run shows noisier loss on code-heavy shards in the small-scale ablation. Anyone looked at the per-domain curves?
mateo: I pulled the per-domain curves last week. Code shards spike right after the Python-heavy batches, looks like whitespace tokens fragmenting differently in the bigger vocab.
hana: Whitespace fragmentation would explain it. Are the spikes aligned with specific shard IDs, or just any batch heavy on indented Python?
mateo: Mostly specific shards, I think. Same few Python-heavy ones from the scrape dedup pass. I'll cross-check shard IDs against the spike steps.
wen: Table's reposted in the sheet. It assumes kestrel pretraining starts Oct 5, so the reserved block stays held from today. Tokenizer choice doesn't change the allocation, only the embedding shard layout.
kofi: Bigger vocab means the embedding shard layout changes, so I want to retest resharding on restore. Does it pad to a multiple of the TP degree?
dmitri: Actually make that Oct 12, not Oct 5. Fabric firmware rollout needs another week.
wen: Then the reserved block sits idle until the new start. Release it to the pool for backfill meanwhile, or keep holding?
lucia: Rollout is staged spine first, leaves after. Still seeing occasional link flaps on the old leaf image, so NCCL busbw will wobble until then.
kofi: Slip gives me time to run the resharding restore test on the bigger vocab layout. Still need an answer on padding to the TP degree.
kofi: With start now Oct 12, I'll move the restart drill to the week before, so the resharding restore test on the new vocab layout runs on the upgraded fabric.
```
