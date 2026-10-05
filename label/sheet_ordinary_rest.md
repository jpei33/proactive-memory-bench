# Labeling sheet: ordinary_rest (171 rows, LLM-labeled)

For each row, decide what an AI teammate with perfect memory should do right after the marked **decision message**: IGNORE, TRACK or INTERVENE, plus severity 1-3 (TRACK is always 1). Follow rubric.md (read it first). Notes are optional: for INTERVENE say which fact you act on, for TRACK what to check and by when, and flag anything you were unsure about.

Suggested order for each row:
1. Read the decision message. Note any date, number, name, owner, ticket, price or promise in it.
2. Look each one up in the team facts (shown again below the messages). Different from the current value = contradiction; matches a "previously" value = stale; asks about something already in the facts = repeat question.
3. Compare open items' check points with Today.
4. Scan the recent messages: already corrected or answered? self-correction? proposal? addressed to a specific person? personal? -> IGNORE (tie-breaks 1-3, 11, 12).
5. Nothing triggered -> IGNORE, unless the message opens a new commitment with an owner and a check point -> TRACK.

## Row 1

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
--- Mon Oct 12 · #harbor ---
yuki: Yes, resample over tasks. Seeds within a task are correlated, so seed-level resampling would understate the spread. Task-level bootstrap, then average seeds inside each draw.
theo: Got it, task-level bootstrap. I'll add the interval bands to the patched-versus-untouched plot per scaffold and flag the refactor one if it looks wide.
marcus: Tutorial-repo commit dates are mostly earlier than the task repos, so I'll describe those fixtures in their own paragraph with the overlay.
--- Wed Oct 21 · #harbor ---
nadia: Two days out. Can everyone post what's still open on your side in here? I'll sort the final list from that.
elena: Cluster queue looks fine on my side. Only thing open is making sure the last batch of eval jobs doesn't get preempted overnight.
theo: Mine's the results table. Two of the baseline rows still have old numbers in them, so I need to refresh those before anyone quotes the table.
yuki: Open on my side: the pass criteria paragraph in the methods section still reads ambiguously. Want to tighten the wording before anyone cites it.
marcus: Mine's the contamination writeup. Need to reword how we describe the overlap check so reviewers don't read it as stronger than it is.
felix: Mine's the release checklist. Changelog is drafted but I still need to go through the tagging steps and double-check the package notes match the paper.
nadia: Thanks all. Theo, can you flag which two baseline rows are stale so Yuki and Marcus know what not to quote yet?
felix: My release jobs are queued behind the eval batch. Who actually owns the compute reservation for the eval runs? Want to know who to ping if they stall.
yuki: Also noticed the pass@1 plot in the draft has a y-axis that makes the gap between models look bigger than it is. Worth rescaling.
theo: Rescaling the plot is easy, I'll regenerate it with a zero-based axis and add error bars so the gap reads honestly.
marcus: I'll say explicitly the overlap check is n-gram matching on function bodies, so paraphrased solutions could slip through. Better than reviewers inferring it.
theo: Sorry, behind on that. Highlighting the stale baseline rows in yellow in the shared sheet now so nobody quotes them.
```

> **>>> DECIDE AFTER THIS:** theo: Sorry, behind on that. Highlighting the stale baseline rows in yellow in the shared sheet now so nobody quotes them.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,140 items (changed Mon Oct 19; previously 1,200 items)
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 2

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
--- Mon Oct 12 · #kestrel-run ---
kofi: Checkpoint writer is up on my side. I'll watch async flush times on the first saves, since stalls there tend to show up as stragglers.
hana: Loss and grad-norm dashboards are live. I'm also tracking per-rank step time so a slow rank shows up before MFU dips.
mateo: Dataloader workers are warm and prefetch queues look full. Should be smooth on the first few batches, no stalls expected from the data side.
dmitri: Good. Kicking off now. Shout the second you see a rank lagging, don't wait for it to show up in MFU.
hana: First steps are in. Per-rank step time looks tight so far, no rank trailing the pack. Still early though.
wen: Heads up, separate from kestrel: the kestrel-mini ablation run starts Oct 14. Different run, I'll keep its nodes carved out so it doesn't touch this allocation.
kofi: First async flush is kicking off now. Writer queue depth looks normal, nothing backing up behind the flush yet.
lucia: Seeing a brief NCCL all-reduce latency bump on one leaf switch during the flush. Still within normal spread, keeping an eye on it.
kofi: Flush finished clean on my side. Lucia, does that latency bump line up with the writer burst hitting the fabric, or is it unrelated?
lucia: Likely correlated. The bump landed on the leaf where the writer nodes uplink. Pulling port counters to see if it was incast on that leaf.
kofi: If it's incast on that leaf, I can stagger the writer nodes' flush start so they don't all burst at once. Want to see the counters first.
lucia: Port counters show egress buffer spikes on the writer uplinks right at flush start. Looks like incast. Staggering would probably flatten it.
kofi: Okay, I'll add a per-node jitter on the flush start so the writers spread out. Hana, watch step time on the next save for any residual dip.
mateo: Unrelated to the flush, but I'm seeing IB link flaps on a couple of the dataloader nodes in my logs. Who's on call for fabric incidents today?
hana: Will do, Kofi. I've tagged the first flush window in the step-time panel so I can diff it against the next save once jitter's in.
```

> **>>> DECIDE AFTER THIS:** hana: Will do, Kofi. I've tagged the first flush window in the step-time panel so I can diff it against the next save once jitter's in.

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps (changed Fri Oct 9; previously every 500 steps)
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

---

## Row 3

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
yuki: Updating the eval config now to point at v1.3. Patched tasks get fresh runs, the rest can reuse saved traces. I'll flag which is which in the config.
elena: For the fresh runs, which scaffolds are slowest? I'd like to queue those first so they don't get stuck behind the quick ones.
theo: The multi-file refactor scaffolds are slowest by far, especially the one with the long tool-use loops. Those should go first in the queue.
elena: Got it, I'll put the refactor ones at the front. The long tool-use loops tend to hit timeouts, so I'll bump the per-run limit for those.
theo: Heads up, the long tool-use scaffold also eats a lot of tokens per run, so the logs get huge. Might want to check disk before queueing.
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
```

> **>>> DECIDE AFTER THIS:** yuki: Once the patched tasks finish, I want a plot of pass rate split by patched versus untouched tasks. If the gap is big, that's a finding.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

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

**Recent messages** (oldest first; the last one is the decision message)

```
--- Thu Oct 8 · #acct-northwind-eng ---
gabe: Pulled Northwind's usage logs from the last few weeks. Traffic is spiky around their morning clinic intake, lots of 429s in that window.
keiko: That tracks with what their ops lead told me on the call. Intake staff complained the assistant stalls right when the clinics open.
gabe: Looks like they fire a burst of parallel requests at open with no backoff. Retries just pile on and make the 429s worse.
keiko: Quick check before I reply to their ops lead: is Northwind's rate limit 40M tokens per minute? React 👍 if so.
gabe: Did you see the postmortem another enterprise customer posted? Their retry storm took down their own gateway for hours.
(gabe reacted 👍 to keiko's message)
keiko: Thanks. So it's burst shape, not capacity. Gabe, can you share a backoff-with-jitter example I can send their ops lead?
gabe: Yep, I'll pull a Python snippet with exponential backoff and full jitter. Also worth suggesting they stagger the opening burst with a small queue.
keiko: Their ops lead also asked if the intake assistant can use a lighter model for the simple form-filling steps. Worth a look?
gabe: Yes, likely. Form-filling is mostly structured extraction, so a smaller model should handle it. I'd want to test accuracy on their real intake forms first.
ines: Since they're sending patient intake data through this, flagging the retention side: zero data retention is approved for Northwind. Worth keeping that in mind when we test on their real forms.
rachel: Yes, saw it. Ouch. Makes me wonder if Northwind's team has backoff with jitter on their side. Worth a quick check with them?
gabe: Good point. I'll ask their ops lead for de-identified sample forms so we can compare the smaller model without touching real patient records.
```

> **>>> DECIDE AFTER THIS:** gabe: Good point. I'll ask their ops lead for de-identified sample forms so we can compare the smaller model without touching real patient records.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

---

## Row 5

**Today: Thu Sep 10** · #eng

**Team facts as of now**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Thu Sep 10 · #eng ---
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
alex: Okay so for the single-agent demo workspace, should I mock up the onboarding screens with just one agent in the sidebar? Easier to screenshot.
```

> **>>> DECIDE AFTER THIS:** alex: Okay so for the single-agent demo workspace, should I mock up the onboarding screens with just one agent in the sidebar? Easier to screenshot.

**Team facts again**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

---

## Row 6

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
marcus: Histogram's rough but promising: reformatted gist copies bunch up at the top, and generic argparse-style boilerplate lookalikes sit well below with a clear dip between.
yuki: That dip is exactly what we want. Can you overlay the borderline cases on the histogram? I'd like to see where the ambiguous ones fall.
marcus: Sure, I'll mark the borderline ones in a different color. A few are fixtures copied from a popular tutorial repo, so they might land near the dip.
yuki: Tutorial-repo fixtures are a good edge case. If they sit near the dip, I'd say describe them separately in the paper rather than force them into either bucket.
```

> **>>> DECIDE AFTER THIS:** yuki: Tutorial-repo fixtures are a good edge case. If they sit near the dip, I'd say describe them separately in the paper rather than force them into either bucket.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 7

**Today: Thu Sep 10** · #eng

**Team facts as of now**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Thu Sep 10 · #eng ---
alex: Slightly random, but does the agent typing indicator also fire for the double replies? Would be good to know for the onboarding demo.
oli: Alex: yes, typing indicator fires per agent, so you'd see two bubbles for a double reply. Not great for a demo, I'd avoid that scenario.
alex: Haha perfect. Should I mock up the snack thread in the sandbox so the agent's reply looks natural on screen? I can draft it.
olavo: For the launch post, can I show agents joining a thread on their own? Want a clean gif, no double bubbles obviously 😅
oli: Olavo: thread-join gif is fine as long as only one agent is in the channel. Use a single-agent demo workspace.
frida: Yes please! Draft it and I'll run it past a couple of partners to see if the snack banter feels real 😊
alex: Okay so for the single-agent demo workspace, should I mock up the onboarding screens with just one agent in the sidebar? Easier to screenshot.
olavo: Yes please Alex, one agent in the sidebar works for me too. I'll grab screenshots from it for the press kit as well.
aj: Oli, pulled up the sim harness. It fakes channel traffic fine, but I'll need to tweak it so agents hit shared memory entries, not just channels.
oli: Makes sense. Have them hit a small set of hot entries plus a wide spread, so we see both contention and the normal case.
frida: Heard back from the partner: their agents mostly hit the same couple of standup channels during the rush. Sounds like hot entries to me.
aj: That fits the hot-entry case then. I'll weight the sim toward a few shared entries and log p95 read latency per run.
alex: Different thing, for the onboarding copy: if someone @-mentions an agent inside a DM, can that agent read the DM? Or is it blocked unless the agent is a member of it?
oli: aj, log write latency too, not just reads. Standup rush probably has agents saving summaries to memory at the same moment.
aj: Will do, write latency goes in the same log. I'll also tag each run with how many agents were active.
```

> **>>> DECIDE AFTER THIS:** aj: Will do, write latency goes in the same log. I'll also tag each run with how many agents were active.

**Team facts again**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

---

## Row 8

**Today: Thu Oct 8** · #acct-northwind-eng

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Thu Oct 8 · #acct-northwind-eng ---
gabe: Pulled Northwind's usage logs from the last few weeks. Traffic is spiky around their morning clinic intake, lots of 429s in that window.
keiko: That tracks with what their ops lead told me on the call. Intake staff complained the assistant stalls right when the clinics open.
```

> **>>> DECIDE AFTER THIS:** keiko: That tracks with what their ops lead told me on the call. Intake staff complained the assistant stalls right when the clinics open.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

---

## Row 9

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
marcus: Yuki, good point. I'll tag any task whose only fixture lives in a shared helper, so you can see which ones need a re-spec before Felix cuts.
nadia: Results table caption reads "harbor v1.2, pass@1 across all scaffolds". Theo, just drop the rerun numbers into that table when they're done, so the wording doesn't change.
elena: Disk check done: shared volume has room, but I'm still routing the refactor scaffold logs to scratch just in case.
yuki: Once the patched tasks finish, I want a plot of pass rate split by patched versus untouched tasks. If the gap is big, that's a finding.
marcus: For the paper, we should describe the near-duplicate similarity cutoff in the contamination section. Reviewers will ask how we picked it.
yuki: Agreed. A histogram of similarity scores would help, if there's a visible gap between reformatted copies and legit lookalikes, the cutoff justifies itself.
theo: Rescored runs on the untouched tasks look nearly identical so far. Curious if the patched ones drop more on the refactor scaffolds.
theo: Quick one, who actually holds the compute reservation for the fresh runs? Want to make sure the refactor jobs land on it.
elena: That's me, I hold the reservation. Refactor jobs are already at the front of the queue, so they'll land on it.
marcus: Histogram's rough but promising: reformatted gist copies bunch up at the top, and generic argparse-style boilerplate lookalikes sit well below with a clear dip between.
yuki: That dip is exactly what we want. Can you overlay the borderline cases on the histogram? I'd like to see where the ambiguous ones fall.
marcus: Sure, I'll mark the borderline ones in a different color. A few are fixtures copied from a popular tutorial repo, so they might land near the dip.
yuki: Tutorial-repo fixtures are a good edge case. If they sit near the dip, I'd say describe them separately in the paper rather than force them into either bucket.
marcus: I'll check commit dates on those tutorial fixtures. If the tutorial repo predates the task repos, that changes how we frame them.
nadia: For the contamination section, let's say "near-duplicate" and keep the tone factual. No "leaked" or "cheated" wording, since reviewers will read that as an accusation.
```

> **>>> DECIDE AFTER THIS:** nadia: For the contamination section, let's say "near-duplicate" and keep the tone factual. No "leaked" or "cheated" wording, since reviewers will read that as an accusation.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 10

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
rachel: Darnell, the deck plan was for the previous sponsor. Who should receive it now, given we haven't met the new owner?
darnell: Fair point, that note was stale. I'll hold off on sending anything until we figure out an intro to the new owner.
keiko: Just thinking out loud: what if we went back to 18% to close faster? Not a proposal, only wondering if it'd help with a new CTO.
tomas: I'd keep the current plan, Keiko. Going back on the discount now would hurt our position, and we don't yet know what the new CTO wants. Let's learn his priorities first.
gabe: Agree with holding the line. If it helps, I can offer their platform lead a quick architecture walkthrough for the new CTO. Technical intros land easier than sales ones.
keiko: Walkthrough would help. Their platform lead mentioned the new CTO is big on clinical safety, so I'd frame it around that.
keiko: Perfect. I'll nudge their admin again tomorrow morning so we're not waiting on her too long.
ines: If he's focused on clinical safety, expect him to ask about logging and how model outputs get reviewed. I'd want our answers consistent across the deck and contract.
gabe: I can pull together a one-pager on how we handle output logging and what controls their team can set. Keeps the answers consistent with the deck.
rachel: Good. Keiko, when you talk to their platform lead, ask if the new CTO would take a short intro call before the QBR.
keiko: Will do. I'll also ask whether he'd like clinical safety examples from other health systems, so the call isn't just us talking at him.
darnell: Good. Once Keiko hears back, I'll look for someone on our side with a clinical safety background to join that intro.
rachel: Sounds like a plan. Keiko, flag anything the platform lead says about the new CTO's priorities so we can adjust the QBR story.
--- Mon Oct 19 · #acct-northwind ---
tomas: Morning all. Friday's finance review is done and I've updated the order form draft with their comments. Redline v4 is in the deal folder. Rachel, can you confirm you've seen it before I send to Ines?
keiko: Heads up, Northwind's security lead asked me again for the sub-processor list. They want it for their internal review packet.
```

> **>>> DECIDE AFTER THIS:** keiko: Heads up, Northwind's security lead asked me again for the sub-processor list. They want it for their internal review packet.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

---

## Row 11

**Today: Tue Oct 6** · #acct-northwind

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30

**Recent messages** (oldest first; the last one is the decision message)

```
--- Tue Oct 6 · #acct-northwind ---
rachel: Kicking off the Northwind renewal thread. Want one place for timeline, pricing, sponsor, and paperwork. Keiko, any early signals from their side?
keiko: Yes, a couple. Their clinical informatics lead mentioned on our last call that usage has grown a lot since the pilot teams went live. Sounds happy overall.
gabe: Good sign. Growth like that usually means we should check their rate limit headroom before we talk renewal. Want me to pull usage trends?
rachel: Yes please, Gabe. Timeline note for everyone: the Northwind renewal signature deadline is Oct 30. Working back from that for pricing, legal review, and sponsor sign-off.
gabe: On it. I'll also check whether any of their pilot teams are bursting at peak hours, since that's usually where throttling shows up first.
tomas: Once Gabe's usage numbers are in, I'll draft the pricing options for the order form. Rachel, any sense of how aggressive they'll be on discount?
```

> **>>> DECIDE AFTER THIS:** tomas: Once Gabe's usage numbers are in, I'll draft the pricing options for the order form. Rachel, any sense of how aggressive they'll be on discount?

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30

---

## Row 12

**Today: Tue Oct 6** · #acct-northwind

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Tue Oct 6 · #acct-northwind ---
rachel: Found the old redline folder. Their legal team marked up the data sections heavily, so I'll tag the clauses they fought hardest on.
ines: Thanks, Rachel. Once tagged, I'll compare their old language against our current standard terms and see where we can realistically give ground.
gabe: Peak-hour breakdown is coming together. Two of the pilot teams look like the main bursters, so I'll flag those for Tomas separately.
keiko: Heads up, their informatics lead said the pilot clinicians love the summarization features. Could be a good angle for the expansion conversation.
rachel: Good angle. Keiko, can you get a customer quote on the summarization wins in their own words? Would help anchor the expansion pitch.
keiko: On it. One of the pilot nurse managers gave a great line on the summarization wins last week, so I'll ask if we can use it.
gabe: Fair warning, the QBR deck is already at like 40 slides. Pretty sure the nurse manager's quote is getting its own slide at this point.
rachel: Gabe, cut it to a handful of slides. Execs skim. Keep the nurse manager quote and the usage trend, drop the rest to appendix.
gabe: Will do. I'll keep the usage trend to one clean chart and move the per-team breakdown to the appendix.
tomas: Once Gabe's peak-hour view is in, I'll model a couple of pricing scenarios. Keiko, any sense yet whether they're comparing us against another vendor?
keiko: Not sure yet. Their informatics lead mentioned procurement asked about other vendors' demos, but nothing concrete. I'll try to learn more on the next call.
darnell: If another vendor is in the mix, I'd like to know before I reach out. Keiko, anything on who's demoing would help.
keiko: Will push on it. I'll ask casually which vendors came through, maybe through their informatics lead since she's friendly with us.
keiko: Also, on the procurement side: I hinted at 20% off list to their procurement lead on our last call, just to set expectations. She didn't push back. Tomas, that should fit your pricing scenarios.
darnell: Gabe, once the QBR deck is trimmed, send me the exec summary version. I want to preview it before the sponsor meeting.
```

> **>>> DECIDE AFTER THIS:** darnell: Gabe, once the QBR deck is trimmed, send me the exec summary version. I want to preview it before the sponsor meeting.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

---

## Row 13

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
dmitri: If those ranks show up as stragglers in burn-in, I want that in the writeup before we lock the placement.
wen: Pulling the current placement map now so I can see which leaf those ranks sit on and what's free to swap into.
lucia: Mapping exported. Both ports are on leaf 7, and the ranks are mostly the last GPU slots per node. Dropping the CSV in the channel.
hana: Got the CSV. Cross-referencing against burn-in straggler logs now, last GPU slots on leaf 7 are my first suspects.
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
```

> **>>> DECIDE AFTER THIS:** dmitri: Actually make that Oct 12, not Oct 5. Fabric firmware rollout needs another week.

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 14

**Today: Thu Sep 10** · #eng

**Team facts as of now**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Thu Sep 10 · #eng ---
oli: Memory store still unchecked. aj, do you have a baseline yet for concurrent reads on shared memory with lots of agents active?
alex: Love the fake chatter idea. Should the sandbox agents have names and personalities so people can tell them apart at a glance? Maybe a little name card at the demo table?
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
```

> **>>> DECIDE AFTER THIS:** olavo: For the launch post, can I show agents joining a thread on their own? Want a clean gif, no double bubbles obviously 😅

**Team facts again**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

---

## Row 15

**Today: Mon Sep 14** · #launch

**Team facts as of now**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Sep 14 · #launch ---
oli: fyi the two open onboarding tickets are both around the add-agents step, one's a flaky state on the skip button. will ping when it's stable.
alex: if the skip button is flaky, should the add-agents step stay skippable at all? Might be cleaner to make it required for admins, just thinking out loud
olavo: catching up, can the waitlist email still go out the day before Sep 17 like we planned? want to lock the send slot 📬
frida: another partner question: can admins mute agents per channel? They're nervous about agents jumping into threads untagged 🤔
aj: Per-channel mute isn't something I can confirm yet. Need to check whether agent permissions are scoped per channel or only per workspace.
oli: repro for the skip button: go back from the next step and the state resets, so skip shows enabled when it shouldn't. Tracing it.
alex: does the reset also hit people who go back after already adding an agent? Might show an empty list again 🤔
alex: quick q, who actually sends the waitlist email? I need to know who to give the header image to 📬
olavo: me! send the header image my way, I'm sending the waitlist email 📬
alex: Sending the header image over now. I made a dark and a light version, so pick whichever fits the email template 🎨
frida: Another partner asked if there's a visible indicator when an agent joins a thread untagged. Would calm the nerves a bit 🙂
alex: Could be a small badge or avatar ring on the message when an agent joins untagged. I can mock a couple options 🎨
aj: Update: the forwarded-DM permission check is merged. Forwarding a DM into a channel now checks the original DM's access first. That one's done.
oli: @alex yes, going back after adding an agent also resets the list view. Same root cause, so the fix should cover both. Testing it now.
frida: One more partner question: can admins see what an agent has stored in shared memory? They want to check it's not holding anything odd 🤔
```

> **>>> DECIDE AFTER THIS:** frida: One more partner question: can admins see what an agent has stored in shared memory? They want to check it's not holding anything odd 🤔

**Team facts again**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

---

## Row 16

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
--- Mon Oct 12 · #harbor ---
nadia: For the contamination section, let's say "near-duplicate" and keep the tone factual. No "leaked" or "cheated" wording, since reviewers will read that as an accusation.
yuki: For the patched-versus-untouched plot, I'd add bootstrap intervals per scaffold. Otherwise a small gap on a few tasks will look bigger than it is.
theo: Resample over tasks, not seeds, right? Otherwise the intervals on the refactor scaffold will look tighter than they should.
yuki: Yes, resample over tasks. Seeds within a task are correlated, so seed-level resampling would understate the spread. Task-level bootstrap, then average seeds inside each draw.
theo: Got it, task-level bootstrap. I'll add the interval bands to the patched-versus-untouched plot per scaffold and flag the refactor one if it looks wide.
marcus: Tutorial-repo commit dates are mostly earlier than the task repos, so I'll describe those fixtures in their own paragraph with the overlay.
--- Wed Oct 21 · #harbor ---
nadia: Two days out. Can everyone post what's still open on your side in here? I'll sort the final list from that.
elena: Cluster queue looks fine on my side. Only thing open is making sure the last batch of eval jobs doesn't get preempted overnight.
theo: Mine's the results table. Two of the baseline rows still have old numbers in them, so I need to refresh those before anyone quotes the table.
yuki: Open on my side: the pass criteria paragraph in the methods section still reads ambiguously. Want to tighten the wording before anyone cites it.
marcus: Mine's the contamination writeup. Need to reword how we describe the overlap check so reviewers don't read it as stronger than it is.
felix: Mine's the release checklist. Changelog is drafted but I still need to go through the tagging steps and double-check the package notes match the paper.
nadia: Thanks all. Theo, can you flag which two baseline rows are stale so Yuki and Marcus know what not to quote yet?
felix: My release jobs are queued behind the eval batch. Who actually owns the compute reservation for the eval runs? Want to know who to ping if they stall.
yuki: Also noticed the pass@1 plot in the draft has a y-axis that makes the gap between models look bigger than it is. Worth rescaling.
```

> **>>> DECIDE AFTER THIS:** yuki: Also noticed the pass@1 plot in the draft has a y-axis that makes the gap between models look bigger than it is. Worth rescaling.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,140 items (changed Mon Oct 19; previously 1,200 items)
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 17

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
```

> **>>> DECIDE AFTER THIS:** aj: Afaik invoices go to the owner's email only. No separate billing contact field in settings yet, I'd have to check how the Stripe side is wired.

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

## Row 18

**Today: Thu Oct 15** · #acct-northwind

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 12 · #acct-northwind ---
rachel: Whatever Tomas finds, finance will want any discount tied to something we get back. Expanded departments could be that trade.
keiko: Their finance lead keeps asking for a peer example of a multi-department rollout. Anything shareable I can bring to the sponsor call?
darnell: There's a regional health system we rolled out across departments. I'll ask if they'd do a reference call; otherwise an anonymized story works.
rachel: Keiko, when you talk to the sponsor, ask who in finance signs off on the discount. I want them in the loop early.
keiko: Will do. I'll also ask if finance wants to see the rollout plan before the discount conversation or alongside it.
darnell: Good. Also worth asking the sponsor whether other departments have already been asking about this. Internal pull makes the expansion story much easier.
keiko: Will do. I'll also see if the sponsor can intro me to the department leads who've been asking, so we can hear their use cases directly.
gabe: Nice, that'd help me too. If I can hear the department leads' use cases, I can sketch the integration shape for each.
rachel: Good. Tomas, once you've sorted the pricing block, ping me before anything goes into the order form draft.
--- Thu Oct 15 · #acct-northwind ---
rachel: Kicking off QBR prep for Northwind. Gabe's check-in cleared the technical side, so now we need a position on term length for the renewal. Tomas, can you model one-year vs multi-year?
keiko: Darnell, for the Northwind QBR dinner, their team mentioned they'd love somewhere quiet enough to actually talk. Any spots you like?
tomas: Yes, I'll model both. For the multi-year case, do we want the discount held flat or stepped across the years?
keiko: Their procurement lead keeps asking about price protection in the later years, so flat might land better. Stepped could feel like a hidden increase to them.
darnell: Quiet is the right call. There's a place with a back room I've used before, good for small groups. I'll check if it's open for us.
ines: If we go flat across years, I'd want the order form to say price holds only while volume stays in the committed band. Otherwise we're exposed.
```

> **>>> DECIDE AFTER THIS:** ines: If we go flat across years, I'd want the order form to say price holds only while volume stays in the committed band. Otherwise we're exposed.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

---

## Row 19

**Today: Mon Sep 28** · #kestrel-run

**Team facts as of now**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Sep 28 · #kestrel-run ---
dmitri: Kickoff thread for kestrel. Need start date, allocation, stability rules and data readiness all pinned down in here today. Who has blockers?
lucia: Fabric blocker from my side: two leaf switches in the new pod still flap under heavy all-reduce. Haven't isolated whether it's optics or firmware.
wen: Do those flapping leaf switches sit in the pod I was planning to hand kestrel? If so I need to rework the allocation table.
lucia: Yes, same pod. Both flapping leafs feed racks in that pod. Seeing CRC errors on the uplinks, so I'm leaning optics, but not confirmed.
dmitri: Decision: kestrel starts Oct 5. Lucia, get the optics vs firmware call made and fixed well before then. Wen, redo the allocation table around whatever the pod looks like once that's resolved.
lucia: Pulling optic transceiver serials on the flapping uplinks now. If they share a batch, that settles it. Will swap one and rerun all-reduce soak.
wen: Whichever way the optics call goes, I'll draft two allocation variants: one with the flapping racks drained, one assuming they come back clean.
dmitri: Quick check Wen: is the kestrel node allocation 2,048 nodes? Want that confirmed before the variants go out.
wen: yep, confirmed
kofi: If the flapping racks get drained, I need to know before I size checkpoint shards. Fewer nodes changes the per-rank write pattern to storage.
mateo: Data side is looking fine so far. Tokenized shards are landing on the new filesystem, just waiting on the last dedup pass to finish.
hana: Whichever variant wins, I want straggler detection on from step zero. Flapping links would show up as a few slow ranks dragging MFU down.
```

> **>>> DECIDE AFTER THIS:** hana: Whichever variant wins, I want straggler detection on from step zero. Flapping links would show up as a few slow ranks dragging MFU down.

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes

---

## Row 20

**Today: Thu Sep 10** · #eng

**Team facts as of now**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Thu Sep 10 · #eng ---
frida: Yes, something relatable like two people arguing over which snack order to get for the lunch 😂 agent jumps in with a tally
alex: Slightly random, but does the agent typing indicator also fire for the double replies? Would be good to know for the onboarding demo.
oli: Alex: yes, typing indicator fires per agent, so you'd see two bubbles for a double reply. Not great for a demo, I'd avoid that scenario.
alex: Haha perfect. Should I mock up the snack thread in the sandbox so the agent's reply looks natural on screen? I can draft it.
olavo: For the launch post, can I show agents joining a thread on their own? Want a clean gif, no double bubbles obviously 😅
oli: Olavo: thread-join gif is fine as long as only one agent is in the channel. Use a single-agent demo workspace.
frida: Yes please! Draft it and I'll run it past a couple of partners to see if the snack banter feels real 😊
alex: Okay so for the single-agent demo workspace, should I mock up the onboarding screens with just one agent in the sidebar? Easier to screenshot.
olavo: Yes please Alex, one agent in the sidebar works for me too. I'll grab screenshots from it for the press kit as well.
aj: Oli, pulled up the sim harness. It fakes channel traffic fine, but I'll need to tweak it so agents hit shared memory entries, not just channels.
oli: Makes sense. Have them hit a small set of hot entries plus a wide spread, so we see both contention and the normal case.
frida: Heard back from the partner: their agents mostly hit the same couple of standup channels during the rush. Sounds like hot entries to me.
aj: That fits the hot-entry case then. I'll weight the sim toward a few shared entries and log p95 read latency per run.
alex: Different thing, for the onboarding copy: if someone @-mentions an agent inside a DM, can that agent read the DM? Or is it blocked unless the agent is a member of it?
oli: aj, log write latency too, not just reads. Standup rush probably has agents saving summaries to memory at the same moment.
```

> **>>> DECIDE AFTER THIS:** oli: aj, log write latency too, not just reads. Standup rush probably has agents saving summaries to memory at the same moment.

**Team facts again**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

---

## Row 21

**Today: Tue Sep 8** · #launch

**Team facts as of now**

- (nothing decided yet)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Tue Sep 8 · #launch ---
sara: ok team, launch kickoff. I'm going to lock the date, the raise announcement, pricing and who owns what for launch week. Read along, shout if something's off.
alex: reading along 👀 quick q: are we showing the agent-as-member idea in the onboarding flow at launch, or keeping that for after?
frida: +1 to Alex's q. Two design partners got lost on day one because they didn't realize the agent shows up in the member list.
oli: Agent already has its own member entry in the runtime, so showing it in onboarding is just a UI change. No backend work needed.
alex: nice, then I can mock it as a pinned card in the welcome step. should the agent introduce itself there or stay quiet until tagged?
sara: Locking the date first: public launch is Sep 17. Alex, agent introduces itself in the welcome card, yes. Keep it short, one line.
```

> **>>> DECIDE AFTER THIS:** sara: Locking the date first: public launch is Sep 17. Alex, agent introduces itself in the welcome card, yes. Keep it short, one line.

**Team facts again**

- (nothing decided yet)

---

## Row 22

**Today: Fri Sep 18** · #eng

**Team facts as of now**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per human seat, agents free (changed Wed Sep 16; previously $12 per seat, agent actions metered)
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: Olavo to send the press kit to the embargoed reporters (check point: Fri Sep 18)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Thu Sep 10 · #eng ---
aj: Oli, pulled up the sim harness. It fakes channel traffic fine, but I'll need to tweak it so agents hit shared memory entries, not just channels.
oli: Makes sense. Have them hit a small set of hot entries plus a wide spread, so we see both contention and the normal case.
frida: Heard back from the partner: their agents mostly hit the same couple of standup channels during the rush. Sounds like hot entries to me.
aj: That fits the hot-entry case then. I'll weight the sim toward a few shared entries and log p95 read latency per run.
alex: Different thing, for the onboarding copy: if someone @-mentions an agent inside a DM, can that agent read the DM? Or is it blocked unless the agent is a member of it?
oli: aj, log write latency too, not just reads. Standup rush probably has agents saving summaries to memory at the same moment.
aj: Will do, write latency goes in the same log. I'll also tag each run with how many agents were active.
frida: I'll also ask that partner whether their standup agents all save summaries at the same moment. Useful for the write-latency runs.
alex: Still need an answer on my DM @-mention question, whoever knows it best. The onboarding copy depends on it 🙏
oli: aj, that's your area. Can you take Alex's DM @-mention question? He needs it for the onboarding copy.
alex: On it! I'll keep the banter light and ping you the draft in a bit. Might add a pun in the agent's tally 😄
aj: Yep, I'll take it. Rechecking the permission code first so Alex gets exact wording for the copy, not my memory of it.
--- Fri Sep 18 · #eng ---
oli: bug bash board is up. 3 p1s so far, all in agent thread-join logic. agents jumping into threads where nobody asked them to
olavo: hey Frida, reporters keep asking for slots to talk to a design partner. Any of your customers up for a quick interview?
aj: Is it the join heuristic firing on keyword match, or is it the memory store surfacing old threads as relevant? Those look the same from outside.
```

> **>>> DECIDE AFTER THIS:** aj: Is it the join heuristic firing on keyword match, or is it the memory store surfacing old threads as relevant? Those look the same from outside.

**Team facts again**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per human seat, agents free (changed Wed Sep 16; previously $12 per seat, agent actions metered)
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: Olavo to send the press kit to the embargoed reporters (check point: Fri Sep 18)

---

## Row 23

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
olavo: Also for the launch post, we should probably have a short demo gif of the shared memory bit. People love seeing that 🎬
oli: For the memory gif, I can set up a clean demo workspace with seeded convos so it records without weird leftovers 🎬
```

> **>>> DECIDE AFTER THIS:** oli: For the memory gif, I can set up a clean demo workspace with seeded convos so it records without weird leftovers 🎬

**Team facts again**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

---

## Row 24

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
yuki: Open on my side: the pass criteria paragraph in the methods section still reads ambiguously. Want to tighten the wording before anyone cites it.
marcus: Mine's the contamination writeup. Need to reword how we describe the overlap check so reviewers don't read it as stronger than it is.
felix: Mine's the release checklist. Changelog is drafted but I still need to go through the tagging steps and double-check the package notes match the paper.
nadia: Thanks all. Theo, can you flag which two baseline rows are stale so Yuki and Marcus know what not to quote yet?
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
```

> **>>> DECIDE AFTER THIS:** yuki: Related caption point: a few runs hit sandbox timeouts mid-task. We should say whether those count as failures or get excluded.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,140 items (changed Mon Oct 19; previously 1,200 items)
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 25

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
lucia: Second C uplink just retrained again, so I'm swapping the cable on that one. Firmware stays parked until counters hold clean.
hana: Once the patch lands, can we run a resume test from a save taken while a C link is deliberately flapping? Want to see the hash check actually trip.
mateo: takeout works, but then it's cold by the time I walk back. what if I just order ahead from the noodle place and pick it up on the way?
kofi: Yes, can do. I'll inject the flap via a fault script on the C leaf port so the short write actually hits a writer rank.
lucia: ordering ahead works. does their app let you set a pickup time? I want it ready right when I'm free between calls
mateo: Heads up, if we run that flap test, dataloader reads from the storage tier on C nodes might stall too. I'll watch for stragglers on the loader side.
wen: If the flap test stalls loaders on C, I can drain those nodes into the spare pool during the run. Which leaf ports are affected?
lucia: Affected ports are on the C leaf, the two uplinks I reseated and recabled. I'll post exact port IDs once counters settle.
mateo: yeah the app has a pickup time picker, I'll set it for when your call wraps. want the usual or something different?
hana: I'll add a monitor on resume that logs hash mismatch counts per rank, so a tripped check shows up on the dashboard and not just in logs.
kofi: Per-rank mismatch counts on the dashboard works for me. I'll emit the hash result as a structured log line so your monitor can scrape it.
lucia: the usual works. the spicy one with extra greens. my call wraps around the half hour, probably runs over though, IB flap again
mateo: Loader side I'll tag reads from C nodes in the metrics so stalls show up per node, not just aggregate throughput.
lucia: Cable swap on the second uplink done. Retrain count on that port is flat so far, watching optics levels on the C leaf.
mateo: ha, IB flap again. I'll pad the pickup a bit so it doesn't sit. I'll grab it and drop it at your desk.
```

> **>>> DECIDE AFTER THIS:** mateo: ha, IB flap again. I'll pad the pickup a bit so it doesn't sit. I'll grab it and drop it at your desk.

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 26

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
```

> **>>> DECIDE AFTER THIS:** alex: Back to FAQ wording. When an agent jumps into a thread untagged, do we say "joins" or "chimes in"? Partners might read that as intrusive.

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

## Row 27

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
lucia: Firmware rollout on the IB leaf switches is staged but not pushed. Seeing a few flapping links on rack group C that I want to look at first.
kofi: Are the flapping links on C causing NCCL timeouts yet? Want to know if checkpoint writes from those nodes are getting stalled mid-save.
hana: Quick check while we're on checkpoints: kestrel checkpoint cadence is every 500 steps, right? React ✅ if that's what you have.
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
```

> **>>> DECIDE AFTER THIS:** hana: That's bad for resume too. If a partial shard gets marked complete, we'd only see it as a loss spike after restart. Can we add a checksum verify on load?

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 28

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
gabe: Sure, I'll write one up in Python with exponential backoff, full jitter, and a cap. Should honor the retry-after header too.
darnell: Their exec sponsor liked the intake demo last quarter. Once the tuning story is solid, that's a good thing to bring back up.
```

> **>>> DECIDE AFTER THIS:** darnell: Their exec sponsor liked the intake demo last quarter. Once the tuning story is solid, that's a good thing to bring back up.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Gabe to load-test Northwind's workload at their full rate limit (check point: Wed Oct 14)

---

## Row 29

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
aj: For the screenshot thread, can someone confirm the agent's reply doesn't quote anything from a private channel? Memory recall can surface odd stuff.
frida: Good catch AJ. I'll read the deploy thread end to end for anything that looks pulled from a private channel before it goes anywhere.
```

> **>>> DECIDE AFTER THIS:** frida: Good catch AJ. I'll read the deploy thread end to end for anything that looks pulled from a private channel before it goes anywhere.

**Team facts again**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per human seat, agents free (changed Wed Sep 16; previously $12 per seat, agent actions metered)
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

---

## Row 30

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
frida: Thanks Oli. Separate thing: I told the agency heads-up that after launch it's agent actions metered, so their invoice will vary month to month. They were fine with it, just wanted finance to know.
alex: Back to FAQ wording. When an agent jumps into a thread untagged, do we say "joins" or "chimes in"? Partners might read that as intrusive.
olavo: "Joins" reads calmer to me, "chimes in" sounds like butting in. Maybe a line in the FAQ about muting an agent per channel?
alex: Good idea on muting. Should it be per channel only, or can someone mute an agent in just one thread too? Partners will ask.
aj: Per channel is easy since mute is a membership-level flag. Per thread means a new subscription state to track, and search needs to respect it too.
frida: One partner mentioned wanting an agent quiet in one noisy thread but still active in the channel. So per-thread might come up.
frida: Unrelated, heads up: I need to leave early Thursday for a family thing. Can someone cover partner questions in the afternoon? Happy to leave notes on who's waiting on what.
oli: I can take partner questions Thursday afternoon, but only the technical ones. Frida, put billing stuff in your notes separately.
alex: Thanks Oli. Frida, could you also jot down which partners asked about per-thread muting? I'd like to quote them in the FAQ review.
frida: Yep, will do. Two of them mentioned it so far, I'll add names and what they said to my notes doc.
olavo: For the waitlist email, should I mention agents can be muted? Feels like a good trust line, but don't want to overpromise on per-thread.
alex: Quick question on muting: does a muted agent still read the channel for memory, or fully stop? Partners will ask.
aj: Mute as built only silences posting and notifications. Memory indexing still runs on the channel. A true stop-reading option would be a separate flag.
alex: Random q while we're on the waitlist email: who's actually sending it Thursday? Olavo, is that you, or does Sara hit send?
frida: Another partner question: if they remove an agent from the workspace, does its shared memory get wiped or stay searchable?
```

> **>>> DECIDE AFTER THIS:** frida: Another partner question: if they remove an agent from the workspace, does its shared memory get wiped or stay searchable?

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

## Row 31

**Today: Thu Sep 10** · #eng

**Team facts as of now**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Thu Sep 10 · #eng ---
frida: Yes please! Draft it and I'll run it past a couple of partners to see if the snack banter feels real 😊
alex: Okay so for the single-agent demo workspace, should I mock up the onboarding screens with just one agent in the sidebar? Easier to screenshot.
olavo: Yes please Alex, one agent in the sidebar works for me too. I'll grab screenshots from it for the press kit as well.
aj: Oli, pulled up the sim harness. It fakes channel traffic fine, but I'll need to tweak it so agents hit shared memory entries, not just channels.
oli: Makes sense. Have them hit a small set of hot entries plus a wide spread, so we see both contention and the normal case.
frida: Heard back from the partner: their agents mostly hit the same couple of standup channels during the rush. Sounds like hot entries to me.
aj: That fits the hot-entry case then. I'll weight the sim toward a few shared entries and log p95 read latency per run.
alex: Different thing, for the onboarding copy: if someone @-mentions an agent inside a DM, can that agent read the DM? Or is it blocked unless the agent is a member of it?
oli: aj, log write latency too, not just reads. Standup rush probably has agents saving summaries to memory at the same moment.
aj: Will do, write latency goes in the same log. I'll also tag each run with how many agents were active.
frida: I'll also ask that partner whether their standup agents all save summaries at the same moment. Useful for the write-latency runs.
alex: Still need an answer on my DM @-mention question, whoever knows it best. The onboarding copy depends on it 🙏
oli: aj, that's your area. Can you take Alex's DM @-mention question? He needs it for the onboarding copy.
alex: On it! I'll keep the banter light and ping you the draft in a bit. Might add a pun in the agent's tally 😄
aj: Yep, I'll take it. Rechecking the permission code first so Alex gets exact wording for the copy, not my memory of it.
```

> **>>> DECIDE AFTER THIS:** aj: Yep, I'll take it. Rechecking the permission code first so Alex gets exact wording for the copy, not my memory of it.

**Team facts again**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

---

## Row 32

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
gabe: Sure, I'll write one up in Python with exponential backoff, full jitter, and a cap. Should honor the retry-after header too.
```

> **>>> DECIDE AFTER THIS:** gabe: Sure, I'll write one up in Python with exponential backoff, full jitter, and a cap. Should honor the retry-after header too.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Gabe to load-test Northwind's workload at their full rate limit (check point: Wed Oct 14)

---

## Row 33

**Today: Mon Oct 5** · #harbor

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 5 · #harbor ---
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
marcus: Rust build tool license came back permissive, so those candidates are usable. The fix touches the parser and config loader together, and the tests are deterministic.
```

> **>>> DECIDE AFTER THIS:** marcus: Rust build tool license came back permissive, so those candidates are usable. The fix touches the parser and config loader together, and the tests are deterministic.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena

---

## Row 34

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
--- Wed Sep 30 · #infra ---
mateo: Still need to answer Hana's headroom question. Pulling current tier usage now, sidecar overhead per shard is the part I haven't measured.
dmitri: Lucia, put a draft rotation in the thread. C leaf pages shouldn't sit on one person while firmware is parked. Kofi and Wen should be on it.
lucia: Draft rotation going up in the thread shortly. Kofi primary on C leaf pages, Wen as backup for drains. Shout if that's wrong.
--- Fri Oct 9 · #infra ---
hana: Post-mortem notes from Thursday's node failure are up in the doc. Loss spiked about 40 steps before the rank dropped, so I want to check whether grad-norm alerts could have caught it earlier. Kofi, can you sanity check the timeline?
lucia: Pulled IB port counters overnight. One leaf uplink is showing creeping symbol errors, still below the alarm line. Keeping an eye on it.
wen: Vendor folks want to come onsite and look at the cluster. Dmitri, you want to be in the room for that or should I just handle it?
wen: Which leaf is that? Want to see if any kestrel nodes hang off it before I touch the spare pool.
dmitri: I'd like to be there. Want them to see the IB fabric flaps firsthand, not just hear about them secondhand.
lucia: Leaf 14, uplink on the second spine side. Checking now which node ranks map to it, will paste the list.
wen: Makes sense. Lucia's flap logs would help here. I'd also like them to check the transceivers on the leaf switches while they're in the hall.
kofi: Going with my Oct 5 suggestion on the kestrel checkpoint cadence. Applying it now, so the restart drill will exercise it. Hana, I'll check your timeline after.
hana: Kofi, which suggestion is that? Don't see it in the doc. Need to know what the drill is actually exercising before I set up the monitoring side.
dmitri: Yes, transceivers too. Flaps cluster on a few leaf ports, so I want vendor eyes on those optics and the cable runs.
lucia: Leaf 14 maps to a contiguous block of kestrel ranks in one rack. No NCCL timeouts on them so far. List is in the doc.
wen: Single rack block is easy to drain if it comes to that. Checking which spares sit off leaf 14 so we're not swapping onto the same uplink.
```

> **>>> DECIDE AFTER THIS:** wen: Single rack block is easy to drain if it comes to that. Checking which spares sit off leaf 14 so we're not swapping onto the same uplink.

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps (changed Fri Oct 9; previously every 500 steps)
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

---

## Row 35

**Today: Mon Oct 5** · #harbor

**Team facts as of now**

- (nothing decided yet)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 5 · #harbor ---
nadia: Morning all. Want to line up the release and the paper this week. Who has the latest on contamination fixes and where compute stands?
```

> **>>> DECIDE AFTER THIS:** nadia: Morning all. Want to line up the release and the paper this week. Who has the latest on contamination fixes and where compute stands?

**Team facts again**

- (nothing decided yet)

---

## Row 36

**Today: Thu Oct 8** · #acct-northwind-eng

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Thu Oct 8 · #acct-northwind-eng ---
gabe: Looks like they fire a burst of parallel requests at open with no backoff. Retries just pile on and make the 429s worse.
keiko: Quick check before I reply to their ops lead: is Northwind's rate limit 40M tokens per minute? React 👍 if so.
gabe: Did you see the postmortem another enterprise customer posted? Their retry storm took down their own gateway for hours.
(gabe reacted 👍 to keiko's message)
keiko: Thanks. So it's burst shape, not capacity. Gabe, can you share a backoff-with-jitter example I can send their ops lead?
gabe: Yep, I'll pull a Python snippet with exponential backoff and full jitter. Also worth suggesting they stagger the opening burst with a small queue.
keiko: Their ops lead also asked if the intake assistant can use a lighter model for the simple form-filling steps. Worth a look?
gabe: Yes, likely. Form-filling is mostly structured extraction, so a smaller model should handle it. I'd want to test accuracy on their real intake forms first.
ines: Since they're sending patient intake data through this, flagging the retention side: zero data retention is approved for Northwind. Worth keeping that in mind when we test on their real forms.
rachel: Yes, saw it. Ouch. Makes me wonder if Northwind's team has backoff with jitter on their side. Worth a quick check with them?
gabe: Good point. I'll ask their ops lead for de-identified sample forms so we can compare the smaller model without touching real patient records.
ines: Also, that applies to all endpoints, batch included, so the same coverage holds if they move the form-filling there.
keiko: Great, I'll ask their ops lead for the de-identified forms and mention the stagger idea when I send the snippet.
gabe: Also spotted their retry loop has no max attempts, so one stuck request can hang an entire intake session. I'll add a cap to the snippet.
keiko: Their ops lead will love the cap. Last week she said a frozen intake session meant staff fell back to paper forms.
```

> **>>> DECIDE AFTER THIS:** keiko: Their ops lead will love the cap. Last week she said a frozen intake session meant staff fell back to paper forms.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

---

## Row 37

**Today: Thu Oct 15** · #acct-northwind

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 12 · #acct-northwind ---
tomas: Rachel, understood. I'm re-checking which approval record I built the pricing block from and will report back once I've compared it against your framing.
rachel: Whatever Tomas finds, finance will want any discount tied to something we get back. Expanded departments could be that trade.
keiko: Their finance lead keeps asking for a peer example of a multi-department rollout. Anything shareable I can bring to the sponsor call?
darnell: There's a regional health system we rolled out across departments. I'll ask if they'd do a reference call; otherwise an anonymized story works.
rachel: Keiko, when you talk to the sponsor, ask who in finance signs off on the discount. I want them in the loop early.
keiko: Will do. I'll also ask if finance wants to see the rollout plan before the discount conversation or alongside it.
darnell: Good. Also worth asking the sponsor whether other departments have already been asking about this. Internal pull makes the expansion story much easier.
keiko: Will do. I'll also see if the sponsor can intro me to the department leads who've been asking, so we can hear their use cases directly.
gabe: Nice, that'd help me too. If I can hear the department leads' use cases, I can sketch the integration shape for each.
rachel: Good. Tomas, once you've sorted the pricing block, ping me before anything goes into the order form draft.
--- Thu Oct 15 · #acct-northwind ---
rachel: Kicking off QBR prep for Northwind. Gabe's check-in cleared the technical side, so now we need a position on term length for the renewal. Tomas, can you model one-year vs multi-year?
keiko: Darnell, for the Northwind QBR dinner, their team mentioned they'd love somewhere quiet enough to actually talk. Any spots you like?
tomas: Yes, I'll model both. For the multi-year case, do we want the discount held flat or stepped across the years?
keiko: Their procurement lead keeps asking about price protection in the later years, so flat might land better. Stepped could feel like a hidden increase to them.
darnell: Quiet is the right call. There's a place with a back room I've used before, good for small groups. I'll check if it's open for us.
```

> **>>> DECIDE AFTER THIS:** darnell: Quiet is the right call. There's a place with a back room I've used before, good for small groups. I'll check if it's open for us.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

---

## Row 38

**Today: Thu Oct 8** · #acct-northwind-eng

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Thu Oct 8 · #acct-northwind-eng ---
gabe: Pulled Northwind's usage logs from the last few weeks. Traffic is spiky around their morning clinic intake, lots of 429s in that window.
keiko: That tracks with what their ops lead told me on the call. Intake staff complained the assistant stalls right when the clinics open.
gabe: Looks like they fire a burst of parallel requests at open with no backoff. Retries just pile on and make the 429s worse.
keiko: Quick check before I reply to their ops lead: is Northwind's rate limit 40M tokens per minute? React 👍 if so.
gabe: Did you see the postmortem another enterprise customer posted? Their retry storm took down their own gateway for hours.
(gabe reacted 👍 to keiko's message)
keiko: Thanks. So it's burst shape, not capacity. Gabe, can you share a backoff-with-jitter example I can send their ops lead?
gabe: Yep, I'll pull a Python snippet with exponential backoff and full jitter. Also worth suggesting they stagger the opening burst with a small queue.
keiko: Their ops lead also asked if the intake assistant can use a lighter model for the simple form-filling steps. Worth a look?
gabe: Yes, likely. Form-filling is mostly structured extraction, so a smaller model should handle it. I'd want to test accuracy on their real intake forms first.
```

> **>>> DECIDE AFTER THIS:** gabe: Yes, likely. Form-filling is mostly structured extraction, so a smaller model should handle it. I'd want to test accuracy on their real intake forms first.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

---

## Row 39

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
marcus: Quick look says most removals were web-app tasks with near-duplicate repos upstream. Long-horizon barely touched, but I'll confirm the per-category split.
felix: If the removals are mostly web-app forks, I can list the upstream repos that triggered them in the release notes. Might be useful for an appendix footnote too.
theo: Can you drop the removed item ids somewhere I can load them? The notebook filters by id, so the tables will just regenerate.
nadia: Side note while we're regenerating tables: we'll decide whether the 3-shot results go in the paper at the Tue Oct 20 paper sync. Theo, export them too so we have both options ready.
marcus: Putting the removed ids in the shared data folder as a flat file, one per line, with the upstream repo that flagged each.
yuki: Recorded runs works for me. We could replay a few agent traces on a projector and talk through them, honestly more useful than live.
yuki: Once the ids are in, can you also log which categories each removal came from? I'd like that next to the plateau figure.
theo: Got it, I'll add a category column to the export so the removal counts sit beside the per-category pass rates. Plateau figure should line up then.
felix: Good, I'll find traces where the agent loops on a flaky test. Those make better discussion than clean passes. Lake house is looking good.
elena: If the tables regenerate, do the plateau curves need a rerun too, or are those computed from cached trajectories?
theo: Curves come from cached trajectories, so no rerun. Just refilter by id and regenerate. Only the plateau figure needs a fresh pass with the smaller denominator.
yuki: Before the refilter, can someone check the build-loop task I picked for the transcript isn't among the removed ids? Awkward to show a task we dropped.
marcus: Good catch. That build-loop task is a CLI tooling repo, not a web-app fork, so it's likely fine. I'll grep the id file against it to be sure.
theo: Dataset section in the draft says 1,200 items, so I'm building the tables to match that. Will grep the plateau task id once Marcus's file is up.
yuki: Drafting the plateau sentence meanwhile. I'd say agents "stall in repair loops" rather than "hit a ceiling", since ceiling implies a capability limit we haven't shown.
```

> **>>> DECIDE AFTER THIS:** yuki: Drafting the plateau sentence meanwhile. I'd say agents "stall in repair loops" rather than "hit a ceiling", since ceiling implies a capability limit we haven't shown.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,140 items (changed Mon Oct 19; previously 1,200 items)
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)
- open item: Nadia to decide whether the 3-shot results go in the paper (check point: Tue Oct 20 paper sync)

---

## Row 40

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
hana: Once the patch lands, can we run a resume test from a save taken while a C link is deliberately flapping? Want to see the hash check actually trip.
mateo: takeout works, but then it's cold by the time I walk back. what if I just order ahead from the noodle place and pick it up on the way?
kofi: Yes, can do. I'll inject the flap via a fault script on the C leaf port so the short write actually hits a writer rank.
lucia: ordering ahead works. does their app let you set a pickup time? I want it ready right when I'm free between calls
mateo: Heads up, if we run that flap test, dataloader reads from the storage tier on C nodes might stall too. I'll watch for stragglers on the loader side.
wen: If the flap test stalls loaders on C, I can drain those nodes into the spare pool during the run. Which leaf ports are affected?
lucia: Affected ports are on the C leaf, the two uplinks I reseated and recabled. I'll post exact port IDs once counters settle.
mateo: yeah the app has a pickup time picker, I'll set it for when your call wraps. want the usual or something different?
hana: I'll add a monitor on resume that logs hash mismatch counts per rank, so a tripped check shows up on the dashboard and not just in logs.
kofi: Per-rank mismatch counts on the dashboard works for me. I'll emit the hash result as a structured log line so your monitor can scrape it.
lucia: the usual works. the spicy one with extra greens. my call wraps around the half hour, probably runs over though, IB flap again
mateo: Loader side I'll tag reads from C nodes in the metrics so stalls show up per node, not just aggregate throughput.
lucia: Cable swap on the second uplink done. Retrain count on that port is flat so far, watching optics levels on the C leaf.
mateo: ha, IB flap again. I'll pad the pickup a bit so it doesn't sit. I'll grab it and drop it at your desk.
kofi: Patch is up for review. Injected short write on a writer rank now retries instead of flipping the shard to complete. Hash lines look right in the structured log.
```

> **>>> DECIDE AFTER THIS:** kofi: Patch is up for review. Injected short write on a writer rank now retries instead of flipping the shard to complete. Hash lines look right in the structured log.

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 41

**Today: Wed Oct 7** · #harbor-evals

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Marcus to finish the license review for the scraped repositories (check point: Fri Oct 9)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Wed Oct 7 · #harbor-evals ---
nadia: Good call on the manifest tags. Marcus, can you also flag which backfilled items come from repos with unusual test setups? Paper reviewers will ask about that.
marcus: Will do on flagging the odd test setups. And I'll finish the license review for the scraped repositories by Fri Oct 9, so the manifest tags and the backfill list can build off it.
theo: Kicked off the seed reruns on the current baseline. Early plots look tight on the single-file bug-fix items, so we'll see how much the multi-file ones spread it.
theo: were the pending jobs the ones with the multi-node affinity flag? I saw that hang last week, scheduler seemed to wait on a placement it couldn't satisfy
yuki: For the paper, I'd report the bug-fix slice separately with confidence intervals. Single-file and multi-file items probably deserve their own breakdown too.
elena: Checked timeouts. The multi-file repos need a longer setup window for dependency installs, otherwise some items will fail before the tests even start.
felix: Longer install window should go in the harness config and the release notes, since it changes what a timeout failure means for those items.
elena: yeah, most of them had it. checking if the affinity label is even getting parsed, might be silently falling back to a placement that never resolves
theo: Plots so far: the multi-file items fail mostly on import errors, not logic. Might be the same install issue Elena hit, so I'll separate those out.
felix: Side note for the release notes: harbor-lite, the internal smoke set, has 200 items. Separate from the held-out set, so I'll keep the two clearly distinguished in the manifest.
yuki: If the import-error failures are really install issues, I'd exclude them from the bug-fix slice analysis or at least report them as a separate failure category. Otherwise we're measuring the environment, not the model.
theo: if it's falling back silently, try a dry-run submit with the flag and compare the resolved placement spec against a job that schedules fine
theo: Agreed. I'll split import errors into their own bucket in the plots and rerun once Elena's longer install window is in.
elena: Also thinking of prebuilding a cached dependency image per repo, so installs don't eat the timeout budget. I'll try it on the messiest multi-file ones first.
elena: good call, running the dry-run now. the resolved spec for the stuck ones has an empty topology field, the working job has it populated
```

> **>>> DECIDE AFTER THIS:** elena: good call, running the dry-run now. the resolved spec for the stuck ones has an empty topology field, the working job has it populated

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Marcus to finish the license review for the scraped repositories (check point: Fri Oct 9)

---

## Row 42

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
sara: On the prompt question, there's a bigger one behind it. We'll decide whether agents may DM a human first, without being asked, at the Mon Sep 21 design review. Hold the gating design until then.
frida: Will do! They're pretty chatty on Slack-style stuff, so I'll ask about naming and whether they'd prefer a call or video.
oli: ok, so I'll keep digging on the root cause in the join path but not touch the gate itself. Will log the trigger breakdown on the board.
frida: Heard back from the design partner: the summary was visible to everyone in the hiring thread, not just the poster. They want to know if agents can be kept out of certain channels entirely.
olavo: Perfect, video's better if they're okay with it, reporters can grab a screenshot of the workspace. Also ask if they have a fav agent moment to share 😄
frida: Separate thing: a design partner hit the double-posting bug again this morning. I'll ping AJ with the details since AND-341 is his.
aj: Keeping agents out of a channel is mostly a read-permission question for us. Does the partner want admins to set it, or any channel member?
frida: Good question, I'll ask. My guess is admins, since it was an HR-type channel, but I'll confirm with them.
frida: Ha yes, they told me last week the agent summarized a messy client thread before anyone asked. I'll get them to retell it 😄
oli: frida AND-341 is mine now, send the details to me. Ask if they saw both posts land at the same moment.
alex: For the 'keep agents out' ask, should the channel show some marker so members know agents can't see it? Otherwise people might assume the agent is reading.
aj: Marker makes sense, and it should come from the same permission flag so it can't drift from what the agent can actually read.
olavo: random q from the launch post side: can I say agents only join threads when relevant, or is that overselling given the hiring thread thing? 😅
oli: I'd skip 'only when relevant' for now. Memory-sourced joins misfire on stale threads. Something softer like 'can chime in' is safer.
olavo: Fair, 'can chime in' works for the post. Should I add a line about admins being able to keep agents out of channels, or too early?
```

> **>>> DECIDE AFTER THIS:** olavo: Fair, 'can chime in' works for the post. Should I add a line about admins being able to keep agents out of channels, or too early?

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

## Row 43

**Today: Thu Oct 8** · #acct-northwind-eng

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Thu Oct 8 · #acct-northwind-eng ---
keiko: That tracks with what their ops lead told me on the call. Intake staff complained the assistant stalls right when the clinics open.
gabe: Looks like they fire a burst of parallel requests at open with no backoff. Retries just pile on and make the 429s worse.
keiko: Quick check before I reply to their ops lead: is Northwind's rate limit 40M tokens per minute? React 👍 if so.
gabe: Did you see the postmortem another enterprise customer posted? Their retry storm took down their own gateway for hours.
(gabe reacted 👍 to keiko's message)
keiko: Thanks. So it's burst shape, not capacity. Gabe, can you share a backoff-with-jitter example I can send their ops lead?
gabe: Yep, I'll pull a Python snippet with exponential backoff and full jitter. Also worth suggesting they stagger the opening burst with a small queue.
keiko: Their ops lead also asked if the intake assistant can use a lighter model for the simple form-filling steps. Worth a look?
gabe: Yes, likely. Form-filling is mostly structured extraction, so a smaller model should handle it. I'd want to test accuracy on their real intake forms first.
ines: Since they're sending patient intake data through this, flagging the retention side: zero data retention is approved for Northwind. Worth keeping that in mind when we test on their real forms.
rachel: Yes, saw it. Ouch. Makes me wonder if Northwind's team has backoff with jitter on their side. Worth a quick check with them?
gabe: Good point. I'll ask their ops lead for de-identified sample forms so we can compare the smaller model without touching real patient records.
ines: Also, that applies to all endpoints, batch included, so the same coverage holds if they move the form-filling there.
keiko: Great, I'll ask their ops lead for the de-identified forms and mention the stagger idea when I send the snippet.
gabe: Also spotted their retry loop has no max attempts, so one stuck request can hang an entire intake session. I'll add a cap to the snippet.
```

> **>>> DECIDE AFTER THIS:** gabe: Also spotted their retry loop has no max attempts, so one stuck request can hang an entire intake session. I'll add a cap to the snippet.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

---

## Row 44

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
darnell: Their exec sponsor liked the intake demo last quarter. Once the tuning story is solid, that's a good thing to bring back up.
gabe: Also noticed their system prompt is huge and resent on every call. Trimming it or using prompt caching should cut latency on intake.
rachel: Perfect. Add a line or two on why jitter matters, so Keiko can frame it as a tip, not criticism.
keiko: Their ops lead hand-tuned that prompt for months, so she'll want reassurance that trimming won't change how the assistant behaves.
gabe: Fair. Caching keeps the prompt text identical, so behavior shouldn't shift. I can diff outputs on the de-identified forms before and after to show her.
gabe: Will do. I'll frame jitter as spreading retries out so clients don't all hit at once. Keiko can drop it in as a friendly tip.
rachel: Before/after diff on the forms would make a solid slide for the renewal deck. Customers like seeing proof, not promises.
rachel: Quick flag so nobody mixes them up: Northwind Logistics is a separate customer and renews Nov 15. Keep their numbers out of the Northwind Health deck.
gabe: On missing fields: yes. Have the model return a list of empty required fields in structured output, and the UI can highlight them for staff.
keiko: That's a clean answer, thanks. I'll pass it to their ops lead. She'll probably ask if staff can override a flagged field.
gabe: Yes, override is easy. I'd log which fields staff overrode though, so we can see where the model keeps misfiring.
keiko: Good call on logging overrides. Their ops lead will want a weekly view of the misfires, so staff feel heard rather than monitored.
gabe: A weekly misfire view is easy once overrides are logged. I can sketch a simple dashboard grouped by field type for her.
rachel: Great. Send it over when it's ready and I'll pass it to Keiko with a short intro. Keep the tone light.
keiko: A dashboard sketch would land well. She's also asking whether the misfire view can be shared with her floor supervisors, not just her.
```

> **>>> DECIDE AFTER THIS:** keiko: A dashboard sketch would land well. She's also asking whether the misfire view can be shared with her floor supervisors, not just her.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Gabe to load-test Northwind's workload at their full rate limit (check point: Wed Oct 14)

---

## Row 45

**Today: Wed Sep 16** · #gtm

**Team facts as of now**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Wed Sep 16 · #gtm ---
olavo: morning all! launch post draft v2 is up in the doc, would love eyes on the intro paragraph. also pricing page copy still needs a pass, I'll start on that after lunch 🚀
alex: read the intro, I like it. quick q: are we explaining what an agent as a workspace member means before the pricing section, or assuming people get it?
olavo: good q alex. I was thinking a short explainer box right above pricing, maybe with a screenshot of an agent joining a thread unprompted?
alex: yes to the screenshot. can we use a real design-partner thread though, or mock one? mocks always look too clean
frida: real thread is doable! I'd need to ask the partner first though. one of them has a good one where the agent chimed in on a deploy question 👀
```

> **>>> DECIDE AFTER THIS:** frida: real thread is doable! I'd need to ask the partner first though. one of them has a good one where the agent chimed in on a deploy question 👀

**Team facts again**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

---

## Row 46

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
lucia: Pulled IB port counters overnight. One leaf uplink is showing creeping symbol errors, still below the alarm line. Keeping an eye on it.
```

> **>>> DECIDE AFTER THIS:** lucia: Pulled IB port counters overnight. One leaf uplink is showing creeping symbol errors, still below the alarm line. Keeping an eye on it.

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

---

## Row 47

**Today: Mon Sep 14** · #launch

**Team facts as of now**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Sep 14 · #launch ---
olavo: good q for oli/aj. on my side, plan is waitlist email Wed night so it lands early, launch post goes live Sep 17 with the press kit, partner heads-up Tuesday. screenshots depend on the onboarding flow tho 👀
alex: For screenshots, should I grab them from a fresh workspace so the add-agents step shows? Or use a beta one that already has agents in the list?
sara: Make it Sep 24, not the 17th. Thursday lands with the Series A announcement.
olavo: oh nice, pairing it with the funding news is way better press-wise 🙌 I'll need to rejig the email and partner heads-up timing around that
alex: so with the shift, can I hold screenshots until the onboarding flow is settled? Otherwise I'd just redo them 😅
oli: Holding screenshots makes sense. Onboarding flow still has a couple open tickets on my side, so no point shooting until they settle.
frida: Updating the partner calendar now: public launch is Sep 24, so I'll move the beta partner notes off the 17th. Will hold the heads-up wording until Olavo has the new timing 👍
aj: Looked at the older beta workspaces. A few have the agent role seeded but no agent members attached, so their member list will look empty even if agents exist.
frida: @aj for those older beta workspaces, can admins just attach agents themselves, or does someone need to fix it on our end? Partners will ask 🤔
aj: Admins should be able to attach them from member settings, I think. Need to confirm the seeded role doesn't block it on those older ones.
olavo: ok so with the new timing I'm redoing the email schedule tonight. will post a fresh send plan here once it's drafted 📝
oli: fyi the two open onboarding tickets are both around the add-agents step, one's a flaky state on the skip button. will ping when it's stable.
alex: if the skip button is flaky, should the add-agents step stay skippable at all? Might be cleaner to make it required for admins, just thinking out loud
olavo: catching up, can the waitlist email still go out the day before Sep 17 like we planned? want to lock the send slot 📬
frida: another partner question: can admins mute agents per channel? They're nervous about agents jumping into threads untagged 🤔
```

> **>>> DECIDE AFTER THIS:** frida: another partner question: can admins mute agents per channel? They're nervous about agents jumping into threads untagged 🤔

**Team facts again**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

---

## Row 48

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
felix: If the removals are mostly web-app forks, I can list the upstream repos that triggered them in the release notes. Might be useful for an appendix footnote too.
theo: Can you drop the removed item ids somewhere I can load them? The notebook filters by id, so the tables will just regenerate.
nadia: Side note while we're regenerating tables: we'll decide whether the 3-shot results go in the paper at the Tue Oct 20 paper sync. Theo, export them too so we have both options ready.
marcus: Putting the removed ids in the shared data folder as a flat file, one per line, with the upstream repo that flagged each.
yuki: Recorded runs works for me. We could replay a few agent traces on a projector and talk through them, honestly more useful than live.
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
```

> **>>> DECIDE AFTER THIS:** yuki: Sounds good. I'll send you the lake house contact so you can ask about projector and screen setup before we lock it in.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,140 items (changed Mon Oct 19; previously 1,200 items)
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)
- open item: Nadia to decide whether the 3-shot results go in the paper (check point: Tue Oct 20 paper sync)

---

## Row 49

**Today: Thu Oct 8** · #acct-northwind-eng

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Thu Oct 8 · #acct-northwind-eng ---
gabe: Pulled Northwind's usage logs from the last few weeks. Traffic is spiky around their morning clinic intake, lots of 429s in that window.
keiko: That tracks with what their ops lead told me on the call. Intake staff complained the assistant stalls right when the clinics open.
gabe: Looks like they fire a burst of parallel requests at open with no backoff. Retries just pile on and make the 429s worse.
keiko: Quick check before I reply to their ops lead: is Northwind's rate limit 40M tokens per minute? React 👍 if so.
gabe: Did you see the postmortem another enterprise customer posted? Their retry storm took down their own gateway for hours.
(gabe reacted 👍 to keiko's message)
keiko: Thanks. So it's burst shape, not capacity. Gabe, can you share a backoff-with-jitter example I can send their ops lead?
gabe: Yep, I'll pull a Python snippet with exponential backoff and full jitter. Also worth suggesting they stagger the opening burst with a small queue.
keiko: Their ops lead also asked if the intake assistant can use a lighter model for the simple form-filling steps. Worth a look?
```

> **>>> DECIDE AFTER THIS:** keiko: Their ops lead also asked if the intake assistant can use a lighter model for the simple form-filling steps. Worth a look?

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

---

## Row 50

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
tomas: I'd keep the current plan, Keiko. Going back on the discount now would hurt our position, and we don't yet know what the new CTO wants. Let's learn his priorities first.
gabe: Agree with holding the line. If it helps, I can offer their platform lead a quick architecture walkthrough for the new CTO. Technical intros land easier than sales ones.
keiko: Walkthrough would help. Their platform lead mentioned the new CTO is big on clinical safety, so I'd frame it around that.
keiko: Perfect. I'll nudge their admin again tomorrow morning so we're not waiting on her too long.
```

> **>>> DECIDE AFTER THIS:** keiko: Perfect. I'll nudge their admin again tomorrow morning so we're not waiting on her too long.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

---

## Row 51

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
ines: For the changelog spreadsheet, I'll draft the confidentiality note for the first tab. Entries should be pasted straight from the addendum wording.
keiko: Their security lead also wants the spreadsheet tabs sorted by vendor name. I'll confirm the column layout with her before we build it.
```

> **>>> DECIDE AFTER THIS:** keiko: Their security lead also wants the spreadsheet tabs sorted by vendor name. I'll confirm the column layout with her before we build it.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

---

## Row 52

**Today: Wed Oct 7** · #harbor-evals

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Marcus to finish the license review for the scraped repositories (check point: Fri Oct 9)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Wed Oct 7 · #harbor-evals ---
theo: Kicked off the seed reruns on the current baseline. Early plots look tight on the single-file bug-fix items, so we'll see how much the multi-file ones spread it.
theo: were the pending jobs the ones with the multi-node affinity flag? I saw that hang last week, scheduler seemed to wait on a placement it couldn't satisfy
yuki: For the paper, I'd report the bug-fix slice separately with confidence intervals. Single-file and multi-file items probably deserve their own breakdown too.
elena: Checked timeouts. The multi-file repos need a longer setup window for dependency installs, otherwise some items will fail before the tests even start.
felix: Longer install window should go in the harness config and the release notes, since it changes what a timeout failure means for those items.
elena: yeah, most of them had it. checking if the affinity label is even getting parsed, might be silently falling back to a placement that never resolves
theo: Plots so far: the multi-file items fail mostly on import errors, not logic. Might be the same install issue Elena hit, so I'll separate those out.
felix: Side note for the release notes: harbor-lite, the internal smoke set, has 200 items. Separate from the held-out set, so I'll keep the two clearly distinguished in the manifest.
yuki: If the import-error failures are really install issues, I'd exclude them from the bug-fix slice analysis or at least report them as a separate failure category. Otherwise we're measuring the environment, not the model.
theo: if it's falling back silently, try a dry-run submit with the flag and compare the resolved placement spec against a job that schedules fine
theo: Agreed. I'll split import errors into their own bucket in the plots and rerun once Elena's longer install window is in.
elena: Also thinking of prebuilding a cached dependency image per repo, so installs don't eat the timeout budget. I'll try it on the messiest multi-file ones first.
elena: good call, running the dry-run now. the resolved spec for the stuck ones has an empty topology field, the working job has it populated
nadia: Cached images are a good idea. Worth a sentence in the paper's methods section so reviewers know installs aren't counted against the model.
marcus: Cached images also help the contamination check. I can diff the pinned dependency versions against the repos' original commit dates and catch anything that predates the snapshots.
```

> **>>> DECIDE AFTER THIS:** marcus: Cached images also help the contamination check. I can diff the pinned dependency versions against the repos' original commit dates and catch anything that predates the snapshots.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Marcus to finish the license review for the scraped repositories (check point: Fri Oct 9)

---

## Row 53

**Today: Wed Oct 7** · #harbor-evals

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items

**Recent messages** (oldest first; the last one is the decision message)

```
--- Wed Oct 7 · #harbor-evals ---
yuki: If the import-error failures are really install issues, I'd exclude them from the bug-fix slice analysis or at least report them as a separate failure category. Otherwise we're measuring the environment, not the model.
theo: if it's falling back silently, try a dry-run submit with the flag and compare the resolved placement spec against a job that schedules fine
theo: Agreed. I'll split import errors into their own bucket in the plots and rerun once Elena's longer install window is in.
elena: Also thinking of prebuilding a cached dependency image per repo, so installs don't eat the timeout budget. I'll try it on the messiest multi-file ones first.
elena: good call, running the dry-run now. the resolved spec for the stuck ones has an empty topology field, the working job has it populated
nadia: Cached images are a good idea. Worth a sentence in the paper's methods section so reviewers know installs aren't counted against the model.
marcus: Cached images also help the contamination check. I can diff the pinned dependency versions against the repos' original commit dates and catch anything that predates the snapshots.
theo: empty topology would explain it. Does the parser drop the label when the node pool name has a hyphen? I hit that once on my branch.
yuki: Good, but dependency pinning only catches so much. Might also be worth checking whether any fix commits are quoted verbatim in public issue threads, since that leaks the answer too.
marcus: Good point on issue threads. I can grep the public trackers for long verbatim diff snippets and flag any items where the fix text shows up before the snapshot.
theo: If the issue-thread grep flags items, I can rerun those separately and see whether baseline scores on them look inflated compared to the clean ones.
yuki: If flagged items do inflate baseline scores, that's a nice contamination figure for the paper. Inflated-vs-clean gap, plotted per slice, with intervals.
marcus: License review for the scraped repos is done. Three repos got excluded over license terms, so I'll update the backfill list and send Felix the cleaned source/license tags for the manifest.
elena: First cached image is built for the messiest monorepo item. Installs barely register now. Trying the Python repos with native extensions next.
theo: Split the import-error bucket out of the multi-file plots. Spread tightens a lot without it. Will rerun properly once more cached images land.
```

> **>>> DECIDE AFTER THIS:** theo: Split the import-error bucket out of the multi-file plots. Spread tightens a lot without it. Will rerun properly once more cached images land.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items

---

## Row 54

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
theo: I'll put the censored-dot marker in the plot legend too, so the caption doesn't have to carry all of it.
```

> **>>> DECIDE AFTER THIS:** theo: I'll put the censored-dot marker in the plot legend too, so the caption doesn't have to carry all of it.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,140 items (changed Mon Oct 19; previously 1,200 items)
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 55

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
lucia: Firmware rollout on the IB leaf switches is staged but not pushed. Seeing a few flapping links on rack group C that I want to look at first.
kofi: Are the flapping links on C causing NCCL timeouts yet? Want to know if checkpoint writes from those nodes are getting stalled mid-save.
hana: Quick check while we're on checkpoints: kestrel checkpoint cadence is every 500 steps, right? React ✅ if that's what you have.
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
```

> **>>> DECIDE AFTER THIS:** kofi: Yes, checksum on load makes sense. I'll write per-shard hashes at flush time and verify on resume, so a bad shard fails loudly instead of loading.

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 56

**Today: Tue Sep 8** · #launch

**Team facts as of now**

- public launch (date): Sep 17
- Series A raise (amount): $20M

**Recent messages** (oldest first; the last one is the decision message)

```
--- Tue Sep 8 · #launch ---
sara: ok team, launch kickoff. I'm going to lock the date, the raise announcement, pricing and who owns what for launch week. Read along, shout if something's off.
alex: reading along 👀 quick q: are we showing the agent-as-member idea in the onboarding flow at launch, or keeping that for after?
frida: +1 to Alex's q. Two design partners got lost on day one because they didn't realize the agent shows up in the member list.
oli: Agent already has its own member entry in the runtime, so showing it in onboarding is just a UI change. No backend work needed.
alex: nice, then I can mock it as a pinned card in the welcome step. should the agent introduce itself there or stay quiet until tagged?
sara: Locking the date first: public launch is Sep 17. Alex, agent introduces itself in the welcome card, yes. Keep it short, one line.
alex: perfect, one line it is. I'll draft a couple of intro variants and drop them here for a vibe check 🙌
frida: Happy to test the intro variants with a couple of design partners too, they'll give honest reactions 😄
olavo: quick check for the launch post draft: Series A raise is $20M, right? react 👍 if so and I'll lock it in
(sara reacted 👍 to olavo's message)
oli: fyi the member list currently sorts agents below humans alphabetically. might want to pin the agent higher for new workspaces, ticket coming
```

> **>>> DECIDE AFTER THIS:** oli: fyi the member list currently sorts agents below humans alphabetically. might want to pin the agent higher for new workspaces, ticket coming

**Team facts again**

- public launch (date): Sep 17
- Series A raise (amount): $20M

---

## Row 57

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
theo: Mine's the results table. Two of the baseline rows still have old numbers in them, so I need to refresh those before anyone quotes the table.
yuki: Open on my side: the pass criteria paragraph in the methods section still reads ambiguously. Want to tighten the wording before anyone cites it.
marcus: Mine's the contamination writeup. Need to reword how we describe the overlap check so reviewers don't read it as stronger than it is.
felix: Mine's the release checklist. Changelog is drafted but I still need to go through the tagging steps and double-check the package notes match the paper.
nadia: Thanks all. Theo, can you flag which two baseline rows are stale so Yuki and Marcus know what not to quote yet?
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
```

> **>>> DECIDE AFTER THIS:** theo: Error bars will be bootstrap over tasks. We only ran a few seeds per model, so seed variance would be too noisy to show.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,140 items (changed Mon Oct 19; previously 1,200 items)
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 58

**Today: Mon Sep 28** · #kestrel-run

**Team facts as of now**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Sep 28 · #kestrel-run ---
dmitri: Kickoff thread for kestrel. Need start date, allocation, stability rules and data readiness all pinned down in here today. Who has blockers?
lucia: Fabric blocker from my side: two leaf switches in the new pod still flap under heavy all-reduce. Haven't isolated whether it's optics or firmware.
wen: Do those flapping leaf switches sit in the pod I was planning to hand kestrel? If so I need to rework the allocation table.
lucia: Yes, same pod. Both flapping leafs feed racks in that pod. Seeing CRC errors on the uplinks, so I'm leaning optics, but not confirmed.
dmitri: Decision: kestrel starts Oct 5. Lucia, get the optics vs firmware call made and fixed well before then. Wen, redo the allocation table around whatever the pod looks like once that's resolved.
lucia: Pulling optic transceiver serials on the flapping uplinks now. If they share a batch, that settles it. Will swap one and rerun all-reduce soak.
wen: Whichever way the optics call goes, I'll draft two allocation variants: one with the flapping racks drained, one assuming they come back clean.
dmitri: Quick check Wen: is the kestrel node allocation 2,048 nodes? Want that confirmed before the variants go out.
wen: yep, confirmed
kofi: If the flapping racks get drained, I need to know before I size checkpoint shards. Fewer nodes changes the per-rank write pattern to storage.
```

> **>>> DECIDE AFTER THIS:** kofi: If the flapping racks get drained, I need to know before I size checkpoint shards. Fewer nodes changes the per-rank write pattern to storage.

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes

---

## Row 59

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
ines: For the changelog spreadsheet, I'll draft the confidentiality note for the first tab. Entries should be pasted straight from the addendum wording.
```

> **>>> DECIDE AFTER THIS:** ines: For the changelog spreadsheet, I'll draft the confidentiality note for the first tab. Entries should be pasted straight from the addendum wording.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

---

## Row 60

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

> **>>> DECIDE AFTER THIS:** keiko: Their procurement lead also wants a usage breakdown by clinical department in the QBR. Gabe, can we pull that from the dashboards?

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

---

## Row 61

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
```

> **>>> DECIDE AFTER THIS:** frida: one of our design partners asked if billing invoices can go to their finance person instead of the workspace owner. Anyone know?

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

## Row 62

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
```

> **>>> DECIDE AFTER THIS:** olavo: "Joins" reads calmer to me, "chimes in" sounds like butting in. Maybe a line in the FAQ about muting an agent per channel?

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

## Row 63

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
felix: Anyone have strong feelings on the offsite venue? I'm leaning toward the lake house over the downtown coworking space. Yuki, you looked at both, right?
nadia: Thinking the appendix should carry the per-category breakdowns and a couple of full agent transcripts. Too heavy for a workshop paper?
theo: Per-category tables are easy, I can export them straight from the results notebook. Full transcripts are the heavy part, some run absurdly long. Maybe trim to the interesting steps?
yuki: Yeah, I toured both. Lake house has way better space for whiteboarding, but the drive is long and wifi there was spotty.
yuki: Trimming is fine, but I'd keep one full transcript from the plateau tasks untouched. Readers will want to see the agent looping, not a cleaned-up version.
felix: Spotty wifi could hurt if we want to demo anything live. Did the lake house have a wired port anywhere, or would we tether?
```

> **>>> DECIDE AFTER THIS:** felix: Spotty wifi could hurt if we want to demo anything live. Did the lake house have a wired port anywhere, or would we tether?

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 64

**Today: Thu Sep 10** · #eng

**Team facts as of now**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

**Recent messages** (oldest first; the last one is the decision message)

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
```

> **>>> DECIDE AFTER THIS:** oli: Who can take AND-341 (agent double-posts in threads)? Needs an owner before standup.

**Team facts again**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

---

## Row 65

**Today: Mon Sep 28** · #kestrel-run

**Team facts as of now**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Sep 28 · #kestrel-run ---
dmitri: Kickoff thread for kestrel. Need start date, allocation, stability rules and data readiness all pinned down in here today. Who has blockers?
lucia: Fabric blocker from my side: two leaf switches in the new pod still flap under heavy all-reduce. Haven't isolated whether it's optics or firmware.
wen: Do those flapping leaf switches sit in the pod I was planning to hand kestrel? If so I need to rework the allocation table.
lucia: Yes, same pod. Both flapping leafs feed racks in that pod. Seeing CRC errors on the uplinks, so I'm leaning optics, but not confirmed.
dmitri: Decision: kestrel starts Oct 5. Lucia, get the optics vs firmware call made and fixed well before then. Wen, redo the allocation table around whatever the pod looks like once that's resolved.
lucia: Pulling optic transceiver serials on the flapping uplinks now. If they share a batch, that settles it. Will swap one and rerun all-reduce soak.
wen: Whichever way the optics call goes, I'll draft two allocation variants: one with the flapping racks drained, one assuming they come back clean.
dmitri: Quick check Wen: is the kestrel node allocation 2,048 nodes? Want that confirmed before the variants go out.
wen: yep, confirmed
kofi: If the flapping racks get drained, I need to know before I size checkpoint shards. Fewer nodes changes the per-rank write pattern to storage.
mateo: Data side is looking fine so far. Tokenized shards are landing on the new filesystem, just waiting on the last dedup pass to finish.
hana: Whichever variant wins, I want straggler detection on from step zero. Flapping links would show up as a few slow ranks dragging MFU down.
hana: Stability rule for the run: roll back if loss rises more than 15%. I'll wire that into the monitor alongside the straggler alerts.
```

> **>>> DECIDE AFTER THIS:** hana: Stability rule for the run: roll back if loss rises more than 15%. I'll wire that into the monitor alongside the straggler alerts.

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes

---

## Row 66

**Today: Tue Oct 6** · #acct-northwind

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Tue Oct 6 · #acct-northwind ---
ines: Thanks, Rachel. Once tagged, I'll compare their old language against our current standard terms and see where we can realistically give ground.
gabe: Peak-hour breakdown is coming together. Two of the pilot teams look like the main bursters, so I'll flag those for Tomas separately.
keiko: Heads up, their informatics lead said the pilot clinicians love the summarization features. Could be a good angle for the expansion conversation.
rachel: Good angle. Keiko, can you get a customer quote on the summarization wins in their own words? Would help anchor the expansion pitch.
keiko: On it. One of the pilot nurse managers gave a great line on the summarization wins last week, so I'll ask if we can use it.
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
```

> **>>> DECIDE AFTER THIS:** gabe: Sure, Darnell. I'll write the exec summary around adoption and the burst patterns, keep the technical detail light.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

---

## Row 67

**Today: Thu Sep 10** · #eng

**Team facts as of now**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Thu Sep 10 · #eng ---
alex: Haha perfect. Should I mock up the snack thread in the sandbox so the agent's reply looks natural on screen? I can draft it.
olavo: For the launch post, can I show agents joining a thread on their own? Want a clean gif, no double bubbles obviously 😅
oli: Olavo: thread-join gif is fine as long as only one agent is in the channel. Use a single-agent demo workspace.
frida: Yes please! Draft it and I'll run it past a couple of partners to see if the snack banter feels real 😊
alex: Okay so for the single-agent demo workspace, should I mock up the onboarding screens with just one agent in the sidebar? Easier to screenshot.
olavo: Yes please Alex, one agent in the sidebar works for me too. I'll grab screenshots from it for the press kit as well.
aj: Oli, pulled up the sim harness. It fakes channel traffic fine, but I'll need to tweak it so agents hit shared memory entries, not just channels.
oli: Makes sense. Have them hit a small set of hot entries plus a wide spread, so we see both contention and the normal case.
frida: Heard back from the partner: their agents mostly hit the same couple of standup channels during the rush. Sounds like hot entries to me.
aj: That fits the hot-entry case then. I'll weight the sim toward a few shared entries and log p95 read latency per run.
alex: Different thing, for the onboarding copy: if someone @-mentions an agent inside a DM, can that agent read the DM? Or is it blocked unless the agent is a member of it?
oli: aj, log write latency too, not just reads. Standup rush probably has agents saving summaries to memory at the same moment.
aj: Will do, write latency goes in the same log. I'll also tag each run with how many agents were active.
frida: I'll also ask that partner whether their standup agents all save summaries at the same moment. Useful for the write-latency runs.
alex: Still need an answer on my DM @-mention question, whoever knows it best. The onboarding copy depends on it 🙏
```

> **>>> DECIDE AFTER THIS:** alex: Still need an answer on my DM @-mention question, whoever knows it best. The onboarding copy depends on it 🙏

**Team facts again**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

---

## Row 68

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
lucia: Affected ports are on the C leaf, the two uplinks I reseated and recabled. I'll post exact port IDs once counters settle.
mateo: yeah the app has a pickup time picker, I'll set it for when your call wraps. want the usual or something different?
hana: I'll add a monitor on resume that logs hash mismatch counts per rank, so a tripped check shows up on the dashboard and not just in logs.
kofi: Per-rank mismatch counts on the dashboard works for me. I'll emit the hash result as a structured log line so your monitor can scrape it.
lucia: the usual works. the spicy one with extra greens. my call wraps around the half hour, probably runs over though, IB flap again
mateo: Loader side I'll tag reads from C nodes in the metrics so stalls show up per node, not just aggregate throughput.
lucia: Cable swap on the second uplink done. Retrain count on that port is flat so far, watching optics levels on the C leaf.
mateo: ha, IB flap again. I'll pad the pickup a bit so it doesn't sit. I'll grab it and drop it at your desk.
kofi: Patch is up for review. Injected short write on a writer rank now retries instead of flipping the shard to complete. Hash lines look right in the structured log.
hana: I'll review the patch. Want to confirm the retry path doesn't stall the writer rank and skew step time during saves.
kofi: Retry runs on the flush thread, so the training step shouldn't block. I'll capture step time during the injected short write and attach it to the review.
lucia: Optics levels on the C leaf look stable so far. Still no clean window to say firmware's safe, so it stays parked.
hana: For storage sizing I'm assuming a checkpoint every 1,000 steps. Mateo, can you confirm the tier has headroom for that plus the per-shard hash sidecars?
lucia: Who should C leaf flap alerts page while firmware is parked? Right now they land in my queue only, nobody else.
wen: Whoever gets those pages should be able to trigger a drain of C nodes, otherwise it's just noise at 3am. I can be in the loop.
```

> **>>> DECIDE AFTER THIS:** wen: Whoever gets those pages should be able to trigger a drain of C nodes, otherwise it's just noise at 3am. I can be in the loop.

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 69

**Today: Wed Sep 30** · #infra

**Team facts as of now**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Wed Sep 30 · #infra ---
lucia: Firmware rollout on the IB leaf switches is staged but not pushed. Seeing a few flapping links on rack group C that I want to look at first.
kofi: Are the flapping links on C causing NCCL timeouts yet? Want to know if checkpoint writes from those nodes are getting stalled mid-save.
hana: Quick check while we're on checkpoints: kestrel checkpoint cadence is every 500 steps, right? React ✅ if that's what you have.
(kofi reacted ✅ to hana's message)
lucia: Not seeing NCCL timeouts yet, just symbol errors and retrains on a couple of C uplinks. Checking cable seating before touching firmware.
```

> **>>> DECIDE AFTER THIS:** lucia: Not seeing NCCL timeouts yet, just symbol errors and retrains on a couple of C uplinks. Checking cable seating before touching firmware.

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 70

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
hana: Tokenizer question again: the 100k vocab run shows noisier loss on code-heavy shards in the small-scale ablation. Anyone looked at the per-domain curves?
```

> **>>> DECIDE AFTER THIS:** hana: Tokenizer question again: the 100k vocab run shows noisier loss on code-heavy shards in the small-scale ablation. Anyone looked at the per-domain curves?

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 71

**Today: Mon Sep 14** · #launch

**Team facts as of now**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Sep 14 · #launch ---
olavo: catching up, can the waitlist email still go out the day before Sep 17 like we planned? want to lock the send slot 📬
frida: another partner question: can admins mute agents per channel? They're nervous about agents jumping into threads untagged 🤔
aj: Per-channel mute isn't something I can confirm yet. Need to check whether agent permissions are scoped per channel or only per workspace.
oli: repro for the skip button: go back from the next step and the state resets, so skip shows enabled when it shouldn't. Tracing it.
alex: does the reset also hit people who go back after already adding an agent? Might show an empty list again 🤔
alex: quick q, who actually sends the waitlist email? I need to know who to give the header image to 📬
olavo: me! send the header image my way, I'm sending the waitlist email 📬
alex: Sending the header image over now. I made a dark and a light version, so pick whichever fits the email template 🎨
frida: Another partner asked if there's a visible indicator when an agent joins a thread untagged. Would calm the nerves a bit 🙂
alex: Could be a small badge or avatar ring on the message when an agent joins untagged. I can mock a couple options 🎨
aj: Update: the forwarded-DM permission check is merged. Forwarding a DM into a channel now checks the original DM's access first. That one's done.
oli: @alex yes, going back after adding an agent also resets the list view. Same root cause, so the fix should cover both. Testing it now.
frida: One more partner question: can admins see what an agent has stored in shared memory? They want to check it's not holding anything odd 🤔
aj: Memory entries are stored per workspace, but I'm not sure there's an admin-facing view yet. Checking what the store exposes before I say anything to partners.
olavo: for the press kit, can someone send me a clean screenshot of an agent replying in a thread? Current one has test data in it 😅
```

> **>>> DECIDE AFTER THIS:** olavo: for the press kit, can someone send me a clean screenshot of an agent replying in a thread? Current one has test data in it 😅

**Team facts again**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

---

## Row 72

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
alex: Back to FAQ wording. When an agent jumps into a thread untagged, do we say "joins" or "chimes in"? Partners might read that as intrusive.
olavo: "Joins" reads calmer to me, "chimes in" sounds like butting in. Maybe a line in the FAQ about muting an agent per channel?
alex: Good idea on muting. Should it be per channel only, or can someone mute an agent in just one thread too? Partners will ask.
aj: Per channel is easy since mute is a membership-level flag. Per thread means a new subscription state to track, and search needs to respect it too.
frida: One partner mentioned wanting an agent quiet in one noisy thread but still active in the channel. So per-thread might come up.
frida: Unrelated, heads up: I need to leave early Thursday for a family thing. Can someone cover partner questions in the afternoon? Happy to leave notes on who's waiting on what.
oli: I can take partner questions Thursday afternoon, but only the technical ones. Frida, put billing stuff in your notes separately.
alex: Thanks Oli. Frida, could you also jot down which partners asked about per-thread muting? I'd like to quote them in the FAQ review.
frida: Yep, will do. Two of them mentioned it so far, I'll add names and what they said to my notes doc.
olavo: For the waitlist email, should I mention agents can be muted? Feels like a good trust line, but don't want to overpromise on per-thread.
alex: Quick question on muting: does a muted agent still read the channel for memory, or fully stop? Partners will ask.
aj: Mute as built only silences posting and notifications. Memory indexing still runs on the channel. A true stop-reading option would be a separate flag.
alex: Random q while we're on the waitlist email: who's actually sending it Thursday? Olavo, is that you, or does Sara hit send?
frida: Another partner question: if they remove an agent from the workspace, does its shared memory get wiped or stay searchable?
aj: Frida, on removal: I'd need to check how memory is keyed. If it's tied to the agent identity, deleting the agent could orphan entries.
```

> **>>> DECIDE AFTER THIS:** aj: Frida, on removal: I'd need to check how memory is keyed. If it's tied to the agent identity, deleting the agent could orphan entries.

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

## Row 73

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
keiko: Security lead replied on the sub-processor question: they want the addendum version, and they'd like a changelog of recent additions too.
```

> **>>> DECIDE AFTER THIS:** keiko: Security lead replied on the sub-processor question: they want the addendum version, and they'd like a changelog of recent additions too.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

---

## Row 74

**Today: Tue Sep 8** · #launch

**Team facts as of now**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered

**Recent messages** (oldest first; the last one is the decision message)

```
--- Tue Sep 8 · #launch ---
olavo: quick check for the launch post draft: Series A raise is $20M, right? react 👍 if so and I'll lock it in
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
```

> **>>> DECIDE AFTER THIS:** frida: One design partner asked if they can mute the agent in a single channel without removing it. Worth a line in the FAQ?

**Team facts again**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered

---

## Row 75

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
--- Mon Oct 12 · #kestrel-run ---
mateo: Unrelated to the flush, but I'm seeing IB link flaps on a couple of the dataloader nodes in my logs. Who's on call for fabric incidents today?
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
```

> **>>> DECIDE AFTER THIS:** mateo: Drain's progressing. Prefetch queue depth on the remaining loaders is climbing a bit but still has headroom, no stalls on the consumer side.

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps (changed Fri Oct 9; previously every 500 steps)
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

---

## Row 76

**Today: Thu Oct 8** · #acct-northwind-eng

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Thu Oct 8 · #acct-northwind-eng ---
gabe: Pulled Northwind's usage logs from the last few weeks. Traffic is spiky around their morning clinic intake, lots of 429s in that window.
```

> **>>> DECIDE AFTER THIS:** gabe: Pulled Northwind's usage logs from the last few weeks. Traffic is spiky around their morning clinic intake, lots of 429s in that window.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

---

## Row 77

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
olavo: morning all! launch post draft v2 is up in the doc, would love eyes on the intro paragraph. also pricing page copy still needs a pass, I'll start on that after lunch 🚀
alex: read the intro, I like it. quick q: are we explaining what an agent as a workspace member means before the pricing section, or assuming people get it?
olavo: good q alex. I was thinking a short explainer box right above pricing, maybe with a screenshot of an agent joining a thread unprompted?
alex: yes to the screenshot. can we use a real design-partner thread though, or mock one? mocks always look too clean
frida: real thread is doable! I'd need to ask the partner first though. one of them has a good one where the agent chimed in on a deploy question 👀
sara: Going with Alex's pricing suggestion from Monday. Acting on it now, Olavo update the page copy to match.
olavo: on it 🙌 quick check while I edit: should agent seats get their own line on the page, or fold into one?
frida: fwiw two design partners asked if agents count toward their seat total, so a separate line might save us support questions 🙏
```

> **>>> DECIDE AFTER THIS:** frida: fwiw two design partners asked if agents count toward their seat total, so a separate line might save us support questions 🙏

**Team facts again**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per human seat, agents free (changed Wed Sep 16; previously $12 per seat, agent actions metered)
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

---

## Row 78

**Today: Wed Sep 30** · #infra

**Team facts as of now**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Wed Sep 30 · #infra ---
lucia: Firmware rollout on the IB leaf switches is staged but not pushed. Seeing a few flapping links on rack group C that I want to look at first.
kofi: Are the flapping links on C causing NCCL timeouts yet? Want to know if checkpoint writes from those nodes are getting stalled mid-save.
hana: Quick check while we're on checkpoints: kestrel checkpoint cadence is every 500 steps, right? React ✅ if that's what you have.
(kofi reacted ✅ to hana's message)
lucia: Not seeing NCCL timeouts yet, just symbol errors and retrains on a couple of C uplinks. Checking cable seating before touching firmware.
kofi: Good. If those C uplinks retrain mid-save, I'd expect partial shards on the writer ranks. I'll check how the async flush handles a stalled write.
wen: Who's owning fabric incident on-call for kestrel right now? I need a name on the rota before I lock the allocation table.
```

> **>>> DECIDE AFTER THIS:** wen: Who's owning fabric incident on-call for kestrel right now? I need a name on the rota before I lock the allocation table.

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 79

**Today: Mon Sep 28** · #kestrel-run

**Team facts as of now**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Sep 28 · #kestrel-run ---
dmitri: Mateo, your loader sizing doesn't match the allocation Wen confirmed. Redo it against the confirmed number.
mateo: Fair, my bad. Redoing the loader sizing against Wen's number. Prefetch worker count per node will probably shift too, rechecking read throughput after.
kofi: Restore path is my next test. Will kill a rank mid-flush and confirm we resume cleanly from the staged NVMe copy.
mateo: Once dedup lands, I'll finish moving the tokenized datasets to the new storage tier by Fri Oct 2. That leaves a few days of buffer before the start.
hana: Lucia, can you send me the port-to-rank mapping for the flapping uplinks? I want straggler alerts to tag those ranks directly.
lucia: Yep, mapping coming. Both ports sit on the same leaf switch, so it's a handful of ranks per node. Exporting from the switch config now.
hana: Thanks. Once I have it I'll also add per-rank NCCL timing to the dashboard, so a slow allreduce on those ranks is visible right away.
kofi: Lucia, when the other uplink gets swapped, give me a heads-up. If those racks drop mid-soak I want to see how the staging path handles a rank vanishing.
lucia: Will do. Swapping the second optic after the current soak window closes, so CRC counters on the first port stay a clean baseline.
lucia: Heads up, the cluster room is louder than a jet engine today. Swapping optics in there with earplugs in, so slow to reply if I miss pings.
kofi: Once the mapping lands I'll also check whether those ranks end up in the same NCCL ring segment. A flaky one could stall the whole ring.
wen: If the ring segment does include those ranks, I can reshuffle placement so they land on a different leaf. Cheap on my side.
hana: Mapping would also let me flag whether those ranks show up as stragglers in the last burn-in logs. Pulling those now to compare.
dmitri: If those ranks show up as stragglers in burn-in, I want that in the writeup before we lock the placement.
wen: Pulling the current placement map now so I can see which leaf those ranks sit on and what's free to swap into.
```

> **>>> DECIDE AFTER THIS:** wen: Pulling the current placement map now so I can see which leaf those ranks sit on and what's free to swap into.

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 80

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
gabe: Dashboards split usage by project and API key, not department. If their clinical teams use separate keys, I can map it. Otherwise we'd need to check how they tag requests.
```

> **>>> DECIDE AFTER THIS:** gabe: Dashboards split usage by project and API key, not department. If their clinical teams use separate keys, I can map it. Otherwise we'd need to check how they tag requests.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

---

## Row 81

**Today: Mon Sep 14** · #launch

**Team facts as of now**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Tue Sep 8 · #launch ---
olavo: random but for launch day, how many pizzas do we order for 7 people? asking for a friend (the friend is me) 🍕😂
frida: Another design partner asked if the agent's replies trigger the same mobile notifications as human messages. Might need a FAQ line on that too 📱
oli: Agent replies go through the same push path as human messages today. A separate setting would be its own ticket, I can scope it.
olavo: For the launch post I'd love a screenshot of the agent jumping into a thread unprompted. Alex, could you mock one up? 📸
alex: Sure, I can mock the unprompted thread jump. Should the agent's message look different from a human reply, like a small badge, or keep it identical?
frida: My design partners liked having an "agent" label in the member list, so a small badge on messages might feel consistent 🙂
alex: Badge makes sense. I'll try a tiny "agent" tag next to the name, nothing loud, so long threads don't get noisy 🏷️
alex: Planning design freeze around the Sep 18 launch, so mocks for the pricing page, badge and thread-jump screenshot all land before then 🎨
olavo: Also for the launch post, we should probably have a short demo gif of the shared memory bit. People love seeing that 🎬
oli: For the memory gif, I can set up a clean demo workspace with seeded convos so it records without weird leftovers 🎬
frida: Nice, a clean demo workspace would help. A couple of design partners offered to share a quote or two for the launch post if useful 🙌
olavo: Love that, quotes from real teams will make the post. Can someone ask which partners are okay being named? Logos would be great too 🙌
--- Mon Sep 14 · #launch ---
olavo: morning all! weekend recap: launch post draft is at v3, waitlist email copy is mostly done, press kit needs final screenshots. waitlist is up a bunch since Friday too 🚀 want to lock send timing for the week today
frida: quick q from a design partner: do agents show up in their workspace member list by default, or do admins need to add them first?
alex: wait, are we sure about the default there? I think onboarding currently has an "add agents" step, but I'd have to check the latest flow. @oli @aj?
```

> **>>> DECIDE AFTER THIS:** alex: wait, are we sure about the default there? I think onboarding currently has an "add agents" step, but I'd have to check the latest flow. @oli @aj?

**Team facts again**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

---

## Row 82

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
keiko: Security lead replied on the sub-processor question: they want the addendum version, and they'd like a changelog of recent additions too.
ines: The changelog is fine in principle. I want to check how the addendum handles notice of new sub-processors before it goes in their packet.
```

> **>>> DECIDE AFTER THIS:** ines: The changelog is fine in principle. I want to check how the addendum handles notice of new sub-processors before it goes in their packet.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

---

## Row 83

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
darnell: Fair point, that note was stale. I'll hold off on sending anything until we figure out an intro to the new owner.
keiko: Just thinking out loud: what if we went back to 18% to close faster? Not a proposal, only wondering if it'd help with a new CTO.
tomas: I'd keep the current plan, Keiko. Going back on the discount now would hurt our position, and we don't yet know what the new CTO wants. Let's learn his priorities first.
gabe: Agree with holding the line. If it helps, I can offer their platform lead a quick architecture walkthrough for the new CTO. Technical intros land easier than sales ones.
keiko: Walkthrough would help. Their platform lead mentioned the new CTO is big on clinical safety, so I'd frame it around that.
keiko: Perfect. I'll nudge their admin again tomorrow morning so we're not waiting on her too long.
ines: If he's focused on clinical safety, expect him to ask about logging and how model outputs get reviewed. I'd want our answers consistent across the deck and contract.
gabe: I can pull together a one-pager on how we handle output logging and what controls their team can set. Keeps the answers consistent with the deck.
rachel: Good. Keiko, when you talk to their platform lead, ask if the new CTO would take a short intro call before the QBR.
keiko: Will do. I'll also ask whether he'd like clinical safety examples from other health systems, so the call isn't just us talking at him.
darnell: Good. Once Keiko hears back, I'll look for someone on our side with a clinical safety background to join that intro.
rachel: Sounds like a plan. Keiko, flag anything the platform lead says about the new CTO's priorities so we can adjust the QBR story.
--- Mon Oct 19 · #acct-northwind ---
tomas: Morning all. Friday's finance review is done and I've updated the order form draft with their comments. Redline v4 is in the deal folder. Rachel, can you confirm you've seen it before I send to Ines?
keiko: Heads up, Northwind's security lead asked me again for the sub-processor list. They want it for their internal review packet.
ines: Which one do they mean: the public sub-processor page, or the list referenced in the addendum? They're maintained separately.
```

> **>>> DECIDE AFTER THIS:** ines: Which one do they mean: the public sub-processor page, or the list referenced in the addendum? They're maintained separately.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

---

## Row 84

**Today: Thu Oct 8** · #acct-northwind-eng

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Thu Oct 8 · #acct-northwind-eng ---
gabe: Pulled Northwind's usage logs from the last few weeks. Traffic is spiky around their morning clinic intake, lots of 429s in that window.
keiko: That tracks with what their ops lead told me on the call. Intake staff complained the assistant stalls right when the clinics open.
gabe: Looks like they fire a burst of parallel requests at open with no backoff. Retries just pile on and make the 429s worse.
keiko: Quick check before I reply to their ops lead: is Northwind's rate limit 40M tokens per minute? React 👍 if so.
gabe: Did you see the postmortem another enterprise customer posted? Their retry storm took down their own gateway for hours.
(gabe reacted 👍 to keiko's message)
keiko: Thanks. So it's burst shape, not capacity. Gabe, can you share a backoff-with-jitter example I can send their ops lead?
gabe: Yep, I'll pull a Python snippet with exponential backoff and full jitter. Also worth suggesting they stagger the opening burst with a small queue.
keiko: Their ops lead also asked if the intake assistant can use a lighter model for the simple form-filling steps. Worth a look?
gabe: Yes, likely. Form-filling is mostly structured extraction, so a smaller model should handle it. I'd want to test accuracy on their real intake forms first.
ines: Since they're sending patient intake data through this, flagging the retention side: zero data retention is approved for Northwind. Worth keeping that in mind when we test on their real forms.
rachel: Yes, saw it. Ouch. Makes me wonder if Northwind's team has backoff with jitter on their side. Worth a quick check with them?
gabe: Good point. I'll ask their ops lead for de-identified sample forms so we can compare the smaller model without touching real patient records.
ines: Also, that applies to all endpoints, batch included, so the same coverage holds if they move the form-filling there.
```

> **>>> DECIDE AFTER THIS:** ines: Also, that applies to all endpoints, batch included, so the same coverage holds if they move the form-filling there.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

---

## Row 85

**Today: Mon Sep 14** · #launch

**Team facts as of now**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Sep 14 · #launch ---
olavo: me! send the header image my way, I'm sending the waitlist email 📬
alex: Sending the header image over now. I made a dark and a light version, so pick whichever fits the email template 🎨
frida: Another partner asked if there's a visible indicator when an agent joins a thread untagged. Would calm the nerves a bit 🙂
alex: Could be a small badge or avatar ring on the message when an agent joins untagged. I can mock a couple options 🎨
aj: Update: the forwarded-DM permission check is merged. Forwarding a DM into a channel now checks the original DM's access first. That one's done.
oli: @alex yes, going back after adding an agent also resets the list view. Same root cause, so the fix should cover both. Testing it now.
frida: One more partner question: can admins see what an agent has stored in shared memory? They want to check it's not holding anything odd 🤔
aj: Memory entries are stored per workspace, but I'm not sure there's an admin-facing view yet. Checking what the store exposes before I say anything to partners.
olavo: for the press kit, can someone send me a clean screenshot of an agent replying in a thread? Current one has test data in it 😅
alex: Random pricing thought while mocking the badge: what if it's $12 per human seat and agents are free? Just an idea, nothing decided. Sara, that's your call 🤔
frida: I can grab a screenshot from our demo workspace for the press kit. Just need to make sure no partner names show 📸
oli: skip button fix is in review. once it's merged I'll rerun the onboarding flow end to end on a fresh workspace 🔧
aj: Looked at the memory store. It can list entries per workspace, so an admin view is mostly UI work. Writing it up for Frida's partners.
frida: Thanks AJ, that helps a lot. I'll hold off on replying to the partners until your writeup is ready 🙏
alex: Mocking the untagged-join badge now. I'll drop two or three options in the design channel for Frida to show partners 🎨
```

> **>>> DECIDE AFTER THIS:** alex: Mocking the untagged-join badge now. I'll drop two or three options in the design channel for Frida to show partners 🎨

**Team facts again**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

---

## Row 86

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
oli: I can take partner questions Thursday afternoon, but only the technical ones. Frida, put billing stuff in your notes separately.
alex: Thanks Oli. Frida, could you also jot down which partners asked about per-thread muting? I'd like to quote them in the FAQ review.
frida: Yep, will do. Two of them mentioned it so far, I'll add names and what they said to my notes doc.
olavo: For the waitlist email, should I mention agents can be muted? Feels like a good trust line, but don't want to overpromise on per-thread.
alex: Quick question on muting: does a muted agent still read the channel for memory, or fully stop? Partners will ask.
aj: Mute as built only silences posting and notifications. Memory indexing still runs on the channel. A true stop-reading option would be a separate flag.
alex: Random q while we're on the waitlist email: who's actually sending it Thursday? Olavo, is that you, or does Sara hit send?
frida: Another partner question: if they remove an agent from the workspace, does its shared memory get wiped or stay searchable?
aj: Frida, on removal: I'd need to check how memory is keyed. If it's tied to the agent identity, deleting the agent could orphan entries.
frida: Thanks AJ. The partner asking is swapping agents mid-project, so they'd want the old one's memory to carry over to the new one.
alex: For the swap case, would partners expect memory to carry over automatically, or a manual "transfer memory" step when they replace an agent?
aj: Automatic carry-over gets tricky. Old memory includes entries from channels the new agent was never in, so permissions would have to be re-checked.
frida: I think that partner would be fine with a manual transfer step, as long as it shows which channels' memory comes across and what gets skipped.
olavo: Draft FAQ answer for the memory question: "Agents read channel and DM history to build team memory, so they pick up context without anyone re-explaining it. You can mute an agent per channel anytime." Thoughts?
oli: Found a bug in staging: a muted agent still shows the typing indicator in the channel. Filing a ticket, ENG-412.
```

> **>>> DECIDE AFTER THIS:** oli: Found a bug in staging: a muted agent still shows the typing indicator in the channel. Filing a ticket, ENG-412.

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

## Row 87

**Today: Thu Oct 8** · #acct-northwind-eng

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Thu Oct 8 · #acct-northwind-eng ---
gabe: Pulled Northwind's usage logs from the last few weeks. Traffic is spiky around their morning clinic intake, lots of 429s in that window.
keiko: That tracks with what their ops lead told me on the call. Intake staff complained the assistant stalls right when the clinics open.
gabe: Looks like they fire a burst of parallel requests at open with no backoff. Retries just pile on and make the 429s worse.
keiko: Quick check before I reply to their ops lead: is Northwind's rate limit 40M tokens per minute? React 👍 if so.
```

> **>>> DECIDE AFTER THIS:** keiko: Quick check before I reply to their ops lead: is Northwind's rate limit 40M tokens per minute? React 👍 if so.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

---

## Row 88

**Today: Mon Oct 5** · #harbor

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 5 · #harbor ---
nadia: Morning all. Want to line up the release and the paper this week. Who has the latest on contamination fixes and where compute stands?
marcus: I've got the contamination scan mostly done. A handful of tasks overlap with public repos, still checking licenses on the replacements before I post the list.
elena: On compute, the last full sweep ran clean overnight. I can slot the rerun once marcus's replacement list is settled.
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
```

> **>>> DECIDE AFTER THIS:** theo: Once the swap list is final I'll rerun the baselines and plot pass rate by repo size. Curious if multi-file tasks widen the gap between models.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena

---

## Row 89

**Today: Mon Sep 14** · #launch

**Team facts as of now**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Sep 14 · #launch ---
alex: For screenshots, should I grab them from a fresh workspace so the add-agents step shows? Or use a beta one that already has agents in the list?
sara: Make it Sep 24, not the 17th. Thursday lands with the Series A announcement.
olavo: oh nice, pairing it with the funding news is way better press-wise 🙌 I'll need to rejig the email and partner heads-up timing around that
alex: so with the shift, can I hold screenshots until the onboarding flow is settled? Otherwise I'd just redo them 😅
oli: Holding screenshots makes sense. Onboarding flow still has a couple open tickets on my side, so no point shooting until they settle.
frida: Updating the partner calendar now: public launch is Sep 24, so I'll move the beta partner notes off the 17th. Will hold the heads-up wording until Olavo has the new timing 👍
aj: Looked at the older beta workspaces. A few have the agent role seeded but no agent members attached, so their member list will look empty even if agents exist.
frida: @aj for those older beta workspaces, can admins just attach agents themselves, or does someone need to fix it on our end? Partners will ask 🤔
aj: Admins should be able to attach them from member settings, I think. Need to confirm the seeded role doesn't block it on those older ones.
olavo: ok so with the new timing I'm redoing the email schedule tonight. will post a fresh send plan here once it's drafted 📝
oli: fyi the two open onboarding tickets are both around the add-agents step, one's a flaky state on the skip button. will ping when it's stable.
alex: if the skip button is flaky, should the add-agents step stay skippable at all? Might be cleaner to make it required for admins, just thinking out loud
olavo: catching up, can the waitlist email still go out the day before Sep 17 like we planned? want to lock the send slot 📬
frida: another partner question: can admins mute agents per channel? They're nervous about agents jumping into threads untagged 🤔
aj: Per-channel mute isn't something I can confirm yet. Need to check whether agent permissions are scoped per channel or only per workspace.
```

> **>>> DECIDE AFTER THIS:** aj: Per-channel mute isn't something I can confirm yet. Need to check whether agent permissions are scoped per channel or only per workspace.

**Team facts again**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

---

## Row 90

**Today: Wed Sep 30** · #infra

**Team facts as of now**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Wed Sep 30 · #infra ---
lucia: Firmware rollout on the IB leaf switches is staged but not pushed. Seeing a few flapping links on rack group C that I want to look at first.
kofi: Are the flapping links on C causing NCCL timeouts yet? Want to know if checkpoint writes from those nodes are getting stalled mid-save.
hana: Quick check while we're on checkpoints: kestrel checkpoint cadence is every 500 steps, right? React ✅ if that's what you have.
(kofi reacted ✅ to hana's message)
lucia: Not seeing NCCL timeouts yet, just symbol errors and retrains on a couple of C uplinks. Checking cable seating before touching firmware.
kofi: Good. If those C uplinks retrain mid-save, I'd expect partial shards on the writer ranks. I'll check how the async flush handles a stalled write.
wen: Who's owning fabric incident on-call for kestrel right now? I need a name on the rota before I lock the allocation table.
mateo: lunch? thinking the taco truck by the loading dock, it's been parked there all week
```

> **>>> DECIDE AFTER THIS:** mateo: lunch? thinking the taco truck by the loading dock, it's been parked there all week

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 91

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
--- Mon Oct 12 · #harbor ---
elena: That's me, I hold the reservation. Refactor jobs are already at the front of the queue, so they'll land on it.
marcus: Histogram's rough but promising: reformatted gist copies bunch up at the top, and generic argparse-style boilerplate lookalikes sit well below with a clear dip between.
yuki: That dip is exactly what we want. Can you overlay the borderline cases on the histogram? I'd like to see where the ambiguous ones fall.
marcus: Sure, I'll mark the borderline ones in a different color. A few are fixtures copied from a popular tutorial repo, so they might land near the dip.
yuki: Tutorial-repo fixtures are a good edge case. If they sit near the dip, I'd say describe them separately in the paper rather than force them into either bucket.
marcus: I'll check commit dates on those tutorial fixtures. If the tutorial repo predates the task repos, that changes how we frame them.
nadia: For the contamination section, let's say "near-duplicate" and keep the tone factual. No "leaked" or "cheated" wording, since reviewers will read that as an accusation.
yuki: For the patched-versus-untouched plot, I'd add bootstrap intervals per scaffold. Otherwise a small gap on a few tasks will look bigger than it is.
theo: Resample over tasks, not seeds, right? Otherwise the intervals on the refactor scaffold will look tighter than they should.
yuki: Yes, resample over tasks. Seeds within a task are correlated, so seed-level resampling would understate the spread. Task-level bootstrap, then average seeds inside each draw.
theo: Got it, task-level bootstrap. I'll add the interval bands to the patched-versus-untouched plot per scaffold and flag the refactor one if it looks wide.
marcus: Tutorial-repo commit dates are mostly earlier than the task repos, so I'll describe those fixtures in their own paragraph with the overlay.
--- Wed Oct 21 · #harbor ---
nadia: Two days out. Can everyone post what's still open on your side in here? I'll sort the final list from that.
elena: Cluster queue looks fine on my side. Only thing open is making sure the last batch of eval jobs doesn't get preempted overnight.
theo: Mine's the results table. Two of the baseline rows still have old numbers in them, so I need to refresh those before anyone quotes the table.
```

> **>>> DECIDE AFTER THIS:** theo: Mine's the results table. Two of the baseline rows still have old numbers in them, so I need to refresh those before anyone quotes the table.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,140 items (changed Mon Oct 19; previously 1,200 items)
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 92

**Today: Mon Oct 5** · #harbor

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 5 · #harbor ---
felix: I'll add a language field and a files-touched field to the task metadata, so Theo's breakdowns come straight from the release without a separate script.
yuki: Felix, can the language field hold more than one value? The Rust parser fix also touches TOML config, and I'd rather not force a single label.
felix: Yes, I'll make language a list instead of a single label. Then the Rust parser fix can carry both Rust and TOML, and Theo can group on either.
yuki: With language as a list, I'll report breakdowns by primary language only, so multi-label tasks don't get double counted in the paper tables.
theo: Primary-language only works for me. I'll flag in the table caption which tasks are multi-label so reviewers don't wonder why TOML never shows up.
elena: Fair warning, the eval jobs have more retries than I do at the gym. Rust timeouts are gonna be the worst offenders.
marcus: I'll also check whether the Rust build tool's test suite pulls anything from the network. If it does, the sandbox will fail those no matter what the model writes.
yuki: If it does pull from the network, vendoring the dependencies into the image would fix that. Otherwise we'd have to drop those tasks and look for others.
elena: Vendoring works for me. I can bake the crates into the sandbox image so builds run offline. Marcus, send me the lockfile once you pick the tasks.
marcus: Will do. Checking now whether the lockfile is pinned for that Rust tool. If it isn't, I'll resolve versions first so the crates don't drift.
yuki: If the lockfile isn't pinned, note which crate versions you resolve to. I'd like the paper's appendix to list the toolchain so the Rust tasks are reproducible.
marcus: Lockfile's checked in but a couple of entries use loose version ranges. I'll resolve them and write down what each crate lands on.
elena: Once the crates are resolved I'll bake them into a test image and do a dry run on the Rust tasks, just to see where the slow ones land.
yuki: When you do the dry run, log per-task wall time too. I'd like to see whether the slow Rust tasks cluster on the multi-file ones.
theo: Per-task wall time would also help the baseline table. I can add a column for median runtime per language if the logs have it.
```

> **>>> DECIDE AFTER THIS:** theo: Per-task wall time would also help the baseline table. I can add a column for median runtime per language if the logs have it.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena

---

## Row 93

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
rachel: Perfect. Add a line or two on why jitter matters, so Keiko can frame it as a tip, not criticism.
keiko: Their ops lead hand-tuned that prompt for months, so she'll want reassurance that trimming won't change how the assistant behaves.
gabe: Fair. Caching keeps the prompt text identical, so behavior shouldn't shift. I can diff outputs on the de-identified forms before and after to show her.
gabe: Will do. I'll frame jitter as spreading retries out so clients don't all hit at once. Keiko can drop it in as a friendly tip.
rachel: Before/after diff on the forms would make a solid slide for the renewal deck. Customers like seeing proof, not promises.
rachel: Quick flag so nobody mixes them up: Northwind Logistics is a separate customer and renews Nov 15. Keep their numbers out of the Northwind Health deck.
gabe: On missing fields: yes. Have the model return a list of empty required fields in structured output, and the UI can highlight them for staff.
keiko: That's a clean answer, thanks. I'll pass it to their ops lead. She'll probably ask if staff can override a flagged field.
gabe: Yes, override is easy. I'd log which fields staff overrode though, so we can see where the model keeps misfiring.
keiko: Good call on logging overrides. Their ops lead will want a weekly view of the misfires, so staff feel heard rather than monitored.
gabe: A weekly misfire view is easy once overrides are logged. I can sketch a simple dashboard grouped by field type for her.
rachel: Great. Send it over when it's ready and I'll pass it to Keiko with a short intro. Keep the tone light.
keiko: A dashboard sketch would land well. She's also asking whether the misfire view can be shared with her floor supervisors, not just her.
gabe: Sharing with supervisors is fine technically. I'd just scope it by role so they only see their own floor's fields, nothing patient-level.
tomas: Looping in pricing for a moment: for the renewal, I'd float 15% off list as a possible discount. Purely a suggestion at this stage; nothing is decided, and it needs Darnell's sign-off.
```

> **>>> DECIDE AFTER THIS:** tomas: Looping in pricing for a moment: for the renewal, I'd float 15% off list as a possible discount. Purely a suggestion at this stage; nothing is decided, and it needs Darnell's sign-off.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Gabe to load-test Northwind's workload at their full rate limit (check point: Wed Oct 14)

---

## Row 94

**Today: Wed Oct 7** · #harbor-evals

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Marcus to finish the license review for the scraped repositories (check point: Fri Oct 9)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Wed Oct 7 · #harbor-evals ---
elena: yeah, most of them had it. checking if the affinity label is even getting parsed, might be silently falling back to a placement that never resolves
theo: Plots so far: the multi-file items fail mostly on import errors, not logic. Might be the same install issue Elena hit, so I'll separate those out.
felix: Side note for the release notes: harbor-lite, the internal smoke set, has 200 items. Separate from the held-out set, so I'll keep the two clearly distinguished in the manifest.
yuki: If the import-error failures are really install issues, I'd exclude them from the bug-fix slice analysis or at least report them as a separate failure category. Otherwise we're measuring the environment, not the model.
theo: if it's falling back silently, try a dry-run submit with the flag and compare the resolved placement spec against a job that schedules fine
theo: Agreed. I'll split import errors into their own bucket in the plots and rerun once Elena's longer install window is in.
elena: Also thinking of prebuilding a cached dependency image per repo, so installs don't eat the timeout budget. I'll try it on the messiest multi-file ones first.
elena: good call, running the dry-run now. the resolved spec for the stuck ones has an empty topology field, the working job has it populated
nadia: Cached images are a good idea. Worth a sentence in the paper's methods section so reviewers know installs aren't counted against the model.
marcus: Cached images also help the contamination check. I can diff the pinned dependency versions against the repos' original commit dates and catch anything that predates the snapshots.
theo: empty topology would explain it. Does the parser drop the label when the node pool name has a hyphen? I hit that once on my branch.
yuki: Good, but dependency pinning only catches so much. Might also be worth checking whether any fix commits are quoted verbatim in public issue threads, since that leaks the answer too.
marcus: Good point on issue threads. I can grep the public trackers for long verbatim diff snippets and flag any items where the fix text shows up before the snapshot.
theo: If the issue-thread grep flags items, I can rerun those separately and see whether baseline scores on them look inflated compared to the clean ones.
yuki: If flagged items do inflate baseline scores, that's a nice contamination figure for the paper. Inflated-vs-clean gap, plotted per slice, with intervals.
```

> **>>> DECIDE AFTER THIS:** yuki: If flagged items do inflate baseline scores, that's a nice contamination figure for the paper. Inflated-vs-clean gap, plotted per slice, with intervals.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Marcus to finish the license review for the scraped repositories (check point: Fri Oct 9)

---

## Row 95

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
wen: Drill is a good chance to check straggler behavior after restore too. Last time a couple of ranks came back with lower MFU than the rest.
```

> **>>> DECIDE AFTER THIS:** wen: Drill is a good chance to check straggler behavior after restore too. Last time a couple of ranks came back with lower MFU than the rest.

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps (changed Fri Oct 9; previously every 500 steps)
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

---

## Row 96

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
aj: For the screenshot thread, can someone confirm the agent's reply doesn't quote anything from a private channel? Memory recall can surface odd stuff.
```

> **>>> DECIDE AFTER THIS:** aj: For the screenshot thread, can someone confirm the agent's reply doesn't quote anything from a private channel? Memory recall can surface odd stuff.

**Team facts again**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per human seat, agents free (changed Wed Sep 16; previously $12 per seat, agent actions metered)
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

---

## Row 97

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
olavo: Also for the launch post, we should probably have a short demo gif of the shared memory bit. People love seeing that 🎬
```

> **>>> DECIDE AFTER THIS:** olavo: Also for the launch post, we should probably have a short demo gif of the shared memory bit. People love seeing that 🎬

**Team facts again**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

---

## Row 98

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
lucia: Pulled IB port counters overnight. One leaf uplink is showing creeping symbol errors, still below the alarm line. Keeping an eye on it.
wen: Vendor folks want to come onsite and look at the cluster. Dmitri, you want to be in the room for that or should I just handle it?
wen: Which leaf is that? Want to see if any kestrel nodes hang off it before I touch the spare pool.
dmitri: I'd like to be there. Want them to see the IB fabric flaps firsthand, not just hear about them secondhand.
```

> **>>> DECIDE AFTER THIS:** dmitri: I'd like to be there. Want them to see the IB fabric flaps firsthand, not just hear about them secondhand.

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

---

## Row 99

**Today: Tue Oct 6** · #acct-northwind

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list

**Recent messages** (oldest first; the last one is the decision message)

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
darnell: Worth getting ahead of procurement on this one. If their big ask comes in early, I'd rather we already have a view on where we'd hold.
ines: Before we settle on a negotiating position, I'd like to see what they redlined last time. Their legal team tends to reopen data terms.
```

> **>>> DECIDE AFTER THIS:** ines: Before we settle on a negotiating position, I'd like to see what they redlined last time. Their legal team tends to reopen data terms.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list

---

## Row 100

**Today: Tue Sep 8** · #launch

**Team facts as of now**

- (nothing decided yet)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Tue Sep 8 · #launch ---
sara: ok team, launch kickoff. I'm going to lock the date, the raise announcement, pricing and who owns what for launch week. Read along, shout if something's off.
alex: reading along 👀 quick q: are we showing the agent-as-member idea in the onboarding flow at launch, or keeping that for after?
frida: +1 to Alex's q. Two design partners got lost on day one because they didn't realize the agent shows up in the member list.
oli: Agent already has its own member entry in the runtime, so showing it in onboarding is just a UI change. No backend work needed.
```

> **>>> DECIDE AFTER THIS:** oli: Agent already has its own member entry in the runtime, so showing it in onboarding is just a UI change. No backend work needed.

**Team facts again**

- (nothing decided yet)

---

## Row 101

**Today: Mon Oct 5** · #harbor

**Team facts as of now**

- (nothing decided yet)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 5 · #harbor ---
nadia: Morning all. Want to line up the release and the paper this week. Who has the latest on contamination fixes and where compute stands?
marcus: I've got the contamination scan mostly done. A handful of tasks overlap with public repos, still checking licenses on the replacements before I post the list.
```

> **>>> DECIDE AFTER THIS:** marcus: I've got the contamination scan mostly done. A handful of tasks overlap with public repos, still checking licenses on the replacements before I post the list.

**Team facts again**

- (nothing decided yet)

---

## Row 102

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
lucia: Firmware rollout on the IB leaf switches is staged but not pushed. Seeing a few flapping links on rack group C that I want to look at first.
kofi: Are the flapping links on C causing NCCL timeouts yet? Want to know if checkpoint writes from those nodes are getting stalled mid-save.
hana: Quick check while we're on checkpoints: kestrel checkpoint cadence is every 500 steps, right? React ✅ if that's what you have.
(kofi reacted ✅ to hana's message)
lucia: Not seeing NCCL timeouts yet, just symbol errors and retrains on a couple of C uplinks. Checking cable seating before touching firmware.
kofi: Good. If those C uplinks retrain mid-save, I'd expect partial shards on the writer ranks. I'll check how the async flush handles a stalled write.
wen: Who's owning fabric incident on-call for kestrel right now? I need a name on the rota before I lock the allocation table.
mateo: lunch? thinking the taco truck by the loading dock, it's been parked there all week
lucia: I'll take it.
kofi: Also want to confirm the async flush path retries on a short write instead of silently marking the shard complete. Looking at the writer rank logs now.
lucia: Reseated one of the C uplinks, symbol errors dropped on that port. Still watching the other. Will hold firmware until counters stay clean.
kofi: Found it: on a short write the flush thread logs a warning but still flips the shard to complete. Need to patch that before we trust any save from C.
```

> **>>> DECIDE AFTER THIS:** kofi: Found it: on a short write the flush thread logs a warning but still flips the shard to complete. Need to patch that before we trust any save from C.

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 103

**Today: Mon Sep 28** · #kestrel-run

**Team facts as of now**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Sep 28 · #kestrel-run ---
lucia: CRC counters on the swapped port are flat so far. Other flapping uplink still on the old optic, I'll swap it next and rerun the soak.
dmitri: Mateo, your loader sizing doesn't match the allocation Wen confirmed. Redo it against the confirmed number.
mateo: Fair, my bad. Redoing the loader sizing against Wen's number. Prefetch worker count per node will probably shift too, rechecking read throughput after.
kofi: Restore path is my next test. Will kill a rank mid-flush and confirm we resume cleanly from the staged NVMe copy.
mateo: Once dedup lands, I'll finish moving the tokenized datasets to the new storage tier by Fri Oct 2. That leaves a few days of buffer before the start.
hana: Lucia, can you send me the port-to-rank mapping for the flapping uplinks? I want straggler alerts to tag those ranks directly.
lucia: Yep, mapping coming. Both ports sit on the same leaf switch, so it's a handful of ranks per node. Exporting from the switch config now.
hana: Thanks. Once I have it I'll also add per-rank NCCL timing to the dashboard, so a slow allreduce on those ranks is visible right away.
kofi: Lucia, when the other uplink gets swapped, give me a heads-up. If those racks drop mid-soak I want to see how the staging path handles a rank vanishing.
lucia: Will do. Swapping the second optic after the current soak window closes, so CRC counters on the first port stay a clean baseline.
lucia: Heads up, the cluster room is louder than a jet engine today. Swapping optics in there with earplugs in, so slow to reply if I miss pings.
kofi: Once the mapping lands I'll also check whether those ranks end up in the same NCCL ring segment. A flaky one could stall the whole ring.
wen: If the ring segment does include those ranks, I can reshuffle placement so they land on a different leaf. Cheap on my side.
hana: Mapping would also let me flag whether those ranks show up as stragglers in the last burn-in logs. Pulling those now to compare.
dmitri: If those ranks show up as stragglers in burn-in, I want that in the writeup before we lock the placement.
```

> **>>> DECIDE AFTER THIS:** dmitri: If those ranks show up as stragglers in burn-in, I want that in the writeup before we lock the placement.

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 104

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
--- Mon Oct 12 · #harbor ---
yuki: For the patched-versus-untouched plot, I'd add bootstrap intervals per scaffold. Otherwise a small gap on a few tasks will look bigger than it is.
theo: Resample over tasks, not seeds, right? Otherwise the intervals on the refactor scaffold will look tighter than they should.
yuki: Yes, resample over tasks. Seeds within a task are correlated, so seed-level resampling would understate the spread. Task-level bootstrap, then average seeds inside each draw.
theo: Got it, task-level bootstrap. I'll add the interval bands to the patched-versus-untouched plot per scaffold and flag the refactor one if it looks wide.
marcus: Tutorial-repo commit dates are mostly earlier than the task repos, so I'll describe those fixtures in their own paragraph with the overlay.
--- Wed Oct 21 · #harbor ---
nadia: Two days out. Can everyone post what's still open on your side in here? I'll sort the final list from that.
elena: Cluster queue looks fine on my side. Only thing open is making sure the last batch of eval jobs doesn't get preempted overnight.
theo: Mine's the results table. Two of the baseline rows still have old numbers in them, so I need to refresh those before anyone quotes the table.
yuki: Open on my side: the pass criteria paragraph in the methods section still reads ambiguously. Want to tighten the wording before anyone cites it.
marcus: Mine's the contamination writeup. Need to reword how we describe the overlap check so reviewers don't read it as stronger than it is.
felix: Mine's the release checklist. Changelog is drafted but I still need to go through the tagging steps and double-check the package notes match the paper.
nadia: Thanks all. Theo, can you flag which two baseline rows are stale so Yuki and Marcus know what not to quote yet?
felix: My release jobs are queued behind the eval batch. Who actually owns the compute reservation for the eval runs? Want to know who to ping if they stall.
yuki: Also noticed the pass@1 plot in the draft has a y-axis that makes the gap between models look bigger than it is. Worth rescaling.
theo: Rescaling the plot is easy, I'll regenerate it with a zero-based axis and add error bars so the gap reads honestly.
```

> **>>> DECIDE AFTER THIS:** theo: Rescaling the plot is easy, I'll regenerate it with a zero-based axis and add error bars so the gap reads honestly.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,140 items (changed Mon Oct 19; previously 1,200 items)
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 105

**Today: Mon Oct 5** · #harbor

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 5 · #harbor ---
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
marcus: Rust build tool license came back permissive, so those candidates are usable. The fix touches the parser and config loader together, and the tests are deterministic.
elena: Rust builds will be slow in the sandbox. I'll check the image has the toolchain cached so timeouts don't masquerade as model failures.
felix: I'll add a language field and a files-touched field to the task metadata, so Theo's breakdowns come straight from the release without a separate script.
yuki: Felix, can the language field hold more than one value? The Rust parser fix also touches TOML config, and I'd rather not force a single label.
```

> **>>> DECIDE AFTER THIS:** yuki: Felix, can the language field hold more than one value? The Rust parser fix also touches TOML config, and I'd rather not force a single label.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena

---

## Row 106

**Today: Thu Sep 10** · #eng

**Team facts as of now**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Thu Sep 10 · #eng ---
frida: Good point. A couple of partners asked about exactly that. Sandbox with fake channels feels safer, maybe seeded with some funny agent chatter 😄
oli: Frida: "Known issue. Two agents can answer the same unaddressed channel message. We've reproduced it and are fixing it in the runtime." Fine to send that.
oli: Side note: closed AND-314, the search indexing bug. That one was mine. AND-341 is still open.
alex: Quick question on the double reply: should the onboarding copy say anything about multiple agents answering in a channel, or wait until the fix lands?
oli: Memory store still unchecked. aj, do you have a baseline yet for concurrent reads on shared memory with lots of agents active?
alex: Love the fake chatter idea. Should the sandbox agents have names and personalities so people can tell them apart at a glance? Maybe a little name card at the demo table?
aj: No baseline yet. I have a read-heavy test script but it only simulates a handful of agents. Need to scale it up first.
oli: There's an agent-sim harness in the runtime tests that spawns fake agents with canned channel traffic. Might save you rebuilding. Check if it fits your script.
frida: Yes! Name cards are great. One partner mentioned she'd love to see an agent jump into a thread unprompted, so maybe a script for that moment 😄
aj: Thanks, I'll try the sim harness for the load test. Also, on DM permissions: I'll merge the forwarded-DM permission check by Tue Sep 15, late-add edge case included.
alex: Ooh, unprompted jump-in is the best demo. Should we seed a thread where two humans are stuck on something, so the agent has a natural reason to chime in?
frida: Related to the load test: one partner runs a ton of agents in a single workspace and said memory lookups felt laggy during their Monday standup rush.
oli: That lag report is useful. Frida, do you know if their agents were all reading the same memory entries or spread out? Changes how I'd shape the load test.
frida: Good question, not sure. I'll ask them which channels the agents were hitting during the rush and get back to you.
frida: Yes, something relatable like two people arguing over which snack order to get for the lunch 😂 agent jumps in with a tally
```

> **>>> DECIDE AFTER THIS:** frida: Yes, something relatable like two people arguing over which snack order to get for the lunch 😂 agent jumps in with a tally

**Team facts again**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

---

## Row 107

**Today: Mon Oct 12** · #acct-northwind

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 12 · #acct-northwind ---
gabe: I can pull their traffic by hour from the last few weeks and see how close they run to the ceiling.
tomas: Order form draft pasted below. Pricing block reads 18% off list, with the rationale itemized line by line underneath so finance can trace each step.

Pricing: Northwind Health API usage, 18% off list. Rationale schedule attached as Exhibit B.
keiko: Clinical informatics also asked if they can pilot the patient messaging use case in a sandbox before committing other departments. Worth planning for.
ines: On the sandbox pilot: will they use real patient messages or synthetic ones? That changes which terms apply during the trial.
keiko: Not sure yet. I'll ask the sponsor on our call. My guess is they start synthetic, but I'll confirm.
rachel: Tomas, the number in that pricing block doesn't match what I've been framing for Northwind. Can you confirm which one it's built on?
keiko: Gabe, while you're pulling traffic, what's Northwind's current rate limit? Sponsor will probably ask when I pitch the rollout.
gabe: Current limit is 40M tokens per minute. I'll compare that against their hourly peaks so you know how much headroom to quote the sponsor.
darnell: Once Gabe has the traffic picture, let's fold it into the rollout story. Capacity plus a bigger footprint is a stronger pitch than discount talk.
gabe: Quick question for the sponsor call: would portal messaging run under the same API project, or a separate one? Changes how we split capacity.
ines: Separate projects would make it cleaner for me too. Data terms could map to each use case instead of one blanket scope.
keiko: Separate projects might land well. Their sponsor mentioned compliance likes to review each use case on its own, so that fits how they already work.
gabe: Load test is done. Ran Northwind's workload at their full rate limit and it passed, p95 latency looked fine the whole run.
tomas: Rachel, understood. I'm re-checking which approval record I built the pricing block from and will report back once I've compared it against your framing.
rachel: Whatever Tomas finds, finance will want any discount tied to something we get back. Expanded departments could be that trade.
```

> **>>> DECIDE AFTER THIS:** rachel: Whatever Tomas finds, finance will want any discount tied to something we get back. Expanded departments could be that trade.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

---

## Row 108

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
alex: Quick question on muting: does a muted agent still read the channel for memory, or fully stop? Partners will ask.
aj: Mute as built only silences posting and notifications. Memory indexing still runs on the channel. A true stop-reading option would be a separate flag.
alex: Random q while we're on the waitlist email: who's actually sending it Thursday? Olavo, is that you, or does Sara hit send?
frida: Another partner question: if they remove an agent from the workspace, does its shared memory get wiped or stay searchable?
aj: Frida, on removal: I'd need to check how memory is keyed. If it's tied to the agent identity, deleting the agent could orphan entries.
frida: Thanks AJ. The partner asking is swapping agents mid-project, so they'd want the old one's memory to carry over to the new one.
alex: For the swap case, would partners expect memory to carry over automatically, or a manual "transfer memory" step when they replace an agent?
aj: Automatic carry-over gets tricky. Old memory includes entries from channels the new agent was never in, so permissions would have to be re-checked.
frida: I think that partner would be fine with a manual transfer step, as long as it shows which channels' memory comes across and what gets skipped.
olavo: Draft FAQ answer for the memory question: "Agents read channel and DM history to build team memory, so they pick up context without anyone re-explaining it. You can mute an agent per channel anytime." Thoughts?
oli: Found a bug in staging: a muted agent still shows the typing indicator in the channel. Filing a ticket, ENG-412.
alex: For the muted state, I'm thinking a small bell-slash icon next to the agent's name in the sidebar. Does the member list already expose that flag?
aj: Yes, the muted flag is on the membership object, so the member list endpoint already returns it. Sidebar just needs to read it.
frida: Also, one of the partners hit the double-post thing again today, agent replying twice in a thread. Who has AND-341 right now?
alex: For the bell-slash icon, should hover show a tooltip like "Muted in this channel"? Want the copy to match the FAQ wording.
```

> **>>> DECIDE AFTER THIS:** alex: For the bell-slash icon, should hover show a tooltip like "Muted in this channel"? Want the copy to match the FAQ wording.

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

## Row 109

**Today: Tue Oct 6** · #acct-northwind

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30

**Recent messages** (oldest first; the last one is the decision message)

```
--- Tue Oct 6 · #acct-northwind ---
rachel: Kicking off the Northwind renewal thread. Want one place for timeline, pricing, sponsor, and paperwork. Keiko, any early signals from their side?
keiko: Yes, a couple. Their clinical informatics lead mentioned on our last call that usage has grown a lot since the pilot teams went live. Sounds happy overall.
gabe: Good sign. Growth like that usually means we should check their rate limit headroom before we talk renewal. Want me to pull usage trends?
rachel: Yes please, Gabe. Timeline note for everyone: the Northwind renewal signature deadline is Oct 30. Working back from that for pricing, legal review, and sponsor sign-off.
gabe: On it. I'll also check whether any of their pilot teams are bursting at peak hours, since that's usually where throttling shows up first.
```

> **>>> DECIDE AFTER THIS:** gabe: On it. I'll also check whether any of their pilot teams are bursting at peak hours, since that's usually where throttling shows up first.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30

---

## Row 110

**Today: Mon Sep 14** · #launch

**Team facts as of now**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Sep 14 · #launch ---
oli: repro for the skip button: go back from the next step and the state resets, so skip shows enabled when it shouldn't. Tracing it.
alex: does the reset also hit people who go back after already adding an agent? Might show an empty list again 🤔
alex: quick q, who actually sends the waitlist email? I need to know who to give the header image to 📬
olavo: me! send the header image my way, I'm sending the waitlist email 📬
alex: Sending the header image over now. I made a dark and a light version, so pick whichever fits the email template 🎨
frida: Another partner asked if there's a visible indicator when an agent joins a thread untagged. Would calm the nerves a bit 🙂
alex: Could be a small badge or avatar ring on the message when an agent joins untagged. I can mock a couple options 🎨
aj: Update: the forwarded-DM permission check is merged. Forwarding a DM into a channel now checks the original DM's access first. That one's done.
oli: @alex yes, going back after adding an agent also resets the list view. Same root cause, so the fix should cover both. Testing it now.
frida: One more partner question: can admins see what an agent has stored in shared memory? They want to check it's not holding anything odd 🤔
aj: Memory entries are stored per workspace, but I'm not sure there's an admin-facing view yet. Checking what the store exposes before I say anything to partners.
olavo: for the press kit, can someone send me a clean screenshot of an agent replying in a thread? Current one has test data in it 😅
alex: Random pricing thought while mocking the badge: what if it's $12 per human seat and agents are free? Just an idea, nothing decided. Sara, that's your call 🤔
frida: I can grab a screenshot from our demo workspace for the press kit. Just need to make sure no partner names show 📸
oli: skip button fix is in review. once it's merged I'll rerun the onboarding flow end to end on a fresh workspace 🔧
```

> **>>> DECIDE AFTER THIS:** oli: skip button fix is in review. once it's merged I'll rerun the onboarding flow end to end on a fresh workspace 🔧

**Team facts again**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

---

## Row 111

**Today: Mon Sep 28** · #kestrel-run

**Team facts as of now**

- kestrel pretraining run (start date): Oct 5

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Sep 28 · #kestrel-run ---
dmitri: Kickoff thread for kestrel. Need start date, allocation, stability rules and data readiness all pinned down in here today. Who has blockers?
lucia: Fabric blocker from my side: two leaf switches in the new pod still flap under heavy all-reduce. Haven't isolated whether it's optics or firmware.
wen: Do those flapping leaf switches sit in the pod I was planning to hand kestrel? If so I need to rework the allocation table.
lucia: Yes, same pod. Both flapping leafs feed racks in that pod. Seeing CRC errors on the uplinks, so I'm leaning optics, but not confirmed.
dmitri: Decision: kestrel starts Oct 5. Lucia, get the optics vs firmware call made and fixed well before then. Wen, redo the allocation table around whatever the pod looks like once that's resolved.
lucia: Pulling optic transceiver serials on the flapping uplinks now. If they share a batch, that settles it. Will swap one and rerun all-reduce soak.
```

> **>>> DECIDE AFTER THIS:** lucia: Pulling optic transceiver serials on the flapping uplinks now. If they share a batch, that settles it. Will swap one and rerun all-reduce soak.

**Team facts again**

- kestrel pretraining run (start date): Oct 5

---

## Row 112

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
marcus: For the paper, we should describe the near-duplicate similarity cutoff in the contamination section. Reviewers will ask how we picked it.
yuki: Agreed. A histogram of similarity scores would help, if there's a visible gap between reformatted copies and legit lookalikes, the cutoff justifies itself.
theo: Rescored runs on the untouched tasks look nearly identical so far. Curious if the patched ones drop more on the refactor scaffolds.
theo: Quick one, who actually holds the compute reservation for the fresh runs? Want to make sure the refactor jobs land on it.
elena: That's me, I hold the reservation. Refactor jobs are already at the front of the queue, so they'll land on it.
marcus: Histogram's rough but promising: reformatted gist copies bunch up at the top, and generic argparse-style boilerplate lookalikes sit well below with a clear dip between.
yuki: That dip is exactly what we want. Can you overlay the borderline cases on the histogram? I'd like to see where the ambiguous ones fall.
marcus: Sure, I'll mark the borderline ones in a different color. A few are fixtures copied from a popular tutorial repo, so they might land near the dip.
yuki: Tutorial-repo fixtures are a good edge case. If they sit near the dip, I'd say describe them separately in the paper rather than force them into either bucket.
marcus: I'll check commit dates on those tutorial fixtures. If the tutorial repo predates the task repos, that changes how we frame them.
nadia: For the contamination section, let's say "near-duplicate" and keep the tone factual. No "leaked" or "cheated" wording, since reviewers will read that as an accusation.
yuki: For the patched-versus-untouched plot, I'd add bootstrap intervals per scaffold. Otherwise a small gap on a few tasks will look bigger than it is.
theo: Resample over tasks, not seeds, right? Otherwise the intervals on the refactor scaffold will look tighter than they should.
yuki: Yes, resample over tasks. Seeds within a task are correlated, so seed-level resampling would understate the spread. Task-level bootstrap, then average seeds inside each draw.
theo: Got it, task-level bootstrap. I'll add the interval bands to the patched-versus-untouched plot per scaffold and flag the refactor one if it looks wide.
```

> **>>> DECIDE AFTER THIS:** theo: Got it, task-level bootstrap. I'll add the interval bands to the patched-versus-untouched plot per scaffold and flag the refactor one if it looks wide.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 113

**Today: Mon Sep 28** · #kestrel-run

**Team facts as of now**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Sep 28 · #kestrel-run ---
lucia: Pulling optic transceiver serials on the flapping uplinks now. If they share a batch, that settles it. Will swap one and rerun all-reduce soak.
wen: Whichever way the optics call goes, I'll draft two allocation variants: one with the flapping racks drained, one assuming they come back clean.
dmitri: Quick check Wen: is the kestrel node allocation 2,048 nodes? Want that confirmed before the variants go out.
wen: yep, confirmed
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
```

> **>>> DECIDE AFTER THIS:** lucia: CRC counters on the swapped port are flat so far. Other flapping uplink still on the old optic, I'll swap it next and rerun the soak.

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps

---

## Row 114

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
hana: Tokenizer question again: the 100k vocab run shows noisier loss on code-heavy shards in the small-scale ablation. Anyone looked at the per-domain curves?
mateo: I pulled the per-domain curves last week. Code shards spike right after the Python-heavy batches, looks like whitespace tokens fragmenting differently in the bigger vocab.
```

> **>>> DECIDE AFTER THIS:** mateo: I pulled the per-domain curves last week. Code shards spike right after the Python-heavy batches, looks like whitespace tokens fragmenting differently in the bigger vocab.

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 115

**Today: Wed Oct 7** · #harbor-evals

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Marcus to finish the license review for the scraped repositories (check point: Fri Oct 9)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Wed Oct 7 · #harbor-evals ---
elena: Checked timeouts. The multi-file repos need a longer setup window for dependency installs, otherwise some items will fail before the tests even start.
felix: Longer install window should go in the harness config and the release notes, since it changes what a timeout failure means for those items.
elena: yeah, most of them had it. checking if the affinity label is even getting parsed, might be silently falling back to a placement that never resolves
theo: Plots so far: the multi-file items fail mostly on import errors, not logic. Might be the same install issue Elena hit, so I'll separate those out.
felix: Side note for the release notes: harbor-lite, the internal smoke set, has 200 items. Separate from the held-out set, so I'll keep the two clearly distinguished in the manifest.
yuki: If the import-error failures are really install issues, I'd exclude them from the bug-fix slice analysis or at least report them as a separate failure category. Otherwise we're measuring the environment, not the model.
theo: if it's falling back silently, try a dry-run submit with the flag and compare the resolved placement spec against a job that schedules fine
theo: Agreed. I'll split import errors into their own bucket in the plots and rerun once Elena's longer install window is in.
elena: Also thinking of prebuilding a cached dependency image per repo, so installs don't eat the timeout budget. I'll try it on the messiest multi-file ones first.
elena: good call, running the dry-run now. the resolved spec for the stuck ones has an empty topology field, the working job has it populated
nadia: Cached images are a good idea. Worth a sentence in the paper's methods section so reviewers know installs aren't counted against the model.
marcus: Cached images also help the contamination check. I can diff the pinned dependency versions against the repos' original commit dates and catch anything that predates the snapshots.
theo: empty topology would explain it. Does the parser drop the label when the node pool name has a hyphen? I hit that once on my branch.
yuki: Good, but dependency pinning only catches so much. Might also be worth checking whether any fix commits are quoted verbatim in public issue threads, since that leaks the answer too.
marcus: Good point on issue threads. I can grep the public trackers for long verbatim diff snippets and flag any items where the fix text shows up before the snapshot.
```

> **>>> DECIDE AFTER THIS:** marcus: Good point on issue threads. I can grep the public trackers for long verbatim diff snippets and flag any items where the fix text shows up before the snapshot.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Marcus to finish the license review for the scraped repositories (check point: Fri Oct 9)

---

## Row 116

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
felix: Anyone have strong feelings on the offsite venue? I'm leaning toward the lake house over the downtown coworking space. Yuki, you looked at both, right?
```

> **>>> DECIDE AFTER THIS:** felix: Anyone have strong feelings on the offsite venue? I'm leaning toward the lake house over the downtown coworking space. Yuki, you looked at both, right?

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 117

**Today: Mon Sep 14** · #launch

**Team facts as of now**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Tue Sep 8 · #launch ---
oli: Either works on the runtime side, memory ingestion would just check the mute flag. Product call though, Sara?
olavo: random but for launch day, how many pizzas do we order for 7 people? asking for a friend (the friend is me) 🍕😂
frida: Another design partner asked if the agent's replies trigger the same mobile notifications as human messages. Might need a FAQ line on that too 📱
oli: Agent replies go through the same push path as human messages today. A separate setting would be its own ticket, I can scope it.
olavo: For the launch post I'd love a screenshot of the agent jumping into a thread unprompted. Alex, could you mock one up? 📸
alex: Sure, I can mock the unprompted thread jump. Should the agent's message look different from a human reply, like a small badge, or keep it identical?
frida: My design partners liked having an "agent" label in the member list, so a small badge on messages might feel consistent 🙂
alex: Badge makes sense. I'll try a tiny "agent" tag next to the name, nothing loud, so long threads don't get noisy 🏷️
alex: Planning design freeze around the Sep 18 launch, so mocks for the pricing page, badge and thread-jump screenshot all land before then 🎨
olavo: Also for the launch post, we should probably have a short demo gif of the shared memory bit. People love seeing that 🎬
oli: For the memory gif, I can set up a clean demo workspace with seeded convos so it records without weird leftovers 🎬
frida: Nice, a clean demo workspace would help. A couple of design partners offered to share a quote or two for the launch post if useful 🙌
olavo: Love that, quotes from real teams will make the post. Can someone ask which partners are okay being named? Logos would be great too 🙌
--- Mon Sep 14 · #launch ---
olavo: morning all! weekend recap: launch post draft is at v3, waitlist email copy is mostly done, press kit needs final screenshots. waitlist is up a bunch since Friday too 🚀 want to lock send timing for the week today
frida: quick q from a design partner: do agents show up in their workspace member list by default, or do admins need to add them first?
```

> **>>> DECIDE AFTER THIS:** frida: quick q from a design partner: do agents show up in their workspace member list by default, or do admins need to add them first?

**Team facts again**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

---

## Row 118

**Today: Mon Sep 28** · #kestrel-run

**Team facts as of now**

- (nothing decided yet)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Sep 28 · #kestrel-run ---
dmitri: Kickoff thread for kestrel. Need start date, allocation, stability rules and data readiness all pinned down in here today. Who has blockers?
lucia: Fabric blocker from my side: two leaf switches in the new pod still flap under heavy all-reduce. Haven't isolated whether it's optics or firmware.
wen: Do those flapping leaf switches sit in the pod I was planning to hand kestrel? If so I need to rework the allocation table.
```

> **>>> DECIDE AFTER THIS:** wen: Do those flapping leaf switches sit in the pod I was planning to hand kestrel? If so I need to rework the allocation table.

**Team facts again**

- (nothing decided yet)

---

## Row 119

**Today: Mon Oct 5** · #harbor

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 5 · #harbor ---
nadia: Morning all. Want to line up the release and the paper this week. Who has the latest on contamination fixes and where compute stands?
marcus: I've got the contamination scan mostly done. A handful of tasks overlap with public repos, still checking licenses on the replacements before I post the list.
elena: On compute, the last full sweep ran clean overnight. I can slot the rerun once marcus's replacement list is settled.
yuki: Quick check before I lock the pass criteria section: is the harbor workshop paper submission deadline Oct 23? React 👍 if so.
(nadia reacted 👍 to yuki's message)
theo: Baselines table is still on the old task set. I'll regenerate once the replacements land, otherwise the numbers won't line up with the new items.
marcus: Two of the overlapping tasks are near-verbatim from a popular CLI repo. Leaning toward dropping those outright rather than rewriting them, since the solutions are easy to find.
felix: Release note for planning: the harbor release version is v1.2. It'll carry the contamination replacements once marcus's list is final, so the changelog stays in one place.
yuki: If marcus drops those two CLI tasks, I'll check the difficulty spread afterward. Don't want the replacements skewing easy and inflating pass rates.
```

> **>>> DECIDE AFTER THIS:** yuki: If marcus drops those two CLI tasks, I'll check the difficulty spread afterward. Don't want the replacements skewing easy and inflating pass rates.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2

---

## Row 120

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
lucia: Reseated one of the C uplinks, symbol errors dropped on that port. Still watching the other. Will hold firmware until counters stay clean.
kofi: Found it: on a short write the flush thread logs a warning but still flips the shard to complete. Need to patch that before we trust any save from C.
lucia: taco truck again? the line there was brutal yesterday. I'd rather do the noodle place, it's faster
hana: That's bad for resume too. If a partial shard gets marked complete, we'd only see it as a loss spike after restart. Can we add a checksum verify on load?
kofi: Yes, checksum on load makes sense. I'll write per-shard hashes at flush time and verify on resume, so a bad shard fails loudly instead of loading.
mateo: the noodle place is a 15 min walk though, and the line there moves slow when the lunch crowd from the other building shows up
hana: Hash verify adds load-time cost on resume. Worth timing it on a big shard set so restart latency doesn't balloon.
wen: @dmitri what's the kestrel start date? Need it to lock the allocation table and size the reservation window.
dmitri: Oct 5. That's the start date, so lock the table against it. I don't want it sliding because of the C uplinks.
wen: Got it, locking the table against that. Holding a small spare pool outside the main reservation in case C nodes need to be drained.
kofi: Patch is small: only flip the shard to complete after the write returns full length, otherwise retry. Testing against an injected short write on a writer rank.
lucia: fair, but I have a fabric call coming up so I can't be gone long. could we grab takeout from the noodle place and eat at our desks?
lucia: Second C uplink just retrained again, so I'm swapping the cable on that one. Firmware stays parked until counters hold clean.
hana: Once the patch lands, can we run a resume test from a save taken while a C link is deliberately flapping? Want to see the hash check actually trip.
mateo: takeout works, but then it's cold by the time I walk back. what if I just order ahead from the noodle place and pick it up on the way?
```

> **>>> DECIDE AFTER THIS:** mateo: takeout works, but then it's cold by the time I walk back. what if I just order ahead from the noodle place and pick it up on the way?

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 121

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
elena: patch works, stuck jobs scheduled right away. adding the hyphenated pool test now, then I'll requeue the dropped batch.
felix: With the cached images, the license exclusions and the new manifest fields, this might warrant v1.3 for the release. Just a thought, nothing decided. Nadia, Yuki, does that numbering seem right to you?
yuki: Theo, the gate number in your draft doesn't match my criteria doc, and it's missing the held-out qualifier. Please recheck before the table gets built around it.
theo: nice. worth grepping the other label parsers for the same split-on-hyphen pattern, wouldn't be surprised if the GPU type one does it too.
theo: Ugh, I pulled that number from an older draft. Rechecking against your criteria doc and adding the held-out qualifier before I build the table.
--- Mon Oct 19 · #harbor-evals ---
yuki: Went through the weekend results. Pass rate curves look clean across the board, but the long-horizon tasks have a weird plateau. Might be worth a sentence in the paper on that.
felix: Anyone have strong feelings on the offsite venue? I'm leaning toward the lake house over the downtown coworking space. Yuki, you looked at both, right?
nadia: Thinking the appendix should carry the per-category breakdowns and a couple of full agent transcripts. Too heavy for a workshop paper?
theo: Per-category tables are easy, I can export them straight from the results notebook. Full transcripts are the heavy part, some run absurdly long. Maybe trim to the interesting steps?
yuki: Yeah, I toured both. Lake house has way better space for whiteboarding, but the drive is long and wifi there was spotty.
yuki: Trimming is fine, but I'd keep one full transcript from the plateau tasks untouched. Readers will want to see the agent looping, not a cleaned-up version.
felix: Spotty wifi could hurt if we want to demo anything live. Did the lake house have a wired port anywhere, or would we tether?
theo: Ok, one untouched plateau transcript, rest trimmed. I'll export per-category tables against the 1,200 held-out items so the denominators match what we say in the main text.
yuki: For the plateau transcript, the task where the agent keeps rerunning the same failing build after editing the wrong config file is the clearest loop.
yuki: There was one ethernet port in the kitchen nook, I think. Router was in the garage though, so tethering might be more reliable.
```

> **>>> DECIDE AFTER THIS:** yuki: There was one ethernet port in the kitchen nook, I think. Router was in the garage though, so tethering might be more reliable.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 122

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
wen: Drill is a good chance to check straggler behavior after restore too. Last time a couple of ranks came back with lower MFU than the rest.
kofi: Good point on stragglers. I'll log per-rank restore time and first-step time so slow ones stand out right away.
```

> **>>> DECIDE AFTER THIS:** kofi: Good point on stragglers. I'll log per-rank restore time and first-step time so slow ones stand out right away.

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps (changed Fri Oct 9; previously every 500 steps)
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

---

## Row 123

**Today: Wed Oct 7** · #harbor-evals

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena

**Recent messages** (oldest first; the last one is the decision message)

```
--- Wed Oct 7 · #harbor-evals ---
nadia: Ok, we need to nail down the release gate and what goes in the held-out set today. Marcus, where are we on licensing for the scraped repos?
marcus: Mostly sorted. Most repos are MIT or Apache, but a handful have no license file at all, so I'm leaning toward dropping those until we hear back from maintainers.
yuki: Dropping the unlicensed ones makes sense to me. Do we know if they skew toward any particular task type? Don't want the held-out set lopsided afterward.
```

> **>>> DECIDE AFTER THIS:** yuki: Dropping the unlicensed ones makes sense to me. Do we know if they skew toward any particular task type? Don't want the held-out set lopsided afterward.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena

---

## Row 124

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
kofi: Good point on stragglers. I'll log per-rank restore time and first-step time so slow ones stand out right away.
dmitri: Fine, but the drill can't slip because of the reseat. If it's going to eat time, tell me now.
kofi: Won't slip. I'll run the checkpoint-restart drill on the full allocation by Sat Oct 10, and the leaf 14 reseat goes in the restore idle window.
hana: Also want a baseline of loss and grad-norm on the restored ranks, so we can tell a clean resume from a silent divergence.
kofi: tighter save interval means more flush volume than I budgeted for. Rerunning the write numbers against the new tier now, will post what I find.
mateo: I can pull sustained write throughput per stripe from the earlier soak test, so you're not plugging in a spec-sheet number.
dmitri: Assume they need an escort until the hall desk says otherwise. Also ask them to bring an optical power meter, a few links look marginal on rx levels.
hana: Heads up, family emergency came up and I have to log off for the day. Alert mute and the baseline setup aren't done yet, so someone please cover monitoring for the drill.
lucia: I can handle the leaf 14 stall alert mute since I'm the one reseating. Someone point me at the rule in Hana's alerting config.
kofi: It's the step_time_stall rule in the stability alerts yaml. Scope the mute by host label for leaf 14, not a global silence.
lucia: Found the rule. Scoping the silence by host label on leaf 14 only, and I'll drop it once symbol error counters stay flat after the reseat.
wen: Baseline for loss and grad-norm on restored ranks is still orphaned. Kofi, can your restore logging also dump those per rank?
wen: Added the power meter to the vendor's bring list. I'll send them the full checklist with the escort note once badge names are in.
kofi: Checkpoint-restart drill is done on the full allocation, and it passed. Restore took 11 minutes. Per-rank restore and first-step times are logged, so I'll go through the slow ranks next.
lucia: Leaf 14 uplink reseat went in during the restore idle window. Symbol error counters flat so far, so the scoped silence stays on while I watch.
```

> **>>> DECIDE AFTER THIS:** lucia: Leaf 14 uplink reseat went in during the restore idle window. Symbol error counters flat so far, so the scoped silence stays on while I watch.

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps (changed Fri Oct 9; previously every 500 steps)
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

---

## Row 125

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
wen: Table's reposted in the sheet. It assumes kestrel pretraining starts Oct 5, so the reserved block stays held from today. Tokenizer choice doesn't change the allocation, only the embedding shard layout.
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
```

> **>>> DECIDE AFTER THIS:** lucia: Port-to-node map for that row is dumped to the sheet. CRC errors all sit on optics from the same vendor lot.

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 126

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
keiko: Security lead replied on the sub-processor question: they want the addendum version, and they'd like a changelog of recent additions too.
ines: The changelog is fine in principle. I want to check how the addendum handles notice of new sub-processors before it goes in their packet.
keiko: Security lead also asked if the changelog can come as a spreadsheet instead of a PDF. Their reviewers like to filter by vendor.
ines: Spreadsheet is fine by me. I'd want a confidentiality note on the first tab, and the entries should match the addendum wording exactly.
```

> **>>> DECIDE AFTER THIS:** ines: Spreadsheet is fine by me. I'd want a confidentiality note on the first tab, and the entries should match the addendum wording exactly.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

---

## Row 127

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
--- Mon Oct 12 · #kestrel-run ---
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
mateo: Both loaders are out of rotation. Prefetch depth on the rest is stable, so I'll keep watching it until the tech finishes the swap.
kofi: Jitter patch is staged. Once the tech's done at the rack, I'll roll it on the writers and Hana can diff the next save.
lucia: Once the tech reseats it I'll watch the leaf port for CRC and link flaps a while before we call that ToR clean.
```

> **>>> DECIDE AFTER THIS:** lucia: Once the tech reseats it I'll watch the leaf port for CRC and link flaps a while before we call that ToR clean.

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps (changed Fri Oct 9; previously every 500 steps)
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

---

## Row 128

**Today: Mon Sep 28** · #kestrel-run

**Team facts as of now**

- (nothing decided yet)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Sep 28 · #kestrel-run ---
dmitri: Kickoff thread for kestrel. Need start date, allocation, stability rules and data readiness all pinned down in here today. Who has blockers?
lucia: Fabric blocker from my side: two leaf switches in the new pod still flap under heavy all-reduce. Haven't isolated whether it's optics or firmware.
```

> **>>> DECIDE AFTER THIS:** lucia: Fabric blocker from my side: two leaf switches in the new pod still flap under heavy all-reduce. Haven't isolated whether it's optics or firmware.

**Team facts again**

- (nothing decided yet)

---

## Row 129

**Today: Mon Oct 5** · #harbor

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 5 · #harbor ---
nadia: Morning all. Want to line up the release and the paper this week. Who has the latest on contamination fixes and where compute stands?
marcus: I've got the contamination scan mostly done. A handful of tasks overlap with public repos, still checking licenses on the replacements before I post the list.
elena: On compute, the last full sweep ran clean overnight. I can slot the rerun once marcus's replacement list is settled.
yuki: Quick check before I lock the pass criteria section: is the harbor workshop paper submission deadline Oct 23? React 👍 if so.
(nadia reacted 👍 to yuki's message)
theo: Baselines table is still on the old task set. I'll regenerate once the replacements land, otherwise the numbers won't line up with the new items.
marcus: Two of the overlapping tasks are near-verbatim from a popular CLI repo. Leaning toward dropping those outright rather than rewriting them, since the solutions are easy to find.
felix: Release note for planning: the harbor release version is v1.2. It'll carry the contamination replacements once marcus's list is final, so the changelog stays in one place.
yuki: If marcus drops those two CLI tasks, I'll check the difficulty spread afterward. Don't want the replacements skewing easy and inflating pass rates.
marcus: Good point on difficulty. The replacement candidates I've pulled so far are mostly single-file fixes, so they'd probably skew easy. I'll look for some multi-file ones.
nadia: Separate thing: we still need someone to own the eval compute reservation for the rerun. Who's taking that on?
elena: I'll grab it.
```

> **>>> DECIDE AFTER THIS:** elena: I'll grab it.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2

---

## Row 130

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
lucia: Pulled IB port counters overnight. One leaf uplink is showing creeping symbol errors, still below the alarm line. Keeping an eye on it.
wen: Vendor folks want to come onsite and look at the cluster. Dmitri, you want to be in the room for that or should I just handle it?
```

> **>>> DECIDE AFTER THIS:** wen: Vendor folks want to come onsite and look at the cluster. Dmitri, you want to be in the room for that or should I just handle it?

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

---

## Row 131

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
alex: Thanks Oli. Frida, could you also jot down which partners asked about per-thread muting? I'd like to quote them in the FAQ review.
frida: Yep, will do. Two of them mentioned it so far, I'll add names and what they said to my notes doc.
olavo: For the waitlist email, should I mention agents can be muted? Feels like a good trust line, but don't want to overpromise on per-thread.
alex: Quick question on muting: does a muted agent still read the channel for memory, or fully stop? Partners will ask.
aj: Mute as built only silences posting and notifications. Memory indexing still runs on the channel. A true stop-reading option would be a separate flag.
alex: Random q while we're on the waitlist email: who's actually sending it Thursday? Olavo, is that you, or does Sara hit send?
frida: Another partner question: if they remove an agent from the workspace, does its shared memory get wiped or stay searchable?
aj: Frida, on removal: I'd need to check how memory is keyed. If it's tied to the agent identity, deleting the agent could orphan entries.
frida: Thanks AJ. The partner asking is swapping agents mid-project, so they'd want the old one's memory to carry over to the new one.
alex: For the swap case, would partners expect memory to carry over automatically, or a manual "transfer memory" step when they replace an agent?
aj: Automatic carry-over gets tricky. Old memory includes entries from channels the new agent was never in, so permissions would have to be re-checked.
frida: I think that partner would be fine with a manual transfer step, as long as it shows which channels' memory comes across and what gets skipped.
olavo: Draft FAQ answer for the memory question: "Agents read channel and DM history to build team memory, so they pick up context without anyone re-explaining it. You can mute an agent per channel anytime." Thoughts?
oli: Found a bug in staging: a muted agent still shows the typing indicator in the channel. Filing a ticket, ENG-412.
alex: For the muted state, I'm thinking a small bell-slash icon next to the agent's name in the sidebar. Does the member list already expose that flag?
```

> **>>> DECIDE AFTER THIS:** alex: For the muted state, I'm thinking a small bell-slash icon next to the agent's name in the sidebar. Does the member list already expose that flag?

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

## Row 132

**Today: Mon Oct 12** · #acct-northwind

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Gabe to load-test Northwind's workload at their full rate limit (check point: Wed Oct 14)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 12 · #acct-northwind ---
darnell: Weekly pipeline note: Northwind is still our biggest renewal this quarter. Their finance team is pushing back on the discount, so let's get aligned before anything goes back to them. Rachel, where are we on the order form draft?
keiko: Their clinical informatics team asked again whether the newer models will be available on their current setup. Worth having an answer ready.
gabe: On the newer models question: depends which endpoints they're calling today. I can check their usage pattern and see what migration would look like.
rachel: Draft is mostly there, still waiting on Tomas for the pricing block. Finance wants to see the discount reasoning, not just a number.
tomas: Pricing block is in progress. I'll lay out the discount rationale line by line so finance can trace how we got there.
ines: Before the order form goes out, I'd like to see how finance's discount ask interacts with the data terms. Those clauses sometimes get traded away quietly.
tomas: Going with my suggestion from Thursday, Oct 8, on the Northwind discount. I'm building the pricing block on that basis now.
rachel: Tomas, which suggestion do you mean? Finance will ask which number we're defending, so I want it spelled out in the pricing block.
darnell: Whatever number we defend, I want to know what Northwind gives in return. Longer term, bigger commit, or a reference?
keiko: On the last call they hinted at rolling this out to more departments. That might be our opening for a bigger commit.
rachel: Working from the new 15% off list. I'll frame it for Northwind alongside the department rollout and a bigger commit, rather than leading with the number. Keiko, can you sound out their sponsor first?
keiko: Happy to. Their sponsor responds better to a quick call than email, so I'll pitch it as rollout planning, not pricing.
gabe: If more departments join, I'd like to know their use cases. Clinical notes versus patient messaging changes the integration and traffic picture.
keiko: From what I've heard, one group wants clinical note summaries and another wants patient portal messaging. I'll confirm on the sponsor call.
ines: Patient portal messaging is a different risk profile than note summaries. If those departments join, the data terms should cover both use cases explicitly.
```

> **>>> DECIDE AFTER THIS:** ines: Patient portal messaging is a different risk profile than note summaries. If those departments join, the data terms should cover both use cases explicitly.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Gabe to load-test Northwind's workload at their full rate limit (check point: Wed Oct 14)

---

## Row 133

**Today: Mon Oct 12** · #acct-northwind

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
--- Tue Oct 6 · #acct-northwind ---
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
keiko: Their clinical informatics team asked again whether the newer models will be available on their current setup. Worth having an answer ready.
gabe: On the newer models question: depends which endpoints they're calling today. I can check their usage pattern and see what migration would look like.
```

> **>>> DECIDE AFTER THIS:** gabe: On the newer models question: depends which endpoints they're calling today. I can check their usage pattern and see what migration would look like.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Gabe to load-test Northwind's workload at their full rate limit (check point: Wed Oct 14)

---

## Row 134

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
aj: Keeping agents out of a channel is mostly a read-permission question for us. Does the partner want admins to set it, or any channel member?
frida: Good question, I'll ask. My guess is admins, since it was an HR-type channel, but I'll confirm with them.
frida: Ha yes, they told me last week the agent summarized a messy client thread before anyone asked. I'll get them to retell it 😄
oli: frida AND-341 is mine now, send the details to me. Ask if they saw both posts land at the same moment.
alex: For the 'keep agents out' ask, should the channel show some marker so members know agents can't see it? Otherwise people might assume the agent is reading.
```

> **>>> DECIDE AFTER THIS:** alex: For the 'keep agents out' ask, should the channel show some marker so members know agents can't see it? Otherwise people might assume the agent is reading.

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

## Row 135

**Today: Mon Oct 12** · #acct-northwind

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Gabe to load-test Northwind's workload at their full rate limit (check point: Wed Oct 14)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 12 · #acct-northwind ---
ines: Before the order form goes out, I'd like to see how finance's discount ask interacts with the data terms. Those clauses sometimes get traded away quietly.
tomas: Going with my suggestion from Thursday, Oct 8, on the Northwind discount. I'm building the pricing block on that basis now.
rachel: Tomas, which suggestion do you mean? Finance will ask which number we're defending, so I want it spelled out in the pricing block.
darnell: Whatever number we defend, I want to know what Northwind gives in return. Longer term, bigger commit, or a reference?
keiko: On the last call they hinted at rolling this out to more departments. That might be our opening for a bigger commit.
rachel: Working from the new 15% off list. I'll frame it for Northwind alongside the department rollout and a bigger commit, rather than leading with the number. Keiko, can you sound out their sponsor first?
keiko: Happy to. Their sponsor responds better to a quick call than email, so I'll pitch it as rollout planning, not pricing.
gabe: If more departments join, I'd like to know their use cases. Clinical notes versus patient messaging changes the integration and traffic picture.
keiko: From what I've heard, one group wants clinical note summaries and another wants patient portal messaging. I'll confirm on the sponsor call.
ines: Patient portal messaging is a different risk profile than note summaries. If those departments join, the data terms should cover both use cases explicitly.
gabe: Patient messaging traffic tends to spike during clinic hours, so I'd want to sanity-check their headroom before we pitch a wider rollout.
darnell: Good point, Gabe. If headroom is tight, that's a fair upsell angle too. Want the rollout story to include capacity, not just price.
gabe: I can pull their traffic by hour from the last few weeks and see how close they run to the ceiling.
tomas: Order form draft pasted below. Pricing block reads 18% off list, with the rationale itemized line by line underneath so finance can trace each step.

Pricing: Northwind Health API usage, 18% off list. Rationale schedule attached as Exhibit B.
keiko: Clinical informatics also asked if they can pilot the patient messaging use case in a sandbox before committing other departments. Worth planning for.
```

> **>>> DECIDE AFTER THIS:** keiko: Clinical informatics also asked if they can pilot the patient messaging use case in a sandbox before committing other departments. Worth planning for.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Gabe to load-test Northwind's workload at their full rate limit (check point: Wed Oct 14)

---

## Row 136

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
wen: If the flap test stalls loaders on C, I can drain those nodes into the spare pool during the run. Which leaf ports are affected?
lucia: Affected ports are on the C leaf, the two uplinks I reseated and recabled. I'll post exact port IDs once counters settle.
mateo: yeah the app has a pickup time picker, I'll set it for when your call wraps. want the usual or something different?
hana: I'll add a monitor on resume that logs hash mismatch counts per rank, so a tripped check shows up on the dashboard and not just in logs.
kofi: Per-rank mismatch counts on the dashboard works for me. I'll emit the hash result as a structured log line so your monitor can scrape it.
lucia: the usual works. the spicy one with extra greens. my call wraps around the half hour, probably runs over though, IB flap again
mateo: Loader side I'll tag reads from C nodes in the metrics so stalls show up per node, not just aggregate throughput.
lucia: Cable swap on the second uplink done. Retrain count on that port is flat so far, watching optics levels on the C leaf.
mateo: ha, IB flap again. I'll pad the pickup a bit so it doesn't sit. I'll grab it and drop it at your desk.
kofi: Patch is up for review. Injected short write on a writer rank now retries instead of flipping the shard to complete. Hash lines look right in the structured log.
hana: I'll review the patch. Want to confirm the retry path doesn't stall the writer rank and skew step time during saves.
kofi: Retry runs on the flush thread, so the training step shouldn't block. I'll capture step time during the injected short write and attach it to the review.
lucia: Optics levels on the C leaf look stable so far. Still no clean window to say firmware's safe, so it stays parked.
hana: For storage sizing I'm assuming a checkpoint every 1,000 steps. Mateo, can you confirm the tier has headroom for that plus the per-shard hash sidecars?
lucia: Who should C leaf flap alerts page while firmware is parked? Right now they land in my queue only, nobody else.
```

> **>>> DECIDE AFTER THIS:** lucia: Who should C leaf flap alerts page while firmware is parked? Right now they land in my queue only, nobody else.

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 137

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
theo: I'll put the censored-dot marker in the plot legend too, so the caption doesn't have to carry all of it.
elena: One thing for the plot: the looping runs cluster on a couple of repos with flaky fixtures. Might be worth a sentence in the analysis section.
```

> **>>> DECIDE AFTER THIS:** elena: One thing for the plot: the looping runs cluster on a couple of repos with flaky fixtures. Might be worth a sentence in the analysis section.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,140 items (changed Mon Oct 19; previously 1,200 items)
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 138

**Today: Wed Sep 16** · #gtm

**Team facts as of now**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per human seat, agents free (changed Wed Sep 16; previously $12 per seat, agent actions metered)
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: Olavo to send the press kit to the embargoed reporters (check point: Fri Sep 18)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Wed Sep 16 · #gtm ---
oli: for the screenshot, shoot it on the prod build. Staging still shows the placeholder avatar on agent profile cards.
frida: Good to know Oli, I'll ask the partner if they can grab it on prod, or if I should screen-share and capture it myself 👍
aj: Also worth checking the screenshot doesn't show the memory panel sidebar, it lists recent recalls with channel names in it.
olavo: Quick commitment on my side: I'll send the press kit to the embargoed reporters by Fri Sep 18. Cropped screenshots go in once Frida clears the thread.
oli: fyi profile cards on prod render fine in dark mode too, if you want a dark variant for the wide header crop.
alex: Dark variant for the wide header could look great next to the pricing hero. Olavo, want both light and dark in the kit?
olavo: Both, yes! Light for socials, dark for the wide header. Alex, can you export them with a bit of padding so the crop doesn't feel tight?
alex: Sure Olavo, I'll export both with extra padding. Want the square one centered on the profile card or on the reply?
olavo: Square one centered on the profile card, I think. The reply text gets tiny at that size anyway 🙂
frida: Partner replied, they're fine grabbing it on prod. They asked if the square crop could skip the channel sidebar too, just the card.
alex: Yep, square crop can be just the card, no sidebar. I'll mask anything around it so nothing leaks in at the edges.
frida: Perfect, I'll pass that to the partner. They also asked if we want a short quote from their team lead for the post, I'll check.
olavo: Ooh a quote from their team lead would be great for the post. Something short about the agent joining threads on its own 🙌
frida: Will do. I'll ask them to keep the quote to a sentence or two, and mention the agent picking up threads without a tag.
alex: Once the partner's quote comes in I can mock the post layout with it, so we see how it sits next to the screenshot.
```

> **>>> DECIDE AFTER THIS:** alex: Once the partner's quote comes in I can mock the post layout with it, so we see how it sits next to the screenshot.

**Team facts again**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per human seat, agents free (changed Wed Sep 16; previously $12 per seat, agent actions metered)
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: Olavo to send the press kit to the embargoed reporters (check point: Fri Sep 18)

---

## Row 139

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
marcus: Grepped the removed-ids file, and the build-loop task isn't in it. Safe to keep in the transcript figure. File's up in the shared folder now.
theo: Pulled the file, joining on id now. The upstream repo column will be handy for Felix's footnote. Regenerating the plateau figure after.
yuki: Once the figure regenerates, I'll check whether the plateau still shows up in the web-app slice or if it was mostly the forked tasks.
felix: Thanks, that works. I'll ask them about the projector and whether there's a blank wall or a screen we can use.
```

> **>>> DECIDE AFTER THIS:** felix: Thanks, that works. I'll ask them about the projector and whether there's a blank wall or a screen we can use.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,140 items (changed Mon Oct 19; previously 1,200 items)
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)
- open item: Nadia to decide whether the 3-shot results go in the paper (check point: Tue Oct 20 paper sync)

---

## Row 140

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

> **>>> DECIDE AFTER THIS:** wen: Overlaying the map on the ECC-flagged nodes. Some of them sit behind those same leaves, so maybe not coincidence.

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 141

**Today: Tue Oct 6** · #acct-northwind

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list

**Recent messages** (oldest first; the last one is the decision message)

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
darnell: Worth getting ahead of procurement on this one. If their big ask comes in early, I'd rather we already have a view on where we'd hold.
ines: Before we settle on a negotiating position, I'd like to see what they redlined last time. Their legal team tends to reopen data terms.
keiko: Their clinical informatics lead also hinted procurement may bring in a new reviewer this cycle. I'll try to find out who before the next call.
```

> **>>> DECIDE AFTER THIS:** keiko: Their clinical informatics lead also hinted procurement may bring in a new reviewer this cycle. I'll try to find out who before the next call.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list

---

## Row 142

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
gabe: Fair. Caching keeps the prompt text identical, so behavior shouldn't shift. I can diff outputs on the de-identified forms before and after to show her.
gabe: Will do. I'll frame jitter as spreading retries out so clients don't all hit at once. Keiko can drop it in as a friendly tip.
rachel: Before/after diff on the forms would make a solid slide for the renewal deck. Customers like seeing proof, not promises.
rachel: Quick flag so nobody mixes them up: Northwind Logistics is a separate customer and renews Nov 15. Keep their numbers out of the Northwind Health deck.
gabe: On missing fields: yes. Have the model return a list of empty required fields in structured output, and the UI can highlight them for staff.
keiko: That's a clean answer, thanks. I'll pass it to their ops lead. She'll probably ask if staff can override a flagged field.
gabe: Yes, override is easy. I'd log which fields staff overrode though, so we can see where the model keeps misfiring.
keiko: Good call on logging overrides. Their ops lead will want a weekly view of the misfires, so staff feel heard rather than monitored.
gabe: A weekly misfire view is easy once overrides are logged. I can sketch a simple dashboard grouped by field type for her.
rachel: Great. Send it over when it's ready and I'll pass it to Keiko with a short intro. Keep the tone light.
keiko: A dashboard sketch would land well. She's also asking whether the misfire view can be shared with her floor supervisors, not just her.
gabe: Sharing with supervisors is fine technically. I'd just scope it by role so they only see their own floor's fields, nothing patient-level.
tomas: Looping in pricing for a moment: for the renewal, I'd float 15% off list as a possible discount. Purely a suggestion at this stage; nothing is decided, and it needs Darnell's sign-off.
gabe: Will do. I'll add a tiny test harness too, so their devs can simulate a 429 and watch the retries spread out.
rachel: Noted, Tomas. Darnell, let me know when you've had a look so I can build the renewal deck around it.
```

> **>>> DECIDE AFTER THIS:** rachel: Noted, Tomas. Darnell, let me know when you've had a look so I can build the renewal deck around it.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Gabe to load-test Northwind's workload at their full rate limit (check point: Wed Oct 14)

---

## Row 143

**Today: Wed Sep 30** · #infra

**Team facts as of now**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Wed Sep 30 · #infra ---
lucia: Firmware rollout on the IB leaf switches is staged but not pushed. Seeing a few flapping links on rack group C that I want to look at first.
```

> **>>> DECIDE AFTER THIS:** lucia: Firmware rollout on the IB leaf switches is staged but not pushed. Seeing a few flapping links on rack group C that I want to look at first.

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 144

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
keiko: Walkthrough would help. Their platform lead mentioned the new CTO is big on clinical safety, so I'd frame it around that.
keiko: Perfect. I'll nudge their admin again tomorrow morning so we're not waiting on her too long.
ines: If he's focused on clinical safety, expect him to ask about logging and how model outputs get reviewed. I'd want our answers consistent across the deck and contract.
gabe: I can pull together a one-pager on how we handle output logging and what controls their team can set. Keeps the answers consistent with the deck.
rachel: Good. Keiko, when you talk to their platform lead, ask if the new CTO would take a short intro call before the QBR.
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
```

> **>>> DECIDE AFTER THIS:** keiko: Their ops team mentioned the morning rush is when the clinics all check patients in at once, so that's what worries them.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

---

## Row 145

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
--- Mon Oct 12 · #kestrel-run ---
kofi: If it's incast on that leaf, I can stagger the writer nodes' flush start so they don't all burst at once. Want to see the counters first.
lucia: Port counters show egress buffer spikes on the writer uplinks right at flush start. Looks like incast. Staggering would probably flatten it.
kofi: Okay, I'll add a per-node jitter on the flush start so the writers spread out. Hana, watch step time on the next save for any residual dip.
mateo: Unrelated to the flush, but I'm seeing IB link flaps on a couple of the dataloader nodes in my logs. Who's on call for fabric incidents today?
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
```

> **>>> DECIDE AFTER THIS:** mateo: Starting the drain on those two loader nodes now. Rebalancing dataloader workers onto the remaining hosts, will watch prefetch queue depth as it shifts.

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps (changed Fri Oct 9; previously every 500 steps)
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

---

## Row 146

**Today: Tue Oct 6** · #acct-northwind

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30

**Recent messages** (oldest first; the last one is the decision message)

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

> **>>> DECIDE AFTER THIS:** tomas: Yes, that is correct.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30

---

## Row 147

**Today: Wed Oct 7** · #harbor-evals

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items

**Recent messages** (oldest first; the last one is the decision message)

```
--- Wed Oct 7 · #harbor-evals ---
nadia: Cached images are a good idea. Worth a sentence in the paper's methods section so reviewers know installs aren't counted against the model.
marcus: Cached images also help the contamination check. I can diff the pinned dependency versions against the repos' original commit dates and catch anything that predates the snapshots.
theo: empty topology would explain it. Does the parser drop the label when the node pool name has a hyphen? I hit that once on my branch.
yuki: Good, but dependency pinning only catches so much. Might also be worth checking whether any fix commits are quoted verbatim in public issue threads, since that leaks the answer too.
marcus: Good point on issue threads. I can grep the public trackers for long verbatim diff snippets and flag any items where the fix text shows up before the snapshot.
theo: If the issue-thread grep flags items, I can rerun those separately and see whether baseline scores on them look inflated compared to the clean ones.
yuki: If flagged items do inflate baseline scores, that's a nice contamination figure for the paper. Inflated-vs-clean gap, plotted per slice, with intervals.
marcus: License review for the scraped repos is done. Three repos got excluded over license terms, so I'll update the backfill list and send Felix the cleaned source/license tags for the manifest.
elena: First cached image is built for the messiest monorepo item. Installs barely register now. Trying the Python repos with native extensions next.
theo: Split the import-error bucket out of the multi-file plots. Spread tightens a lot without it. Will rerun properly once more cached images land.
elena: that's it, the stuck jobs all target pools with hyphens in the name. parser truncates at the first one. patching the regex locally to confirm.
nadia: For the paper, let's call that bucket "environment failures" rather than model errors. Reviewers will read it more kindly, and it's more accurate.
yuki: Fine by me. Should we report environment failures as a separate rate per slice, so readers see how much each slice is affected?
theo: Yes, per-slice rate works. I'll add it to the results table. Also, I put in the draft that the release gate is 75% pass@1, so the environment-failure rate sits right next to it.
theo: nice, that matches what I saw on my branch. once the patch works, add a test with a hyphenated pool name so it doesn't regress.
```

> **>>> DECIDE AFTER THIS:** theo: nice, that matches what I saw on my branch. once the patch works, add a test with a hyphenated pool name so it doesn't regress.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items

---

## Row 148

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
alex: Should the agent ask before posting in a thread it wasn't invited to? Like a small 'want me to weigh in?' prompt instead of a summary.
oli: Prompt makes sense for memory-sourced joins at least. Keyword ones are closer to a direct mention, so maybe those can stay as is. Needs a gate in the join path either way.
sara: On the prompt question, there's a bigger one behind it. We'll decide whether agents may DM a human first, without being asked, at the Mon Sep 21 design review. Hold the gating design until then.
frida: Will do! They're pretty chatty on Slack-style stuff, so I'll ask about naming and whether they'd prefer a call or video.
oli: ok, so I'll keep digging on the root cause in the join path but not touch the gate itself. Will log the trigger breakdown on the board.
frida: Heard back from the design partner: the summary was visible to everyone in the hiring thread, not just the poster. They want to know if agents can be kept out of certain channels entirely.
olavo: Perfect, video's better if they're okay with it, reporters can grab a screenshot of the workspace. Also ask if they have a fav agent moment to share 😄
frida: Separate thing: a design partner hit the double-posting bug again this morning. I'll ping AJ with the details since AND-341 is his.
aj: Keeping agents out of a channel is mostly a read-permission question for us. Does the partner want admins to set it, or any channel member?
frida: Good question, I'll ask. My guess is admins, since it was an HR-type channel, but I'll confirm with them.
frida: Ha yes, they told me last week the agent summarized a messy client thread before anyone asked. I'll get them to retell it 😄
oli: frida AND-341 is mine now, send the details to me. Ask if they saw both posts land at the same moment.
alex: For the 'keep agents out' ask, should the channel show some marker so members know agents can't see it? Otherwise people might assume the agent is reading.
aj: Marker makes sense, and it should come from the same permission flag so it can't drift from what the agent can actually read.
olavo: random q from the launch post side: can I say agents only join threads when relevant, or is that overselling given the hiring thread thing? 😅
```

> **>>> DECIDE AFTER THIS:** olavo: random q from the launch post side: can I say agents only join threads when relevant, or is that overselling given the hiring thread thing? 😅

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

## Row 149

**Today: Mon Oct 12** · #acct-northwind

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
--- Tue Oct 6 · #acct-northwind ---
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
keiko: Their clinical informatics team asked again whether the newer models will be available on their current setup. Worth having an answer ready.
```

> **>>> DECIDE AFTER THIS:** keiko: Their clinical informatics team asked again whether the newer models will be available on their current setup. Worth having an answer ready.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Gabe to load-test Northwind's workload at their full rate limit (check point: Wed Oct 14)

---

## Row 150

**Today: Mon Oct 12** · #acct-northwind

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Gabe to load-test Northwind's workload at their full rate limit (check point: Wed Oct 14)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 12 · #acct-northwind ---
tomas: Going with my suggestion from Thursday, Oct 8, on the Northwind discount. I'm building the pricing block on that basis now.
rachel: Tomas, which suggestion do you mean? Finance will ask which number we're defending, so I want it spelled out in the pricing block.
darnell: Whatever number we defend, I want to know what Northwind gives in return. Longer term, bigger commit, or a reference?
keiko: On the last call they hinted at rolling this out to more departments. That might be our opening for a bigger commit.
rachel: Working from the new 15% off list. I'll frame it for Northwind alongside the department rollout and a bigger commit, rather than leading with the number. Keiko, can you sound out their sponsor first?
keiko: Happy to. Their sponsor responds better to a quick call than email, so I'll pitch it as rollout planning, not pricing.
gabe: If more departments join, I'd like to know their use cases. Clinical notes versus patient messaging changes the integration and traffic picture.
keiko: From what I've heard, one group wants clinical note summaries and another wants patient portal messaging. I'll confirm on the sponsor call.
ines: Patient portal messaging is a different risk profile than note summaries. If those departments join, the data terms should cover both use cases explicitly.
gabe: Patient messaging traffic tends to spike during clinic hours, so I'd want to sanity-check their headroom before we pitch a wider rollout.
darnell: Good point, Gabe. If headroom is tight, that's a fair upsell angle too. Want the rollout story to include capacity, not just price.
gabe: I can pull their traffic by hour from the last few weeks and see how close they run to the ceiling.
tomas: Order form draft pasted below. Pricing block reads 18% off list, with the rationale itemized line by line underneath so finance can trace each step.

Pricing: Northwind Health API usage, 18% off list. Rationale schedule attached as Exhibit B.
keiko: Clinical informatics also asked if they can pilot the patient messaging use case in a sandbox before committing other departments. Worth planning for.
ines: On the sandbox pilot: will they use real patient messages or synthetic ones? That changes which terms apply during the trial.
```

> **>>> DECIDE AFTER THIS:** ines: On the sandbox pilot: will they use real patient messages or synthetic ones? That changes which terms apply during the trial.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Gabe to load-test Northwind's workload at their full rate limit (check point: Wed Oct 14)

---

## Row 151

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
marcus: Near-duplicate check is doable. I'll run fuzzy matching on the solution diffs against the fork and gist dumps, then flag anything above a similarity cutoff.
yuki: Updating the eval config now to point at v1.3. Patched tasks get fresh runs, the rest can reuse saved traces. I'll flag which is which in the config.
elena: For the fresh runs, which scaffolds are slowest? I'd like to queue those first so they don't get stuck behind the quick ones.
theo: The multi-file refactor scaffolds are slowest by far, especially the one with the long tool-use loops. Those should go first in the queue.
elena: Got it, I'll put the refactor ones at the front. The long tool-use loops tend to hit timeouts, so I'll bump the per-run limit for those.
theo: Heads up, the long tool-use scaffold also eats a lot of tokens per run, so the logs get huge. Might want to check disk before queueing.
elena: Good call on disk. I'll check free space on the shared volume and point the big logs at scratch before queueing anything.
marcus: Fuzzy match on the fork dumps is running. A few gist hits look like reformatted copies, so whitespace and renamed variables won't fool it.
theo: Ok, committing: I'll rerun all baselines on harbor v1.3 and have them done by Fri Oct 16. Rescoring the unpatched tasks from saved traces, fresh runs only for the patched ones.
marcus: Also noticing some flagged tasks share a helper file across repos, so dropping one may orphan others. I'll list those dependencies for Felix.
felix: Helpful, Marcus. Send the helper-file dependencies as a list per task and I'll check which ones break when I cut the manifest.
yuki: Once Marcus's helper-file list is in, I'd like to check whether any orphaned tasks lose their only test fixture. Those would need a re-spec, not just removal.
marcus: Yuki, good point. I'll tag any task whose only fixture lives in a shared helper, so you can see which ones need a re-spec before Felix cuts.
nadia: Results table caption reads "harbor v1.2, pass@1 across all scaffolds". Theo, just drop the rerun numbers into that table when they're done, so the wording doesn't change.
elena: Disk check done: shared volume has room, but I'm still routing the refactor scaffold logs to scratch just in case.
```

> **>>> DECIDE AFTER THIS:** elena: Disk check done: shared volume has room, but I'm still routing the refactor scaffold logs to scratch just in case.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 152

**Today: Mon Sep 14** · #launch

**Team facts as of now**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Sep 14 · #launch ---
aj: Admins should be able to attach them from member settings, I think. Need to confirm the seeded role doesn't block it on those older ones.
olavo: ok so with the new timing I'm redoing the email schedule tonight. will post a fresh send plan here once it's drafted 📝
oli: fyi the two open onboarding tickets are both around the add-agents step, one's a flaky state on the skip button. will ping when it's stable.
alex: if the skip button is flaky, should the add-agents step stay skippable at all? Might be cleaner to make it required for admins, just thinking out loud
olavo: catching up, can the waitlist email still go out the day before Sep 17 like we planned? want to lock the send slot 📬
frida: another partner question: can admins mute agents per channel? They're nervous about agents jumping into threads untagged 🤔
aj: Per-channel mute isn't something I can confirm yet. Need to check whether agent permissions are scoped per channel or only per workspace.
oli: repro for the skip button: go back from the next step and the state resets, so skip shows enabled when it shouldn't. Tracing it.
alex: does the reset also hit people who go back after already adding an agent? Might show an empty list again 🤔
alex: quick q, who actually sends the waitlist email? I need to know who to give the header image to 📬
olavo: me! send the header image my way, I'm sending the waitlist email 📬
alex: Sending the header image over now. I made a dark and a light version, so pick whichever fits the email template 🎨
frida: Another partner asked if there's a visible indicator when an agent joins a thread untagged. Would calm the nerves a bit 🙂
alex: Could be a small badge or avatar ring on the message when an agent joins untagged. I can mock a couple options 🎨
aj: Update: the forwarded-DM permission check is merged. Forwarding a DM into a channel now checks the original DM's access first. That one's done.
```

> **>>> DECIDE AFTER THIS:** aj: Update: the forwarded-DM permission check is merged. Forwarding a DM into a channel now checks the original DM's access first. That one's done.

**Team facts again**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

---

## Row 153

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
--- Mon Oct 12 · #kestrel-run ---
hana: Loss and grad-norm dashboards are live. I'm also tracking per-rank step time so a slow rank shows up before MFU dips.
mateo: Dataloader workers are warm and prefetch queues look full. Should be smooth on the first few batches, no stalls expected from the data side.
dmitri: Good. Kicking off now. Shout the second you see a rank lagging, don't wait for it to show up in MFU.
hana: First steps are in. Per-rank step time looks tight so far, no rank trailing the pack. Still early though.
wen: Heads up, separate from kestrel: the kestrel-mini ablation run starts Oct 14. Different run, I'll keep its nodes carved out so it doesn't touch this allocation.
kofi: First async flush is kicking off now. Writer queue depth looks normal, nothing backing up behind the flush yet.
lucia: Seeing a brief NCCL all-reduce latency bump on one leaf switch during the flush. Still within normal spread, keeping an eye on it.
kofi: Flush finished clean on my side. Lucia, does that latency bump line up with the writer burst hitting the fabric, or is it unrelated?
lucia: Likely correlated. The bump landed on the leaf where the writer nodes uplink. Pulling port counters to see if it was incast on that leaf.
kofi: If it's incast on that leaf, I can stagger the writer nodes' flush start so they don't all burst at once. Want to see the counters first.
lucia: Port counters show egress buffer spikes on the writer uplinks right at flush start. Looks like incast. Staggering would probably flatten it.
kofi: Okay, I'll add a per-node jitter on the flush start so the writers spread out. Hana, watch step time on the next save for any residual dip.
mateo: Unrelated to the flush, but I'm seeing IB link flaps on a couple of the dataloader nodes in my logs. Who's on call for fabric incidents today?
hana: Will do, Kofi. I've tagged the first flush window in the step-time panel so I can diff it against the next save once jitter's in.
wen: Pulling per-node ECC and thermal counters across the allocation. A throttling GPU would show up as a slow rank before anything else.
```

> **>>> DECIDE AFTER THIS:** wen: Pulling per-node ECC and thermal counters across the allocation. A throttling GPU would show up as a slow rank before anything else.

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps (changed Fri Oct 9; previously every 500 steps)
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

---

## Row 154

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
marcus: Histogram's rough but promising: reformatted gist copies bunch up at the top, and generic argparse-style boilerplate lookalikes sit well below with a clear dip between.
yuki: That dip is exactly what we want. Can you overlay the borderline cases on the histogram? I'd like to see where the ambiguous ones fall.
marcus: Sure, I'll mark the borderline ones in a different color. A few are fixtures copied from a popular tutorial repo, so they might land near the dip.
yuki: Tutorial-repo fixtures are a good edge case. If they sit near the dip, I'd say describe them separately in the paper rather than force them into either bucket.
marcus: I'll check commit dates on those tutorial fixtures. If the tutorial repo predates the task repos, that changes how we frame them.
```

> **>>> DECIDE AFTER THIS:** marcus: I'll check commit dates on those tutorial fixtures. If the tutorial repo predates the task repos, that changes how we frame them.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 155

**Today: Tue Sep 8** · #launch

**Team facts as of now**

- public launch (date): Sep 17
- Series A raise (amount): $20M

**Recent messages** (oldest first; the last one is the decision message)

```
--- Tue Sep 8 · #launch ---
sara: ok team, launch kickoff. I'm going to lock the date, the raise announcement, pricing and who owns what for launch week. Read along, shout if something's off.
alex: reading along 👀 quick q: are we showing the agent-as-member idea in the onboarding flow at launch, or keeping that for after?
frida: +1 to Alex's q. Two design partners got lost on day one because they didn't realize the agent shows up in the member list.
oli: Agent already has its own member entry in the runtime, so showing it in onboarding is just a UI change. No backend work needed.
alex: nice, then I can mock it as a pinned card in the welcome step. should the agent introduce itself there or stay quiet until tagged?
sara: Locking the date first: public launch is Sep 17. Alex, agent introduces itself in the welcome card, yes. Keep it short, one line.
alex: perfect, one line it is. I'll draft a couple of intro variants and drop them here for a vibe check 🙌
frida: Happy to test the intro variants with a couple of design partners too, they'll give honest reactions 😄
olavo: quick check for the launch post draft: Series A raise is $20M, right? react 👍 if so and I'll lock it in
(sara reacted 👍 to olavo's message)
oli: fyi the member list currently sorts agents below humans alphabetically. might want to pin the agent higher for new workspaces, ticket coming
alex: good catch Oli. pinning the agent up top in the member list would fit with the welcome card too, I'll sketch both together 🙂
sara: Next up: who's taking the launch waitlist email? Need one owner for it.
olavo: I'll grab it 🙌
```

> **>>> DECIDE AFTER THIS:** olavo: I'll grab it 🙌

**Team facts again**

- public launch (date): Sep 17
- Series A raise (amount): $20M

---

## Row 156

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
aj: Keeping agents out of a channel is mostly a read-permission question for us. Does the partner want admins to set it, or any channel member?
```

> **>>> DECIDE AFTER THIS:** aj: Keeping agents out of a channel is mostly a read-permission question for us. Does the partner want admins to set it, or any channel member?

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

## Row 157

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
gabe: Will do. I'll frame jitter as spreading retries out so clients don't all hit at once. Keiko can drop it in as a friendly tip.
rachel: Before/after diff on the forms would make a solid slide for the renewal deck. Customers like seeing proof, not promises.
rachel: Quick flag so nobody mixes them up: Northwind Logistics is a separate customer and renews Nov 15. Keep their numbers out of the Northwind Health deck.
gabe: On missing fields: yes. Have the model return a list of empty required fields in structured output, and the UI can highlight them for staff.
keiko: That's a clean answer, thanks. I'll pass it to their ops lead. She'll probably ask if staff can override a flagged field.
gabe: Yes, override is easy. I'd log which fields staff overrode though, so we can see where the model keeps misfiring.
keiko: Good call on logging overrides. Their ops lead will want a weekly view of the misfires, so staff feel heard rather than monitored.
gabe: A weekly misfire view is easy once overrides are logged. I can sketch a simple dashboard grouped by field type for her.
rachel: Great. Send it over when it's ready and I'll pass it to Keiko with a short intro. Keep the tone light.
keiko: A dashboard sketch would land well. She's also asking whether the misfire view can be shared with her floor supervisors, not just her.
gabe: Sharing with supervisors is fine technically. I'd just scope it by role so they only see their own floor's fields, nothing patient-level.
tomas: Looping in pricing for a moment: for the renewal, I'd float 15% off list as a possible discount. Purely a suggestion at this stage; nothing is decided, and it needs Darnell's sign-off.
gabe: Will do. I'll add a tiny test harness too, so their devs can simulate a 429 and watch the retries spread out.
rachel: Noted, Tomas. Darnell, let me know when you've had a look so I can build the renewal deck around it.
keiko: Their ops lead is also curious whether the missing-field flags could show a short reason, so staff know why something got flagged.
```

> **>>> DECIDE AFTER THIS:** keiko: Their ops lead is also curious whether the missing-field flags could show a short reason, so staff know why something got flagged.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Gabe to load-test Northwind's workload at their full rate limit (check point: Wed Oct 14)

---

## Row 158

**Today: Thu Sep 10** · #eng

**Team facts as of now**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Thu Sep 10 · #eng ---
oli: Starting the launch-readiness checklist for the agent runtime. Three open items: DM permissions, the double-posting bug, memory store under load. Want status on each before standup.
```

> **>>> DECIDE AFTER THIS:** oli: Starting the launch-readiness checklist for the agent runtime. Three open items: DM permissions, the double-posting bug, memory store under load. Want status on each before standup.

**Team facts again**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

---

## Row 159

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
felix: Anyone have strong feelings on the offsite venue? I'm leaning toward the lake house over the downtown coworking space. Yuki, you looked at both, right?
nadia: Thinking the appendix should carry the per-category breakdowns and a couple of full agent transcripts. Too heavy for a workshop paper?
theo: Per-category tables are easy, I can export them straight from the results notebook. Full transcripts are the heavy part, some run absurdly long. Maybe trim to the interesting steps?
yuki: Yeah, I toured both. Lake house has way better space for whiteboarding, but the drive is long and wifi there was spotty.
yuki: Trimming is fine, but I'd keep one full transcript from the plateau tasks untouched. Readers will want to see the agent looping, not a cleaned-up version.
```

> **>>> DECIDE AFTER THIS:** yuki: Trimming is fine, but I'd keep one full transcript from the plateau tasks untouched. Readers will want to see the agent looping, not a cleaned-up version.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 160

**Today: Mon Oct 5** · #harbor

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 5 · #harbor ---
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
marcus: Rust build tool license came back permissive, so those candidates are usable. The fix touches the parser and config loader together, and the tests are deterministic.
elena: Rust builds will be slow in the sandbox. I'll check the image has the toolchain cached so timeouts don't masquerade as model failures.
```

> **>>> DECIDE AFTER THIS:** elena: Rust builds will be slow in the sandbox. I'll check the image has the toolchain cached so timeouts don't masquerade as model failures.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena

---

## Row 161

**Today: Mon Sep 28** · #kestrel-run

**Team facts as of now**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Sep 28 · #kestrel-run ---
dmitri: Decision: kestrel starts Oct 5. Lucia, get the optics vs firmware call made and fixed well before then. Wen, redo the allocation table around whatever the pod looks like once that's resolved.
lucia: Pulling optic transceiver serials on the flapping uplinks now. If they share a batch, that settles it. Will swap one and rerun all-reduce soak.
wen: Whichever way the optics call goes, I'll draft two allocation variants: one with the flapping racks drained, one assuming they come back clean.
dmitri: Quick check Wen: is the kestrel node allocation 2,048 nodes? Want that confirmed before the variants go out.
wen: yep, confirmed
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
```

> **>>> DECIDE AFTER THIS:** kofi: NVMe staging test looks good so far: flush overlaps the next forward pass, no stalls on the slow writer. Restore path from the new filesystem still untested.

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps

---

## Row 162

**Today: Mon Sep 14** · #launch

**Team facts as of now**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Tue Sep 8 · #launch ---
frida: My design partners liked having an "agent" label in the member list, so a small badge on messages might feel consistent 🙂
alex: Badge makes sense. I'll try a tiny "agent" tag next to the name, nothing loud, so long threads don't get noisy 🏷️
alex: Planning design freeze around the Sep 18 launch, so mocks for the pricing page, badge and thread-jump screenshot all land before then 🎨
olavo: Also for the launch post, we should probably have a short demo gif of the shared memory bit. People love seeing that 🎬
oli: For the memory gif, I can set up a clean demo workspace with seeded convos so it records without weird leftovers 🎬
frida: Nice, a clean demo workspace would help. A couple of design partners offered to share a quote or two for the launch post if useful 🙌
olavo: Love that, quotes from real teams will make the post. Can someone ask which partners are okay being named? Logos would be great too 🙌
--- Mon Sep 14 · #launch ---
olavo: morning all! weekend recap: launch post draft is at v3, waitlist email copy is mostly done, press kit needs final screenshots. waitlist is up a bunch since Friday too 🚀 want to lock send timing for the week today
frida: quick q from a design partner: do agents show up in their workspace member list by default, or do admins need to add them first?
alex: wait, are we sure about the default there? I think onboarding currently has an "add agents" step, but I'd have to check the latest flow. @oli @aj?
oli: default is agents are not auto-added, admin has to add them in onboarding. checking whether that changed in the latest build, will confirm in a bit
aj: If it's admin-add, worth noting the member list for existing beta workspaces might look different than fresh ones. I'll check how permissions get seeded on those.
frida: Thanks all! I'll tell them admins add agents for now. Also two partners asked if existing beta workspaces need to redo onboarding to get that step 🤔
olavo: good q for oli/aj. on my side, plan is waitlist email Wed night so it lands early, launch post goes live Sep 17 with the press kit, partner heads-up Tuesday. screenshots depend on the onboarding flow tho 👀
alex: For screenshots, should I grab them from a fresh workspace so the add-agents step shows? Or use a beta one that already has agents in the list?
```

> **>>> DECIDE AFTER THIS:** alex: For screenshots, should I grab them from a fresh workspace so the add-agents step shows? Or use a beta one that already has agents in the list?

**Team facts again**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

---

## Row 163

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
aj: Keeping agents out of a channel is mostly a read-permission question for us. Does the partner want admins to set it, or any channel member?
frida: Good question, I'll ask. My guess is admins, since it was an HR-type channel, but I'll confirm with them.
```

> **>>> DECIDE AFTER THIS:** frida: Good question, I'll ask. My guess is admins, since it was an HR-type channel, but I'll confirm with them.

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

## Row 164

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
--- Mon Oct 12 · #kestrel-run ---
lucia: Port counters show egress buffer spikes on the writer uplinks right at flush start. Looks like incast. Staggering would probably flatten it.
kofi: Okay, I'll add a per-node jitter on the flush start so the writers spread out. Hana, watch step time on the next save for any residual dip.
mateo: Unrelated to the flush, but I'm seeing IB link flaps on a couple of the dataloader nodes in my logs. Who's on call for fabric incidents today?
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
```

> **>>> DECIDE AFTER THIS:** lucia: Once the drain completes I'll send a tech to the rack for the transceiver. Keeping CRC counters on that ToR under watch in the meantime.

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps (changed Fri Oct 9; previously every 500 steps)
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

---

## Row 165

**Today: Mon Oct 5** · #harbor

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 5 · #harbor ---
felix: Yes, I'll make language a list instead of a single label. Then the Rust parser fix can carry both Rust and TOML, and Theo can group on either.
yuki: With language as a list, I'll report breakdowns by primary language only, so multi-label tasks don't get double counted in the paper tables.
theo: Primary-language only works for me. I'll flag in the table caption which tasks are multi-label so reviewers don't wonder why TOML never shows up.
elena: Fair warning, the eval jobs have more retries than I do at the gym. Rust timeouts are gonna be the worst offenders.
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
```

> **>>> DECIDE AFTER THIS:** marcus: Two of the Rust candidates look like they share a fixture directory, so I'll check they don't leak each other's expected outputs before they go in.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena

---

## Row 166

**Today: Fri Sep 18** · #eng

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
--- Fri Sep 18 · #eng ---
alex: For the 'keep agents out' ask, should the channel show some marker so members know agents can't see it? Otherwise people might assume the agent is reading.
aj: Marker makes sense, and it should come from the same permission flag so it can't drift from what the agent can actually read.
olavo: random q from the launch post side: can I say agents only join threads when relevant, or is that overselling given the hiring thread thing? 😅
oli: I'd skip 'only when relevant' for now. Memory-sourced joins misfire on stale threads. Something softer like 'can chime in' is safer.
olavo: Fair, 'can chime in' works for the post. Should I add a line about admins being able to keep agents out of channels, or too early?
olavo: Love that story, that's the quote I want. Ping me once they answer and I'll slot reporters in around their calendar 🙌
aj: I'd leave it out for now. We don't know yet who gets to set it, and the marker isn't designed. Don't want the post promising a feature that's still a question.
frida: Another partner asked whether the agent's summaries can be turned off per workspace. Adding it to my list of questions for them.
olavo: Got it, I'll keep the summaries toggle out of the post too. Draft is locked for review ahead of the Sep 17 launch, so anything uncertain stays out of the copy 👍
olavo: sorry, typo in my last msg: public launch is Sep 24, not Sep 17. Draft is still locked for review ahead of that.
frida: Will do. Also one partner asked if agents can tell which channels are private before they join, or only after. Adding to the list.
olavo: press kit is out to all six embargoed reporters, done ✅ will flag here if anyone replies with questions
aj: Re Frida's private-channel question: agents can only see channels they have read access to, so I'll check what the join path does with membership first.
alex: For the bug bash, I'll add a scenario for joining a private channel to the checklist so we catch it in the UI too.
frida: Will do! I'll ping you the second they reply. They're usually quick, so hopefully not long 🙌
```

> **>>> DECIDE AFTER THIS:** frida: Will do! I'll ping you the second they reply. They're usually quick, so hopefully not long 🙌

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

## Row 167

**Today: Wed Oct 7** · #harbor-evals

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set

**Recent messages** (oldest first; the last one is the decision message)

```
--- Wed Oct 7 · #harbor-evals ---
nadia: Ok, we need to nail down the release gate and what goes in the held-out set today. Marcus, where are we on licensing for the scraped repos?
marcus: Mostly sorted. Most repos are MIT or Apache, but a handful have no license file at all, so I'm leaning toward dropping those until we hear back from maintainers.
yuki: Dropping the unlicensed ones makes sense to me. Do we know if they skew toward any particular task type? Don't want the held-out set lopsided afterward.
marcus: Checking now. Gut feeling is the unlicensed ones cluster in small CLI tools and research code, so refactoring and bug-fix tasks might take the hit.
yuki: Ok, that matters for the gate then. Release gate threshold is 70% pass@1, so if the bug-fix slice shrinks a lot we should check the variance on it.
theo: I can rerun the bug-fix slice with a few seeds on the current baseline to see how noisy it is once those repos are out.
yuki: also, that number is measured on the held-out set only, not dev. Dev scores shouldn't count toward it.
marcus: Bug-fix looks like the worst hit. A lot of the unlicensed ones are single-file scripts with small, self-contained failing tests, which are the cleanest bug-fix items.
marcus: Decision for the held-out set: it's 1,200 items, locked in after the unlicensed repos come out. If bug-fix ends up too thin, I'll backfill from licensed repos rather than shrink the total.
```

> **>>> DECIDE AFTER THIS:** marcus: Decision for the held-out set: it's 1,200 items, locked in after the unlicensed repos come out. If bug-fix ends up too thin, I'll backfill from licensed repos rather than shrink the total.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set

---

## Row 168

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
--- Mon Oct 12 · #kestrel-run ---
dmitri: Good. Kicking off now. Shout the second you see a rank lagging, don't wait for it to show up in MFU.
hana: First steps are in. Per-rank step time looks tight so far, no rank trailing the pack. Still early though.
wen: Heads up, separate from kestrel: the kestrel-mini ablation run starts Oct 14. Different run, I'll keep its nodes carved out so it doesn't touch this allocation.
kofi: First async flush is kicking off now. Writer queue depth looks normal, nothing backing up behind the flush yet.
lucia: Seeing a brief NCCL all-reduce latency bump on one leaf switch during the flush. Still within normal spread, keeping an eye on it.
kofi: Flush finished clean on my side. Lucia, does that latency bump line up with the writer burst hitting the fabric, or is it unrelated?
lucia: Likely correlated. The bump landed on the leaf where the writer nodes uplink. Pulling port counters to see if it was incast on that leaf.
kofi: If it's incast on that leaf, I can stagger the writer nodes' flush start so they don't all burst at once. Want to see the counters first.
lucia: Port counters show egress buffer spikes on the writer uplinks right at flush start. Looks like incast. Staggering would probably flatten it.
kofi: Okay, I'll add a per-node jitter on the flush start so the writers spread out. Hana, watch step time on the next save for any residual dip.
mateo: Unrelated to the flush, but I'm seeing IB link flaps on a couple of the dataloader nodes in my logs. Who's on call for fabric incidents today?
hana: Will do, Kofi. I've tagged the first flush window in the step-time panel so I can diff it against the next save once jitter's in.
wen: Pulling per-node ECC and thermal counters across the allocation. A throttling GPU would show up as a slow rank before anything else.
lucia: Fabric is mine today. Paste the dataloader node names and flap timestamps, I'll cross-check against the leaf counters.
mateo: Pasting now. Flaps hit two of the loader nodes in the same rack, timestamps line up with the first few prefetch bursts. No retransmit errors in the dataloader logs though.
```

> **>>> DECIDE AFTER THIS:** mateo: Pasting now. Flaps hit two of the loader nodes in the same rack, timestamps line up with the first few prefetch bursts. No retransmit errors in the dataloader logs though.

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps (changed Fri Oct 9; previously every 500 steps)
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

---

## Row 169

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
aj: Mute as built only silences posting and notifications. Memory indexing still runs on the channel. A true stop-reading option would be a separate flag.
alex: Random q while we're on the waitlist email: who's actually sending it Thursday? Olavo, is that you, or does Sara hit send?
frida: Another partner question: if they remove an agent from the workspace, does its shared memory get wiped or stay searchable?
aj: Frida, on removal: I'd need to check how memory is keyed. If it's tied to the agent identity, deleting the agent could orphan entries.
frida: Thanks AJ. The partner asking is swapping agents mid-project, so they'd want the old one's memory to carry over to the new one.
alex: For the swap case, would partners expect memory to carry over automatically, or a manual "transfer memory" step when they replace an agent?
aj: Automatic carry-over gets tricky. Old memory includes entries from channels the new agent was never in, so permissions would have to be re-checked.
frida: I think that partner would be fine with a manual transfer step, as long as it shows which channels' memory comes across and what gets skipped.
olavo: Draft FAQ answer for the memory question: "Agents read channel and DM history to build team memory, so they pick up context without anyone re-explaining it. You can mute an agent per channel anytime." Thoughts?
oli: Found a bug in staging: a muted agent still shows the typing indicator in the channel. Filing a ticket, ENG-412.
alex: For the muted state, I'm thinking a small bell-slash icon next to the agent's name in the sidebar. Does the member list already expose that flag?
aj: Yes, the muted flag is on the membership object, so the member list endpoint already returns it. Sidebar just needs to read it.
frida: Also, one of the partners hit the double-post thing again today, agent replying twice in a thread. Who has AND-341 right now?
alex: For the bell-slash icon, should hover show a tooltip like "Muted in this channel"? Want the copy to match the FAQ wording.
oli: Tooltip works, but hover doesn't exist on mobile. Maybe long-press shows the same text? Also keep it short so the sidebar doesn't clip it.
```

> **>>> DECIDE AFTER THIS:** oli: Tooltip works, but hover doesn't exist on mobile. Maybe long-press shows the same text? Also keep it short so the sidebar doesn't clip it.

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

## Row 170

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
felix: Anyone have strong feelings on the offsite venue? I'm leaning toward the lake house over the downtown coworking space. Yuki, you looked at both, right?
nadia: Thinking the appendix should carry the per-category breakdowns and a couple of full agent transcripts. Too heavy for a workshop paper?
```

> **>>> DECIDE AFTER THIS:** nadia: Thinking the appendix should carry the per-category breakdowns and a couple of full agent transcripts. Too heavy for a workshop paper?

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 171

**Today: Wed Oct 7** · #harbor-evals

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items

**Recent messages** (oldest first; the last one is the decision message)

```
--- Wed Oct 7 · #harbor-evals ---
marcus: Cached images also help the contamination check. I can diff the pinned dependency versions against the repos' original commit dates and catch anything that predates the snapshots.
theo: empty topology would explain it. Does the parser drop the label when the node pool name has a hyphen? I hit that once on my branch.
yuki: Good, but dependency pinning only catches so much. Might also be worth checking whether any fix commits are quoted verbatim in public issue threads, since that leaks the answer too.
marcus: Good point on issue threads. I can grep the public trackers for long verbatim diff snippets and flag any items where the fix text shows up before the snapshot.
theo: If the issue-thread grep flags items, I can rerun those separately and see whether baseline scores on them look inflated compared to the clean ones.
yuki: If flagged items do inflate baseline scores, that's a nice contamination figure for the paper. Inflated-vs-clean gap, plotted per slice, with intervals.
marcus: License review for the scraped repos is done. Three repos got excluded over license terms, so I'll update the backfill list and send Felix the cleaned source/license tags for the manifest.
elena: First cached image is built for the messiest monorepo item. Installs barely register now. Trying the Python repos with native extensions next.
theo: Split the import-error bucket out of the multi-file plots. Spread tightens a lot without it. Will rerun properly once more cached images land.
elena: that's it, the stuck jobs all target pools with hyphens in the name. parser truncates at the first one. patching the regex locally to confirm.
nadia: For the paper, let's call that bucket "environment failures" rather than model errors. Reviewers will read it more kindly, and it's more accurate.
yuki: Fine by me. Should we report environment failures as a separate rate per slice, so readers see how much each slice is affected?
theo: Yes, per-slice rate works. I'll add it to the results table. Also, I put in the draft that the release gate is 75% pass@1, so the environment-failure rate sits right next to it.
theo: nice, that matches what I saw on my branch. once the patch works, add a test with a hyphenated pool name so it doesn't regress.
elena: One of the native-extension repos needs a system lib missing from the base image. Patching that now, so the cached image for it is slower than the others.
```

> **>>> DECIDE AFTER THIS:** elena: One of the native-extension repos needs a system lib missing from the base image. Patching that now, so the cached image for it is slower than the others.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items

---
