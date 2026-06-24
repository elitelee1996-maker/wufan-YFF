/**
 * OKR Bridge API Client
 * 连接 HTML 页面与简道云后端服务
 */
const OKR_API = {
  BASE_URL: 'http://47.98.192.245:8200',
  
  /**
   * 提交目标制定
   * @param {Object} data - 目标数据
   * @returns {Promise}
   */
  async submitGoal(data) {
    return this._post('/api/okr/goal', data);
  },
  
  /**
   * 更新 KR 进度
   * @param {string} kr_data_id - KR 数据 ID
   * @param {number} current_progress - 当前进度 (0-1)
   * @param {string} progress_desc - 进展说明
   * @returns {Promise}
   */
  async updateProgress(kr_data_id, current_progress, progress_desc) {
    return this._post('/api/okr/progress', {
      kr_data_id,
      current_progress,
      progress_desc
    });
  },
  
  /**
   * 查询 OKR 列表
   * @param {Object} filters - 过滤条件
   * @returns {Promise}
   */
  async listOKR(filters = {}) {
    const params = new URLSearchParams(filters);
    return this._get(`/api/okr/list?${params}`);
  },
  
  /**
   * 查询战略列表
   * @param {string} cycle - 周期
   * @returns {Promise}
   */
  async listStrategy(cycle = '') {
    const params = cycle ? `?cycle=${encodeURIComponent(cycle)}` : '';
    return this._get(`/api/okr/strategy${params}`);
  },
  
  /**
   * 健康检查
   * @returns {Promise}
   */
  async health() {
    return this._get('/health');
  },
  
  // 内部方法
  async _post(path, data) {
    const resp = await fetch(this.BASE_URL + path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!resp.ok) {
      const err = await resp.text();
      throw new Error(`API Error: ${resp.status} - ${err}`);
    }
    return resp.json();
  },
  
  async _get(path) {
    const resp = await fetch(this.BASE_URL + path);
    if (!resp.ok) {
      const err = await resp.text();
      throw new Error(`API Error: ${resp.status} - ${err}`);
    }
    return resp.json();
  }
};

/**
 * 显示 Toast 提示
 */
function showToast(message, type = 'success', duration = 3000) {
  const colors = {
    success: '#34c759',
    error: '#ff3b30',
    warning: '#f5a623',
    info: '#3370ff'
  };
  
  const toast = document.createElement('div');
  toast.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 12px 20px;
    background: ${colors[type] || colors.info};
    color: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 10000;
    font-size: 14px;
    font-weight: 500;
    animation: slideIn 0.3s ease;
  `;
  toast.textContent = message;
  
  // 添加动画样式
  if (!document.getElementById('toast-styles')) {
    const style = document.createElement('style');
    style.id = 'toast-styles';
    style.textContent = `
      @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
      }
      @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
      }
    `;
    document.head.appendChild(style);
  }
  
  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.style.animation = 'slideOut 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

/**
 * 显示加载状态
 */
function showLoading(show = true) {
  let loader = document.getElementById('api-loader');
  
  if (show) {
    if (!loader) {
      loader = document.createElement('div');
      loader.id = 'api-loader';
      loader.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255,255,255,0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
      `;
      loader.innerHTML = `
        <div style="text-align: center;">
          <div style="width: 40px; height: 40px; border: 3px solid #e8eaed; border-top-color: #3370ff; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 12px;"></div>
          <div style="color: #646a73; font-size: 14px;">正在提交...</div>
        </div>
      `;
      
      // 添加旋转动画
      if (!document.getElementById('loader-styles')) {
        const style = document.createElement('style');
        style.id = 'loader-styles';
        style.textContent = `@keyframes spin { to { transform: rotate(360deg); } }`;
        document.head.appendChild(style);
      }
      
      document.body.appendChild(loader);
    }
  } else {
    if (loader) loader.remove();
  }
}
