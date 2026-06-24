import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


async def execute(ctx, app_id, entry_id, data_id, skip=0, limit=100):
    api_key = ctx.connections.get("jiandaoyun").field("api_key")
    payload = {"skip": skip, "limit": min(limit, 100)}
    resp = await ctx.http.post(
        f"https://api.jiandaoyun.com/api/v1/app/{app_id}/entry/{entry_id}/data/{data_id}/approval_comments",
        json=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    )
    if resp.status_code != 200:
        return f"Error {resp.status_code}: {resp.text}"
    return resp.json()
