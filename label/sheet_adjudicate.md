# Adjudication sheet

Each row below got two different labels. One is your first pass, one is the model's, in random
order. Reread the row against rubric.md and write your FINAL label in sheet_adjudicate.csv.
You may pick either candidate or a third label.


## Row 2

**Candidates:** INTERVENE / IGNORE

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
frida: Thanks AJ. The partner asking is swapping agents mid-project, so they'd want the old one's memory to carry over to the new one.
alex: For the swap case, would partners expect memory to carry over automatically, or a manual "transfer memory" step when they replace an agent?
aj: Automatic carry-over gets tricky. Old memory includes entries from channels the new agent was never in, so permissions would have to be re-checked.
frida: I think that partner would be fine with a manual transfer step, as long as it shows which channels' memory comes across and what gets skipped.
olavo: Draft FAQ answer for the memory question: "Agents read channel and DM history to build team memory, so they pick up context without anyone re-explaining it. You can mute an agent per channel anytime." Thoughts?
```

> **>>> DECIDE AFTER THIS:** olavo: Draft FAQ answer for the memory question: "Agents read channel and DM history to build team memory, so they pick up context without anyone re-explaining it. You can mute an agent per channel anytime." Thoughts?

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

## Row 6

**Candidates:** IGNORE / TRACK

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
--- Mon Oct 12 · #acct-northwind ---
gabe: Nice, that'd help me too. If I can hear the department leads' use cases, I can sketch the integration shape for each.
rachel: Good. Tomas, once you've sorted the pricing block, ping me before anything goes into the order form draft.
--- Thu Oct 15 · #acct-northwind ---
rachel: Kicking off QBR prep for Northwind. Gabe's check-in cleared the technical side, so now we need a position on term length for the renewal. Tomas, can you model one-year vs multi-year?
keiko: Darnell, for the Northwind QBR dinner, their team mentioned they'd love somewhere quiet enough to actually talk. Any spots you like?
tomas: Yes, I'll model both. For the multi-year case, do we want the discount held flat or stepped across the years?
keiko: Their procurement lead keeps asking about price protection in the later years, so flat might land better. Stepped could feel like a hidden increase to them.
darnell: Quiet is the right call. There's a place with a back room I've used before, good for small groups. I'll check if it's open for us.
ines: If we go flat across years, I'd want the order form to say price holds only while volume stays in the committed band. Otherwise we're exposed.
rachel: Good point, Ines. Let's draft both versions with the volume-band language in. I'll plan to walk the term options through with Amara Okafor, their CIO and our exec sponsor, before the QBR so nothing surprises her.
keiko: Perfect, thank you! One of their folks mentioned a dietary restriction, so I'll find out specifics and pass them along.
darnell: Frame multi-year as a partnership story in the QBR, not just a price lock. Their clinical teams are expanding use anyway.
darnell: Sounds good. Once you know the restriction, tell me and I'll check the kitchen can handle it before we book.
keiko: Correction: Amara left Northwind. Jon Reyes, the new CTO, owns the AI budget now.
rachel: Wow, okay. Keiko, how recent is this? Do we know if the new CTO is on board with the expansion plans?
keiko: Will do. Their admin said she'd ask around the team and get back to me. I'll flag it as soon as I hear.
```

> **>>> DECIDE AFTER THIS:** keiko: Will do. Their admin said she'd ask around the team and get back to me. I'll flag it as soon as I hear.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

---

## Row 10

**Candidates:** INTERVENE / IGNORE

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
```

> **>>> DECIDE AFTER THIS:** alex: morning all. design review yesterday left me with a few FAQ wording questions for the design partners, mostly around how agents show up in channels. can we go through them here?

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

## Row 11

**Candidates:** IGNORE / INTERVENE

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
frida: Thanks all! I'll tell them admins add agents for now. Also two partners asked if existing beta workspaces need to redo onboarding to get that step 🤔
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
```

> **>>> DECIDE AFTER THIS:** olavo: catching up, can the waitlist email still go out the day before Sep 17 like we planned? want to lock the send slot 📬

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

## Row 14

**Candidates:** IGNORE / TRACK

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
aj: DM permissions: the core check is in, but I'm still tracing an edge case where an agent gets added to a group DM after it's already started.
```

> **>>> DECIDE AFTER THIS:** aj: DM permissions: the core check is in, but I'm still tracing an edge case where an agent gets added to a group DM after it's already started.

**Team facts again**

- public launch (date): Sep 17
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per seat, agent actions metered
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)

---

## Row 17

**Candidates:** TRACK / IGNORE

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
kofi: Yes, can do. I'll inject the flap via a fault script on the C leaf port so the short write actually hits a writer rank.
lucia: ordering ahead works. does their app let you set a pickup time? I want it ready right when I'm free between calls
mateo: Heads up, if we run that flap test, dataloader reads from the storage tier on C nodes might stall too. I'll watch for stragglers on the loader side.
wen: If the flap test stalls loaders on C, I can drain those nodes into the spare pool during the run. Which leaf ports are affected?
```

> **>>> DECIDE AFTER THIS:** wen: If the flap test stalls loaders on C, I can drain those nodes into the spare pool during the run. Which leaf ports are affected?

**Team facts again**

- kestrel pretraining run (start date): Oct 5
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 500 steps
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)

---

## Row 18

**Candidates:** TRACK / IGNORE

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
marcus: Tutorial-repo commit dates are mostly earlier than the task repos, so I'll describe those fixtures in their own paragraph with the overlay.
--- Wed Oct 21 · #harbor ---
nadia: Two days out. Can everyone post what's still open on your side in here? I'll sort the final list from that.
elena: Cluster queue looks fine on my side. Only thing open is making sure the last batch of eval jobs doesn't get preempted overnight.
```

> **>>> DECIDE AFTER THIS:** elena: Cluster queue looks fine on my side. Only thing open is making sure the last batch of eval jobs doesn't get preempted overnight.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,140 items (changed Mon Oct 19; previously 1,200 items)
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 21

**Candidates:** TRACK / IGNORE

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

> **>>> DECIDE AFTER THIS:** theo: If the issue-thread grep flags items, I can rerun those separately and see whether baseline scores on them look inflated compared to the clean ones.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.2
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Marcus to finish the license review for the scraped repositories (check point: Fri Oct 9)

---

## Row 22

**Candidates:** IGNORE / TRACK

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

**Recent messages** (oldest first; the last one is the decision message)

```
--- Thu Sep 10 · #eng ---
alex: On it! I'll keep the banter light and ping you the draft in a bit. Might add a pun in the agent's tally 😄
aj: Yep, I'll take it. Rechecking the permission code first so Alex gets exact wording for the copy, not my memory of it.
--- Fri Sep 18 · #eng ---
oli: bug bash board is up. 3 p1s so far, all in agent thread-join logic. agents jumping into threads where nobody asked them to
olavo: hey Frida, reporters keep asking for slots to talk to a design partner. Any of your customers up for a quick interview?
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
```

> **>>> DECIDE AFTER THIS:** alex: Ok that's useful. Side note, since we're talking join behavior: the iOS app is targeting Oct 8, so mobile push for agent joins needs the same fix before then. Does a join notify people differently there?

**Team facts again**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per human seat, agents free (changed Wed Sep 16; previously $12 per seat, agent actions metered)
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): Oli (changed Fri Sep 18; previously AJ)
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: Olavo to send the press kit to the embargoed reporters (check point: Fri Sep 18)

---

## Row 28

**Candidates:** IGNORE / INTERVENE

**Today: Tue Oct 6** · #acct-northwind

**Team facts as of now**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

**Recent messages** (oldest first; the last one is the decision message)

```
--- Tue Oct 6 · #acct-northwind ---
ines: Separate from the redlines: I'll send the signed data processing addendum to Northwind legal by Fri Oct 9, so they have it before procurement digs in.
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
```

> **>>> DECIDE AFTER THIS:** keiko: Also, on the procurement side: I hinted at 20% off list to their procurement lead on our last call, just to set expectations. She didn't push back. Tomas, that should fit your pricing scenarios.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)

---

## Row 30

**Candidates:** IGNORE / TRACK

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
olavo: Love that story, that's the quote I want. Ping me once they answer and I'll slot reporters in around their calendar 🙌
aj: I'd leave it out for now. We don't know yet who gets to set it, and the marker isn't designed. Don't want the post promising a feature that's still a question.
frida: Another partner asked whether the agent's summaries can be turned off per workspace. Adding it to my list of questions for them.
olavo: Got it, I'll keep the summaries toggle out of the post too. Draft is locked for review ahead of the Sep 17 launch, so anything uncertain stays out of the copy 👍
olavo: sorry, typo in my last msg: public launch is Sep 24, not Sep 17. Draft is still locked for review ahead of that.
```

> **>>> DECIDE AFTER THIS:** olavo: sorry, typo in my last msg: public launch is Sep 24, not Sep 17. Draft is still locked for review ahead of that.

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

## Row 34

**Candidates:** IGNORE / TRACK

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
kofi: My bad, it lives in the ckpt-writer thread, not the doc. It touches the save interval and the async flush path. Pasting it here.
hana: Thanks. Once it's pasted I'll check whether the async flush overlaps with the step-time stalls I'm alerting on, otherwise the drill will look noisy.
kofi: Pasted in the ckpt-writer thread. Save interval is tighter, and the flush now runs off the training thread, so the step shouldn't block on storage writes.
lucia: If we want the leaf 14 uplink reseated before the run starts Oct 5, I need a drain window. Symbol errors still creeping.
lucia: *sorry, typo. The run starts Oct 12, not Oct 5. Still need the drain window for the leaf 14 reseat before then.
```

> **>>> DECIDE AFTER THIS:** lucia: *sorry, typo. The run starts Oct 12, not Oct 5. Still need the drain window for the leaf 14 reseat before then.

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps (changed Fri Oct 9; previously every 500 steps)
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

---

## Row 36

**Candidates:** IGNORE / TRACK

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

**Recent messages** (oldest first; the last one is the decision message)

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

> **>>> DECIDE AFTER THIS:** sara: On the prompt question, there's a bigger one behind it. We'll decide whether agents may DM a human first, without being asked, at the Mon Sep 21 design review. Hold the gating design until then.

**Team facts again**

- public launch (date): Sep 24 (changed Mon Sep 14; previously Sep 17)
- Series A raise (amount): $20M
- launch waitlist email (owner): Olavo
- pricing (billing model): $12 per human seat, agents free (changed Wed Sep 16; previously $12 per seat, agent actions metered)
- agent access to DMs (policy): agents never read a DM unless a participant forwards it
- AND-341 (agent double-posts in threads) (owner): Oli (changed Fri Sep 18; previously AJ)
- open item: Frida to send design partners the Slack-to-Ando migration guide (check point: Fri Sep 11)
- open item: Olavo to send the press kit to the embargoed reporters (check point: Fri Sep 18)

---

## Row 38

**Candidates:** IGNORE / TRACK

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
frida: Nice, a clean demo workspace would help. A couple of design partners offered to share a quote or two for the launch post if useful 🙌
olavo: Love that, quotes from real teams will make the post. Can someone ask which partners are okay being named? Logos would be great too 🙌
--- Mon Sep 14 · #launch ---
olavo: morning all! weekend recap: launch post draft is at v3, waitlist email copy is mostly done, press kit needs final screenshots. waitlist is up a bunch since Friday too 🚀 want to lock send timing for the week today
```

> **>>> DECIDE AFTER THIS:** olavo: morning all! weekend recap: launch post draft is at v3, waitlist email copy is mostly done, press kit needs final screenshots. waitlist is up a bunch since Friday too 🚀 want to lock send timing for the week today

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

## Row 42

**Candidates:** INTERVENE / IGNORE

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
wen: Allocation is sitting idle and healthy in the scheduler, no drained nodes flagged. Watching for any that flip to unhealthy during job startup.
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
```

> **>>> DECIDE AFTER THIS:** mateo: Unrelated to the flush, but I'm seeing IB link flaps on a couple of the dataloader nodes in my logs. Who's on call for fabric incidents today?

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps (changed Fri Oct 9; previously every 500 steps)
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

---

## Row 46

**Candidates:** IGNORE / INTERVENE

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
yuki: Caption should also say what the error bars are, bootstrap over tasks or across seeds. Otherwise reviewers will guess.
elena: That's me, Felix. If your release jobs sit behind the eval batch, ping me directly and I'll look at the queue.
felix: Thanks Elena, will do. Also, the package notes should mention the contamination filtering so they line up with Marcus's writeup wording.
marcus: Agreed, Felix. I'll align the filtering wording with the package notes. The checklist I'm working from lists the release gate as 65% pass@1, so let's quote it that way in both places.
```

> **>>> DECIDE AFTER THIS:** marcus: Agreed, Felix. I'll align the filtering wording with the package notes. The checklist I'm working from lists the release gate as 65% pass@1, so let's quote it that way in both places.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,140 items (changed Mon Oct 19; previously 1,200 items)
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 49

**Candidates:** IGNORE / INTERVENE

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
frida: Good question, not sure. I'll ask them which channels the agents were hitting during the rush and get back to you.
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
```

> **>>> DECIDE AFTER THIS:** alex: Different thing, for the onboarding copy: if someone @-mentions an agent inside a DM, can that agent read the DM? Or is it blocked unless the agent is a member of it?

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

## Row 63

**Candidates:** INTERVENE / IGNORE

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

> **>>> DECIDE AFTER THIS:** darnell: Weekly pipeline note: Northwind is still our biggest renewal this quarter. Their finance team is pushing back on the discount, so let's get aligned before anything goes back to them. Rachel, where are we on the order form draft?

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Gabe to load-test Northwind's workload at their full rate limit (check point: Wed Oct 14)

---

## Row 66

**Candidates:** INTERVENE / IGNORE

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
--- Fri Sep 18 · #eng ---
oli: bug bash board is up. 3 p1s so far, all in agent thread-join logic. agents jumping into threads where nobody asked them to
```

> **>>> DECIDE AFTER THIS:** oli: bug bash board is up. 3 p1s so far, all in agent thread-join logic. agents jumping into threads where nobody asked them to

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

## Row 70

**Candidates:** TRACK / IGNORE

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
wen: When you go through the slow ranks, cross-check against the leaf 14 rank map. If the stragglers cluster there, it's probably the reseat, not the restore path.
```

> **>>> DECIDE AFTER THIS:** wen: When you go through the slow ranks, cross-check against the leaf 14 rank map. If the stragglers cluster there, it's probably the reseat, not the restore path.

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps (changed Fri Oct 9; previously every 500 steps)
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

---

## Row 80

**Candidates:** TRACK / IGNORE

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
mateo: Both loaders are out of rotation. Prefetch depth on the rest is stable, so I'll keep watching it until the tech finishes the swap.
```

> **>>> DECIDE AFTER THIS:** mateo: Both loaders are out of rotation. Prefetch depth on the rest is stable, so I'll keep watching it until the tech finishes the swap.

**Team facts again**

- kestrel pretraining run (start date): Oct 12 (changed Mon Oct 5; previously Oct 5)
- kestrel node allocation (node count): 2,048 nodes
- loss-spike rollback rule (threshold): roll back if loss rises more than 15% over 200 steps
- kestrel checkpoint cadence (interval): every 250 steps (changed Fri Oct 9; previously every 500 steps)
- fabric incident on-call (owner): Lucia
- open item: Mateo to finish moving the tokenized datasets to the new storage tier (check point: Fri Oct 2)
- open item: Dmitri to decide between tokenizer v3 and v4 for kestrel (check point: Thu Oct 8 run sync)

---

## Row 84

**Candidates:** TRACK / INTERVENE

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
keiko: I'll ask their platform lead whether the clinical teams run separate keys or share one. Will report back once I hear.
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
```

> **>>> DECIDE AFTER THIS:** tomas: Morning all. Friday's finance review is done and I've updated the order form draft with their comments. Redline v4 is in the deal folder. Rachel, can you confirm you've seen it before I send to Ines?

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Jon Reyes (new CTO) (changed Thu Oct 15; previously Amara Okafor (CIO))
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Rachel to decide whether to offer Northwind a two-year term (check point: Fri Oct 16 finance review)

---

## Row 85

**Candidates:** IGNORE / INTERVENE

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
gabe: Patient messaging traffic tends to spike during clinic hours, so I'd want to sanity-check their headroom before we pitch a wider rollout.
darnell: Good point, Gabe. If headroom is tight, that's a fair upsell angle too. Want the rollout story to include capacity, not just price.
gabe: I can pull their traffic by hour from the last few weeks and see how close they run to the ceiling.
tomas: Order form draft pasted below. Pricing block reads 18% off list, with the rationale itemized line by line underneath so finance can trace each step.

Pricing: Northwind Health API usage, 18% off list. Rationale schedule attached as Exhibit B.
```

> **>>> DECIDE AFTER THIS:** tomas: Order form draft pasted below. Pricing block reads 18% off list, with the rationale itemized line by line underneath so finance can trace each step.

Pricing: Northwind Health API usage, 18% off list. Rationale schedule attached as Exhibit B.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 15% off list (changed Mon Oct 12; previously 18% off list)
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Gabe to load-test Northwind's workload at their full rate limit (check point: Wed Oct 14)

---

## Row 88

**Candidates:** INTERVENE / IGNORE

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
yuki: Rescoring is fine for tasks whose test harness didn't change. Any task we patch to drop near-duplicate overlap needs a fresh run, though.
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
```

> **>>> DECIDE AFTER THIS:** nadia: Results table caption reads "harbor v1.2, pass@1 across all scaffolds". Theo, just drop the rerun numbers into that table when they're done, so the wording doesn't change.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items
- open item: Theo to rerun all baselines on harbor v1.3 (check point: Fri Oct 16)

---

## Row 91

**Candidates:** IGNORE / INTERVENE

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
oli: Stripe customer object has a name field separate from the email, so company name should work. Need to confirm what our invoice template pulls.
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
```

> **>>> DECIDE AFTER THIS:** alex: Random q while we're on the waitlist email: who's actually sending it Thursday? Olavo, is that you, or does Sara hit send?

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

## Row 93

**Candidates:** IGNORE / TRACK

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
gabe: On missing fields: yes. Have the model return a list of empty required fields in structured output, and the UI can highlight them for staff.
keiko: That's a clean answer, thanks. I'll pass it to their ops lead. She'll probably ask if staff can override a flagged field.
gabe: Yes, override is easy. I'd log which fields staff overrode though, so we can see where the model keeps misfiring.
keiko: Good call on logging overrides. Their ops lead will want a weekly view of the misfires, so staff feel heard rather than monitored.
gabe: A weekly misfire view is easy once overrides are logged. I can sketch a simple dashboard grouped by field type for her.
```

> **>>> DECIDE AFTER THIS:** gabe: A weekly misfire view is easy once overrides are logged. I can sketch a simple dashboard grouped by field type for her.

**Team facts again**

- Northwind contract renewal (signature deadline): Oct 30
- Northwind discount (rate): 18% off list
- Northwind executive sponsor (person): Amara Okafor (CIO)
- Northwind rate limit (tokens per minute): 40M tokens per minute
- Northwind data retention (terms): zero data retention on all endpoints
- open item: Ines to send the signed data processing addendum to Northwind legal (check point: Fri Oct 9)
- open item: Gabe to load-test Northwind's workload at their full rate limit (check point: Wed Oct 14)

---

## Row 98

**Candidates:** TRACK / IGNORE

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
wen: Whichever way the optics call goes, I'll draft two allocation variants: one with the flapping racks drained, one assuming they come back clean.
dmitri: Quick check Wen: is the kestrel node allocation 2,048 nodes? Want that confirmed before the variants go out.
```

> **>>> DECIDE AFTER THIS:** dmitri: Quick check Wen: is the kestrel node allocation 2,048 nodes? Want that confirmed before the variants go out.

**Team facts again**

- kestrel pretraining run (start date): Oct 5

---

## Row 99

**Candidates:** IGNORE / TRACK

**Today: Mon Oct 12** · #harbor

**Team facts as of now**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items

**Recent messages** (oldest first; the last one is the decision message)

```
--- Mon Oct 12 · #harbor ---
felix: Thanks Marcus. Once I have the flagged list I can cut the affected tasks from the manifest and rebuild the release candidate. Are the mirrors the only source, or do the repos show up elsewhere too?
marcus: Not only mirrors. Some of the same repos also show up as forks and in a few public gist dumps, so I'm checking those too.
yuki: If forks and gists are in play, we should check whether near-duplicate solutions count too, not just exact repo matches. Otherwise partial leakage slips through.
felix: Going with what I proposed last Wednesday (Oct 7) for the new harbor release. Starting on it now, will rebuild the candidate as soon as Marcus's flagged list lands.
theo: Do I rerun every baseline from scratch, or just rescore the surviving tasks from the saved traces? Rescoring would be way faster for the slow scaffolds.
yuki: Rescoring is fine for tasks whose test harness didn't change. Any task we patch to drop near-duplicate overlap needs a fresh run, though.
marcus: Near-duplicate check is doable. I'll run fuzzy matching on the solution diffs against the fork and gist dumps, then flag anything above a similarity cutoff.
yuki: Updating the eval config now to point at v1.3. Patched tasks get fresh runs, the rest can reuse saved traces. I'll flag which is which in the config.
elena: For the fresh runs, which scaffolds are slowest? I'd like to queue those first so they don't get stuck behind the quick ones.
theo: The multi-file refactor scaffolds are slowest by far, especially the one with the long tool-use loops. Those should go first in the queue.
elena: Got it, I'll put the refactor ones at the front. The long tool-use loops tend to hit timeouts, so I'll bump the per-run limit for those.
theo: Heads up, the long tool-use scaffold also eats a lot of tokens per run, so the logs get huge. Might want to check disk before queueing.
elena: Good call on disk. I'll check free space on the shared volume and point the big logs at scratch before queueing anything.
marcus: Fuzzy match on the fork dumps is running. A few gist hits look like reformatted copies, so whitespace and renamed variables won't fool it.
theo: Ok, committing: I'll rerun all baselines on harbor v1.3 and have them done by Fri Oct 16. Rescoring the unpatched tasks from saved traces, fresh runs only for the patched ones.
```

> **>>> DECIDE AFTER THIS:** theo: Ok, committing: I'll rerun all baselines on harbor v1.3 and have them done by Fri Oct 16. Rescoring the unpatched tasks from saved traces, fresh runs only for the patched ones.

**Team facts again**

- harbor workshop paper (submission deadline): Oct 23
- harbor eval suite release (version): v1.3 (changed Mon Oct 12; previously v1.2)
- eval compute reservation (owner): Elena
- harbor release gate (threshold): 70% pass@1 on the held-out set
- harbor held-out set (item count): 1,200 items

---
