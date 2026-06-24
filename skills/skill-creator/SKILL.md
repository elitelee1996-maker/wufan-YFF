---
name: 技能创建
description: 技能创建与安装指南。当用户想要创建新技能、安装外部技能或更新现有技能来扩展 Agent 的能力时使用此技能，包括专业知识、工作流程或工具集成。
---

# 技能创建器

本技能提供创建和安装高效技能的指南。

## 关于技能

技能是模块化、自包含的知识包，通过提供专业知识、工作流程和工具来扩展 Agent 的能力。它们将通用 Agent 转变为配备程序性知识的专业 Agent。

### 技能提供什么

1. 专业工作流程 - 特定领域的多步骤程序
2. 工具集成 - 使用特定文件格式或 API 的说明
3. 领域专业知识 - 公司特定知识、数据模式、业务逻辑
4. 捆绑资源 - 用于复杂和重复任务的脚本、参考文档和素材

## 核心原则

### 简洁至关重要

上下文窗口是公共资源。**默认假设：Agent 已经非常聪明。** 只添加 Agent 尚未具备的上下文。优先使用简洁的示例而非冗长的解释。

### 设置适当的自由度

- **高自由度（文本指令）**：多种方法都有效时
- **中等自由度（伪代码或带参数的脚本）**：有首选模式但允许变化时
- **低自由度（特定脚本）**：操作脆弱且容易出错时

### 技能结构

```
skill-name/
├── SKILL.md（必需）
│   ├── YAML 前置元数据（name + description，必需）
│   └── Markdown 说明（必需）
└── 捆绑资源（可选）
    ├── scripts/          - 可执行代码（Python/Bash 等）
    ├── references/       - 需要时加载到上下文的文档
    └── assets/           - 用于输出的文件（模板、图标等）
```

所有技能统一存储在 `skills/` 目录下。目录名必须使用小写字母、数字和连字符（如 `my-skill-name`）。

### 渐进式披露

1. **元数据（name + description）** - 始终在上下文中（约 100 字）
2. **SKILL.md 正文** - 技能触发时加载（<5k 字）
3. **捆绑资源** - Agent 按需加载

保持 SKILL.md 正文精简，控制在 500 行以内。接近限制时将内容拆分到 `references/` 目录。

## 技能创建流程

1. 通过具体示例理解技能
2. 规划可复用的技能内容
3. 初始化技能
4. 编辑技能
5. 根据实际使用迭代

### 步骤 1：通过具体示例理解技能

要创建有效的技能，需要清楚理解技能将如何使用的具体示例。例如：

- "技能应支持哪些功能？"
- "能给出一些使用示例吗？"
- "用户说什么应该触发此技能？"

避免在单条消息中提出过多问题。当对技能应支持的功能有清晰认识时，结束此步骤。

### 步骤 2：规划可复用的技能内容

分析每个示例，识别哪些脚本、参考文档和素材会对重复使用有帮助：

- 每次都需要重写的代码 → `scripts/` 中的脚本
- Agent 工作时需要参考的信息 → `references/` 中的文档
- 输出所需的模板和素材 → `assets/` 中的文件

### 步骤 3：初始化技能

从头创建新技能时，运行初始化脚本：

```bash
python skills/skill-creator/scripts/init_skill.py <skill-name>
```

脚本会在 `skills/<skill-name>/` 下创建完整的模板目录结构。

> 如果脚本执行报错（如文件不存在），可以使用 write 工具手动创建 `skills/<skill-name>/SKILL.md`，目录会自动创建。

### 步骤 4：编辑技能

编辑技能时，记住技能是为另一个 Agent 实例创建的。包含对 Agent 有益且非显而易见的信息。

#### 学习设计模式

- **多步骤流程**：见 `references/workflows.md`
- **输出格式或质量标准**：见 `references/output-patterns.md`

#### 从可复用资源开始

先实现 `scripts/`、`references/` 和 `assets/` 中的文件。添加的脚本必须通过实际运行来测试：

```bash
python skills/{name}/scripts/xxx.py
```

从会话目录使用完整路径运行脚本，不要 cd 进入技能目录。这样产出文件会保存到会话目录中。

#### 更新 SKILL.md

**前置元数据**：

- `name`：技能显示名（支持中文）
- `description`：技能的主要触发机制，帮助 Agent 理解何时使用技能。包括做什么和具体触发场景。

**正文**：使用技能及其捆绑资源的说明。始终使用祈使句/不定式形式。

### 步骤 5：迭代

创建完成后技能立即生效，无需重启。在实际任务中使用技能，注意困难或低效之处，然后改进。

## 安装外部技能

### 从 GitHub 安装(优先方式)

如果用户提供了 GitHub 仓库链接,**优先使用精确下载**,避免把整个仓库 clone 到 skills/:

**方案 A · 仓库本身就是单技能**(根目录有 SKILL.md):

```bash
# 直接 clone 到 skills/{skill-name}/
git clone --depth 1 <repo_url> skills/<skill-name>
# 清理 git 元数据(可选)
rm -rf skills/<skill-name>/.git
```

**方案 B · 仓库含多技能**(如 vercel-labs/skills,真实技能在 `skills/{name}/`):

```bash
# 用 sparse-checkout 只拉需要的那份技能
git clone --depth 1 --filter=blob:none --sparse <repo_url> /tmp/skill-src
cd /tmp/skill-src && git sparse-checkout set skills/<skill-name>
# 搬到正确位置
cp -r skills/<skill-name>/<files> "$SESSION_DIR/skills/<skill-name>/"
```

**方案 C · 只要一个 SKILL.md**(最小方案):

```bash
# 用 GitHub raw 直接下载
mkdir -p skills/<skill-name>
curl -s "https://raw.githubusercontent.com/<owner>/<repo>/main/skills/<skill-name>/SKILL.md" \
  -o skills/<skill-name>/SKILL.md
```

**关键红线**:

1. 不要 `git clone` 整个仓库到 `skills/<repo-name>/` — 这样 `package.json`、
   `pnpm-lock.yaml` 等开发工程文件会混进你的技能库
2. 最终 `skills/<skill-name>/` 下**必须**有且仅有 `SKILL.md`(及其 `scripts/` / `references/` / `assets/` 子目录)
3. 完成后先 `ls skills/<skill-name>/` 确认结构整洁,再告诉用户"安装成功"

### 用 npx 类工具安装(注意默认装路径)

某些社区工具(如 `npx skills add ...`、`vercel-labs/skills`)会把技能装到自己的默认目录,
**不在我们的 `skills/`**:

```bash
npx -y skills add https://github.com/owner/repo --skill <skill-name> --yes
# ↑ 这条命令默认装到 .agents/skills/<skill-name>/ ,不会自动登记到团队资产库
```

**安装完后必须手动搬运到正确位置**:

```bash
# 装完查找一下实际位置(npx 工具的默认输出目录通常是 .agents/skills/)
ls -la .agents/skills/<skill-name>/  2>/dev/null || \
  find . -name "<skill-name>" -type d 2>/dev/null | head -3

# 看到了之后整目录搬到 skills/
cp -r .agents/skills/<skill-name> skills/<skill-name>
# 或者(如果不再需要原位置):
mv .agents/skills/<skill-name> skills/
```

搬到 `skills/<skill-name>/` 后,系统会自动登记。**告知用户安装成功之前,务必先确认
`skills/<skill-name>/SKILL.md` 真的存在**。

### 从 ZIP/.skill 包安装

如果用户提供了 ZIP 或 .skill 文件(本质是 ZIP),解压**直接到 `skills/` 目录**:

```bash
unzip <file>.zip -d skills/
# 解压后检查目录结构 — 有时压缩包里多套了一层目录,需要扁平化
ls skills/
```

### 安装后必做:让 Agent 立刻可用

任意安装方式完成后,系统会自动把新技能加入当前 Agent 视角(本轮对话立刻可读),
但要让其他 Agent 也能用,需要在 Agent 配置里勾选绑定 — 提醒用户即可。

## 注意事项

- 技能目录名必须是小写字母、数字和连字符的组合（如 `data-analyzer`）
- `skills/` 路径会自动路由到团队技能目录，所有同团队 Agent 共享
- 禁止在内核路径（如 `/app/core/skills/builtin`）下创建或修改技能
- 技能不需要打包即可使用，创建后直接生效
- 如需发布到 Explore 市场，用户可在设置页面的技能面板中提交
