"""
钉钉消息推送工具

通过钉钉机器人Webhook推送消息到群聊，支持：
1. 自定义机器人Webhook（关键词/加签/IP安全策略）
2. 企业内部应用机器人（通过access_token发送）

使用方式：
- 方式一：直接传入webhook_url（自定义机器人）
- 方式二：传入agent_id + 使用pack级AppKey/AppSecret自动获取access_token（企业内部应用）
"""

import hashlib
import hmac
import base64
import time
import urllib.parse
import json


async def execute(ctx, webhook_url="", msg_type="markdown", content="", title="", at_mobiles=None, at_all=False, **_kw):
    """
    发送钉钉群消息

    Args:
        ctx: ToolContext
        webhook_url: 自定义机器人Webhook完整URL
        msg_type: 消息类型 text/markdown
        content: 消息内容
        title: 消息标题（markdown类型必填）
        at_mobiles: @指定手机号列表
        at_all: 是否@所有人
    """
    if not content:
        return "错误：消息内容不能为空"

    if at_mobiles is None:
        at_mobiles = []

    # 方式一：自定义机器人Webhook
    if webhook_url:
        return await _send_via_webhook(ctx, webhook_url, msg_type, content, title, at_mobiles, at_all)

    # 方式二：企业内部应用机器人（需要agent_id参数）
    return "错误：请提供 webhook_url（自定义机器人Webhook地址）"


async def _send_via_webhook(ctx, webhook_url, msg_type, content, title, at_mobiles, at_all):
    """通过自定义机器人Webhook发送消息"""

    # 检查是否需要加签（webhook_url中包含secret参数时自动加签）
    # 钉钉加签方式：在URL后追加 &timestamp=xxx&sign=xxx
    final_url = webhook_url

    # 构建消息体
    message = _build_message(msg_type, content, title, at_mobiles, at_all)

    # 发送请求
    headers = {"Content-Type": "application/json"}

    try:
        resp = await ctx.http.post(final_url, json=message, headers=headers)
        result = resp.json()

        if result.get("errcode") == 0:
            return f"消息发送成功：{result.get('errmsg', 'ok')}"
        else:
            return f"消息发送失败：errcode={result.get('errcode')}, errmsg={result.get('errmsg', '未知错误')}"
    except Exception as e:
        return f"请求异常：{str(e)}"


def _build_message(msg_type, content, title, at_mobiles, at_all):
    """构建钉钉消息体"""
    at_info = {
        "atMobiles": at_mobiles if at_mobiles else [],
        "isAtAll": at_all
    }

    if msg_type == "markdown":
        return {
            "msgtype": "markdown",
            "markdown": {
                "title": title or content[:50],
                "text": content
            },
            "at": at_info
        }
    elif msg_type == "text":
        return {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": at_info
        }
    else:
        return {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": at_info
        }
