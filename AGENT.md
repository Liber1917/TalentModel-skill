# AGENT.md — TalentModel-skill 开发规范

> 本项目使用 Agent-Aware Git 工作流。
> 所有变更遵循 atomic commit + commit trailer 规范。

---

## Git 工作流

### 分支策略

- **main**：稳定版本，只接受 PR 合并
- **feature/v2.0-lacanian**：v2.0 开发分支（当前活跃）
- 分支命名：`agent/<task-id>-<description>`

### Commit 规范

每个 commit 必须包含：

```
<type>(<scope>): <summary>

[可选正文]

Agent-Task: <任务描述>
Agent-Model: <模型标识>
```

**类型前缀**：
- `feat`：新功能（Phase 0L 拉康画像 / Phase 5 双Agent精炼 等）
- `refactor`：重构（方法论整合 / 流程重组）
- `docs`：文档更新
- `fix`：修复验证问题
- `chore`：工具/依赖更新

**Commit Trailer**：
- `Agent-Task:` 描述本 commit 对应的任务
- `Agent-Model:` 使用的模型

### PR 要求

使用 `.github/pull_request_template/agent.md` 模板，PR 中必须包含：
- Task Description
- Agent Context（权衡了哪些方案）
- Changes Made
- Testing（跑了哪些验证）
- Related Issues

---

## Skill 开发规范

### Phase 流程

```
Phase 0（入口）→ Phase 0.5（目录创建）→ Phase 1（6-Agent并行）→
Phase 1.5（Review checkpoint）→ Phase 2（提炼）→ Phase 2.5（提炼确认）→
Phase 3（构建）→ Phase 4（质量验证）→ Phase 5（双Agent精炼）
```

**强制 checkpoint**：
- Phase 1.5：调研 Review 检查点（展示来源统计表，用户确认后才推进）
- Phase 2.5：提炼确认检查点（展示心智模型/矛盾张力/诚实边界，用户确认后才推进）
- Phase 4：质量自检清单逐项验证（禁止跳过）

### 引用文件管理

- `references/` 目录存放方法论和模板
- `references/research/` 目录存放 Agent 调研产物
- Skill 目录必须是**自包含**的，复制整个目录就能独立使用

### 维度起草规则

- 一级维度**禁止**是技能/工具/技术栈
- 一级维度**禁止**是岗位职责拆分
- 必须通过三重验证（跨域复现/生成力/排他性）
- 数量强制为 **6个，不多不少**

### 拉康画像规范（Phase 0L）

- 核心原则：不问「优点是什么」，问「你是怎么注意到这件事的」
- 记录原话，不归纳成性格标签
- 保留矛盾，不强行调和
- 观察叙事缺口，捕捉实在界信号

---

## 失败模式速查

| 陷阱 | 防范 |
|------|------|
| 技能维度陷阱 | 扫描维度名称，不含 Python/Go/CUDA/K8s 等词 |
| 大厂偏差 | Q7 验证公司必须覆盖≥2种企业类型 |
| 图表惯性漂移 | 检查 HTML 中不出现 radar/bar/line/pie |
| 量化幻觉 | 检查图表中无精确数值 value/min/max |
| 旭日图文字堆叠 | 只显示 D1 维度名（二级折叠） |
| 降级说明缺失 | HTML 报告必须有显式「降级说明」节 |
| 跳过 checkpoint | Phase 1.5 和 2.5 强制执行，用户确认后才推进 |

---

## 运行时环境

- Node/Python：用于质量检查脚本
- ECharts 5.4.3（CDN：jsdelivr → unpkg → 本地 fallback）
- macOS Zsh 环境
