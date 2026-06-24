import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


async def execute(ctx, username, instance_id, task_id, flow_id=0, comment="", back_type=0):
    api_key = ctx.connections.get("jiandaoyun").field("api_key")
    
    payload = {"username": username, "instance_id": instance_id, "task_id": task_id}
    if flow_id is not None and flow_id != 0:
        payload["flow_id"] = int(flow_id)
    if comment:
        payload["comment"] = comment
    if back_type is not None and back_type != 0:
        payload["back_type"] = int(back_type)

    url = "https://api.jiandaoyun.com/api/v2/workflow/task/rollback"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    ctx.log.info(f"Request: POST {url}, payload={payload}")

    resp = await ctx.http.post(url, json=payload, headers=headers)

    ctx.log.info(f"Response: status={resp.status_code}, body={resp.text[:500] if resp.text else '(empty)'}")

    if resp.status_code != 200:
        error_detail = ""
        if resp.text:
            try:
                error_json = resp.json()
                code = error_json.get("code", "")
                message = error_json.get("message", "")
                status = error_json.get("status", "")
                parts = []
                if status:
                    parts.append(f"status={status}")
                if code:
                    parts.append(f"code={code}")
                if message:
                    parts.append(f"message={message}")
                if parts:
                    error_detail = ", ".join(parts)
                else:
                    error_detail = resp.text
            except Exception:
                error_detail = resp.text
        else:
            error_detail = "(empty response body)"

        return {
            "success": False,
            "http_status": resp.status_code,
            "error": error_detail,
            "request_payload": {k: v for k, v in payload.items() if k != "username"},
            "hint": "Check: 1) API Key has workflow rollback permission; 2) Flow node allows rollback; 3) Parameters are correct"
        }

    result = resp.json()
    return {"success": True, "data": result}
