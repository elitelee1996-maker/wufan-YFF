import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


async def execute(ctx, username, instance_id, task_id, sign_user_names, sign_type="after", comment=""):
    api_key = ctx.connections.get("jiandaoyun").field("api_key")
    # Map sign_type string to API number: 0=前加签, 1=后加签, 2=并加签
    type_map = {"before": 0, "after": 1, "parallel": 2}
    add_sign_type = type_map.get(sign_type, 1)
    # API expects a single string, take the first username from the array
    add_sign_username = sign_user_names[0] if isinstance(sign_user_names, list) else sign_user_names
    payload = {
        "username": username,
        "instance_id": instance_id,
        "task_id": task_id,
        "add_sign_username": add_sign_username,
        "add_sign_type": add_sign_type
    }
    if comment:
        payload["comment"] = comment
    resp = await ctx.http.post(
        "https://api.jiandaoyun.com/api/v1/workflow/task/add_sign",
        json=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    )
    if resp.status_code != 200:
        return f"Error {resp.status_code}: {resp.text}"
    return resp.json()
