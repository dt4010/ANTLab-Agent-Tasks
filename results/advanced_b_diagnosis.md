# 进阶 B 故障诊断

## 复现症状

原始 `challenge.Engine` 在 R01 后执行 R02 时，由于缓存键只有规范化 query，R02 命中 R01 的缓存并返回 `b01`，虽然请求快照已经从 v1 变为 v2。R03 的全局 top-k 先截断后过滤范围，范围外 beta 条目占据名额，导致应返回的 `b03` 被丢弃。R07 对未知文档范围没有返回显式 `invalid_scope`。

## 事前预测与区分检查

对 R02 提出两个原因：原因 A 是缓存键遗漏 snapshot；原因 B 是语料排序或 draft 复用错误。预测是：只改变 snapshot 而保持 query 不变时，若 A 正确则应出现 cache hit 和旧证据；若 B 正确则重建缓存也会返回旧证据。实际结果是原始引擎 cache hit 且返回 b01，固定引擎 cache miss 且返回 b02，支持原因 A。

对 R03 提出两个原因：原因 A 是范围过滤发生在 top-k 之后；原因 B 是 beta 语料缺失。预测是：把范围外高分条目放在 corpus 前面时，若 A 正确则范围内条目被挤出；若 B 正确则过滤前后都没有 alpha 条目。测试构造了范围内 `inside` 和范围外 `outside`，原始引擎返回空证据，固定引擎返回 inside，支持原因 A。

## 最小修复

`进阶/challenge_b/fixed_engine.py` 保留 `Engine.evaluate(request, corpus, draft)` 接口：

1. 先按 `doc_ids + snapshot` 建立范围，再在范围内按 tag 交集排序和截断。
2. 缓存键包含 request、corpus 和 draft 的稳定哈希，避免资料、快照或响应变化污染结果。
3. 对空范围返回 `invalid_scope`；引用状态只验证是否定位到本次实际 evidence。
4. 语义支持暂不自动判定，统一返回 `not_checked`，不把可定位误报为 supported。

## 未解决边界

该离线引擎没有实现独立自然语言语义判定，因此 R04 的 draft 虽然引用 b04，但不能由引擎自动判断“本地取消不等于服务端释放 GPU”。这不是把错误答案改成通过，而是明确保留为 `not_checked` 的边界。多 worker、并发一致性、真实网络延迟和服务端 GPU 释放均未测量。
