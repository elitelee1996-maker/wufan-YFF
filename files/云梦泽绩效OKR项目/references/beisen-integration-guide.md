# 北森绩效云复刻 - 集成指南

**版本**: v1.0  
**最后更新**: 2026-05-17  
**关联主文档**: `files/beisen-performance-replication-plan.md`  
**适用对象**: 系统管理员、开发人员、HRBP

---

## 一、集成总览

本文档汇总北森绩效云复刻方案中的 **5大核心集成场景**，提供技术实现指南。

| 集成编号 | 集成场景 | 简道云原生支持 | 是否需二开 | 复杂度 |
|---------|---------|--------------|-----------|--------|
| INT-01 | 电子签署功能 | 部分支持（签名字段） | 是（PDF生成） | 中 |
| INT-02 | IM集成（飞书/钉钉） | 支持（第三方集成） | 否 | 低 |
| INT-03 | 多语言配置 | 不支持 | 是（前端事件） | 中 |
| INT-04 | API数据同步 | 企业版支持 | 部分 | 高 |
| INT-05 | SSO单点登录 | 企业版支持 | 否 | 低 |

---

## 二、INT-01: 电子签署功能

### 2.1 业务需求

北森支持目标/绩效的电子签署，员工和经理需在审批通过后手写签名，系统自动生成带签名的PDF归档。

### 2.2 简道云原生能力

- **签名字段**: 支持手写签名采集
- **打印模板**: 企业版支持自定义打印模板（Excel/Word）
- **附件字段**: 可存储生成的PDF文件

### 2.3 技术架构

```mermaid
graph LR
    A[审批通过] --> B[员工签名]
    B --> C[经理签名]
    C --> D[智能助手触发]
    D --> E[二开服务API调用]
    E --> F[简道云打印API]
    F --> G[生成PDF]
    G --> H[回传至附件字段]
    H --> I[推送通知]
```

### 2.4 实现步骤

#### 步骤1: 配置打印模板

1. 进入"系统管理" > "打印模板" > "新建模板"
2. 选择Word模板，设计目标书/考核表格式
3. 插入签名字段占位符：
   ```
   员工签名: {{electronic_signature_employee}}
   经理签名: {{electronic_signature_manager}}
   ```
4. 保存模板，记录template_id

#### 步骤2: 配置智能助手

```yaml
智能助手名称: 电子签署PDF生成
触发类型: 表单触发
触发条件: OKR主表.status 变更为 "已生效" 
         OR 员工目标主表.status 变更为 "已生效"
         OR 绩效主表.status 变更为 "已完成"

执行节点:
  1. 等待节点:
    - 等待条件: electronic_signature_employee 和 electronic_signature_manager 均不为空
    - 超时时间: 24小时（若超时则发送提醒）
    
  2. HTTP请求节点:
    - 请求方式: POST
    - 请求URL: https://your-backend-api.com/api/generate-signature-pdf
    - 请求头:
      Content-Type: application/json
      Authorization: Bearer {{API_KEY}}
    - 请求体:
      {
        "form_type": "{{触发表单名称}}",
        "record_id": "{{触发记录ID}}",
        "template_id": "{{对应的模板ID}}",
        "employee_signature": "{{electronic_signature_employee}}",
        "manager_signature": "{{electronic_signature_manager}}"
      }
      
  3. 等待节点:
    - 等待时长: 10秒（等待PDF生成）
    
  4. 更新节点:
    - 更新对象: 触发表单
    - 更新条件: record_id = {{触发记录ID}}
    - 更新字段: signed_pdf = {{HTTP响应.pdf_url}}
    
  5. 通知节点:
    - 通知方式: IM推送
    - 通知对象: 员工 + 经理
    - 消息内容: "您的{{文档类型}}已签署完成，PDF已归档"
```

#### 步骤3: 二开服务代码（Node.js示例）

```javascript
// /api/generate-signature-pdf
const express = require('express');
const router = express.Router();
const jiandaoyun = require('./jiandaoyun-sdk');
const PDFDocument = require('pdfkit');
const fs = require('fs');

router.post('/generate-signature-pdf', async (req, res) => {
  try {
    const { form_type, record_id, template_id, employee_signature, manager_signature } = req.body;
    
    // 1. 调用简道云API获取表单数据
    const formData = await jiandaoyun.getRecord(form_type, record_id);
    
    // 2. 调用简道云打印API生成基础PDF
    const basePdfUrl = await jiandaoyun.generatePrintPDF({
      template_id: template_id,
      record_id: record_id
    });
    
    // 3. 下载基础PDF
    const basePdfBuffer = await downloadPDF(basePdfUrl);
    
    // 4. 使用PDF库嵌入签名图片
    const signedPdfBuffer = await embedSignatures(basePdfBuffer, {
      employee_signature: employee_signature,
      manager_signature: manager_signature
    });
    
    // 5. 上传签名后的PDF到简道云
    const signedPdfUrl = await jiandaoyun.uploadAttachment(signedPdfBuffer, {
      filename: `${form_type}_${record_id}_signed.pdf`
    });
    
    // 6. 返回PDF URL
    res.json({ pdf_url: signedPdfUrl });
    
  } catch (error) {
    console.error('PDF生成失败:', error);
    res.status(500).json({ error: 'PDF生成失败' });
  }
});

// 辅助函数：嵌入签名图片
async function embedSignatures(pdfBuffer, signatures) {
  return new Promise((resolve, reject) => {
    const doc = new PDFDocument();
    const chunks = [];
    
    doc.on('data', chunk => chunks.push(chunk));
    doc.on('end', () => resolve(Buffer.concat(chunks)));
    doc.on('error', reject);
    
    // 加载基础PDF
    // ...（使用pdf-lib或其他库合并签名）
    
    doc.end();
  });
}

module.exports = router;
```

### 2.5 注意事项

1. **版本限制**: 免费版不支持自定义打印模板，需企业版及以上
2. **签名图片格式**: 简道云签名字段返回的是Base64编码的图片，需转换为图片文件
3. **PDF安全性**: 生成的PDF应添加水印和加密，防止篡改
4. **归档策略**: 建议将签署后的PDF同步到企业网盘或文档管理系统

---

## 三、INT-02: IM集成（飞书/钉钉）

### 3.1 业务需求

目标任务变更时实时推送IM消息，支持@提及功能，提升协作效率。

### 3.2 简道云原生能力

- **第三方集成**: 支持飞书/钉钉/企微/微信
- **智能助手HTTP节点**: 可调用IM机器人Webhook
- **消息模板**: 支持交互式卡片消息

### 3.3 集成场景

| 场景 | 触发条件 | 接收人 | 消息类型 |
|------|---------|--------|---------|
| OKR审批待办 | OKR状态变更为"审批中" | 直线经理 | 交互式卡片 |
| 目标进度提醒 | 定时触发（每周一9:00） | 全体员工 | 文本消息 |
| 绩效评估邀请 | 绩效状态变更为"评估中" | 评价人 | 交互式卡片 |
| 电子签署完成 | signed_pdf字段不为空 | 员工+经理 | 文本消息 |
| 申诉处理通知 | 申诉状态变更 | HRBP | 文本消息 |

### 3.4 飞书集成配置

#### 步骤1: 启用第三方集成

1. 进入"系统管理" > "第三方集成" > "飞书"
2. 点击"授权"，跳转至飞书开放平台
3. 授权简道云访问飞书API
4. 配置回调URL（可选，用于接收飞书事件）

#### 步骤2: 获取机器人Webhook

1. 在飞书群聊中添加"自定义机器人"
2. 复制Webhook地址，格式：
   ```
   https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx
   ```
3. 将Webhook地址配置到智能助手的HTTP节点

#### 步骤3: 配置智能助手

```yaml
智能助手名称: OKR审批待办推送（飞书）
触发类型: 表单触发
触发条件: OKR主表.status 变更为 "审批中"

执行节点:
  1. 查询节点:
    - 查询对象: 员工信息表
    - 查询条件: employee_id = {{触发记录.employee_id}}
    - 获取字段: direct_manager_id, direct_manager_name
    
  2. HTTP请求节点:
    - 请求方式: POST
    - 请求URL: https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx
    - 请求头:
      Content-Type: application/json
    - 请求体:
      {
        "msg_type": "interactive",
        "card": {
          "config": {
            "wide_screen_mode": true
          },
          "header": {
            "title": {
              "tag": "plain_text",
              "content": "OKR审批待办"
            },
            "template": "blue"
          },
          "elements": [
            {
              "tag": "div",
              "text": {
                "tag": "lark_md",
                "content": "**{{employee_name}}** 提交了 **{{cycle_name}}** 周期的OKR\n\n请尽快审批"
              }
            },
            {
              "tag": "action",
              "actions": [
                {
                  "tag": "button",
                  "text": {
                    "tag": "plain_text",
                    "content": "去审批"
                  },
                  "type": "primary",
                  "url": "{{approval_link}}"
                }
              ]
            }
          ]
        }
      }
```

#### 步骤4: @提及功能实现

在消息内容中包含 `@user_id`，飞书会自动渲染为可点击的用户链接：

```json
{
  "msg_type": "text",
  "content": {
    "text": "请 <at user_id=\"ou_xxx123\"></at> 审批OKR"
  }
}
```

**获取user_id**:
- 从员工信息表中存储飞书user_id字段
- 或通过飞书API根据手机号查询user_id

### 3.5 钉钉集成配置

与飞书类似，区别在于：

1. **Webhook地址格式**:
   ```
   https://oapi.dingtalk.com/robot/send?access_token=xxxxx
   ```

2. **消息格式**:
   ```json
   {
     "msgtype": "actionCard",
     "actionCard": {
       "title": "OKR审批待办",
       "text": "{{employee_name}} 提交了 {{cycle_name}} 周期的OKR",
       "btnOrientation": "0",
       "btns": [
         {
           "title": "去审批",
           "actionURL": "{{approval_link}}"
         }
       ]
     }
   }
   ```

3. **@提及功能**:
   ```json
   {
     "at": {
       "atMobiles": ["13800138000"],
       "isAtAll": false
     }
   }
   ```

### 3.6 注意事项

1. **防骚扰机制**: 同一用户短时间内多次触发时，合并消息推送
2. **消息限流**: 飞书/钉钉对机器人消息有频率限制（如飞书20条/分钟）
3. **错误处理**: HTTP请求失败时，记录日志并 retry（最多3次）
4. **安全性**: Webhook地址应存储在环境变量中，不要硬编码

---

## 四、INT-03: 多语言配置

### 4.1 业务需求

北森支持多语言（中英文切换），适配国际化企业场景。

### 4.2 简道云限制

简道云**不原生支持**多语言，需通过以下方案实现：

### 4.3 实现方案

#### 方案A: 双语字段（推荐）

**原理**: 为每个文本字段创建中英文两个版本，通过前端事件动态显示

**步骤**:

1. **字段设计**:
   ```yaml
   OKR主表字段:
     - objective_cn: 富文本（中文目标描述）
     - objective_en: 富文本（英文目标描述）
     - kr_description_cn: 文本（中文KR描述）
     - kr_description_en: 文本（英文KR描述）
   ```

2. **用户偏好表**:
   ```yaml
   表单名称: 用户偏好表
   字段:
     - user_id: 成员字段
     - preferred_language: 单选 [中文, English]
     - updated_time: 日期时间
   ```

3. **前端事件配置**:
   ```javascript
   // 表单加载时执行
   jd.event.onFormLoad(async () => {
     const userLang = await getUserPreferredLanguage();
     
     if (userLang === 'English') {
       // 隐藏中文字段，显示英文字段
       jd.field.hide('objective_cn');
       jd.field.show('objective_en');
       jd.field.hide('kr_description_cn');
       jd.field.show('kr_description_en');
       
       // 修改字段标签为英文
       jd.field.setLabel('objective_en', 'Objective');
       jd.field.setLabel('kr_description_en', 'Key Results');
     } else {
       // 隐藏英文字段，显示中文字段
       jd.field.hide('objective_en');
       jd.field.show('objective_cn');
       jd.field.hide('kr_description_en');
       jd.field.show('kr_description_cn');
       
       // 修改字段标签为中文
       jd.field.setLabel('objective_cn', '目标描述');
       jd.field.setLabel('kr_description_cn', '关键结果');
     }
   });
   
   // 获取用户偏好语言
   async function getUserPreferredLanguage() {
     const userId = jd.context.currentUserId;
     const result = await jd.data.query({
       formId: '用户偏好表',
       filter: { user_id: userId }
     });
     
     return result.data.length > 0 ? result.data[0].preferred_language : '中文';
   }
   ```

4. **语言切换按钮**:
   - 在表单顶部添加"语言切换"按钮
   - 点击按钮时更新用户偏好表，并刷新页面

#### 方案B: 独立表单（适用于完全隔离的场景）

**原理**: 为每种语言创建独立的表单，通过智能助手同步数据

**缺点**: 维护成本高，数据一致性难保证

**不推荐**: 除非两种语言的使用场景完全隔离

### 4.4 仪表盘多语言

**挑战**: 仪表盘的图表标题、筛选器标签等也需要多语言

**解决方案**:
1. 为每种语言创建独立的仪表盘
2. 通过前端事件根据用户语言跳转到对应仪表盘
3. 或使用Mermaid语法绘制图表（支持HTML嵌入，可动态替换文本）

### 4.5 注意事项

1. **字段数量翻倍**: 双语字段会导致表单字段数量翻倍，注意简道云的字段上限
2. **数据录入负担**: 员工需同时填写中英文，增加工作量
3. **自动翻译**: 可集成翻译API（如百度翻译/Google Translate）自动填充英文字段，人工校对
4. **默认语言**: 新用户默认语言设为"中文"，可在首次登录时引导用户选择

---

## 五、INT-04: API数据同步

### 5.1 业务需求

绩效结果需同步到薪酬系统、ERP系统等外部系统，实现数据闭环。

### 5.2 简道云原生能力

- **企业版支持**: API/webhook功能（企业版及以上）
- **数据推送**: 智能助手Pro的HTTP请求节点
- **数据拉取**: 外部系统调用简道云API

### 5.3 同步场景

| 同步方向 | 场景 | 触发条件 | 目标系统 |
|---------|------|---------|---------|
| 简道云 → 外部 | 绩效结果同步薪酬系统 | 绩效状态变更为"已完成" | 薪酬系统 |
| 简道云 → 外部 | 组织绩效同步ERP | 组织绩效状态变更 | ERP系统 |
| 外部 → 简道云 | 员工信息同步 | HR系统员工入职/离职 | 简道云员工信息表 |
| 外部 → 简道云 | 项目数据同步 | 项目管理系统结项 | 简道云项目绩效表 |

### 5.4 简道云API简介

**API文档**: https://hc.jiandaoyun.com/doc/30/148

**认证方式**: API Key + API Secret

**常用接口**:

| 接口名称 | 方法 | 用途 |
|---------|------|------|
| 查询数据 | POST /api/v2/app/{app_id}/entry/{entry_id}/data/get | 查询表单数据 |
| 新增数据 | POST /api/v2/app/{app_id}/entry/{entry_id}/data/create | 新增表单记录 |
| 更新数据 | POST /api/v2/app/{app_id}/entry/{entry_id}/data/update | 更新表单记录 |
| 删除数据 | POST /api/v2/app/{app_id}/entry/{entry_id}/data/delete | 删除表单记录 |

### 5.5 实现示例：绩效结果同步薪酬系统

#### 步骤1: 配置智能助手

```yaml
智能助手名称: 绩效结果同步薪酬系统
触发类型: 表单触发
触发条件: 绩效主表.status 变更为 "已完成"

执行节点:
  1. 查询节点:
    - 查询对象: 绩效主表
    - 查询条件: performance_id = {{触发记录.performance_id}}
    - 获取字段: employee_id, total_score, performance_grade, cycle_id
    
  2. 查询节点:
    - 查询对象: 员工信息表
    - 查询条件: employee_id = {{employee_id}}
    - 获取字段: employee_no, department_id
    
  3. 查询节点:
    - 查询对象: 绩效系数表
    - 查询条件: performance_grade = {{performance_grade}}
    - 获取字段: bonus_coefficient
    
  4. HTTP请求节点:
    - 请求方式: POST
    - 请求URL: https://payroll-system.com/api/performance-result
    - 请求头:
      Content-Type: application/json
      Authorization: Bearer {{PAYROLL_API_KEY}}
    - 请求体:
      {
        "employee_no": "{{employee_no}}",
        "cycle_id": "{{cycle_id}}",
        "performance_score": {{total_score}},
        "performance_grade": "{{performance_grade}}",
        "bonus_coefficient": {{bonus_coefficient}},
        "sync_time": "{{当前时间}}"
      }
      
  5. 写入节点:
    - 写入对象: 绩效同步日志表
    - 写入内容: 记录同步时间、状态、响应结果
```

#### 步骤2: 外部系统接收接口（Python Flask示例）

```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/performance-result', methods=['POST'])
def receive_performance_result():
    try:
        data = request.json
        
        # 1. 验证数据
        required_fields = ['employee_no', 'cycle_id', 'performance_score', 'performance_grade']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # 2. 更新薪酬系统
        update_payroll_data(data)
        
        # 3. 返回成功响应
        return jsonify({'status': 'success', 'message': 'Performance result received'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def update_payroll_data(data):
    # 更新薪酬系统逻辑
    pass

if __name__ == '__main__':
    app.run(port=5000)
```

### 5.6 注意事项

1. **API限流**: 简道云API有调用频率限制（如100次/分钟），需做好限流控制
2. **错误处理**: HTTP请求失败时，记录日志并加入重试队列
3. **数据一致性**: 采用"最终一致性"策略，定期全量对账
4. **安全性**: API Key应存储在环境变量或密钥管理系统中
5. **幂等性**: 外部系统接口应支持幂等性，避免重复同步导致数据错误

---

## 六、INT-05: SSO单点登录

### 6.1 业务需求

企业已有统一身份认证系统（如AD/LDAP/OAuth2），需实现SSO单点登录。

### 6.2 简道云原生能力

- **企业版支持**: SSO功能（企业版及以上）
- **支持协议**: SAML 2.0、OAuth 2.0、CAS

### 6.3 配置步骤

#### 步骤1: 配置身份提供商（IdP）

以Azure AD为例：

1. 登录Azure Portal
2. 进入"Enterprise applications" > "New application"
3. 搜索"简道云"或选择"SAML Toolkit"
4. 配置SAML参数：
   - Identifier (Entity ID): `https://www.jiandaoyun.com`
   - Reply URL (Assertion Consumer Service URL): `https://www.jiandaoyun.com/sso/callback`
5. 下载SAML证书和元数据文件

#### 步骤2: 配置简道云SSO

1. 进入"系统管理" > "登录设置" > "SSO配置"
2. 选择SSO协议（SAML 2.0）
3. 上传IdP元数据文件或手动填写参数：
   - IdP Entity ID
   - SSO URL
   - X.509证书
4. 配置属性映射：
   - NameID → 简道云账号（手机号/邮箱）
   - displayName → 姓名
   - department → 部门
5. 启用SSO登录

#### 步骤3: 测试SSO

1. 访问简道云登录页
2. 点击"SSO登录"按钮
3. 跳转至Azure AD登录页
4. 输入企业账号密码
5. 自动跳转回简道云，完成登录

### 6.4 注意事项

1. **账号匹配**: 确保IdP返回的NameID与简道云账号一致（通常为手机号或邮箱）
2. **备用登录**: 保留账号密码登录方式，防止SSO故障时无法登录
3. **会话超时**: 配置合理的会话超时时间（如8小时）
4. **退出登录**: 配置SLO（Single Logout），实现全局退出

---

## 七、集成测试清单

### 7.1 电子签署测试

| 测试项 | 预期结果 | 实际结果 | 状态 |
|-------|---------|---------|------|
| 员工签名采集 | 签名图片正常显示 | | ☐ |
| 经理签名采集 | 签名图片正常显示 | | ☐ |
| PDF生成 | PDF包含双签名 | | ☐ |
| PDF归档 | signed_pdf字段有值 | | ☐ |
| 通知推送 | 员工和经理收到通知 | | ☐ |

### 7.2 IM集成测试

| 测试项 | 预期结果 | 实际结果 | 状态 |
|-------|---------|---------|------|
| OKR审批待办推送 | 经理收到飞书卡片消息 | | ☐ |
| @提及功能 | 消息中@经理可点击 | | ☐ |
| 定时提醒 | 每周一9:00推送提醒 | | ☐ |
| 消息合并 | 同一用户多条待办合并为一条 | | ☐ |

### 7.3 多语言测试

| 测试项 | 预期结果 | 实际结果 | 状态 |
|-------|---------|---------|------|
| 中文界面 | 显示中文字段和标签 | | ☐ |
| 英文界面 | 显示英文字段和标签 | | ☐ |
| 语言切换 | 切换后页面刷新并显示对应语言 | | ☐ |
| 用户偏好持久化 | 下次登录保持上次选择的语言 | | ☐ |

### 7.4 API同步测试

| 测试项 | 预期结果 | 实际结果 | 状态 |
|-------|---------|---------|------|
| 绩效结果推送 | 薪酬系统收到数据 | | ☐ |
| 错误处理 | 推送失败时记录日志 | | ☐ |
| 重试机制 | 失败后自动重试（最多3次） | | ☐ |
| 幂等性 | 重复推送不产生重复数据 | | ☐ |

### 7.5 SSO测试

| 测试项 | 预期结果 | 实际结果 | 状态 |
|-------|---------|---------|------|
| SSO登录 | 成功跳转并登录 | | ☐ |
| 账号匹配 | NameID正确匹配简道云账号 | | ☐ |
| 退出登录 | 全局退出成功 | | ☐ |
| 备用登录 | 账号密码登录仍可用 | | ☐ |

---

## 八、常见问题与解决方案

### 8.1 电子签署PDF生成失败

**问题**: 智能助手调用二开服务API超时

**解决方案**:
- 检查二开服务是否正常运行
- 增加智能助手等待节点的超时时间
- 查看二开服务日志定位错误原因
- 测试简道云打印API是否正常

### 8.2 IM消息推送失败

**问题**: HTTP请求返回403 Forbidden

**解决方案**:
- 检查Webhook地址是否正确
- 确认机器人是否在群聊中
- 检查飞书/钉钉应用权限配置
- 查看IM平台开发者文档的错误码说明

### 8.3 多语言切换无效

**问题**: 切换语言后字段未更新

**解决方案**:
- 检查前端事件是否正确绑定
- 确认用户偏好表中有对应记录
- 清除浏览器缓存后重试
- 检查字段显隐规则是否冲突

### 8.4 API同步数据不一致

**问题**: 简道云与外部系统数据不一致

**解决方案**:
- 检查API请求体字段映射是否正确
- 确认外部系统接口是否支持幂等性
- 定期运行全量对账脚本
- 查看同步日志定位失败记录

---

## 九、附录：API接口参考

### 9.1 简道云API示例

**查询数据**:
```bash
curl -X POST https://api.jiandaoyun.com/api/v2/app/{app_id}/entry/{entry_id}/data/get \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": ["field1", "field2"],
    "filter": {
      "field1": { "$eq": "value1" }
    },
    "limit": 100
  }'
```

**新增数据**:
```bash
curl -X POST https://api.jiandaoyun.com/api/v2/app/{app_id}/entry/{entry_id}/data/create \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "field1": "value1",
      "field2": "value2"
    }
  }'
```

### 9.2 飞书机器人API示例

**发送文本消息**:
```bash
curl -X POST https://open.feishu.cn/open-apis/bot/v2/hook/{webhook_id} \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "text",
    "content": {
      "text": "Hello, this is a test message"
    }
  }'
```

**发送交互式卡片**:
```bash
curl -X POST https://open.feishu.cn/open-apis/bot/v2/hook/{webhook_id} \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "interactive",
    "card": {
      "header": {
        "title": {
          "tag": "plain_text",
          "content": "Test Card"
        }
      },
      "elements": [
        {
          "tag": "div",
          "text": {
            "tag": "lark_md",
            "content": "This is a test card"
          }
        }
      ]
    }
  }'
```

---

**文档维护说明**:
- 本工作表为主文档 `files/beisen-performance-replication-plan.md` 的详细补充
- 每次集成配置调整需同步更新版本号
- 所有飞书云文档需自动添加 Frank (ou_1e87f1890876b57a6f2ab437a3fce415) 为编辑协作者
