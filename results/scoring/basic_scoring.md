# 基础题评分记录

当前记录为 dry-run 结构检查，不作为真实模型质量结论。已验证：D01-D04 开发题的输入可构造；T01-T08 共 32 条 baseline 条件请求可构造；消息只包含 question 与传入 passages，并要求 JSON answer/citations。

正式 40 次主请求仍需在本机配置 `ASSESSMENT_API_KEY`、HTTPS endpoint 和 model 后执行。正式结果应在 `runs/basic/` 保存每次输入、原始响应、失败、重试和配置摘要，并在 `results/results.csv` 逐条记录 answer correctness、citation origin、support status、elapsed time。
