import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


async def execute(ctx, username, app_id="", entry_id="", skip=0, limit=10):
    api_key = ctx.connections.get("jiandaoyun").field("api_key")
    payload = {"username": username, "skip": skip, "limit": min(limit, 100)}
    if app_id:
        payload["app_id"] = app_id
    if entry_id:
        payload["entry_id"] = entry_id
    resp = await ctx.http.post(
        "https://api.jiandaoyun.com/api/v1/workflow/task/list",
        json=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    )
    if resp.status_code != 200:
        return f"Error {resp.status_code}: {resp.text}"
    return resp.json()
