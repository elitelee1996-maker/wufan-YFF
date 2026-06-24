# Kinetic Noir · 动感暗夜运动能量

> Nike Run Club × Whoop × Strava × Linear (Plasma) × Apple Fitness
> 黑底上烧着烈橙火焰的运动 banner.

## 一句话气质

**纯黑深底 + 烈橙红 #FF6B2E 主色 + Anton 极粗工业大写字 + 超大软圆角卡片 + 悬浮数据 pill + 橙→透明 area 渐变** — 直接有力、有温度的运动品牌质感.

调性关键词: 暗 · 暖 · 直接 · 能量 · 工业大写字.

## 视觉灵魂

### 1. 纯黑底 + 烈橙红主色

不是奢华暖黑 (那是 ember), 是中性纯黑 + 高对比烈橙. 直接、有温度:

```css
:root {
  --bg-void:    #0E0E0E;          /* 纯黑, 中性不暖不冷 */
  --bg-card:    #1A1A1A;
  --orange:     #FF6B2E;          /* 烈橙红, 主色 */
  --orange-soft: rgba(255, 107, 46, 0.20);
  --text-1:     #F5F5F5;
  --text-2:     #B8B8B8;
  --text-muted: #6E6E6E;
  --hairline:   rgba(255, 255, 255, 0.06);
}
body { background: var(--bg-void); color: var(--text-1); }
```

### 2. Anton 极粗工业大写字 (灵魂第一招牌)

整套主题最强视觉指纹. Anton condensed 极粗 + UPPERCASE + 大字号, 像运动品牌广告:

```html
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&family=Noto+Sans+SC:wght@500;600;700;800&display=swap" rel="stylesheet">
```

```css
:root {
  --font-display: 'Anton', 'Noto Sans SC', sans-serif;
  --font-body:    'Inter', 'Noto Sans SC', sans-serif;
  --font-mono:    'JetBrains Mono', monospace;
}
.hero-title {
  font-family: var(--font-display);
  font-weight: 400;                 /* Anton 只有 400 一个字重, 但天生极粗 */
  font-size: clamp(4rem, 10vw, 9rem);
  letter-spacing: 0.02em;           /* condensed 字加正字距才好看 */
  line-height: 0.95;
  text-transform: uppercase;        /* ⭐ 必须大写 */
  color: var(--text-1);
}
.kicker {                           /* 章节小标 */
  font-family: var(--font-display);
  font-size: 14px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--orange);
}
```

### 3. 超大软圆角卡 + 圆形头像/按钮 (灵魂第二招牌)

跟 Anton 的硬朗工业字形成"软硬反差":

```css
.card {
  background: var(--bg-card);
  border-radius: 28px;              /* 24-32px 超大软圆角 */
  padding: 28px;
  border: 0.5px solid var(--hairline);
}
.avatar-circle {
  width: 56px; height: 56px;
  border-radius: 50%;               /* ⭐ 圆形 */
  background: var(--orange);
  display: inline-flex; align-items: center; justify-content: center;
  font-family: var(--font-display);
  font-size: 22px;
  color: #0E0E0E;
}
.btn-pill {
  padding: 14px 28px;
  border-radius: 999px;             /* ⭐ pill 按钮 */
  background: var(--orange);
  color: #0E0E0E;
  font-family: var(--font-display);
  font-size: 14px; letter-spacing: 0.08em;
  text-transform: uppercase;
}
```

### 4. 悬浮数据 pill (灵魂第三招牌)

数据点旁边浮一个小 pill 标注, 像 Strava / Apple Fitness:

```css
.data-pill {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 6px 12px;
  border-radius: 999px;
  background: var(--orange);
  color: #0E0E0E;
  font-family: var(--font-mono);
  font-weight: 600; font-size: 12px;
}
.data-pill::before {                 /* 三角箭头方向, 表示趋势 */
  content: '↑';
  font-size: 11px;
}
```

### 5. 橙→透明 area 渐变 (chart / hero 背景)

线性图、hero 背景都用这种"运动燃烧感"渐变:

```css
.energy-area {
  background: linear-gradient(180deg,
    rgba(255, 107, 46, 0.32) 0%,
    rgba(255, 107, 46, 0.12) 50%,
    transparent 100%);
}
.hero-bg {                          /* hero 背景: 橙色光晕从底部往上 */
  background: radial-gradient(ellipse 800px 400px at 50% 100%,
    rgba(255, 107, 46, 0.18), transparent 70%);
}
```

## 工艺底线 (这些做到才是 kinetic-noir 品质)

- 必须 Anton 极粗大写字 (Montserrat / Inter 都掉档; Anton condensed 是这套灵魂)
- 必须 24-32px 超大软圆角 (12px 立刻像普通暗色 UI; 跟 Anton 的硬朗形成软硬反差)
- 必须有橙→透明渐变 (能量燃烧感, 没了立刻像普通深色)
- 不发光 (这是直接有力, 不是奢华内敛, 也不是赛博炫光)
- 不用金 (那是 ember-noir; 烈橙才是这套灵魂)
- 不加紫青 (那是 aurora; 别串色)

## 一行心法

**软硬反差** — Anton 极粗大写字是硬, 24-32px 超大软圆角是软. 一刚一柔撑起这套"运动直接 + 设计感"的张力, 漏一边就掉档.
