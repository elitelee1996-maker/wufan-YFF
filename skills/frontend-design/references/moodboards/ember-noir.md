# Ember Noir · 鎏金暗夜奢华

> Vacheron Constantin × Apple Card (钛金属) × Macallan 威士忌 × Aesop × 私人银行黑卡
> 磨砂暗夜里, 一缕香槟金的克制奢华. 不是"橙色发光", 是烫金箔压在哑光黑纸上.

## 一句话气质

**哑光暖黑深底 + 磨砂颗粒质感 + 金属拉丝纹理 + 香槟金 hairline 点睛 + 极克制的一处暖光 + Sora 几何字** — 高端腕表 / 私人银行级的沉稳奢华, 靠质感+克制而非发光.

调性关键词: 暗 · 暖 · 克制 · 奢华 · 颗粒质感.

## 视觉灵魂

### 1. 哑光暖黑底 + 磨砂颗粒 (灵魂第一招牌)

不是冷蓝黑 (那是 aurora 的事), 是带一点暖棕的哑光黑 + 噪点磨砂. 颗粒是质感的根:

```css
:root {
  --bg-void:     #0C0B09;          /* 哑光暖黑, 带一点棕 */
  --bg-card:     #15130F;
  --champagne:   #C9A86A;          /* 香槟金, 占面积 < 10% */
  --champagne-soft: rgba(201, 168, 106, 0.45);
  --hairline:    rgba(201, 168, 106, 0.18);
  --text-1:      #F5F1E6;
  --text-muted:  #8A8276;
}
body {
  background-color: var(--bg-void);
  color: var(--text-1);
}
body::before {                     /* ⭐ 磨砂颗粒, 灵魂 */
  content: ''; position: fixed; inset: 0; z-index: 0;
  pointer-events: none;
  background-image:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2'/%3E%3CfeColorMatrix values='0 0 0 0 0.79 0 0 0 0 0.66 0 0 0 0 0.42 0 0 0 0.08 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0.6;
  mix-blend-mode: overlay;
}
.stage { position: relative; z-index: 1; }
```

### 2. 香槟金 hairline + 烫金箔标题 (灵魂第二招牌)

金是稀缺点睛, 不是泛滥填充:

```css
.gold-line {                       /* 卡顶部一条香槟金 hairline, 极细 */
  height: 1px;
  background: linear-gradient(90deg,
    transparent 0%, var(--champagne) 30%, var(--champagne) 70%, transparent 100%);
  margin-bottom: 20px;
}
.foil-title {                      /* 烫金箔标题, 大字才有这处理 */
  background: linear-gradient(135deg,
    #E8C780 0%, #C9A86A 50%, #B89556 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-family: 'Sora', sans-serif;
  font-weight: 600;
  letter-spacing: -0.02em;
}
```

### 3. 玑镂纹质感 (奢华腕表的标志纹理)

```css
.guilloché-bg {                    /* 用 conic-gradient 模拟玑镂纹 */
  background:
    conic-gradient(from 0deg at 50% 50%,
      transparent 0deg, rgba(201,168,106,0.04) 1deg,
      transparent 2deg, rgba(201,168,106,0.04) 3deg,
      transparent 4deg);
  background-size: 100% 100%;
}
```

### 4. Sora 几何字 + 极宽留白

Sora 的几何感跟 Anton/Montserrat 不同, 留白多, 显克制内敛:

```html
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=Noto+Serif+SC:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

```css
:root {
  --font-display: 'Sora', sans-serif;
  --font-body:    'Sora', 'Noto Serif SC', sans-serif;
  --font-mono:    'JetBrains Mono', monospace;
}
.hero-title {
  font-family: var(--font-display);
  font-weight: 600;
  font-size: clamp(2.8rem, 6vw, 5.2rem);
  letter-spacing: -0.025em;
  line-height: 1.05;
  color: var(--text-1);
}
.body-text {
  font-weight: 300;
  font-size: 16px; line-height: 1.85;
  color: var(--text-muted);
}
```

### 5. 卡片: 哑光黑 + 极薄金 hairline

```css
.luxury-card {
  background: var(--bg-card);
  border: 0.5px solid var(--hairline);
  border-radius: 14px;             /* 不要 999 pill, 要 14px 中等 */
  padding: 32px;
  position: relative;
}
.luxury-card::before {             /* 顶部一道香槟金极细 hairline */
  content: ''; position: absolute; top: 0; left: 24px; right: 24px;
  height: 1px;
  background: linear-gradient(90deg,
    transparent, var(--champagne) 50%, transparent);
}
```

## 工艺底线 (这些做到才是 ember-noir 品质)

- 不发光 (满屏 shadowBlur 立刻廉价; 高级是靠**质感+克制**, 不是炫光)
- 香槟金面积 < 10% (灵魂是稀缺点睛; 满屏金立刻 GMV 装腔)
- 不用纯黑 #000 (灵魂是哑光暖黑 #0C0B09, 微棕)
- 必须有磨砂颗粒 (跟 aurora 的玻璃透光是反方向; 颗粒才是这套质感的根)
- 不用 Montserrat / Anton / Inter (Sora 几何 + 大量留白才是这套灵魂)
- 不加紫青 / 烈橙 (那是 noir 双子的另两套, 别串色)

## 一行心法

**克制即奢华** — 满屏金属于"穷得只剩金", 极少金才是"贵到不张扬". 跟 aurora-noir 的"满场霓虹"是反方向 — 一个张扬, 一个内敛, 同是 noir 调性, 哲学相反.
