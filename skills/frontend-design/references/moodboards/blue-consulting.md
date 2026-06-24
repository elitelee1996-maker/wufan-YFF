# Blue Consulting · 蓝色咨询学术

> The Modern Renaissance Thesis × FT Weekend × 麦肯锡 PoV × Stripe Press × Bloomberg Annual Report
> 顶尖咨询学术论文风, 极致克制.

## 一句话气质

**深蓝底 + 唯一钢蓝 spot + Cormorant 衬线大字 + 4-6px 极小圆角 + 大量留白 + 极薄 hairline** — 90% 灰阶/蓝阶 + 10% 钢蓝点睛, 极少色 = 极强信号.

调性关键词: 暗 · 学术 · 克制 · 极简 · 论文级.

## 视觉灵魂

### 1. 深蓝底 + 唯一钢蓝 spot

```css
:root {
  --bg-deep:    #0A1128;            /* 深蓝, 不用纯黑 */
  --bg-card:    #131C3F;            /* 卡片底, 比深底浅一阶 */
  --steel-blue: #3A6EA5;            /* 唯一 spot 色, 全场只此一处亮 */
  --text-1:     #E8EDF7;
  --text-2:     #9AA8C7;
  --text-muted: #5A6688;
  --hairline:   rgba(232, 237, 247, 0.08);
}
body { background: var(--bg-deep); color: var(--text-1); }
```

### 2. Cormorant 衬线大字 + Dropcap 引言首字

学术论文味:

```html
<link href="https://fonts.googleapis.com/css2?family=Cormorant:wght@400;500;600;700&family=Noto+Serif+SC:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

```css
:root {
  --font-display: 'Cormorant', 'Noto Serif SC', serif;
  --font-body:    'Noto Serif SC', serif;
  --font-mono:    'JetBrains Mono', monospace;
}
.hero-title {
  font-family: var(--font-display);
  font-weight: 500;                 /* 衬线 500 才有论文感, 不要 700 */
  font-size: clamp(2.4rem, 5vw, 4.4rem);
  line-height: 1.1; letter-spacing: -0.01em;
  color: var(--text-1);
}
.dropcap {                          /* ⭐ dropcap 是灵魂 */
  float: left;
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 5em;
  line-height: 0.85;
  color: var(--steel-blue);
  margin: 8px 16px 0 0;
}
```

### 3. 极薄 hairline + 极小圆角 (4-6px)

跟 luminous-paper 的 12px 圆角拉开:

```css
.card {
  background: var(--bg-card);
  border: 0.5px solid var(--hairline);  /* 极薄, 0.5px 不是 1px */
  border-radius: 4px;                   /* 4-6px 极小圆角, 学术克制 */
  padding: 32px;
}
.divider {
  height: 1px;
  background: var(--hairline);          /* 横分隔线极淡 */
  margin: 48px 0;
}
```

### 4. Pull-quote + 钢蓝重音

唯一允许的"亮色", 用在最重要的判断词上:

```css
.spot-emphasis { color: var(--steel-blue); }
.pull-quote {
  font-family: var(--font-display);
  font-weight: 400;
  font-size: clamp(1.6rem, 2.8vw, 2.4rem);
  line-height: 1.4;
  color: var(--text-1);
  border-left: 2px solid var(--steel-blue);
  padding: 8px 0 8px 24px;
  margin: 32px 0;
}
.pull-quote em {
  color: var(--steel-blue);
  font-style: italic;
}
```

### 5. 数字大字 + 极宽字距

数据展示时用 mono 等宽:

```css
.big-stat {
  font-family: var(--font-mono);
  font-weight: 500;
  font-size: clamp(3.6rem, 8vw, 6.4rem);
  letter-spacing: -0.02em;
  font-variant-numeric: tabular-nums;
  color: var(--text-1);
}
.stat-label {
  font-family: var(--font-mono);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.18em;             /* 极宽字距, 论文标签味 */
  color: var(--text-muted);
}
```

## 工艺底线 (这些做到才是 blue-consulting 品质)

- 唯一钢蓝 (整页只允许 1 个亮色, 加红/绿/紫立刻掉档)
- 不用纯黑 #000 (灵魂是深蓝 #0A1128)
- 不用无衬线主显示字 (Cormorant 衬线是论文感的根, 用 Inter 立刻退化)
- 圆角必须 4-6px 极小 (12px 立刻像 SaaS 工作台)
- 大量留白 (内容密度低于其它任何风格, 这是克制美学的体现)
- 不用 emoji / 不用渐变 / 不用 webgl 装饰

## 一行心法

**克制是力量** — 90% 灰阶/蓝阶 + 10% 钢蓝点睛, 越敢"不放东西", 越显得每一处放上去的都是 important. 跟"渐变胶囊一颗接一颗"的 graphic-press 是反方向哲学.
