import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


async def execute(ctx, username, skip=0, limit=10):
    api_key = ctx.connections.get("jiandaoyun").field("api_key")
    payload = {"username": username, "skip": skip, "limit": min(limit, 100)}
    resp = await ctx.http.post(
        "https://api.jiandaoyun.com/api/v1/workflow/cc/list",
        json=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    )
    if resp.status_code != 200:
        return f"Error {resp.status_code}: {resp.text}"
    return resp.json()
