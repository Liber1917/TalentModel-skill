# TalentModel-skill

> 🎯 **岗位胜任力建模工具** — 通过交互式配置向导，基于候选人画像而非技能清单，生成三层结构（核心维度→可观察行为→角色证据）的胜任力模型报告。

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
| `OUTPUT_FORMAT` | `html` | HTML report with 4 charts |
| `SELF_CHECK_MATRIX` | `false` | 3-tier self-assessment table |
| `CHART_RENDER` | `offline` | echarts bundled locally |

**Key constraints you must follow:**
- **No radar/bar/line/pie charts.** Only `sunburst`, `treemap`, `scatter`, `tree`.
- **No quantitative values in charts.** No `value:` numbers, no axis `min/max`, no percentages — competence models have no measurement data.
- **3-level structure is mandatory.** Dimension → Observable Behavior → Evidence. Never skip levels or collapse them.
- **Verify before reporting.** Check the post-generation checklist in `SKILL.md` before returning the report.

**File layout:**
```
TalentModel-skill/
├── SKILL.md                        # ← Load this
├── test_cases/
│   ├── TEST_CASES.md               # Validation test suite
│   └── ENTERPRISE_REFERENCE.md      # Valid company list by type
├── prompts/
│   ├── config_wizard.md
│   └── report_builder.md
└── templates/
    └── report.html
```

**Raw content URLs (fetch directly):**
- SKILL.md: `https://raw.githubusercontent.com/Liber1917/TalentModel-skill/master/SKILL.md`
- TEST_CASES: `https://raw.githubusercontent.com/Liber1917/TalentModel-skill/master/test_cases/TEST_CASES.md`
- ENTERPRISE_REFERENCE: `https://raw.githubusercontent.com/Liber1917/TalentModel-skill/master/test_cases/ENTERPRISE_REFERENCE.md`

---



## 快速开始

### 下载

```bash
# 克隆仓库
git clone https://github.com/yourusername/TalentModel-skill.git

# 或下载 ZIP
# https://github.com/yourusername/TalentModel-skill/archive/refs/heads/main.zip
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
| ✅ **官网验证** | 基于真实招聘页面交叉验证胜任力模型 |
| 📊 **4种可视化图表** | 旭日图、矩形树图、散点图、能力树 |
| 🧭 **人才分型象限** | 识别潜力型/达标型/突出型/平台型人才 |
| 📝 **行为锚点表格** | 可观察行为的具体判定标准 |

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
| `OUTPUT_FORMAT` | 输出格式 | `html` |
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
├── SKILL.md              # 技能入口点
├── README.md             # 本文件
├── config_template.txt   # 配置模板
├── prompts/             # 提示模板
│   ├── config_wizard.md  # 配置向导
│   └── report_builder.md # 报告生成器
├── templates/            # HTML 模板
│   └── report.html       # 报告模板
└── examples/             # 示例
    └── ai_infra_campus.txt
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
