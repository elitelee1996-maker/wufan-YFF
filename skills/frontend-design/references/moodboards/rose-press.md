# Rose Press · 杂志高级时装

> Vogue × Apple Newsroom × Bloomberg Businessweek × The Gentlewoman × MagCulture
> 一本你舍不得撕掉封面的 Vogue, 主编的克制与挑衅.

## 一句话气质

**浅粉雾染 mesh 底 + 唯一玫红 #E13B7A + Cormorant italic em 自动重音 + 黑白骨架 + polaroid 拍立得物感** — 高级时装杂志感.

调性关键词: 暖 · 柔粉 · 杂志 · 衬线 · 物感.

## 视觉灵魂

### 1. `<em>` 自动玫红 italic (灵魂第一招牌)

整套主题最强视觉指纹. 在标题 / 段落里直接写 `<em>关键词</em>`, **自动**变成 Cormorant 衬线斜体 + 玫红. 不用记 class, 写 em 即可:

```css
em, .rp-em {
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
  color: #E13B7A;
  font-weight: 500;
}
em:where(:lang(zh)), .rp-em:where(:lang(zh)) {
  font-family: 'Noto Serif SC', serif;
  font-style: normal;        /* 中文 italic 渲染丑, 改用宋体玫红粗体 */
  font-weight: 600;
}
```

> 用法: `<h1>这一年, 我们 <em>跨过了</em> 转折点.</h1>`

### 2. 浅粉雾染 mesh 底

不是单色浅粉, 是 4 层 radial gradient 叠出来的"雾染":

```css
:root { --bg-paper: #F2EBDD; --rose: #E13B7A; }
body {
  background-color: var(--bg-paper);
  background-image:
    radial-gradient(ellipse 800px 600px at 20% 30%, rgba(225, 59, 122, 0.08), transparent 60%),
    radial-gradient(ellipse 700px 500px at 80% 60%, rgba(225, 59, 122, 0.05), transparent 60%),
    radial-gradient(ellipse 600px 400px at 50% 90%, rgba(0, 0, 0, 0.03), transparent 60%);
  background-attachment: fixed;
}
```

### 3. Cormorant Garamond 衬线大字

```html
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500;1,600&family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
```

```css
.hero-title {
  font-family: 'Cormorant Garamond', serif;
  font-weight: 500;                /* 衬线 500 不是 700, 才有杂志味 */
  font-size: clamp(3rem, 7vw, 6rem);
  line-height: 1.05;
  letter-spacing: -0.02em;
  color: #1a1a1a;
}
```

### 4. 杂志阶梯圆角 (28 / 40 / 64px)

不是统一圆角, 按尺寸阶梯化, 像杂志大封面:

```css
.card-small  { border-radius: 28px; }
.card-medium { border-radius: 40px; }
.mag-cover   { border-radius: 64px; }    /* 大封面卡, 近圆 */
```

### 5. Polaroid 拍立得旋转卡 (灵魂招牌)

卡片轻微旋转 ±1.5°, 像拍立得贴在杂志页里:

```css
.polaroid {
  background: #fff;
  padding: 16px 16px 32px;        /* 底部留 polaroid 标签空间 */
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08), 0 16px 40px rgba(0,0,0,0.06);
  transform: rotate(-1.5deg);
  transition: transform 0.3s;
}
.polaroid:nth-child(even) { transform: rotate(1.2deg); }
.polaroid:hover { transform: rotate(0) translateY(-4px); }
.polaroid img { width: 100%; height: 280px; object-fit: cover; border-radius: 2px; }
.polaroid .caption {
  font-family: 'Cormorant Garamond', serif;
  font-style: italic; color: var(--rose);
  font-size: 14px; margin-top: 12px;
}
```

### 6. Pull-quote 引言重音

大段叙事中插入引言:

```css
.pull-quote {
  font-family: 'Cormorant Garamond', serif;
  font-style: italic; color: var(--rose);
  font-size: clamp(1.6rem, 3vw, 2.4rem);
  line-height: 1.3; letter-spacing: -0.01em;
  padding: 24px 0;
  border-top: 1px solid rgba(0,0,0,0.10);
  border-bottom: 1px solid rgba(0,0,0,0.10);
  text-align: center;
}
```

## 工艺底线 (这些做到才是 rose-press 品质)

- 不用 Inter / Roboto / Arial (灵魂是 Cormorant 衬线; 用无衬线立刻退化)
- 唯一玫红 (加蓝加绿就乱; 黑白骨架 + 玫红重音是这套的克制美学)
- 不用纯白底 (浅粉雾染 #F2EBDD 是灵魂)
- 中文不用 italic (中文斜体丑; 用宋体玫红粗体)
- 圆角阶梯化 (28/40/64, 别全用 12px)
- 不复杂动效 / 不 webgl (杂志反技术炫耀, polaroid 旋转就够)

## 一行心法

**em 是这套的 magic word** — 包关键词为 `<em>`, 自动获得衬线 + italic + 玫红, 比任何 .class 都快, 这是其它风格学不来的视觉签名.
