import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


async def execute(ctx, instance_id, username, task_id="", comment=""):
    api_key = ctx.connections.get("jiandaoyun").field("api_key")
    payload = {"instance_id": instance_id, "username": username}
    if task_id:
        payload["task_id"] = task_id
    if comment:
        payload["comment"] = comment
    resp = await ctx.http.post(
        "https://api.jiandaoyun.com/api/v2/workflow/task/revoke",
        json=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    )
    if resp.status_code != 200:
        return f"Error {resp.status_code}: {resp.text}"
    return resp.json()
