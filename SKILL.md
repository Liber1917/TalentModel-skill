---
name: talent-model
description: "岗位胜任力建模工具：通过交互式配置向导，基于候选人画像而非技能清单，生成三层结构（核心维度→可观察行为→角色证据）的胜任力模型报告。支持HTML可视化输出。Competency model builder with interactive config, MECE structure, official validation, and HTML reports."
license: MIT

# MCP Server Configuration (for agent harness integration)
# Add to your ~/.workbuddy/mcp.json:
# {
#   "mcpServers": {
#     "talent-model": {
#       "command": "npx",
#       "args": ["-y", "@codebuddy/talent-model-mcp"]
#     }
#   }
# }
# Agents can then call this skill as a native MCP tool.

compatibility:
  web-access: required    # Step 3.5 needs web fetch for company validation
  offline-render: true    # echarts.min.js bundled for HTML export
  mcp-native: true        # callable as MCP tool if server is configured

allowed-tools:
  Read:       mandatory   # read SKILL.md, prompts/, templates/
  Write:      mandatory   # write report output
  Bash:       optional    # copy echarts.min.js, run local servers
  WebFetch:   mandatory   # fetch job pages for validation (Step 3.5)
  WebSearch:  optional    # research company context

workflow:
  type: interactive       # guided 10-step wizard (cannot skip)
  output: html            # primary output format
  validation: post-hoc    # self-check checklist after generation

constraints:
  chart-types: [sunburst, treemap, scatter, tree]
  chart-forbidden: [radar, bar, line, pie]
  chart-no-quantitative: true    # no value:/min:/max: in echarts config
  structure: three-level         # Dimension → Behavior → Evidence

metadata:
  version: "1.1.0"
  category: "hr"
  emoji: "🎯"
  author: "Liber1917"
  repository: "https://github.com/Liber1917/TalentModel-skill"
---

# Competency Model Skill — 岗位胜任力建模

## 核心原则

**胜任力模型不是整理后的职位描述，而是对"组织真正想识别什么样的人"的结构化判断。**

建模顺序：
1. **先建模"人"** — 识别稳定、可迁移的特质
2. **再映射行为** — 这些特质如何表现
3. **最后验证证据** — 用角色场景佐证

**禁止反向操作**：不要从工具栈或JD bullet points直接组装画像。

**维度层级约束（硬约束）：**
- ❌ **一级维度禁止是技能/工具/技术栈**（如"系统抽象能力""硬件感知""编程语言"）
- ❌ **一级维度禁止是岗位职责的拆分**（如"需求分析""项目管理"是一级 → 这是行为，不是维度）
- ✅ **一级维度必须是人的稳定特质**（如：方向感、高驱动力、认知复杂度、韧性、协作意识、专业成长性）
- ✅ **行为（二级）才是技能和岗位任务的落脚点** — 行为描述中可以包含技能要求，但维度本身不能是技能

> **原因**：大模型倾向从JD关键词提炼维度，容易把"Python/Go"或"系统设计"直接当成一级维度，导致胜任力模型退化为职位描述。维度必须是对"什么样的人"的判断，而非"需要什么技能"的枚举。

**校招/实习边界约束（硬约束）：**
- ❌ **验证公司信息严禁使用社招JD**（如 LinkedIn Senior/5年经验 等）
- ❌ **禁止用资深岗位描述反推校招/实习标准**（典型失败模式：把"5年系统设计经验"→"需要很强的系统思维"→"系统设计"作为校招核心维度）
- ✅ **只允许使用校招/实习入口**：各公司 careers 页面的 campus/graduate/intern 板块，或招聘官网标注"应届"的岗位
- ✅ **校招维度以"潜力"和"可塑性"为核心**：衡量的是"能否长成"，不是"当前会什么"
- ✅ **社招/晋升评估场景**才允许使用5年+ JD，此时维度应以"当前交付能力"为核心

> **原因**：校招与社招的核心差异是"用人标准"而非"技能清单"。用社招JD反推校招是极高发的失败模式，必须硬性约束。

---

## 交互式配置向导

当用户请求构建胜任力模型时，**必须**按以下顺序引导用户填写配置，**不能跳过任何字段**。

### Step 0: 企业分布探索【前置，建模前必做】

**在进入配置向导之前**，先用 WebFetch 搜索该岗位在市场上的企业分布情况。

**目的：** 建立对"哪些类型的企业招这个岗位"的基本认知，避免默认大厂偏差，确保后续验证公司列表（Q7）覆盖多元类型。

**执行方式：**
```
搜索关键词（可调整）：
  - "{岗位名} 招聘 行业分布"
  - "{岗位名} 哪些公司招聘"
  - "{role_name} job market company types"

目标：了解以下4类企业是否招聘该岗位：
  1. 互联网大厂（字节、阿里、腾讯、谷歌等）
  2. 中型/成长期公司（独角兽、上市中型企业）
  3. 垂直行业龙头（金融、医疗、制造、教育等行业的头部公司）
  4. 传统行业/非互联网企业（国企、外资、传统制造等）
```

**输出要求：** 告知用户探索结论，例如：
```
【企业分布探索结论】
"后端开发工程师"在以下类型企业广泛分布：
  ✓ 互联网大厂 — 核心技术岗（代表：ByteDance、Alibaba）
  ✓ 金融科技公司 — 核心系统开发（代表：平安科技、招银网络）
  ✓ 传统金融机构 — 银行/保险IT部门（代表：工商银行软件中心）
  ✓ 制造业/工业互联网 — 系统集成（代表：华为、中车）
  ✓ 企业服务SaaS — 产品后端（代表：用友、金蝶）

→ Q7 验证公司将从以上5类中各选至少1家，避免单一互联网视角。
```

**⚠️ 强制约束：** 如果用户提供的 Q5 行业背景不是"互联网"，验证公司列表中互联网大厂占比不得超过 50%。

---

### Step 1: 意图识别

首先判断用户想要什么：

```
用户输入分析：
- 如果提到"校招/实习/应届生" → TALENT_LEVEL = 校招
- 如果提到"面试题/评估表" → USE_CASE = 面试设计
- 如果提到"晋升/发展" → USE_CASE = 晋升评估
- 如果提到"HTML/图表/可视化" → OUTPUT_FORMAT = html
```

### Step 2: 逐项配置（带智能提示）

**必须逐个字段询问，每字段提供填写提示和示例。**

#### Q1: 目标岗位名称
```
提示：具体岗位名称，如"产品经理"、"销售总监"、"软件工程师"
示例：产品经理 / 客户成功经理 / 算法工程师 / 运营专员
```

#### Q2: 人才级别 ⚠️【关键区分点】
```
选项：
  A. 校招/实习 — 侧重潜力、基础素质、学习敏捷
  B. 应届生 — 侧重成长空间、主动性、工程基础
  C. 1-3年经验 — 侧重执行力、专业深度
  D. 资深专家 — 侧重判断力、系统思维、影响力
  E. 管理者 — 侧重组织判断、人才杠杆、战略对齐

⚠️ 警告：不要用资深社招标准去要求校招生！
```

#### Q3: 使用场景
```
选项：
  - 招聘筛选 — 用于简历筛选和初面评估
  - 面试设计 — 用于设计面试问题和评分表
  - 能力发展 — 用于制定培养计划
  - 晋升评估 — 用于晋升答辩和校准
  - 人才盘点 — 用于团队能力盘点
```

#### Q4: 角色范围/业务边界
```
提示：界定岗位的职责边界
示例：企业级SaaS产品销售 / 用户增长运营 / 后端服务开发
```

#### Q5: 行业背景
```
提示：行业特性会影响胜任力侧重点
示例：金融科技 / 电商/零售 / 企业服务 / 医疗健康
```

#### Q6: 目标地区
```
提示：影响验证公司的选择
示例：中国 / 全球 / 北美 / 亚太
```

#### Q7: 验证公司列表
```
提示：基于 Step 0 企业分布探索结论，从不同类型企业中各选 1-2 家

【强制多元化规则】
  ✅ 必须覆盖：至少 2 种企业类型（从以下5类中选）
     - 互联网大厂（Google/ByteDance/Tencent 等）
     - 中型/成长期公司（独角兽、上市中型）
     - 垂直行业龙头（金融/医疗/制造/教育行业头部）
     - 传统行业企业（国企/外资/传统制造等）
     - 专业服务公司（咨询/SaaS/企业服务等）
  ❌ 禁止：验证公司全部来自互联网大厂（除非用户明确指定）

示例（后端开发工程师 · 互联网+金融）：
  - 互联网大厂：ByteDance, Tencent
  - 金融科技：平安科技, 招银网络科技
  - 传统金融IT：工商银行软件中心
  - 企业服务：用友网络

示例（后端开发工程师 · 制造业）：
  - 制造业龙头：华为, 中联重科
  - 工业互联网：海尔工业互联（卡奥斯）, 树根互联
  - 互联网大厂（参照）：Alibaba Cloud（仅作上限参照，非主要对标）

⚠️ 优先选择有公开招聘入口的企业，校招场景优先选有校招专页的
```

#### Q8: 输出格式
```
选项：
  - HTML报告 — 带可视化图表的完整报告（推荐）
  - Markdown — 结构化文本
  - 面试评分表 — 面试问题与评分标准
```

#### Q8.5: 图表渲染方式 【仅当选择HTML时】
```
选项：
  - 完全离线 — 使用内嵌的 echarts.min.js，无需网络（推荐）
  - 外部CDN — 使用 CDN 加载 ECharts，报告更轻量但需要网络

提示：完全离线版可分享给无网络环境的同事；CDN 版文件更小、图表版本更新。
```

#### Q9: 语言
```
选项：中文 / English
```

#### Q10: 特殊要求（可选）
```
提示：任何特殊约束或偏好
示例：
  - 必须包含：高目标、自驱力、韧性
  - 必须避免：技能清单、量化权重
  - 图表风格：管理咨询式人才评估报告
```

### Step 3: 配置确认与校准

汇总用户填写的内容，展示完整配置，并做智能校验：

```
【配置确认】
岗位：产品经理
级别：校招/实习 ⚠️
场景：招聘筛选
范围：企业级SaaS产品
行业：企业服务
地区：中国+全球
验证公司：Google, Microsoft, ByteDance, Alibaba, Tencent...
输出：HTML报告
图表渲染：完全离线（内嵌echarts.min.js）
语言：中文

【智能校验】
✓ 校招级别已选择，将侧重潜力与基础素质
✓ 验证公司包含多家校招入口，适合交叉检验
⚠ 提醒：输出将避免技能清单陷阱，聚焦人才画像

【可选功能】
□ 添加自测矩阵（三水位：起步/达标/突出）— 适用于候选人有自测需求的场景

请确认或修改：
[确认] [修改配置]
```

---

## 执行流程（11步标准序列）

配置确认后，严格按照以下顺序执行：

### Step 1: 任务框架确定
- 明确建模类型：候选人画像模型（默认）
- 确认人才级别和使用场景
- 设定输出格式要求

### Step 2: 人才级别校准
根据Q2的选择，调整期望重点：

**校招/实习/应届生：**
- 强调：成长潜力、学习敏捷、基础素质、主动性、韧性、协作准备度
- 避免：成熟所有权意识、完整战略判断

**资深专家：**
- 强调：判断力、复杂度处理、持续执行、专业深度、超越自我的影响力

**管理者：**
- 强调：人才杠杆、组织判断、模糊决策、战略对齐、团队赋能

### Step 3: 分离画像与证据
- 画像：描述"人"的稳定特质
- 证据：角色场景中的具体表现
- **关键**：工具/平台属于证据层，不要提升为一级维度

### Step 3.5: 企业信息采集【⚠️ 在起草维度之前执行，不可跳过】

**目的：让证据塑造结论，而不是让先验框架去找证据支持。**

使用 Q7 确定的多元化验证公司列表，访问官方招聘页面，**在起草维度之前**收集原始信息：

**采集对象：**
- 各公司对该岗位的招聘描述（JD）
- 校招/实习入口中对人才的表述（优先）
- 不同类型企业之间的共性和差异

**采集重点（只观察，不组装）：**
```
从各类型企业的 JD 中，找出：
  1. 反复出现的词汇 → 候选维度信号
  2. 仅大厂提到的词汇 → 大厂特有，降为证据层
  3. 传统行业/垂直行业强调而大厂不提的 → 行业特定维度信号
  4. 所有类型企业都提到的 → 跨公司稳定特质，核心维度候选
```

**输出一份「原始信号归纳表」：**

| 信号词 | 大厂 | 中型 | 垂直行业 | 传统行业 | 出现频率 |
|--------|------|------|----------|----------|----------|
| 例：系统设计能力 | ✓ | ✓ | ✓ | ✓ | 跨类型稳定 → 核心维度 |
| 例：高并发经验 | ✓ | ✓ | — | — | 大厂/中型特有 → 证据层 |
| 例：合规意识 | — | — | ✓（金融） | ✓（金融） | 行业特定 → D3 替换词 |

**禁止**：不要用 JD bullet points 直接组装模型。

**优先顺序：**
1. 官方校招页面
2. 官方实习页面
3. 官方 careers 页面
4. 具体岗位页面（仅作上限参照）

### Step 4: 起草一级维度
**基于 Step 3.5 的原始信号归纳表**，而非基于预设框架，提出6个MECE主维度候选：

**参考结构（可被信号表推翻，非固定模板）：**
1. 方向与标尺 — 目标感、长期思维、质量标准
2. 内驱与主动 — 自驱力、主动性、闭环意识
3. 韧性与稳定性 — 抗压、恢复力、持续推进
4. 认知与进化 — 系统思维、学习敏捷、抽象迁移
5. 专业成熟度 — 知识结构、工程判断、场景证据
6. 协作与影响 — 跨团队协作、影响力、表达信任

**如果信号表显示某维度有行业特定替换词，在此步骤直接替换，不要保留通用措辞。**

### Step 5: MECE压力测试
对每个候选维度问：
- 它描述的是稳定特质还是临时技能？
- 它能解释真实的选择差异吗？
- 它与相邻维度有明显区别吗？
- 它应该是一级维度、行为还是证据？
- **新增**：它是跨企业类型稳定存在的，还是只有大厂才强调的？

**删除或降级**不符合标准的维度。

### Step 6: 构建可观察行为
为每个一级维度设计2-3个二级行为：
- 回答："如何在真实候选人身上识别这个维度？"
- 使用可观察、可验证的行为描述

### Step 7: 映射角色证据
为每个二级行为添加三级证据：
- 回答："在这个角色中，什么经历/产出能证明？"
- 将工具/平台/框架放在这一层

### Step 8: 边界精炼（扬弃反思）【原官网验证已前移至 Step 3.5】
基于 Step 3.5 采集的多元企业信息，对已起草的模型进行批判性校验：

**「扬」— 保留并强化的内容：**
- 被多类型公司（而非仅大厂）共同强调的维度 → 确认为核心特质
- 结构清晰、三层分层合理的部分 → 保持框架稳定
- 贴合人才级别的期望水位 → 确保不偏高/偏低

**「弃」— 修正或降级的内容：**
- 仅互联网大厂强调、其他类型企业不提的表述 → 降级为证据层或标注"大厂场景"
- 与目标行业企业差异较大的表述 → 修正措辞或边界
- 仅个别公司提到的要求 → 降级为证据层
- 混淆证据层与特质层的内容 → 重新归位
- 层级错配的期望 → 调整水位

**调整优先级：** wording → evidence → boundary → core dimensions

### Step 9: 生成输出

**必须包含的7个部分：**

1. **一句话候选人画像** — "这个角色真正想找什么样的人？"
2. **一级胜任力维度** — 最终确定的6个MECE维度
3. **维度定义** — 含义与重要性
4. **可观察行为** — 每个维度下的行为表现
5. **角色证据** — 该角色的具体验证点
6. **验证结论** — 多元企业信息采集的发现与调整（含"仅大厂特有"的降级说明）
7. **适用范围说明** — 哪里适用，哪里不要过度延伸

**如果是HTML格式，额外要求：**
- 单文件、可本地运行
- 4个图表：旭日图、矩形树图、散点图、能力树（**缺一不可**）
- 管理咨询风格视觉
- 无虚假量化权重
- 验证链接可点击

**⚠️ HTML图表硬约束 — 禁止项：**
- ❌ **禁止使用雷达图（radar）**：胜任力报告的高频训练数据联想，但不适合展示多层级维度结构
- ❌ **禁止使用柱状图（bar）/折线图（line）**：这些是通用数据图表，不传达胜任力模型的层级关系
- ❌ **禁止使用饼图（pie）**：胜任力维度不是比例分割关系
- ❌ **禁止省略任何图表**：4个图表必须全部生成，缺少任何一个报告不合格
- ✅ **只允许**：sunburst（旭日图）、treemap（矩形树图）、scatter（散点图）、tree（能力树）
- ❌ **图表中禁止使用量化数值**（value/坐标/百分比/轴刻度）：胜任力模型无真实测量数据，图表value只表示相对结构比例，ECharts示例中的数值均为结构占位符；严禁在图表中填写精确数字

> **原因**：大模型生成"胜任力+自评"类内容时，训练数据中高频出现雷达图，导致统计惯性压倒规范要求。同时大模型倾向于为图表填写精确数值（权重/百分比/坐标），这是幻觉高发区。以上禁止项是经过测试验证的失败模式，必须硬性约束。

**HTML生成时必须同时提供：**
1. `{ROLE_NAME}_胜任力模型.html` — 主报告文件
2. `echarts.min.js` — ECharts图表库（必须复制到同一目录）

**操作步骤：**
```bash
# 1. 生成HTML报告
write_to_file(filePath="{workspace}/{ROLE_NAME}_胜任力模型.html", content=html_content)

# 2. 复制echarts.min.js到工作目录（关键！）
# 从Skill的assets目录复制echarts.min.js到用户工作目录
# 源文件路径: .workbuddy/skills/competency-model/assets/echarts.min.js
# 目标路径: {workspace}/echarts.min.js
```

**使用说明（告知用户）：**
- HTML报告需要与`echarts.min.js`在同一目录才能正常显示图表
- 用浏览器打开HTML文件即可查看完整可视化效果
- 如需分享报告，请同时分享HTML文件和echarts.min.js
- 报告完全离线可用，无需网络连接
- 每个图表区域提供导出按钮，支持导出为 PNG/SVG/JPEG 格式

---

## HTML报告模板规范

生成的HTML必须包含以下结构：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8"/>
  <title>{ROLE_NAME} 候选人人才画像胜任力模型</title>
  <!-- 内嵌CSS样式（参考案例风格） -->
  <style>...</style>
</head>
<body>
  <header>
    <h1>{ROLE_NAME} 候选人人才画像胜任力模型</h1>
    <p>一句话画像描述...</p>
    <div class="source-strip">验证公司标签...</div>
  </header>
  
  <main>
    <!-- 建模口径说明 -->
    <div class="model-note">...</div>
    
    <!-- 01 旭日图：人才画像全景 -->
    <section>
      <div class="section-header">
        <span class="section-num">01</span>
        <span class="section-title">人才画像全景</span>
      </div>
      <div class="chart-wrapper">
        <div class="chart-toolbar">
          <button class="chart-export-btn" onclick="exportChart('chart-sunburst', 'png')" title="导出PNG">PNG</button>
          <button class="chart-export-btn" onclick="exportChart('chart-sunburst', 'svg')" title="导出SVG">SVG</button>
        </div>
        <div id="chart-sunburst" class="chart-container">
          <!-- ECharts 旭日图配置示例（禁止替换为 radar/bar/line/pie）：
          ⚠️ 注意：value 只表示结构占比（无真实数据），不要写精确数字。
          {
            type: 'sunburst',
            data: [{
              name: 'D1 维度名',
              children: [
                { name: 'B1.1 行为名',
                  children: [
                    { name: 'E1.1.1 证据名' },
                    { name: 'E1.1.2 证据名' }
                  ]
                },
                { name: 'B1.2 行为名', children: [{ name: 'E1.2.1 证据名' }] }
              ]
            }, {
              name: 'D2 维度名',
              children: [
                { name: 'B2.1 行为名', children: [{ name: 'E2.1.1 证据名' }] }
              ]
            }],
            radius: ['15%', '90%'],
            label: { rotate: 'radial' }
          }
          -->
        </div>
      </div>
    </section>

    <!-- 02 矩形树图：评估关注结构 -->
    <section>
      <div class="section-header">
        <span class="section-num">02</span>
        <span class="section-title">评估关注结构</span>
      </div>
      <div class="chart-wrapper">
        <div class="chart-toolbar">
          <button class="chart-export-btn" onclick="exportChart('chart-treemap', 'png')" title="导出PNG">PNG</button>
          <button class="chart-export-btn" onclick="exportChart('chart-treemap', 'svg')" title="导出SVG">SVG</button>
        </div>
        <div id="chart-treemap" class="chart-container">
          <!-- ECharts 矩形树图配置示例（禁止替换为 radar/bar/line/pie）：
          ⚠️ 注意：value 只控制视觉面积比例（无真实数据），不要写精确数字或百分比。
          {
            type: 'treemap',
            data: [
              { name: 'D1 产品思维',
                children: [
                  { name: 'B1.1 需求分析' },
                  { name: 'B1.2 用户洞察' },
                  { name: 'B1.3 方案设计' }
                ]
              },
              { name: 'D2 执行力',
                children: [
                  { name: 'B2.1 项目管理' },
                  { name: 'B2.2 跨部门协作' }
                ]
              },
              { name: 'D3 技术理解',
                children: [
                  { name: 'B3.1 技术方案评估' },
                  { name: 'B3.2 技术风险判断' }
                ]
              },
              { name: 'D4 商业敏感',
                children: [
                  { name: 'B4.1 商业逻辑拆解' }
                ]
              },
              { name: 'D5 沟通影响',
                children: [
                  { name: 'B5.1 跨团队推动' }
                ]
              }
            ],
            label: { formatter: '{b}' },
            levels: [{ itemStyle: { borderWidth: 0 } }]
          }
          -->
        </div>
      </div>
    </section>
    
    <!-- 03 散点图：人才分型象限 + 行为锚点表格 -->
    <section>
      <div class="section-header">
        <span class="section-num">03</span>
        <span class="section-title">人才分型象限 + 行为锚点</span>
      </div>
      <p class="section-desc">将候选人在各维度的表现投射到「成长潜力×当前能力」象限，识别不同发展路径的人才分型。</p>
      
      <!-- 散点图 -->
      <div class="chart-wrapper">
        <div class="chart-toolbar">
          <button class="chart-export-btn" onclick="exportChart('chart-scatter', 'png')" title="导出PNG">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            PNG
          </button>
          <button class="chart-export-btn" onclick="exportChart('chart-scatter', 'svg')" title="导出SVG">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            SVG
          </button>
        </div>
        <div id="chart-scatter" class="chart-container">
          <!-- ECharts 散点图配置示例（禁止替换为 radar/bar/line/pie）：
          ⚠️ 注意：坐标值只表示相对位置关系（无真实测量数据），禁止写精确数字。
          散点图展示"成长潜力 vs 当前能力"的两维分布，用气泡大小或颜色区分维度。
          {
            type: 'scatter',
            data: [
              { name: 'D1 产品思维', value: [null, null], itemStyle: { color: '#5470c6' } },
              { name: 'D2 执行力',     value: [null, null], itemStyle: { color: '#91cc75' } },
              { name: 'D3 技术理解',   value: [null, null], itemStyle: { color: '#fac858' } },
              { name: 'D4 商业敏感',   value: [null, null], itemStyle: { color: '#ee6666' } },
              { name: 'D5 沟通影响',   value: [null, null], itemStyle: { color: '#73c0de' } }
            ],
            xAxis: { name: '成长潜力（相对位置）', type: 'category' },
            yAxis: { name: '当前能力（相对位置）', type: 'category' }
          }
          -->
        </div>
      </div>
      
      <!-- 行为锚点表格 -->
      <div class="persona-table">
        <table>
          <thead>
            <tr>
              <th>人才分型</th>
              <th>位置特征</th>
              <th>核心特征</th>
              <th>典型信号</th>
              <th>培养建议</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>🌱 潜力型</td>
              <td>潜力高 × 能力低</td>
              <td>学习敏锐度高、好奇心强、适应性好</td>
              <td>快速掌握新概念、主动提问、跨领域迁移</td>
              <td>给予挑战性任务、配对导师、关注基础夯实</td>
            </tr>
            <tr>
              <td>⚡ 达标型</td>
              <td>潜力中 × 能力中</td>
              <td>执行力强、稳定性好、团队协作佳</td>
              <td>按时交付、主动汇报、乐于帮助他人</td>
              <td>逐步增加挑战性、鼓励承担更多责任</td>
            </tr>
            <tr>
              <td>🔥 突出型</td>
              <td>潜力高 × 能力高</td>
              <td>成长型思维、卓越交付、影响力强</td>
              <td>超预期交付、带动团队、推动创新</td>
              <td>授权更多自主权、战略性项目、领导力培养</td>
            </tr>
            <tr>
              <td>⏸️ 平台型</td>
              <td>潜力中 × 能力高</td>
              <td>经验丰富、稳健可靠、专业深度</td>
              <td>独当一面、知识沉淀、稳定输出</td>
              <td>保持稳定发挥、适度引入新挑战、传承经验</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
    
    <!-- 04 能力树：完整MECE结构 -->
    <section>
      <div class="section-header">
        <span class="section-num">04</span>
        <span class="section-title">完整MECE结构</span>
      </div>
      <div class="chart-wrapper">
        <div class="chart-toolbar">
          <button class="chart-export-btn" onclick="exportChart('chart-tree', 'png')" title="导出PNG">PNG</button>
          <button class="chart-export-btn" onclick="exportChart('chart-tree', 'svg')" title="导出SVG">SVG</button>
        </div>
        <div id="chart-tree" class="chart-container">
          <!-- ECharts 能力树/矩形树图配置示例（禁止替换为 radar/bar/line/pie）：
          {
            type: 'tree',
            orient: 'LR',  // 左右布局，便于展示横向层级
            data: [{
              name: '{ROLE_NAME}\n胜任力模型',
              children: [
                {
                  name: 'D1 产品思维',
                  children: [
                    { name: 'B1.1 需求分析', children: [{ name: 'E1.1.1 能拆解需求' }, { name: 'E1.1.2 优先级判断' }] },
                    { name: 'B1.2 用户洞察', children: [{ name: 'E1.2.1 用户访谈' }, { name: 'E1.2.2 行为数据分析' }] }
                  ]
                },
                {
                  name: 'D2 执行力',
                  children: [
                    { name: 'B2.1 项目管理', children: [{ name: 'E2.1.1 排期计划' }, { name: 'E2.1.2 风险识别' }] },
                    { name: 'B2.2 跨部门协作', children: [{ name: 'E2.2.1 推动对齐' }, { name: 'E2.2.2 结果导向' }] }
                  ]
                }
              ]
            }]
          }
          -->
        </div>
      </div>
    </section>
    
    <!-- 【可选】自测矩阵（三水位对照） -->
    <!-- 仅当用户选择添加自测矩阵功能时包含此节 -->
    <section class="self-check-section">
      <div class="section-header">
        <span class="section-num">04.5</span>
        <span class="section-title">自测矩阵（三水位对照）</span>
      </div>
      <p class="section-desc">帮助候选人自我评估在各维度的当前水位，明确下一步努力方向。适合自测、培训发展、辅导对话等场景。</p>
      
      <div class="matrix-legend">
        <span><span class="matrix-level level-seedling"></span> 🌱 起步 — 尚未稳定展现该特质</span>
        <span><span class="matrix-level level-qualified"></span> ⚡ 达标 — 在多数场景能稳定展现</span>
        <span><span class="matrix-level level-outstanding"></span> 🔥 突出 — 在复杂场景也能引领示范</span>
      </div>
      
      <div class="self-check-matrix">
        <div class="matrix-grid">
          <!-- 表头 -->
          <div class="matrix-header">胜任力维度</div>
          <div class="matrix-header">🌱 起步</div>
          <div class="matrix-header">⚡ 达标</div>
          <div class="matrix-header">🔥 突出</div>
          <div class="matrix-header">下一步努力方向</div>
          
          <!-- 示例行 -->
          <div class="matrix-cell matrix-dim-name">方向与标尺</div>
          <div class="matrix-cell">
            <label><input type="radio" name="dim1" value="seedling"><span>能完成指定任务，但对目标主动思考较少</span></label>
          </div>
          <div class="matrix-cell">
            <label><input type="radio" name="dim1" value="qualified"><span>能理解任务背景，对质量有一定追求</span></label>
          </div>
          <div class="matrix-cell">
            <label><input type="radio" name="dim1" value="outstanding"><span>主动定义目标，推动标准提升，带动他人</span></label>
          </div>
          <div class="matrix-cell matrix-action">→ 主动认领有挑战的子目标，记录质量反思</div>
          
          <!-- 更多维度行... -->
        </div>
      </div>
      
      <div class="matrix-tip">
        <strong>使用建议：</strong>
        <ul>
          <li>建议在安静的时段独立完成，避免匆忙勾选</li>
          <li>如有具体事例支撑选择，会更有价值</li>
          <li>「下一步」方向可与导师或上级讨论确认</li>
        </ul>
      </div>
    </section>
    
    <!-- 05 官网岗位链接（人工检验） -->
    <section>
      <div class="section-header">
        <span class="section-num">05</span>
        <span class="section-title">官网岗位链接（人工检验）</span>
      </div>
      <p class="section-desc">以下链接仅作为人工校验这个模型的外部参照：能切到校招、应届生招聘或实习的，已优先切换；其余保留官方招聘入口作为补充。目的不是要求年轻候选人与资深岗位逐项对标，而是观察不同公司在早期人才身上重视哪些稳定特征。</p>
      <div class="validation-note">阅读建议：优先关注岗位或校招页中反复出现的学习潜力、主动性、责任感、工程基础、协作气质与长期建设倾向，而不是逐条比对工具栈。对年轻候选人，更适合看"能否长成"而不是"是否已经全部具备"。</div>
      <div class="link-grid">
        <!-- 链接卡片示例 -->
        <a class="link-card" href="{公司官网校招/实习链接}" target="_blank" rel="noopener noreferrer">
          <div class="link-card-meta">{公司名} · 官方校招 / 实习</div>
          <div class="link-card-title">{岗位名称}</div>
          <div class="link-card-desc">检验点：{简明说明这个链接用来检验什么，例如"观察对潜力、主动性、协作气质的要求"}</div>
        </a>
        <!-- 更多链接卡片... -->
      </div>
    </section>
  </main>
  
  <footer>...</footer>
  
  <!-- ECharts + 图表初始化脚本 -->
  <script src="echarts.min.js"></script>
  <script>...</script>
</body>
</html>
```

**图表数据规则：**
- value 仅表达相对关注重心，不表示精确分数
- 颜色区分6个主维度
- 所有图表支持SVG导出

**图表导出功能规范：**

```css
/* 图表工具栏 */
.chart-wrapper {
  position: relative;
  margin-bottom: 1.5rem;
}
.chart-toolbar {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  display: flex;
  gap: 0.35rem;
  z-index: 10;
  opacity: 0;
  transition: opacity 0.2s ease;
}
.chart-wrapper:hover .chart-toolbar {
  opacity: 1;
}
.chart-export-btn {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.35rem 0.6rem;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-muted);
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
}
.chart-export-btn:hover {
  color: var(--primary);
  border-color: var(--primary);
  background: rgba(59,130,246,0.06);
}
.chart-container {
  min-height: 400px;
}
@media (max-width: 768px) {
  .chart-toolbar { opacity: 1; }
  .chart-container { min-height: 300px; }
}
```

**导出功能 JS 实现：**
```javascript
// 使用 ECharts 内置的导出功能
function exportChart(chartId, format) {
  const chart = echarts.getInstanceByDom(document.getElementById(chartId));
  if (!chart) return;
  
  const formats = {
    png: { type: 'png', quality: 1 },
    jpeg: { type: 'jpeg', quality: 0.8 },
    svg: { type: 'svg' }
  };
  
  const option = formats[format];
  if (!option) return;
  
  // 生成数据URL或SVG字符串
  const url = chart.getDataURL(option);
  
  // 自动下载
  const link = document.createElement('a');
  link.download = `${chartId}_${Date.now()}.${format}`;
  link.href = url;
  link.click();
}
```

**人才分型表格样式规范：**
```css
.persona-table {
  margin-top: 1.5rem;
  overflow-x: auto;
}
.persona-table table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.88rem;
}
.persona-table th,
.persona-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid var(--border);
  vertical-align: top;
}
.persona-table th {
  background: var(--surface);
  font-weight: 700;
  color: var(--text);
  font-size: 0.85rem;
}
.persona-table td:first-child {
  font-weight: 700;
  color: var(--primary);
  white-space: nowrap;
}
.persona-table tr:hover td {
  background: var(--surface);
}
```

**自测矩阵样式规范（可选功能）：**
```css
.self-check-matrix {
  margin-top: 1.5rem;
}
.matrix-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1.5fr;
  gap: 0;
  font-size: 0.88rem;
}
.matrix-header {
  background: var(--surface);
  font-weight: 700;
  font-size: 0.82rem;
  color: var(--text-muted);
}
.matrix-header,
.matrix-cell {
  padding: 0.75rem;
  border-bottom: 1px solid var(--border);
}
.matrix-dim-name {
  font-weight: 600;
  color: var(--text);
}
.matrix-cell { color: var(--text-muted); }
.matrix-cell label { display: flex; align-items: flex-start; gap: 0.5rem; cursor: pointer; }
.matrix-level {
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-top: 3px;
  flex-shrink: 0;
}
.level-seedling { background: #22c55e; }   /* 起步 */
.level-qualified { background: #3b82f6; }  /* 达标 */
.level-outstanding { background: #f59e0b; } /* 突出 */
.matrix-action { font-size: 0.85rem; color: var(--text-muted); }
.matrix-legend {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1rem;
  font-size: 0.85rem;
  color: var(--text-muted);
}
.matrix-legend span { display: flex; align-items: center; gap: 0.4rem; }
@media (max-width: 900px) {
  .matrix-grid { grid-template-columns: 1fr; }
  .matrix-header { display: none; }
  .matrix-cell { border-left: 3px solid var(--border); padding-left: 1rem; }
}
```

**链接卡片样式规范：**
```css
.validation-note {
  margin-bottom: 1rem;
  color: var(--text-muted);
  font-size: 0.92rem;
}
.link-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}
.link-card {
  display: block;
  text-decoration: none;
  color: inherit;
  background: var(--surface);
  border: 1px solid rgba(59,130,246,0.16);
  border-radius: 12px;
  padding: 1rem 1.1rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.04);
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}
.link-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(15,23,42,0.08);
  border-color: rgba(59,130,246,0.3);
}
.link-card-title {
  font-size: 0.98rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 0.35rem;
}
.link-card-meta {
  font-size: 0.82rem;
  color: var(--primary);
  margin-bottom: 0.35rem;
  font-weight: 600;
}
.link-card-desc {
  font-size: 0.9rem;
  color: var(--text-muted);
}
@media (max-width: 900px) {
  .link-grid { grid-template-columns: 1fr; }
}
```

**链接选择优先级：**
1. 优先使用官方校招/实习入口
2. 其次使用官方 careers/招聘主页
3. 最后才用具体岗位页面（标注为"上限参照"）

**链接卡片标签规范：**
- 校招/实习入口：`{公司} · 官方校招 / 实习`
- 官方招聘主页：`{公司} · 官方招聘入口`
- 上限参照岗位：`{公司} · 官方岗位（上限参照）`

**每个卡片必须包含：**
- `link-card-meta`：公司名和入口类型
- `link-card-title`：具体岗位或页面名称
- `link-card-desc`：**必须包含"检验点"**，说明这个链接用来检验模型的哪个维度或特质

---

## 报告生成后自检清单

**每次生成 HTML 报告后，在返回结果前必须逐项检查：**

**内容完整性：**
- [ ] **一级维度是"人的特质"，不是技能/工具/技术栈**（禁止"系统抽象能力""Python""硬件感知"等作为一级维度）
- [ ] 每个维度下有二级行为，且行为可观察、可区分
- [ ] 每个行为下有三级证据，且证据不直接等于工具/语言/框架
- [ ] 有"验证结论"节，说明从多元企业信息中提炼出的发现
- [ ] **校招/实习场景**：验证公司信息全部来自campus/graduate/intern入口，无社招JD污染

**图表规范性（硬约束）：**
- [ ] **旭日图存在**：`id="chart-sunburst"` 且 ECharts 配置 `type: 'sunburst'`（不是 radar/bar/line/pie）
- [ ] **矩形树图存在**：`id="chart-treemap"` 且 `type: 'treemap'`（不是 radar/bar/line/pie）
- [ ] **散点图存在**：`id="chart-scatter"` 且 `type: 'scatter'`（不是 radar/bar/line/pie）
- [ ] **能力树存在**：`id="chart-tree"` 且 `type: 'tree'`（不是 radar/bar/line/pie）
- [ ] **四个图表全部生成**，缺少任何一个 → 必须补充后再输出
- [ ] **图表中无量化数值**：ECharts data 中没有 value 精确数字、没有百分比、没有坐标轴刻度 min/max、没有 markArea 精确分界线；散点图坐标用 `[null, null]` 占位

**echarts.min.js 关联：**
- [ ] `<script src="echarts.min.js">` 存在于 `<head>` 或 `<body>` 底部
- [ ] echarts.min.js 文件已复制到 HTML 文件同目录

**格式规范：**
- [ ] 无虚假量化权重（不用百分比/分数表达维度重要程度，只用相对"关注重心"）
- [ ] 验证链接卡片有实际可点击 URL，且描述包含"检验点"说明
- [ ] 报告可本地打开（无 CDN 依赖路径）

**若发现违规项 → 立即修正后再输出，不要忽略任何一项。**

---

## 失败模式防范

执行中必须主动避免：

| 陷阱 | 防范措施 |
|------|---------|
| 技能树陷阱 | 工具/框架放在三级证据，不要作为一级维度 |
| 通用软技能陷阱 | 每个维度必须能区分该角色的特定要求 |
| 层级混淆 | 严格区分一级维度、二级行为、三级证据 |
| 级别错配 | 校招不套用资深标准，反之亦然 |
| 来源误用 | 先用模型验证JD，而不是用JD组装模型 |
| 虚假精度 | 不分配数值权重，只用相对关注重心 |
| **大厂偏差** | **验证公司不能全为互联网大厂；Q5 非互联网行业时，大厂占比不超过50%；大厂特有要求降级为证据层** |
| **先验框架陷阱** | **企业信息采集（Step 3.5）必须在起草维度（Step 4）之前执行；禁止先套框架再找证据支持** |
| **技能维度陷阱** | **一级维度禁止是技能/工具/技术栈；维度必须是对"什么样的人"的特质判断，而非"需要什么技能"的枚举；行为（二级）才是技能落脚点** |
| **校招社招污染** | **校招/实习场景严禁使用社招JD；禁止用资深岗位反推校招标准；只允许campus/graduate/intern入口；校招维度以"潜力/可塑性"为核心** |
| **图表惯性漂移** | **HTML报告必须使用 sunburst/treemap/scatter/tree 四种图表；禁止使用 radar/bar/line/pie；生成后必须按自检清单逐项验证图表类型** |
| **图表量化幻觉** | **图表ECharts配置中禁止填写精确数值（value/坐标/百分比/轴刻度）；胜任力模型无测量数据，图表只展示相对结构关系；若生成时填写了具体数字→立即清除** |

---

## 示例对话

**用户**：帮我做一个产品经理的胜任力模型

**Skill**：
> 我来帮你构建产品经理岗位的胜任力模型。这需要通过配置向导收集一些信息，大概需要2-3分钟。
>
> **Q1: 目标岗位的具体名称是什么？**
> 提示：如"产品经理"、"产品专员"、"B端产品经理"等

**用户**：产品经理

**Skill**：
> **Q2: 人才级别是什么？** ⚠️【这个选择会显著影响模型侧重点】
> 
> A. 校招/实习 — 侧重潜力、基础素质、学习敏捷  
> B. 应届生 — 侧重成长空间、主动性、产品思维  
> C. 1-3年经验 — 侧重执行力、需求分析能力  
> D. 资深专家 — 侧重判断力、战略规划  
> E. 管理者 — 侧重组织判断、产品领导力

**用户**：校招

**Skill**：
> ✅ 已选择【校招/实习】级别。模型将侧重潜力与基础素质，避免用资深标准去要求年轻候选人。
>
> **Q3: 使用场景是什么？**
> ...

[继续直到所有字段填写完成]

**Skill（Q7 之前，Step 0 企业分布探索）**：
> 在进入验证公司选择之前，我先来了解一下产品经理岗位在市场上的企业分布：
>
> 【企业分布探索结论】
> "产品经理（校招）"在以下类型企业广泛分布：
>   ✓ 互联网大厂 — 业务产品/平台产品（代表：ByteDance、Tencent、Alibaba）
>   ✓ 中型互联网/独角兽 — 垂直赛道产品（代表：小红书、快手、Boss直聘）
>   ✓ 企业服务/SaaS — B端产品（代表：飞书、钉钉、用友、金蝶）
>   ✓ 金融科技 — 金融产品（代表：蚂蚁集团、微众银行、招银网络）
>   ✓ 传统行业数字化 — 行业产品（代表：华为、OPPO、宁德时代）
>
> → Q7 验证公司将从以上5类中各选，避免单一大厂视角。

**Skill**：
> 【配置确认】
> 岗位：产品经理
> 级别：校招/实习 ⚠️
> 验证公司：ByteDance（大厂）、小红书（中型互联网）、飞书（企业服务）、蚂蚁集团（金融科技）、华为终端（传统行业）
> ...
>
> 【智能校验】
> ✓ 校招级别已选择，将侧重潜力与基础素质
> ✓ 验证公司覆盖5种类型企业，已避免大厂偏差
> ⚠ 提醒：Step 3.5 将在起草维度前先采集5家企业招聘信息，信号归纳后再建模
>
> [确认] [修改配置]

**用户**：确认

**Skill**：
> 开始执行，预计需要3-5分钟...
>
> **Step 3.5 企业信息采集中...**
> 正在访问：ByteDance校招页 / 小红书招聘 / 飞书招聘 / 蚂蚁集团校招 / 华为校园招聘
>
> 【原始信号归纳表（节选）】
> | 信号 | 大厂 | 中型 | 企业服务 | 金融 | 传统行业 | 判断 |
> |------|------|------|----------|------|----------|------|
> | 用户同理心 | ✓ | ✓ | ✓ | ✓ | ✓ | 核心维度 |
> | 数据驱动决策 | ✓ | ✓ | ✓ | ✓ | — | 核心维度 |
> | 合规/风控意识 | — | — | — | ✓ | — | 金融特有→证据层 |
> | 快速迭代/AB测试 | ✓ | ✓ | — | — | — | 互联网特有→证据层 |
>
> 基于信号表起草维度，而非预设框架...
>
> ✅ 胜任力模型已生成！

---

## 最终指导原则

> **胜任力模型不是整理后的职位描述。**
> **它是对"组织真正想识别什么样的人"的结构化判断。**
> **先建模人，再映射行为，最后验证证据。**
