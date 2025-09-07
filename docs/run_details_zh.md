运行汇总与工具调用细节（自动生成）


总体汇总
--------

| run | mode | total | EM acc | judged acc | tool_calls | steps |
|---|---|---:|---:|---:|---|---:|
| labbench-cloning-kimi | - | 3 | 0.0 | - | serper-search=7, crawl-page-summary=1 | 19 |
| labbench-cloning-kimi-free-fc15 | forced_choice | 15 | 0.2 | 0.5 | serper-search=32, crawl-page-summary=4 | 82 |
| labbench-cloning-kimi-free15 | free_form | 15 | 0.0 | 0.2 | serper-search=30, crawl-page-summary=3 | 77 |
| labbench-cloning-kimi-judge | - | 3 | 0.6666666666666666 | - | serper-search=6 | 14 |
| labbench-cloning-kimi-v3 | - | 3 | 0.0 | - | serper-search=3 | 9 |
| labbench-cloning-kimi-v4 | - | 5 | 0.0 | - | serper-search=6 | 16 |
| labbench-cloning-kimi-v5 | - | 3 | 0.6666666666666666 | - | serper-search=5, crawl-page-summary=1 | 14 |

labbench-cloning-kimi
---------------------

| id | question | gold | pred | ok | judged_ok | tool_calls | tools_seq | steps |
|---|---|---|---|:--:|:--:|---:|---|---:|
| 8cd98408-8672-4330-911e-57bff9ec334a | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | GCTGGCCTTTTGCTCACATG |  | False | None | 0 | - | 1 |
| 908754dd-ffea-48f6-a969-25e954bfe68f | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | 406, 538, 1164 |  | False | None | 4 | serper-search | 9 |
| deb05431-8569-408d-aa7b-ddde9ab3f69c | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | White | The white colonies are likely the correct clones. Your anne… | False | None | 4 | serper-search, crawl-page-summary, serper-search | 9 |

labbench-cloning-kimi-free-fc15
-------------------------------

| id | question | gold | pred | ok | judged_ok | tool_calls | tools_seq | steps |
|---|---|---|---|:--:|:--:|---:|---|---:|
| 8cd98408-8672-4330-911e-57bff9ec334a | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | GCTGGCCTTTTGCTCACATG |  | False | True | 6 | serper-search, crawl-page-summary, serper-search | 12 |
| 908754dd-ffea-48f6-a969-25e954bfe68f | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | 406, 538, 1164 | 406, 534, 1168 | False | False | 0 | - | 1 |
| deb05431-8569-408d-aa7b-ddde9ab3f69c | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | White | White | True | None | 0 | - | 1 |
| 44aa0f62-8e7b-4f1c-bdbc-e0387900fa57 | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | Creating a transcriptional unit for expression of a CRISPR … | Creating a transcriptional unit for expression of a CRISPR … | True | None | 0 | - | 1 |
| 2f6249e8-cd4a-4a7b-a305-aacd2d835322 | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTC… |  | False | True | 6 | serper-search | 12 |

labbench-cloning-kimi-free15
----------------------------

| id | question | gold | pred | ok | judged_ok | tool_calls | tools_seq | steps |
|---|---|---|---|:--:|:--:|---:|---|---:|
| 8cd98408-8672-4330-911e-57bff9ec334a | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | GCTGGCCTTTTGCTCACATG | CGCCAGGGTTTTCCCAGTCACGAC | False | False | 0 | - | 1 |
| 908754dd-ffea-48f6-a969-25e954bfe68f | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | 406, 538, 1164 | Correct clones will show EcoRI-RsaI fragments of 1.2 kb and… | False | False | 0 | - | 1 |
| deb05431-8569-408d-aa7b-ddde9ab3f69c | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | White | The green colonies are likely correct. In Golden Gate cloni… | False | False | 2 | serper-search | 5 |
| 44aa0f62-8e7b-4f1c-bdbc-e0387900fa57 | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | Creating a transcriptional unit for expression of a CRISPR … | pLAB050 is a Golden Gate cloning vector for modular assembl… | False | True | 0 | - | 1 |
| 2f6249e8-cd4a-4a7b-a305-aacd2d835322 | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTC… |  | False | True | 6 | serper-search | 12 |

labbench-cloning-kimi-judge
---------------------------

| id | question | gold | pred | ok | judged_ok | tool_calls | tools_seq | steps |
|---|---|---|---|:--:|:--:|---:|---|---:|
| 8cd98408-8672-4330-911e-57bff9ec334a | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | GCTGGCCTTTTGCTCACATG |  | False | True | 6 | serper-search | 12 |
| 908754dd-ffea-48f6-a969-25e954bfe68f | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | 406, 538, 1164 | 406, 538, 1164 | True | None | 0 | - | 1 |
| deb05431-8569-408d-aa7b-ddde9ab3f69c | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | White | White | True | None | 0 | - | 1 |

labbench-cloning-kimi-v3
------------------------

| id | question | gold | pred | ok | judged_ok | tool_calls | tools_seq | steps |
|---|---|---|---|:--:|:--:|---:|---|---:|
| 8cd98408-8672-4330-911e-57bff9ec334a | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | GCTGGCCTTTTGCTCACATG | U6-F primer (GAGGGCCTATTTCCCATGATTCC) | False | None | 3 | serper-search | 7 |
| 908754dd-ffea-48f6-a969-25e954bfe68f | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | 406, 538, 1164 | Correct clones will yield three fragments: 1872 bp, 26 bp, … | False | None | 0 | - | 1 |
| deb05431-8569-408d-aa7b-ddde9ab3f69c | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | White | White colonies are likely correct. The insert disrupts GFP … | False | None | 0 | - | 1 |

labbench-cloning-kimi-v4
------------------------

| id | question | gold | pred | ok | judged_ok | tool_calls | tools_seq | steps |
|---|---|---|---|:--:|:--:|---:|---|---:|
| 8cd98408-8672-4330-911e-57bff9ec334a | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | GCTGGCCTTTTGCTCACATG | AAACCGGGGGAAAAGATAGTGATGAA | False | None | 0 | - | 1 |
| 908754dd-ffea-48f6-a969-25e954bfe68f | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | 406, 538, 1164 | Correct clones would show EcoRI/RsaI fragments of 2,631 bp … | False | None | 0 | - | 1 |
| deb05431-8569-408d-aa7b-ddde9ab3f69c | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | White | White colonies are likely correct. The insert disrupts GFP … | False | None | 0 | - | 1 |
| 44aa0f62-8e7b-4f1c-bdbc-e0387900fa57 | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | Creating a transcriptional unit for expression of a CRISPR … | Expression vector for GFP fusion proteins in E. coli; the c… | False | None | 0 | - | 1 |
| 2f6249e8-cd4a-4a7b-a305-aacd2d835322 | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTC… |  | False | None | 6 | serper-search | 12 |

labbench-cloning-kimi-v5
------------------------

| id | question | gold | pred | ok | judged_ok | tool_calls | tools_seq | steps |
|---|---|---|---|:--:|:--:|---:|---|---:|
| 8cd98408-8672-4330-911e-57bff9ec334a | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | GCTGGCCTTTTGCTCACATG |  | False | None | 6 | serper-search, crawl-page-summary, serper-search | 12 |
| 908754dd-ffea-48f6-a969-25e954bfe68f | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | 406, 538, 1164 | 406, 538, 1164 | True | None | 0 | - | 1 |
| deb05431-8569-408d-aa7b-ddde9ab3f69c | I have a plasmid pLAB050 with sequence TCGGTCTCCAACGATGTGCTTCAGTATTACATTTTTTGCCTTCAACGCCTTGATTGTTCT… | White | White | True | None | 0 | - | 1 |