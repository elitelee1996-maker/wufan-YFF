import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


async def execute(ctx, app_id, entry_id, data_id="", limit=10, fields=None, filter=None, max_records=0):
    """
    查询表单数据，支持两种模式：
    - 单次查询：传入 data_id 游标、limit，行为与原声明式工具完全一致
    - 自动分页全量拉取：设 limit=100 且 max_records=0（或指定上限），工具内部循环翻页直到取完
    
    自动分页触发条件：limit == 100 且 data_id 为空（首次调用且请求最大批量）
    其他情况退化为单次查询，与原工具行为完全一致。
    
    v5 API：app_id/entry_id 放在请求 body 中，URL 不含路径参数。
    """
    # 从 connection_credential 获取 API Key
    conn = ctx.connections.get("jiandaoyun")
    api_key = conn.field("api_key")
    if not api_key:
        return "ERROR: 未配置简道云 API Key，请通过连接中心配置 jiandaoyun 连接器"

    url = "https://api.jiandaoyun.com/api/v5/app/entry/data/list"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # 构建基础请求体（v5 格式：app_id/entry_id 在 body 中）
    def build_payload(cursor, batch_limit):
        payload = {
            "app_id": app_id,
            "entry_id": entry_id,
            "limit": batch_limit,
        }
        if cursor:
            payload["data_id"] = cursor
        if fields:
            payload["fields"] = fields
        if filter:
            payload["filter"] = filter
        return payload

    # ── 判断模式 ──────────────────────────────────────────────
    # 自动分页模式：limit=100 且首次调用（data_id 为空）
    auto_paginate = (limit == 100 and not data_id)

    if not auto_paginate:
        # ── 单次查询模式（与原声明式工具行为完全一致）──────────
        payload = build_payload(data_id, limit)
        resp = await ctx.http.post(url, headers=headers, json=payload)
        if resp.status_code != 200:
            return f"ERROR: HTTP {resp.status_code} — {resp.text[:300]}"
        result = resp.json()
        data = result.get("data", [])
        return {
            "data": data,
            "total_returned": len(data),
        }

    # ── 自动分页模式 ────────────────────────────────────────────
    all_records = []
    cursor = ""
    page = 0

    while True:
        page += 1
        await ctx.report_progress(f"正在拉取第 {page} 页数据（已获取 {len(all_records)} 条）...")

        payload = build_payload(cursor, 100)
        resp = await ctx.http.post(url, headers=headers, json=payload)

        if resp.status_code != 200:
            return (
                f"ERROR: 第 {page} 页请求失败 HTTP {resp.status_code} — {resp.text[:300]}\n"
                f"已成功获取 {len(all_records)} 条记录（不完整）"
            )

        batch = resp.json().get("data", [])
        all_records.extend(batch)

        # 检查 max_records 上限
        if max_records > 0 and len(all_records) >= max_records:
            all_records = all_records[:max_records]
            break

        # 不足 100 条说明已是最后一页
        if len(batch) < 100:
            break

        # 取最后一条 _id 作为下一页游标
        cursor = batch[-1]["_id"]

    await ctx.report_progress(f"全量拉取完成，共 {len(all_records)} 条", 100)

    return {
        "data": all_records,
        "total_returned": len(all_records),
        "pages_fetched": page,
    }