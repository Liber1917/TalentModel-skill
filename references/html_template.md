# HTML 报告模板参考

> 本模板用于生成胜任力模型可视化报告

## 模板结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>胜任力模型报告</title>

  <!-- ECharts CDN -->
  <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>

  <style>
    :root {
      --primary: #2C3E50;
      --accent: #3498DB;
      --success: #27AE60;
      --warning: #F39C12;
      --danger: #E74C3C;
      --bg: #F8F9FA;
    }

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background: var(--bg);
      color: var(--primary);
      line-height: 1.6;
    }

    /* 图表容器 - 透明背景 */
    .chart-container {
      width: 100%;
      height: 400px;
      background: transparent !important;
    }

    .section {
      padding: 2rem;
      max-width: 1200px;
      margin: 0 auto;
    }

    .card {
      background: white;
      border-radius: 8px;
      padding: 1.5rem;
      margin-bottom: 1.5rem;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }

    h1, h2, h3 { color: var(--primary); }
    h1 { font-size: 1.75rem; margin-bottom: 0.5rem; }
    h2 { font-size: 1.25rem; margin-bottom: 1rem; border-left: 4px solid var(--accent); padding-left: 0.75rem; }
    h3 { font-size: 1rem; margin: 1rem 0 0.5rem; }

    .meta {
      color: #666;
      font-size: 0.875rem;
      margin-bottom: 1.5rem;
    }

    .competency-item {
      padding: 0.75rem;
      border-left: 3px solid var(--accent);
      background: rgba(52, 152, 219, 0.05);
      margin-bottom: 0.75rem;
      border-radius: 0 4px 4px 0;
    }

    .tag {
      display: inline-block;
      padding: 0.25rem 0.5rem;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 600;
    }

    .tag-high { background: rgba(231, 76, 60, 0.15); color: var(--danger); }
    .tag-medium { background: rgba(243, 156, 18, 0.15); color: var(--warning); }
    .tag-low { background: rgba(39, 174, 96, 0.15); color: var(--success); }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 1.5rem;
    }

    footer {
      text-align: center;
      padding: 2rem;
      color: #999;
      font-size: 0.75rem;
    }
  </style>
</head>
<body>

  <!-- 报告头部 -->
  <header class="section">
    <h1>胜任力模型报告</h1>
    <p class="meta">
      候选人：<span id="candidate-name">-</span> &nbsp;|&nbsp;
      岗位：<span id="candidate-role">-</span> &nbsp;|&nbsp;
      生成时间：<span id="report-date">-</span>
    </p>
  </header>

  <!-- 三层胜任力模型 -->
  <section class="section">
    <div class="grid">

      <!-- Layer 1: 可观测行为 -->
      <div class="card">
        <h2>Layer 1 · 可观测行为</h2>
        <p style="color:#666;font-size:0.875rem;margin-bottom:1rem;">
          可直接观察的工作行为和产出
        </p>
        <div id="layer1-chart" class="chart-container"></div>
        <div id="layer1-list"></div>
      </div>

      <!-- Layer 2: 可发展能力 -->
      <div class="card">
        <h2>Layer 2 · 可发展能力</h2>
        <p style="color:#666;font-size:0.875rem;margin-bottom:1rem;">
          通过培养可提升的能力
        </p>
        <div id="layer2-chart" class="chart-container"></div>
        <div id="layer2-list"></div>
      </div>

    </div>
  </section>

  <!-- Layer 3: 不易改变特质 -->
  <section class="section">
    <div class="card">
      <h2>Layer 3 · 不易改变特质</h2>
      <p style="color:#666;font-size:0.875rem;margin-bottom:1rem;">
        长期稳定的人格特质，难以短期改变
      </p>
      <div id="layer3-chart" class="chart-container"></div>
      <div id="layer3-list"></div>
    </div>
  </section>

  <!-- 图表导出功能 -->
  <section class="section">
    <div class="card">
      <h2>导出报告</h2>
      <button onclick="exportChart('layer1-chart', 'layer1')" class="export-btn">导出 Layer 1 图表</button>
      <button onclick="exportChart('layer2-chart', 'layer2')" class="export-btn">导出 Layer 2 图表</button>
      <button onclick="exportChart('layer3-chart', 'layer3')" class="export-btn">导出 Layer 3 图表</button>
    </div>
  </section>

  <footer>
    本报告由胜任力建模系统生成 · 仅供参考
  </footer>

  <script>
    // 图表初始化函数
    function initCharts(data) {
      // Layer 1: 分组柱状图
      const layer1Chart = echarts.init(document.getElementById('layer1-chart'));
      layer1Chart.setOption({
        backgroundColor: 'transparent',
        tooltip: { trigger: 'axis' },
        legend: { top: 10, textStyle: { color: '#666' } },
        xAxis: {
          type: 'category',
          data: data.layer1.map(d => d.name),
          axisLabel: { color: '#333', rotate: 15 }
        },
        yAxis: {
          type: 'value',
          max: 5,
          axisLabel: { color: '#666' }
        },
        series: [
          {
            name: '当前水平',
            type: 'bar',
            data: data.layer1.map(d => d.current),
            itemStyle: { color: '#3498DB' }
          },
          {
            name: '目标水平',
            type: 'bar',
            data: data.layer1.map(d => d.target),
            itemStyle: { color: '#27AE60' }
          }
        ]
      });

      // Layer 3: 树图
      const layer3Chart = echarts.init(document.getElementById('layer3-chart'));
      layer3Chart.setOption({
        backgroundColor: 'transparent',
        tooltip: { trigger: 'item' },
        series: [{
          type: 'tree',
          data: [data.layer3Root],
          label: { position: 'left', color: '#333' },
          leaves: { label: { position: 'right' } },
          initialTreeDepth: 3
        }]
      });
    }

    // 图表导出函数
    function exportChart(chartId, filename) {
      const chartDom = document.getElementById(chartId);
      const chart = echarts.getInstanceByDom(chartDom);
      if (!chart) return;

      // 导出 SVG
      const svgData = chart.getDataURL({ type: 'svg' });
      const svgLink = document.createElement('a');
      svgLink.download = filename + '.svg';
      svgLink.href = svgData;
      svgLink.click();

      // 导出 PNG
      const pngData = chart.getDataURL({ type: 'png', pixelRatio: 2, backgroundColor: '#fff' });
      const pngLink = document.createElement('a');
      pngLink.download = filename + '.png';
      pngLink.href = pngData;
      pngLink.click();
    }

    // 数据填充
    const reportData = {
      layer1: [
        { name: '系统设计', current: 4, target: 5 },
        { name: '技术方案', current: 4, target: 5 },
        { name: '跨团队协作', current: 3, target: 4 }
      ],
      layer2: [
        { name: '技术视野', current: 3, target: 5 },
        { name: '技术影响力', current: 2, target: 4 },
        { name: '人才培养', current: 2, target: 4 }
      ],
      layer3Root: {
        name: '深层特质',
        children: [
          { name: '追求卓越', children: [
            { name: '对稳定性有执念' },
            { name: '不妥协质量' }
          ]},
          { name: '长期主义', children: [
            { name: '考虑长期维护' },
            { name: '拒绝短期捷径' }
          ]},
          { name: '风险意识', children: [
            { name: '预防性思维' },
            { name: '兜底方案' }
          ]}
        ]
      }
    };

    // 初始化
    document.addEventListener('DOMContentLoaded', () => {
      initCharts(reportData);
    });
  </script>

</body>
</html>
```

## 关键实现要点

### 1. 图表背景透明

```css
.chart-container {
  background: transparent !important;
}

/* ECharts 初始化时也设置透明 */
chart.setOption({
  backgroundColor: 'transparent'
});
```

### 2. 导出 SVG / PNG

使用 ECharts 原生 API，不依赖 html2canvas：

```javascript
// SVG 导出
const svgData = chart.getDataURL({ type: 'svg' });

// PNG 导出（支持透明背景）
const pngData = chart.getDataURL({
  type: 'png',
  pixelRatio: 2,  // 2x 分辨率
  backgroundColor: '#fff'  // 或 '#transparent'
});
```

### 3. 禁止使用雷达图

```javascript
// ❌ 错误示例
series: [{ type: 'radar', ... }]

// ✅ 正确示例：使用分组柱状图
series: [
  { name: '当前水平', type: 'bar', data: [...] },
  { name: '目标水平', type: 'bar', data: [...] }
]
```

### 4. 图表类型选择决策树

```
能力项数量 ≤ 7 且需横向对比？
├── 是 → 分组柱状图
└── 否 → 考虑其他类型
    ├── 展示层级关系 → 树图 / 嵌套圆环图
    ├── 展示时间变化 → 折线图
    └── 展示分布 → 散点图 / 气泡图
```

### 5. 量化描述规范

```
❌ "沟通能力很强"
✅ "在 X 项目中，通过与 Y 部门的跨团队沟通，缩短了 Z 天的交付周期"

❌ "技术很牛"
✅ "QPS 从 500 提升到 5000，可用性从 99% 提升到 99.9%"

❌ "学习能力不错"
✅ "3 个月内从 0 到 1 掌握了 Kubernetes，并主导了容器化迁移"
```
