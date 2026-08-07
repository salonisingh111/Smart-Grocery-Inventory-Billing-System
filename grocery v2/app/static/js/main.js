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
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 300);
    }, 4000);
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
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
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
