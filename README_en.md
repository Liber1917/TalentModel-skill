# TalentModel Skill

> An interactive competency modeling tool that generates three-layer competency model reports based on candidate profiles

## Features

- **Three-Layer Competency Modeling**: Above waterline (observable behaviors) → Middle (developable skills) → Below waterline (stable traits)
- **Genealogical Questioning**: StopAndThink framework — drill from abstract descriptions to concrete behavioral evidence
- **Dynamic Visualization**: Four compliant chart types (sunburst / treemap / scatter / tree), radar charts prohibited
- **Validation Engine**: Internal consistency check + campus/professional cross-contamination detection + visualization validity check
- **Multi-Scenario**: Campus hiring / Professional hiring / Promotion assessment / Team portfolio review

## Quick Start

Reference in your workflow entry:

```
Use the talent-model skill. Target role: [role name], Level: [校招/实习/资深/管理], Scenario: [recruitment/interview/promotion], Companies: [company A, company B, ...]
```

## Directory Structure

```
TalentModel-Skill/
├── SKILL.md                          # Main entry (methodology + hard constraints + interaction guide)
├── README.md                         # Chinese version
├── README_en.md                      # This file
├── references/
│   ├── html_template.md               # HTML report template reference
│   ├── enterprise_reference.md        # Enterprise type reference library
│   └── test_cases.md                 # Test case suite
├── assets/
│   ├── echarts.min.js                 # ECharts (offline mode)
│   ├── agent-workflow.html            # Agent recommended workflow visualization
│   ├── agent-workflow.svg             # SVG export version
│   └── examples/                      # Sample files
│       ├── sunburst-comparison.html   # Sunburst comparison example
│       └── ai_infra_campus.txt        # AI infra campus JD sampling
└── config_template.txt               # Configuration template
```

## Methodology Framework

### Three-Layer Iceberg Model

| Layer | Name | Characteristics |
|-------|------|----------------|
| Layer 1 | Observable Behaviors | Directly observable work behaviors and outputs |
| Layer 2 | Developable Skills | Abilities that can be improved through training |
| Layer 3 | Stable Traits | Long-term stable personality traits, hard to change in short term |

### Core Principles

1. **Data-Driven, Not Intuition-Driven** — Competencies come from candidate's actual behavioral evidence, not from inference
2. **Distinguish Observable from Unobservable** — Layer 1 must be directly observable; Layer 3 traits must be verified through probing
3. **Reject Prior Frameworks** — Do not use external assessment frameworks (e.g., McClelland, SHL) with pre-existing standards
4. **Chart Discipline** — Use only chart types that directly reflect data relationships

### Prohibited Practices

- 🚫 Radar charts (LLMs tend to use them, but they create quantification hallucinations)
- 🚫 Mixing campus/professional hiring standards
- 🚫 Directly applying external pre-built competency models
- 🚫 Treating inferred "personality traits" as Layer 1 behavioral descriptions

## Test Cases

See `references/test_cases.md` for full test suite:

| Case | Type | Validation Focus |
|------|------|------------------|
| TC001 | Tech Expert Assessment | Professional / Proficient, 8yr backend architect |
| TC002 | Campus Potential Assessment | Campus / Potential type, 985 graduate |
| TC003 | Management Promotion | M1→M2, Engineering Manager promotion |
| TC004 | Insufficient Info Questioning | Triggers probing flow, no direct output |
| TC005 | Chart Compliance | Radar prohibited, bar charts mandatory |
| TC006 | Campus/Professional Isolation | Contamination detection and alerting |

## Workflow Diagram

![Agent Recommended Workflow](assets/agent-workflow.svg)

---

This project follows anti-distillation design principles; core methodology has been desensitized for safe external sharing.
