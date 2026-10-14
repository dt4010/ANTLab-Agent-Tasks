# Agent 考核整合报告

## 1. 完成概览

方向为 Agent；完成基础题代码骨架、消息构造和改进证据排序，完成进阶 B 的原始故障复现、原因区分、最小修复、回归与变体。基础题已使用 HTTPS Responses API 完成真实运行：baseline 32/32 条有效主结果成功，improved 8/8 条有效主结果成功；一次 transport_error 已保留，并在独立重试中成功。没有用 mock 结果替代正式结果。

## 2. 阅读与命题

基础题关注长上下文中的证据组织、引用定位和支持关系。B 题进一步要求区分“引用能定位”“内容支持主张”“资料快照一致”和“页面显示当前请求”。本报告把 B 的主命题定为：范围过滤和缓存键错误会让页面显示旧或错误范围的证据，即使 HTTP/JSON 结构正常。

## 3. 实验设计

固定输入为题包 `进阶/challenge_b/data.json`，对照为原始 `challenge:Engine`，改进为 `fixed_engine:Engine`。主要指标是 evidence 是否属于请求范围、引用 locator 状态和快照一致性；代价指标是本地 elapsed_ms 与 cache_hit。B 运行类型统一为 `offline_replay`。基础题 dry-run 使用题包 manifest 和 config.example.json，真实运行命令见 README。

## 4. 实现与结果

R02 证明原始缓存键遗漏 snapshot：v2 请求返回 v1 的 b01；修复后返回 b02。R03 证明全局 top-k 再过滤会丢失范围内 b03；修复后范围内排序返回 b03。R07 修复后明确返回 invalid_scope。R01、R05、R06 保持正常。R04 的引用可定位，但修复后不再声称语义 supported，保留 not_checked。

原始和修复输出分别位于 `runs/advanced_b/baseline.json` 与 `runs/advanced_b/fixed.json`，逐例说明见 `results/advanced_b_regression.md`。

## 5. 失败、变体与边界

事前预测和区分干预见 `results/advanced_b_diagnosis.md`。等价变体覆盖 corpus 顺序和 document ID 顺序。未解决边界是语义支持判断、多 worker 并发、服务端取消和真实服务延迟；这些没有被离线样机测量。

## 6. 决策与下一步

保留范围先过滤、完整缓存键和显式状态字段；停止把 locator 直接升级为 semantic support。接入真实系统前应增加 request_id、scope snapshot、evidence source、locator_status、support_status 和 cache key 摘要日志。下一步实验应使用真实模型或独立语义评测器，在固定输入下比较支持/矛盾/不足的人工复核一致性。

## 7. 复现入口

见 `README.md`。测试使用 Python 3.10+ 标准库：`python -m unittest discover -s tests -v`。

页面已通过固定引擎的本地 HTTP 端到端检查，验证 R02 返回 b02、显示实际 snapshot 和 `not_checked`。当前环境未安装 Python Playwright，因此没有提交浏览器自动化截图；这项验证缺口已明确记录。
