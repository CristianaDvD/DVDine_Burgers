// Modals
document.addEventListener('DOMContentLoaded', function () {
  const modal = new bootstrap.Modal(document.getElementById('modalForm'));

  function showToast(title, message, type = 'success') {
    const toastId = "toast-" + Math.floor(Math.random() * 10000);
    const toast = document.createElement("div");
    toast.className = `toast align-items-center text-white bg-${type} border-0 show`;
    toast.id = toastId;
    toast.role = "alert";
    toast.ariaLive = "assertive";
    toast.ariaAtomic = "true";
    toast.style.minWidth = '250px';
    toast.style.marginBottom = '0.5rem';
    toast.innerHTML = `
      <div class="d-flex">
        <div class="toast-body">
          <strong>${title}</strong><br>${message}
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
      </div>
    `;
    document.getElementById("toast-container").appendChild(toast);

    setTimeout(() => {
      toast.remove();
    }, 3500);
  }

  function loadForm(url) {
    fetch(url, {headers: {'X-Requested-With': 'XMLHttpRequest'}})
    .then(res => res.json())
    .then(data => {
      if (!data.success) {
        document.body.innerHTML = data.html;
        bindButtons();
        bindForms();
        modal.show();
      }
    });
  }

  function bindForms() {
    document.querySelectorAll('.ajax-form').forEach(form => {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        fetch(form.action, {
          method: 'POST',
          body: new FormData(form),
          headers: {'X-Requested-With': 'XMLHttpRequest'}
        })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            showToast("Success", data.message, "success");
            modal.hide();
            // Reload page after short delay to update list
            setTimeout(() => location.reload(), 1000);
          } else {
            document.body.innerHTML = data.html;
            bindButtons();
            bindForms();
            modal.show();
          }
        });
      });
    });
  }

  function bindButtons() {
    document.getElementById('openCreateModal')?.addEventListener('click', function () {
      loadForm(this.getAttribute('data-url'));
    });
    document.querySelectorAll('.openUpdateModal').forEach(btn => {
      btn.addEventListener('click', function () {
        loadForm(this.getAttribute('data-url'));
      });
    });
    document.querySelectorAll('.openDeleteModal').forEach(btn => {
      btn.addEventListener('click', function () {
        loadForm(this.getAttribute('data-url'));
      });
    });
  }

  bindButtons();
  bindForms();
});