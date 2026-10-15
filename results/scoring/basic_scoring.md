# 基础题评分记录

已完成真实模型运行。使用 DeepSeek 官方 Chat Completions API，D01 开发题请求成功；T01-T08 共 32 条 baseline 有效主结果全部成功，另有 1 条网络传输失败记录并已单独重试成功；R0 共 8 条 improved 有效主结果全部成功。独立结果见 `results/deepseek_results.csv`，原始运行目录在本地忽略，不提交。

DeepSeek 运行配置为 HTTPS Chat Completions API，模型为 `deepseek-chat`。检查 41 条成功记录，响应没有额外 `instructions` 字段；token 统计来自正常 prompt/completion usage。`results/deepseek_results.csv` 记录每条 DeepSeek 运行的状态、耗时、模型和输出；正确性与引用支持关系仍需人工复核。此前中转站的注入问题已作为外部渠道限制记录，不与本结果合并。
