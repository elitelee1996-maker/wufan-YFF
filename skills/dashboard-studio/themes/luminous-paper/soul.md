# Luminous Paper · 晨光纸笺

> Notion × Linear × Coda × Monday.com × Vercel Analytics × Pitch
> — **清爽明亮的工程师 SaaS 工作台**. 刻意无 webgl / 无动效装饰, 一切灵魂在 CSS 细节里.

---

## 一句话理念

**近白三阶底 + dot-grid 极淡背景 + 蓝主线 + 4 套低饱和贴纸色 + Inter/思源黑 500-600 + 无阴影 hairline 卡 = 顶级现代 SaaS 工作台**.

跟 graphic-press / blue-consulting / rose-press / aurora-noir 的哲学**都不一样** — 这是**第五条路: Notion / Linear 的明亮清爽工程师美学, 不张扬但每一像素都精准**.

---

## 跟其他 4 套的五角对比 (5 套主题完全分立)

| 维度 | Graphic Press | Blue Consulting | Rose Press | Aurora Noir | **Luminous Paper** |
|---|---|---|---|---|---|
| 哲学 | 鲜艳报刊艺术 | 咨询学术克制 | 杂志高级时装 | 暗夜霓虹电影感 | **清爽 SaaS 工作台 (Notion / Linear)** |
| 明暗 | 暖亮 (米黄) | 暗 (深蓝) | 暖亮 (浅粉) | 暗 (近黑) | **冷亮 (近白 #fff)** |
| 底色 | 米黄 #e9e7e2 + 45° 暗线 | 深蓝 #0A1128 | 浅粉 mesh #F2EBDD | 近黑 #030406 + 极光 | **近白三阶 #fff/#f9fafb/#f3f4f6 + dot-grid** |
| 主色 | 5 套渐变胶囊 | 唯一钢蓝 | 唯一玫红 | 主紫 + cyan 协奏 | **蓝主线 #3b82f6 + 4 贴纸色 (粉/紫/橙/绿)** |
| 字体 | Space Grotesk 几何 | Cormorant 衬线 | Cormorant italic 衬线 | Montserrat 极粗 | **Inter + 思源黑 SC 500-600 (不要 700)** |
| 圆角 | 999px 全场 pill | 4-6px 极小 | 28/40/64 杂志阶梯 | 8/12px + pill | **12px (Notion 标准)** |
| 卡片质感 | 印刷渐变胶囊 | 极薄 hairline | 杂志大圆角 + 拍立得 | 玻璃 + backdrop blur | **无阴影 1px hairline + 12px 圆角 (灵魂)** |
| 灵魂招牌 | 5 套渐变胶囊胸标 | dropcap + 3D 点云球 | em 玫红 italic + polaroid | CSS 极光 + 玻璃震慑卡 + shadowBlur | **dot-grid 底 + 4 套贴纸色 badge + 无阴影 hairline 卡 + tabular-nums 数字** |
| 适合业务 | 创意 / 营销 / Wrapped | 咨询 / 学术 / 投研 | 时装 / 品牌 / 杂志 | Web3 / 加密 / 科技炫酷 | **SaaS 产品 / 项目管理 / 团队协作 / 数据运营 / 工程效率 / B 端 BI** |

**记忆锚点**: 5 套里只有 luminous-paper 是"**明亮清爽**"的. 想做 Notion / Linear / Vercel 那种干净工作台感, 就是它.

---

## 跨 archetype 通用 (视觉灵魂跨形态不变)

luminous-paper **同时支持 dashboard 跟 editorial**:

| | dashboard 形态 | editorial 形态 |
|---|---|---|
| 用什么 | 紧凑标题 (无 sticky topbar) + **KPI 严格 4 张** + 周期 segmented + 全局筛选 + 无阴影 panel + 明细表 | 清爽长报告 + 蓝色 dropcap + 章节叙事 + takeaway alert 提示块 + 3 列短评 |
| 看哪个 example | `dashboard-example.html` | `editorial-example.html` |
| 看哪个 playbook | `references/dashboard-playbook.md` | `references/editorial-playbook.md` |

---

## ⭐ 视觉灵魂 (4 个不可丢的招牌, 一个少了就不是 luminous-paper)

### 1. ⭐ 近白三阶底 + dot-grid 极淡背景 — **第一品牌印记**

纯白会"白茫茫", 三阶让层次出来. dot-grid 让白底"有纸感":

```css
:root {
  --bg-base:   #ffffff;   /* 主底 */
  --bg-subtle: #f9fafb;   /* 卡片底 / 二级区 */
  --bg-hover:  #f3f4f6;   /* 三阶 / hover */
}
body {
  background-color: var(--bg-base);
  /* dot-grid 极淡背景 (灵魂: 让白底不白茫茫) */
  background-image: radial-gradient(circle, rgba(17, 24, 39, 0.055) 0.6px, transparent 0.6px);
  background-size: 22px 22px;
}
```

### 2. ⭐ 无阴影 hairline 卡 — **第二品牌印记 (Notion 灵魂)**

**决不用阴影撑卡片** (那是 Bootstrap). 靠 1px hairline + 12px 圆角:

```css
.card, .kpi, .panel {
  background: var(--bg-base);
  border: 1px solid #e5e7eb;        /* 1px hairline */
  border-radius: 12px;              /* Notion 标准 */
  box-shadow: none;                 /* ❗ 灵魂: 无阴影 */
  padding: 24px;
}
.card:hover { border-color: #d1d5db; background: var(--bg-subtle); transition: all .15s; }
```

### 3. ⭐ 4 套低饱和贴纸色 badge (语义严格) — **第三品牌印记**

蓝是主线, 4 套贴纸色是状态语义 (Notion/Linear 的 Stuck/Done/Todo/Doing 列表色), **严格语义, 不许乱用**:

```css
:root {
  --accent:     #3b82f6;   /* 蓝: 主线 / 进度 / 唯一主 accent */
  --pink:   #ec4899;  --pink-bg:   #fce7f3;  --pink-text:   #db2777;   /* Stuck 受阻 */
  --purple: #a855f7;  --purple-bg: #f3e8ff;  --purple-text: #7e22ce;   /* Done 完成 */
  --orange: #f97316;  --orange-bg: #ffedd5;  --orange-text: #c2410c;   /* Todo 待办 */
  --green:  #10b981;  --green-bg:  #dcfce7;  --green-text:  #15803d;   /* Doing 进行中 */
}
.badge { display:inline-flex; align-items:center; gap:6px; padding:3px 10px; border-radius:999px; font-size:12px; font-weight:600; }
.badge.stuck { background: var(--pink-bg);   color: var(--pink-text); }
.badge.done  { background: var(--purple-bg); color: var(--purple-text); }
.badge.todo  { background: var(--orange-bg); color: var(--orange-text); }
.badge.doing { background: var(--green-bg);  color: var(--green-text); }
```

### 4. ⭐ Inter + 思源黑 500-600 + tabular-nums 数字 — **第四品牌印记**

中文用思源黑 **500-600 weight** (不要 700, 太"喊"), 行高 1.7-1.85; 数字 Inter `font-variant-numeric: tabular-nums` 等宽对齐:

```css
:root {
  --font-display: 'Inter', system-ui, sans-serif;
  --font-body:    'Inter', 'Noto Sans SC', sans-serif;
  --font-cn:      'Noto Sans SC', 'PingFang SC', sans-serif;
}
.title { font-family: var(--font-display); font-weight: 600; letter-spacing: -0.01em; color: #111827; }
.title:lang(zh) { font-family: var(--font-cn); font-weight: 600; }  /* 中文 600 上限, 不 700 */
.kpi-value, .big-number {
  font-family: var(--font-display);
  font-weight: 700; font-size: clamp(1.9rem, 3vw, 2.4rem);
  font-variant-numeric: tabular-nums;   /* 等宽数字, 中文环境对齐 */
  letter-spacing: -0.02em; color: #111827;
}
```

---

## ❌ 必避 (做了立刻失去 Luminous Paper 味)

- ❌ **用阴影撑卡片** (那是 Bootstrap, 不是 Notion; 灵魂是 1px hairline + 圆角 + 无阴影)
- ❌ **用衬线字体** (那是 blue-consulting / rose-press 路线; luminous 必须 Inter + 思源黑无衬线)
- ❌ **中文用 700 weight** (太"喊", 上限 600; 标题 600, 正文 400-500)
- ❌ **KPI 不是严格 4 张一排** (Linear / Vercel / Stripe 标准, 数字是重点)
- ❌ **暗底 / 鲜艳底** (luminous 灵魂是近白 #fff 三阶 + dot-grid)
- ❌ **4 套贴纸色乱用 / 滥用进 KPI 主区** (它们是状态 badge / chart 语义, 主区保持克制)
- ❌ 漏 dot-grid (白底会"白茫茫"廉价)
- ❌ 加 webgl / 粒子 / 协作光标 / shader 动画 / 鼠标视差 (落地页道具, 工作台不需要)
- ❌ 加 sticky topbar / workspace 头部 / 用户头像群 / 分享按钮 (那是 SaaS 产品壳, 不是仪表盘内容)
- ❌ **在 KPI 卡上加显眼色条 / 竖线 / 边框装饰** (太丑, 卡片本身的克制就够)
- ❌ **HTML 文案 / 最终回复文本里用 emoji 跟装饰 unicode** (📊 💡 ✓ ★ ✨ ❗ ...). luminous 是克制工程师气质, emoji 立刻破坏精确感

---

## ECharts 配色 (顶层 spread)

```js
const lpEchartsBase = {
  color: ['#3b82f6', '#10b981', '#a855f7', '#f97316', '#ec4899'],  // 5 色: 蓝(主)/绿/紫/橙/粉
  textStyle: { color: '#111827', fontFamily: "'Inter', 'Noto Sans SC', sans-serif" },
  backgroundColor: 'transparent',
  grid: { left: '6%', right: '4%', top: '14%', bottom: '12%', containLabel: true },
  tooltip: {
    trigger: 'axis',
    backgroundColor: 'rgba(255,255,255,0.98)',
    borderColor: '#e5e7eb', borderWidth: 1, padding: [10, 14],
    textStyle: { color: '#111827', fontSize: 12, fontFamily: "'Inter', sans-serif" },
    extraCssText: 'box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.10), 0 4px 6px -4px rgb(0 0 0 / 0.05); border-radius: 8px;',
    axisPointer: { type: 'line', lineStyle: { color: '#3b82f6', type: 'dashed', width: 1, opacity: 0.5 } }
  },
  legend: { top: 4, right: 8, textStyle: { color: '#6b7280', fontSize: 12 }, icon: 'circle', itemWidth: 8, itemHeight: 8, itemGap: 18 },
  xAxis: {
    type: 'category',
    axisLine: { lineStyle: { color: '#e5e7eb' } }, axisTick: { show: false },
    axisLabel: { color: '#6b7280', fontSize: 11, margin: 10 },
    splitLine: { show: false }
  },
  yAxis: {
    type: 'value',
    axisLine: { show: false }, axisTick: { show: false },
    axisLabel: { color: '#6b7280', fontSize: 11 },
    splitLine: { lineStyle: { color: '#f3f4f6', type: 'dashed' } }
  }
};
```

**series 一律"扁平 + 干净" — 无 shadowBlur (这是 luminous 跟 aurora-noir 的关键反差)**:
- `bar`: `itemStyle: { color, borderRadius: [4, 4, 0, 0] }` (圆角顶, 无 glow)
- `line`: `lineStyle: { color: '#3b82f6', width: 2.2 }` + 浅色 area 渐变 (0.15 → 0)
- `donut`: `itemStyle: { borderColor: '#fff', borderWidth: 4, borderRadius: 4 }` (白色描边)
- 永远不要 shadowBlur / 渐变填充柱 — 那是别的主题

---

## 适用业务

- **dashboard 首选**: SaaS 产品 dashboard / 项目管理看板 / 团队协作数据台 / 工程效率指标 / 数据运营周报 / B 端业务 BI
- **editorial 首选**: 产品复盘报告 / 数据分析周报 / 工程师友好的清爽长读 / SaaS 增长报告 / 团队 OKR 回顾
- **不适**: 暗夜炫酷 (用 aurora-noir) / 严肃财报 (用 blue-consulting) / 鲜艳营销 (用 graphic-press) / 时装杂志 (用 rose-press)

---

## 关键提示

看完 `editorial-example.html` 跟 `dashboard-example.html` 就知道这套理念的呈现方式. **不要从 0 写 CSS**, 直接抄 example 的 `<style>` 段, 改业务即可.

⚠ luminous-paper 的精髓是**克制 + 精确** — 不靠任何特效撑场, 全靠"近白三阶 + dot-grid + 无阴影 hairline + 思源黑 500-600 + tabular-nums" 这些细节堆出工程师 SaaS 的高级感. 抄的时候**别加阴影、别加衬线、别上 700 weight、别加 webgl** — 任何一个都会立刻破坏这套克制美学.
