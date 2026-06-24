/* ============================================
   范式F 双模式协同增强组件 v2.0
   统一JS逻辑：链接跳转 + 闭环模拟 + Toast提示
   ============================================ */

// 1. 范式F顶部状态栏
function renderParadigmFBar(pageName, modeA_desc, modeB_desc, loopback_desc) {
  const bar = document.createElement('div');
  bar.className = 'paradigm-f-bar';
  bar.innerHTML = `
    <div style="display:flex;align-items:center;gap:12px;">
      <span style="font-weight:700;color:#e2e8f0;">⚡ 范式F · 双模式协同</span>
      <span class="mode-tag mode-a">模式A · ${pageName}</span>
      <span style="color:#64748b;">${modeA_desc}</span>
    </div>
    <div class="loop-info">
      <span class="loop-arrow">⇄</span>
      <span>点击 📄 跳转简道云详情页(模式B) → ${loopback_desc} → 本页刷新</span>
      <span class="loopback-indicator active"><span class="dot"></span>闭环就绪</span>
    </div>
  `;
  document.body.prepend(bar);
}

// 2. 数据链接按钮生成器
function createJDYLink(entryId, dataId, label) {
  const link = document.createElement('a');
  link.className = 'jdy-link';
  link.href = `https://www.jiandaoyun.com/open/entry/${entryId}?data_id=${dataId}`;
  link.target = '_blank';
  link.title = `在简道云中打开: ${label}`;
  link.textContent = label || '详情';
  link.onclick = function(e) {
    e.preventDefault();
    simulateLoopback(label);
  };
  return link;
}

// 3. 闭环模拟 - 点击链接后模拟Bridge回调
function simulateLoopback(taskName) {
  // 显示Toast
  const toast = document.createElement('div');
  toast.className = 'loopback-toast';
  toast.innerHTML = `
    <div class="toast-icon">🔄</div>
    <div class="toast-text">
      <strong>闭环模拟</strong><br>
      ① 跳转简道云详情页编辑「${taskName}」<br>
      ② 智能助手检测数据变更<br>
      ③ Webhook → Bridge重算CPM<br>
      ④ 结果写回简道云 → 本页刷新可见
    </div>
  `;
  document.body.appendChild(toast);

  // 3秒后更新状态
  setTimeout(() => {
    toast.querySelector('.toast-icon').textContent = '✅';
    toast.querySelector('.toast-text').innerHTML = `
      <strong>闭环完成</strong><br>
      「${taskName}」数据已更新，CPM已重算。<br>
      <span style="color:#64748b;">生产环境此流程自动执行</span>
    `;
  }, 3000);

  // 6秒后消失
  setTimeout(() => {
    toast.style.transition = 'opacity 0.3s';
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 6000);
}

// 4. 右键菜单（甘特图专用）
function showContextMenu(e, taskName, taskId) {
  e.preventDefault();
  let menu = document.getElementById('paradigm-f-context-menu');
  if (!menu) {
    menu = document.createElement('div');
    menu.id = 'paradigm-f-context-menu';
    menu.className = 'context-menu';
    document.body.appendChild(menu);
  }
  menu.innerHTML = `
    <div class="context-menu-item" onclick="simulateLoopback('${taskName}');hideContextMenu();">
      <span class="cm-icon">📄</span> 在简道云中打开详情
    </div>
    <div class="context-menu-item" onclick="alert('编辑任务属性（原型演示）');hideContextMenu();">
      <span class="cm-icon">✏️</span> 快速编辑属性
    </div>
    <div class="context-menu-divider"></div>
    <div class="context-menu-item" onclick="alert('查看依赖关系（原型演示）');hideContextMenu();">
      <span class="cm-icon">🔗</span> 查看依赖关系
    </div>
    <div class="context-menu-item" onclick="alert('查看资源分配（原型演示）');hideContextMenu();">
      <span class="cm-icon">👥</span> 查看资源分配
    </div>
  `;
  menu.style.left = e.clientX + 'px';
  menu.style.top = e.clientY + 'px';
  menu.classList.add('show');
}

function hideContextMenu() {
  const menu = document.getElementById('paradigm-f-context-menu');
  if (menu) menu.classList.remove('show');
}

document.addEventListener('click', function(e) {
  if (!e.target.closest('.context-menu')) hideContextMenu();
});
