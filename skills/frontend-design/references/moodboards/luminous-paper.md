# Luminous Paper · 清爽 SaaS 工作台

> Notion × Linear × Coda × Vercel Analytics × Pitch
> 工程师的 SaaS 美学, 刻意无 webgl 无炫光, 一切灵魂在 CSS 细节里.

## 一句话气质

**近白三阶底 + dot-grid 极淡背景 + 蓝主线 + 4 套低饱和贴纸色 + Inter/思源黑 500-600 + 无阴影 hairline 卡** — 不张扬但每一像素都精准.

调性关键词: 冷 · 清爽 · 工程 · 极简 · 像素精准.

## 视觉灵魂

### 1. 近白三阶底 + dot-grid

纯白会"白茫茫", 三阶让层次出来. dot-grid 让白底"有纸感":

```css
:root {
  --bg-base:   #ffffff;
  --bg-subtle: #f9fafb;
  --bg-hover:  #f3f4f6;
}
body {
  background-color: var(--bg-base);
  background-image:
    radial-gradient(circle at 25% 25%, rgba(59, 130, 246, 0.012) 0, transparent 50%),
    radial-gradient(rgba(0, 0, 0, 0.045) 0.8px, transparent 0.8px);
  background-size: 100% 100%, 18px 18px;
}
```

### 2. 蓝主线 + 4 套低饱和贴纸色

主线是蓝, 不是渐变, 是单色; 配 4 个低饱和贴纸色做语义标签:

```css
:root {
  --blue:    #3b82f6;            /* 主线 / CTA */
  --pink:    #fbcfe8;            /* 贴纸: 新功能 / Beta */
  --purple:  #ddd6fe;            /* 贴纸: 升级 */
  --orange:  #fed7aa;            /* 贴纸: 警示 */
  --green:   #bbf7d0;            /* 贴纸: 成功 */
}
.badge {
  display: inline-flex; align-items: center;
  padding: 3px 8px;
  border-radius: 6px;            /* 贴纸感 6px 不是 999 pill */
  font-size: 11px; font-weight: 500;
  color: #1f2937;
}
```

### 3. 无阴影 hairline 卡 (灵魂招牌)

不要 shadow, 用 0.5px hairline + 12px Notion 标准圆角. 卡之间靠**间距 + 微差背景色**分层:

```css
.card {
  background: var(--bg-base);
  border: 1px solid #e5e7eb;       /* hairline */
  border-radius: 12px;              /* Notion 标准 */
  padding: 24px;
  box-shadow: none;                 /* 无阴影是灵魂 */
}
.card:hover {
  border-color: #d1d5db;
  background: var(--bg-subtle);
  /* 仍然不加阴影 */
}
```

### 4. Inter + 思源黑, 字重 500-600 (不要 700+)

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

```css
.hero-title {
  font-family: 'Inter', 'Noto Sans SC', sans-serif;
  font-weight: 600;                 /* 不要 700, 600 才清爽 */
  font-size: clamp(2.4rem, 5vw, 4.2rem);
  letter-spacing: -0.02em;
  line-height: 1.1;
  color: #111827;
}
.body-text {
  font-weight: 400; font-size: 15px;
  line-height: 1.65; color: #6b7280;
}
.big-number {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 500;
  font-variant-numeric: tabular-nums;
}
```

### 5. Segmented control (工作台标志)

```css
.segmented {
  display: inline-flex;
  background: var(--bg-subtle);
  border-radius: 8px;
  padding: 4px;
}
.segmented button {
  padding: 6px 14px;
  border: none; background: transparent;
  font-size: 13px; font-weight: 500;
  color: #6b7280;
  border-radius: 6px;
  cursor: pointer; transition: all 0.15s;
}
.segmented button.active {
  background: var(--bg-base); color: #111827;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
```

## 工艺底线 (这些做到才是 luminous-paper 品质)

- 不用 box-shadow 撑卡 (Notion 风的反面是阴影; 灵魂是无阴影靠 hairline + 间距)
- 字重控制 500-600 (700+ 会破坏清爽感)
- 不用高饱和色 (这是低饱和贴纸色, 别上 #FF0000)
- 不用渐变 (这是单色主义, 渐变是 graphic-press 的)
- 不用 999px pill (12px 标准圆角才是这套灵魂; pill 用了违和)
- 不加 webgl / 粒子 (清爽靠克制, 不靠特效)

## 一行心法

**字重 500-600 + 卡无阴影 + dot-grid 极淡背景, 三件齐了就是 Notion 味** — 漏一个就掉到普通"扁平 UI"; 三件齐了就是顶尖工程师审美.
