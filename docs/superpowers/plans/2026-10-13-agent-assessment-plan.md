# Agent Assessment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the mandatory basic evidence-grounded document QA task and the offline advanced B fault-diagnosis task with reproducible code, results, reports, and submission metadata.

**Architecture:** Keep the supplied starter and challenge implementations as immutable baselines. Add a dependency-free student pipeline for the basic task and a separate `fixed_engine.py` implementing the same B `Engine.evaluate` interface. Store every experiment group under `runs/` and every human/scoring decision under `results/`, with a single integration report linking inputs, outputs, and evidence.

**Tech Stack:** Python 3.10+ standard library, JSON/CSV/Markdown, `unittest`; optional HTTPS model provider through the supplied provider adapter, with dry-run and offline replay always available.

**Spec:** `开始阅读.md`, `基础/01_考核题目.md`, `进阶/00_共同规则与接口.md`, `进阶/02_B_系统失效诊断.md`, `进阶/05_提交与报告格式.md`

## Global Constraints

- Do not read development answers from runtime inference code.
- Do not hard-code case IDs, gold labels, or answer strings into the student implementation.
- Preserve raw inputs, raw responses, failures, first attempts, retries, and baseline-versus-improved pairings.
- B must remain offline and dependency-free; report `run_kind=offline_replay` and local elapsed time honestly.
- B responses must include request ID, actual scope/source, evidence, locator/support status, judgment source, cache hit, and elapsed time.
- Secrets, private endpoints, and local configuration remain untracked.

---

### Task 1: Establish reproducible workspace and baseline records

**Files:**
- Create: `tests/test_basic_student.py`
- Create: `tests/test_fixed_engine.py`
- Create: `runs/README.md`
- Create: `results/README.md`
- Create: `.gitignore` additions for local config, secrets, and generated private runs

**Interfaces:**
- Tests import `基础/starter/student.py` through an explicit file loader and import `进阶/challenge_b/fixed_engine.py` as `fixed_engine:Engine`.

- [ ] **Step 1: Write failing contract tests** for the required basic message shape and the B fixed-engine public response fields.
- [ ] **Step 2: Run both test files** and confirm failures are caused by missing implementation/modules.
- [ ] **Step 3: Add only workspace documentation and ignore rules** needed to run tests without committing secrets.
- [ ] **Step 4: Run the tests again** and record the expected remaining failures.
- [ ] **Step 5: Commit** `chore: establish reproducible assessment workspace`.

### Task 2: Implement basic evidence-grounded prompt pipeline

**Files:**
- Modify: `基础/starter/student.py`
- Modify: `基础/starter/runner.py` only if required to expose request logging without changing the evaluator contract
- Create: `tests/test_student_pipeline.py`
- Create: `基础/config.local.example.json`

**Interfaces:**
- `prepare_messages(question, passages) -> list[dict[str, str]]`
- `improve(question, passages) -> list[dict]`

- [ ] **Step 1: Write failing tests** asserting messages contain only the supplied question/passages, request a JSON object with `answer` and `citations`, preserve passage IDs, and make the improved path a deterministic content-based reordering/selection rather than an identity placeholder.
- [ ] **Step 2: Run the focused tests** and confirm they fail against the starter implementation.
- [ ] **Step 3: Implement minimal prompt construction** with explicit evidence insufficiency behavior, citation-ID-only output, and stable formatting.
- [ ] **Step 4: Implement deterministic `improve`** using query-term overlap and original-order tie breaking; never use case IDs, expected answers, or dev-answer files.
- [ ] **Step 5: Run focused tests and the supplied dry-run command**; preserve generated request artifacts outside tracked secrets.
- [ ] **Step 6: Commit** `feat: add evidence-grounded basic task pipeline`.

### Task 3: Run and score the basic task

**Files:**
- Create: `runs/basic/`
- Create: `results/results.csv`
- Create: `results/scoring/basic_scoring.md`
- Create: `results/basic_summary.md`

- [ ] **Step 1: Run development cases D01-D04 in dry-run mode** and verify request construction before any paid call.
- [ ] **Step 2: Freeze provider/model/prompt/config hashes** in a run manifest.
- [ ] **Step 3: Run the 32 baseline paired requests and 8 improved R0 requests**, keeping failures and retries as separate records.
- [ ] **Step 4: Evaluate every required case** for answer correctness, citation origin, semantic support, insufficiency handling, and client elapsed time.
- [ ] **Step 5: Run one diagnostic check and one no-model ordering/ID remapping check**, recording predictions before observations.
- [ ] **Step 6: Commit** `data: record basic task experiments and scoring`.

### Task 4: Reproduce and characterize the B baseline fault

**Files:**
- Create: `runs/advanced_b/baseline.json`
- Create: `runs/advanced_b/predictions.md`
- Create: `results/advanced_b_diagnosis.md`
- Create: `tests/test_baseline_faults.py`

- [ ] **Step 1: Write failing regression tests** for a scope-local match being displaced by an out-of-scope higher-ranked entry, changed snapshot returning cached old evidence, and invalid citations being reported as verified.
- [ ] **Step 2: Run tests against `challenge:Engine`** and capture the baseline failures.
- [ ] **Step 3: Record two still-plausible causes per selected symptom** with distinct predicted observations before changing code.
- [ ] **Step 4: Run `challenge_b/run_cases.py --output runs/advanced_b/baseline.json`** and preserve the raw output.
- [ ] **Step 5: Run a discriminating input-order/scope/snapshot intervention** to separate ranking, filtering, and cache-key explanations.
- [ ] **Step 6: Commit** `test: capture advanced B baseline failures`.

### Task 5: Implement the minimal B repair

**Files:**
- Create: `进阶/challenge_b/fixed_engine.py`
- Create: `tests/test_fixed_engine.py` updates
- Create: `进阶/challenge_b/README.md`

**Interfaces:**
- `fixed_engine.Engine.__init__() -> None`
- `fixed_engine.Engine.evaluate(request, corpus, draft) -> dict`

- [ ] **Step 1: Extend failing tests** for exact scope validation, scope-first positive ranking, cache keys including normalized query/doc IDs/snapshot/k, defensive copies, unique request IDs, and honest locator/support states.
- [ ] **Step 2: Run the tests against the untouched baseline** and confirm the expected failures.
- [ ] **Step 3: Implement scope validation and scope-first ranking** with `invalid_scope` for unknown document/snapshot combinations and no out-of-scope evidence.
- [ ] **Step 4: Implement a complete cache key** and ensure cached responses update per-request metadata without changing evidence scope.
- [ ] **Step 5: Implement citation validation** as locator-only `valid/invalid/absent`; use `not_checked` for semantic support unless an independently justified rule can prove it.
- [ ] **Step 6: Add current request/source evidence fields and defensive copying** while retaining the original Engine interface.
- [ ] **Step 7: Run all B tests and offline replay with `--engine fixed_engine:Engine`**.
- [ ] **Step 8: Commit** `fix: repair scope cache and citation states in B engine`.

### Task 6: Verify B regressions, variants, and boundaries

**Files:**
- Create: `runs/advanced_b/fixed.json`
- Create: `runs/advanced_b/comparison.csv`
- Create: `results/advanced_b_regression.md`
- Create: `results/advanced_b_variants.md`

- [ ] **Step 1: Run two normal regression cases** and assert unchanged expected behavior.
- [ ] **Step 2: Run two semantic-equivalent variants** covering reordered document IDs and reordered corpus records.
- [ ] **Step 3: Run one unresolved or explicitly rejected boundary case** such as semantic support not being implemented by the offline engine.
- [ ] **Step 4: Compare baseline/fixed outputs under identical inputs** and record status changes, evidence, and elapsed time.
- [ ] **Step 5: Commit** `data: record B repair regressions and variants`.

### Task 7: Write integrated report, README, declaration, and submission metadata

**Files:**
- Create: `report.md`
- Create: `declaration.md`
- Create: `decisions.md`
- Modify: `README.md`
- Create: `SUBMISSION.md`

- [ ] **Step 1: Write the report** with completed/incomplete scope, source reading, hypotheses, controls, baseline, implementation, per-case results, failures, variants, boundaries, and next-step decision.
- [ ] **Step 2: Add three decision records** containing original judgment, alternative, falsifier, AI/other influence, evidence, and final decision; mark retrospective entries honestly.
- [ ] **Step 3: Add the AI declaration** covering use in reading, implementation, debugging, and verification, plus personal validation steps.
- [ ] **Step 4: Update README** with direction `Agent`, selected advanced task `B`, setup, commands, result locations, source commit, final branch, and final commit placeholder.
- [ ] **Step 5: Run a repository secret scan and verify no private endpoint/config is tracked.**
- [ ] **Step 6: Commit** `docs: add assessment report and submission metadata`.

### Task 8: Final verification and GitHub delivery preparation

- [ ] **Step 1: Run the full standard-library test suite.**
- [ ] **Step 2: Run both baseline and fixed B replays from a clean working tree.**
- [ ] **Step 3: Recalculate result counts, hashes, and final commit SHA.**
- [ ] **Step 4: Update README/SUBMISSION with the final branch and SHA.**
- [ ] **Step 5: Confirm GitHub remote/fork access and push the final branch.**
- [ ] **Step 6: Re-run the final verification commands after the final commit and report any blocked external step explicitly.**
