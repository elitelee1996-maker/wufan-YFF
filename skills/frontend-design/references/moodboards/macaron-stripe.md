# Macaron Stripe · 马卡龙糖果条纹

> Apple Card UI × Cash App × Robinhood × 韩系生活方式 App
> 把马卡龙摆在印着斜纹的奶油蛋糕上, 软糯但有设计张力.

## 一句话气质

**浅灰绿底 + 薄荷绿/薰衣草紫马卡龙双主色 + 斜条纹/圆点纹理 + 24-40px 超大软圆角 + Poppins 极粗大数字 + 一张近黑卡反差** — 柔与硬撞出的设计张力.

调性关键词: 柔 · 糖果 · 条纹质感 · 大圆角 · 黑卡反差.

## 视觉灵魂

### 1. 马卡龙双主色 + 浅灰绿底 + 黑卡反差 (灵魂第一招牌)

铁律: 马卡龙色块**亮**, 上面放**深色字**; 近黑卡上放**浅色字**:

```css
:root {
  --bg-page:    #E4EAE4;          /* 浅灰绿底 (不是纯白, 带一点灰绿) */
  --bg-card:    #FFFFFF;
  --bg-black:   #1C1C1E;          /* ⭐ 近黑反差卡, 至少 1 张 */
  --mint:       #A8E6A0;          /* 薄荷绿主色 */
  --mint-deep:  #7DD87A;
  --lavender:   #B0A4F5;          /* 薰衣草紫主色 */
  --lavender-deep: #9B8AF0;
  --ink:        #1C1C1E;
  --ink-soft:   #5A5A5E;
  --ink-on-color: #1C1C1E;        /* 色块上放深色字 */
}
body { background: var(--bg-page); }
```

### 2. 斜条纹 + 圆点纹理 (灵魂第二招牌, 最大灵魂)

整套主题最独特的视觉指纹. 在色块的**一部分**填条纹/圆点, 表达"部分 / 进度 / 质感":

```css
/* 斜条纹纹理 (45° repeating-linear-gradient) */
.stripe-mint {
  background-image: repeating-linear-gradient(
    -45deg,
    rgba(28,28,30,0.14) 0, rgba(28,28,30,0.14) 2px,
    transparent 2px, transparent 7px
  );
}
/* 圆点纹理 (radial-gradient) */
.dot-tex {
  background-image: radial-gradient(circle, rgba(28,28,30,0.16) 1.2px, transparent 1.2px);
  background-size: 9px 9px;
}
/* 典型用法: 一个色块上半实心, 下半条纹 (表示"已达成 vs 目标") */
.bar-block {
  background: var(--mint);
  border-radius: 16px;
  position: relative; overflow: hidden;
}
.bar-block .hatched {
  position: absolute; inset: 0 0 60% 0;
  background-image: repeating-linear-gradient(
    -45deg,
    rgba(28,28,30,0.16) 0 2px,
    transparent 2px 7px
  );
}
```

### 3. 超大软圆角 + 圆形 icon (灵魂第三招牌)

```css
:root { --r-card: 32px; --r-block: 20px; --r-pill: 999px; }
.card  { border-radius: var(--r-card); }      /* 卡片 24-40px 超大软圆角 */
.block { border-radius: var(--r-block); }     /* 色块 16-24px */
.icon-btn {                                    /* 圆形 icon button */
  width: 40px; height: 40px; border-radius: 50%;
  background: #fff;
  border: 1px solid rgba(28,28,30,0.08);
  display: inline-flex; align-items: center; justify-content: center;
}
```

### 4. Poppins 极粗大数字

```html
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Inter:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
```

```css
:root {
  --font-display: 'Poppins', 'Inter', sans-serif;     /* 几何无衬线圆润 */
  --font-body:    'Inter', 'Noto Sans SC', sans-serif;
}
.big-number, .kpi-value {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: clamp(2.2rem, 4vw, 3.4rem);
  letter-spacing: -0.03em; line-height: 1;
  font-variant-numeric: tabular-nums;
}
.hero-title {
  font-family: var(--font-display);
  font-weight: 800;
  font-size: clamp(2.8rem, 6vw, 5rem);
  letter-spacing: -0.025em;
  line-height: 1.05;
}
```

### 5. 近黑反差卡 (灵魂第四招牌, 必须有 ≥ 1 张)

```css
.dark-card {
  background: var(--bg-black);
  color: #fff;
  border-radius: var(--r-card);
  padding: 28px;
}
.dark-card .label { color: rgba(255,255,255,0.6); font-size: 12px; }
.dark-card .value { font-size: 2.4rem; font-weight: 700; color: #fff; }
```

## 工艺底线 (这些做到才是 macaron-stripe 品质)

- 必须有斜条纹 / 圆点纹理 (这是最大灵魂招牌, 没了就普通糖果色)
- 必须有近黑反差卡 (灵魂是马卡龙亮色块 + 1 张近黑卡的强反差; 全亮就平了)
- 不用纯白底 (灵魂是浅灰绿 #E4EAE4, 带一点灰绿才柔)
- 不用 sharp 小圆角 (必须 24-40px 超大软圆角)
- 马卡龙色块上放深色字 (亮色块上浅字立刻退化)
- 不用衬线字 (Poppins / Inter 几何无衬线才是这套灵魂)
- 双主色必须交替 (满屏绿就单调了, 薄荷绿 + 薰衣草紫要交替)

## 一行心法

**柔 × 硬的张力** — 马卡龙色 + 超大软圆角是柔, 斜条纹/圆点纹理 + 近黑反差卡是硬. 一柔一硬撑起这套"软糯但有设计感"的平衡, 漏任何一边都会破坏.
