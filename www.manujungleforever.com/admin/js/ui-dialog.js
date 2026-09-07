/**
 * UI Dialog & Sonner-style Toast Library for Manu Jungle Forever Admin
 * Provides zero-dependency, modern dark-theme Promise-based ConfirmDialog and Toasts.
 */

(function (window) {
  'use strict';

  // Inject CSS styles for ConfirmDialog, Toasts, and Item Deletion animations
  const styleEl = document.createElement('style');
  styleEl.id = 'mjf-ui-dialog-styles';
  styleEl.textContent = `
    /* --- Modern Backdrop Dialog --- */
    .mjf-dialog-overlay {
      position: fixed;
      inset: 0;
      background: rgba(3, 8, 7, 0.75);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 99999;
      opacity: 0;
      transition: opacity 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      padding: 20px;
    }
    .mjf-dialog-overlay.mjf-open {
      opacity: 1;
    }
    .mjf-dialog-modal {
      background: #071f1a;
      background: radial-gradient(circle at 50% 0%, #0d362d 0%, #061814 100%);
      border: 1px solid rgba(45, 212, 191, 0.22);
      border-radius: 20px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7), 0 0 0 1px rgba(45, 212, 191, 0.1);
      width: 100%;
      max-width: 440px;
      padding: 28px;
      transform: scale(0.94) translateY(10px);
      transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      color: #f1f5f9;
      font-family: 'Poppins', sans-serif;
    }
    .mjf-dialog-overlay.mjf-open .mjf-dialog-modal {
      transform: scale(1) translateY(0);
    }
    .mjf-dialog-header {
      display: flex;
      align-items: flex-start;
      gap: 16px;
      margin-bottom: 16px;
    }
    .mjf-dialog-icon {
      width: 44px;
      height: 44px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.4rem;
      flex-shrink: 0;
    }
    .mjf-dialog-icon.danger {
      background: rgba(239, 68, 68, 0.15);
      color: #ef4444;
      border: 1px solid rgba(239, 68, 68, 0.3);
    }
    .mjf-dialog-icon.warning {
      background: rgba(245, 158, 11, 0.15);
      color: #f59e0b;
      border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .mjf-dialog-icon.info {
      background: rgba(45, 212, 191, 0.15);
      color: #2dd4bf;
      border: 1px solid rgba(45, 212, 191, 0.3);
    }
    .mjf-dialog-titles h3 {
      font-size: 1.2rem;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 6px;
      line-height: 1.3;
    }
    .mjf-dialog-titles p {
      font-size: 0.9rem;
      color: #94a3b8;
      line-height: 1.55;
    }
    .mjf-dialog-actions {
      display: flex;
      gap: 12px;
      justify-content: flex-end;
      margin-top: 24px;
    }
    .mjf-dialog-btn {
      padding: 10px 20px;
      border-radius: 12px;
      font-size: 0.88rem;
      font-weight: 600;
      cursor: pointer;
      border: none;
      transition: all 0.2s ease;
      font-family: inherit;
    }
    .mjf-dialog-btn-cancel {
      background: rgba(255, 255, 255, 0.07);
      color: #cbd5e1;
      border: 1px solid rgba(255, 255, 255, 0.12);
    }
    .mjf-dialog-btn-cancel:hover {
      background: rgba(255, 255, 255, 0.12);
      color: #ffffff;
    }
    .mjf-dialog-btn-confirm.danger {
      background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(239, 68, 68, 0.4);
    }
    .mjf-dialog-btn-confirm.danger:hover {
      box-shadow: 0 6px 18px rgba(239, 68, 68, 0.6);
      transform: translateY(-1px);
    }
    .mjf-dialog-btn-confirm.primary {
      background: linear-gradient(135deg, #0d9488 0%, #10b981 100%);
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(13, 148, 136, 0.4);
    }
    .mjf-dialog-btn-confirm.primary:hover {
      box-shadow: 0 6px 18px rgba(13, 148, 136, 0.6);
      transform: translateY(-1px);
    }

    /* --- Sonner-Style Toast Container --- */
    .mjf-toast-container {
      position: fixed;
      bottom: 28px;
      right: 28px;
      z-index: 100000;
      display: flex;
      flex-direction: column;
      gap: 10px;
      pointer-events: none;
    }
    .mjf-toast {
      background: rgba(7, 31, 26, 0.92);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(45, 212, 191, 0.25);
      border-radius: 14px;
      padding: 14px 18px;
      color: #f1f5f9;
      font-family: 'Poppins', sans-serif;
      font-size: 0.88rem;
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.45);
      display: flex;
      align-items: center;
      gap: 12px;
      pointer-events: auto;
      transform: translateY(20px) scale(0.95);
      opacity: 0;
      transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1);
      max-width: 360px;
    }
    .mjf-toast.mjf-toast-visible {
      transform: translateY(0) scale(1);
      opacity: 1;
    }
    .mjf-toast.mjf-toast-hiding {
      transform: translateY(-10px) scale(0.92);
      opacity: 0;
    }
    .mjf-toast-icon {
      font-size: 1.15rem;
      display: flex;
      align-items: center;
    }
    .mjf-toast.success .mjf-toast-icon { color: #10b981; }
    .mjf-toast.error .mjf-toast-icon { color: #ef4444; }
    .mjf-toast.loading .mjf-toast-icon { color: #2dd4bf; }
    .mjf-toast-spinner {
      width: 16px;
      height: 16px;
      border: 2px solid rgba(45, 212, 191, 0.3);
      border-top-color: #2dd4bf;
      border-radius: 50%;
      animation: mjf-spin 0.8s linear infinite;
    }
    @keyframes mjf-spin {
      to { transform: rotate(360deg); }
    }

    /* --- Standardized 300ms Deletion Animation for Tables / Cards --- */
    .item-deleting,
    .row-deleting {
      transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1) !important;
      opacity: 0 !important;
      transform: scale(0.95) translateY(-6px) !important;
      max-height: 0 !important;
      padding-top: 0 !important;
      padding-bottom: 0 !important;
      margin-top: 0 !important;
      margin-bottom: 0 !important;
      overflow: hidden !important;
      pointer-events: none !important;
      border-color: transparent !important;
    }
  `;
  document.head.appendChild(styleEl);

  /**
   * Global Confirm Dialog
   * @param {Object} options
   * @param {string} options.title
   * @param {string} options.message
   * @param {string} [options.confirmText='Confirmar']
   * @param {string} [options.cancelText='Cancelar']
   * @param {'danger'|'warning'|'primary'} [options.type='danger']
   * @returns {Promise<boolean>}
   */
  window.confirmDialog = function ({
    title = '¿Estás seguro?',
    message = 'Esta acción no se puede deshacer.',
    confirmText = 'Confirmar',
    cancelText = 'Cancelar',
    type = 'danger'
  }) {
    return new Promise((resolve) => {
      const iconClass = type === 'danger' ? 'ph-trash' : type === 'warning' ? 'ph-warning' : 'ph-check-circle';
      const overlay = document.createElement('div');
      overlay.className = 'mjf-dialog-overlay';

      overlay.innerHTML = `
        <div class="mjf-dialog-modal" role="dialog" aria-modal="true">
          <div class="mjf-dialog-header">
            <div class="mjf-dialog-icon ${type}">
              <i class="ph ${iconClass}"></i>
            </div>
            <div class="mjf-dialog-titles">
              <h3>${title}</h3>
              <p>${message}</p>
            </div>
          </div>
          <div class="mjf-dialog-actions">
            <button type="button" class="mjf-dialog-btn mjf-dialog-btn-cancel" id="mjf-btn-cancel">${cancelText}</button>
            <button type="button" class="mjf-dialog-btn mjf-dialog-btn-confirm ${type}" id="mjf-btn-confirm">${confirmText}</button>
          </div>
        </div>
      `;

      document.body.appendChild(overlay);
      requestAnimationFrame(() => overlay.classList.add('mjf-open'));

      const cleanup = (result) => {
        overlay.classList.remove('mjf-open');
        setTimeout(() => {
          overlay.remove();
          document.removeEventListener('keydown', handleKeyDown);
          resolve(result);
        }, 250);
      };

      const handleKeyDown = (e) => {
        if (e.key === 'Escape') cleanup(false);
      };
      document.addEventListener('keydown', handleKeyDown);

      overlay.querySelector('#mjf-btn-cancel').onclick = () => cleanup(false);
      overlay.querySelector('#mjf-btn-confirm').onclick = () => cleanup(true);
      overlay.onclick = (e) => {
        if (e.target === overlay) cleanup(false);
      };
    });
  };

  /**
   * Sonner-Style Toast Notifications
   */
  let toastContainer = null;
  const ensureToastContainer = () => {
    if (!toastContainer || !document.body.contains(toastContainer)) {
      toastContainer = document.createElement('div');
      toastContainer.className = 'mjf-toast-container';
      document.body.appendChild(toastContainer);
    }
    return toastContainer;
  };

  window.toast = {
    show(message, type = 'info', duration = 3500) {
      const container = ensureToastContainer();
      const el = document.createElement('div');
      el.className = `mjf-toast ${type}`;

      let iconHtml = '<i class="ph ph-info"></i>';
      if (type === 'success') iconHtml = '<i class="ph ph-check-circle"></i>';
      if (type === 'error') iconHtml = '<i class="ph ph-x-circle"></i>';
      if (type === 'loading') iconHtml = '<div class="mjf-toast-spinner"></div>';

      el.innerHTML = `
        <span class="mjf-toast-icon">${iconHtml}</span>
        <span class="mjf-toast-msg">${message}</span>
      `;
      container.appendChild(el);
      requestAnimationFrame(() => el.classList.add('mjf-toast-visible'));

      const dismiss = () => {
        el.classList.remove('mjf-toast-visible');
        el.classList.add('mjf-toast-hiding');
        setTimeout(() => el.remove(), 300);
      };

      if (duration > 0) {
        setTimeout(dismiss, duration);
      }

      return {
        update(newMessage, newType = type, newDuration = 3500) {
          el.className = `mjf-toast ${newType} mjf-toast-visible`;
          let nIcon = '<i class="ph ph-info"></i>';
          if (newType === 'success') nIcon = '<i class="ph ph-check-circle"></i>';
          if (newType === 'error') nIcon = '<i class="ph ph-x-circle"></i>';
          if (newType === 'loading') nIcon = '<div class="mjf-toast-spinner"></div>';
          el.querySelector('.mjf-toast-icon').innerHTML = nIcon;
          el.querySelector('.mjf-toast-msg').textContent = newMessage;
          if (newDuration > 0) setTimeout(dismiss, newDuration);
        },
        dismiss
      };
    },

    success(message, duration = 3500) {
      return this.show(message, 'success', duration);
    },

    error(message, duration = 4000) {
      return this.show(message, 'error', duration);
    },

    loading(message) {
      return this.show(message, 'loading', 0);
    },

    /**
     * Toast with Promise state handling (loading -> success or error)
     * @param {Promise<any>} promise
     * @param {Object} options
     * @param {string} options.loading
     * @param {string} options.success
     * @param {string} options.error
     */
    async promise(promise, { loading = 'Cargando...', success = 'Completado con éxito', error = 'Ocurrió un error' }) {
      const activeToast = this.loading(loading);
      try {
        const res = await promise;
        activeToast.update(typeof success === 'function' ? success(res) : success, 'success', 3500);
        return res;
      } catch (err) {
        activeToast.update(typeof error === 'function' ? error(err) : error, 'error', 4500);
        throw err;
      }
    }
  };
})(window);
