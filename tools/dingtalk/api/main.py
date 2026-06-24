"""
钉钉开放平台API通用调用工具

自动管理access_token（缓存7200秒有效期），支持所有钉钉v2 API。
认证方式：AppKey + AppSecret → access_token → x-acs-token header
"""

import json
import time


async def execute(ctx, method="POST", api_path="", query=None, body=None, **_kw):
    """
    调用钉钉开放平台API

    Args:
        ctx: ToolContext
        method: HTTP方法 GET/POST
        api_path: API路径，如 /topapi/message/corpconversation/asyncsend_v2
        query: 查询参数
        body: 请求体
    """
    if not api_path:
        return "错误：请提供 api_path（钉钉API路径）"

    if query is None:
        query = {}
    if body is None:
        body = {}

    # 获取密钥
    app_key = ctx.secrets.get("DINGTALK_APP_KEY", "")
    app_secret = ctx.secrets.get("DINGTALK_APP_SECRET", "")

    if not app_key or not app_secret:
        return "错误：请先配置钉钉 AppKey 和 AppSecret（在密钥配置面板中填写）"

    # 获取access_token（带缓存）
    access_token = await _get_access_token(ctx, app_key, app_secret)
    if not access_token:
        return "错误：获取access_token失败，请检查AppKey和AppSecret是否正确"

    # 构建请求
    base_url = "https://oapi.dingtalk.com"
    # v2新版API使用不同base_url
    if api_path.startswith("/v1.0") or api_path.startswith("/v2.0"):
        base_url = "https://api.dingtalk.com"

    url = f"{base_url}{api_path}"

    headers = {
        "x-acs-token": access_token,
        "Content-Type": "application/json",
    }

    try:
        if method.upper() == "GET":
            resp = await ctx.http.get(url, params=query, headers=headers)
        else:
            # 钉钉旧版API用query传参，新版API用body传参
            if api_path.startswith("/v1.0") or api_path.startswith("/v2.0"):
                resp = await ctx.http.post(url, params=query, json=body, headers=headers)
            else:
                # 旧版topapi通常用query传参
                merged_query = {**query, **body}
                resp = await ctx.http.post(url, params=merged_query, headers=headers)

        try:
            data = resp.json()
            return json.dumps(data, ensure_ascii=False, indent=2)[:25000]
        except Exception:
            return resp.text[:5000]
    except Exception as e:
        return f"请求异常：{str(e)}"


async def _get_access_token(ctx, app_key, app_secret):
    """获取钉钉access_token，带缓存（有效期7200秒）"""

    # 检查缓存
    cache_key = "dingtalk_access_token"
    cache_time_key = "dingtalk_token_time"

    if cache_key in ctx.cache:
        token_time = ctx.cache.get(cache_time_key, 0)
        # token有效期7200秒，提前5分钟刷新
        if time.time() - token_time < 7200 - 300:
            return ctx.cache[cache_key]

    # 请求新token
    url = "https://oapi.dingtalk.com/gettoken"
    params = {
        "appkey": app_key,
        "appsecret": app_secret,
    }

    try:
        resp = await ctx.http.get(url, params=params)
        data = resp.json()

        if data.get("errcode") == 0:
            token = data.get("access_token", "")
            ctx.cache[cache_key] = token
            ctx.cache[cache_time_key] = time.time()
            return token
        else:
            ctx.log.warning(f"获取access_token失败: errcode={data.get('errcode')}, errmsg={data.get('errmsg')}")
            return None
    except Exception as e:
        ctx.log.warning(f"获取access_token异常: {str(e)}")
        return None