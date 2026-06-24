# OKR 系统通讯录集成与权限控制方案

## 一、架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                    简道云 iframe 嵌入                         │
│  URL 参数: ?username=jdy-xxx&userId=xxx                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   Bridge API 层 (Flask)                      │
│                                                              │
│  /api/auth/user     → 查询通讯录，返回用户完整信息            │
│  /api/okr/options   → 查询表单字段选项（周期/类型/状态）      │
│  /api/okr/goals     → 按用户权限过滤目标数据                  │
│  /api/okr/goal      → 写入目标（携带用户身份）                │
│  /api/okr/progress  → 更新进度（校验权限）                    │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     简道云 API                                │
│  通讯录 API / 表单数据 API / 权限 API                         │
└─────────────────────────────────────────────────────────────┘
```

## 二、用户身份识别

### 2.1 身份传递链路

```
简道云 iframe 嵌入
    ↓ URL 参数 ?username=jdy-xxx
Bridge API /api/auth/user?username=jdy-xxx
    ↓ 查询简道云通讯录
返回: {name, username, dept_no, dept_name, role, avatar}
    ↓
前端存储到 sessionStorage
    ↓
后续所有 API 请求携带 X-User-Name 头
```

### 2.2 身份验证流程

```python
# Bridge API 中间件
@app.before_request
def verify_user():
    username = request.headers.get('X-User-Name') or request.args.get('username')
    if not username:
        return jsonify({"error": "未识别用户身份"}), 401
    
    # 查询通讯录验证用户存在
    user_info = get_user_from_directory(username)
    if not user_info:
        return jsonify({"error": "用户不存在"}), 403
    
    g.current_user = user_info
```

### 2.3 无身份时的降级处理

- URL 无 username 参数 → 显示"请从简道云入口访问"提示
- 通讯录查不到 → 显示"用户未注册"提示
- 会话过期 → 重定向到简道云登录页

## 三、数据权限控制

### 3.1 权限矩阵

| 操作 | 权限规则 | 实现方式 |
|------|---------|---------|
| 查看自己的目标 | 仅看自己创建的 | filter: submitor = current_user |
| 查看上级目标 | 同部门 + 上级部门 | filter: dept_no IN (self_dept, parent_depts) |
| 查看团队目标 | 部门管理员可见 | 检查用户是否为部门负责人 |
| 创建目标 | 所有用户 | 自动填充 submitor = current_user |
| 更新进度 | 仅目标责任人 | 校验 KR 的 owner = current_user |
| 审批目标 | 上级负责人 | 检查目标树中 parent_goal 的 owner |

### 3.2 部门层级查询

```python
def get_dept_hierarchy(dept_no):
    """获取部门层级链：自己 → 上级 → 上上级 → ... → 根"""
    hierarchy = [dept_no]
    current = dept_no
    
    while current:
        parent = get_parent_dept(current)
        if parent:
            hierarchy.append(parent)
            current = parent
        else:
            break
    
    return hierarchy
```

### 3.3 目标可见性过滤

```python
@app.route("/api/okr/goals")
def list_user_goals():
    user = g.current_user
    
    # 基础过滤：只看自己的
    filter_cond = {
        "rel": "and",
        "cond": [
            {"field": "submitor", "method": "eq", 
             "value": [{"username": user['username']}]}
        ]
    }
    
    # 如果是部门负责人，可看本部门全部
    if user.get('is_dept_manager'):
        filter_cond = {
            "rel": "and",
            "cond": [
                {"field": "_widget_1778393571473", "method": "eq",
                 "value": [{"dept_no": user['dept_no']}]}
            ]
        }
    
    goals = jdy.list_data(FORMS["goal_tree"], limit=50, filter_cond=filter_cond)
    return jsonify({"goals": goals})
```

## 四、表单权限组同步

### 4.1 简道云权限组映射

| 简道云权限组 | Bridge API 角色 | 可见范围 |
|-------------|----------------|---------|
| OKR-普通员工 | employee | 仅自己 |
| OKR-部门负责人 | dept_manager | 本部门 |
| OKR-公司管理员 | admin | 全公司 |
| OKR-只读查看 | viewer | 只读 |

### 4.2 角色检测

```python
def detect_user_role(username):
    """根据简道云权限组判断用户角色"""
    # 查询用户在哪些权限组中
    groups = jdy.list_data(FORMS["permission_group"], 
        filter_cond={
            "rel": "and",
            "cond": [{"field": "member", "method": "contains",
                      "value": [{"username": username}]}]
        })
    
    group_names = [g.get('name') for g in groups]
    
    if 'OKR-公司管理员' in group_names:
        return 'admin'
    elif 'OKR-部门负责人' in group_names:
        return 'dept_manager'
    elif 'OKR-只读查看' in group_names:
        return 'viewer'
    else:
        return 'employee'
```

## 五、API 端点汇总

### 5.1 新增端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/auth/user` | GET | 查询当前用户信息 |
| `/api/auth/dept` | GET | 查询部门信息 |
| `/api/okr/options` | GET | 获取表单下拉选项 |
| `/api/okr/goals/upper` | GET | 获取上级目标链 |

### 5.2 现有端点增强

| 端点 | 增强内容 |
|------|---------|
| `/api/okr/goal` | 自动填充 submitor，校验用户身份 |
| `/api/okr/list` | 按用户权限过滤数据 |
| `/api/okr/progress` | 校验当前用户是否为 KR 责任人 |

## 六、安全约束

1. **不暴露其他用户数据**：API 返回结果中不包含非当前用户的敏感信息
2. **写操作校验**：所有写入操作必须校验当前用户有权操作该数据
3. **防越权**：用户不能通过修改参数访问超出权限的数据
4. **审计日志**：关键操作记录到简道云日志表单
