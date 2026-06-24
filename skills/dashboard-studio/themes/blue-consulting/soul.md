# Blue Consulting · 蓝色咨询风

> The Modern Renaissance Thesis × FT Weekend × 麦肯锡 PoV × Stripe Press × Bloomberg Annual Report
> — **顶尖咨询学术论文风**. 深蓝底 + 钢蓝单 spot + 衬线大字 + 极致克制.

---

## 一句话理念

**深蓝底 + 唯一钢蓝 spot + 衬线大字 + 极小圆角 + 大量留白 = 顶尖咨询/学术期刊感**.

90% 灰阶/蓝阶 + 10% 钢蓝点睛. **极少色 = 极强信号**. 跟 graphic-press 的"鲜艳报刊"哲学相反 — 这是**克制美学**.

---

## ⚡⭐ 灵魂背景动效 · 3D 深蓝点云球 ❗ 是**背景层**, 不是首屏 hero

这是 blue-consulting **最标志性的视觉特性**, 老 midnight-thesis 时代就在的灵魂遗产. **任何 blue-consulting 产物 (editorial / dashboard) 都必须带上这个动效, 缺了就立刻退化成"普通深蓝主题"**.

构成: 32 阶 IcosahedronGeometry (~1k 点) + simplex 3D noise 顶点位移 + 钢蓝→深蓝渐变 + additive blending + opacity 0.32~0.38 + 缓慢呼吸旋转 + 靠右悬浮 (窄屏自动居中).

### ⚠️ 最大坑 (90% Agent 都会踩): 误把它当首屏 hero

它是**永远在最底层呼吸的背景动效**, 你的 Hero / KPI / 章节 / 表格全部**叠在它之上**. 不是页面打开看到一个孤零零的大球, 是页面打开看到**正常的 Hero 跟内容**, 然后背景里**若隐若现**有个点云球在呼吸:

```
✅ 正确 (z-index 分层)               ❌ 错误 (Agent 常踩)
┌───────────────────────────┐        ┌───────────────────────────┐
│ Hero · 一座城市的 分层 折叠 │        │                           │
│ ─────────────────────────  │        │              .·.    .'.   │
│  KPI · KPI · KPI · KPI    │ ← z:1 │           .: ·★·    ·   │
│  ─────────────────────    │        │            '. : .'        │
│  章节 / 段落 / 表格 / ...   │        │          (点云球独占首屏,  │
│   . ·☆.   (背景层呼吸)    │ ← z:0 │           看上去像 splash) │
└───────────────────────────┘        └───────────────────────────┘
```

### 怎么加 (三件套, 全部 4 个位置, 一个都不能漏)

直接抄 `editorial-example.html` 或 `dashboard-example.html` 里这 4 个位置的代码 **一字不改**:

| # | 位置 | 抄什么 | 漏了的后果 |
|---|---|---|---|
| ① | `<head>` 内 | three.js CDN `<script>` 一行 | three.js 加载不到, 报 `THREE is undefined`, 没球 |
| ② | `<body>` 开头 (`<div class="dash">` 之前) | `<div id="bg-orb"></div>` 一行 | host 不存在, IIFE 找不到挂载点, 没球 |
| ③ | **`<style>` 段里 (中部)** | **`#bg-orb { ... }` CSS 块 + `.dash, .page { position: relative; z-index: 1 }`** | **⚡ 最容易漏! 漏了 = 点云球变成普通 block 占满首屏, 内容被推到下方** |
| ④ | `</script>` 之前 (页面最末尾) | `mountPointCloudOrb` IIFE 整段 (~160 行) | 没渲染逻辑, 没球 |

### ⚡ ⚡ ⚡ ③ 号位是 90% Agent 都会漏的位置, 单独高亮

因为 #bg-orb 的 CSS 块在 example.html 的 `<style>` 段里, 容易被 Agent 抄 CSS 时跳过. **必抄的 4 行 CSS 是这个**:

```css
/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
/* ⚡⚡⚡ 灵魂背景动效 · #bg-orb 必抄 CSS (漏抄 = 90% Agent 都犯的错)        */
/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
#bg-orb {
  position: fixed; inset: 0;
  z-index: 0; pointer-events: none;
  opacity: 0.32;           /* dashboard 用 0.32, editorial 用 0.38 */
  mix-blend-mode: screen;
}
/* ❗ 这一行**绝不能漏**! 漏了主内容会被点云球盖住, 全屏一片空只看见个球 */
.dash, .page { position: relative; z-index: 1; }
```

**❗ 抄完后用 grep 自检**: 在你生成的 HTML 文件里搜 `#bg-orb`, 应该至少出现 **3 次** — ① CSS 选择器 (`#bg-orb {`) ② IIFE 里的 `getElementById('bg-orb')` ③ HTML 的 `<div id="bg-orb">`. 少于 3 次 = 你漏了上面那段 CSS.

### 自检 (写完打开看)

- ✅ 打开页面**第一眼看到的是 Hero / KPI 的正常内容**, 点云球若隐若现在背景里
- ❌ 打开页面**只看到一个大球**占满屏幕, 上面没内容 → 你十有八九漏了 ③ 号位 (#bg-orb 的 CSS 块没抄), 或者漏了 `.dash / .page { z-index: 1 }` 那行
- ❌ 没任何球出现, console 报 `THREE is undefined` → 漏了 ① three.js CDN
- ❌ 没任何球出现, 但 console 干净 → 漏了 ② host div 或 ④ IIFE

---

## 跟 graphic-press 对照 (两套主题的哲学完全相反)

| 维度 | Graphic Press | Blue Consulting |
|---|---|---|
| 哲学 | 鲜艳报刊艺术 | 咨询学术克制 |
| 底色 | 米黄纸 #e9e7e2 | 深蓝 #0A1128 |
| 颜色 | 5 套渐变胶囊轮流 | 唯一钢蓝 #3A6EA5 |
| 圆角 | 999px 全场 pill | 4-6px 极小 |
| 字体 | Space Grotesk 几何 | Cormorant Garamond 衬线 (拉丁) + Noto Serif SC (中文) |
| 数字 | 几何无衬线 | 衬线大字 / Manrope 副 |
| 装饰 | 大色棍交叉 + 胶囊 + 拍立得 | 极薄 hairline + 钢蓝细线 + dropcap |
| 适合 | 创意 / 鲜艳 / 营销 / 年度 Wrapped | 咨询 / 学术 / 战略复盘 / 投资分析 / 行业研究 |

---

## 跨 archetype 通用 (视觉灵魂跨形态不变)

blue-consulting **同时支持 dashboard 跟 editorial**:

| | dashboard 形态 | editorial 形态 |
|---|---|---|
| 用什么 | 紧凑顶 nav + 简洁 KPI 阵 + 单色筛选 + 钢蓝 chart + 极薄明细表 | sticky 顶 nav + kicker 横线 + 大字衬线主标 + dropcap 引言 + 章节叙事 |
| 看哪个 example | `dashboard-example.html` | `editorial-example.html` |
| 看哪个 playbook | `references/dashboard-playbook.md` | `references/editorial-playbook.md` |

---

## 视觉灵魂 (8 个不可丢的招牌)

### 1. 近黑深蓝底 #0A1128 (灵魂)

```css
body { background-color: #0A1128; color: #F4F4F5; }
```

不是真黑, 是**带 5% 蓝色调的近黑** — 比纯黑更暖, 比深灰更冷. 咨询期刊感的关键.

### 2. 唯一钢蓝 spot #3A6EA5

```css
:root {
  --accent: #3A6EA5;
  --accent-hi: #5689C2;          /* hover */
  --accent-soft: rgba(58,110,165,0.30);  /* 弱辅助 */
  --hairline: rgba(244,244,245,0.08);    /* 极薄边框 */
}
```

**全工程只用这一个色**做 spot. 不超过 5-10% 像素面积. 极致克制.

### 3. Cormorant Garamond 衬线 + Noto Serif SC 中文衬线

```css
:root {
  --font-serif:    'Cormorant Garamond', 'Noto Serif SC', serif;
  --font-cn-serif: 'Noto Serif SC', 'Cormorant Garamond', serif;
  --font-sans:     'Manrope', 'Noto Sans SC', sans-serif;
}
```

主标用衬线大字 (5rem light 500), em 钢蓝斜体. Manrope light 300 做副字体 / 元数据.

### 4. ⭐ Lead 首字 dropcap (灵魂招牌)

```css
.lead::first-letter {
  float: left;
  font-family: var(--font-serif);
  font-weight: 600; font-size: 4em; line-height: 0.84;
  color: var(--accent-hi);
  padding-right: 0.1em; margin: 0.08em 0.32em 0 0;
}
```

引言段第一个字会自动派生为 4em 大字 — **咨询报告的灵魂招牌, 一眼就知道是 "Blue Consulting"**.

### 5. Kicker 横线 + 斜体

```css
.kicker {
  font-family: var(--font-serif); font-style: italic;
  color: var(--accent-hi); letter-spacing: 0.08em;
  display: inline-flex; align-items: center; gap: 14px;
}
.kicker::before {
  content: ''; display: inline-block;
  width: 36px; height: 1px; background: var(--accent);
}
```

每节顶部一行斜体 kicker 带 36px 钢蓝细线. **不是胶囊**, 是**期刊编号感**.

### 6. 极小圆角 4-6px (跟 graphic-press 的 999px 哲学完全相反)

```css
:root {
  --radius-sm: 3px; --radius-md: 4px; --radius-card: 6px;
}
```

学术期刊感. 卡片几乎不圆, 数据表完全直角.

### 7. 极薄 hairline 边框 (0.5px / rgba 0.08)

```css
.card { border: 0.5px solid rgba(255,255,255,0.08); }
.hairline { border-bottom: 0.5px solid rgba(255,255,255,0.08); }
```

跟 graphic-press 的"色块大胶囊"形成最大对比. 边框几乎不可见, 用极少线条划分区域.

### 8. mono UPPERCASE 编号 + Spectral 数字

```css
.section-num {
  font-family: 'Space Mono', monospace;
  font-size: 11px; letter-spacing: 0.12em;
  text-transform: uppercase; color: var(--accent);
}
.big-number {
  font-family: var(--font-serif);
  font-size: 3rem; font-weight: 500;
  color: var(--accent-hi);
}
```

数字用衬线大字 (期刊感), 标签用 mono UPPERCASE (咨询感).

---

## ❌ 必避 (做了立刻失去 Blue Consulting 味)

- ❌ **没有 3D 深蓝点云球背景** (这是最大招牌, 抄 example 末尾 IIFE 整段, 不带 = 退化成普通深蓝)
- ❌ **把 3D 点云球当首屏 hero 主视觉** (它是 **z-index:0 背景层**, Hero / KPI / 段落必须 z-index:1 叠在它**之上**. 打开页面看到的应该是正常内容 + 背景里若隐若现一个呼吸的球, 不是一个孤零零的大球占满屏幕)
- ❌ 漏写 `.dash / .page { position: relative; z-index: 1 }` (主内容容器没提 z-index → content 被 fixed 的 bg-orb 盖住 → 看上去全屏空白只剩一个球)
- ❌ 把 `<div id="bg-orb">` 放进 `<main>` 或 `.dash` 里面 (它必须**直接挂在 `<body>` 上**, 跟主内容容器**同级**, 而且在它**之前**)
- ❌ 用渐变胶囊柱状 (那是 graphic-press)
- ❌ 999px 大圆角 (用 4-6px 极小)
- ❌ 米黄底 / 白底 (必须深蓝 #0A1128)
- ❌ 多色 (只用钢蓝 + 灰阶)
- ❌ 几何无衬线主标 (必须 Cormorant + Noto Serif SC)
- ❌ 厚重视觉装饰 (要"极致克制", 大量留白)
- ❌ 大字 hero 不带 dropcap (引言 dropcap 是灵魂招牌)
- ❌ Section 编号用纯数字 "1." "2." (用 mono UPPERCASE "01 / SECTION")
- ❌ **HTML 文案 / 最终回复文本里用 emoji 跟装饰 unicode** (📊 💡 ✓ ★ ✨ ❗ ...). blue-consulting 是顶级咨询学术气质, 一个 emoji 立刻掉档. 用 `<em>` 钢蓝 spot / mono 编号 / 衬线大字代替. 详见 SKILL.md "🚫 严禁 emoji" 段

---

## ECharts 配色 (顶层 spread)

```js
const bcEchartsBase = {
  color: ['#5689C2', '#3A6EA5', '#94A3B8', '#64748B', '#475569', '#34D399', '#F87171'],
  textStyle: { fontFamily: "'Manrope', 'Noto Sans SC', sans-serif", color: '#F4F4F5' },
  backgroundColor: 'transparent',
  tooltip: {
    backgroundColor: 'rgba(15,23,42,0.95)',
    borderColor: 'rgba(58,110,165,0.30)',
    borderWidth: 0.5,
    textStyle: { color: '#F4F4F5' }
  },
  legend: { textStyle: { color: '#CBD5E1', fontSize: 11 } },
  xAxis: {
    axisLine: { lineStyle: { color: 'rgba(244,244,245,0.12)', width: 0.5 } },
    axisLabel: { color: '#94A3B8', fontSize: 10, fontFamily: 'Space Mono, monospace' },
    splitLine: { show: false }
  },
  yAxis: {
    axisLine: { show: false },
    axisLabel: { color: '#94A3B8', fontSize: 10, fontFamily: 'Space Mono, monospace' },
    splitLine: { lineStyle: { color: 'rgba(244,244,245,0.05)', type: 'dashed' } }
  }
};
```

**series 用钢蓝细线** (lineStyle width 1.5), bar 用钢蓝单色 + 极小圆角 (borderRadius 2). **绝对不要渐变填充**, 跟 graphic-press 形成对比.

---

## 适用业务

- **editorial 首选**: 战略复盘 / 投资分析 / 行业研究 / 咨询报告 / 学术论文 / 年度 thesis / 政策研究
- **dashboard 首选**: 咨询型 BI / 投资监控驾驶舱 / 严肃业务看板 (跟 graphic-press 的"鲜艳看板"互补)
- **不适**: 营销 / 鲜艳风格 / Spotify Wrapped (用 graphic-press)

---

## 关键提示

看完 `editorial-example.html` 跟 `dashboard-example.html` 就知道这套理念的呈现方式. **不要从 0 写 CSS**, 直接抄 example 的 `<style>` 段, 改业务即可.

⚠ **抄的时候连 `mountPointCloudOrb` 那段 IIFE + `#bg-orb` host + `three@0.158.0` CDN 三件套一起抄**, 千万别漏 — 那是 blue-consulting 的灵魂动效.

⚠⚠ **再次强调**: 点云球是**背景层** (z-index: 0). 你写完打开浏览器, **第一眼必须看到正常的 Hero / KPI / 段落**, 背景里若隐若现一个球在呼吸. 如果看到只有一个大球占满屏幕、上面啥也没有 — 说明你**漏了主容器的 `position: relative; z-index: 1`**, 或者**把 `<div id="bg-orb">` 错放进了主容器里面**. 这是 90% Agent 都会踩的坑, 上一节有 ASCII 示意图.
