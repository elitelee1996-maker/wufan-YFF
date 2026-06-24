# Rose Press · 玫红报刊

> Vogue × Apple Newsroom × Bloomberg Businessweek × The Gentlewoman × The Drift × MagCulture
> — **顶级时装杂志风**. 浅粉雾染底 + 玫红 italic em 灵魂字 + 黑白骨架 + polaroid 拍立得物感.

---

## 一句话理念

**浅粉雾染 mesh 底 + 唯一玫红 #E13B7A + Cormorant italic em 自动重音 + 黑白骨架 + 拍立得旋转卡 = 高级时装杂志感**.

跟 graphic-press (鲜艳 Wrapped 张扬) / blue-consulting (深蓝学术克制) 的哲学**都不一样** — 这是**第三条路: 杂志主编的克制与挑衅, 像一本你舍不得撕掉封面的 Vogue / The Gentlewoman**.

---

## 跟 graphic-press / blue-consulting 三角对比

| 维度 | Graphic Press | Blue Consulting | **Rose Press** |
|---|---|---|---|
| 哲学 | 鲜艳报刊艺术 (Spotify Wrapped 张扬) | 咨询学术克制 (Bloomberg Terminal) | **杂志高级时装 (Vogue / Apple Newsroom)** |
| 底色 | 米黄 #e9e7e2 + 45° 暗线纹理 | 深蓝 #0A1128 | **浅粉雾染 mesh #F2EBDD + 4 层 radial gradient** |
| 主色 | 5 套渐变胶囊轮流 | 唯一钢蓝 #3A6EA5 | **唯一玫红 #E13B7A** |
| 字体 | Space Grotesk 几何无衬线 | Cormorant 衬线 + Noto Serif SC | **Cormorant Garamond italic + Noto Serif SC** |
| 灵魂招牌字 | 5 套渐变胶囊胸标 | dropcap 引言首字 | **`<em>` 自动玫红 italic 关键判断词** |
| 圆角 | 999px 全场 pill | 4-6px 极小 | **28 / 40 / 64px 杂志阶梯** |
| 灵魂动效 | 无 | 3D 点云球 (WebGL) | **无 (杂志反 WebGL, 拒绝技术炫耀)** |
| 物感 | 印刷胶囊 | 学术 hairline | **拍立得旋转卡 ±1.5° + 浅粉雾染** |
| 适合业务 | 创意 / 营销 / Wrapped / 年报 | 咨询 / 学术 / 战略 / 投研 | **时装 / 品牌 / 编辑部 / 生活方式 / 文化报道 / Vogue 感年度刊** |

---

## 跨 archetype 通用 (视觉灵魂跨形态不变)

rose-press **同时支持 dashboard 跟 editorial**, 但 polaroid 旋转卡是 **editorial 独家** (dashboard 用会跟工作台违和):

| | dashboard 形态 | editorial 形态 |
|---|---|---|
| 用什么 | 杂志 masthead + 6 KPI **严格混搭** (1 黑+1 玫红+4 白) + 周期 tab + panel + 明细表 | 杂志 masthead + 大字 italic Hero + dropcap lead + polaroid 旋转 + pull-quote 重音 + mag-cover 大圆角 |
| 看哪个 example | `dashboard-example.html` | `editorial-example.html` |
| 看哪个 playbook | `references/dashboard-playbook.md` | `references/editorial-playbook.md` |

---

## ⭐ 视觉灵魂 (4 个不可丢的招牌, 一个少了就不是 rose-press)

### 1. ⭐ `<em>` 自动玫红 italic — **第一品牌印记**

整套主题最强视觉指纹. Agent 在任何标题 / 段落 / 引言里写 `<em>关键词</em>`, 自动获得 Cormorant 衬线斜体 + 玫红 #E13B7A:

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

**用法铁律**: 关键判断词都用 `<em>` 包住, **不要直接写 `style="color: #E13B7A"`** — 那不是品牌印记, 是滥用色彩.

```html
<h1>一座城市的 <em>分层折叠</em></h1>
<p>南向溢价 <em>199%</em>, 远超装修等级溢价.</p>
```

### 2. ⭐ Polaroid 拍立得旋转卡 `.rp-polaroid` — **editorial 独家**

微旋 ±1.5°, hover 校正归零. 给杂志版面"物感":

```css
.rp-polaroid {
  background: #FFFCF5;
  padding: 16px 16px 32px 16px;
  box-shadow: 0 4px 16px rgba(15,15,15,0.10), 0 1px 2px rgba(15,15,15,0.08);
  transition: transform 400ms cubic-bezier(0.16, 1, 0.3, 1);
  border-radius: 8px;
}
.rp-polaroid:nth-of-type(odd)  { transform: rotate( 1.0deg); }
.rp-polaroid:nth-of-type(even) { transform: rotate(-1.4deg); }
.rp-polaroid:hover             { transform: rotate(0) scale(1.02); z-index: 5; }
```

⚠ **dashboard 严禁用 polaroid** — 工作台带旋转卡违和.

### 3. ⭐ Pull-quote 整页大字 italic 玫红 `.rp-pull-quote` — **章节重音**

杂志感重音, 章节之间打"重击":

```css
.rp-pull-quote {
  padding: clamp(48px, 8vw, 96px) clamp(24px, 5vw, 48px);
  margin: clamp(40px, 6vw, 80px) 0;
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
  font-size: clamp(2rem, 4vw, 4rem);
  font-weight: 500;
  line-height: 1.15;
  text-align: center;
  border-top: 0.5px solid rgba(15,15,15,0.20);
  border-bottom: 0.5px solid rgba(15,15,15,0.20);
}
.rp-pull-quote em {
  font-style: italic; color: #E13B7A;
  background: linear-gradient(180deg, transparent 60%, rgba(225,59,122,0.18) 60%, rgba(225,59,122,0.18) 92%, transparent 92%);
  padding: 0 0.08em;
  box-decoration-break: clone;
}
```

editorial 长报告**至少出现 1-2 处**. dashboard 偶尔可用 (作为大 panel 之间的视觉锚).

### 4. ⭐ Magazine-cover 大圆角刊封卡 `.rp-mag-cover` — **章节封面感**

64px 大圆角 + 80px padding, 章节起始处用, 强烈的"翻到下一页"感:

```css
.rp-mag-cover {
  background: #FFFCF5;
  border-radius: 64px;       /* 全主题最大圆角 */
  padding: clamp(40px, 6vw, 80px);
  box-shadow: 0 0 0 1px rgba(15,15,15,0.06), 0 8px 32px rgba(15,15,15,0.10);
  position: relative; overflow: hidden;
}
```

---

## 调色板 (基础)

```css
:root {
  /* ── 基础底色 ── */
  --bg-page:        #F2EBDD;             /* 米黄基底 */
  --bg-elevated:    #FFFCF5;             /* 白卡 */
  --bg-card:        rgba(255, 252, 245, 0.85);
  --bg-blackcard:   #101010;             /* 黑色重音卡 */

  /* ── 文字 (油墨黑 + 暖灰) ── */
  --text-primary:   #0F0F0F;
  --text-secondary: #5A5246;
  --text-muted:     #8A8275;
  --text-on-black:  #F2EBDD;

  /* ── 灵魂玫红 (唯一主色) ── */
  --accent-magenta: #E13B7A;
  --accent-magenta-soft: #c12d68;
  --accent-magenta-bg: rgba(225, 59, 122, 0.08);
  --accent-magenta-glow: rgba(225, 59, 122, 0.18);
  --accent:         #E13B7A;             /* 别名 */

  /* ── 辅助色 (只入图表, 主区域 KPI 严禁滥用) ── */
  --accent-purple:  #A48CD9;
  --accent-orange:  #E5722A;
  --accent-green:   #3F7E45;
  --accent-blue:    #5B8DEE;

  /* ── 杂志阶梯圆角 ── */
  --radius-sm:   8px;
  --radius-lg:   28px;        /* 普通卡 */
  --radius-xl:   40px;        /* 重音卡 */
  --radius-2xl:  64px;        /* 杂志封面卡 */

  /* ── 字体 ── */
  --font-display:   'Cormorant Garamond', serif;
  --font-body:      'Inter', sans-serif;
  --font-mono:      'JetBrains Mono', monospace;
  --font-cn-hero:   'Noto Serif SC', serif;
  --font-cn-body:   'Noto Sans SC', sans-serif;
}
```

### body 浅粉雾染 mesh 底 (灵魂背景, 跟其他两套主题完全不一样)

```css
body {
  background-color: #F2EBDD;
  background-image:
    radial-gradient(at 20% 30%, rgba(225, 59, 122, 0.14) 0%, transparent 50%),  /* 玫红主导 */
    radial-gradient(at 80% 20%, rgba(164, 140, 217, 0.10) 0%, transparent 50%), /* 紫 */
    radial-gradient(at 40% 80%, rgba(229, 114, 42, 0.08) 0%, transparent 50%),  /* 橙 */
    radial-gradient(at 90% 70%, rgba(63, 126, 69, 0.06) 0%, transparent 50%);   /* 绿 */
  background-attachment: fixed;
}
```

4 层 radial gradient 在米黄底上晕染出**浅粉**视觉效果 (而不是米黄). 这是 rose-press 视觉印象的"第一印象".

---

## ❌ 必避 (做了立刻失去 Rose Press 味)

- ❌ **直接写 `style="color: #E13B7A"` 当玫红字** — 灵魂用法是 `<em>` 包关键词, 不是滥用色彩
- ❌ **dashboard 用 polaroid 旋转卡** (那是 editorial 独家, 工作台旋转违和)
- ❌ **多彩 (紫/橙/绿/蓝) 滥用进 KPI 主区域** — 只入图表, 主区域永远黑/玫红/白三色
- ❌ KPI 6 张**全用普通白卡** (违反 rose-press 张力铁律: 至少 1 黑底 hero + 1 玫红 accent)
- ❌ 用 WebGL / 3D 动效 (rose-press 杂志反技术炫耀, 跟 blue-consulting 完全相反)
- ❌ 用蓝色 / 米黄 / 深蓝主色 (那不是 rose-press 的辨识色)
- ❌ 用 999px 全场 pill 圆角 (那是 graphic-press)
- ❌ 无衬线大字主标 (必须 Cormorant Garamond + Noto Serif SC)
- ❌ 章节标题没 `<em>` 重音 (杂志感丢了)
- ❌ **HTML 文案 / 最终回复文本里用 emoji 跟装饰 unicode** (📊 💡 ✓ ★ ✨ ❗ ...). rose-press 是 Vogue / The Gentlewoman 高级时装杂志感, emoji 立刻降格成"小红书图". 用 `<em>` 玫红 italic / 衬线大数字 / mono 编号代替. 详见 SKILL.md "🚫 严禁 emoji" 段

---

## ECharts 配色 (顶层 spread)

```js
const rpEchartsBase = {
  color: ['#E13B7A', '#A48CD9', '#E5722A', '#3F7E45', '#5B8DEE', '#c12d68'],  // 5 色 series, 玫红主
  textStyle: { fontFamily: "'Inter', 'Noto Sans SC', sans-serif", color: '#0F0F0F' },
  backgroundColor: 'transparent',
  grid: { left: '6%', right: '4%', top: '14%', bottom: '12%', containLabel: true },
  tooltip: {
    trigger: 'axis',
    backgroundColor: 'rgba(255, 252, 245, 0.98)',
    borderColor: 'rgba(15,15,15,0.12)', borderWidth: 1,
    padding: [10, 14],
    textStyle: { color: '#0F0F0F', fontSize: 12 },
    extraCssText: 'box-shadow: 0 8px 32px rgba(15,15,15,0.12); border-radius: 12px;',
    axisPointer: { type: 'line', lineStyle: { color: '#E13B7A', type: 'dashed', width: 1, opacity: 0.45 } }
  },
  legend: { top: 4, right: 8, textStyle: { color: '#8A8275', fontSize: 12 }, icon: 'circle', itemWidth: 8, itemHeight: 8, itemGap: 18 },
  xAxis: {
    type: 'category',
    axisLine:  { lineStyle: { color: 'rgba(15,15,15,0.12)' } },
    axisTick:  { show: false },
    axisLabel: { color: '#8A8275', fontSize: 11, fontFamily: 'JetBrains Mono, monospace', margin: 10 },
    splitLine: { show: false }
  },
  yAxis: {
    type: 'value',
    axisLine: { show: false }, axisTick: { show: false },
    axisLabel: { color: '#8A8275', fontSize: 11, fontFamily: 'JetBrains Mono, monospace' },
    splitLine: { lineStyle: { color: 'rgba(15,15,15,0.08)', type: 'dashed' } }
  }
};
```

**bar 用玫红主 + 圆角顶部 6px** (`borderRadius: [6, 6, 0, 0]`), area 渐变玫红 #E13B7A 0.18 → 0, donut 5 色循环 + 白色描边 4px + 内圆角 4. **绝对不要荧光色 / 深蓝 / 米黄底图表** — 那是别的主题.

---

## 适用业务

- **editorial 首选**: 时装 / 品牌 / 生活方式 / 文化报道 / 编辑部年度刊 / Vogue 感深度报告 / 居住美学 / 餐饮 / 旅行
- **dashboard 首选**: 创意 / 品牌方 / 营销 / 内容运营 / 编辑部数据台 (有"高级感"需求的看板)
- **不适**: 严肃财报 (用 blue-consulting) / Wrapped 营销 (用 graphic-press) / 战术大屏 (后续考虑 amber-terminal)

---

## 关键提示

看完 `editorial-example.html` 跟 `dashboard-example.html` 就知道这套理念的呈现方式. **不要从 0 写 CSS**, 直接抄 example 的 `<style>` 段, 改业务即可.

**特别留意**: rose-press 的灵魂 70% 在文案表达, 30% 在 CSS. **Agent 写文案时必须主动用 `<em>` 包关键判断词**, 让玫红 italic em 在整页频繁出现 — 这才是"杂志感"的源头, 不是把 CSS 抄一遍就能复刻的.
