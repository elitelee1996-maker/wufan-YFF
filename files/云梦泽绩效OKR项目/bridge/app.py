"""
OKR Bridge Service - Flask 版本（兼容 Python 3.6）
连接 HTML 页面与简道云表单
"""
import os
import json
import time
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

# ========== 配置 ==========
JDY_API_KEY = os.environ.get("JDY_API_KEY", "")
JDY_BASE_URL = "https://api.jiandaoyun.com/api/v5"
APP_ID = "6a2829aa42f13fb09f975991"

# 表单 entry_id
FORMS = {
    "goal_setting": "6a11148b53d55e801b934191",
    "goal_tree": "6a0021768032acf3d1f2ca30",
    "kr_setting": "6a00812ab6299729fbe8672c",
    "kr_list": "6a008c543a9e5537040237de",
    "kr_feedback": "6a042676d3de57c41216fd1b",
    "strategy": "6a096414dada5bef9edc2e11",
    "goal_list": "6a11166195e08fcde5d9f446",
    # 配置表（下拉选项数据源）
    "goal_type_config": "69ff58373d653593c585312e",   # 目标类型设置
    "goal_cycle_config": "6a002257a145e7ce97365ef8",  # 目标周期设置（周期类型枚举）
    "performance_cycle": "6a096375e74c918b35a5940d",  # 绩效周期（具体周期实例）
}

# ========== Flask App ==========
app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

@app.route('/')
def index():
    """首页 - 重定向到主页面"""
    return app.send_static_file('01-my-okr.html')

@app.route('/page/<filename>')
def serve_page(filename):
    """提供 HTML 页面访问"""
    if not filename.endswith('.html'):
        filename += '.html'
    return app.send_static_file(filename)


@app.route("/api/okr/options")
def get_okr_options():
    """从简道云配置表动态读取下拉选项"""
    try:
        # 1. 目标类型 → 从「目标类型设置」表读取
        type_records = jdy.list_data(FORMS["goal_type_config"], limit=100)
        goal_types = []
        for rec in type_records:
            name = rec.get("_widget_1778341942873", "")
            if name:
                goal_types.append(name)

        # 2. 绩效周期 → 从「绩效周期」表读取具体周期实例
        #    字段: _widget_1779002069643=周期名称, _widget_1779003956973=周期类型,
        #          _widget_1779002069657=绩效周期状态, _widget_1779002069647=开始日期,
        #          _widget_1779002069649=结束日期
        cycle_records = jdy.list_data(FORMS["performance_cycle"], limit=100)
        cycles = []
        for rec in cycle_records:
            name = rec.get("_widget_1779002069643", "")
            if name:
                cycles.append({
                    "value": name,
                    "label": name + (" (" + rec.get("_widget_1779003956973", "") + ")" if rec.get("_widget_1779003956973") else ""),
                    "id": rec.get("_id", ""),
                    "name": name,
                    "type": rec.get("_widget_1779003956973", ""),
                    "status": rec.get("_widget_1779002069657", ""),
                    "start": rec.get("_widget_1779002069647", ""),
                    "end": rec.get("_widget_1779002069649", ""),
                })

        # 3. 状态选项（固定，简道云中无独立配置表）
        statuses = ["草稿", "进行中", "已完成", "已关闭"]

        return jsonify({
            "goal_types": goal_types,
            "cycles": cycles,
            "statuses": statuses,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ========== JDY API Client ==========
class JDYClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "Authorization": "Bearer {}".format(api_key),
            "Content-Type": "application/json"
        }

    def _post(self, path, payload):
        url = "{}{}".format(JDY_BASE_URL, path)
        resp = requests.post(url, json=payload, headers=self.headers, timeout=30)
        if resp.status_code != 200:
            raise Exception("JDY API error: {} - {}".format(resp.status_code, resp.text))
        return resp.json()

    def create_data(self, entry_id, data):
        return self._post("/app/entry/data/create", {
            "app_id": APP_ID,
            "entry_id": entry_id,
            "data": data,
            "is_start_trigger": True
        })

    def update_data(self, entry_id, data_id, data):
        return self._post("/app/entry/data/update", {
            "app_id": APP_ID,
            "entry_id": entry_id,
            "data_id": data_id,
            "data": data,
            "is_start_trigger": True
        })

    def list_data(self, entry_id, limit=10, filter_cond=None):
        payload = {"app_id": APP_ID, "entry_id": entry_id, "limit": limit}
        if filter_cond:
            payload["filter"] = filter_cond
        result = self._post("/app/entry/data/list", payload)
        return result.get("data", [])

    def get_data(self, entry_id, data_id):
        result = self._post("/app/entry/data/get", {
            "app_id": APP_ID,
            "entry_id": entry_id,
            "data_id": data_id
        })
        return result.get("data", {})

    def get_widgets(self, entry_id):
        """获取表单字段列表及选项（combo/radio 等字段的 options）"""
        result = self._post("/app/entry/widget/list", {
            "app_id": APP_ID,
            "entry_id": entry_id
        })
        return result.get("widgets", [])

    def list_contacts(self):
        """查询简道云通讯录成员列表"""
        result = self._post("/app/contacts", {"app_id": APP_ID})
        return result.get("data", [])

    def list_departments(self, dept_no=1, has_child=True):
        """查询部门列表"""
        result = self._post("/corp/department/list", {
            "dept_no": dept_no,
            "has_child": has_child
        })
        return result.get("departments", [])

    def list_dept_users(self, dept_no=1, has_child=True):
        """查询部门成员列表"""
        result = self._post("/corp/department/user/list", {
            "dept_no": dept_no,
            "has_child": has_child
        })
        return result.get("users", [])

jdy = JDYClient(JDY_API_KEY)

# ========== Helper ==========
def v(value):
    """包装简道云字段值格式"""
    return {"value": value}

def now_iso():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")


def build_permission_filter(user_dept_no, user_username):
    """
    构建行级权限过滤条件
    - 公司级目标：所有人可见
    - 部门级/团队级目标：同部门可见
    - 个人级目标：仅本人可见
    """
    return {
        "rel": "or",
        "cond": [
            # 公司级目标：所有人可见
            {"field": "cate", "method": "eq", "value": "公司级目标"},
            # 部门级/团队级目标：同部门可见
            {"rel": "and", "cond": [
                {"field": "cate", "method": "in", "value": ["部门级目标", "团队级目标"]},
                {"field": "_widget_1778393571473", "method": "eq", "value": [{"dept_no": user_dept_no}]}
            ]},
            # 个人级目标：仅本人
            {"rel": "and", "cond": [
                {"field": "cate", "method": "eq", "value": "个人级目标"},
                {"field": "_widget_1687852504644", "method": "eq", "value": [{"username": user_username}]}
            ]}
        ]
    }

def safe_get(data, key, default=""):
    """安全获取字段值（处理 dict 和直接值两种格式）"""
    val = data.get(key, default)
    if isinstance(val, dict):
        return val.get("value", default)
    return val

# ========== API Endpoints ==========

@app.route("/health")
def health():
    return jsonify({"status": "ok", "app_id": APP_ID})

@app.route("/api/okr/goal", methods=["POST"])
def submit_goal():
    """
    提交目标制定 → 写入 4 张表：
    1. 目标制定（批次记录）
    2. 目标树（O 记录）
    3. KR设定（批次记录）
    4. KR列表（多条 KR 记录）
    """
    req = request.json
    results = {}
    fill_time = now_iso()

    # Step 1: 创建目标制定记录
    goal_setting_data = {
        "_widget_1778393571473": v({"dept_no": req.get("dept_no")}),
        "_widget_1687852504644": v({"username": req.get("owner_username")}),
        "_widget_1778321965043": v(req.get("goal_type")),
        "_widget_1778393571477": v(req.get("cycle")),
        "_widget_1687852504646": v(req.get("year")),
        "_widget_1687852504651": v(fill_time),
        "_widget_1688022155570": v(req.get("start_date")),
        "_widget_1688022155571": v(req.get("end_date")),
    }
    gs_result = jdy.create_data(FORMS["goal_setting"], goal_setting_data)
    gs_id = gs_result.get("data", {}).get("_id", "")
    results["goal_setting_id"] = gs_id
    time.sleep(0.1)

    # Step 2: 创建目标树记录（O）
    goal_tree_data = {
        "_widget_1778393571473": v({"dept_no": req.get("dept_no")}),
        "_widget_1687852504644": v({"username": req.get("owner_username")}),
        "_widget_1778321965043": v(req.get("goal_type")),
        "_widget_1778393571477": v(req.get("cycle")),
        "_widget_1687852504646": v(req.get("year")),
        "_widget_1687852504651": v(fill_time),
        "_widget_1688022155570": v(req.get("start_date")),
        "_widget_1688022155571": v(req.get("end_date")),
        "_widget_1778393738999": v("草稿"),
        "_widget_1778342107843": v(req.get("objective_name")),  # 当前目标字段
        "_widget_1779454389522": v(req.get("objective_name")),  # 战略标题字段（读取时用这个）
        "_widget_1779502600094": v(req.get("weight", 1.0)),
        "_widget_1778342107844": v(req.get("objective_desc", "")),
        "_widget_1780649802079": v(0),
    }
    # 上级目标对齐
    if req.get("parent_goal_id"):
        goal_tree_data["_widget_1778342107846"] = v(req.get("parent_goal_id"))
    if req.get("parent_goal_name"):
        goal_tree_data["_widget_1778342107848"] = v(req.get("parent_goal_name"))
    if req.get("parent_goal_desc"):
        goal_tree_data["_widget_1778342107849"] = v(req.get("parent_goal_desc"))
    # 战略对齐
    if req.get("strategy_id"):
        goal_tree_data["_widget_1779454389520"] = v(req.get("strategy_id"))
    if req.get("strategy_no"):
        goal_tree_data["_widget_1779454389521"] = v(req.get("strategy_no"))
    if req.get("strategy_title"):
        goal_tree_data["_widget_1779454389522"] = v(req.get("strategy_title"))

    gt_result = jdy.create_data(FORMS["goal_tree"], goal_tree_data)
    gt_id = gt_result.get("data", {}).get("_id", "")
    gt_sn = gt_result.get("data", {}).get("_widget_1778418029462", "")
    results["goal_tree_id"] = gt_id
    results["goal_tree_sn"] = gt_sn
    time.sleep(0.1)

    # Step 3: 创建 KR设定记录
    krs = req.get("krs", [])
    if krs:
        kr_setting_data = {
            "_widget_1778417962277": v(gt_id),  # 关联目标树
            "_widget_1778417962278": v({"dept_no": req.get("dept_no")}),
            "_widget_1778417962279": v({"username": req.get("owner_username")}),
            "_widget_1778417962280": v(req.get("goal_type")),
            "_widget_1778417962282": v(req.get("cycle")),
            "_widget_1778417962284": v(req.get("year")),
            "_widget_1778417962285": v(req.get("start_date")),
            "_widget_1778417962286": v(req.get("end_date")),
        }
        ks_result = jdy.create_data(FORMS["kr_setting"], kr_setting_data)
        ks_id = ks_result.get("data", {}).get("_id", "")
        results["kr_setting_id"] = ks_id
        time.sleep(0.1)

        # Step 4: 循环单条创建 KR列表记录（避免批量权限问题）
        kr_ids = []
        for kr in krs:
            kr_data = {
                "_widget_1779772785343": v("草稿"),
                "_widget_1779720494053": v(req.get("cycle")),
                "_widget_1779720494054": v(req.get("year")),
                "_widget_1779720494055": v(req.get("start_date")),
                "_widget_1779720494056": v(req.get("end_date")),
                "_widget_1778417962321": v(ks_id),       # 关联KR设定
                "_widget_1779711624595": v(gt_id),       # 关联目标树
                "_widget_1779772097599": v({"dept_no": req.get("dept_no")}),
                "_widget_1778420820819": v({"username": req.get("owner_username")}),
                "_widget_1778420820820": v(req.get("objective_name")),
                "_widget_1779724399008": v(req.get("goal_type")),
                "_widget_1778420820821": v(req.get("objective_desc", "")),
                "_widget_1778420820822": v(kr.get("name", "")),
                "_widget_1778420820825": v(kr.get("detail", "")),
                "_widget_1779707806167": v(str(kr.get("start_value", "0"))),
                "_widget_1779707806166": v(str(kr.get("target_value", ""))),
                "_widget_1778423297961": v(kr.get("weight", 0)),
                "_widget_1780474043464": v(0),
                "_widget_1780544598681": v(0),
                "_widget_1780545251576": v(fill_time),
            }
            kr_result = jdy.create_data(FORMS["kr_list"], kr_data)
            kr_id = kr_result.get("data", {}).get("_id", "")
            kr_ids.append(kr_id)
            time.sleep(0.1)
        
        results["kr_count"] = len(kr_ids)
        results["kr_ids"] = kr_ids

    return jsonify({"success": True, "results": results})


@app.route("/api/okr/progress", methods=["POST"])
def update_progress():
    """
    提交进度更新 → 写入 KR过程反馈
    """
    req = request.json
    kr_data_id = req.get("kr_data_id")
    current_progress = req.get("current_progress", 0)
    progress_desc = req.get("progress_desc", "")

    # 先读取 KR 信息
    kr_data = jdy.get_data(FORMS["kr_list"], kr_data_id)
    
    # 创建 KR过程反馈
    feedback_data = {
        "_widget_1778656964739": v(kr_data_id),  # 关联KR
        "_widget_1778656964740": v(kr_data.get("_widget_1778420820819", {})),  # 目标责任人
        "_widget_1778656964741": v(safe_get(kr_data, "_widget_1778420820820")),  # 当前目标
        "_widget_1778656964742": v(safe_get(kr_data, "_widget_1778420820822")),  # KR名称
        "_widget_1779720108327": v(now_iso()),
        "_widget_1778420820821": v(progress_desc),
        "_widget_1780474000349": v(current_progress),
    }
    fb_result = jdy.create_data(FORMS["kr_feedback"], feedback_data)
    time.sleep(0.1)

    return jsonify({
        "success": True,
        "feedback_id": fb_result.get("data", {}).get("_id", ""),
        "message": "进度已更新至 {:.0f}%".format(current_progress * 100)
    })


@app.route("/api/okr/list")
def list_okr():
    """查询 OKR 数据（目标树 + KR列表），带行级权限过滤"""
    owner_username = request.args.get("owner_username", "")
    cycle = request.args.get("cycle", "")
    # 权限过滤所需参数
    user_dept_no = request.args.get("user_dept_no", "")
    user_username = request.args.get("user_username", owner_username)

    # 构建过滤条件
    and_conds = []
    
    # 权限过滤（必须）
    if user_dept_no and user_username:
        perm_filter = build_permission_filter(user_dept_no, user_username)
        and_conds.append(perm_filter)
    
    if owner_username:
        and_conds.append({
            "field": "_widget_1687852504644",
            "method": "eq",
            "value": [{"username": owner_username}]
        })
    if cycle:
        and_conds.append({
            "field": "_widget_1778393571477",
            "method": "eq",
            "value": cycle
        })

    filter_cond = {"rel": "and", "cond": and_conds} if and_conds else None
    goals = jdy.list_data(FORMS["goal_tree"], limit=50, filter_cond=filter_cond)
    
    # 批量获取所有 KR（一次性查询）
    all_krs = jdy.list_data(FORMS["kr_list"], limit=100, filter_cond=None)
    
    # 按目标 ID 分组 KR
    kr_map = {}
    for kr in all_krs:
        goal_id = safe_get(kr, "_widget_1779711624595")
        if goal_id not in kr_map:
            kr_map[goal_id] = []
        kr_map[goal_id].append(kr)
    
    result = []
    for g in goals:
        goal_id = g.get("_id")
        creator = g.get("creator", {})
        goal_info = {
            "id": goal_id,
            "sn": g.get("_widget_1778418029462", ""),
            "name": safe_get(g, "_widget_1778342107843") or safe_get(g, "_widget_1779454389522") or "",
            "desc": safe_get(g, "_widget_1778342107844"),
            "cate": safe_get(g, "_widget_1778321965043"),
            "goal_type": safe_get(g, "_widget_1778321965043"),
            "parent_id": safe_get(g, "_widget_1778342107846"),
            "status": safe_get(g, "_widget_1778393738999"),
            "weight": safe_get(g, "_widget_1779502600094", 0),
            "progress": safe_get(g, "_widget_1780649802079", 0),
            "cycle": safe_get(g, "_widget_1778393571477"),
            "owner_name": creator.get("name", ""),
            "strategy_no": safe_get(g, "_widget_1779454389521"),
            "strategy_title": safe_get(g, "_widget_1779454389522"),
            "krs": []
        }
        
        # 从预加载的 KR 中获取
        krs = kr_map.get(goal_id, [])
        for kr in krs:
            kr_info = {
                "id": kr.get("_id"),
                "name": safe_get(kr, "_widget_1778420820822"),
                "detail": safe_get(kr, "_widget_1778420820825"),
                "start_value": safe_get(kr, "_widget_1779707806167"),
                "target_value": safe_get(kr, "_widget_1779707806166"),
                "weight": safe_get(kr, "_widget_1778423297961", 0),
                "progress": safe_get(kr, "_widget_1780474043464", 0),
                "status": safe_get(kr, "_widget_1779772785343"),
            }
            goal_info["krs"].append(kr_info)
        
        result.append(goal_info)

    return jsonify({"goals": result, "total": len(result)})


@app.route("/api/okr/strategy")
def list_strategy():
    """查询战略解码列表"""
    cycle = request.args.get("cycle", "")
    
    filter_cond = None
    if cycle:
        filter_cond = {"rel": "and", "cond": [
            {"field": "_widget_1779445346267", "method": "eq", "value": cycle}
        ]}
    
    strategies = jdy.list_data(FORMS["strategy"], limit=50, filter_cond=filter_cond)
    result = []
    for s in strategies:
        result.append({
            "id": s.get("_id"),
            "sn": s.get("_widget_1779445346264", ""),
            "title": safe_get(s, "_widget_1779445346265"),
            "content": safe_get(s, "_widget_1779445346266"),
            "level": safe_get(s, "_widget_1779445346271"),
            "weight": safe_get(s, "_widget_1779445346275", 0),
        })
    return jsonify({"strategies": result, "total": len(result)})


# ========== New API Endpoints ==========

@app.route("/api/auth/user")
def get_user():
    """根据 URL 参数 username 查询用户信息（优先从通讯录 API，降级到表单数据）"""
    username = request.args.get("username", "")
    if not username:
        return jsonify({"error": "username parameter is required"}), 400

    try:
        # 优先尝试从通讯录 API 获取用户信息
        try:
            contacts = jdy.list_contacts()
            
            # 在通讯录中查找该用户
            for contact in contacts:
                if contact.get("username") == username:
                    dept_info = contact.get("departments", [])
                    dept_no = dept_info[0] if dept_info else ""
                    dept_name = contact.get("dept_name", "")
                    
                    # 如果通讯录没有返回部门名称，尝试从部门列表获取
                    if not dept_name and dept_no:
                        depts = contact.get("departments_detail", [])
                        if depts and len(depts) > 0:
                            dept_name = depts[0].get("name", "")
                    
                    return jsonify({
                        "username": contact.get("username", username),
                        "name": contact.get("name", ""),
                        "dept_no": str(dept_no) if dept_no else "",
                        "dept_name": dept_name,
                        "role": "employee",
                    })
        except Exception as e:
            # 通讯录 API 失败，降级到表单数据方式
            print("通讯录 API 失败，降级处理:", str(e))
            pass
        
        # 降级：从目标树表单查询该用户创建的数据，提取 creator 信息
        filter_cond = {
            "rel": "and",
            "cond": [
                {"field": "submitor", "method": "eq",
                 "value": [{"username": username}]}
            ]
        }
        records = jdy.list_data(FORMS["goal_tree"], limit=1, filter_cond=filter_cond)

        if records:
            creator = records[0].get("creator", {})
            dept_info = creator.get("departments", [])
            dept_no = dept_info[0] if dept_info else ""
            return jsonify({
                "username": creator.get("username", username),
                "name": creator.get("name", ""),
                "dept_no": str(dept_no) if dept_no else "",
                "dept_name": "",
                "role": "employee",
            })

        return jsonify({"error": "user not found", "username": username}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/auth/users")
def list_users():
    """查询通讯录成员列表（降级到表单数据）"""
    try:
        # 优先尝试通讯录 API
        try:
            contacts = jdy.list_contacts()
            users = []
            for c in contacts:
                dept_info = c.get("departments", [])
                dept_no = dept_info[0] if dept_info else ""
                dept_name = c.get("dept_name", "")
                
                users.append({
                    "username": c.get("username", ""),
                    "name": c.get("name", ""),
                    "dept_no": str(dept_no) if dept_no else "",
                    "dept_name": dept_name,
                })
            
            return jsonify({"users": users, "total": len(users)})
        except Exception as e:
            # 通讯录 API 失败，降级到表单数据
            print("通讯录 API 失败，降级处理:", str(e))
            pass
        
        # 降级：从目标树表单提取所有创建者信息
        all_records = jdy.list_data(FORMS["goal_tree"], limit=100)
        users_map = {}
        for rec in all_records:
            creator = rec.get("creator", {})
            username = creator.get("username", "")
            if username and username not in users_map:
                dept_info = creator.get("departments", [])
                dept_no = dept_info[0] if dept_info else ""
                users_map[username] = {
                    "username": username,
                    "name": creator.get("name", ""),
                    "dept_no": str(dept_no) if dept_no else "",
                    "dept_name": "",
                }
        
        users = list(users_map.values())
        return jsonify({"users": users, "total": len(users)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def _extract_widget_options(widget):
    """从 widget 定义中提取 options，兼容多种返回格式"""
    # 格式1: 顶层 options（部分 API 版本）
    opts = widget.get("options", [])
    if opts:
        return opts
    # 格式2: props.options（简道云 v5 API 标准格式）
    props = widget.get("props", {})
    if isinstance(props, dict):
        opts = props.get("options", [])
        if opts:
            return opts
    # 格式3: config.options
    config = widget.get("config", {})
    if isinstance(config, dict):
        opts = config.get("options", [])
        if opts:
            return opts
    return []


@app.route("/api/okr/goals/upper")
def get_upper_goals():
    """查询上级目标链：同部门的公司级/部门级/团队级目标，带行级权限过滤"""
    username = request.args.get("username", "")
    dept_no = request.args.get("dept_no", "")
    cycle = request.args.get("cycle", "")
    year = request.args.get("year", "")

    if not dept_no:
        return jsonify({"error": "dept_no parameter is required"}), 400

    try:
        # 权限过滤：公司级 + 同部门的部门级/团队级
        perm_filter = build_permission_filter(dept_no, username)
        
        conds = [
            perm_filter,
            {
                "field": "cate",
                "method": "in",
                "value": ["公司级目标", "部门级目标", "团队级目标"]
            }
        ]
        # 可选过滤条件
        if cycle:
            conds.append({"field": "_widget_1778393571477", "method": "eq", "value": cycle})
        if year:
            conds.append({"field": "year", "method": "eq", "value": year})

        filter_cond = {"rel": "and", "cond": conds}
        goals = jdy.list_data(FORMS["goal_tree"], limit=50, filter_cond=filter_cond)

        # 提取 owner 信息
        # 注意：cate/name/desc/year/id/id_parent 是顶层字段，不是 _widget_xxx
        result = []
        for g in goals:
            creator = g.get("creator", {})
            owner_name = creator.get("name", "")
            result.append({
                "id": g.get("_id"),
                "sn": safe_get(g, "_widget_1778418029462"),
                "name": g.get("name") or safe_get(g, "_widget_1779454389522") or "",
                "desc": g.get("desc") or "",
                "cate": g.get("cate"),
                "goal_type": g.get("cate"),
                "cycle": safe_get(g, "_widget_1778393571477"),
                "year": g.get("year"),
                "status": safe_get(g, "_widget_1778393738999"),
                "weight": safe_get(g, "_widget_1779502600094", 0),
                "progress": safe_get(g, "_widget_1780649802079", 0),
                "parent_id": g.get("id_parent") or safe_get(g, "_widget_1778342107846"),
                "parent_text": safe_get(g, "_widget_1778342107848") or "",
                "related_id": safe_get(g, "_widget_1779454389520"),
                "related_title": safe_get(g, "_widget_1779454389522") or "",
                "owner_name": owner_name,
            })

        # 构建树形结构：公司级 → 部门级 → 团队级
        company_goals = [g for g in result if g["cate"] == "公司级目标"]
        dept_goals = [g for g in result if g["cate"] == "部门级目标"]
        team_goals = [g for g in result if g["cate"] == "团队级目标"]
        other_goals = [g for g in result if g["cate"] not in ("公司级目标", "部门级目标", "团队级目标")]

        # 已挂载的 team goal ID 集合
        mounted_team_ids = set()

        # 为每个部门级目标挂载子目标
        tree = []
        for dg in dept_goals:
            children = [tg for tg in team_goals if tg.get("parent_id") == dg["id"]]
            for c in children:
                mounted_team_ids.add(c["id"])
            tree.append({**dg, "children": children})

        # 孤儿团队目标（没有 parent_id 或 parent 不在当前结果集中）挂到第一个部门下
        orphan_teams = [tg for tg in team_goals if tg["id"] not in mounted_team_ids]
        if orphan_teams and tree:
            tree[0]["children"].extend(orphan_teams)
        elif orphan_teams:
            # 没有部门级目标时，作为独立节点
            for ot in orphan_teams:
                tree.append({**ot, "children": []})

        # 公司级目标放在最前面
        for cg in company_goals:
            tree.insert(0, {**cg, "children": []})

        return jsonify({"tree": tree, "total": len(result), "dept_count": len(dept_goals), "team_count": len(team_goals)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ========== Org Tree (通讯录) ==========

@app.route("/api/okr/org-tree")
def get_org_tree():
    """获取组织架构树：部门 + 成员"""
    try:
        # 1. 获取所有子部门（list_departments 返回的是子部门，不包含指定部门本身）
        departments = jdy.list_departments(dept_no=1, has_child=True)

        # 2. 获取所有成员
        users = jdy.list_dept_users(dept_no=1, has_child=True)

        # 3. 从子部门推断根部门信息（parent_no=1 的部门，其父就是根部门）
        root_dept_no = 1
        root_dept_name = "公司"
        if departments:
            # 找到任意一个 parent_no=1 的子部门，推断根部门
            for d in departments:
                if d.get("parent_no") == 1:
                    root_dept_no = 1
                    break

        # 4. 构建部门树（包含根部门）
        dept_map = {}
        # 先添加根部门
        dept_map[root_dept_no] = {
            "dept_no": root_dept_no,
            "name": root_dept_name,
            "parent_no": 0,
            "children": [],
            "members": []
        }
        # 再添加所有子部门
        for d in departments:
            dept_map[d["dept_no"]] = {
                "dept_no": d["dept_no"],
                "name": d.get("name", ""),
                "parent_no": d.get("parent_no", 0),
                "children": [],
                "members": []
            }

        # 5. 挂载子部门
        for d in departments:
            node = dept_map[d["dept_no"]]
            parent_no = d.get("parent_no", 0)
            if parent_no in dept_map:
                dept_map[parent_no]["children"].append(node)

        # 6. 挂载成员到部门
        for u in users:
            user_depts = u.get("departments", [])
            user_info = {
                "username": u.get("username", ""),
                "name": u.get("name", ""),
                "type": u.get("type", 0),
                "status": u.get("status", 0)
            }
            for dept_no in user_depts:
                if dept_no in dept_map:
                    dept_map[dept_no]["members"].append(user_info)

        # 7. 返回以根部门为起点的树
        roots = [dept_map[root_dept_no]]
        return jsonify({"departments": roots, "users": users})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8200, debug=False)
