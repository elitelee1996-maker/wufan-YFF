# Graphic Press · 多彩胶囊报刊

> Spotify Wrapped × Apple Newsroom × Penguin Books × Wallpaper* Magazine
> — **Spotify Wrapped 投放到再生纸上的视觉语言**.

---

## 一句话理念

**米黄纸张底 + 5 套渐变胶囊 + 全场 999px pill 圆角 + 几何字体 + 印刷品质感**.

每个数字配一个渐变, 整页读完是**色彩旅程**. Pill 是动词, 不是装饰.

---

## 跨 archetype 通用 (视觉灵魂跨形态不变)

graphic-press **同时支持 dashboard 跟 editorial**, 视觉变量 (色 / 字体 / 圆角 / 纹理) 完全一致:

| | dashboard 形态 | editorial 形态 |
|---|---|---|
| 用什么 | 紧凑 Header + 8 KPI 阵 + 筛选条 + 多 panel + 明细表 + 抽屉 | 大字 Hero + 章节胶囊胸标 + 反常识引语 + Polaroid 卡 |
| 看哪个 example | `dashboard-example.html` | `editorial-example.html` |
| 看哪个 playbook | `references/dashboard-playbook.md` | `references/editorial-playbook.md` |

**两种形态共用同一份 soul.md** (这份文件), 主题灵魂不变. **章节胸标在 editorial 用, KPI 顶条在 dashboard 用 — 都是 5 套渐变 + 999px pill**.

---

## 适用业务

- **editorial 首选**: 深度报告 / 长卷叙事 / 年度回顾 / 产品 Wrapped / Spotlight
- **dashboard 首选**: 创意 / 营销 / 内容运营 / 房产 / 消费品 的鲜艳气质看板
- **不适**: 严肃学术报告 (后续考虑出 mono-paper) / 暗夜监控 (后续考虑出 amber-terminal)

---

## 视觉灵魂 (5 个不可丢的招牌)

### 1. 米黄纸底 + 45° 暗线纹理 = "印刷品不是网页"

```css
body {
  background: #e9e7e2;
}
body::before {
  content: ''; position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background-image: repeating-linear-gradient(
    45deg,
    rgba(0,0,0,0.025) 0 1px,
    transparent 1px 6px
  );
  opacity: 0.6;
}
```

### 2. 5 套 135° 双色渐变 = 叙事色谱

```css
:root {
  --grad-fire:  linear-gradient(135deg, #ff2a2a 0%, #ff8c00 100%);  /* 增长/突破/爆款 */
  --grad-ocean: linear-gradient(135deg, #00b359 0%, #0055ff 100%);  /* 稳健/留存/信任 */
  --grad-berry: linear-gradient(135deg, #a322ff 0%, #ff4d88 100%);  /* 创新/年轻/活跃 */
  --grad-sun:   linear-gradient(135deg, #ffb300 0%, #ff5500 100%);  /* 高亮/获奖/里程碑 */
  --grad-smoke: linear-gradient(135deg, #2a2a2a 0%, #8c8c8c 100%);  /* 总量/基础/对照/风险 */
}
```

**每个数字配一种颜色**, 5 套循环用. 不要随机配色, 让色彩成为叙事弧本身.

### 3. 全场 999px Pill 圆角 (按钮 / 标签 / KPI 条 / 章节胸标)

```css
.pill { border-radius: 999px; }
```

KPI 卡 24px 圆角, 章节胸标用 999px, **全场 pill 是动词**.

### 4. Space Grotesk 几何字体 + 思源黑/宋体

```css
:root {
  --font-display: 'Space Grotesk', sans-serif;  /* 数字 / hero 标题 / 几何感 */
  --font-body: 'Inter', 'Noto Sans SC', sans-serif;  /* 正文 / 描述 */
  --font-serif: 'Noto Serif SC', serif;  /* 章节大字 (杂志感) */
}
```

数字用 Space Grotesk 700, 字间距 -0.03em. Hero 大字可用衬线 (Noto Serif SC) 增强杂志感.

### 5. 章节胶囊胸标 = graphic-press 标志性视觉锚

```html
<div class="section-badge pill-fire">
  <span class="badge-num">01</span>
  <span class="badge-cn">章节理念 · 关键词</span>
</div>
```

```css
.section-badge {
  display: inline-flex; align-items: center; gap: 14px;
  padding: 10px 28px; border-radius: 999px;
  font-family: var(--font-display); font-weight: 600;
  font-size: 13px; color: #fff;
  margin-bottom: 28px;
}
.section-badge.pill-fire  { background: var(--grad-fire);  }
.section-badge.pill-ocean { background: var(--grad-ocean); }
.section-badge.pill-berry { background: var(--grad-berry); }
.section-badge.pill-sun   { background: var(--grad-sun);   }
.section-badge.pill-smoke { background: var(--grad-smoke); }
.badge-num {
  font-size: 14px; opacity: 0.85;
  padding-right: 12px; border-right: 1px solid rgba(255,255,255,0.4);
}
```

---

## ❌ 必避 (做了立刻没有 graphic-press 味)

- ❌ 白底 (必须米黄 #e9e7e2)
- ❌ 普通方块 KPI (必须圆角 + 渐变胶囊)
- ❌ 暗黑底 (那是 amber-terminal / aurora-noir)
- ❌ 蓝绿默认 ECharts 配色 (必须套 5 套渐变胶囊色)
- ❌ 章节用纯数字编号 ("1." "2.") — 必须胶囊胸标 + 中文理念
- ❌ 一种渐变用通篇 (必须 5 种循环, 形成色彩节奏)
- ❌ 视觉过于"创意感" (它是**印刷期刊**, 不是设计师 portfolio)
- ❌ **HTML 文案 / 最终回复文本里用 emoji 跟装饰 unicode** (📊 💡 ✓ ★ ✨ ❗ ...). graphic-press 是 Spotify Wrapped 印刷品质感, emoji 立刻退化成"PPT 风". 用渐变胶囊胸标 / 衬线大数字 / mono 编号代替. 详见 SKILL.md "🚫 严禁 emoji" 段

---

## ECharts 配色建议 (顶层 spread)

```js
const gpEchartsBase = {
  color: ['#ff5500', '#a322ff', '#0055ff', '#00b359', '#ff4d88', '#ffb300'],
  textStyle: { fontFamily: "'Space Grotesk', 'Noto Sans SC', sans-serif", color: '#1a1918' },
  backgroundColor: 'transparent',
  grid: { left: 50, right: 30, top: 30, bottom: 40, containLabel: true },
  tooltip: {
    backgroundColor: 'rgba(255,255,255,0.95)',
    borderColor: 'rgba(0,0,0,0.08)',
    borderWidth: 0.5,
    textStyle: { color: '#1a1918' }
  },
  xAxis: {
    axisLine: { lineStyle: { color: 'rgba(0,0,0,0.18)', width: 0.5 } },
    axisLabel: { color: '#7a7873', fontSize: 11 },
    splitLine: { show: false }
  },
  yAxis: {
    axisLine: { show: false },
    axisLabel: { color: '#7a7873', fontSize: 11 },
    splitLine: { lineStyle: { color: 'rgba(0,0,0,0.06)', type: 'dashed' } }
  }
};
```

直接拷到你的 HTML, 每个 `chart.setOption({ ...gpEchartsBase, series: [...] })`.

---

## 关键提示

看完 `example.html` 你就知道这套理念长什么样. **不要从 0 写 CSS**, 直接抄 example 的 `<style>` 段, 改业务即可.
