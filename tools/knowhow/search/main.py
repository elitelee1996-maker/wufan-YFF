import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

BASE_URL = "https://digitchat.fanruan.com/dataset"


async def execute(ctx, **params):
    """Search KnowHow knowledge base."""
    conn = ctx.connections.get("knowhow")
    api_key = conn.field("api_key")

    # Build retrieval_model
    retrieval_model = {}
    retrieval_model["business_domain"] = params.get("business_domain") or "project"
    retrieval_model["datasets"] = params.get("datasets") or "both"

    if "rerank_enable" in params and params["rerank_enable"] is not None:
        retrieval_model["rerank_enable"] = params["rerank_enable"]
    else:
        retrieval_model["rerank_enable"] = True

    retrieval_model["top_k"] = params.get("top_k") or 20

    if params.get("score_threshold") is not None:
        retrieval_model["score_threshold"] = params["score_threshold"]
    if params.get("vector_weight") is not None:
        retrieval_model["vector_weight"] = params["vector_weight"]
    if params.get("rerank_blend_weight") is not None:
        retrieval_model["rerank_blend_weight"] = params["rerank_blend_weight"]

    # Build metadata_filters
    metadata_filters = {}

    filter_map = {
        "filter_author": ("author", "equals"),
        "filter_quality": ("quality", "equals"),
        "filter_customer": ("customer", "equals"),
    }

    # String equality filters
    for param_key, (meta_key, op) in filter_map.items():
        if params.get(param_key):
            metadata_filters[meta_key] = {"value": params[param_key], "operator": op}

    # Array containsAny filters
    if params.get("filter_tags"):
        tags = params["filter_tags"]
        if isinstance(tags, str):
            tags = json.loads(tags)
        metadata_filters["tags"] = {"value": tags, "operator": "containsAny"}

    if params.get("filter_industry"):
        metadata_filters["industry"] = {
            "value": [params["filter_industry"]],
            "operator": "containsAny"
        }

    if params.get("filter_products"):
        metadata_filters["products"] = {
            "value": [params["filter_products"]],
            "operator": "containsAny"
        }

    if params.get("filter_node_path"):
        metadata_filters["node_path"] = {
            "value": [params["filter_node_path"]],
            "operator": "containsAny"
        }

    # Build request body
    body = {
        "query": params.get("query", ""),
        "retrieval_model": retrieval_model,
    }
    if metadata_filters:
        body["metadata_filters"] = metadata_filters

    # Send request
    url = f"{BASE_URL}/api/v1/retrieve"
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")

    req = Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        resp = urlopen(req, timeout=30)
        result = json.loads(resp.read().decode("utf-8"))
        return json.dumps(result, ensure_ascii=False, indent=2)
    except HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        return json.dumps(
            {"error": f"HTTP {e.code}", "detail": error_body},
            ensure_ascii=False,
            indent=2,
        )
