# TalentModel-skill

> 🎯 **岗位胜任力建模工具** — 通过交互式配置向导，基于候选人画像而非技能清单，生成三层结构（核心维度→可观察行为→角色证据）的胜任力模型报告。

📄 **English version:** [README_en.md](README_en.md)

---

## 🤖 Agent 推荐工作流

> 🤖 Agent 执行 Skill 时的推荐工作路径，从读 SKILL.md → 生成并迭代 HTML 报告

**在线预览（可导出 SVG/PNG）：** [assets/agent-workflow.html](assets/agent-workflow.html)

<!--
  GitHub README 不执行 ECharts 脚本，请访问上方 agent-workflow.html 在线预览完整交互图表。
  可在浏览器中右键图表 → 存储为 PNG，或使用导出工具生成 SVG。
  截图备选（请替换为实际截图路径）：
  ![Agent 工作流](assets/agent-workflow.png)
-->

---

## ⚡ For Agents & LLMs

> **Don't read this README. Load `SKILL.md` instead.**
>
> `SKILL.md` is the authoritative entry point. This file is human-facing documentation.

### How to use this skill

**Entry point:** `SKILL.md`

**Minimal invocation (chat):**
```
Use the TalentModel-skill. Target role: [岗位名称], Level: [校招/实习/资深/管理], Scenario: [招聘/面试/晋升], Companies: [公司A, 公司B, ...]
```

**Required config:**
| Parameter | Values | Notes |
|-----------|--------|-------|
| `ROLE_NAME` | any string | e.g. "AI Infra工程师" |
| `TALENT_LEVEL` | `校招` / `实习` / `资深专家` / `管理者` | |
| `USE_CASE` | `招聘筛选` / `面试设计` / `晋升评估` | |
| `VALIDATION_COMPANIES` | 3–8 company names | Mix of types (big tech + vertical + traditional). See `test_cases/ENTERPRISE_REFERENCE.md` for valid options. |

**Optional config:**
| Parameter | Default | Notes |
|-----------|---------|-------|
| `OUTPUT_FORMAT` | `html` | HTML报告（含4种图表），唯一输出格式 |
| `SELF_CHECK_MATRIX` | `false` | 3-tier self-assessment table |
| `CHART_RENDER` | `offline` | echarts bundled locally |

**Key constraints you must follow:**
- **No radar/bar/line/pie charts.** Only `sunburst`, `treemap`, `scatter`, `tree`.
- **No quantitative values in charts.** No `value:` numbers, no axis `min/max`, no percentages — competence models have no measurement data.
- **Mandatory intermediate artifact verification.** Signal table (≥15 rows with judgment + demotion reason columns) and URL validation (WebFetch confirmed) must pass before drafting dimensions.
- **3-level structure is mandatory.** Dimension → Observable Behavior → Evidence. Never skip levels or collapse them.
- **Verify before reporting.** Check the post-generation checklist in `SKILL.md` before returning the report.

**MCP integration (optional):**
If your agent harness supports MCP, add this to your `mcp.json`:
```json
{
  "mcpServers": {
    "talent-model": {
      "command": "npx",
      "args": ["-y", "@codebuddy/talent-model-mcp"]
    }
  }
}
```
Agents can then invoke the skill as a native MCP tool without reading SKILL.md directly.

**File layout:**
```
TalentModel-skill/
├── SKILL.md                        # ← Load this (entry point)
├── assets/
│   ├── echarts.min.js               # ECharts 图表库（离线渲染）
│   ├── config_template.txt          # 配置模板
│   ├── agent-workflow.html          # Agent 推荐工作流（可导出 SVG/PNG）
│   └── examples/                    # 示例文件
│       ├── ai_infra_campus.txt      # 示例对话输出
│       └── sunburst-comparison*.html # 图表方案对比示例
└── references/                      # 参考文档（按需加载）
    ├── html_template.md              # HTML 报告模板（含 CSS/JS）
    ├── enterprise_reference.md       # 按类型分类的验证公司参考列表
    └── test_cases.md                # 验证测试用例
```

**Raw content URLs (fetch directly):**
- SKILL.md: `https://raw.githubusercontent.com/Liber1917/TalentModel-skill/master/SKILL.md`
- TEST_CASES: `https://raw.githubusercontent.com/Liber1917/TalentModel-skill/master/references/TEST_CASES.md`
- ENTERPRISE_REFERENCE: `https://raw.githubusercontent.com/Liber1917/TalentModel-skill/master/references/ENTERPRISE_REFERENCE.md`

---



## 快速开始

### 下载

```bash
# 克隆仓库
git clone https://github.com/Liber1917/TalentModel-skill.git

# 或下载 ZIP
# https://github.com/Liber1917/TalentModel-skill/archive/refs/heads/main.zip
```

### 安装

将 `TalentModel-skill` 目录添加到你的 agent skills 路径：

```bash
# 方法1: 链接到工作目录
ln -s /path/to/TalentModel-skill <your-agent>/skills/talent-model

# 方法2: 直接复制
cp -r TalentModel-skill <your-agent>/skills/talent-model
```

### 使用

在 agent 对话中输入：

```
@talent-model
```

或直接描述需求：

> "帮我做一个 AI Infra 的胜任力模型"

---

## 功能特性

### 核心功能

| 功能 | 说明 |
|------|------|
| 🎯 **交互式配置向导** | 10步引导式配置，带智能提示和意图识别 |
| 📐 **MECE 结构建模** | 6维胜任力框架，避免技能树陷阱 |
| ✅ **官网验证** | 基于真实招聘页面交叉验证胜任力模型（URL 强制 WebFetch 验证） |
| 📊 **4种可视化图表** | 旭日图、矩形树图、散点图、能力树 |
| 🧭 **人才分型象限** | 识别潜力型/达标型/突出型/平台型人才 |
| 📝 **行为锚点表格** | 可观察行为的具体判定标准 |
| 🔒 **强制中间产物验证** | Step 3.5 信号归纳表 + Step 4 维度黑名单扫描 + Step 9 报告自检，三阶段门控 |
| 🛡️ **防幻觉约束** | 维度黑名单扫描、URL 验证硬约束、跳过验证阻断 |

### 可选功能

| 功能 | 说明 | 启用方式 |
|------|------|----------|
| 📈 **自测矩阵** | 三水位对照（🌱起步/⚡达标/🔥突出） | 配置阶段选择 |
| 🖼️ **图表导出** | PNG / SVG / JPEG 多格式下载 | 悬停即可导出 |
| 📦 **离线渲染** | 内嵌 echarts.min.js，无需网络 | 配置阶段选择 |

---

## 配置参数

### 必需参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `ROLE_NAME` | 目标岗位名称 | AI Infra工程师 |
| `TALENT_LEVEL` | 人才级别 | 校招 / 实习 / 资深专家 / 管理者 |
| `USE_CASE` | 使用场景 | 招聘筛选 / 面试设计 / 晋升评估 |
| `VALIDATION_COMPANIES` | 验证公司列表 | OpenAI, NVIDIA, ByteDance... |

### 可选参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `OUTPUT_FORMAT` | 输出格式 | `html`（已锁定，不可更改） |
| `SELF_CHECK_MATRIX` | 自测矩阵 | `false` |
| `CHART_RENDER` | 图表渲染方式 | `offline` |

### 配置示例

创建 `config.txt` 或在对话中提供：

```
ROLE_NAME = AI Infra工程师
TALENT_LEVEL = 校招
USE_CASE = 招聘筛选
VALIDATION_COMPANIES = OpenAI, NVIDIA, ByteDance, 阿里云
OUTPUT_FORMAT = html
SELF_CHECK_MATRIX = true
CHART_RENDER = offline
```

---

## HTML 报告使用

### 文件说明

当选择 **HTML报告** 输出格式时，会生成：

| 文件 | 说明 | 必需 |
|------|------|------|
| `{岗位名称}_胜任力模型.html` | 主报告文件 | ✅ |
| `echarts.min.js` | ECharts 图表库（离线模式） | 仅离线模式 |

### 使用步骤

1. **确保文件在同一目录**
   ```
   工作目录/
   ├── AI_Infra工程师_胜任力模型.html
   └── echarts.min.js          ← 离线模式必需
   ```

2. **用浏览器打开 HTML 文件**
   - 双击或拖入浏览器
   - 支持 Chrome、Edge、Firefox、Safari

3. **导出图表**
   - 鼠标悬停在图表区域
   - 右上角出现导出按钮
   - 支持 PNG / SVG / JPEG 格式

4. **离线使用**（离线模式）
   - 报告完全离线可用
   - 所有图表通过本地 `echarts.min.js` 渲染

### 注意事项

- CDN 模式需要网络连接，但图表更清晰
- 离线模式文件更大，但完全自包含
- 如需分享报告，离线模式请同时分享两个文件

---

## 更新日志

### v1.3.0 (2026.04)

> **Agent 约束工程专项升级**

**P0 修复：**
- 🔒 **HTML-only 输出锁定** — 移除 Markdown 和面试评分表选项，所有输出强制为 HTML 报告（含4种图表）
- 🛡️ **消除隐性模板风险** — 移除 Step 4 中"参考结构"作为预设维度的暗示，改为强制基于信号归纳表起草
- 📋 **信号归纳表结构化强制模板** — 必须输出 ≥15 行表格，含"判断"列和"降级原因"列，禁止仅用文字描述
- 🔗 **验证链接 WebFetch 硬约束** — 禁止生成未验证的 URL，禁止推测/编造链接，规定标准降级策略

**P1 增强：**
- ✅ **中间产物验证机制** — Step 3.5 / Step 4 / Step 9 三阶段验证，维度黑名单关键词扫描
- 🌐 **WebFetch 失败标准降级行为** — 定义无公开入口时的明确处理方式
- 🧭 **维度分类 Few-shot 示例** — 提供特质 vs 技能/工具/行为的判断标准和示例
- 📝 **失败模式防范扩展** — 新增"验证链接幻觉"和"跳过中间验证"两类防范条目

**其他：**
- workflow.type 改为 `pipeline`，validation 改为 `mandatory`
- Q8 输出格式描述更新，Q8.5 限定语移除
- 完整示例对话更新以反映新流程

### v1.2.0 (2026.04)

- 🛡️ 6个硬约束失败模式（技能维度陷阱、校招/社招边界、图表类型禁止、图表量化幻觉等）
- 📋 报告生成后自检清单
- ⚡ For Agents & LLMs 区块，含 MCP 集成说明
- 🎨 HTML 模板嵌入 ECharts 配置示例
- 🔍 ENTERPRISE_REFERENCE.md — 四类企业参考库（互联网大厂/中型成长期/垂直龙头/传统行业）

### v1.0.0 (2026.04)

- 🎉 初始版本发布
- 🎯 交互式配置向导
- 📐 MECE 六维胜任力框架
- ✅ 官网验证机制
- 📊 4种可视化图表（旭日图、矩形树图、散点图、能力树）
- 🧭 人才分型象限 + 行为锚点表格
- 📈 可选自测矩阵（三水位：🌱起步/⚡达标/🔥突出）
- 🖼️ 图表导出功能（PNG / SVG / JPEG）
- 📦 离线/CDN 双渲染模式

---

## 项目结构

```
TalentModel-skill/
├── SKILL.md                        # 技能入口点（Agent 必读）
├── README.md                       # 中文说明文档
├── assets/                         # 静态资源
│   ├── echarts.min.js               # ECharts 图表库（离线渲染）
│   ├── config_template.txt          # 配置模板
│   └── examples/                    # 示例文件
│       ├── ai_infra_campus.txt      # 示例对话输出
│       ├── sunburst-comparison*.html # 图表方案对比示例
│       └── dev-roadmap.html          # 版本演进路线图 × Agent 工作流
└── references/                     # 参考文档（按需加载）
    ├── html_template.md              # HTML 报告模板（含 CSS/JS）
    ├── enterprise_reference.md        # 按类型分类的验证公司参考列表
    └── test_cases.md                # 验证测试用例
```

---

## 核心原则

> **胜任力模型不是整理后的职位描述。**
>
> **它是对"组织真正想识别什么样的人"的结构化判断。**
>
> **先建模人，再映射行为，最后验证证据。**

---

## 参考资料

- [MECE 原则](https://en.wikipedia.org/wiki/MECE_principle) — 相互独立，完全穷尽
- [行为事件访谈法 (BEI)](https://wiki.mbalib.com/wiki/%E8%A1%8C%E4%B8%BA%E4%BA%8B%E4%BB%B6%E8%AE%BF%E8%B0%88%E6%B3%95) — 揭示胜任特征的主要工具（MBA智库百科）

---

## 许可证

MIT
