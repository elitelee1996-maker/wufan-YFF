# Prism Studio · 科技品牌编辑设计

> Solvd × Stripe Press × Pentagram × Mirror.xyz × 现代科技品牌编辑系统
> 优雅衬线 × 电光紫绿 × 几何线框 × 拼贴反差, 像一本会发光的品牌杂志.

## 一句话气质

**炭黑 / 暖米白拼贴底 + Fraunces 现代衬线大标题 + 电光紫绿光谱渐变 + 3D 等距线框几何 + 像素条形马赛克** — 自信现代、有人文温度的科技品牌编辑设计, 全程零发光.

调性关键词: 暗 · 人文 · 衬线 · 扁平 · 拼贴反差.

## 视觉灵魂

### 1. 炭黑 + 暖米白拼贴底 (灵魂第一招牌)

不是单一深底 (那是 aurora / ember), 是**两种底色并置拼贴**, 像杂志开页:

```css
:root {
  --bg-charcoal: #161618;            /* 炭黑, 不是纯黑 */
  --bg-cream:    #F5F1E6;            /* 暖米白, 跟炭黑反差强 */
  --electric-purple: #6C4FF5;        /* 电光紫, 扁平实色 */
  --neon-green:      #3DF577;        /* 荧光绿, 高饱和扁平 */
  --text-1-dark:     #F5F1E6;
  --text-1-light:    #161618;
}
/* 拼贴布局: 半屏炭黑半屏米白 (或上下分) */
.split-bg {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 100vh;
}
.split-bg .left  { background: var(--bg-charcoal); color: var(--text-1-dark); }
.split-bg .right { background: var(--bg-cream); color: var(--text-1-light); }
```

### 2. Fraunces 现代衬线大标题 (灵魂第二招牌)

跟 aurora-noir / ember-noir 拉开差距的关键 — 这套是**衬线**, 给冰冷科技注入人文气质:

```html
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

```css
:root {
  --font-display: 'Fraunces', serif;             /* ⭐ 现代衬线, 灵魂 */
  --font-body:    'Inter', 'Noto Sans SC', sans-serif;
  --font-mono:    'JetBrains Mono', monospace;
}
.hero-title {
  font-family: var(--font-display);
  font-variation-settings: 'opsz' 144;            /* Fraunces 大字优化 */
  font-weight: 600;
  font-size: clamp(3.6rem, 8vw, 7rem);
  letter-spacing: -0.025em;
  line-height: 0.95;
  color: var(--text-1-dark);
}
```

### 3. 电光紫绿光谱渐变

跟 aurora 的"发光"哲学相反, 这是**扁平实色 + 渐变**, 全程零 shadowBlur:

```css
.spectrum-pill {
  display: inline-flex; align-items: center;
  padding: 8px 20px;
  border-radius: 999px;
  background: linear-gradient(90deg, var(--electric-purple), var(--neon-green));
  color: #fff;
  font-family: var(--font-mono);
  font-weight: 500; font-size: 13px;
}
.flat-purple { background: var(--electric-purple); }   /* 扁平实色 */
.flat-green  { background: var(--neon-green); color: #161618; }
```

### 4. 3D 等距线框几何 (灵魂第三招牌)

不是 webgl 渲染的 3D, 是 SVG / CSS 画的等距线框 — 数学几何感:

```css
.iso-wireframe {
  width: 240px; height: 240px;
  position: relative;
}
.iso-wireframe::before {
  /* 用 conic-gradient + transform: skew 模拟等距视图 */
  content: ''; position: absolute; inset: 20%;
  border: 1.5px solid var(--electric-purple);
  transform: rotate(45deg) skew(-10deg, -10deg);
}
.iso-wireframe::after {
  content: ''; position: absolute; inset: 30%;
  border: 1.5px solid var(--neon-green);
  transform: rotate(45deg) skew(-10deg, -10deg) translate(20%, 20%);
}
```

### 5. 像素条形马赛克 (灵魂第四招牌)

复古像素 + 紫绿光带, 像 Stripe Press 封面:

```css
.pixel-band {
  display: grid;
  grid-template-columns: repeat(40, 1fr);
  gap: 2px;
  height: 12px;
}
.pixel-band div {
  background: var(--electric-purple);
  /* 给每个偶数 / 第 5 个换色 — 用 nth-child 实现马赛克分布 */
}
.pixel-band div:nth-child(3n)   { background: var(--neon-green); }
.pixel-band div:nth-child(7n)   { background: transparent; }
.pixel-band div:nth-child(11n)  { background: var(--bg-cream); }
```

### 6. 米白胶囊 + 方块 logo

拼贴反差的小元件:

```css
.cream-pill {
  background: var(--bg-cream);
  color: var(--text-1-light);
  padding: 6px 14px;
  border-radius: 999px;
  font-family: var(--font-display);
  font-weight: 500; font-size: 12px;
}
.square-logo {                       /* 方块 logo, 跟圆形头像反向 */
  width: 32px; height: 32px;
  background: var(--electric-purple);
  border-radius: 4px;
  display: inline-flex; align-items: center; justify-content: center;
  color: #fff;
  font-family: var(--font-display);
  font-weight: 700;
}
```

## 工艺底线 (这些做到才是 prism-studio 品质)

- 必须 Fraunces 现代衬线大标题 (用无衬线立刻退化成普通暗色 UI)
- 全程零发光 (没有 shadowBlur, 没有 backdrop blur; 这是扁平人文派, 不是赛博发光派)
- 必须有炭黑/米白拼贴 (单一深底就退化)
- 紫绿是高饱和扁平实色 (加 glow 立刻像 aurora)
- 圆角中等 14px (不是 macaron 的 32px 软, 不是 blue 的 4px 极小)
- 不用纯黑 #000 (灵魂是炭黑 #161618)

## 一行心法

**衬线 × 几何 = 人文 × 科技** — Fraunces 衬线是人文温度, 等距线框 + 像素马赛克 + 电光紫绿是科技未来. 撞出来的张力是这套"会发光的品牌杂志"独有.
