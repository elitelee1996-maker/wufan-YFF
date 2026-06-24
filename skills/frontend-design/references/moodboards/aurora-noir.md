# Aurora Noir · 暗夜霓虹电影感

> Cursor × Phantom Wallet × Apple Vision Pro × Linear Dark
> 漂在北极光里的玻璃片, 装置艺术级科技高级感.

## 一句话气质

**近黑深底 + CSS 极光环境光 + 玻璃震慑卡 + 紫青霓虹双色 + Montserrat 极粗大字** — 不是普通"深色主题", 是真极光打在你脸上的暗夜.

调性关键词: 冷 · 赛博 · 炫光 · 玻璃质感 · 大字气场.

## 视觉灵魂

### 1. CSS 极光环境光 (灵魂招牌)

完全 CSS 实现, 不依赖图片. **是 z-index:0 背景层**, 主内容必须叠在 z-index:1 上面 (常见错误是把它做成首屏 hero):

```css
.aurora-bg {
  position: fixed; inset: 0; z-index: 0; pointer-events: none;
  background-color: #030406;
  background-image:
    radial-gradient(ellipse 1200px 800px at 25% 25%, rgba(6,182,212,0.16), transparent 55%),
    radial-gradient(ellipse 1100px 750px at 75% 75%, rgba(139,43,246,0.20), transparent 55%);
}
.aurora-bg::before {
  content: ''; position: absolute; inset: 0;
  background:
    radial-gradient(ellipse 700px 360px at 18% 28%, rgba(74,222,128,0.16), transparent 60%),
    radial-gradient(ellipse 900px 480px at 80% 35%, rgba(139,43,246,0.22), transparent 60%),
    radial-gradient(ellipse 800px 420px at 45% 70%, rgba(6,182,212,0.16), transparent 60%);
  filter: blur(40px) saturate(1.4); mix-blend-mode: screen; opacity: 0.82;
}
.stage { position: relative; z-index: 1; }
```

> 用法: `<body><div class="aurora-bg"></div><main class="stage">真内容</main></body>`

### 2. 玻璃震慑卡 (backdrop-filter blur)

像漂在极光里的玻璃片:

```css
.glass-card {
  background: rgba(15, 20, 25, 0.40);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 0.5px solid rgba(255, 255, 255, 0.10);
  border-radius: 12px;
  padding: 28px;
  position: relative; overflow: hidden;
}
.glass-card::before {  /* 右上角 radial 高光, 玻璃质感的精髓 */
  content: ''; position: absolute; top: 0; right: 0;
  width: 60%; height: 60%;
  background: radial-gradient(ellipse at top right, rgba(139,43,246,0.10), transparent 70%);
  pointer-events: none;
}
```

### 3. 紫青霓虹色 + 严格语义

```css
:root {
  --bg-void:    #030406;          /* 不用纯黑 #000, 用微蓝深黑 */
  --accent:     #8B2BF6;          /* 主紫: hero / CTA */
  --neon-cyan:  #06B6D4;          /* 协奏色 / 次重音 */
  --neon-green: #4ADE80;          /* 正向 / UP */
  --neon-red:   #EF4444;          /* 告警 / DOWN */
  --neon-amber: #ffd166;          /* 中性提示 */
}
```

### 4. Montserrat 极粗大字 + 等宽数字

```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800;900&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
```

```css
.hero-title {
  font-family: 'Montserrat', sans-serif;
  font-weight: 900;                    /* 极粗灵魂 */
  font-size: clamp(3rem, 7vw, 6rem);
  letter-spacing: -0.03em;
  text-transform: uppercase;
  color: #fff;
  text-shadow: 0 0 40px rgba(139, 43, 246, 0.40);
}
.big-number {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}
```

## 工艺底线 (这些做到才是 aurora-noir 品质)

- 不用纯黑 `#000` (灵魂是 `#030406`, 略带蓝)
- 极光是背景层 (z-index:0), 内容必须叠 z-index:1
- 玻璃卡必带 `backdrop-filter: blur` (没了立刻廉价)
- 色彩限制在紫 / cyan / 翠青 / 玫红 / 琥珀 (加粉 / 棕 / 暖橙就不是 aurora 了)
- Hero 大字必须极粗 (Montserrat 800-900), 数字必须等宽 (`tabular-nums`)

## 一行心法

**背景永远是 z-index:0 的 CSS 极光层, 内容叠在 z-index:1 上面**. 这是它跟"普通深色主题"的根本区别 — 让用户一眼感觉到"漂在光里", 而不是"在黑色里看东西".
