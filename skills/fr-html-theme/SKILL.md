---
name: 帆软HTML主题
description: 帆软PPT浅色模版的HTML/CSS视觉规范与生成工具。当需要生成HTML报告、方案文档、流程图、数据看板等任何面向客户的HTML页面时使用。确保所有HTML产出物在色彩、字体、间距、页眉页脚、Logo使用上与帆软官方PPT模版保持视觉一致。触发词：帆软主题、帆软风格、帆软配色、FR主题、生成报告HTML、方案HTML。
---

# 帆软 HTML 主题

将帆软 PPT 浅色模版的视觉体系应用到 HTML 产出物中，确保品牌一致性。

## 快速使用

### 方式一：脚本生成基础框架（推荐）

```bash
python skills/fr-html-theme/scripts/generate_html_base.py \
  --title "报告标题" \
  --subtitle "副标题（可选）" \
  --sections "章节1,章节2,章节3" \
  --output report.html
```

生成的 HTML 已包含完整的帆软视觉体系：页眉（标题+Logo+蓝色分隔线）、章节导航、内容区域（含预制组件样式）、页脚（Logo+标语）。

### 方式二：手动引用设计令牌

当需要自定义复杂页面（如流程图、数据看板）时：

1. 读取 `skills/fr-html-theme/references/design-tokens.md` 获取完整色彩/字体/间距规范
2. 读取 `skills/fr-html-theme/assets/fr-logo.svg` 获取 Logo SVG 路径
3. 按规范中的 CSS 变量体系编写 HTML

## 设计令牌速查

### 色彩（CSS 变量）

```css
:root {
  /* 主题色 */
  --fr-blue: #0086E6;       /* 主色 */
  --fr-navy: #17346E;       /* 深蓝/主文字 */
  --fr-gray: #566280;       /* 普通文字 */
  --fr-mid-blue: #0F6FC6;   /* 中蓝 */
  --fr-light-blue: #00ACE6; /* 浅蓝 */
  --fr-orange: #F39600;     /* 重点/强调 */
  /* 功能色 */
  --fr-success: #00B35C;    /* 成功 */
  --fr-warn: #CC0010;       /* 错误/危险 */
  --fr-yellow: #F3C900;     /* 警告 */
  /* 中性色 */
  --fr-line: #B8BECC;       /* 线/边框 */
  --fr-bg1: #EBEFF4;        /* 浅背景1 */
  --fr-bg2: #F0F4F8;        /* 浅背景2/页面背景 */
  --fr-bg3: #F0F2F5;        /* 浅背景3/页脚背景 */
  --fr-dk-bg: #8F99B3;      /* 深色背景 */
  --fr-white: #FFFFFF;
  /* Logo */
  --fr-logo-dark: #007ed3;
  --fr-logo-light: #20ade5;
}
```

### 字体

- 全局字体：`"微软雅黑", "Microsoft YaHei", "PingFang SC", Arial, sans-serif`
- 标题：`--fr-navy`(#17346E)，20-24px，font-weight 700
- 正文：`--fr-gray`(#566280)，14px，line-height 1.6-1.8
- 辅助文字：`--fr-dk-bg`(#8F99B3)，12px

### 页眉页脚结构

```
页眉：[标题 22px 粗体] ─────────── [帆软Logo 97×32px]
      ━━━━━━━━━━━━ (#0086E6 2px蓝色分隔线)

页脚：━━━━━━━━━━━━ (#0086E6 2px蓝色分隔线)
      [帆软Logo 58×19px] [让数据成为生产力]
```

### 预制组件

脚本生成的 HTML 包含以下 CSS class，直接使用：

| 组件 | class | 说明 |
|------|-------|------|
| 卡片 | `.card` `.card-title` | 白底圆角卡片 |
| 信息块 | `.info-block` `.warn` `.success` `.danger` | 左侧彩色边条 |
| 徽章 | `.badge` `.badge-blue/green/orange/red/gray` | 状态标签 |
| 表格 | `.fr-table` | 深蓝表头+斑马行 |
| 指标卡 | `.metric-grid` `.metric-card` `.metric-value` `.metric-label` | 数字展示 |

## 设计红线

1. **禁止自创配色**：所有颜色必须来自上述 CSS 变量，不得自行发明色值
2. **禁止修改 Logo**：Logo SVG 路径和双色（#007ed3 + #20ade5）不可更改
3. **禁止省略页眉页脚**：面向客户的 HTML 必须包含帆软页眉（标题+Logo+蓝线）和页脚（Logo+标语）
4. **谨慎使用高饱和色**：功能色（红/橙/黄/绿）只能小面积出现，不得大面积铺底
5. **字体统一**：全局使用微软雅黑，不得使用其他字体

## 高清 PNG 导出

如需将 HTML 导出为高清 PNG 发给客户：

```python
import asyncio, os
from playwright.async_api import async_playwright

async def export_png():
    html_path = os.path.abspath("report.html")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": 1600, "height": 900},
            device_scale_factor=3  # 3x 高清
        )
        await page.goto(f"file://{html_path}")
        await page.wait_for_timeout(2000)
        el = await page.query_selector('.page')
        await el.screenshot(path="report.png", type="png")
        await browser.close()

asyncio.run(export_png())
```

## 资源文件

| 路径 | 用途 |
|------|------|
| `assets/fr-logo.svg` | 帆软 Logo SVG 源文件 |
| `references/design-tokens.md` | 完整设计令牌文档（色彩/字体/间距/原则） |
| `scripts/generate_html_base.py` | HTML 基础框架生成脚本 |
