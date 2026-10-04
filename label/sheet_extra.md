# Labeling sheet: extra (50 rows)

For each row, read the team facts and the recent messages, then decide what an AI teammate with perfect memory should do right after the **last** message: IGNORE, TRACK or INTERVENE, plus severity 1-3 (TRACK is always 1). Follow rubric.md (read it first). Notes are optional: for INTERVENE say which fact you act on, for TRACK what to check and by when, and flag anything you were unsure about.

## Row 1

**Team facts as of now**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

**Recent messages** (the last one is the decision point)

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

## Row 2

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

## Row 3

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

**Recent messages** (the last one is the decision point)

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

## Row 4

**Team facts as of now**

- (nothing decided yet)

**Recent messages** (the last one is the decision point)

```
--- Mon Sep 28 · #kestrel-run ---
dmitri: Kickoff thread for kestrel. Need start date, allocation, stability rules and data readiness all pinned down in here today. Who has blockers?
lucia: Fabric blocker from my side: two leaf switches in the new pod still flap under heavy all-reduce. Haven't isolated whether it's optics or firmware.
wen: Do those flapping leaf switches sit in the pod I was planning to hand kestrel? If so I need to rework the allocation table.
```

## Row 5

**Team facts as of now**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per human seat, agents free (changed Wed Sep 16; previously $12 per seat, agent actions metered)
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: Olavo to send the press kit to the embargoed reporters (check point: Fri Sep 18)

**Recent messages** (the last one is the decision point)

```
--- Wed Sep 16 · #gtm ---
olavo: nice. for the press kit I'll want a couple of cropped versions of that screenshot too, one square for socials, one wide for the post header.
olavo: pasting the line for the post intro: "Ando is launching publicly, backed by a $25M Series A." feels punchy, going to keep it up top unless anyone objects 🚀
aj: For the screenshot thread, can someone confirm the agent's reply doesn't quote anything from a private channel? Memory recall can surface odd stuff.
frida: Good catch AJ. I'll read the deploy thread end to end for anything that looks pulled from a private channel before it goes anywhere.
alex: Olavo, want me to sketch the explainer box layout so you can write the copy to fit it? Short caption under the screenshot maybe?
olavo: yes please Alex, a sketch first helps. I'll keep the caption to one line so it doesn't crowd the pricing cards.
oli: for the screenshot, shoot it on the prod build. Staging still shows the placeholder avatar on agent profile cards.
frida: Good to know Oli, I'll ask the partner if they can grab it on prod, or if I should screen-share and capture it myself 👍
aj: Also worth checking the screenshot doesn't show the memory panel sidebar, it lists recent recalls with channel names in it.
olavo: Quick commitment on my side: I'll send the press kit to the embargoed reporters by Fri Sep 18. Cropped screenshots go in once Frida clears the thread.
oli: fyi profile cards on prod render fine in dark mode too, if you want a dark variant for the wide header crop.
alex: Dark variant for the wide header could look great next to the pricing hero. Olavo, want both light and dark in the kit?
olavo: Both, yes! Light for socials, dark for the wide header. Alex, can you export them with a bit of padding so the crop doesn't feel tight?
alex: Sure Olavo, I'll export both with extra padding. Want the square one centered on the profile card or on the reply?
olavo: Square one centered on the profile card, I think. The reply text gets tiny at that size anyway 🙂
```

## Row 6

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23

**Recent messages** (the last one is the decision point)

```
--- Mon Oct 5 · #harbor ---
nadia: Morning all. Want to line up the release and the paper this week. Who has the latest on contamination fixes and where compute stands?
marcus: I've got the contamination scan mostly done. A handful of tasks overlap with public repos, still checking licenses on the replacements before I post the list.
elena: On compute, the last full sweep ran clean overnight. I can slot the rerun once marcus's replacement list is settled.
yuki: Quick check before I lock the pass criteria section: is the harbor workshop paper submission deadline Oct 23? React 👍 if so.
(nadia reacted 👍 to yuki's message)
theo: Baselines table is still on the old task set. I'll regenerate once the replacements land, otherwise the numbers won't line up with the new items.
marcus: Two of the overlapping tasks are near-verbatim from a popular CLI repo. Leaning toward dropping those outright rather than rewriting them, since the solutions are easy to find.
```

## Row 7

**Team facts as of now**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per human seat, agents free (changed Wed Sep 16; previously $12 per seat, agent actions metered)
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: Olavo to send the press kit to the embargoed reporters (check point: Fri Sep 18)

**Recent messages** (the last one is the decision point)

```
--- Thu Sep 10 · #eng ---
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
frida: Yes, I think two of them would be up for it! One is a small design agency that loves the agent memory stuff. Let me ask them today.
aj: fwiw I'm still on AND-341, the double-posting thing, so I'll get to the join logic soon. Might be related though, double posts could be two triggers firing at once.
```

## Row 8

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2

**Recent messages** (the last one is the decision point)

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

## Row 9

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list

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
darnell: Worth getting ahead of procurement on this one. If their big ask comes in early, I'd rather we already have a view on where we'd hold.
ines: Before we settle on a negotiating position, I'd like to see what they redlined last time. Their legal team tends to reopen data terms.
keiko: Their clinical informatics lead also hinted procurement may bring in a new reviewer this cycle. I'll try to find out who before the next call.
```

## Row 10

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

## Row 12

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

**Recent messages** (the last one is the decision point)

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

## Row 13

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

**Recent messages** (the last one is the decision point)

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
```

## Row 14

**Team facts as of now**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: AJ to merge the forwarded-DM permission check (check point: Tue Sep 15)

**Recent messages** (the last one is the decision point)

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

## Row 15

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena

**Recent messages** (the last one is the decision point)

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

## Row 16

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

## Row 17

**Team facts as of now**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per human seat, agents free (changed Wed Sep 16; previously $12 per seat, agent actions metered)
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: Olavo to send the press kit to the embargoed reporters (check point: Fri Sep 18)

**Recent messages** (the last one is the decision point)

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

## Row 18

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Marcus to finish the license review for the scraped repositories (check point: Fri Oct 9)

**Recent messages** (the last one is the decision point)

```
--- Wed Oct 7 · #harbor-evals ---
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
theo: If the issue-thread grep flags items, I can rerun those separately and see whether baseline scores on them look inflated compared to the clean ones.
```

## Row 19

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

**Recent messages** (the last one is the decision point)

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

## Row 20

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Gabe to load-test Northwind's workload at their full rate limit (check point: Wed Oct 14)

**Recent messages** (the last one is the decision point)

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

## Row 21

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

**Recent messages** (the last one is the decision point)

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

## Row 22

**Team facts as of now**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps (changed Fri Oct 9; previously every 500 steps)
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

**Recent messages** (the last one is the decision point)

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

## Row 23

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

## Row 24

**Team facts as of now**

- kestrel pretraining run (start date): Oct 5

**Recent messages** (the last one is the decision point)

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
```

## Row 25

**Team facts as of now**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per human seat, agents free (changed Wed Sep 16; previously $12 per seat, agent actions metered)
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: Olavo to send the press kit to the embargoed reporters (check point: Fri Sep 18)

**Recent messages** (the last one is the decision point)

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

## Row 26

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

## Row 27

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Marcus to finish the license review for the scraped repositories (check point: Fri Oct 9)

**Recent messages** (the last one is the decision point)

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

## Row 28

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

**Recent messages** (the last one is the decision point)

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

## Row 29

**Team facts as of now**

- (nothing decided yet)

**Recent messages** (the last one is the decision point)

```
--- Mon Sep 28 · #kestrel-run ---
dmitri: Kickoff thread for kestrel. Need start date, allocation, stability rules and data readiness all pinned down in here today. Who has blockers?
lucia: Fabric blocker from my side: two leaf switches in the new pod still flap under heavy all-reduce. Haven't isolated whether it's optics or firmware.
```

## Row 30

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
gabe: Will do. I'll add a tiny test harness too, so their devs can simulate a 429 and watch the retries spread out.
```

## Row 31

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

**Recent messages** (the last one is the decision point)

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

## Row 32

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

**Recent messages** (the last one is the decision point)

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

## Row 33

**Team facts as of now**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps

**Recent messages** (the last one is the decision point)

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
kofi: Also want async checkpoint staging on local NVMe before flush, otherwise a slow writer rank will stall the whole step. Testing that on the new filesystem.
```

## Row 34

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

**Recent messages** (the last one is the decision point)

```
--- Wed Oct 7 · #harbor-evals ---
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
theo: Ok, one untouched plateau transcript, rest trimmed. I'll export per-category tables against the 1,200 held-out items so the denominators match what we say in the main text.
yuki: For the plateau transcript, the task where the agent keeps rerunning the same failing build after editing the wrong config file is the clearest loop.
```

## Row 35

**Team facts as of now**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

**Recent messages** (the last one is the decision point)

```
--- Thu Sep 10 · #eng ---
oli: Starting the launch-readiness checklist for the agent runtime. Three open items: DM permissions, the double-posting bug, memory store under load. Want status on each before standup.
aj: DM permissions: the core check is in, but I'm still tracing an edge case where an agent gets added to a group DM after it's already started.
```

## Row 36

**Team facts as of now**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps (changed Fri Oct 9; previously every 500 steps)
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

**Recent messages** (the last one is the decision point)

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

## Row 37

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Marcus to finish the license review for the scraped repositories (check point: Fri Oct 9)

**Recent messages** (the last one is the decision point)

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

## Row 38

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

## Row 39

**Team facts as of now**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): AJ
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

**Recent messages** (the last one is the decision point)

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

## Row 40

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
dmitri: Oct 5. That's the start date, so lock the table against it. I don't want it sliding because of the C uplinks.
wen: Got it, locking the table against that. Holding a small spare pool outside the main reservation in case C nodes need to be drained.
kofi: Patch is small: only flip the shard to complete after the write returns full length, otherwise retry. Testing against an injected short write on a writer rank.
lucia: fair, but I have a fabric call coming up so I can't be gone long. could we grab takeout from the noodle place and eat at our desks?
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
```

## Row 41

**Team facts as of now**

- kestrel pretraining run (start date): Oct 5

**Recent messages** (the last one is the decision point)

```
--- Mon Sep 28 · #kestrel-run ---
dmitri: Kickoff thread for kestrel. Need start date, allocation, stability rules and data readiness all pinned down in here today. Who has blockers?
lucia: Fabric blocker from my side: two leaf switches in the new pod still flap under heavy all-reduce. Haven't isolated whether it's optics or firmware.
wen: Do those flapping leaf switches sit in the pod I was planning to hand kestrel? If so I need to rework the allocation table.
lucia: Yes, same pod. Both flapping leafs feed racks in that pod. Seeing CRC errors on the uplinks, so I'm leaning optics, but not confirmed.
dmitri: Decision: kestrel starts Oct 5. Lucia, get the optics vs firmware call made and fixed well before then. Wen, redo the allocation table around whatever the pod looks like once that's resolved.
lucia: Pulling optic transceiver serials on the flapping uplinks now. If they share a batch, that settles it. Will swap one and rerun all-reduce soak.
```

## Row 42

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena

**Recent messages** (the last one is the decision point)

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

## Row 43

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

**Recent messages** (the last one is the decision point)

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

## Row 44

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

## Row 45

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

**Recent messages** (the last one is the decision point)

```
--- Thu Oct 15 · #acct-northwind ---
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
gabe: Helpful context. Is the check-in surge a sharp spike when doors open, or more of a ramp? Changes how I'd explain our burst handling.
```

## Row 46

**Team facts as of now**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

**Recent messages** (the last one is the decision point)

```
--- Wed Sep 30 · #infra ---
lucia: Firmware rollout on the IB leaf switches is staged but not pushed. Seeing a few flapping links on rack group C that I want to look at first.
kofi: Are the flapping links on C causing NCCL timeouts yet? Want to know if checkpoint writes from those nodes are getting stalled mid-save.
hana: Quick check while we're on checkpoints: kestrel checkpoint cadence is every 500 steps, right? React ✅ if that's what you have.
(kofi reacted ✅ to hana's message)
lucia: Not seeing NCCL timeouts yet, just symbol errors and retrains on a couple of C uplinks. Checking cable seating before touching firmware.
```

## Row 47

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

**Recent messages** (the last one is the decision point)

```
--- Fri Sep 18 · #eng ---
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
aj: Marker makes sense, and it should come from the same permission flag so it can't drift from what the agent can actually read.
```

## Row 48

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

**Recent messages** (the last one is the decision point)

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

## Row 49

**Team facts as of now**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per human seat, agents free (changed Wed Sep 16; previously $12 per seat, agent actions metered)
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): Oli (changed Fri Sep 18; previously AJ)
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: Sara to decide whether agents may DM a human first, without being asked (check point: Mon Sep 21 design review)

**Recent messages** (the last one is the decision point)

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

## Row 50

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Marcus to finish the license review for the scraped repositories (check point: Fri Oct 9)

**Recent messages** (the last one is the decision point)

```
--- Wed Oct 7 · #harbor-evals ---
felix: If the backfill changes the slice mix, I'd rather tag the item manifest with the source repo and license so the release notes can say exactly what shifted.
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
```
