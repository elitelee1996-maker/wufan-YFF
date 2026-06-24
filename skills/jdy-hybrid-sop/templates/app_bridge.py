"""Bridge模式Flask主应用模板 - 仅含基础设施，不含业务逻辑"""
import os
import logging
from flask import Flask, Blueprint, jsonify, send_from_directory

from jdy_client import JDYClient
from field_mapper import FieldMapper

# ---------------------------------------------------------------------------
# 配置加载
# ---------------------------------------------------------------------------
API_KEY = os.environ.get("JDY_API_KEY", "")
BASE_URL = os.environ.get("JDY_BASE_URL", "https://api.jiandaoyun.com")
APP_ID = os.environ.get("JDY_APP_ID", "")
MAPPING_PATH = os.environ.get("FIELD_MAPPING_PATH", "field_mapping.json")
STATIC_DIR = os.environ.get("STATIC_DIR", "static")
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "5000"))
DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 核心组件初始化
# ---------------------------------------------------------------------------
field_mapper = FieldMapper(mapping_path=MAPPING_PATH)
jdy_client = JDYClient(api_key=API_KEY, base_url=BASE_URL, app_id=APP_ID)

# ---------------------------------------------------------------------------
# Flask App & Blueprint
# ---------------------------------------------------------------------------
app = Flask(__name__, static_folder=None)  # 静态文件手动路由
api_bp = Blueprint("api", __name__, url_prefix="/api")


# ---------------------------------------------------------------------------
# 静态文件路由
# ---------------------------------------------------------------------------
@app.route("/")
def serve_index():
    """返回前端入口页面"""
    return send_from_directory(STATIC_DIR, "index.html")


@app.route("/<path:filename>")
def serve_static(filename: str):
    """提供静态资源"""
    return send_from_directory(STATIC_DIR, filename)


# ---------------------------------------------------------------------------
# 健康检查端点
# ---------------------------------------------------------------------------
@app.route("/health")
def health_check():
    """健康检查 - 供systemd/负载均衡器使用"""
    return jsonify({"status": "ok", "mode": "bridge"}), 200


# ---------------------------------------------------------------------------
# 错误处理器
# ---------------------------------------------------------------------------
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad Request", "message": str(error)}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found", "message": str(error)}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.exception("Internal server error")
    return jsonify({"error": "Internal Server Error"}), 500


# ---------------------------------------------------------------------------
# Blueprint注册（业务Blueprint在此处导入并注册）
# ---------------------------------------------------------------------------
# from routes.xxx import xxx_bp
# app.register_blueprint(xxx_bp)
app.register_blueprint(api_bp)

# ---------------------------------------------------------------------------
# 启动入口
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    logger.info("Starting Bridge mode on %s:%s", HOST, PORT)
    field_mapper.validate()
    app.run(host=HOST, port=PORT, debug=DEBUG)
