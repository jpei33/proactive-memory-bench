* what does an agent need to remember to intervene at the right moment, and what does each way of remembering cost? (compare memory strategies)

strategies
1) window only, last x messages
    - baseline lower bound 
2) full workspace history (cap at x tokens) + summary of the rest
    - just use big context 
4) self-managed notes (agent capability to summarize)
    - can model curate its own memory?
5) fact store (extract + add/update/delete memory)
    - structured memory
6) temporal fact store 
    - keep history of changed facts
7) agentic search (judge uses a search_history(query) call)
    - retrieval on demand vs. memory prepared in advance
8) Oracle = window + gold facts
9) mention RAG is considered but dropped 

fact store: (M4) 
- entries of (entity, attribute, value, source msg, time)
- new value will cause old value to be mark SUPERSEDED 

* insert decoys messages
- intervening correctly but with the wrong/stale value is the worst failure 
- intervening with sth similar but different, causes major confusion 
- shouldn't intervene but looks like you should 

data
- X simulated workspaces with Y threads each

structure
- TRACK/INTERVENE/IGNORE 

measure:
- capture rate (outputting INTERVENE, grounded reason)
    - p(capture) = p(delivered)*p(capture|delivered) + p(capture|not delivered)
- capture vs distance (distance groups: in window, in this thread, in another thread)
- harmful intervention (bad intervention, stale intervention)
    - stale intervention rate likely higher when richer memory is used (confidently wrong, general LLM problem)
- accuracy of TRACK 
- cost/latency

headline result = stricture capture rate vs cost per 1000 decisions 

failure analysis:
- evidence not in memory
- evidence in memory but not retrieved
- evidence in context, but still chose IGNORE/TRACK instead of INTERVENE (oracle vs gold)
- stale (retrieved superseded value)
- late (correct intervention, but outside the accepted window)
- over-trigger (policy fired on decoy)
