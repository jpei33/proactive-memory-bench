| Condition                       |   Evidence delivered % | Catches wrong value % [95% CI]   |   False alarm on correct value % |   Balanced acc. % |   Catch given evidence delivered % |
|:--------------------------------|-----------------------:|:---------------------------------|---------------------------------:|------------------:|-----------------------------------:|
| S0 (window only)                |                      2 | 6 [2, 11]                        |                                6 |                50 |                                 67 |
| A3 (A · per message + RRF)      |                     56 | 72 [59, 84]                      |                               27 |                72 |                                 89 |
| B3 (B · window + RRF)           |                     64 | 69 [62, 76]                      |                               15 |                77 |                                 91 |
| Cs2 (Cstar · gold links + emb)  |                     70 | 69 [56, 80]                      |                               18 |                76 |                                 93 |
| D2 (D · topics + emb)           |                     66 | 72 [59, 82]                      |                               19 |                76 |                                 92 |
| E1 (E · rewrite + BM25)         |                     91 | 82 [74, 90]                      |                               20 |                81 |                                 88 |
| AG-grep (agent searches (grep)) |                     69 | 74 [62, 84]                      |                                8 |                83 |                                 93 |
| OR (oracle facts box)           |                        | 96 [92, 100]                     |                               30 |                84 |                                    |
