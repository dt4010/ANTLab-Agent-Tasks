# 决策记录

## D1：进阶方向选择 B

- 当时判断：剩余时间较短，应优先选择自带离线样机、能形成完整复现闭环的 B。
- 替代方案：A 需要真实 PDF 定位和 14 条主结果；C 需要设计两条产品路线和至少 12 条任务输出。
- 可否定观察：如果 B 样机无法启动、故障无法稳定复现，或修复不能保留原接口，就应切换到基础题骨架并报告阻塞。
- AI/他人影响：AI 帮助比较题目要求；我通过读取题目文件和启动代码核验了离线依赖与接口。
- 证据：`进阶/02_B_系统失效诊断.md`、`进阶/challenge_b/spec.md`、`runs/advanced_b/baseline.json`。
- 最终决定：选择 B，并保留基础题代码作为必做部分。

## D2：B 题主问题选择范围过滤与缓存污染

- 当时判断：R02 返回 v1 证据而请求是 v2，R03 丢失 beta 范围内证据；两者都直接破坏用户对当前资料的核验。
- 替代方案：先重写页面或只改引用状态。
- 可否定观察：若缓存键已包含快照且范围内排序仍能返回 b03，则这条因果解释不成立。
- AI/他人影响：AI 提示了需要先写回归测试；我用原始 `challenge:Engine` 和固定输入重放核验。
- 证据：`tests/test_baseline_faults.py`、`runs/advanced_b/baseline.json`、`runs/advanced_b/fixed.json`。
- 最终决定：先做范围裁剪再排序，并将请求、语料和 draft 纳入缓存键。

## D3：语义支持状态不冒充已验证

- 当时判断：离线样机只能确认引用定位，不能从字符串规则可靠证明 answer 的语义支持；因此修复引擎统一返回 `support_status=not_checked`。
- 替代方案：用关键词包含关系直接标记 supported/contradicted。
- 可否定观察：若存在明确、独立且覆盖全部 draft 语义的规则，并有反例测试证明其可靠，才可升级状态。
- AI/他人影响：AI 提醒区分 locator 与 semantic support；我根据 spec 和 R04 的“取消不等于释放 GPU”反例保守实现。
- 证据：`进阶/challenge_b/spec.md`、`tests/test_fixed_engine.py`、`runs/advanced_b/fixed.json`。
- 最终决定：定位有效不等于语义支持，未实现独立语义校验时如实标记 `not_checked`。
