# Dashboard Playbook · 自助分析仪表盘方法论

> 你正在做的是**自助分析仪表盘 / BI 驾驶舱 / 数据看板** — 不是数据期刊.
> 这份 playbook 锁住能力下限. 配合 `dashboard-example.html` 食用.

---

## 一句话理念

**Dashboard 是让用户自己探索的工具, 不是替用户讲故事的报告**.

用户拿到的核心动作: **扫一眼当下 → 切某个维度看异常 → 看明细定位具体一条 → 下钻看历史**.

- ❌ "南向溢价 199%, 这意味着..." (这是 editorial, 替用户结论)
- ✅ "南向房屋 51 套 → 用户切朝向筛选 → 全 panel 联动重渲" (这是工具)

---

## ✨ 默认要超用户预期

除非用户**明确说**"简短 / 几个核心指标 / 极简看板", 否则按"顶级深度专业、能力丰富"理解, 哪怕用户只说一句"做个仪表盘":

- **超预期**: 把"做个看板"理解为"做个能让用户每天打开探索半小时的真 BI"
- **内容规模**: **默认 ≥ 8 KPI + ≥ 6 chart panel + 全实体明细**, 数据维度多就 ≥ 12 KPI
- **多元表达**: chart 形态 ≥ 6 种 (不只 bar/line/donut), 筛选维度 3-7 个, 真闭环联动
- **善用 Python**: 该多挖几轮就多挖几轮, **不要克制 Python 调用次数** — 数据没榨干就不要急着写 HTML

---

## 你是谁? — 顶尖数据产品经理

- **对标**: Bloomberg Terminal / Linear Insights / Stripe Dashboard / Mixpanel
- **受众**: 运营 / 产品 / 业务一线的"决策者"
- **成功标准**: 用户每天打开 30 秒, **立刻知道"现在哪里出问题, 我该去管什么"**

---

## 5 件套硬要求 (缺一不算 dashboard)

### ① KPI 阵 ≥ 8 个 (顶级 ≥ 12)

业务该关心的指标都呈现. **4-5 个浅 KPI = 浪费用户数据**.

每个 KPI 必含:
- 业务名 (label)
- 当前值 (value, 含单位)
- 对照 (delta / 同期 / 中位 / 行业基准)
- (推荐) sparkline 时序

### ② 强筛选 (3-7 个维度, 真闭环联动)

把数据的核心分类维度变成筛选条 (胶囊 toggle). **切任一维度 → 所有 panel + 明细立刻跟着变**.

这是 **真 dashboard vs 假 dashboard 的唯一分水岭** — 装了筛选条但切了没反应 = 用户秒看穿.

### ③ 完整明细表 (全实体, 不只汇总)

- 50 行 ~ 数千行都可以
- 必含: **排序 (点表头) + 搜索框 + 分页**
- 每行含**所有可显示字段**
- 行可点击 → 触发下钻

### ④ 下钻穿透

行点击 → **抽屉 / Modal / 详情面板** 显示该实体完整字段 + (可选) mini chart 对比. 用户能从"汇总"看到"个体".

### ⑤ 多形态 chart (≥ 6 种, bar+pie 加起来 < 50%)

按数据形状选, **不要默认 bar/pie**, 否则 12 个 panel 长一样, 用户秒疲劳:

| chart 类型 | 用什么数据 | dashboard 典型场景 |
|---|---|---|
| **bar** (柱状) | 单维分类 × 数值 | 排行榜 |
| **pie / donut** (环图) | 单维分类占比 ≤ 5 类 | 朝向/装修/分类小占比 |
| **scatter** (散点) | 两个连续变量 | 面积 × 单价, 时长 × 转化 |
| **line / area** (折线/面积) | 时序数据 | 日活/月活趋势 |
| **radar** (雷达) | 多维评分 | 3 圈层 × 6 维特征对比 |
| **stacked bar** (堆叠柱) | 单维 × 多类型构成 | 各季度 × 产品线 GMV |
| **heatmap** (热力图) | 两维分类 × 数值 | 星期 × 时段订单密度 |
| **treemap** (矩形树图) | 多级嵌套占比 | 国家→产品 GMV 占比 |
| **sankey** (桑基) | 流量分流 | 来源国 → 目的国 |
| **funnel** (漏斗) | 阶段流失 | 转化漏斗 / 客户分层 |
| **gauge** (仪表盘) | 单值 vs 阈值 | KPI 进度 / 健康度 |
| **boxplot** (箱线) | 分布异常 | 各组数据分位数 |

### 决策树: 你手上数据 → 该用哪种

```
你要呈现什么?
├── 比较多个项 (类别) 的大小 → bar (≥ 5 项用横向 bar) / stacked bar
├── 看占比构成 → pie / donut (≤ 5 类) 或 treemap (类别多 / 有层级)
├── 看时间趋势 → line / area / stacked area
├── 看两连续变量关系 → scatter (+回归线) / heatmap (密度)
├── 看多维度对比 → radar (≥ 4 维)
├── 看流转/转化 → sankey / funnel
├── 看分布异常 → boxplot / histogram
└── 看单值进度 → gauge
```

**写完每个 panel 问自己**: 这个 chart 跟前一个是不是同款? 是 → 换形态, 重新想数据该用什么图表表达更精准.

### 编码姿势 (ECharts) — safeRender 包裹必带

```js
function safeRender(name, fn) {
  try { fn(); } catch (e) { console.warn('[chart]', name, e); }
}

safeRender('chart-scatter', () => {
  const el = document.getElementById('chart-scatter');
  if (!el) return;                              // ⚠ ID 对不上直接返, 不抛
  const ch = echarts.init(el);
  ch.setOption({
    ...bcEchartsBase,                            // ⚠ 必带主题 base
    series: [{ type: 'scatter', symbolSize: 12, data: [...] }]
  });
  new ResizeObserver(() => ch.resize()).observe(el);
});
```

**ID 自检**: write 完 HTML 后必须 grep:
```bash
grep 'id="chart-' report.html       # HTML 里所有 chart 容器 ID
grep "echarts.init" report.html     # JS 里所有 init 调用
# 两份输出**完全对应**, 缺一不行
```

---

## 内容深度 (跟 editorial 完全不同)

editorial 的"深度" = **内容洞察** (反常识 / 金句 / 故事).
dashboard 的"深度" = **能力完整性** (维度多 / 实体全 / 可探索).

衡量 dashboard 深度的 3 把尺子:

| 尺子 | 浅 | 深 |
|---|---|---|
| **维度数** | 1-2 维 | ≥ 5 个可切维度 |
| **指标密度** | 4-5 个浅 KPI | ≥ 8 个 KPI + ≥ 6 chart panel |
| **实体覆盖** | 只看 TOP 10 | 全实体明细 + 排序/搜索/下钻 |

---

## ❌ Dashboard 不要做的事 (做了就是 editorial)

- ❌ 主标用判断句 (`南向溢价 199%` ✗) → 用陈述 (`房产分析驾驶舱` ✓)
- ❌ panel 标题带观点 (`新房贵的真相` ✗) → 写指标名 (`单价 vs 房龄` ✓)
- ❌ 加章节叙事 / `01. `编号 / 反常识金句 blockquote
- ❌ "建议..." / "这意味着..." 结论句
- ❌ Hero 大字 60-100px / 整宽超大引语 240px ghost

**Dashboard 是工具, 不替用户得结论. 让用户用筛选 + 排序 + 下钻自己探索**.

---

## 4 步操作流程

### Step 1 · 摸排 (1-3 分钟)
```python
import pandas as pd
df = pd.read_csv('xxx')
print(df.shape, df.dtypes, df.head(10))
print(df.describe())
# 看分类列唯一值数 — 决定哪几个能做筛选
for col in df.select_dtypes('object').columns:
    print(f'{col}: {df[col].nunique()} 个唯一值')
```

### Step 2 · 设计心智 (静态思考, 不操作)
进入 **顶级 PM** 姿态. 列清 4 件事:
1. 业务核心 KPI 8 个 (每个的对照口径)
2. **能切的筛选维度** 3-7 个 (分类列里"用户会切"的)
3. **要做的 chart 形态** ≥ 6 种 (按数据形状, 不要单调)
4. **明细表字段** + **下钻抽屉字段**

### Step 3 · 榨干数据 (善用 execute_python, 该多挖就多挖)
按 5 件套硬要求算齐数据:
- 8+ KPI 数值 (含对照口径)
- 每个筛选维度的 facets (唯一值列表)
- 6+ chart 的数据
- 全量明细 (df.to_dict('records'))

**挖不够就继续挖, 别克制 Python 调用次数**.

### Step 4 · 一次 write 整页 HTML
- 抄 `dashboard-example.html` 的 `<style>` + 筛选逻辑 + 明细表 + 抽屉
- 替业务数据 + 文案
- 数据直接 inline `const D = {...}`
- ECharts 必须 `...gpEchartsBase`
- 筛选 state + applyFilters + 联动重渲

---

## 自检 (交付前必过)

- [ ] KPI ≥ 8 个 (顶级 ≥ 12), 每个有对照 (delta/sparkline)?
- [ ] 筛选维度 3-7 个, 切了**所有 panel 真联动**?
- [ ] 明细表全实体, 有排序 + 搜索 + 分页?
- [ ] 下钻抽屉行点击有反馈?
- [ ] **chart 形态 ≥ 6 种** (顶级 ≥ 8 种), bar+pie 加起来 < 50%?
- [ ] **每个 chart 都用 `safeRender` 包裹** (一个错不拖死全部)?
- [ ] **grep `id="chart-` 跟 `echarts.init` 两份完全对应**?
- [ ] **grep `fetch(` / `src="[^h].*\.js"` / `src=".*\.json"` 全部 0 命中?** (产物不能引用任何本地数据文件 — D 死路必触发浏览器 file:// CORS, 双击空白)
- [ ] **数据是 inline 在 `<script>const D = {...}</script>` 里**, 不是放在外部 data.json / data.js?
- [ ] 没用 editorial 元素 (大字判断/章节编号/金句 blockquote)?
- [ ] ECharts 每个都 spread 主题 base?
- [ ] 整页**一次 write 完整 HTML / 一次 execute_python 内构造** (不是多次追加!), **1 个 HTML 文件**交付 (不是 HTML + data.json 两个文件)?

**全 ✓ = 顶级 dashboard**.
