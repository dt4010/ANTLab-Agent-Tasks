# B 修复回归与变体

| case | baseline | fixed | 结论 |
|---|---|---|---|
| R01 | b01, valid | b01, valid | 正常回归 |
| R02 | b01, cache_hit | b02, cache_miss | 快照缓存故障修复 |
| R03 | 空证据, invalid | b03, valid | 范围先过滤修复 |
| R04 | b04, valid/supported | b04, valid/not_checked | 防止定位冒充语义支持 |
| R05 | b05, valid | b05, valid | 正常回归 |
| R06 | b06, valid | b06, valid | 正常回归 |
| R07 | 空证据, invalid | invalid_scope | 未知范围显式化 |

等价变体：重排 corpus 记录后，固定引擎仍按分数与 id 排序；重排 request.doc_ids 后，实际范围和 evidence 不变。边界：draft 的语义支持仍为 `not_checked`，因为样机没有独立语义判定器。
