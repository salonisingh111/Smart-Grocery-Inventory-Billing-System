document.addEventListener('DOMContentLoaded', () => {
  // Sidebar Toggle for Responsive Layout
  const toggleBtn = document.getElementById('sidebarToggle');
  const sidebar = document.querySelector('.app-sidebar');

  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('compact');
      sidebar.classList.toggle('active');
    });
  }

  // Flash Message auto dismiss
  const alerts = document.querySelectorAll('.alert-dismissible, .flash-alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 300ms ease';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 300);
    }, 3000);
  });
});

// Toast notification helper
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  
  let icon = 'fa-info-circle';
  if (type === 'success') icon = 'fa-check-circle';
  if (type === 'danger') icon = 'fa-exclamation-triangle';
  if (type === 'warning') icon = 'fa-exclamation-circle';

  toast.innerHTML = `<i class="fas ${icon}"></i> <span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = 'opacity 300ms ease';
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

// Global Sensitive Password Confirmation Trigger
function promptPasswordConfirmation(formElement, title = 'Security Password Confirmation') {
  const modal = document.getElementById('passwordConfirmModal');
  const pwdInput = document.getElementById('modalConfirmPassword');
  const modalTitle = document.getElementById('modalConfirmTitle');

  if (!modal || !pwdInput) return true;

  modalTitle.textContent = title;
  modal.classList.add('show');
  pwdInput.value = '';
  pwdInput.focus();

  return new Promise((resolve) => {
    const confirmBtn = document.getElementById('modalConfirmSubmitBtn');
    const cancelBtn = document.getElementById('modalConfirmCancelBtn');

    const handleConfirm = () => {
      const password = pwdInput.value;
      if (!password) {
        showToast('Password is required!', 'danger');
        return;
      }
      modal.classList.remove('show');
      cleanup();
      
      // inject hidden password input into original form
      let hiddenInput = formElement.querySelector('input[name="confirm_password"]');
      if (!hiddenInput) {
        hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'confirm_password';
        formElement.appendChild(hiddenInput);
      }
      hiddenInput.value = password;
      
      resolve(true);
      formElement.submit();
    };

    const handleCancel = () => {
      modal.classList.remove('show');
      cleanup();
      resolve(false);
    };

    const cleanup = () => {
      confirmBtn.removeEventListener('click', handleConfirm);
      cancelBtn.removeEventListener('click', handleCancel);
    };

    confirmBtn.addEventListener('click', handleConfirm);
    cancelBtn.addEventListener('click', handleCancel);
  });
}

// Logout Confirmation Modal
function openLogoutModal() {
  const modal = document.getElementById('logoutModalBackdrop');
  if (modal) modal.classList.add('show');
}

function closeLogoutModal() {
  const modal = document.getElementById('logoutModalBackdrop');
  if (modal) modal.classList.remove('show');
}

// Close logout modal when clicking outside the card
document.addEventListener('DOMContentLoaded', () => {
  const logoutModal = document.getElementById('logoutModalBackdrop');
  if (logoutModal) {
    logoutModal.addEventListener('click', (e) => {
      if (e.target === logoutModal) closeLogoutModal();
    });
  }

  // Close notification panel on outside click
  document.addEventListener('click', (e) => {
    const wrapper = document.getElementById('notifBellWrapper');
    const panel = document.getElementById('notifPanel');
    if (panel && wrapper && !wrapper.contains(e.target)) {
      panel.classList.remove('open');
    }
  });
});

// Notification Bell Toggle
function toggleNotifPanel(e) {
  e.stopPropagation();
  const panel = document.getElementById('notifPanel');
  if (panel) panel.classList.toggle('open');
}

function closeNotifPanel() {
  const panel = document.getElementById('notifPanel');
  if (panel) panel.classList.remove('open');
}

// Switch between Alerts and Activity tabs
function switchNotifTab(tab) {
  const alertsBody   = document.getElementById('notifBodyAlerts');
  const activityBody = document.getElementById('notifBodyActivity');
  const tabAlerts    = document.getElementById('tabAlerts');
  const tabActivity  = document.getElementById('tabActivity');

  if (!alertsBody || !activityBody) return;

  if (tab === 'alerts') {
    alertsBody.style.display   = 'flex';
    activityBody.style.display = 'none';
    tabAlerts.classList.add('active');
    tabActivity.classList.remove('active');
  } else {
    alertsBody.style.display   = 'none';
    activityBody.style.display = 'flex';
    tabActivity.classList.add('active');
    tabAlerts.classList.remove('active');
  }
}

// Delete a single notification item
function deleteNotifItem(btn) {
  const item = btn.closest('.notif-item');
  if (!item) return;

  const notifId = item.getAttribute('data-id');
  if (notifId && notifId !== '0') {
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    fetch(`/api/notifications/dismiss/${notifId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken || ''
      }
    }).catch(err => console.error("Error dismissing notification:", err));
  }

  item.style.transition = 'opacity 0.2s, max-height 0.25s';
  item.style.opacity = '0';
  item.style.overflow = 'hidden';
  item.style.maxHeight = item.offsetHeight + 'px';
  requestAnimationFrame(() => {
    item.style.maxHeight = '0';
    item.style.padding   = '0';
  });
  setTimeout(() => {
    item.remove();
    _checkEmptyBody();
    _updateNotifBadges();
  }, 260);
}

// Clear all notifications from the currently active tab
function clearAllNotifs() {
  const alertsBody   = document.getElementById('notifBodyAlerts');
  const activityBody = document.getElementById('notifBodyActivity');
  const activeBody   = (activityBody && activityBody.style.display !== 'none') ? activityBody : alertsBody;
  if (!activeBody) return;

  const tabType = (activityBody && activityBody.style.display !== 'none') ? 'activity' : 'alert';
  const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
  fetch('/api/notifications/dismiss-all', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken || ''
    },
    body: JSON.stringify({ type: tabType })
  }).catch(err => console.error("Error dismissing all notifications:", err));

  const items = activeBody.querySelectorAll('.notif-item');
  let delay = 0;
  items.forEach(item => {
    setTimeout(() => {
      item.style.transition = 'opacity 0.18s';
      item.style.opacity = '0';
      setTimeout(() => item.remove(), 200);
    }, delay);
    delay += 40;
  });
  setTimeout(() => {
    _checkEmptyBody();
    _updateNotifBadges();
  }, delay + 220);
}

// Show empty state if all items in a body are gone
function _checkEmptyBody() {
  ['notifBodyAlerts', 'notifBodyActivity'].forEach(id => {
    const body = document.getElementById(id);
    if (!body) return;
    if (!body.querySelector('.notif-item')) {
      if (!body.querySelector('.notif-empty-state')) {
        const iconClass = id === 'notifBodyAlerts' ? 'fa-circle-check' : 'fa-inbox';
        const msg = id === 'notifBodyAlerts' ? 'No alerts right now. Store is running smoothly.' : 'No recent activity yet';
        const iconStyle = id === 'notifBodyAlerts' ? 'style="color: var(--success); opacity: 1;"' : '';
        body.innerHTML = `<div class="notif-empty-state"><i class="fas ${iconClass}" ${iconStyle}></i><div>${msg}</div></div>`;
      }
    }
  });
}

// Recalculate and update the bell badge + both tab badges
function _updateNotifBadges() {
  const alertsBody   = document.getElementById('notifBodyAlerts');
  const activityBody = document.getElementById('notifBodyActivity');
  const tabAlerts    = document.getElementById('tabAlerts');
  const tabActivity  = document.getElementById('tabActivity');
  const bellBadge    = document.querySelector('.notif-badge');

  const alertCount    = alertsBody   ? alertsBody.querySelectorAll('.notif-item').length   : 0;
  const activityCount = activityBody ? activityBody.querySelectorAll('.notif-item').length : 0;
  const totalCount    = alertCount + activityCount;

  // Update bell badge
  if (bellBadge) {
    if (totalCount > 0) {
      bellBadge.textContent = totalCount > 99 ? '99+' : totalCount;
      bellBadge.style.display = '';
    } else {
      bellBadge.style.display = 'none';
    }
  }

  // Update Alerts tab badge
  if (tabAlerts) {
    let badge = tabAlerts.querySelector('.notif-tab-badge');
    if (alertCount > 0) {
      if (!badge) {
        badge = document.createElement('span');
        badge.className = 'notif-tab-badge';
        tabAlerts.appendChild(badge);
      }
      badge.textContent = alertCount;
    } else if (badge) {
      badge.remove();
    }
  }

  // Update Activity tab badge
  if (tabActivity) {
    let badge = tabActivity.querySelector('.notif-tab-badge');
    if (activityCount > 0) {
      if (!badge) {
        badge = document.createElement('span');
        badge.className = 'notif-tab-badge notif-tab-badge-info';
        tabActivity.appendChild(badge);
      }
      badge.textContent = activityCount;
    } else if (badge) {
      badge.remove();
    }
  }
}
