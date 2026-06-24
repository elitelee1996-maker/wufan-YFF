# Graphic Press · 多彩胶囊报刊

> Spotify Wrapped × Apple Newsroom × Penguin Books × Wallpaper* Magazine
> Spotify Wrapped 投放到再生纸上的视觉语言.

## 一句话气质

**米黄纸张底 + 45° 暗线纹理 + 5 套渐变胶囊 + 全场 999px pill 圆角 + Space Grotesk 几何字** — 印刷品质感 + 鲜艳色彩, 整页读完是色彩旅程.

调性关键词: 暖 · 鲜艳 · 报刊艺术 · 印刷感 · pill 圆角节奏.

## 视觉灵魂

### 1. 米黄纸底 + 45° 暗线纹理 (灵魂第一招牌)

让 HTML 看起来像印在再生纸上, 而不是网页上:

```css
:root { --bg-paper: #e9e7e2; }
body { background: var(--bg-paper); }
body::before {
  content: ''; position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background-image: repeating-linear-gradient(
    45deg, transparent 0 2px,
    rgba(0,0,0,0.025) 2px 3px,
    transparent 3px 5px
  );
  opacity: 0.6;
}
.stage { position: relative; z-index: 1; }
```

### 2. 5 套 135° 双色渐变 (灵魂第二招牌 — 叙事色谱)

每个数字 / 章节 / 标签**配一个不同的渐变胸标**, 整页读完像翻杂志:

```css
:root {
  --grad-fire:  linear-gradient(135deg, #ff2a2a 0%, #ff8c00 100%);   /* 火焰 */
  --grad-ocean: linear-gradient(135deg, #00b359 0%, #0055ff 100%);   /* 海洋 */
  --grad-berry: linear-gradient(135deg, #a322ff 0%, #ff4d88 100%);   /* 浆果 */
  --grad-sun:   linear-gradient(135deg, #ffb300 0%, #ff5500 100%);   /* 日落 */
  --grad-mint:  linear-gradient(135deg, #00d9c4 0%, #00a2ff 100%);   /* 薄荷 */
}
.pill {
  display: inline-flex; align-items: center;
  padding: 6px 16px;
  border-radius: 999px;
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 600; font-size: 12px;
  text-transform: uppercase; letter-spacing: 0.08em;
  color: #fff;
}
.pill-fire { background: var(--grad-fire); }
.pill-ocean { background: var(--grad-ocean); }
/* 5 套交替用, 不要只用一套 */
```

### 3. 全场 999px pill 圆角

不只是按钮, **Header / 卡片 / 标签**都用 pill, 是这套主题的视觉签名:

```css
.dash-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 14px 22px;
  border-radius: 999px;            /* Header 也是 pill */
  background: #fff;
  border: 0.5px solid rgba(0,0,0,0.08);
  box-shadow: 0 2px 12px rgba(0,0,0,0.03);
}
.tag { padding: 4px 10px; border-radius: 999px;
  background: #fff; border: 1px solid rgba(0,0,0,0.10); }
```

### 4. Space Grotesk 几何字

```html
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
```

```css
:root {
  --font-display: 'Space Grotesk', sans-serif;
  --font-body:    'Noto Sans SC', 'Inter', sans-serif;
}
.hero-title {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: clamp(2.8rem, 6vw, 5rem);
  letter-spacing: -0.03em;
  color: #1a1918;
}
.big-number {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: clamp(3rem, 7vw, 6rem);
  letter-spacing: -0.04em;
  font-variant-numeric: tabular-nums;
}
```

## 工艺底线 (这些做到才是 graphic-press 品质)

- 不用纯白底 (灵魂是米黄 #e9e7e2 + 暗线纹理, 纯白立刻平淡)
- 5 套渐变交替 (一种用到底就不是叙事色谱)
- pill 圆角覆盖到 Header / 卡片 / 标签 (是签名, 不只是按钮)
- 不混衬线字体 (那是 rose-press / blue-consulting 的事)
- 不加 webgl / 复杂动效 (报刊感是平面的, 不靠特效)

## 一行心法

**Pill 是动词不是装饰** — 把所有"需要强调"的元素 (header / 数字 / 标签 / CTA) 都做成 pill, 整页就有"被一颗一颗按下去的图章感", 这就是这套风格的灵魂.
