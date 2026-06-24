# Aurora Noir · 暗夜极光

> Microsoft Build × Apple Vision Pro × Cursor × Linear Dark × Phantom Wallet × Liquid Glass
> — **电影感暗夜霓虹**. 不是"暗色主题", 是**真极光打在你脸上的暗夜**.

---

## 一句话理念

**近黑深底 + CSS 极光环境光 + 玻璃震慑卡 + 三辉光 + cyan 协奏 + Montserrat 极粗大字 = 装置艺术级科技高级感**.

跟 graphic-press / blue-consulting / rose-press 的哲学**都不一样** — 这是**第四条路: Cursor / Phantom Wallet / Microsoft Build 的产品级霓虹电影感, 像漂在北极光里的玻璃片**.

---

## 跟其他 3 套的四角对比 (4 套主题完全分立)

| 维度 | Graphic Press | Blue Consulting | Rose Press | **Aurora Noir** |
|---|---|---|---|---|
| 哲学 | 鲜艳报刊艺术 (Spotify Wrapped) | 咨询学术克制 (Bloomberg) | 杂志高级时装 (Vogue) | **暗夜霓虹电影感 (Cursor / Phantom)** |
| 底色 | 米黄 #e9e7e2 + 45° 暗线 | 深蓝 #0A1128 | 浅粉 mesh #F2EBDD | **近黑 #030406 + CSS 极光环境光** |
| 主色 | 5 套渐变胶囊 | 唯一钢蓝 #3A6EA5 | 唯一玫红 #E13B7A | **主紫 #8B2BF6 + cyan #06B6D4 协奏 + 4 霓虹语义色** |
| 字体 | Space Grotesk 几何 | Cormorant 衬线 | Cormorant italic + 玫红 em | **Montserrat 极粗 700/900 + JetBrains Mono** |
| 圆角 | 999px 全场 pill | 4-6px 极小 | 28/40/64 杂志阶梯 | **8px 卡 / 12px panel / pill 按钮** |
| 灵魂招牌 | 5 套渐变胶囊胸标 | dropcap 引言首字 + 3D 点云球 | em 玫红 italic + polaroid 拍立得 + pull-quote | **CSS 极光环境光 + 玻璃震慑卡 + 主紫 hero CTA + chart 真"光圈" (shadowBlur)** |
| 卡片质感 | 印刷渐变胶囊 | 极薄 hairline | 杂志大圆角 + 拍立得旋转 | **半透玻璃 + backdrop-filter blur(20px) + 右上角 radial 高光** |
| 适合业务 | 创意 / 营销 / Wrapped / 年报 | 咨询 / 学术 / 战略 / 投研 | 时装 / 品牌 / 编辑部 / Vogue 感 | **Web3 / 加密 / 科技产品 / SaaS / 实时监控 / 创业团队 keynote** |

---

## 跨 archetype 通用 (视觉灵魂跨形态不变)

aurora-noir **同时支持 dashboard 跟 editorial**, 玻璃卡 + 极光底跨形态完全一致:

| | dashboard 形态 | editorial 形态 |
|---|---|---|
| 用什么 | 紧凑 Header + **KPI 严格 4 张** + 全局筛选 + 玻璃 panel + 明细表 | 大字 Hero (主紫 CTA) + dropcap 主紫色块 + 章节叙事 + chart hero viz + 引语主紫光圈 |
| 看哪个 example | `dashboard-example.html` | `editorial-example.html` |
| 看哪个 playbook | `references/dashboard-playbook.md` | `references/editorial-playbook.md` |

---

## ⭐ 视觉灵魂 (4 个不可丢的招牌, 一个少了就不是 aurora-noir)

### 1. ⚡⭐ CSS 极光环境光背景 — **第一品牌印记**

整套主题最大视觉指纹. **完全 CSS 实现**, 不依赖任何外部图片资源, 单文件自包含:

```css
.an-aurora-bg {
  position: fixed; inset: 0;
  z-index: 0; pointer-events: none;
  background-color: #030406;
  /* 双 radial 色温底 (cyan + purple, 极淡) */
  background-image:
    radial-gradient(ellipse 1200px 800px at 25% 25%, rgba(6, 182, 212, 0.16), transparent 55%),
    radial-gradient(ellipse 1100px 750px at 75% 75%, rgba(139, 43, 246, 0.20), transparent 55%);
  isolation: isolate;
}
.an-aurora-bg::before {
  content: '';
  position: absolute; inset: 0;
  /* 极光带状光晕 - 多层渐变叠加, 模拟北极光的色光弥漫 */
  background:
    radial-gradient(ellipse 700px 360px at 18% 28%, rgba(74, 222, 128, 0.18), transparent 60%),
    radial-gradient(ellipse 900px 480px at 80% 35%, rgba(139, 43, 246, 0.22), transparent 60%),
    radial-gradient(ellipse 800px 420px at 45% 70%, rgba(6, 182, 212, 0.16), transparent 60%),
    radial-gradient(ellipse 600px 320px at 90% 80%, rgba(255, 209, 102, 0.10), transparent 60%);
  filter: blur(40px) saturate(1.4);
  mix-blend-mode: screen;
  opacity: 0.85;
}
.an-aurora-bg::after {
  content: '';
  position: absolute; inset: 0;
  /* vignette 把光裁到中央, 边缘暗下去 */
  background:
    radial-gradient(ellipse at center, transparent 35%, #030406 95%),
    linear-gradient(to right, #030406 0%, transparent 25%, transparent 75%, #030406 100%),
    linear-gradient(to bottom, #030406 0%, transparent 20%, #030406 95%);
  pointer-events: none;
}
```

⚡ **重要**: `.an-aurora-bg` 是 **z-index 0 背景层**, **不是首屏 hero**! 永远在最底层呼吸, 上面叠 `<main class="an-stage">` 装真内容. 主内容必须 `position: relative; z-index: 1` 才不会被极光盖住.

### 2. ⭐ 玻璃震慑卡 — **第二品牌印记**

所有 KPI / panel / 章节卡都用半透玻璃 + backdrop-filter blur, 像漂在极光里的玻璃片:

```css
.kpi, .panel {
  background: rgba(15, 20, 25, 0.40);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 0.5px solid rgba(255, 255, 255, 0.10);
  border-radius: 8px;
  padding: 24px;
  position: relative;
  overflow: hidden;
}
/* 右上角 radial 高光, 玻璃质感的精髓 */
.kpi::before, .panel::before {
  content: '';
  position: absolute;
  top: 0; right: 0;
  width: 60%; height: 60%;
  background: radial-gradient(ellipse at top right,
    rgba(139, 43, 246, 0.10), transparent 70%);
  pointer-events: none;
}
.kpi:hover, .panel:hover {
  transform: translateY(-2px);
  border-color: rgba(139, 43, 246, 0.30);
  box-shadow: 0 12px 36px rgba(139, 43, 246, 0.15);
}
```

### 3. ⭐ 三辉光 + cyan 协奏 (语义严格) — **第三品牌印记**

**4 个霓虹色, 每个有严格语义, 不许乱用**:

```css
:root {
  --accent:        #8B2BF6;          /* 主紫: hero / CTA / 唯一 active 描边 */
  --accent-glow:   rgba(139, 43, 246, 0.50);
  --neon-cyan:     #06B6D4;          /* cyan: 协奏色 / 主视觉次重音 / area 渐变收尾 */
  --neon-cyan-glow:rgba(6, 182, 212, 0.50);
  --neon-green:    #4ADE80;          /* 翠青: UP / 在线 / 正向 delta */
  --neon-red:      #EF4444;          /* 玫红: DOWN / 告警 / 负向 delta */
  --neon-amber:    #ffd166;          /* 琥珀: WARN / 黄区 / 中性提示 */
  --neon-blue:     #3B82F6;          /* 钴蓝: 信息 / 第二参考线 */
}
```

**ECharts series 必带 shadowBlur** (灵魂铁律 — 是真"光圈"不是描边):

```js
// line / bar / donut 全部都加
itemStyle: { color: '#8B2BF6', shadowColor: '#8B2BF6', shadowBlur: 14 }
lineStyle: { color: '#8B2BF6', width: 2.6, shadowColor: '#8B2BF6', shadowBlur: 14 }
```

### 4. ⭐ Montserrat 极粗大字 — **第四品牌印记**

主显示字 Montserrat **font-weight 700/900**, 数字用 JetBrains Mono `font-variant-numeric: tabular-nums`. 大字气场:

```css
:root {
  --font-display: 'Montserrat', 'Inter', sans-serif;
  --font-mono:    'JetBrains Mono', monospace;
  --font-body:    'Inter', 'Noto Sans SC', sans-serif;
}
.hero-title {
  font-family: var(--font-display);
  font-weight: 900;                    /* 极粗灵魂 */
  font-size: clamp(3rem, 7vw, 6rem);
  letter-spacing: -0.03em;
  text-transform: uppercase;           /* hero 大字必 UPPERCASE (英文) */
  color: #fff;
  text-shadow: 0 0 40px rgba(139, 43, 246, 0.40);
}
.kpi-value, .big-number {
  font-family: var(--font-mono);
  font-weight: 700;
  font-variant-numeric: tabular-nums;  /* 等宽数字, 对齐严格 */
  letter-spacing: -0.02em;
  color: #fff;
}
```

---

## ❌ 必避 (做了立刻失去 Aurora Noir 味)

- ❌ **没有 CSS 极光背景** (这是最大招牌, `.an-aurora-bg` + 三层叠加是物理必带)
- ❌ **把极光做成首屏 hero** (它是 z-index:0 背景层, 上面必须叠 Hero / KPI / 段落; 只看到背景没内容 = 漏了 `.an-stage { position: relative; z-index: 1 }`)
- ❌ 用纯黑 `#000` (灵魂是 `#030406`, 略带蓝)
- ❌ 用 sharp 圆角 (卡 ≥ 8px / panel ≥ 12px / 按钮 pill)
- ❌ 漏掉 `backdrop-filter: blur` (玻璃质感灵魂, 没了立刻廉价)
- ❌ 加额外 hue 的 accent (只用主紫 / cyan / 翠青 / 玫红 / 琥珀 / 钴蓝六色, 不许加粉 / 橙红 / 棕这种暖色)
- ❌ ECharts series 不加 shadowBlur (是光圈不是描边, 漏了立刻退化成"普通深色主题")
- ❌ **dashboard 加 hero 大字 / 主 CTA 按钮 / nav tabs / 用户头像** (那是落地页, 不是工作台)
- ❌ **dashboard KPI 卡上加 active 描边 / inset 内辉 / 右上角彩色状态点** (mockup 装饰, 真 dashboard 不需要; 卡片要纯净 — label / 大数字 / delta / sparkline 就够)
- ❌ **dashboard KPI 不是严格 4 张** (Linear / Stripe / Bybit / Vercel 都是 4, 顶级标准 — 数字是重点, 卡片密度不是)
- ❌ 加 WebGL / 粒子 / 协作光标 / 鼠标视差 (落地页演示道具, 不是 dashboard / editorial 灵魂)
- ❌ **HTML 文案 / 最终回复文本里用 emoji 跟装饰 unicode** (📊 💡 ✓ ★ ✨ ❗ ...). aurora-noir 是科技产品级气质, emoji 立刻降格成"PPT 风"

---

## ECharts 配色 (顶层 spread)

```js
const anEchartsBase = {
  color: ['#8B2BF6', '#06B6D4', '#4ADE80', '#EF4444', '#ffd166', '#3B82F6'],  // 6 色 series
  textStyle: { color: '#fff', fontFamily: "'Inter', sans-serif" },
  backgroundColor: 'transparent',
  grid: { left: '8%', right: '5%', top: '14%', bottom: '12%', containLabel: true },
  tooltip: {
    trigger: 'axis',
    backgroundColor: 'rgba(10, 12, 16, 0.95)',
    borderColor: '#8B2BF6', borderWidth: 1,
    padding: [10, 14],
    textStyle: { color: '#fff', fontSize: 12, fontFamily: "'JetBrains Mono', monospace" },
    extraCssText: 'box-shadow: 0 8px 32px rgba(139,43,246,0.40); border-radius: 8px; backdrop-filter: blur(16px);',
    axisPointer: { type: 'line', lineStyle: { color: '#8B2BF6', type: 'dashed', width: 0.8, opacity: 0.65 } }
  },
  legend: {
    top: 4, right: 8,
    textStyle: { color: '#8E9BAE', fontSize: 11, fontFamily: "'JetBrains Mono', monospace" },
    icon: 'circle', itemWidth: 8, itemHeight: 8, itemGap: 18
  },
  xAxis: {
    type: 'category',
    axisLine: { lineStyle: { color: 'rgba(255,255,255,0.10)' } },
    axisTick: { show: false },
    axisLabel: { color: '#8E9BAE', fontSize: 10, fontFamily: 'JetBrains Mono', margin: 10 },
    splitLine: { show: false }
  },
  yAxis: {
    type: 'value',
    axisLine: { show: false }, axisTick: { show: false },
    axisLabel: { color: '#8E9BAE', fontSize: 10, fontFamily: 'JetBrains Mono' },
    splitLine: { lineStyle: { color: 'rgba(255,255,255,0.04)', type: 'dashed' } }
  }
};
```

**series 必带 shadowBlur** (light is light, not stroke):
- `bar`: `itemStyle: { color, shadowColor: color, shadowBlur: 12 }`
- `line`: `lineStyle: { color, width: 2.6, shadowColor: color, shadowBlur: 14 }`
- `donut`: `itemStyle: { borderColor: '#030406', borderWidth: 3, shadowColor: color, shadowBlur: 16 }`
- `area`: cyan→purple 跨色相 linearGradient (灵魂)

---

## 适用业务

- **editorial 首选**: Web3 项目年报 / 加密市场分析 / 科技产品 keynote / SaaS 产品复盘 / 创业公司年度报告 / 设计工具 (Cursor 类) 产品故事
- **dashboard 首选**: 加密交易看板 / 实时监控驾驶舱 / SaaS 产品 dashboard / 开发者工具数据台 / 系统健康度仪表盘
- **不适**: 严肃财报 (用 blue-consulting) / 时装杂志 (用 rose-press) / 鲜艳营销 (用 graphic-press)

---

## 关键提示

看完 `editorial-example.html` 跟 `dashboard-example.html` 就知道这套理念的呈现方式. **不要从 0 写 CSS**, 直接抄 example 的 `<style>` 段, 改业务即可.

⚠ **抄的时候连 `.an-aurora-bg` + 配套 `<div class="an-aurora-bg"></div>` host + `.an-stage { position: relative; z-index: 1 }` 三件套一起抄**, 千万别漏 — 那是 aurora-noir 的灵魂动效.

⚠⚠ **再次强调**: 极光是**背景层** (z-index: 0). 你写完打开浏览器, **第一眼必须看到正常的 Hero / KPI / 段落**, 背景里若隐若现极光在弥漫. 如果看到只有一片极光占满屏幕 — 说明你**漏了 `.an-stage / .dash` 的 `position: relative; z-index: 1`**, 或者**没把 `<div class="an-aurora-bg">` 放在主容器之前**.
