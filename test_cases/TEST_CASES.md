# TalentModel-skill 测试用例集
# 测试目标：验证 skill 的泛化能力以及先验胜任力模型的恰当性

---

## 测试用例 1：技术类 - 社招中级

```yaml
ROLE_NAME: 后端开发工程师
TALENT_LEVEL: 社招 3-5年
USE_CASE: 招聘筛选
VALIDATION_COMPANIES: 字节跳动, 阿里云, 腾讯
OUTPUT_FORMAT: html
SELF_CHECK_MATRIX: false
CHART_RENDER: cdn
```

---

## 测试用例 2：技术类 - 校招

```yaml
ROLE_NAME: 前端开发实习生
TALENT_LEVEL: 校招大三/研二
USE_CASE: 实习招聘
VALIDATION_COMPANIES: 字节跳动, 美团, 网易
OUTPUT_FORMAT: markdown
SELF_CHECK_MATRIX: false
CHART_RENDER: offline
```

---

## 测试用例 3：产品类

```yaml
ROLE_NAME: 产品经理
TALENT_LEVEL: 社招 5年+
USE_CASE: 晋升评估
VALIDATION_COMPANIES: 腾讯, 阿里, 字节跳动
OUTPUT_FORMAT: html
SELF_CHECK_MATRIX: true
CHART_RENDER: offline
```

---

## 测试用例 4：设计类

```yaml
ROLE_NAME: UI/UX 设计师
TALENT_LEVEL: 社招 1-3年
USE_CASE: 招聘筛选
VALIDATION_COMPANIES: 字节跳动, 小米, 大疆
OUTPUT_FORMAT: html
SELF_CHECK_MATRIX: true
CHART_RENDER: cdn
```

---

## 测试用例 5：数据类

```yaml
ROLE_NAME: 数据分析师
TALENT_LEVEL: 校招
USE_CASE: 校园招聘
VALIDATION_COMPANIES: 阿里巴巴, 腾讯, 京东
OUTPUT_FORMAT: markdown
SELF_CHECK_MATRIX: false
CHART_RENDER: offline
```

---

## 测试用例 6：算法类 - 高级

```yaml
ROLE_NAME: 算法工程师（推荐方向）
TALENT_LEVEL: 资深专家 P7+
USE_CASE: 高端人才猎聘
VALIDATION_COMPANIES: 字节跳动, 快手, 阿里妈妈
OUTPUT_FORMAT: html
SELF_CHECK_MATRIX: false
CHART_RENDER: cdn
```

---

## 测试用例 7：运营类

```yaml
ROLE_NAME: 用户运营
TALENT_LEVEL: 社招 2-4年
USE_CASE: 招聘面试设计
VALIDATION_COMPANIES: 拼多多, 美团, 滴滴
OUTPUT_FORMAT: html
SELF_CHECK_MATRIX: true
CHART_RENDER: offline
```

---

## 测试用例 8：管理类

```yaml
ROLE_NAME: 技术团队负责人（TL）
TALENT_LEVEL: 管理者 10-30人团队
USE_CASE: 晋升评估
VALIDATION_COMPANIES: 腾讯, 阿里云, 字节跳动
OUTPUT_FORMAT: html
SELF_CHECK_MATRIX: false
CHART_RENDER: offline
```

---

## 测试用例 9：传统行业 - 金融

```yaml
ROLE_NAME: 金融科技工程师
TALENT_LEVEL: 社招 3-5年
USE_CASE: 内部培训规划
VALIDATION_COMPANIES: 蚂蚁集团, 腾讯金融科技, 招商银行金融科技
OUTPUT_FORMAT: html
SELF_CHECK_MATRIX: true
CHART_RENDER: offline
```

---

## 测试用例 10：传统行业 - 制造业

```yaml
ROLE_NAME: 智能制造工程师
TALENT_LEVEL: 社招 5年+
USE_CASE: 人才盘点
VALIDATION_COMPANIES: 华为, 海尔智家, 比亚迪
OUTPUT_FORMAT: markdown
SELF_CHECK_MATRIX: false
CHART_RENDER: offline
```

---

## 测试覆盖矩阵

| 维度 | 覆盖情况 |
|------|----------|
| 岗位类型 | 技术(3), 产品(1), 设计(1), 数据(1), 运营(1), 管理(1), 金融(1), 制造(1) |
| 人才级别 | 校招(3), 初级(2), 中级(2), 资深(2), 管理(1) |
| 使用场景 | 招聘筛选(4), 晋升评估(2), 面试设计(1), 培训规划(1), 人才盘点(1), 猎聘(1) |
| 行业 | 互联网(7), 金融(1), 制造(1), 混合(1) |
| 输出格式 | HTML(7), Markdown(3) |
| 自测矩阵 | 是(4), 否(6) |
| 渲染方式 | 离线(7), CDN(3) |

---

生成时间：2026-04-09 04:00
