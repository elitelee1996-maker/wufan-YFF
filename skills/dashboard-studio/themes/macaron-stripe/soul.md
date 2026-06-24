# Macaron Stripe · 马卡龙条纹

> 马卡龙糖果色 × 斜条纹/圆点纹理质感 × 超大软圆角 × 黑卡反差
> — **柔软甜美但有设计感的现代金融/产品 UI**. 像把马卡龙摆在印着斜纹的奶油蛋糕上.

---

## 一句话理念

**浅灰绿底 + 薄荷绿/薰衣草紫马卡龙色块 + 斜条纹/圆点纹理质感 + 超大软圆角 + 一张近黑卡做反差 = 柔软甜美的高级设计感**.

跟 graphic-press / blue-consulting / rose-press / aurora-noir / luminous-paper 的哲学**都不一样** — 这是**第六条路: 马卡龙糖果的柔软 + 工业斜纹的质感, 软与硬撞出的设计张力**.

---

## 跟其他 5 套的六角对比 (6 套主题完全分立)

| 维度 | Graphic Press | Blue Consulting | Rose Press | Aurora Noir | Luminous Paper | **Macaron Stripe** |
|---|---|---|---|---|---|---|
| 哲学 | 鲜艳报刊艺术 | 咨询学术克制 | 杂志高级时装 | 暗夜霓虹电影 | 清爽 SaaS 工作台 | **马卡龙糖果 + 条纹质感** |
| 明暗 | 暖亮 | 暗 | 暖亮 | 暗 | 冷亮 | **柔亮 (浅灰绿)** |
| 底色 | 米黄 + 暗线 | 深蓝 #0A1128 | 浅粉 mesh | 近黑 + 极光 | 近白 + dot-grid | **浅灰绿 #E4EAE4** |
| 主色 | 5 套渐变胶囊 | 唯一钢蓝 | 唯一玫红 | 主紫 + cyan | 蓝 + 4 贴纸色 | **薄荷绿 #A8E6A0 + 薰衣草紫 #B0A4F5 (双主色)** |
| 字体 | Space Grotesk | Cormorant 衬线 | Cormorant italic | Montserrat 极粗 | Inter/思源黑 500-600 | **Poppins/Inter 700-800 极粗大数字** |
| 圆角 | 999px pill | 4-6px 极小 | 28/40/64 杂志 | 8/12px | 12px Notion | **24-40px 超大软圆角 + 圆形 icon** |
| 纹理灵魂 | 45° 暗线 | 极薄 hairline | polaroid | CSS 极光 | dot-grid | **斜条纹 + 圆点纹理 (灵魂招牌, 填进色块/柱/进度条)** |
| 反差手法 | 渐变胶囊 | dropcap | em 玫红 | 玻璃震慑卡 | 无阴影卡 | **近黑卡 vs 马卡龙色块 强反差 (灵魂)** |
| 适合业务 | 创意 / 营销 | 咨询 / 投研 | 时装 / 杂志 | Web3 / 科技炫酷 | SaaS / 协作 | **加密 / 金融 / 消费产品 / 年轻品牌 / 生活方式 App** |

**记忆锚点**: 6 套里只有 macaron-stripe 有"**斜条纹纹理质感**". 想做马卡龙糖果色 + 那种条纹剖面感的柔软设计, 就是它.

---

## 跨 archetype 通用 (视觉灵魂跨形态不变)

macaron-stripe **同时支持 dashboard 跟 editorial**:

| | dashboard 形态 | editorial 形态 |
|---|---|---|
| 用什么 | 软圆角 header + **KPI 阵 (含 1 张近黑反差卡)** + 圆形 icon + 周期 pill + 条纹柱 panel + 明细表 | 大数字 Hero + 马卡龙色块章节 + 斜条纹装饰 + 黑卡反差节 + 圆点时间线 |
| 看哪个 example | `dashboard-example.html` | `editorial-example.html` |
| 看哪个 playbook | `references/dashboard-playbook.md` | `references/editorial-playbook.md` |

---

## ⭐ 视觉灵魂 (4 个不可丢的招牌, 一个少了就不是 macaron-stripe)

### 1. ⭐ 马卡龙双主色 + 浅灰绿底 + 黑卡反差 — **第一品牌印记**

```css
:root {
  --bg-page:    #E4EAE4;   /* 浅灰绿底 (不是纯白, 带一点灰绿, 柔) */
  --bg-card:    #FFFFFF;   /* 白卡 */
  --bg-black:   #1C1C1E;   /* ⭐ 近黑反差卡 (灵魂, 至少 1 张) */
  --mint:       #A8E6A0;   /* 薄荷绿 (主色之一) */
  --mint-deep:  #7DD87A;
  --lavender:   #B0A4F5;   /* 薰衣草紫 (主色之二) */
  --lavender-deep:#9B8AF0;
  --ink:        #1C1C1E;   /* 文字 */
  --ink-soft:   #5A5A5E;
  --ink-on-color:#1C1C1E;  /* 马卡龙色块上的深色字 (色块亮, 用深字) */
}
body { background: var(--bg-page); }
```

**铁律**: 马卡龙色块**亮**, 上面放**深色字** (#1C1C1E); 近黑卡上放**浅色字** (#fff). 两种主色 (薄荷绿 + 薰衣草紫) 交替用, 不要只用一种.

### 2. ⭐⭐ 斜条纹 + 圆点纹理质感 — **第二品牌印记 (最大灵魂)**

这是整套主题最独特的视觉指纹. 在色块的**一部分**填斜条纹 / 圆点, 表达"部分 / 进度 / 质感". 纯 CSS:

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
/* 典型用法: 一个色块上半部分实心, 下半部分条纹 (表示"已达成 vs 目标") */
.bar-block { background: var(--mint); border-radius: 16px; position: relative; overflow: hidden; }
.bar-block .hatched { position: absolute; inset: 0 0 60% 0; background-image: repeating-linear-gradient(-45deg, rgba(28,28,30,0.16) 0 2px, transparent 2px 7px); }
```

**ECharts 里用 `decal` 做斜纹柱** (灵魂技法, 完美复刻参考图的"条纹柱"):

```js
series: [{
  type: 'bar', data,
  itemStyle: {
    color: '#A8E6A0', borderRadius: [12, 12, 0, 0],
    decal: { symbol: 'rect', dashArrayX: [1, 0], dashArrayY: [3, 6], rotation: -Math.PI/4, color: 'rgba(28,28,30,0.18)' }
  }
}]
```

### 3. ⭐ 超大软圆角 + 圆形 icon button — **第三品牌印记**

```css
:root { --r-card: 32px; --r-block: 20px; --r-pill: 999px; }
.card  { border-radius: var(--r-card); }        /* 卡片 24-40px 超大软圆角 */
.block { border-radius: var(--r-block); }        /* 色块 16-24px */
.icon-btn {                                       /* 圆形 icon button (灵魂) */
  width: 40px; height: 40px; border-radius: 50%;
  background: #fff; border: 1px solid rgba(28,28,30,0.08);
  display: inline-flex; align-items: center; justify-content: center;
}
```

### 4. ⭐ Poppins/Inter 极粗大数字 — **第四品牌印记**

```css
:root {
  --font-display: 'Poppins', 'Inter', sans-serif;   /* 几何无衬线, 圆润 */
  --font-body:    'Inter', 'Noto Sans SC', sans-serif;
}
.big-number, .kpi-value {
  font-family: var(--font-display);
  font-weight: 700;                  /* 极粗, 大数字是主角 */
  font-size: clamp(2.2rem, 4vw, 3.4rem);
  letter-spacing: -0.03em; line-height: 1;
  font-variant-numeric: tabular-nums;
}
.hero-title { font-family: var(--font-display); font-weight: 800; }
```

---

## ❌ 必避 (做了立刻失去 Macaron Stripe 味)

- ❌ **没有斜条纹 / 圆点纹理** (这是最大灵魂招牌, 必须出现在色块装饰 / 进度条 / chart decal 里)
- ❌ **没有近黑反差卡** (灵魂是马卡龙亮色块 + 1 张近黑卡的强反差, 全亮就平了)
- ❌ 用纯白底 (灵魂是浅灰绿 #E4EAE4, 带一点灰绿才柔)
- ❌ 用 sharp 小圆角 (必须 24-40px 超大软圆角 + 圆形 icon)
- ❌ 马卡龙色块上放浅色字 (色块亮, 必须放深色 #1C1C1E 字)
- ❌ 高饱和刺眼色 (马卡龙是**低饱和柔色**, 薄荷绿不是荧光绿, 薰衣草紫不是品红)
- ❌ 只用一种主色 (薄荷绿 + 薰衣草紫双主色必须交替, 不要满屏绿)
- ❌ 用衬线字体 (必须 Poppins/Inter 几何无衬线圆润)
- ❌ 加阴影撑卡 / webgl / 粒子 (柔软靠圆角 + 色块, 不靠特效)
- ❌ **HTML 文案 / 最终回复文本里用 emoji 跟装饰 unicode** (📊 💡 ✓ ★ ✨ ❗ ...). 用条纹/圆点/圆形 icon 这些原生视觉元素代替

---

## ECharts 配色 (顶层 spread)

```js
const msEchartsBase = {
  color: ['#A8E6A0', '#B0A4F5', '#1C1C1E', '#7DD87A', '#9B8AF0', '#F5C99B'],  // 薄荷/薰衣草/黑/深薄荷/深紫/马卡龙橙
  textStyle: { color: '#1C1C1E', fontFamily: "'Poppins', 'Inter', 'Noto Sans SC', sans-serif" },
  backgroundColor: 'transparent',
  grid: { left: '6%', right: '4%', top: '14%', bottom: '12%', containLabel: true },
  tooltip: {
    trigger: 'axis',
    backgroundColor: 'rgba(28,28,30,0.92)',
    borderColor: 'rgba(255,255,255,0.1)', borderWidth: 1, padding: [10, 14],
    textStyle: { color: '#fff', fontSize: 12, fontFamily: "'Inter', sans-serif" },
    extraCssText: 'border-radius: 14px; box-shadow: 0 8px 24px rgba(28,28,30,0.2);',
    axisPointer: { type: 'line', lineStyle: { color: '#1C1C1E', type: 'dashed', width: 1, opacity: 0.4 } }
  },
  legend: { top: 4, right: 8, textStyle: { color: '#5A5A5E', fontSize: 12 }, icon: 'circle', itemWidth: 8, itemHeight: 8, itemGap: 18 },
  xAxis: {
    type: 'category',
    axisLine: { lineStyle: { color: 'rgba(28,28,30,0.12)' } }, axisTick: { show: false },
    axisLabel: { color: '#5A5A5E', fontSize: 11, margin: 10 },
    splitLine: { show: false }
  },
  yAxis: {
    type: 'value',
    axisLine: { show: false }, axisTick: { show: false },
    axisLabel: { color: '#5A5A5E', fontSize: 11 },
    splitLine: { lineStyle: { color: 'rgba(28,28,30,0.07)', type: 'dashed' } }
  }
};
```

**灵魂技法 — 至少一个 chart 用 `decal` 斜纹填充** (复刻参考图的条纹柱):
- `bar`: `itemStyle: { color: '#A8E6A0', borderRadius: [12,12,0,0], decal: { symbol:'rect', dashArrayX:[1,0], dashArrayY:[3,6], rotation:-Math.PI/4, color:'rgba(28,28,30,0.18)' } }`
- `line`: 圆润粗线 (width 3) + 圆点 symbol (symbolSize 8) + 浅色 area 渐变
- `donut`: 薄荷/薰衣草交替 + 白色描边 4px + 内圆角 6
- `pie/scatter/radar/treemap/heatmap` 用马卡龙色, 圆角软, 不要硬边

---

## 适用业务

- **dashboard 首选**: 加密钱包 / 金融理财 App / 消费数据看板 / 年轻品牌运营台 / 生活方式产品 / 健康记录
- **editorial 首选**: 消费趋势报告 / 年轻品牌年报 / 生活方式数据故事 / 加密市场柔性解读
- **不适**: 严肃财报 (用 blue-consulting) / 暗夜炫酷 (用 aurora-noir) / 严肃工程台 (用 luminous-paper)

---

## 关键提示

看完 `editorial-example.html` 跟 `dashboard-example.html` 就知道这套理念的呈现方式. **不要从 0 写 CSS**, 直接抄 example 的 `<style>` 段, 改业务即可.

⚠ macaron-stripe 的灵魂 = **柔 (马卡龙色 + 超大圆角) × 硬 (斜条纹/圆点纹理 + 近黑卡反差)** 的张力. 抄的时候**别漏条纹纹理、别漏那张近黑反差卡、别把色块字改成浅色、别用刺眼高饱和** — 任何一个都会破坏这套"软糯但有设计感"的平衡.
