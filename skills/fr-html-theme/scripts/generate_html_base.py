#!/usr/bin/env python3
"""
帆软 HTML 主题生成器
生成带有帆软 PPT 浅色模版视觉风格的 HTML 基础框架

用法:
    python generate_html_base.py --title "报告标题" --output report.html
    python generate_html_base.py --title "报告标题" --subtitle "副标题" --output report.html
    python generate_html_base.py --title "报告标题" --sections "摘要,详情,结论" --output report.html
"""

import argparse
import os
import sys

# 帆软 Logo SVG (内联)
FR_LOGO_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96.91 32.19" width="{w}" height="{h}">
  <g>
    <path fill="#20ade5" d="M21.92,0h-9.72v9.98h9.97v22.21h1.09c5.04,0,8.88-3.82,8.88-8.87V1.12c0-.72-.4-1.12-1.12-1.12h-9.11Z"/>
    <path fill="#007ed3" d="M19.97,12.2h-9.98V0h-1.11C3.84,0,0,3.86,0,8.9v21.99c0,.72.58,1.3,1.3,1.3h8.68v-9.99h9.98v-10Z"/>
  </g>
  <g>
    <g>
      <path fill="#007ed3" d="M62.05,10.52h-2.74c-.32,0-.27.29-.27.29l.34,11.09s.16,1.24,1.11,1.24h1.95c.25,0,.26-.24.26-.24l-.37-12.12s-.03-.27-.28-.27Z"/>
      <path fill="#007ed3" d="M52.86,6.24h-3.21v-1.92c0-.15-.08-.24-.21-.24h-2.81c-.34,0-.27.28-.27.28v1.87h-3.29s-.99.03-.99,1.02v19.32s-.02.21.16.21h1.58s1.55-.03,1.55-2V8.5h.99v19.37s0,.24.18.24h1.54s1.57,0,1.57-1.67V8.5h.33c.63,0,.57.6.57.6v17.37s-.05.32.23.32h1.31c1.81,0,1.75-2.09,1.75-2.09V7.31c0-1.07-.98-1.07-.98-1.07Z"/>
      <path fill="#007ed3" d="M67.28,25.82c-.86,0-.79-.92-.79-.92V5.88s.02-1.82-1.95-1.82h-8.52s-1.22-.11-1.22,1.29v22.42c0,.2.11.3.28.3h1.2c1.77,0,1.81-2.07,1.81-2.07V6.9s-.14-.58.54-.58c1.05,0,3.39,0,3.96,0,.64,0,.62.64.62.64v19.13s.11,1.98,1.7,1.98h2.34c.35,0,.35-.37.35-.37v-1.52s0-.37-.31-.37Z"/>
    </g>
    <g>
      <path fill="#007ed3" d="M95.37,6.71h-6.98c-.54,0-.39-.34-.39-.34.03-.06.07-.16.09-.23l.63-1.93c.02-.07-.02-.12-.08-.12h-3.45c-.07,0-.14.05-.16.12l-.98,3.02c-.02.07-.05.17-.07.24,0,0-.35,1.5,1.25,1.5h7.47c.55,0,.53.48.53.48,0,.07,0,.18,0,.25v4.54c0,.07.06.12.12.12h3.45c.07,0,.12-.05.12-.12v-6.1c0-.07,0,1.03,0-.25s-1.47-1.18-1.54-1.18Z"/>
      <path fill="#007ed3" d="M82.91,23.86c.07,0,.12-.06.12-.12v-2.01c0-.07-.05-.12-.12-.12h-2.37v-3.48h2.37c.07,0,.12-.06.12-.12v-2.01c0-.07-.05-.12-.12-.12h-2.37v-4.93c0-.07-.06-.12-.12-.12h-3.45c-.07,0-.12.05-.12.12v4.93h-.86c-.45,0-.41-.46-.41-.46,0-.07.02-.18.04-.24l1.19-6.19h6.11c.07,0,.12-.05.12-.12v-2.01c0-.07-.05-.12-.12-.12h-5.68l.48-2.5c.01-.07-.03-.12-.1-.12h-3.45c-.07,0-.13.05-.15.12l-.48,2.5h-2.07c-.07,0-.12.05-.12.12v2.01c0,.07.05.12.12.12h1.63l-1.44,7.5c-.01.07-.03.18-.04.24,0,0-.21,1.42,1.15,1.42h2.15c.07,0,.12,0,.12,0,0,0,.06,0,.13,0h1.68v3.48h-5.37c-.07,0-.12.05-.12.12v2.01c0,.07.05.12.12.12h5.37v4.15c0,.07.05.12.12.12h2.1c1.38,0,1.47-1.47,1.47-1.47,0-.07,0-.18,0-.25v-2.55h2.37Z"/>
      <path fill="#007ed3" d="M96.37,25.85h-.38c-.47,0-.57-.35-.57-.35-.02-.06-.04-.17-.06-.24l-1.93-8.96c-.02-.06-.08-.12-.15-.12h-3.36c.79-3.47.69-5.24.69-5.24,0-.07-.06-.12-.13-.12h-3.45c-.07,0-.12.05-.12.12,0,0,.16,3.62-1.41,8.36-1.39,4.22-3.34,8.72-3.34,8.72-.02.06,0,.12.08.12h2.86c.07,0-.33,0,.25,0s.76-.66.79-.73c0,0,1.66-3.97,2.87-7.82.35-1.1.6-2.06.81-2.95l2.24,10.38c.01.07.05.17.07.23,0,0,.32.86,1.18.86h.47s.06,0,.12,0h2.59c.43,0,.4-.42.4-.48v-1.27c0-.07.03-.51-.52-.51Z"/>
    </g>
  </g>
</svg>'''


def generate_html(title: str, subtitle: str = "", sections: list = None, output: str = "report.html", max_width: int = 1400):
    """生成带有帆软主题的 HTML 基础框架"""
    
    # 构建章节导航
    nav_html = ""
    sections_html = ""
    if sections:
        nav_items = []
        for i, sec in enumerate(sections, 1):
            sec_id = f"section-{i}"
            nav_items.append(f'<a href="#{sec_id}" class="nav-item">{sec}</a>')
            sections_html += f'''
    <section id="{sec_id}" class="content-section">
      <h2 class="section-title">{sec}</h2>
      <div class="section-body">
        <!-- 在此填充 {sec} 的内容 -->
        <p class="placeholder">内容待填充</p>
      </div>
    </section>
'''
        nav_html = f'''
  <nav class="section-nav">
    {"".join(nav_items)}
  </nav>
'''
    
    # 副标题 HTML
    subtitle_html = ""
    if subtitle:
        subtitle_html = f'<p class="header-subtitle">{subtitle}</p>'
    
    # Logo SVG
    logo_header = FR_LOGO_SVG.format(w=97, h=32)
    logo_footer = FR_LOGO_SVG.format(w=58, h=19)
    
    # Pre-compute content block
    default_content = "    <!-- 在此填充页面内容 -->\n    <p class=\"placeholder\">内容待填充</p>"
    content_block = sections_html if sections_html else default_content

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  /* ========================================
     帆软 PPT 浅色模版 — 设计令牌
     ======================================== */
  :root {{
    /* 主题色 */
    --fr-blue: #0086E6;
    --fr-navy: #17346E;
    --fr-gray: #566280;
    --fr-mid-blue: #0F6FC6;
    --fr-light-blue: #00ACE6;
    --fr-sky: #33AAFF;
    --fr-deep: #1567D9;
    --fr-orange: #F39600;
    /* 功能色 */
    --fr-warn: #CC0010;
    --fr-success: #00B35C;
    --fr-yellow: #F3C900;
    /* 中性色 */
    --fr-line: #B8BECC;
    --fr-bg1: #EBEFF4;
    --fr-bg2: #F0F4F8;
    --fr-bg3: #F0F2F5;
    --fr-arrow: #DADEE6;
    --fr-white: #FFFFFF;
    --fr-dk-bg: #8F99B3;
    /* Logo 色 */
    --fr-logo-dark: #007ed3;
    --fr-logo-light: #20ade5;
  }}

  /* ========================================
     基础重置
     ======================================== */
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: var(--fr-bg2);
    font-family: "微软雅黑", "Microsoft YaHei", "PingFang SC", "Hiragino Sans GB", Arial, sans-serif;
    font-size: 14px;
    line-height: 1.6;
    color: var(--fr-gray);
    padding: 24px;
  }}

  /* ========================================
     页面容器
     ======================================== */
  .page {{
    max-width: {max_width}px;
    margin: 0 auto;
    background: var(--fr-white);
    border-radius: 2px;
    box-shadow: 0 2px 12px rgba(23,52,110,.06);
    overflow: hidden;
  }}

  /* ========================================
     页眉 (Header)
     ======================================== */
  .header-bar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 36px 12px;
    background: var(--fr-white);
  }}
  .header-left {{
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}
  .header-title {{
    font-size: 22px;
    font-weight: 700;
    color: var(--fr-navy);
    letter-spacing: .5px;
    line-height: 1.3;
  }}
  .header-subtitle {{
    font-size: 12px;
    color: var(--fr-gray);
    font-weight: 400;
  }}
  .header-logo svg {{
    display: block;
  }}
  .header-line {{
    height: 2px;
    background: var(--fr-blue);
    margin: 0;
  }}

  /* ========================================
     章节导航
     ======================================== */
  .section-nav {{
    display: flex;
    gap: 0;
    padding: 0 36px;
    background: var(--fr-bg3);
    border-bottom: 1px solid var(--fr-line);
    overflow-x: auto;
  }}
  .nav-item {{
    padding: 10px 20px;
    font-size: 13px;
    color: var(--fr-gray);
    text-decoration: none;
    border-bottom: 2px solid transparent;
    white-space: nowrap;
    transition: all .2s;
  }}
  .nav-item:hover {{
    color: var(--fr-blue);
    border-bottom-color: var(--fr-blue);
    background: rgba(0,134,230,.04);
  }}

  /* ========================================
     内容区域
     ======================================== */
  .content-area {{
    padding: 24px 36px;
  }}
  .content-section {{
    margin-bottom: 32px;
  }}
  .content-section:last-child {{
    margin-bottom: 0;
  }}

  /* ========================================
     排版 (Typography)
     ======================================== */
  .section-title {{
    font-size: 20px;
    font-weight: 700;
    color: var(--fr-navy);
    padding-bottom: 10px;
    margin-bottom: 16px;
    border-bottom: 2px solid var(--fr-blue);
    line-height: 1.3;
  }}
  .section-body h3 {{
    font-size: 16px;
    font-weight: 600;
    color: var(--fr-navy);
    margin: 20px 0 10px;
  }}
  .section-body h4 {{
    font-size: 14px;
    font-weight: 600;
    color: var(--fr-mid-blue);
    margin: 16px 0 8px;
  }}
  .section-body p {{
    font-size: 14px;
    color: var(--fr-gray);
    line-height: 1.8;
    margin-bottom: 12px;
  }}
  .section-body ul, .section-body ol {{
    padding-left: 20px;
    margin-bottom: 12px;
  }}
  .section-body li {{
    font-size: 14px;
    color: var(--fr-gray);
    line-height: 1.8;
    margin-bottom: 4px;
  }}

  /* ========================================
     通用组件
     ======================================== */

  /* 卡片 */
  .card {{
    background: var(--fr-white);
    border: 1px solid var(--fr-line);
    border-radius: 4px;
    padding: 16px 20px;
    margin-bottom: 16px;
  }}
  .card-title {{
    font-size: 15px;
    font-weight: 600;
    color: var(--fr-navy);
    margin-bottom: 8px;
  }}

  /* 信息块 */
  .info-block {{
    background: var(--fr-bg1);
    border-left: 3px solid var(--fr-blue);
    padding: 12px 16px;
    margin-bottom: 16px;
    border-radius: 0 4px 4px 0;
  }}
  .info-block.warn {{
    border-left-color: var(--fr-orange);
    background: #FFF8EC;
  }}
  .info-block.success {{
    border-left-color: var(--fr-success);
    background: #F0FAF5;
  }}
  .info-block.danger {{
    border-left-color: var(--fr-warn);
    background: #FEF2F2;
  }}

  /* 徽章 */
  .badge {{
    display: inline-block;
    padding: 2px 10px;
    border-radius: 3px;
    font-size: 12px;
    font-weight: 600;
    line-height: 1.6;
  }}
  .badge-blue {{ background: #E6F3FF; color: var(--fr-blue); }}
  .badge-green {{ background: #E6F7F0; color: var(--fr-success); }}
  .badge-orange {{ background: #FFF3E0; color: var(--fr-orange); }}
  .badge-red {{ background: #FEE2E2; color: var(--fr-warn); }}
  .badge-gray {{ background: var(--fr-bg1); color: var(--fr-gray); }}

  /* 表格 */
  .fr-table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 16px;
    font-size: 13px;
  }}
  .fr-table th {{
    background: var(--fr-navy);
    color: var(--fr-white);
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
    font-size: 13px;
  }}
  .fr-table td {{
    padding: 10px 14px;
    border-bottom: 1px solid var(--fr-line);
    color: var(--fr-gray);
  }}
  .fr-table tr:nth-child(even) td {{
    background: var(--fr-bg2);
  }}
  .fr-table tr:hover td {{
    background: var(--fr-bg1);
  }}

  /* 指标卡 */
  .metric-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin-bottom: 20px;
  }}
  .metric-card {{
    background: var(--fr-white);
    border: 1px solid var(--fr-line);
    border-radius: 4px;
    padding: 16px;
    text-align: center;
  }}
  .metric-value {{
    font-size: 28px;
    font-weight: 700;
    color: var(--fr-blue);
    line-height: 1.2;
  }}
  .metric-label {{
    font-size: 12px;
    color: var(--fr-gray);
    margin-top: 4px;
  }}
  .metric-card.warn .metric-value {{ color: var(--fr-orange); }}
  .metric-card.success .metric-value {{ color: var(--fr-success); }}
  .metric-card.danger .metric-value {{ color: var(--fr-warn); }}

  /* 占位符 */
  .placeholder {{
    color: var(--fr-dk-bg);
    font-style: italic;
    padding: 20px;
    text-align: center;
    background: var(--fr-bg2);
    border-radius: 4px;
    border: 1px dashed var(--fr-line);
  }}

  /* ========================================
     页脚 (Footer)
     ======================================== */
  .footer-bar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 36px;
    border-top: 2px solid var(--fr-blue);
    background: var(--fr-bg3);
  }}
  .footer-left {{
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .footer-slogan {{
    font-size: 11px;
    color: var(--fr-blue);
    font-weight: 600;
    letter-spacing: 1px;
  }}

  /* ========================================
     打印优化
     ======================================== */
  @media print {{
    body {{ padding: 0; background: white; }}
    .page {{ box-shadow: none; max-width: 100%; }}
    .section-nav {{ display: none; }}
  }}
</style>
</head>
<body>
<div class="page">

  <!-- ====== 页眉 ====== -->
  <div class="header-bar">
    <div class="header-left">
      <div class="header-title">{title}</div>
      {subtitle_html}
    </div>
    <div class="header-logo">
      {logo_header}
    </div>
  </div>
  <div class="header-line"></div>
{nav_html}
  <!-- ====== 内容区域 ====== -->
  <div class="content-area">
{content_block}
  </div>

  <!-- ====== 页脚 ====== -->
  <div class="footer-bar">
    <div class="footer-left">
      {logo_footer}
      <span class="footer-slogan">让数据成为生产力</span>
    </div>
  </div>

</div>
</body>
</html>'''
    
    # 写入文件
    with open(output, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 帆软主题 HTML 已生成: {output}")
    print(f"   标题: {title}")
    if subtitle:
        print(f"   副标题: {subtitle}")
    if sections:
        print(f"   章节: {', '.join(sections)}")
    print(f"   最大宽度: {max_width}px")
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="帆软 HTML 主题生成器")
    parser.add_argument("--title", required=True, help="页面标题")
    parser.add_argument("--subtitle", default="", help="页面副标题")
    parser.add_argument("--sections", default="", help="章节列表，逗号分隔")
    parser.add_argument("--output", default="report.html", help="输出文件名")
    parser.add_argument("--max-width", type=int, default=1400, help="最大宽度(px)")
    
    args = parser.parse_args()
    sections = [s.strip() for s in args.sections.split(",") if s.strip()] if args.sections else None
    
    generate_html(
        title=args.title,
        subtitle=args.subtitle,
        sections=sections,
        output=args.output,
        max_width=args.max_width
    )
