(function () {
    const token = sessionStorage.getItem('cms_token');
    if (!token) { 
        if (!window.location.href.includes('index.html') && window.location.pathname !== '/admin/') {
            window.location.href = 'index.html'; 
        }
        return; 
    }
    
    // Auth success - show body
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => { document.body.style.opacity = '1'; });
    } else {
        document.body.style.opacity = '1';
    }

    // Set user name if element exists
    window.addEventListener('DOMContentLoaded', () => {
        const adminNameEl = document.getElementById('admin-name');
        if (adminNameEl) {
            const u = sessionStorage.getItem('cms_user');
            if(u) adminNameEl.textContent = u.split('@')[0];
        }
    });
})();

function logout() {
    sessionStorage.clear();
    window.location.href = 'index.html';
}
