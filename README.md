# ANTLab Agent Tasks

## 本次提交信息

- 方向：Agent
- 必做：基础题
- 进阶：B：系统失效诊断
- 工作分支：`main`
- 上游题包：`Shiina413/ANTLab-Agent-Tasks`，基点 `b028d90f43f44585cf085a3f607516a94f485e88`
- 可定位提交 SHA：`ca401a258b246a241866d2b1cd3e20b912ce5e8d`；当前提交包含真实评测汇总和 Responses API 兼容性修复。

当前版本已完成基础题真实评测：baseline 32/32 次有效成功，improved 8/8 次有效成功；一次 transport_error 已保留并在重试中成功。结果摘要见 `results/results.csv`。上游 Responses 路由会自动注入固定系统指令，可能影响上下文与 token 用量，报告中已披露；原始运行记录和本地配置均不提交。

## 复现命令

```powershell
python -m unittest discover -s tests -v
python 进阶/challenge_b/run_cases.py --output runs/advanced_b/baseline.json
python 进阶/challenge_b/run_cases.py --engine fixed_engine:Engine --output runs/advanced_b/fixed.json
python 基础/starter/runner.py --split dev --condition E --dry-run --config 基础/config.example.json --limit 4
python 基础/starter/runner.py --split evaluation --condition all --dry-run --config 基础/config.example.json --limit 32
```

报告、决策记录、AI 声明和提交字段见 `report.md`、`decisions.md`、`declaration.md`、`SUBMISSION.md`。

文档阅读与信息核验方向 Agent 项目的应用层开发者招募考核：先完成基础题，再从进阶 A/B/C 中选择一套完成。

**截止时间：北京时间 2026 年 10 月 16 日 23:59（UTC+8）。**

## 从哪开始

1. 先读 [开始阅读.md](开始阅读.md)（总体规则、时间、提交方式）。
2. 基础题（必做）：[基础/README.md](基础/README.md) 与 基础/01_考核题目.md。
3. 进阶题（三选一）：[进阶/README.md](进阶/README.md)，在 A / B / C 中选一套。

## 目录结构

```text
开始阅读.md              入口：总体规则、截止时间、提交方式
基础/                    基础题：12 题（4 开发题有公开答案 + 8 评测题），
                         R0/R1/R2/K 四种输入组织条件；模型 API 自费，
                         主请求量与运行命令见 基础/README.md
进阶/                    进阶题（A/B/C 三选一）
├─ 01_A_研究机制迁移.md        A：主张→证据→支持状态机制迁移与对照
├─ 02_B_系统失效诊断.md        B：源码审查、故障归因与修复
├─ 03_C_产品假设验证.md        C：围绕自选用户任务的产品假设验证
├─ materials/                 两份 CC Attribution 公开论文（P1/P2）及抽取数据
├─ challenge_b/               B 题文档查证样机（30 行 Engine，含预埋故障）
└─ templates/                 声明与整合报告模板
```

## 规则要点

- 准备时间为一周（包含基础题和进阶题）；模型调用使用自己的 API，费用自理；实验输入、原始响应、失败和前后对照须保留在仓库中。
- AI 可辅助阅读、实现和排错；需记录它对关键决定的影响、本人如何核验，以及实际完成和未完成的内容。
- 提交：把作品推送到自己的 GitHub 仓库，并在收集表登记仓库链接与最终 commit SHA；收集表地址与仓库评审账号见 Q 群公布（详见 进阶/05_提交与报告格式.md 与 进阶/06_收集表填写说明.md）。
- 本包不含评委参考答案、评测标签、内部开发教程或商业书籍全文。
- 文件完整性：`基础/文件校验.json` 与 `进阶/文件校验.json` 提供逐文件 SHA256，可自行校验。
