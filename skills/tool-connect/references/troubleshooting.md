# 常见错误与排查

| 错误信息 | 原因 | 解决方式 |
|---------|------|---------|
| CoreX 工具执行超时 | 脚本执行时间超过 timeout 配置 | 增大 tool.json 的 `timeout`，或优化脚本逻辑 |
| CoreX 工具内存溢出 | 脚本分配了过多内存 | 减少一次性加载的数据量，分批处理 |
| CoreX 工具缺少 Python 依赖 | dependencies 中声明的包未安装 | 联系管理员在服务端安装 |
| 该工具尚未完成连接配置 | `requires_connections` 声明的连接器未连接 | 用 `connection_credential(action="request", slug=...)` 弹出连接卡,或让用户到"设置 → 连接中心"配置 |
| MissingConnectionField(key=..., owner_level=...) | 连接器存在但某字段缺失 | owner_level=team 需管理员补;owner_level=user 需用户补(走 `connection_credential(action="request")`) |
| Error: tool 'xxx' not found | call_tool 调用了不存在的工具 | 检查工具名拼写，确认工具已注册 |
| main.py must define 'execute' | main.py 没有定义 execute 函数 | 确保 main.py 定义了 `async def execute(ctx, **params)` 或 `def execute(ctx, **params)` |
| ModuleNotFoundError: No module named 'lib.xxx' | lib/ 子模块缺少 \_\_init\_\_.py | 确保 `lib/__init__.py` 存在（内容可为空） |
| sys.exit() 不允许 | main.py 中调用了 sys.exit() | 改为 return 返回结果 |
| API Error 401 / 403 | API 密钥无效或权限不足 | 检查密钥是否正确配置、是否过期、scope 是否匹配 |
| 连接超时 | 目标 API 不可达 | 检查 URL 是否正确、网络是否可达、timeout 是否过短 |
| CLI command not found | CLI 工具未安装 | 用 bash 安装对应的 CLI（如 `npm install -g @larksuite/cli`） |
