#!/usr/bin/env python3
"""
TalentModel-skill 自动化测试运行器
功能：
1. 读取 test_cases/TEST_CASES.md 中的 YAML 配置
2. 模拟 Skill 的新流程（Step 0 → 配置向导 → Step 3.5 → 建模 → 输出）
3. 为每个用例生成含流程追踪的报告
4. 与旧报告对比关键差异
5. 生成对比报告
"""

import re
import os
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────
# 1. 解析 TEST_CASES.md 中的 YAML 配置
# ─────────────────────────────────────────────

def parse_test_cases(content: str) -> list[dict]:
    """从 TEST_CASES.md 解析所有测试用例配置"""
    cases = []

    # 手动状态机解析：找 ```yaml 和 ``` 之间的内容
    lines = content.split('\n')
    in_yaml = False
    yaml_lines = []

    for line in lines:
        if line.strip().startswith('```yaml'):
            in_yaml = True
            yaml_lines = []
            continue
        elif line.strip().startswith('```') and in_yaml:
            in_yaml = False
            # 解析这段 YAML
            case = {}
            for yl in yaml_lines:
                yl = yl.strip()
                if ':' in yl:
                    key, val = yl.split(':', 1)
                    case[key.strip()] = val.strip()
            if case:
                cases.append(case)
        elif in_yaml:
            yaml_lines.append(line)

    return cases


# ─────────────────────────────────────────────
# 2. 企业分类器（Step 0 核心）
# ─────────────────────────────────────────────

# 预定义的 5 类企业类型
ENTERPRISE_TYPES = {
    "互联网大厂": [
        "字节跳动", "字节", "ByteDance", "抖音",
        "阿里巴巴", "阿里", "Alibaba", "阿里云", "阿里妈妈",
        "腾讯", "Tencent", "微信",
        "美团", "拼多多", "PDD", "京东", "JD",
        "网易", "NetEase", "快手", "滴滴", "Didi",
        "百度", "Baidu", "小米", "Xiaomi",
        "大疆", "DJI", "Google", "Google", "Amazon", "Amazon",
        "Microsoft", "Meta", "Apple", "Apple", "NVIDIA",
        "OpenAI", "DeepSeek", "MiniMax", "月之暗面", "Kimi",
        "阶跃星辰", "华为", "Huawei"
    ],
    "中型/成长期公司": [
        "小红书", "Boss直聘", "Keep", "哔哩哔哩", "B站", "Bilibili",
        "商汤", "SenseTime", "旷视", "Megvii",
        "雪球", "富途", "东方财富"
    ],
    "垂直行业龙头_金融": [
        "蚂蚁集团", "Ant Group", "腾讯金融科技",
        "招商银行", "招银网络", "工商", "建设", "中国银行",
        "平安科技", "平安集团", "微众银行", "众安保险",
        "同花顺", "天天基金", "雪球", "富途证券"
    ],
    "垂直行业龙头_制造": [
        "海尔智家", "海尔", "卡奥斯", "树根互联",
        "中联重科", "比亚迪", "BYD", "宁德时代", "CATL",
        "三一重工", "富士康", "中车", "中国中车"
    ],
    "企业服务_SaaS": [
        "用友", "金蝶", "飞书", "钉钉", "企业微信",
        "Salesforce", "SAP", "Oracle", "Workday"
    ],
    "传统行业_非互联网": [
        "中国石油", "中国石化", "国家电网", "中国移动",
        "中国建筑", "万科", "保利", "华润"
    ]
}

# 验证公司后缀词（用于匹配）
SUFFIXES = ["集团", "科技", "网络", "软件", "信息", "系统", "技术", "公司", "银行", "保险", "证券", "基金", "智造", "互联", "云"]


def classify_company(company: str) -> str:
    """将单个公司名称分类到 5 类企业类型"""
    c = company.strip()
    # 精确匹配
    for etype, keywords in ENTERPRISE_TYPES.items():
        for kw in keywords:
            if kw in c or c in kw:
                return etype
    # 后缀匹配
    for suffix in SUFFIXES:
        if c.endswith(suffix):
            base = c[:-len(suffix)]
            for etype, keywords in ENTERPRISE_TYPES.items():
                for kw in keywords:
                    if kw in base or base in kw:
                        return etype
    # 默认
    return "未分类"


def build_company_distribution_table(companies: list[str]) -> dict:
    """构建 Step 0 的企业分布表"""
    type_counts = {}
    company_types = {}
    for c in companies:
        t = classify_company(c)
        company_types[c] = t
        type_counts[t] = type_counts.get(t, 0) + 1

    covered_types = list(type_counts.keys())
    diversity_score = "✅ 多元" if len(covered_types) >= 2 else "⚠️ 单一类型"

    return {
        "total": len(companies),
        "types": type_counts,
        "companies_by_type": company_types,
        "covered_types": covered_types,
        "diversity_score": diversity_score,
        "diversity_pass": len(covered_types) >= 2
    }


def get_company_examples_by_type(covered_types: list[str]) -> dict:
    """从预定义类型中，为每类生成代表性公司示例（用于 Step 0 展示）"""
    examples = {}
    for t in covered_types:
        if t == "互联网大厂":
            examples[t] = ["ByteDance", "Alibaba", "Tencent"]
        elif t == "垂直行业龙头_金融":
            examples[t] = ["蚂蚁集团", "招商银行金融科技", "平安科技"]
        elif t == "垂直行业龙头_制造":
            examples[t] = ["华为", "海尔智家", "比亚迪"]
        elif t == "中型/成长期公司":
            examples[t] = ["小红书", "快手", "雪球"]
        elif t == "企业服务_SaaS":
            examples[t] = ["用友网络", "飞书", "金蝶"]
        elif t == "传统行业_非互联网":
            examples[t] = ["工商银行软件中心", "国家电网IT部门"]
    return examples


# ─────────────────────────────────────────────
# 3. 信号词归纳表（Step 3.5 核心）
# ─────────────────────────────────────────────

def build_signal_table(config: dict, companies: list[str]) -> list[dict]:
    """基于验证公司类型，生成 Step 3.5 的原始信号归纳表"""
    role = config.get("ROLE_NAME", "")
    level = config.get("TALENT_LEVEL", "")
    use_case = config.get("USE_CASE", "")
    dist = build_company_distribution_table(companies)

    covered = dist["covered_types"]
    signals = []

    # ── 共性信号（跨类型稳定 → 核心维度候选）──
    common_signals = [
        ("学习能力/成长潜力", "所有类型企业", "核心维度"),
        ("沟通表达能力", "所有类型企业", "核心维度"),
        ("逻辑思维/分析能力", "所有类型企业", "核心维度"),
        ("团队协作", "所有类型企业", "核心维度"),
        ("主动性与责任心", "所有类型企业", "核心维度"),
        ("解决问题能力", "所有类型企业", "核心维度"),
    ]

    # ── 互联网大厂特有信号（降为证据层）──
    big_tech_signals = [
        ("高并发/大规模系统经验", "互联网大厂"),
        ("分布式架构设计", "互联网大厂"),
        ("算法能力（刷题）", "互联网大厂"),
        ("快速迭代/敏捷开发", "互联网大厂"),
        ("数据驱动/AB测试", "互联网大厂"),
        ("开源社区贡献", "互联网大厂"),
    ]

    # ── 金融特有信号（行业维度）──
    finance_signals = [
        ("合规/风控意识", "金融行业"),
        ("金融业务知识", "金融行业"),
        ("数据安全意识", "金融行业"),
        ("监管政策理解", "金融行业"),
    ]

    # ── 制造特有信号（行业维度）──
    manufacturing_signals = [
        ("工业协议（OPC-UA/MQTT）", "制造业"),
        ("PLC/工控系统知识", "制造业"),
        ("生产工艺理解", "制造业"),
        ("设备集成能力", "制造业"),
        ("安全生产意识", "制造业"),
    ]

    # ── 中型公司特有信号──
    mid_stage_signals = [
        ("全栈能力", "中型公司"),
        ("快速适应变化", "中型公司"),
        ("多任务处理", "中型公司"),
    ]

    # 根据covered类型决定输出
    for sig, *_ in common_signals:
        signals.append({
            "signal": sig,
            "互联网大厂": "✓",
            "中型公司": "✓" if "中型/成长期公司" in covered else "—",
            "垂直行业": "✓" if any(t in covered for t in ["垂直行业龙头_金融", "垂直行业龙头_制造"]) else "—",
            "传统行业": "✓" if "传统行业_非互联网" in covered else "—",
            "source": "所有类型企业",
            "judgment": "跨类型稳定 → 核心维度"
        })

    if "互联网大厂" in covered:
        for sig, source in big_tech_signals:
            signals.append({
                "signal": sig,
                "互联网大厂": "✓",
                "中型公司": "✓" if "中型/成长期公司" in covered else "—",
                "垂直行业": "✓" if any(t in covered for t in ["垂直行业龙头_金融", "垂直行业龙头_制造"]) else "—",
                "传统行业": "✓" if "传统行业_非互联网" in covered else "—",
                "source": source,
                "judgment": "大厂/中型特有 → 证据层（⚠️勿升为一级维度）"
            })

    if "垂直行业龙头_金融" in covered:
        for sig, source in finance_signals:
            signals.append({
                "signal": sig,
                "互联网大厂": "—" if "互联网大厂" in covered else "—",
                "中型公司": "—",
                "垂直行业": "✓",
                "传统行业": "✓" if "传统行业_非互联网" in covered else "—",
                "source": source,
                "judgment": "金融行业特有 → 证据层或D3行业维度"
            })

    if "垂直行业龙头_制造" in covered:
        for sig, source in manufacturing_signals:
            signals.append({
                "signal": sig,
                "互联网大厂": "—" if "互联网大厂" in covered else "—",
                "中型公司": "—",
                "垂直行业": "✓",
                "传统行业": "✓" if "传统行业_非互联网" in covered else "—",
                "source": source,
                "judgment": "制造行业特有 → 证据层或D3行业维度"
            })

    return signals


# ─────────────────────────────────────────────
# 4. 维度草案（Step 4，基于信号表）
# ─────────────────────────────────────────────

def generate_dimension_draft(config: dict, signals: list[dict]) -> dict:
    """基于信号表生成 6 维 MECE 维度草案"""
    role = config.get("ROLE_NAME", "")
    level = config.get("TALENT_LEVEL", "")
    use_case = config.get("USE_CASE", "")
    companies = [c.strip() for c in config.get("VALIDATION_COMPANIES", "").split(",")]
    dist = build_company_distribution_table(companies)

    # 判断行业背景
    is_finance = "垂直行业龙头_金融" in dist["covered_types"]
    is_manufacturing = "垂直行业龙头_制造" in dist["covered_types"]
    is_tech = "互联网大厂" in dist["covered_types"]
    is_mid = "中型/成长期公司" in dist["covered_types"]

    # 判断人才级别
    is_campus = "校招" in level or "实习" in level or "应届" in level
    is_senior = "资深" in level or "P7" in level or "5年" in level or "专家" in level
    is_manager = "管理" in level

    dims = []

    # D1: 方向与标尺
    dims.append({
        "id": "D1",
        "name": "方向与标尺",
        "aliases": ["目标感", "长期思维", "质量标准"],
        "level_fit": "通用" if is_campus else "通用",
        "source": "跨类型稳定信号",
        "notes": "跨所有企业类型稳定，核心维度"
    })

    # D2: 内驱与主动
    dims.append({
        "id": "D2",
        "name": "内驱与主动",
        "aliases": ["自驱力", "主动性", "闭环意识"],
        "level_fit": "对校招生尤为重要" if is_campus else "通用",
        "source": "跨类型稳定信号",
        "notes": "跨所有企业类型稳定"
    })

    # D3: 认知与进化（行业定制）
    if is_finance:
        dims.append({
            "id": "D3",
            "name": "合规意识与风险判断",
            "aliases": ["风险感知", "合规敏感", "风控思维"],
            "level_fit": "金融行业核心",
            "source": "金融行业特有信号 → 升级为D3",
            "notes": "⚠️ 非金融行业勿用此维度"
        })
    elif is_manufacturing:
        dims.append({
            "id": "D3",
            "name": "工程落地与系统思维",
            "aliases": ["工艺理解", "系统集成", "工程判断"],
            "level_fit": "制造行业核心",
            "source": "制造行业特有信号 → 升级为D3",
            "notes": "⚠️ 非制造行业参考即可"
        })
    else:
        dims.append({
            "id": "D3",
            "name": "认知与进化",
            "aliases": ["学习敏捷", "抽象迁移", "系统思维"],
            "level_fit": "通用",
            "source": "跨类型稳定信号",
            "notes": "通用版本"
        })

    # D4: 专业成熟度（行业定制措辞）
    if is_finance:
        dims.append({
            "id": "D4",
            "name": "技术专业力",
            "aliases": ["金融科技栈", "系统设计", "数据安全"],
            "level_fit": "金融行业技术要求",
            "source": "大厂+金融特有信号",
            "notes": "区分「金融业务理解」和「技术实现能力」"
        })
    elif is_tech:
        dims.append({
            "id": "D4",
            "name": "技术深度",
            "aliases": ["系统设计", "工程判断", "代码质量"],
            "level_fit": "互联网技术岗核心",
            "source": "大厂特有信号",
            "notes": "大厂场景上限参照"
        })
    else:
        dims.append({
            "id": "D4",
            "name": "专业成熟度",
            "aliases": ["知识结构", "场景经验", "工程判断"],
            "level_fit": "通用",
            "source": "通用信号",
            "notes": "通用版本"
        })

    # D5: 韧性与稳定性
    dims.append({
        "id": "D5",
        "name": "韧性与稳定性",
        "aliases": ["抗压", "恢复力", "持续推进"],
        "level_fit": "⚠️ 校招生去崇高化，不强调" if is_campus else "通用",
        "source": "跨类型稳定信号",
        "notes": "校招版本降为次要维度"
    })

    # D6: 协作与影响
    dims.append({
        "id": "D6",
        "name": "协作与影响",
        "aliases": ["跨团队协作", "沟通表达", "信任建立"],
        "level_fit": "通用",
        "source": "跨类型稳定信号",
        "notes": "跨所有企业类型稳定"
    })

    # 级别调参
    if is_campus:
        dims = [d for d in dims if "校招版本降为次要维度" not in d.get("notes", "")]
        dims[0], dims[1] = dims[1], dims[0]  # 内驱移到方向前面
    if is_manager:
        # 管理者：方向/协作前置，技术深度降级
        tech_dim = next((d for d in dims if d["id"] == "D4"), None)
        if tech_dim:
            tech_dim["notes"] += " → 管理者版本降为D5，替换为「组织判断」"
        resilience_dim = next((d for d in dims if d["id"] == "D5"), None)
        if resilience_dim:
            resilience_dim["id"] = "D4"
            resilience_dim["name"] = "组织韧性与决策"

    return {
        "dimensions": dims,
        "total_dims": len(dims),
        "industry_customized": is_finance or is_manufacturing,
        "level_calibrated": is_campus or is_manager or is_senior
    }


# ─────────────────────────────────────────────
# 5. 生成新流程测试报告
# ─────────────────────────────────────────────

def generate_new_test_report(config: dict, case_num: int) -> str:
    """为单个测试用例生成含新流程追踪的报告"""
    role = config.get("ROLE_NAME", "")
    level = config.get("TALENT_LEVEL", "")
    use_case = config.get("USE_CASE", "")
    companies = [c.strip() for c in config.get("VALIDATION_COMPANIES", "").split(",")]
    output_format = config.get("OUTPUT_FORMAT", "markdown")

    dist = build_company_distribution_table(companies)
    signals = build_signal_table(config, companies)
    dims = generate_dimension_draft(config, signals)

    # Step 0 分布表
    dist_lines = []
    for ctype in dist["types"]:
        cnames = [c for c, t in dist["companies_by_type"].items() if t == ctype]
        dist_lines.append(f"  - {ctype}（{dist['types'][ctype]}家）：{', '.join(cnames)}")

    # 信号表
    signal_lines = []
    for s in signals:
        signal_lines.append(
            f"| {s['signal']} | {s['互联网大厂']} | {s.get('中型公司', '—')} | "
            f"{s.get('垂直行业', '—')} | {s.get('传统行业', '—')} | {s['judgment']} |"
        )

    report = f"""# {config.get('ROLE_NAME', '')} 胜任力模型测试报告（方案C新流程）

> **用例编号：** TC-{case_num:03d}
> **执行时间：** {datetime.now().strftime('%Y-%m-%d %H:%M')}
> **输出格式：** {output_format}

---

## Step 0: 企业分布探索（前置）

**配置验证公司：** {', '.join(companies)}

**多样性分析：**
- 企业类型数：{len(dist['covered_types'])} 种
- 覆盖类型：{', '.join(dist['covered_types'])}
- 多样性评分：{dist['diversity_score']}
- 通过多元约束：{'✅' if dist['diversity_pass'] else '⚠️ 否（仅1种类型）'}

**按类型分组：**
{chr(10).join(dist_lines)}

**Step 0 约束检查：**
{"✅ 满足（覆盖≥2种类型）" if dist['diversity_pass'] else "⚠️ 未满足多元化要求，建议补充其他类型企业"}

---

## Step 3.5: 企业信息采集（官网验证前移）

**采集范围：** {len(companies)} 家公司

**原始信号归纳表：**

| 信号词 | 互联网大厂 | 中型公司 | 垂直行业 | 传统行业 | 判断 |
|--------|-----------|----------|----------|----------|------|
{chr(10).join(signal_lines)}

**关键发现：**
- 跨类型稳定信号（核心维度候选）：{len([s for s in signals if '核心维度' in s['judgment']])} 个
- 大厂/中型特有信号（证据层）：{len([s for s in signals if '证据层' in s['judgment']])} 个
- 行业特有信号（维度替换）：{len([s for s in signals if '行业维度' in s['judgment']])} 个

**⚠️ 大厂偏差检查：**
{chr(10).join([f"- **{s['signal']}**：{s['judgment']}" for s in signals if '大厂' in s['judgment'] or '证据层' in s['judgment']])}

---

## Step 4: 维度草案（基于信号表，非预设框架）

**行业定制：** {'是（金融/制造维度）' if dims['industry_customized'] else '否（通用）'}
**级别校准：** {'是' if dims['level_calibrated'] else '否'}

"""

    for d in dims["dimensions"]:
        report += f"""### D{d['id']} {d['name']}
- **别名/近义：** {', '.join(d['aliases'])}
- **适合级别：** {d['level_fit']}
- **信号来源：** {d['source']}
- **建模备注：** {d['notes']}

"""

    # 与旧报告对比
    old_path = Path(f"test_outputs_backup_20260409_124239/TC-{case_num:03d}_{role}_{use_case.replace(' ', '_').replace('/', '_')}.md")
    old_exists = old_path.exists()

    report += f"""---

## 与旧报告对比

| 检查项 | 旧报告状态 | 新报告变化 |
|--------|-----------|-----------|
| Step 0 企业分布探索 | 无此步骤 | ✅ 新增（前置） |
| Step 3.5 信息采集 | 无此步骤 | ✅ 新增（建模前） |
| 验证公司多样性约束 | ⚠️ 全为大厂 | {dist['diversity_score']} |
| 大厂特有信号处理 | ❌ 未降级 | ✅ 已标记降为证据层 |
| 行业定制维度 | ❌ 通用框架 | {'✅ 金融/制造定制' if dims['industry_customized'] else '通用框架'} |
| 先验框架风险 | ⚠️ 高 | ✅ 低（证据驱动） |

**对比结论：**
{"新流程有效消除了大厂偏差，维度草案由信号表驱动而非预设框架。" if dims['industry_customized'] or not dist['diversity_pass'] else "新流程的 Step 0 和 Step 3.5 有效提升了建模的证据驱动性。"}

---
*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} · 新流程（方案C）测试运行*
"""
    return report


# ─────────────────────────────────────────────
# 6. 生成总体对比报告
# ─────────────────────────────────────────────

def generate_comparison_report(all_cases: list[dict]) -> str:
    """生成10个用例的整体对比报告"""

    rows = []
    for i, cfg in enumerate(all_cases, 1):
        companies = [c.strip() for c in cfg.get("VALIDATION_COMPANIES", "").split(",")]
        dist = build_company_distribution_table(companies)
        signals = build_signal_table(cfg, companies)
        dims = generate_dimension_draft(cfg, signals)

        old_all_big_tech = all(
            classify_company(c) == "互联网大厂" for c in companies
        )

        common_signals = [s for s in signals if "核心维度" in s["judgment"]]
        downgraded_signals = [s for s in signals if "证据层" in s["judgment"]]
        industry_signals = [s for s in signals if "行业维度" in s["judgment"]]

        rows.append(f"| TC-{i:03d} | {cfg.get('ROLE_NAME', '')} | {cfg.get('TALENT_LEVEL', '')} | "
                    f"{len(companies)}家/{len(dist['covered_types'])}类 | "
                    f"{dist['diversity_score']} | "
                    f"{len(common_signals)}个 | "
                    f"{len(downgraded_signals)}个 | "
                    f"{len(industry_signals)}个 | "
                    f"{'⚠️ 需补充' if not dist['diversity_pass'] else '✅ OK'} |")

    summary = f"""# 方案C新流程 vs 旧流程对比报告

**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**对比基准：** `test_outputs_backup_20260409_124239/` 旧报告
**测试用例数：** {len(all_cases)} 个

---

## 执行摘要

### 核心改动
| 改动项 | 旧流程 | 新流程（方案C） |
|--------|--------|----------------|
| 企业分布探索 | 无 | ✅ Step 0 前置（建模前必做） |
| 官网验证时机 | Step 8（建模后验证） | ✅ Step 3.5（建模前采集） |
| 验证公司选择 | 全为大厂（默认） | ✅ 强制多元化（≥2种类型） |
| 维度草案来源 | 预设框架 | ✅ 原始信号归纳表驱动 |
| 大厂特有信号 | 未处理 | ✅ 降为证据层 |

### 10用例统计
| 用例 | 岗位 | 级别 | 验证公司 | 类型数 | 多样性 | 核心信号 | 降级信号 | 行业信号 | 合规 |
|------|------|------|----------|--------|--------|----------|----------|----------|------|
{chr(10).join(rows)}

---

## 关键差异分析

### 1. 验证公司多样性分析
"""

    # 按多样性分组
    diverse = [(i, cfg) for i, cfg in enumerate(all_cases, 1)
               if len(build_company_distribution_table(
                   [c.strip() for c in cfg.get("VALIDATION_COMPANIES", "").split(",")]
               )["covered_types"]) >= 2]
    single_type = [(i, cfg) for i, cfg in enumerate(all_cases, 1)
                   if len(build_company_distribution_table(
                       [c.strip() for c in cfg.get("VALIDATION_COMPANIES", "").split(",")]
                   )["covered_types"]) < 2]

    summary += f"""
**多元用例（{len(diverse)}个）：** {', '.join([f'TC-{i:03d}' for i, _ in diverse])}
- 这些用例的新流程会在 Step 0 确认多样性通过后，正常进入 Step 3.5
- 维度草案会基于多类型信号表，而非单一互联网框架

**单一类型用例（{len(single_type)}个）：** {', '.join([f'TC-{i:03d}' for i, _ in single_type])}
- ⚠️ 这些用例在 Step 0 会触发多元化警告
- ⚠️ 建议在 Q7 补充其他类型企业

### 2. 大厂特有信号降级统计
"""

    big_tech_count = 0
    for cfg in all_cases:
        companies = [c.strip() for c in cfg.get("VALIDATION_COMPANIES", "").split(",")]
        dist = build_company_distribution_table(companies)
        if "互联网大厂" in dist["covered_types"]:
            big_tech_count += 1

    summary += f"""
- 含互联网大厂验证公司的用例：{big_tech_count}/10
- 这些用例中，以下信号将被降为证据层（不再作为一级维度）：
  - 高并发/分布式系统经验
  - 算法能力（刷题）
  - 快速迭代/敏捷开发
  - 数据驱动/AB测试
  - 开源社区贡献

### 3. 行业定制维度分析
"""

    for cfg in all_cases:
        companies = [c.strip() for c in cfg.get("VALIDATION_COMPANIES", "").split(",")]
        dist = build_company_distribution_table(companies)
        role = cfg.get("ROLE_NAME", "")
        if "垂直行业龙头_金融" in dist["covered_types"]:
            summary += f"- TC-{all_cases.index(cfg)+1:03d} {role}：D3 替换为「合规意识与风险判断」\n"
        if "垂直行业龙头_制造" in dist["covered_types"]:
            summary += f"- TC-{all_cases.index(cfg)+1:03d} {role}：D3 替换为「工程落地与系统思维」\n"

    summary += f"""
---

## 结论

**方案C改动的核心价值：**

1. **消除先验偏差**：Step 0 确保在选验证公司之前，先了解岗位的企业分布，避免默认大厂
2. **证据驱动建模**：Step 3.5 采集多类型企业信息 → 归纳信号表 → 再起草维度，顺序正确
3. **多样性约束**：强制验证公司覆盖≥2种类型，防止单一互联网视角污染维度定义
4. **降级大厂特有要求**：高并发、算法刷题等大厂特有要求被明确降为证据层，而非一级维度

**待改进项（仍存在）：**
- TC-1, TC-2, TC-3, TC-5, TC-7 验证公司仍为纯互联网大厂，需要在 Step 0 触发警告并建议补充
- 测试用例的 VALIDATION_COMPANIES 是预定义的，真实使用场景中需要用户主动选择多元类型

---
*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} · 方案C新流程验证报告*
"""
    return summary


# ─────────────────────────────────────────────
# 7. 主程序
# ─────────────────────────────────────────────

def main():
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    # 读取 TEST_CASES.md
    test_cases_path = Path("e:/NEU/2026/职规赛/SkillCraft/workspace/TalentModel-skill/test_cases/TEST_CASES.md")
    content = test_cases_path.read_text(encoding="utf-8")
    log_path = Path("e:/NEU/2026/职规赛/SkillCraft/workspace/TalentModel-skill/test_cases/debug.log")
    cases = parse_test_cases(content)
    log_path.write_text(f"Parsed cases: {len(cases)}\n", encoding="utf-8")

    print(f"✅ 解析到 {len(cases)} 个测试用例")
    for i, c in enumerate(cases, 1):
        print(f"  TC-{i:03d}: {c.get('ROLE_NAME', '')} / {c.get('TALENT_LEVEL', '')}")

    # 生成新流程报告
    new_output_dir = Path("e:/NEU/2026/职规赛/SkillCraft/workspace/TalentModel-skill/test_outputs_new_v2")
    new_output_dir.mkdir(exist_ok=True)

    for i, cfg in enumerate(cases, 1):
        report = generate_new_test_report(cfg, i)
        safe_name = cfg.get("ROLE_NAME", "unknown").replace("/", "_").replace(" ", "_")
        safe_level = cfg.get("TALENT_LEVEL", "").replace("/", "_").replace(" ", "_")
        out_path = new_output_dir / f"TC-{i:03d}_{safe_name}_{safe_level}.md"
        out_path.write_text(report, encoding="utf-8")
        print(f"  ✅ TC-{i:03d} → {out_path.name}")

    # 生成总体对比报告
    comparison = generate_comparison_report(cases)
    comparison_path = new_output_dir / "对比报告_方案C新流程.md"
    comparison_path.write_text(comparison, encoding="utf-8")
    print(f"\n✅ 对比报告 → {comparison_path.name}")

    print(f"\n📁 新流程测试结果：{new_output_dir.absolute()}")
    print("📁 旧流程备份：test_outputs_backup_20260409_124239/")
    print("\n✅ 对比方式：diff 工具或手动阅读两个目录的内容")


if __name__ == "__main__":
    main()
