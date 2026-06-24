"""
腾讯会议开放平台 API 通用调用工具
鉴权方式: HMAC-SHA256 → hex → Base64(hex_string)
文档参考: https://meeting.tencent.com/support/topic/510/
签名步骤:
  1. headerString = "X-TC-Key={SecretId}&X-TC-Nonce={nonce}&X-TC-Timestamp={timestamp}"
  2. stringToSign = "{Method}\n{headerString}\n{URI}\n{body}"
  3. hexHash = HMAC-SHA256(SecretKey, stringToSign).hexdigest()
  4. signature = Base64(hexHash)
"""

import json
import hashlib
import hmac
import time
import random
import base64


def _build_signature(method, uri, body_str, secret_id, secret_key):
    """
    生成腾讯会议API签名
    
    注意: 每次调用必须生成新的 timestamp 和 nonce，
    否则会返回"请求重放错误"(error_code=190301)
    
    Args:
        method: HTTP方法 (GET/POST)
        uri: 请求URI，GET请求含完整查询串 (如 /v1/meetings?userid=xxx&instanceid=1)
        body_str: 请求体字符串，GET请求为空串 ""
        secret_id: SecretId (X-TC-Key的值)
        secret_key: SecretKey (签名密钥)
    
    Returns:
        dict: 包含所有必需请求头的字典
    """
    timestamp = str(int(time.time()))
    nonce = str(random.randint(100000, 999999))
    
    # Step 1: headerString - 参与签名的Header参数按字典序排列
    header_string = f"X-TC-Key={secret_id}&X-TC-Nonce={nonce}&X-TC-Timestamp={timestamp}"
    
    # Step 2: stringToSign
    string_to_sign = f"{method}\n{header_string}\n{uri}\n{body_str}"
    
    # Step 3: HMAC-SHA256 → hex
    hex_hash = hmac.new(
        secret_key.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    
    # Step 4: Base64(hex_string)
    signature = base64.b64encode(hex_hash.encode("utf-8")).decode("utf-8")
    
    return {
        "Content-Type": "application/json",
        "X-TC-Key": secret_id,
        "X-TC-Timestamp": timestamp,
        "X-TC-Nonce": nonce,
        "X-TC-Signature": signature,
    }


async def execute(ctx, method="GET", path="", query=None, body=None, userid="", **_kw):
    """
    执行腾讯会议 API 调用
    
    参数:
        method: HTTP方法 (GET/POST)
        path: API路径 (如 /v1/meetings, /v1/users/list)
        query: 查询参数 dict (GET请求)
        body: 请求体 dict (POST请求)
        userid: 腾讯会议userid (可选，默认用operator_id)
    
    常用API路径:
        - /v1/meetings: 查询用户会议列表 (GET, 参数: userid, instanceid, meeting_state)
        - /v1/users/list: 查询企业用户列表 (GET, 参数: page, size)
        - /v1/records/transcripts/paragraphs: 获取转写段落 (GET, 参数: meeting_id, record_file_id)
        - /v1/addresses/{record_file_id}: 获取智能纪要 (GET)
    """
    # 读取连接器凭证
    conn = ctx.connections.get("tencent_meeting")
    app_id = conn.field("app_id")
    sdk_id = conn.field("sdk_id")
    secret_id = conn.field("secret_id")
    secret_key = conn.field("secret_key")
    operator_id = conn.field("operator_id")
    
    # userid 默认使用 operator_id
    effective_userid = userid or operator_id
    
    # 构建URI和请求体
    method_upper = method.upper()
    
    if method_upper == "GET":
        # GET请求: URI含完整查询串
        params = dict(query or {})
        if "userid" not in params:
            params["userid"] = effective_userid
        
        # 按key排序拼接查询串
        sorted_params = sorted(params.items())
        query_string = "&".join(f"{k}={v}" for k, v in sorted_params)
        uri = f"{path}?{query_string}" if query_string else path
        body_str = ""
    else:
        # POST请求: URI不含查询串，body为JSON
        uri = path
        if body:
            body_str = json.dumps(body, separators=(',', ':'), ensure_ascii=False)
        else:
            body_str = ""
    
    # 生成签名头
    sig_headers = _build_signature(method_upper, uri, body_str, secret_id, secret_key)
    
    # 添加业务头
    sig_headers["AppId"] = app_id
    sig_headers["SdkId"] = sdk_id
    sig_headers["UserId"] = effective_userid
    sig_headers["X-TC-Registered"] = "1"
    
    # 构建完整URL
    base_url = "https://api.meeting.qq.com"
    url = f"{base_url}{uri}"
    
    ctx.log.info(f"TM API: {method_upper} {path} userid={effective_userid}")
    
    # 发送请求
    try:
        if method_upper == "GET":
            # GET请求: 直接用完整URL（参数已在URI中）
            resp = await ctx.http.get(url, headers=sig_headers)
        elif method_upper == "POST":
            # POST请求: 发送JSON body
            resp = await ctx.http.post(url, content=body_str.encode("utf-8"), headers=sig_headers)
        else:
            resp = await ctx.http.request(method_upper, url, headers=sig_headers)
        
        ctx.log.info(f"TM API response: {resp.status_code}")
        
        if resp.status_code >= 400:
            ctx.log.error(f"TM API error: {resp.status_code} {resp.text[:500]}")
            return f"API Error {resp.status_code}: {resp.text[:2000]}"
        
        # 解析响应
        try:
            data = resp.json()
            # 检查腾讯会议业务错误
            error_info = data.get("error_info", {})
            if error_info and error_info.get("error_code", 0) != 0:
                ctx.log.error(f"TM business error: {error_info}")
                return f"腾讯会议API业务错误: code={error_info.get('error_code')}, message={error_info.get('message')}"
            
            return json.dumps(data, ensure_ascii=False, indent=2)[:25000]
        except Exception:
            return resp.text[:5000]
            
    except Exception as e:
        ctx.log.error(f"TM API request failed: {e}")
        return f"请求失败: {str(e)}"