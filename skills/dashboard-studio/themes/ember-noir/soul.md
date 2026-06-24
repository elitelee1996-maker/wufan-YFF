# Ember Noir · 鎏金暗夜

> Vacheron Constantin × Apple Card (钛金属) × Macallan 威士忌 × Aesop × 私人银行黑卡
> — **磨砂暗夜里, 一缕香槟金的克制奢华**. 不是"橙色发光", 是**烫金箔压在哑光黑纸上**的质感.

---

## 一句话理念

**哑光暖黑深底 + 磨砂颗粒质感 + 金属拉丝纹理 + 香槟金 hairline 点睛 + 极克制的一处暖光 + Sora 几何字 = 高端腕表 / 私人银行级的沉稳奢华**.

⚠ **核心审美**: 金是**稀缺的点睛**, 不是泛滥的填充. 真正高级的黑金靠**质感 (颗粒 + 拉丝 + 烫金) 跟克制 (大量哑光黑 + 极少金)** 撑起, 而**不是靠满屏发光**. 满屏橙金 + shadowBlur 泛滥 = 廉价炫光, 是要极力避免的反面.

跟现有几套**都不一样** — 这是**暗夜家族的暖调一极**: 和 `aurora-noir` 构成 **noir 双子**, 一个**冷** (极光紫青, 赛博炫酷), 一个**暖** (香槟金质感, 沉稳奢华). 同是近黑底, 一个张扬一个内敛.

---

## ⚠ 跟 aurora-noir 的关键区分 (最容易混, 务必看清)

| | **Ember Noir (暖·质感克制)** | Aurora Noir (冷·炫光张扬) |
|---|---|---|
| 情绪 | **沉稳 / 奢华 / 高端腕表** | 赛博 / 电影 / 科技炫酷 |
| 底色 | **哑光暖黑 #0C0B09 + 磨砂颗粒** | 蓝黑 #030406 + 极光弥漫 |
| 光 | **极克制, 一处暖光焦点 (低调)** | 满场极光 + 三辉光 (张扬) |
| 质感 | **磨砂颗粒 + 金属拉丝 + 烫金 (核心)** | 玻璃透光 (backdrop blur) |
| 主色 | **香槟金 #C9A86A (沉稳, 极小面积点睛)** | 紫 #8B2BF6 + cyan (大面积霓虹) |
| chart 辉光 | **几乎不用 shadowBlur, 最多 1 处极淡** | 每条 series 都强 shadowBlur |
| 字体 | **Sora 几何 (留白多)** | Montserrat 极粗 |
| 关键禁忌 | **绝不满屏发光 / 绝不刺眼橙黄 / 绝不出现紫青** | 绝不出现橙 / 暖色 |

**记忆锚点**: ember-noir = "**哑光黑 + 烫金箔 + 颗粒质感, 金极少而精**"; aurora-noir = "**极光满场 + 霓虹发光, 色彩张扬**". 一个内敛奢华, 一个张扬炫酷.

---

## 跟其他主题的七角定位 (7 套主题完全分立)

| 维度 | Graphic Press | Blue Consulting | Rose Press | Aurora Noir | Luminous Paper | Macaron Stripe | **Ember Noir** |
|---|---|---|---|---|---|---|---|
| 哲学 | 鲜艳报刊 | 咨询克制 | 杂志时装 | 暗夜极光 (冷·炫) | 清爽工作台 | 马卡龙条纹 | **鎏金暗夜 (暖·质感)** |
| 明暗 | 暖亮 | 暗 | 暖亮 | 暗·冷 | 冷亮 | 柔亮 | **暗·暖** |
| 底色 | 米黄 | 深蓝 | 浅粉 | 蓝黑 | 近白 | 浅灰绿 | **哑光暖黑 #0C0B09 + 颗粒** |
| 主色 | 5 渐变胶囊 | 唯一钢蓝 | 唯一玫红 | 紫 + cyan | 蓝 + 贴纸 | 薄荷 + 薰衣草 | **香槟金 #C9A86A (点睛)** |
| 字体 | Space Grotesk | Cormorant 衬线 | Cormorant italic | Montserrat 极粗 | Inter/思源黑 | Poppins 圆润 | **Sora 几何 (留白)** |
| 灵魂招牌 | 渐变胶囊 | 3D 点云球 | polaroid em | 极光 + 玻璃光圈 | dot-grid hairline | 斜条纹 decal | **磨砂颗粒 + 金属拉丝 + 烫金 hairline + 极克制暖光** |
| 适合业务 | 营销 / Wrapped | 咨询 / 投研 | 时装 / 杂志 | Web3 / 炫酷 | SaaS / 协作 | 加密 / 年轻 | **私人银行 / 财富 / 高端腕表 / 奢侈品 / 精品投研** |

---

## 跨 archetype 通用 (视觉灵魂跨形态不变)

ember-noir **同时支持 dashboard 跟 editorial**, 哑光黑 + 颗粒质感 + 香槟金 hairline 跨形态完全一致:

| | dashboard 形态 | editorial 形态 |
|---|---|---|
| 用什么 | 紧凑 Header + **KPI 严格 4 张 (哑光卡 + 金细线, 不发光)** + 全局筛选 + 拉丝 panel + 沉稳 chart + 明细表 | 烫金标题 Hero (留白克制) + dropcap 香槟金 + 章节叙事 + 沉稳 chart + 金 hairline 分隔 |
| 看哪个 example | `dashboard-example.html` | `editorial-example.html` |
| 看哪个 playbook | `references/dashboard-playbook.md` | `references/editorial-playbook.md` |

---

## ⭐ 视觉灵魂 (4 个不可丢的招牌, 一个少了就不是 ember-noir)

### 1. ⭐ 香槟金巧色 + 哑光暖黑 — **第一品牌印记 (色要沉稳, 不要刺眼)**

```css
:root {
  --void:       #0C0B09;            /* 哑光暖黑底 (微暖微棕, 不是纯黑也不是蓝黑) */
  --surface:    #15130E;            /* 卡片面 (深棕黑) */
  --surface-2:  #1C1813;            /* 抬升面 */
  --gold:       #C9A86A;            /* ⭐ 香槟金 (主点睛色 — 沉稳, 不是刺眼橙黄!) */
  --gold-bright:#E6CE9A;            /* 亮金 (仅细线 / 微高光) */
  --gold-deep:  #8A6D3C;            /* 古铜暗金 (阴影侧 / 渐变收尾) */
  --gold-line:  rgba(201,168,106,0.22);  /* 金 hairline 描边 */
  --amber:      #D9883C;            /* 暖橙 (降饱和, 仅 1 处焦点高亮, 极小面积) */
  --ink:        #F2EDE4;            /* 暖白文字 (不是纯白) */
  --ink-soft:   #9C948A;            /* 暖灰 */
  --ink-faint:  #645D54;
}
body { background: var(--void); color: var(--ink); }
```

**铁律**: 金是**点睛**不是填充 — 全屏 90% 是哑光暖黑, 香槟金只出现在 hairline / 关键数字 / 标题烫金 / 1 个 chart 焦点. **绝不大面积铺金黄渐变** (那就是杀马特). 用香槟金 `#C9A86A` 这种沉稳色, 不用刺眼的 `#FFB155`.

### 2. ⭐⭐ 磨砂颗粒 + 金属拉丝纹理 — **第二品牌印记 (去塑料感的关键)**

整套主题最大质感来源. 两层 CSS 纹理, 让哑光黑"有材质"而不死板:

```css
/* (A) 磨砂颗粒 grain — 全局叠一层 SVG 噪点, 去塑料感 (高端网站标配) */
.en-grain::after {
  content:''; position:fixed; inset:0; z-index:2; pointer-events:none;
  opacity:0.05; mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
/* (B) 金属拉丝 brushed — 极细竖向丝纹, 用在 hero / 标题块 / 重点 panel */
.brushed {
  background-image:repeating-linear-gradient(90deg, rgba(230,206,154,0.04) 0 1px, transparent 1px 3px);
}
/* 卡片金属边缘高光 (上缘一缕极细金反光, 像金属切边) */
.card-edge::before {
  content:''; position:absolute; top:0; left:0; right:0; height:1px;
  background:linear-gradient(90deg, transparent, rgba(230,206,154,0.4), transparent);
}
```

⚠ grain 是**质感命脉** — 没有它, 哑光黑就是死的塑料黑. 抄 example 时务必连 grain 层一起抄.

### 3. ⭐ 光收敛 + 极克制暖光 — **第三品牌印记 (反"杀马特"铁律)**

**整页最多一处暖光焦点**, 且低调弥漫, 不是满屏 glow:

```css
/* 背景层: 哑光黑 + 角落极淡金雾 (几乎不可见地弥漫, 不是一道亮光斜插) */
.en-ambient-bg {
  position:fixed; inset:0; z-index:0; pointer-events:none;
  background-color:#0C0B09;
  background-image:
    radial-gradient(ellipse 1100px 800px at 80% -5%, rgba(201,168,106,0.10), transparent 55%),
    radial-gradient(ellipse 900px 700px at 5% 105%, rgba(138,109,60,0.07), transparent 55%);
}
/* vignette 让四周更沉, 内容浮起 (沉稳感) */
.en-ambient-bg::after {
  content:''; position:absolute; inset:0;
  background:radial-gradient(ellipse at center, transparent 45%, rgba(8,7,6,0.6) 100%);
}
```

**ECharts 几乎不用 shadowBlur** (这是跟 aurora 最大区别): 最多 1 个核心 chart 的焦点系列加**极淡** (`shadowBlur:8`, 金色) 提一下, 其余全部干净沉稳, 靠**香槟金多明度梯度**做层次, 不靠光晕.

### 4. ⭐ 烫金标题 + 金 hairline 精致细节 — **第四品牌印记**

金的高级用法是**细线 + 烫金箔字**, 不是大色块:

```css
:root { --font-display:'Sora','Inter',sans-serif; --font-body:'Inter','Noto Sans SC',sans-serif; }
/* 烫金箔标题 (香槟金竖向渐变 + 极细, 像压印的金箔, 克制用 1-2 处) */
.text-foil {
  background:linear-gradient(180deg, #E6CE9A 0%, #C9A86A 50%, #8A6D3C 100%);
  -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
}
/* 金 hairline 分隔线 (精致细节, 替代粗边框) */
.gold-rule { height:1px; background:linear-gradient(90deg, transparent, var(--gold-line) 20%, var(--gold-line) 80%, transparent); }
/* 数字: 暖白为主, 关键数字才用烫金, 等宽对齐 */
.kpi-value { font-family:var(--font-display); font-weight:600; font-variant-numeric:tabular-nums; letter-spacing:-0.02em; color:var(--ink); }
```

---

## ❌ 必避 (做了立刻变回"杀马特炫光")

- ❌ **满屏橙金渐变 / 大面积铺金** (这是头号反面; 金只占全屏 < 10%, 90% 是哑光暖黑)
- ❌ **shadowBlur 泛滥** (每个 chart / 卡都发光 = 廉价炫光; 最多 1 处极淡焦点光)
- ❌ **大面积发光卡 / 渐变高亮卡** (土豪味; KPI 卡是哑光黑 + 金细线描边, 不发光)
- ❌ **刺眼金黄 `#FFB155` / `#FFD089`** (杀马特; 用沉稳香槟金 `#C9A86A` / 古铜 `#8A6D3C`)
- ❌ **没有 grain 颗粒层** (哑光黑会变成死塑料黑, 质感全失 — grain 是命脉)
- ❌ **没有金属拉丝 / 烫金 / hairline 等质感细节** (只剩纯色块就是平庸)
- ❌ 出现紫 / cyan / 绿霓虹 (那是 aurora-noir; ember 是暖色系, 香槟金 + 极小暖橙)
- ❌ 用纯黑 `#000` / 蓝黑 (灵魂是 `#0C0B09` 哑光暖黑微棕)
- ❌ 用冷灰文字 / 纯白 (用暖白 `#F2EDE4` + 暖灰 `#9C948A`)
- ❌ 把光带做成首屏 hero (它是 z-index:0 极淡背景, 上面叠 `.en-stage { position:relative; z-index:1 }`)
- ❌ **dashboard 加 hero 大字 / 主 CTA / nav tabs / 头像**; KPI 严格 4 张
- ❌ 加 WebGL / 粒子 / 视差 (奢华靠质感 + 克制, 不靠特效)
- ❌ **HTML 文案 / 回复文本里用 emoji 跟装饰 unicode** (📊 ★ ✨ ...). 奢华金融气质, emoji 立刻降格

---

## ECharts 配色 (顶层 spread — 香槟金多明度梯度, 沉稳不炫光)

```js
const enEchartsBase = {
  color: ['#C9A86A', '#8A6D3C', '#E6CE9A', '#A98B52', '#6F5933', '#D9883C'],  // 香槟金多明度梯度 (末位暖橙仅作焦点)
  textStyle: { color:'#F2EDE4', fontFamily:"'Sora','Inter',sans-serif" },
  backgroundColor: 'transparent',
  grid: { left:'6%', right:'5%', top:'16%', bottom:'12%', containLabel:true },
  tooltip: {
    trigger:'axis',
    backgroundColor:'rgba(12,11,9,0.95)',
    borderColor:'rgba(201,168,106,0.35)', borderWidth:1, padding:[10,14],
    textStyle:{ color:'#F2EDE4', fontSize:12, fontFamily:"'Inter',sans-serif" },
    extraCssText:'box-shadow:0 10px 30px rgba(0,0,0,0.5); border-radius:10px;',  // 阴影是黑的不是金的, 沉稳
    axisPointer:{ type:'line', lineStyle:{ color:'#C9A86A', type:'dashed', width:0.8, opacity:0.5 } }
  },
  legend: { top:4, right:8, textStyle:{ color:'#9C948A', fontSize:11 }, icon:'circle', itemWidth:7, itemHeight:7, itemGap:18 },
  xAxis: {
    type:'category',
    axisLine:{ lineStyle:{ color:'rgba(201,168,106,0.18)' } }, axisTick:{ show:false },
    axisLabel:{ color:'#9C948A', fontSize:10, margin:10 }, splitLine:{ show:false }
  },
  yAxis: {
    type:'value',
    axisLine:{ show:false }, axisTick:{ show:false },
    axisLabel:{ color:'#9C948A', fontSize:10 },
    splitLine:{ lineStyle:{ color:'rgba(201,168,106,0.07)', type:'dashed' } }
  }
};
```

**沉稳铁律** (不靠光晕靠质感):
- `bar`: 香槟金竖向 linearGradient (`#E6CE9A → #8A6D3C`) + 细顶圆角. **不加 shadowBlur**. 想强调某根 → 用更亮的金 (#E6CE9A) 而非发光
- `line`: `lineStyle:{ color:'#C9A86A', width:2 }` + 极淡金 area 渐变 (`rgba(201,168,106,0.14) → 0`). 至多焦点线 `shadowBlur:8`
- `donut`: 香槟金多明度各段 + `borderColor:'#0C0B09', borderWidth:3` (黑描边切割, 干净). 不发光
- `heatmap`: 哑光黑 → 古铜 → 香槟金梯度 (`#15130E → #8A6D3C → #C9A86A → #E6CE9A`)
- `scatter/radar/treemap`: 香槟金多明度, 焦点项用亮金, 其余古铜/暗金, 靠明度拉层次

---

## 适用业务

- **dashboard 首选**: 私人银行 / 财富管理 / 家族办公室 / 高端腕表零售台 / 精品投研台 / 黑卡会员系统
- **editorial 首选**: 财富年度报告 / 私募复盘 / 高端品牌年报 / 奢侈品市场解读 / 腕表 / 威士忌行业研究
- **不适**: 冷感科技炫酷 (用 aurora-noir) / 严肃学术财报 (用 blue-consulting) / 清爽工程台 (用 luminous-paper)

---

## 关键提示

看完 `editorial-example.html` 跟 `dashboard-example.html` 就知道这套理念的呈现方式. **不要从 0 写 CSS**, 直接抄 example 的 `<style>` 段, 改业务即可.

⚠ **三件套必抄**: `.en-ambient-bg` (极淡金雾背景) + `.en-grain` (磨砂颗粒, 质感命脉) + `.en-stage { position:relative; z-index:1 }`. 缺 grain 质感全失, 缺 z-index 背景会盖住内容.

⚠⚠ **反"杀马特"自检** (做完打开浏览器, 逐条对照):
1. 第一眼是**沉稳的哑光黑**, 金只在标题 / 细线 / 1 个焦点上若隐若现? (是 → 对; 满眼金光 → 错, 金铺太多了)
2. 大色块上能看到**细腻磨砂颗粒**而不是死平的塑料色? (看不到 → 你漏了 grain 层)
3. chart 是**沉稳的香槟金梯度**, 而不是每条都在发光? (都发光 → 删掉多余 shadowBlur)
4. 金色是**沉稳的香槟金/古铜**, 而不是刺眼的亮黄橙? (刺眼 → 换 #C9A86A)

⚠⚠⚠ **别串到 aurora**: 全程只用香槟金 + 极小暖橙. 一旦出现 `#8B2BF6` / `#06B6D4` / 紫青, 就破坏了 ember-noir 的暖调灵魂.
