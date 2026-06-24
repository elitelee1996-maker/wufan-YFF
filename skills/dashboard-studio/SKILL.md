---
name: 数据分析与可视化工坊
description: "数据深度挖掘 + 顶尖视觉的可视化交付工坊 — 让 Agent 既会榨干数据找业务洞察, 又能交付截图发朋友圈级审美的独立 HTML 作品。本技能不解决对话内的简单看数(那种直接出 widget 即可), 而是解决高价值、独立交付物级别的产出。数据来源不限: 用户上传的本地文件(Excel/CSV/JSON)或 Agent 联网研究、抓取、整合后的二手数据均可。两大产出形态: ① dashboard(BI 驾驶舱 / 自助分析仪表盘 / 数据看板, 多面板真联动 + 全局筛选 + 下钻抽屉) ② editorial(数据分析报告 / 数据期刊 / 行业白皮书 / 复盘长读 / 杂志感年度刊, 深度叙事 + 富文本排版 + 视觉冲击)。当用户提及 数据分析/数据分析报告/数据报告/数据期刊/数据看板/数据驾驶舱/仪表盘/dashboard/BI/数据故事/数据叙事/复盘/月报/周报/年报/白皮书/行业研究/业务洞察/数据可视化, 或上传/抓取数据并希望产出专业可视化交付物时, 优先触发本技能。"
---

# 数据分析与可视化工坊

> 这个技能让你做好两件事:
> 1. **数据深度挖掘 + 专业分析** — 善用 Python 把数据榨干, 不要克制调用次数, 找反常识、找金句、找业务洞察.
> 2. **顶尖视觉的可视化产出** — 选一套主题样板, 抄它的视觉结构跟交互逻辑, 改成业务数据, 一次性交付一份能截图发朋友圈的 HTML.

---

## 🎯 4 步工作流 (一气呵成)

```
1. read 用户数据 (看字段 + 样本)
2. read 本文档 — 选主题 (graphic-press / ...) + 选形态 (dashboard / editorial)
3. read 3 个文件:
   · themes/<主题>/soul.md
   · themes/<主题>/<形态>-example.html
   · references/<形态>-playbook.md
4. 善用 execute_python 把数据榨干 → write 一次性整页 HTML
```

**完事**. 不要 scaffold / analyze / lint, 不要套子目录, 不要**多次 execute_python 分段追加** (详见下方"两条路 + B 路径强规范"), 不要产多个 HTML.

---

## ✨ 输出心法 · 默认要超用户预期

除非用户**明确说**"简短 / 概要 / 几条要点", 否则**默认按"顶级深度专业、内容量丰富"理解**, 哪怕用户只说一句"做个分析报告":

- **超预期**: 把"做个分析"理解成"做个能拿去给老板汇报的深度专业作品"
- **内容规模**: editorial 默认 **≥ 15 节**; dashboard 默认 ≥ 8 KPI + ≥ 6 chart panel + 全实体明细
- **多元表达**: 多角度观点 + 丰富 chart 形态 (≥ 6 种) + 不同布局节奏, 不要一种模板通篇重复
- **善用 Python**: 该多挖几轮就多挖几轮, **不要克制 Python 调用次数** — 数据没榨干就不要急着写 HTML

**极简的是技能本身, 不是产物**. 用户给你 1 句话, 你回他 1 篇深度报告.

---

## 🧭 形态选择 (dashboard vs editorial)

**两种产物完全不同, 不要混**:

| 形态 | 用什么时候 | 关键差异 |
|---|---|---|
| **`dashboard`** (自助分析仪表盘) | 用户要"看板 / 仪表盘 / 监控 / BI / 驾驶舱 / 自助分析", 或数据有**多维筛选 + 实体明细**需求 | 高密度 KPI 阵 + 全局筛选 + 多 chart panel + 明细表 + 下钻抽屉. **工具型**, 用户来探索 |
| **`editorial`** (数据期刊 / 深度报告) | 用户要"报告 / 期刊 / 复盘 / 白皮书 / 故事 / 深度分析", 或数据**有可叙事的反常识洞察** | 大字 Hero 判断主标 + 章节叙事 + 反常识金句 + 引语 + Polaroid 卡. **作品型**, 用户来阅读 |

**模糊场景默认 `editorial`** — 它的"截图发朋友圈" 视觉冲击更强.

---

## 🎨 主题选择

| 主题 | 中文名 | 适合场景 | dashboard | editorial |
|---|---|---|---|---|
| `graphic-press` | 多彩胶囊报刊 | ⭐**默认首选** · 创意 / 鲜艳 / Spotify Wrapped 感 / 营销周报 / 年度回顾 / 数据故事 / 视觉爆款 / 任何"想做得好看"的通用数据报告 | ✅ | ✅ |
| `blue-consulting` | 蓝色咨询风 | ⚠**显式白名单** · 仅当用户明确点名"蓝色"/"咨询"/咨询公司名(麦肯锡/Bain/BCG)时才用 | ✅ | ✅ |
| `rose-press` | 玫红报刊 | 时装 / 品牌 / 编辑部 / 生活方式 / 文化报道 / Vogue 感年度刊 | ✅ | ✅ |
| `aurora-noir` | 暗夜极光 | Web3 / 加密 / 科技产品 / SaaS / 实时监控 / 创业团队 / Cursor 感 | ✅ | ✅ |
| `luminous-paper` | 晨光纸笺 | SaaS 产品 / 项目管理 / 团队协作 / 数据运营 / 工程效率 / Notion·Linear 感 | ✅ | ✅ |
| `macaron-stripe` | 马卡龙条纹 | 加密 / 金融理财 / 消费产品 / 年轻品牌 / 生活方式 App / 健康记录 | ✅ | ✅ |
| `ember-noir` | 鎏金暗夜 | 私人银行 / 财富管理 / Pro 交易所 / 高端金融 / 奢侈品零售 / 黑卡会员 | ✅ | ✅ |
| `prism-studio` | 棱镜工作室 | 科技公司 / AI / 软件 / 设计工作室 / 品牌报告 / 开发者平台 / 前瞻白皮书 | ✅ | ✅ |
| `kinetic-noir` | 动感暗夜 | 运动健身 / 训练监控 / 健康追踪 / 户外品牌 / 能量饮料 / Nike·Strava·Whoop 感 | ✅ | ✅ |
| _其他主题_ | | | 🚧 | 🚧 |

**怎么选**:

> 💡 **没明确风格倾向时, 默认优先 `graphic-press`** — 这是视觉表现力最强、实施最稳、最通用的"美观数据报告"风格. 只有用户明确点名其他主题的语境特征 (暗夜霓虹 / 香槟金奢华 / 运动健身 / 时装杂志...) 时才换.
>
> 🚫 **`blue-consulting` 是严格显式白名单触发** — **只有**用户明确说出"蓝色"/"咨询"/咨询公司名(麦肯锡/Bain/BCG)时才用. **绝不**因为"严肃 / 学术 / 投研 / 战略 / 投资分析 / 复盘 / 报告"等通用严肃语境就选它. 这些场景一律走 `graphic-press`(它做严肃报告也完全够用且更稳). 原因: blue 的 3D 点云球用 three.js + WebGL 实现, 标志元素复杂, 实施失败率明显高于其他主题.

- 用户说"多彩胶囊 / 鲜艳 / 多彩 / 缤纷 / 高颜值 / 好看 / 醒目 / 视觉冲击 / 视觉爆款 / Spotify Wrapped / 营销 / 周报 / 月报 / 年报 / 年度回顾 / 复盘 / 数据故事 / 创意报告 / 报刊艺术 / 印刷感 / 胶囊 / pill / 渐变 / Wrapped / 想做得好看" → `graphic-press` (⭐**默认首选**)
- 用户**显式**说"蓝色 / 咨询 / Blue / Consulting / 麦肯锡 / Bain / BCG / 咨询风" → `blue-consulting` (🚫 **严格白名单 only** — 必须命中以上显式关键词才触发; "学术/战略/投资分析/行业研究/严肃报告"**等通用严肃语境一律不触发**, 走 graphic-press)
- 用户说"时装 / 品牌 / 编辑部 / 生活方式 / Vogue / Apple Newsroom / 杂志 / 高级感 / 玫红 / 浅粉" → `rose-press`
- 用户说"暗夜 / 霓虹 / 极光 / 科技感 / 未来感 / 酷炫 / Web3 / 加密 / Cursor / 暗色 / 电影感 / 深邃" → `aurora-noir`
- 用户说"清爽 / 明亮 / 简洁 / 工作台 / 协作 / SaaS / Notion / Linear / 工程师 / 项目管理 / 白底" → `luminous-paper`
- 用户说"马卡龙 / 糖果色 / 薄荷绿 / 条纹 / 斜纹 / 软糯 / 大圆角 / 加密钱包 / 理财 / 年轻 / 可爱有设计感" → `macaron-stripe`
- 用户说"黑金 / 香槟金 / 鎏金 / 烫金 / 质感 / 私人银行 / 财富 / 高端理财 / 奢侈 / 黑卡 / 腕表 / 暖色暗夜 / 沉稳奢华" → `ember-noir`
- 用户说"科技品牌 / 软件公司 / AI / 衬线 + 科技 / 电光紫绿 / 几何线框 / 编辑设计 / Solvd / Stripe 感 / 设计工作室" → `prism-studio`
- 用户说"运动 / 健身 / 训练 / 跑步 / 户外 / 能量 / Nike / Strava / Whoop / Apple Fitness / 烈橙 / 极粗大写字 / 运动品牌" → `kinetic-noir`
- 模糊场景: **完全没指定 / 想做得好看 / 不知道选哪个 / 通用严肃报告 / 学术 / 投研 / 战略复盘** → ⭐`graphic-press` (默认首选, 几乎所有模糊场景都走它); **明确说"蓝色咨询"或点名咨询公司** → `blue-consulting` (显式 only); **鲜艳活跃** → `graphic-press`; **高级杂志感** → `rose-press`; **科技暗夜·冷炫酷** → `aurora-noir`; **奢华暗夜·暖金融** → `ember-noir`; **清爽明亮工作台** → `luminous-paper`; **马卡龙糖果柔软** → `macaron-stripe`; **科技品牌·衬线编辑** → `prism-studio`; **运动品牌·能量直接** → `kinetic-noir`
- ⚠ **noir 三子别选混** (aurora / ember / kinetic 同是暗底, 调性完全相反, 看主色 + 字体一秒辨):
  - 冷紫青·赛博炫光发光·Montserrat → `aurora-noir`
  - 暖香槟金·磨砂玑镂沉稳·Sora 几何 → `ember-noir`
  - **烈橙红·直接有力·Anton 极粗大写** → `kinetic-noir` (运动品牌能量, 跟 ember 的奢华内敛是反方向)
- ⚠ **prism-studio vs aurora-noir** (都暗+都有紫): prism 是**衬线编辑·扁平紫绿·几何线框·零发光**; aurora 是**霓虹玻璃·发光极光·赛博电影**. 要"科技品牌杂志感" → prism; 要"赛博发光炫酷" → aurora
- ⚠ **prism-studio vs macaron-stripe** (用户强调拉开): prism 是**炭黑深底·高饱和电光紫绿·锐利几何·优雅衬线** (科技前卫); macaron 是**浅灰绿底·马卡龙柔色·软糯大圆角·圆润字** (甜美柔和). 一深一浅、一锐一柔, 天壤之别

**九套风格哲学九角** (四暗·三调性分立 + 两暖亮 + 一冷亮 + 一柔亮, 彼此分立):
- `graphic-press` = ⭐**鲜艳报刊艺术 · 默认首选** (暖亮 · 米黄底 + 45° 暗线 + 5 套渐变胶囊 + 999px pill. 视觉表现力最强、实施最稳, 通用美观数据报告的兜底首选 — 用户无明确风格倾向时默认它)
- `blue-consulting` = **咨询学术克制** (暗 · 深蓝底 + 唯一钢蓝 + 极薄 hairline + 4-6px 极小圆角 + 3D 点云球. 🚫 **严格显式白名单触发** — 仅当用户明确点名"蓝色 / 咨询 / 麦肯锡 / Bain / BCG"时才用. "学术/战略/投资分析"等通用严肃场景一律走 graphic-press. 3D 点云球用 three.js + WebGL, 实施失败率明显高于其他主题)
- `rose-press` = **杂志高级时装** (暖亮 · 浅粉雾染 mesh + 唯一玫红 + Cormorant italic em 自动重音 + polaroid 拍立得 + 64px 杂志圆角)
- `aurora-noir` = **暗夜霓虹电影感 (冷)** (暗 · 近黑 #030406 + CSS 极光环境光 + 玻璃震慑卡 + 主紫 #8B2BF6 + cyan 协奏 + Montserrat 极粗大字 + chart 真"光圈" shadowBlur)
- `luminous-paper` = **清爽 SaaS 工作台** (冷亮 · 近白三阶 #fff/#f9fafb/#f3f4f6 + dot-grid + 蓝主线 #3b82f6 + 4 套贴纸色 + Inter/思源黑 500-600 + 无阴影 hairline 卡 + tabular-nums)
- `macaron-stripe` = **马卡龙糖果 + 条纹质感** (柔亮 · 浅灰绿底 #E4EAE4 + 薄荷绿 #A8E6A0/薰衣草紫 #B0A4F5 双主色 + ⭐斜条纹/圆点纹理 + 一张近黑卡反差 + 24-40px 超大软圆角 + 圆形 icon + Poppins 极粗大数字 + chart decal 斜纹柱)
- `ember-noir` = **鎏金暗夜·奢华金融 (暖·质感克制)** (暗 · 哑光暖黑 #0C0B09 + ⭐磨砂颗粒 (grain) + 金属拉丝 + 玑镂纹质感 + 香槟金 #C9A86A 点睛 (沉稳, 占面积 < 10%) + 烫金箔标题 + 金 hairline 细节 + Sora 几何字 + chart 香槟金多明度梯度 (几乎不用 shadowBlur). **高端腕表 / 私人银行级的沉稳奢华, 靠质感+克制而非发光**. 跟 aurora-noir 是 noir 双子: 一冷紫青·炫光张扬 / 一暖香槟金·质感内敛, 绝不串色)
- `prism-studio` = **科技品牌编辑设计** (暗 · 炭黑 #161618 + 暖米白 #F5F1E6 拼贴 + ⭐Fraunces 现代衬线大标题 (人文) + 电光紫 #6C4FF5 / 荧光绿 #3DF577 双主色 (扁平高饱和) + 紫绿光谱渐变 + 像素条形马赛克 + ⭐3D 等距线框几何 + 米白胶囊 + 方块 logo. **优雅衬线 × 几何科技的人文自信, 全程零发光**. 跟 aurora-noir 区分: prism 衬线编辑·扁平·线框, aurora 霓虹玻璃·发光; 跟 macaron-stripe 区分: prism 炭黑锐利前卫, macaron 浅柔糖果)
- `kinetic-noir` = **动感暗夜·运动品牌能量 (暖·直接有力)** (暗 · 纯黑 #0E0E0E 中性底 + ⭐Anton 极粗 condensed 工业大写字 (Druk 替代, 第一识别符号) + 烈橙红 #FF6B2E 主色 (温度直接, 不是金) + 灰白对照 + ⭐橙→透明 area 渐变 + ⭐悬浮 pill 数据标注 (markPoint) + 超大软圆角 24-32px + 圆形头像/按钮. **Nike Run Club / Apple Fitness / Whoop 级运动品牌质感, 直接有力·零发光**. 跟 noir 双子区分: ember 是奢华金融香槟金内敛 / aurora 是赛博紫青霓虹炫光 / kinetic 是**运动烈橙能量直接** — 三套调性完全相反)

选错风格 → 跟业务气质不匹配, 哪怕做得再深度也"贴错标签".

---

## 🚀 操作指南

### Step 1 · 摸排数据

```python
import pandas as pd
df = pd.read_csv('xxx.csv')  # 或 pd.read_excel
print(df.shape, df.dtypes)
print(df.head(10))
# Dashboard 才需要的: 看分类列唯一值数, 决定哪些能做筛选
for col in df.select_dtypes('object').columns:
    print(f'{col}: {df[col].nunique()} 个唯一值')
```

知道 **字段名 + 样本 + 数据量级** 就够.

### Step 2 · 选主题 + 选形态

按上面两个表选. 例:
- 用户给海关流水说"做份咨询风战略复盘" → `blue-consulting` + `editorial`
- 用户给房产数据说"做个鲜艳的年度回顾" → `graphic-press` + `editorial`
- 用户给品牌数据说"做个杂志感的年度刊" → `rose-press` + `editorial`
- 用户给运营数据说"做个监控驾驶舱" + 强调"创意感" → `graphic-press` + `dashboard`

### Step 3 · read 3 个文件 (一次性读完)

按选定的形态, 从本技能目录下 read 3 个文件 (`<theme>` = 你选的主题 slug):

**如果选了 dashboard**:
```
themes/<theme>/soul.md                  (主题理念)
themes/<theme>/dashboard-example.html   (样板)
references/dashboard-playbook.md        (5 件套硬要求)
```

**如果选了 editorial**:
```
themes/<theme>/soul.md                  (主题理念)
themes/<theme>/editorial-example.html   (样板)
references/editorial-playbook.md        (3 硬指标 + 章节铁律)
```

**重点是 example.html** — 它是这套主题在该形态的完整呈现. 你**抄它的视觉结构 + JS 逻辑**, 改业务数据.

### Step 4 · execute_python 把数据榨干 → 选 A 或 B 路径交付整页 HTML

**两条路 (详见下方"写整页 HTML 的两条路")**:
- **路径 A**: 直接 `write` 整页 HTML (默认推荐, 简单稳)
- **路径 B**: 单次 `execute_python` 内构造 HTML 字符串 + `Path.write_text` 落盘 (复杂/大数据时用, 必须遵守 B 强规范)

无论 A 还是 B, 严禁多次 execute_python 分段追加 (= C 死路).

```python
# 用 execute_python 把所有要呈现的指标都算好 (按 playbook 的内容深度要求多挖几轮)
D = { ... }   # dashboard: 含 D.rows 全量明细; editorial: 含各节 chart 数据 + 文案数据
# write 整页
html = """<!DOCTYPE html>...
<script>
const D = """ + json.dumps(D, ensure_ascii=False) + """;
// 抄 example.html 的渲染逻辑
</script>..."""
Path('XXX.html').write_text(html, encoding='utf-8')
```

**关键纪律**:
- ✅ 一次交付 (A: 一次 write / B: 一次 execute_python + 一次 Path.write_text), 不分段追加
- ✅ 数据 inline 到 `<script>const D = {...}</script>` (不要 data.json / data.js 外置)
- ✅ 视觉结构抄 example.html (CSS / ECharts base / 章节模板)
- ✅ ECharts 每个都 spread `...gpEchartsBase`
- ✅ 走 B 路径必带 4 条强规范 (一个 cell / CHARTS list 维护 / ID 自检 / 错了重建不追加)
- ❌ 不要多次 execute_python 分段追加 (= C 死路, 12 个 chart 全空白警示)
- ❌ 不要产多个 .html (1 个就够)
- ❌ 不要混 dashboard + editorial 元素 (这个文件是 dashboard 就一直是 dashboard)

---

## ⚠ 绝对不要做的事

- ❌ 找 scaffold.py / analyze.py / lint.py — **本技能没有脚本**, 只有 markdown + example HTML
- ❌ **多次 `execute_python` 分段追加 HTML** (Path 多次 write_text / `mode='a'` / 一个 cell 写头一个 cell 写脚) — C 死路, 详见下方
- ❌ **任何形态的"数据外置文件 + HTML 引用"** — D 死路, 浏览器 file:// 禁止跨文件 fetch, 双击必空白:
  - 严禁 `fetch("*.json")` / `fetch("*.csv")` 在 HTML 内调
  - 严禁 `<script src="*.js">` 引用本地数据 JS (data.js / chart-data.js 等业务数据)
  - 严禁 `<link rel="import">` 跨文件加载
  - 严禁产物目录里出现 `data.json` / `data.js` / `chart-config.js` 等业务数据文件
  - 数据无论多大都 inline 到 `<script>const D = {...}</script>`, 详见下方 D 死路说明
- ❌ 产多个 .html 文件 (1 个就够)
- ❌ 混 dashboard 跟 editorial 元素 (选一种就一直是那种)
- ❌ **HTML 产物里 / 给用户的最终回复文本里使用 emoji 跟装饰 unicode 符号** — 详见下方铁律

**注**: ECharts / Three.js / 字体 CDN (jsdelivr / unpkg / googleapis) 是允许的 — 这些是 https:// 公开 CDN, 不受 file:// CORS 限制, 跟"业务数据外置"是两回事.

---

## 🛠 写整页 HTML 的两条路 + 两条死路

你有两条合法路径 (A / B), 自己根据场景选. **另有两条死路 (C / D) 严禁**.

### 路径 A · 一次 `write` 整页 (默认推荐)
直接调用 write tool 把完整 HTML 字符串作为 `content` 参数交付.

- ✅ 上下文最一致, ID 物理上不可能对不上
- ✅ 写完即交付, 不用额外自检
- ⚠ HTML 越大, 占的 LLM token 越多 (多轮修改时会重复传输)

**什么时候用**: **默认就用 A**. 简单/中型报告 / 一锤子交付场景.

### 路径 B · 单次 `execute_python` 构造 (高级, 复杂场景可用)
**一次** `execute_python`, 在 Python 内部完整构造 HTML 字符串, 末尾**一次** `Path.write_text(html)` 落盘.

- ✅ 大幅省 LLM token (HTML 字符串在 sandbox 里构造, 不进 LLM context)
- ✅ 适合数据驱动 (1000 行明细表用 for loop 模板)
- ✅ 适合复杂报告 / 反复修改的迭代场景
- ⚠ 必须 100% 遵守下方"B 路径强规范", 否则容易踩 ID 不对照 / 上下文割裂的坑

**什么时候用**: 报告**很复杂** / **数据量很大** / **需要数据驱动模板** / **预期多轮修改要省 token** — Agent 自己判断.

### 路径 C · 多次 `execute_python` 分段追加 ❌ 死路严禁
两次或以上 execute_python: cell 1 写头, cell 2 写中段, cell 3 写脚 / `Path.write_text` 多次调用 / `open(mode='a')` 追加 / `re.sub` 局部替换 ...

**为什么死**: HTML 里 `<div id="chart-yearly">` 跟 JS 里 `getElementById('chart-yearly-trend')` 在**不同 cell 里独立起名**, 上下文割裂必然对不上 → 一个 chart 抛异常 → **后续所有 chart 全停**. 实测案例: 12 个 chart 全空白就是这个原因.

### 路径 D · 数据外置 (写 data.json/data.js + HTML 引用) ❌ 死路严禁
任何形态的"代码/数据分离": 写 `data.json` + HTML 里 `fetch("data.json")` / 写 `data.js` + HTML 里 `<script src="data.js">` / 写 `config.json` + HTML 里 `<link rel="import">` ...

**为什么死**: **file:// 协议下浏览器禁止跨本地文件 fetch (Same-Origin Policy 强制)**. 用户拿到 dashboard 最常见的打开方式是**双击 HTML**, 此时:
- `fetch("data.json")` → CORS error, 数据加载不到 → 全屏空白
- `<script src="data.js">` 部分浏览器允许部分禁止, 加载路径还经常错位
- 用户不会调试浏览器 console, 看到空白只会觉得"Agent 做的不能用"

**这是浏览器物理限制, 不是技能偏好** — 任何外置都会触发. 唯一对的做法:
```python
# ✅ 数据无论多大, 都 inline 到 HTML 内
html = f"""...
<script>
const D = {json.dumps(D, ensure_ascii=False)};
// 全部 chart / 表格 / KPI 从 D 取数据
</script>
..."""
```

实测体感: 单文件 HTML 即使 **5MB+** (含数据 + ECharts CDN + 几千行明细) 浏览器也流畅. 不要怕 inline 大数据.

### write 失败别滑到 C / D 死路

| 失败场景 | ❌ 滑到死路 | ✅ 对的做法 |
|---|---|---|
| `write` 报"缺 content 参数" | 切 multi-shot Python 拼 (C) | **再调一次 `write`, 这次带上 content** |
| `write` 报"content 太长" | 切 multi-shot Python 分段 (C) / 拆 data.js + html (D) | **改走 B 路径** (一次 execute_python 内构造 + inline 数据) |
| 觉得"数据这么大 inline 太丑" | 拆出 data.json (D) | **没事, 浏览器吃得消; 用户只看打开效果, 不看源码** |
| 觉得"数据独立修改更方便" | 拆出 data.js (D) | **重新走 A 或 B 整页重生, 比 D 更稳** |
| 写完浏览器看着不对 | 切 multi-shot Python 重写 (C) | 用 `edit` 工具精改 / 重新走 A 或 B |

---

## 🚨 B 路径强规范 (走 B 必须 100% 遵守, 4 条)

### 规矩 ① 一个 cell 写完所有 HTML, 不许追加
```python
# ✅ 正确: 一个 cell 里完整构造 + 一次落盘
html = build_head() + build_body() + build_js()
Path("report.html").write_text(html, encoding='utf-8')
```
```python
# ❌ 死路: 多 cell 分段
Path("report.html").write_text(part1)            # cell 1
with open("report.html", "a") as f: f.write(p2)  # cell 2 (这是 C, 严禁)
```

### 规矩 ② 所有 chart ID 用一个 list 维护, HTML 跟 JS 都从它生成
这条最关键 — 物理上让 ID 不可能不对照:

```python
CHARTS = [
    {'id': 'chart-scatter',  'title': '面积 × 单价 散点',  'render': 'renderScatter'},
    {'id': 'chart-radar',    'title': '三圈层 6 维特征',   'render': 'renderRadar'},
    {'id': 'chart-heatmap',  'title': '朝向 × 装修 密度',  'render': 'renderHeatmap'},
    {'id': 'chart-treemap',  'title': '圈层 → 户型',       'render': 'renderTreemap'},
]

# HTML 部分: 容器 div 自动生成
chart_divs_html = "\n".join(
    f'<div class="chart-card"><h3>{c["title"]}</h3>'
    f'<div class="chart-host" id="{c["id"]}"></div></div>'
    for c in CHARTS
)

# JS 部分: init 调用自动生成
chart_init_js = "\n".join(
    f'safeRender("{c["id"]}", () => {c["render"]}("{c["id"]}"));'
    for c in CHARTS
)
```

HTML 跟 JS 都引用同一份 CHARTS, 改 ID 只改一处, 不可能漏改一边.

### 规矩 ③ 落盘前用 Python 自检 ID 对照
```python
import re
html_ids = set(re.findall(r'id="(chart-[a-zA-Z0-9_-]+)"', html))
js_ids   = set(re.findall(r'["\'](chart-[a-zA-Z0-9_-]+)["\']', html))
missing  = html_ids - js_ids
extra    = js_ids - html_ids
assert not missing, f"❌ HTML 有 div 但 JS 没引用: {missing}"
assert not extra,   f"❌ JS 引用了不存在的 ID: {extra}"
print(f"✅ chart ID 对照通过 · {len(html_ids)} 个")
Path("report.html").write_text(html, encoding='utf-8')
```

不通过 → 修了再 write, 千万别带病落盘.

### 规矩 ④ 错了不许切 C 路径修补
- write_text 写完发现内容不对? → 重新跑一个 execute_python **整段重建** (还是 B 路径), 或用 `edit` 工具精改
- ❌ 永远不要 `with open(mode='a')` 追加补丁
- ❌ 永远不要再起一个 execute_python 在尾巴 append 一段

---

---

## 🚫 严禁 emoji 跟装饰符号 (产物里)

**铁律**: 你产出的 HTML 文件文案 (标题/段落/章节名/KPI 标签...) 跟最终回复给用户的文本 **绝对不要用 emoji 跟装饰 unicode 符号**. 三套主题都是顶级专业刊物/咨询/杂志气质, 一个 emoji 就让整个作品掉一档.

**包括但不限于**:
- emoji: 📊 📈 💡 🔍 📌 📦 🚀 🎨 🎯 ✨ ⚡ ⭐ ❗ 🌟 🔥 ✅ ❌ 🎉 ...
- 装饰 unicode: ✓ ✗ ★ ☆ ▲ ▼ ● ◆ ■ ◯ ... (这些常被 LLM 当 "checkmark" 用, 也禁)
- 复合修饰: 「✓ 完成」「📊 数据看板」「💡 洞察」 ...

**用什么代替**:
- 标题强调: 用 `<em>` 包关键词 (rose-press 玫红 italic / blue-consulting 钢蓝 spot / graphic-press 渐变胶囊) 或 `<strong>` — 比 emoji 高级 100 倍
- 列表分隔: 用 mono 编号 (`01 / 02 / 03`) 或衬线大数字, 不要 emoji bullet
- 状态指示: 用文字 ("已完成 · 待处理 · 异常") 或 CSS pill 标签
- 章节装饰: 用 kicker 横线 / hairline / 数字 ghost 等主题原生元素

**例外 (可以用的)**:
- `<` `>` `←` `→` `↑` `↓` `÷` `×` `±` `≥` `≤` ... 这些是**数学/方向运算符**, 不是 emoji
- `·` `—` `…` ... 这些是**排版标点**, 不是 emoji
- skill 文档 (SKILL.md / soul.md / playbook.md) 里的 emoji 是给 Agent 阅读的引导符号, **跟产物无关**, 不在禁用之列

**自检**: 写完 HTML 跟最终回复后, 自己扫一眼有没有这些字符 (Unicode 范围 U+1F300-1F9FF / U+2600-27BF / 还有 ✓ ✗ ★ 等). 有就改掉.

---

## 📦 产物

一个 `.html` 文件, 自含一切. 用户双击打开就能看, 截图发朋友圈不掉链子.

