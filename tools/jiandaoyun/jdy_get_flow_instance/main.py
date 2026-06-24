import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


async def execute(ctx, instance_id):
    api_key = ctx.connections.get("jiandaoyun").field("api_key")
    resp = await ctx.http.post(
        "https://api.jiandaoyun.com/api/v1/workflow/instance/get",
        json={"instance_id": instance_id},
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    )
    if resp.status_code != 200:
        return f"Error {resp.status_code}: {resp.text}"
    return resp.json()
