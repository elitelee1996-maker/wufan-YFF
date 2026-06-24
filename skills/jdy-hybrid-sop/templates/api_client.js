/**
 * 前端 API 客户端模板 - Bridge 模式
 * BASE_URL 自动取当前页面 origin，不硬编码 IP
 */

const BASE_URL = window.location.origin;

// ---------------------------------------------------------------------------
// Toast / Loading UI 工具
// ---------------------------------------------------------------------------

/**
 * 显示轻提示消息
 * @param {string} message - 提示文本
 * @param {'success'|'error'|'info'} type - 提示类型
 * @param {number} duration - 显示时长(ms)
 */
function showToast(message, type = 'info', duration = 3000) {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  Object.assign(toast.style, {
    position: 'fixed', top: '20px', right: '20px', zIndex: '9999',
    padding: '12px 24px', borderRadius: '6px', color: '#fff', fontSize: '14px',
    background: type === 'error' ? '#e74c3c' : type === 'success' ? '#27ae60' : '#3498db',
    transition: 'opacity 0.3s',
  });
  document.body.appendChild(toast);
  setTimeout(() => { toast.style.opacity = '0'; }, duration - 300);
  setTimeout(() => { toast.remove(); }, duration);
}

/**
 * 显示/隐藏全局加载遮罩
 * @param {boolean} show - true 显示，false 隐藏
 */
function showLoading(show) {
  let overlay = document.getElementById('global-loading-overlay');
  if (show) {
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.id = 'global-loading-overlay';
      Object.assign(overlay.style, {
        position: 'fixed', inset: '0', zIndex: '9998',
        background: 'rgba(255,255,255,0.6)', display: 'flex',
        alignItems: 'center', justifyContent: 'center',
      });
      overlay.innerHTML = '<div style="font-size:24px;color:#333;">加载中…</div>';
      document.body.appendChild(overlay);
    }
    overlay.style.display = 'flex';
  } else if (overlay) {
    overlay.style.display = 'none';
  }
}

// ---------------------------------------------------------------------------
// 统一请求方法
// ---------------------------------------------------------------------------

/**
 * 发送 HTTP 请求（内部统一入口）
 * @param {string} path - API 路径（如 /api/orders）
 * @param {object} options - fetch 选项
 * @returns {Promise<any>} 响应 JSON
 */
async function request(path, options = {}) {
  const url = `${BASE_URL}${path}`;
  const config = {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  };

  try {
    const response = await fetch(url, config);
    if (!response.ok) {
      const errBody = await response.json().catch(() => ({}));
      throw new Error(errBody.message || errBody.error || `HTTP ${response.status}`);
    }
    // 204 No Content
    if (response.status === 204) return null;
    return await response.json();
  } catch (err) {
    showToast(err.message || '网络请求失败', 'error');
    throw err;
  }
}

/**
 * GET 请求
 * @param {string} path - API 路径
 * @param {object} [params] - 查询参数
 */
async function get(path, params = {}) {
  const qs = new URLSearchParams(params).toString();
  const fullPath = qs ? `${path}?${qs}` : path;
  return request(fullPath, { method: 'GET' });
}

/**
 * POST 请求
 * @param {string} path - API 路径
 * @param {object} body - 请求体
 */
async function post(path, body = {}) {
  return request(path, { method: 'POST', body: JSON.stringify(body) });
}

/**
 * PUT 请求
 * @param {string} path - API 路径
 * @param {object} body - 请求体
 */
async function put(path, body = {}) {
  return request(path, { method: 'PUT', body: JSON.stringify(body) });
}

/**
 * DELETE 请求
 * @param {string} path - API 路径
 */
async function del(path) {
  return request(path, { method: 'DELETE' });
}

// 导出（兼容模块化和全局挂载）
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { BASE_URL, request, get, post, put, del, showToast, showLoading };
}
