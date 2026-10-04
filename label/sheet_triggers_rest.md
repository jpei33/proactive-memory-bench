# Labeling sheet: triggers_rest (32 rows)

For each row, decide what an AI teammate with perfect memory should do right after the marked **decision message**: IGNORE, TRACK or INTERVENE, plus severity 1-3 (TRACK is always 1). Follow rubric.md (read it first). Notes are optional: for INTERVENE say which fact you act on, for TRACK what to check and by when, and flag anything you were unsure about.

Suggested order for each row:
1. Read the decision message. Note any date, number, name, owner, ticket, price or promise in it.
2. Look each one up in the team facts (shown again below the messages). Different from the current value = contradiction; matches a "previously" value = stale; asks about something already in the facts = repeat question.
3. Compare open items' check points with Today.
4. Scan the recent messages: already corrected or answered? self-correction? proposal? addressed to a specific person? personal? -> IGNORE (tie-breaks 1-3, 11, 12).
5. Nothing triggered -> IGNORE, unless the message opens a new commitment with an owner and a check point -> TRACK.

## Row 1

**Today: Mon Oct 19** · #acct-northwind

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 19 · #acct-northwind ---
keiko: From what ops described, it's a sharp spike right when doors open. I'll ask if they have a rough traffic graph from last quarter.
gabe: A sharp spike like that is the case I'd want to walk them through. A graph would help me show how it looks on our side.
rachel: Good. If the graph shows the spike clearly, let's fold it into the security packet so they stop asking in pieces.
gabe: Quick one so I can plan the burst call: what's the date Northwind needs to sign by for the renewal?
keiko: Security lead replied on the sub-processor question: they want the addendum version, and they'd like a changelog of recent additions too.
ines: The changelog is fine in principle. I want to check how the addendum handles notice of new sub-processors before it goes in their packet.
keiko: Security lead also asked if the changelog can come as a spreadsheet instead of a PDF. Their reviewers like to filter by vendor.
ines: Spreadsheet is fine by me. I'd want a confidentiality note on the first tab, and the entries should match the addendum wording exactly.
darnell: On our side, I'm happy to ping their exec sponsor before signature if it helps close out the security packet questions.
rachel: That would help, Darnell. Keep it to the security packet and the process, nothing on terms. I'll loop you in on the thread.
keiko: Their ops lead offered to join the burst call and bring someone from the check-in app team, since that's what fires the requests.
gabe: Perfect, having the check-in app team on the call helps. I want to ask how their client retries when a request gets throttled.
keiko: I'll ask their app team whether the check-in client backs off on throttling or just retries right away. Will pass along what they say.
rachel: Let's keep the burst call about how throttling behaves, not a limits renegotiation. They're already getting 18% off list, so I don't want new asks sneaking in late.
rachel: *correction: it's 15% off list, not 18%. Tomas, please confirm against the order form so nobody quotes the wrong number to Northwind.
```

> **>>> DECIDE AFTER THIS:** rachel: *correction: it's 15% off list, not 18%. Tomas, please confirm against the order form so nobody quotes the wrong number to Northwind.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

---

## Row 2

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

## Row 3

**Today: Mon Oct 19** · #harbor-evals

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,140 items (changed Mon Oct 19; previously 1,200 items)
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)
- open item: Nadia to decide whether the 3-shot results go in the paper (check point: Tue Oct 20 paper sync)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 19 · #harbor-evals ---
yuki: Once the ids are in, can you also log which categories each removal came from? I'd like that next to the plateau figure.
theo: Got it, I'll add a category column to the export so the removal counts sit beside the per-category pass rates. Plateau figure should line up then.
felix: Good, I'll find traces where the agent loops on a flaky test. Those make better discussion than clean passes. Lake house is looking good.
elena: If the tables regenerate, do the plateau curves need a rerun too, or are those computed from cached trajectories?
theo: Curves come from cached trajectories, so no rerun. Just refilter by id and regenerate. Only the plateau figure needs a fresh pass with the smaller denominator.
yuki: Before the refilter, can someone check the build-loop task I picked for the transcript isn't among the removed ids? Awkward to show a task we dropped.
marcus: Good catch. That build-loop task is a CLI tooling repo, not a web-app fork, so it's likely fine. I'll grep the id file against it to be sure.
theo: Dataset section in the draft says 1,200 items, so I'm building the tables to match that. Will grep the plateau task id once Marcus's file is up.
yuki: Drafting the plateau sentence meanwhile. I'd say agents "stall in repair loops" rather than "hit a ceiling", since ceiling implies a capability limit we haven't shown.
yuki: Sounds good. I'll send you the lake house contact so you can ask about projector and screen setup before we lock it in.
nadia: I like "repair loops" better than "ceiling". Could we tie it to the wrong-config-file example in the figure caption?
yuki: Caption works. I'd annotate the transcript excerpt where the agent edits the wrong config, then reruns the identical build command, so readers see the loop.
theo: I'll keep the stderr in that excerpt so the same build error visibly repeats after the config edit. Collapsing everything else around it.
elena: Kicking off a rerun on v1.2 now so the appendix compute numbers come from the same filtered set. Should finish while you regenerate tables.
elena: sorry, typo: I meant v1.3, not v1.2. The rerun is on v1.3.
```

> **>>> DECIDE AFTER THIS:** elena: sorry, typo: I meant v1.3, not v1.2. The rerun is on v1.3.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,140 items (changed Mon Oct 19; previously 1,200 items)
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)
- open item: Nadia to decide whether the 3-shot results go in the paper (check point: Tue Oct 20 paper sync)

---

## Row 4

**Today: Thu Oct 8** · #acct-northwind-eng

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Gabe to load-test Northwind's workload at their full rate limit (check point: Wed Oct 14)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Thu Oct 8 · #acct-northwind-eng ---
gabe: Streaming responses plus a "working on it" spinner fixes most of that. Separately, I'll load-test Northwind's workload at their full rate limit and have results by Wed Oct 14.
keiko: Streaming plus a spinner is an easy sell. Their ops lead said staff just want to know it's alive, not faster.
rachel: Yeah, a fixed interval with no jitter is exactly how those pile up. Could you put together a short backoff snippet I can send Keiko?
rachel: Good. I'll frame this in the renewal conversation as proactive tuning, not a capacity problem. Keeps the upsell door open.
keiko: Their ops lead also asked whether the assistant can flag when a form comes back with missing fields instead of silently moving on.
keiko: Gabe, can the assistant flag missing fields? If it misfires they'll want to debug, and logs will be available since Northwind is on standard 30-day retention. I'll tell their ops lead.
gabe: Sure, I'll write one up in Python with exponential backoff, full jitter, and a cap. Should honor the retry-after header too.
darnell: Their exec sponsor liked the intake demo last quarter. Once the tuning story is solid, that's a good thing to bring back up.
gabe: Also noticed their system prompt is huge and resent on every call. Trimming it or using prompt caching should cut latency on intake.
rachel: Perfect. Add a line or two on why jitter matters, so Keiko can frame it as a tip, not criticism.
keiko: Their ops lead hand-tuned that prompt for months, so she'll want reassurance that trimming won't change how the assistant behaves.
gabe: Fair. Caching keeps the prompt text identical, so behavior shouldn't shift. I can diff outputs on the de-identified forms before and after to show her.
gabe: Will do. I'll frame jitter as spreading retries out so clients don't all hit at once. Keiko can drop it in as a friendly tip.
rachel: Before/after diff on the forms would make a solid slide for the renewal deck. Customers like seeing proof, not promises.
rachel: Quick flag so nobody mixes them up: Northwind Logistics is a separate customer and renews Nov 15. Keep their numbers out of the Northwind Health deck.
```

> **>>> DECIDE AFTER THIS:** rachel: Quick flag so nobody mixes them up: Northwind Logistics is a separate customer and renews Nov 15. Keep their numbers out of the Northwind Health deck.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Gabe to load-test Northwind's workload at their full rate limit (check point: Wed Oct 14)

---

## Row 5

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

## Row 6

**Today: Mon Oct 5** · #harbor

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 5 · #harbor ---
elena: I'll grab it.
theo: Once the swap list is final I'll rerun the baselines and plot pass rate by repo size. Curious if multi-file tasks widen the gap between models.
yuki: Theo, if you plot by repo size, bucket by files touched too. Otherwise size and multi-file get tangled and the gap is hard to read.
theo: Good call, will do. I'll also split by language since the Python tasks tend to be the easiest, so that might be another confound.
marcus: Found a couple of multi-file candidates in a Rust build tool, bug spans the parser and the config loader. Checking the license now.
yuki: Rust is useful there too. If the models do much worse on those, I'd want to report language as its own breakdown in the paper.
theo: Rust tasks would be a good breakdown. Since the paper's due Oct 30, I'll plan to have the baseline reruns done a few days before so we have time to write up the language split.
marcus: Rust build tool license came back permissive, so those candidates are usable. The fix touches the parser and config loader together, and the tests are deterministic.
elena: Rust builds will be slow in the sandbox. I'll check the image has the toolchain cached so timeouts don't masquerade as model failures.
felix: I'll add a language field and a files-touched field to the task metadata, so Theo's breakdowns come straight from the release without a separate script.
yuki: Felix, can the language field hold more than one value? The Rust parser fix also touches TOML config, and I'd rather not force a single label.
felix: Yes, I'll make language a list instead of a single label. Then the Rust parser fix can carry both Rust and TOML, and Theo can group on either.
yuki: With language as a list, I'll report breakdowns by primary language only, so multi-label tasks don't get double counted in the paper tables.
theo: Primary-language only works for me. I'll flag in the table caption which tasks are multi-label so reviewers don't wonder why TOML never shows up.
elena: Fair warning, the eval jobs have more retries than I do at the gym. Rust timeouts are gonna be the worst offenders.
```

> **>>> DECIDE AFTER THIS:** elena: Fair warning, the eval jobs have more retries than I do at the gym. Rust timeouts are gonna be the worst offenders.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena

---

## Row 7

**Today: Tue Sep 8** · #launch

**Team facts as of now**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Tue Sep 8 · #launch ---
alex: meanwhile I'm sketching the pricing page. $15 per seat up top, with a small note under it about agent actions being metered 💸 will drop the mock here soon
frida: One design partner asked if they can mute the agent in a single channel without removing it. Worth a line in the FAQ?
frida: Separate from the FAQ: I'll send design partners the Slack-to-Ando migration guide by Fri Sep 11, so they have time to try it before launch 🙂
oli: Per-channel mute is doable on the runtime side, agent just stops listening there. I'll open a ticket for it.
alex: For per-channel mute, I'm thinking a small toggle in the channel header next to the agent avatar. Will sketch it with the member list 🔇
aj: Edge case on per-channel mute: should memory still keep what was said in a muted channel, or skip it entirely? Worth deciding before the FAQ line.
oli: Either works on the runtime side, memory ingestion would just check the mute flag. Product call though, Sara?
olavo: random but for launch day, how many pizzas do we order for 7 people? asking for a friend (the friend is me) 🍕😂
frida: Another design partner asked if the agent's replies trigger the same mobile notifications as human messages. Might need a FAQ line on that too 📱
oli: Agent replies go through the same push path as human messages today. A separate setting would be its own ticket, I can scope it.
olavo: For the launch post I'd love a screenshot of the agent jumping into a thread unprompted. Alex, could you mock one up? 📸
alex: Sure, I can mock the unprompted thread jump. Should the agent's message look different from a human reply, like a small badge, or keep it identical?
frida: My design partners liked having an "agent" label in the member list, so a small badge on messages might feel consistent 🙂
alex: Badge makes sense. I'll try a tiny "agent" tag next to the name, nothing loud, so long threads don't get noisy 🏷️
alex: Planning design freeze around the Sep 18 launch, so mocks for the pricing page, badge and thread-jump screenshot all land before then 🎨
```

> **>>> DECIDE AFTER THIS:** alex: Planning design freeze around the Sep 18 launch, so mocks for the pricing page, badge and thread-jump screenshot all land before then 🎨

**Team facts again**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

---

## Row 8

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

## Row 9

**Today: Wed Sep 30** · #infra

**Team facts as of now**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Wed Sep 30 · #infra ---
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
dmitri: Oct 5. That's the start date, so lock the table against it. I don't want it sliding because of the C uplinks.
```

> **>>> DECIDE AFTER THIS:** dmitri: Oct 5. That's the start date, so lock the table against it. I don't want it sliding because of the C uplinks.

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 10

**Today: Thu Oct 15** · #acct-northwind

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Thu Oct 15 · #acct-northwind ---
keiko: Perfect, thank you! One of their folks mentioned a dietary restriction, so I'll find out specifics and pass them along.
darnell: Frame multi-year as a partnership story in the QBR, not just a price lock. Their clinical teams are expanding use anyway.
darnell: Sounds good. Once you know the restriction, tell me and I'll check the kitchen can handle it before we book.
keiko: Correction: Amara left Northwind. Jon Reyes, the new CTO, owns the AI budget now.
rachel: Wow, okay. Keiko, how recent is this? Do we know if the new CTO is on board with the expansion plans?
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
```

> **>>> DECIDE AFTER THIS:** rachel: Timeline: we decide whether to offer Northwind a two-year term after the Fri Oct 16 finance review. Tomas, have both models ready for that so we're not scrambling.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

---

## Row 11

**Today: Tue Sep 8** · #launch

**Team facts as of now**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Tue Sep 8 · #launch ---
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
oli: Per-channel mute is doable on the runtime side, agent just stops listening there. I'll open a ticket for it.
alex: For per-channel mute, I'm thinking a small toggle in the channel header next to the agent avatar. Will sketch it with the member list 🔇
aj: Edge case on per-channel mute: should memory still keep what was said in a muted channel, or skip it entirely? Worth deciding before the FAQ line.
oli: Either works on the runtime side, memory ingestion would just check the mute flag. Product call though, Sara?
olavo: random but for launch day, how many pizzas do we order for 7 people? asking for a friend (the friend is me) 🍕😂
```

> **>>> DECIDE AFTER THIS:** olavo: random but for launch day, how many pizzas do we order for 7 people? asking for a friend (the friend is me) 🍕😂

**Team facts again**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

---

## Row 12

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

## Row 13

**Today: Mon Oct 19** · #acct-northwind

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Thu Oct 15 · #acct-northwind ---
keiko: Will do. I'll also ask whether he'd like clinical safety examples from other health systems, so the call isn't just us talking at him.
darnell: Good. Once Keiko hears back, I'll look for someone on our side with a clinical safety background to join that intro.
rachel: Sounds like a plan. Keiko, flag anything the platform lead says about the new CTO's priorities so we can adjust the QBR story.
--- Mon Oct 19 · #acct-northwind ---
tomas: Morning all. Friday's finance review is done and I've updated the order form draft with their comments. Redline v4 is in the deal folder. Rachel, can you confirm you've seen it before I send to Ines?
keiko: Heads up, Northwind's security lead asked me again for the sub-processor list. They want it for their internal review packet.
ines: Which one do they mean: the public sub-processor page, or the list referenced in the addendum? They're maintained separately.
keiko: Good question. I'll ask them which one. Their wording was "the full list for our vendor packet," so I'm guessing the addendum one.
rachel: Yes, seen v4 and it looks fine to me. Tomas, go ahead and send to Ines. Let's keep redlines moving.
gabe: Their security lead also pinged me about how we handle burst traffic during their clinic morning rush. Happy to join a call if that helps the packet.
keiko: Their ops team mentioned the morning rush is when the clinics all check patients in at once, so that's what worries them.
gabe: Helpful context. Is the check-in surge a sharp spike when doors open, or more of a ramp? Changes how I'd explain our burst handling.
keiko: From what ops described, it's a sharp spike right when doors open. I'll ask if they have a rough traffic graph from last quarter.
gabe: A sharp spike like that is the case I'd want to walk them through. A graph would help me show how it looks on our side.
rachel: Good. If the graph shows the spike clearly, let's fold it into the security packet so they stop asking in pieces.
gabe: Quick one so I can plan the burst call: what's the date Northwind needs to sign by for the renewal?
```

> **>>> DECIDE AFTER THIS:** gabe: Quick one so I can plan the burst call: what's the date Northwind needs to sign by for the renewal?

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

---

## Row 14

**Today: Fri Oct 9** · #infra

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
--- Fri Oct 9 · #infra ---
lucia: Leaf 14 maps to a contiguous block of kestrel ranks in one rack. No NCCL timeouts on them so far. List is in the doc.
wen: Single rack block is easy to drain if it comes to that. Checking which spares sit off leaf 14 so we're not swapping onto the same uplink.
kofi: My bad, it lives in the ckpt-writer thread, not the doc. It touches the save interval and the async flush path. Pasting it here.
hana: Thanks. Once it's pasted I'll check whether the async flush overlaps with the step-time stalls I'm alerting on, otherwise the drill will look noisy.
kofi: Pasted in the ckpt-writer thread. Save interval is tighter, and the flush now runs off the training thread, so the step shouldn't block on storage writes.
lucia: If we want the leaf 14 uplink reseated before the run starts Oct 5, I need a drain window. Symbol errors still creeping.
lucia: *sorry, typo. The run starts Oct 12, not Oct 5. Still need the drain window for the leaf 14 reseat before then.
wen: I'll ask them to bring spare optics and a fiber scope for those leaf ports. Also need hall badge access sorted for their people.
wen: Spares off leaf 14 exist, but they're in the pool I'd rather not drain. Can the reseat wait for a natural gap in the drill?
dmitri: I'll have Lucia export the flap logs with a leaf port map so they can match optics to the worst offenders. Badge request needs legal names for the hall desk.
kofi: A gap in the drill works for the reseat. Restore path reads shards from storage anyway, so that's a natural idle window on those ranks.
wen: I'll get legal names from their account rep and file the badge request. Also asking whether their techs need a hall escort.
hana: Then I'll mute the step-time stall alert on the leaf 14 ranks during restore, so the reseat doesn't page anyone.
mateo: Restore reads will hit the new storage tier hard on those shards. Should be fine, but I'll watch read latency during the drill.
mateo: I sized the storage write budget around a checkpoint every 500 steps, so the new tier should absorb the async flushes with headroom. Restore reads are the bigger unknown.
```

> **>>> DECIDE AFTER THIS:** mateo: I sized the storage write budget around a checkpoint every 500 steps, so the new tier should absorb the async flushes with headroom. Restore reads are the bigger unknown.

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps (changed Fri Oct 9; previously every 500 steps)
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

---

## Row 15

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
felix: My release jobs are queued behind the eval batch. Who actually owns the compute reservation for the eval runs? Want to know who to ping if they stall.
yuki: Also noticed the pass@1 plot in the draft has a y-axis that makes the gap between models look bigger than it is. Worth rescaling.
theo: Rescaling the plot is easy, I'll regenerate it with a zero-based axis and add error bars so the gap reads honestly.
marcus: I'll say explicitly the overlap check is n-gram matching on function bodies, so paraphrased solutions could slip through. Better than reviewers inferring it.
theo: Sorry, behind on that. Highlighting the stale baseline rows in yellow in the shared sheet now so nobody quotes them.
yuki: Caption should also say what the error bars are, bootstrap over tasks or across seeds. Otherwise reviewers will guess.
elena: That's me, Felix. If your release jobs sit behind the eval batch, ping me directly and I'll look at the queue.
felix: Thanks Elena, will do. Also, the package notes should mention the contamination filtering so they line up with Marcus's writeup wording.
marcus: Agreed, Felix. I'll align the filtering wording with the package notes. The checklist I'm working from lists the release gate as 65% pass@1, so let's quote it that way in both places.
theo: Error bars will be bootstrap over tasks. We only ran a few seeds per model, so seed variance would be too noisy to show.
yuki: Related caption point: a few runs hit sandbox timeouts mid-task. We should say whether those count as failures or get excluded.
elena: Some of those timeouts were on the slower nodes, so they may be infra rather than the model. I can pull the logs and tag which.
yuki: Yes please, Elena. If they're infra, I'd lean toward reporting those separately instead of counting them as model failures. Footnote it in the caption.
theo: Once Elena's tags are in, I'll add an infra-timeout column to the results table so it's separate from the failure counts.
theo: Random what-if, with the table and plot rework piling up: should we skip the workshop and aim for the main conference instead? More time to do the results properly.
```

> **>>> DECIDE AFTER THIS:** theo: Random what-if, with the table and plot rework piling up: should we skip the workshop and aim for the main conference instead? More time to do the results properly.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,140 items (changed Mon Oct 19; previously 1,200 items)
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 16

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

## Row 17

**Today: Mon Oct 12** · #harbor

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 5 · #harbor ---
marcus: I'll also check whether the Rust build tool's test suite pulls anything from the network. If it does, the sandbox will fail those no matter what the model writes.
yuki: If it does pull from the network, vendoring the dependencies into the image would fix that. Otherwise we'd have to drop those tasks and look for others.
elena: Vendoring works for me. I can bake the crates into the sandbox image so builds run offline. Marcus, send me the lockfile once you pick the tasks.
marcus: Will do. Checking now whether the lockfile is pinned for that Rust tool. If it isn't, I'll resolve versions first so the crates don't drift.
yuki: If the lockfile isn't pinned, note which crate versions you resolve to. I'd like the paper's appendix to list the toolchain so the Rust tasks are reproducible.
marcus: Lockfile's checked in but a couple of entries use loose version ranges. I'll resolve them and write down what each crate lands on.
elena: Once the crates are resolved I'll bake them into a test image and do a dry run on the Rust tasks, just to see where the slow ones land.
yuki: When you do the dry run, log per-task wall time too. I'd like to see whether the slow Rust tasks cluster on the multi-file ones.
theo: Per-task wall time would also help the baseline table. I can add a column for median runtime per language if the logs have it.
felix: Per-task wall time is already in the harness logs, I'll make sure it gets exported with the results so Theo's runtime column doesn't need scraping.
marcus: Two of the Rust candidates look like they share a fixture directory, so I'll check they don't leak each other's expected outputs before they go in.
yuki: If they do share a fixture directory, I'd rather split it per task than drop either one. Cleaner isolation and we keep the multi-file case.
marcus: Splitting per task works. I'll copy the shared fixtures into each task's own directory and diff the expected outputs afterward to confirm nothing carried over.
theo: Once the split fixtures are in, I'll rerun the baseline on those Rust tasks so we can see if isolation shifts any scores.
--- Mon Oct 12 · #harbor ---
nadia: Morning all. Marcus's check on Friday confirmed the contamination, so harbor needs a new version and we have to rerun the baselines. Let's sort out who does what today.
```

> **>>> DECIDE AFTER THIS:** nadia: Morning all. Marcus's check on Friday confirmed the contamination, so harbor needs a new version and we have to rerun the baselines. Let's sort out who does what today.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items

---

## Row 18

**Today: Mon Oct 12** · #harbor

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 12 · #harbor ---
elena: Good call on disk. I'll check free space on the shared volume and point the big logs at scratch before queueing anything.
marcus: Fuzzy match on the fork dumps is running. A few gist hits look like reformatted copies, so whitespace and renamed variables won't fool it.
theo: Ok, committing: I'll rerun all baselines on harbor v1.3 and have them done by Fri Oct 16. Rescoring the unpatched tasks from saved traces, fresh runs only for the patched ones.
marcus: Also noticing some flagged tasks share a helper file across repos, so dropping one may orphan others. I'll list those dependencies for Felix.
felix: Helpful, Marcus. Send the helper-file dependencies as a list per task and I'll check which ones break when I cut the manifest.
yuki: Once Marcus's helper-file list is in, I'd like to check whether any orphaned tasks lose their only test fixture. Those would need a re-spec, not just removal.
marcus: Yuki, good point. I'll tag any task whose only fixture lives in a shared helper, so you can see which ones need a re-spec before Felix cuts.
nadia: Results table caption reads "harbor v1.2, pass@1 across all scaffolds". Theo, just drop the rerun numbers into that table when they're done, so the wording doesn't change.
elena: Disk check done: shared volume has room, but I'm still routing the refactor scaffold logs to scratch just in case.
yuki: Once the patched tasks finish, I want a plot of pass rate split by patched versus untouched tasks. If the gap is big, that's a finding.
marcus: For the paper, we should describe the near-duplicate similarity cutoff in the contamination section. Reviewers will ask how we picked it.
yuki: Agreed. A histogram of similarity scores would help, if there's a visible gap between reformatted copies and legit lookalikes, the cutoff justifies itself.
theo: Rescored runs on the untouched tasks look nearly identical so far. Curious if the patched ones drop more on the refactor scaffolds.
theo: Quick one, who actually holds the compute reservation for the fresh runs? Want to make sure the refactor jobs land on it.
elena: That's me, I hold the reservation. Refactor jobs are already at the front of the queue, so they'll land on it.
```

> **>>> DECIDE AFTER THIS:** elena: That's me, I hold the reservation. Refactor jobs are already at the front of the queue, so they'll land on it.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 19

**Today: Mon Oct 5** · #kestrel-run

**Team facts as of now**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

**Recent messages** (oldest first; the last one is the decision message)

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

> **>>> DECIDE AFTER THIS:** kofi: With start now Oct 12, I'll move the restart drill to the week before, so the resharding restore test on the new vocab layout runs on the upgraded fabric.

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 20

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
```

> **>>> DECIDE AFTER THIS:** frida: Thanks Oli. Separate thing: I told the agency heads-up that after launch it's agent actions metered, so their invoice will vary month to month. They were fine with it, just wanted finance to know.

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

## Row 21

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

## Row 22

**Today: Mon Oct 12** · #harbor

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 5 · #harbor ---
felix: Per-task wall time is already in the harness logs, I'll make sure it gets exported with the results so Theo's runtime column doesn't need scraping.
marcus: Two of the Rust candidates look like they share a fixture directory, so I'll check they don't leak each other's expected outputs before they go in.
yuki: If they do share a fixture directory, I'd rather split it per task than drop either one. Cleaner isolation and we keep the multi-file case.
marcus: Splitting per task works. I'll copy the shared fixtures into each task's own directory and diff the expected outputs afterward to confirm nothing carried over.
theo: Once the split fixtures are in, I'll rerun the baseline on those Rust tasks so we can see if isolation shifts any scores.
--- Mon Oct 12 · #harbor ---
nadia: Morning all. Marcus's check on Friday confirmed the contamination, so harbor needs a new version and we have to rerun the baselines. Let's sort out who does what today.
marcus: I can share the list of flagged tasks now. Most overlap traces back to a couple of popular GitHub repos that leaked into the public mirrors.
felix: Thanks Marcus. Once I have the flagged list I can cut the affected tasks from the manifest and rebuild the release candidate. Are the mirrors the only source, or do the repos show up elsewhere too?
marcus: Not only mirrors. Some of the same repos also show up as forks and in a few public gist dumps, so I'm checking those too.
yuki: If forks and gists are in play, we should check whether near-duplicate solutions count too, not just exact repo matches. Otherwise partial leakage slips through.
felix: Going with what I proposed last Wednesday (Oct 7) for the new harbor release. Starting on it now, will rebuild the candidate as soon as Marcus's flagged list lands.
theo: Do I rerun every baseline from scratch, or just rescore the surviving tasks from the saved traces? Rescoring would be way faster for the slow scaffolds.
yuki: Rescoring is fine for tasks whose test harness didn't change. Any task we patch to drop near-duplicate overlap needs a fresh run, though.
marcus: Near-duplicate check is doable. I'll run fuzzy matching on the solution diffs against the fork and gist dumps, then flag anything above a similarity cutoff.
yuki: Updating the eval config now to point at v1.3. Patched tasks get fresh runs, the rest can reuse saved traces. I'll flag which is which in the config.
```

> **>>> DECIDE AFTER THIS:** yuki: Updating the eval config now to point at v1.3. Patched tasks get fresh runs, the rest can reuse saved traces. I'll flag which is which in the config.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items

---

## Row 23

**Today: Mon Sep 28** · #kestrel-run

**Team facts as of now**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Sep 28 · #kestrel-run ---
kofi: If the flapping racks get drained, I need to know before I size checkpoint shards. Fewer nodes changes the per-rank write pattern to storage.
mateo: Data side is looking fine so far. Tokenized shards are landing on the new filesystem, just waiting on the last dedup pass to finish.
hana: Whichever variant wins, I want straggler detection on from step zero. Flapping links would show up as a few slow ranks dragging MFU down.
hana: Stability rule for the run: roll back if loss rises more than 15%. I'll wire that into the monitor alongside the straggler alerts.
kofi: Also want async checkpoint staging on local NVMe before flush, otherwise a slow writer rank will stall the whole step. Testing that on the new filesystem.
hana: Also, that's measured over a 200-step window, not single-step spikes, so one noisy batch won't trip it.
lucia: Serials back: both flapping uplinks have transceivers from the same vendor lot. Swapped one, soak is running now, watching CRC counters on that port.
wen: If the swapped port stays clean, I'd want the other flapping uplink swapped too before I count those racks as healthy in the second variant.
mateo: Sized the data loader for 2,560 nodes. Filesystem read throughput has headroom, and prefetch workers per node should keep the GPUs fed. Dedup finishing is the only gate on my side.
kofi: NVMe staging test looks good so far: flush overlaps the next forward pass, no stalls on the slow writer. Restore path from the new filesystem still untested.
lucia: CRC counters on the swapped port are flat so far. Other flapping uplink still on the old optic, I'll swap it next and rerun the soak.
dmitri: Mateo, your loader sizing doesn't match the allocation Wen confirmed. Redo it against the confirmed number.
mateo: Fair, my bad. Redoing the loader sizing against Wen's number. Prefetch worker count per node will probably shift too, rechecking read throughput after.
kofi: Restore path is my next test. Will kill a rank mid-flush and confirm we resume cleanly from the staged NVMe copy.
mateo: Once dedup lands, I'll finish moving the tokenized datasets to the new storage tier by Fri Oct 2. That leaves a few days of buffer before the start.
```

> **>>> DECIDE AFTER THIS:** mateo: Once dedup lands, I'll finish moving the tokenized datasets to the new storage tier by Fri Oct 2. That leaves a few days of buffer before the start.

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps

---

## Row 24

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

## Row 25

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
elena: That's me, Felix. If your release jobs sit behind the eval batch, ping me directly and I'll look at the queue.
felix: Thanks Elena, will do. Also, the package notes should mention the contamination filtering so they line up with Marcus's writeup wording.
marcus: Agreed, Felix. I'll align the filtering wording with the package notes. The checklist I'm working from lists the release gate as 65% pass@1, so let's quote it that way in both places.
theo: Error bars will be bootstrap over tasks. We only ran a few seeds per model, so seed variance would be too noisy to show.
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
```

> **>>> DECIDE AFTER THIS:** marcus: Heads up, I'm not doing great this week, so I might be slow to reply. Ping me directly if something is blocking on the contamination writeup.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,140 items (changed Mon Oct 19; previously 1,200 items)
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 26

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

## Row 27

**Today: Mon Oct 5** · #kestrel-run

**Team facts as of now**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

**Recent messages** (oldest first; the last one is the decision message)

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

> **>>> DECIDE AFTER THIS:** dmitri: We'll decide between tokenizer v3 and v4 for kestrel at the Thu Oct 8 run sync. Mateo, have the shard diff ready by then. Kofi, get the TP padding answer to the group before.

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 28

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

## Row 31

**Today: Thu Oct 15** · #acct-northwind

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Thu Oct 15 · #acct-northwind ---
darnell: Fine either way. If the back room is taken, I know a second place with a quiet corner. Less private but good food.
rachel: I'd lean toward building both, since the model is cheap. Just keep the multi-year one internal until we know where the new exec lands.
rachel: Timeline: we decide whether to offer Northwind a two-year term after the Fri Oct 16 finance review. Tomas, have both models ready for that so we're not scrambling.
keiko: Either works for me. The quiet corner might actually feel more relaxed for them. I'll pass both options along once I hear back on the dietary thing.
tomas: Understood. I'll build both models so they're ready for the review, with the volume-band language Ines asked for in each order form draft.
ines: Worth checking whether the new exec's arrival reopens any security or compliance review on their side. That could shift how they read the contract terms.
gabe: Good call, Ines. Their security team did a pretty thorough architecture review last time, so I'd expect questions on data flow again.
darnell: I'll send the QBR deck to Amara Okafor once the term section is locked. Better she sees it from me than cold.
keiko: Their procurement lead also wants a usage breakdown by clinical department in the QBR. Gabe, can we pull that from the dashboards?
gabe: Dashboards split usage by project and API key, not department. If their clinical teams use separate keys, I can map it. Otherwise we'd need to check how they tag requests.
darnell: Sounds good. Whichever we land on, I'll hold off confirming until we hear on the dietary side.
keiko: I'll ask their platform lead whether the clinical teams run separate keys or share one. Will report back once I hear.
rachel: Darnell, the deck plan was for the previous sponsor. Who should receive it now, given we haven't met the new owner?
darnell: Fair point, that note was stale. I'll hold off on sending anything until we figure out an intro to the new owner.
keiko: Just thinking out loud: what if we went back to 18% to close faster? Not a proposal, only wondering if it'd help with a new CTO.
```

> **>>> DECIDE AFTER THIS:** keiko: Just thinking out loud: what if we went back to 18% to close faster? Not a proposal, only wondering if it'd help with a new CTO.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

---

## Row 32

**Today: Mon Oct 19** · #acct-northwind

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

**Recent messages** (oldest first; the last one is the decision message)

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

> **>>> DECIDE AFTER THIS:** gabe: Quick one before we wrap: who's the exec contact at Northwind now? I want to cc them on the renewal thread when I send the one-pager.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

---
