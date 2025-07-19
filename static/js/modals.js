document.addEventListener('DOMContentLoaded', function () {
  const modalEl = document.getElementById('modalForm');
  let modal = null;

  if (modalEl) {
    modal = new bootstrap.Modal(modalEl);
  }

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
    document.getElementById("toast-container")?.appendChild(toast);

    setTimeout(() => {
      toast.remove();
    }, 3500);
  }

  function clearFormErrors(form) {
    // Remove any existing error messages
    form.querySelectorAll('.invalid-feedback').forEach(el => el.remove());
    // Remove invalid classes
    form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
  }

  function showFormErrors(form, errors) {
    for (const [fieldName, messages] of Object.entries(errors)) {
      const field = form.querySelector(`[name="${fieldName}"]`);
      if (field) {
        // Mark field invalid
        field.classList.add('is-invalid');
        // Create error message element
        let errorEl = document.createElement('div');
        errorEl.classList.add('invalid-feedback');
        errorEl.innerHTML = messages.join('<br>');
        // Insert after the field
        if (field.nextSibling) {
          field.parentNode.insertBefore(errorEl, field.nextSibling);
        } else {
          field.parentNode.appendChild(errorEl);
        }
      }
    }
  }

  function loadForm(url) {
    fetch(url, {
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    .then(res => res.json())
    .then(data => {
      if (!data.success && modalEl) {
        modalEl.querySelector('.modal-dialog').innerHTML = data.html;
        bindForms(); // Re-bind submit handler
        modal?.show();
      }
    });
  }

  function bindForms() {
    document.querySelectorAll('.ajax-form').forEach(form => {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        clearFormErrors(form);

        fetch(form.action, {
          method: 'POST',
          body: new FormData(form),
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            showToast("Success", data.message || "Operation completed.", "success");
            modal?.hide();
            setTimeout(() => location.reload(), 1000);
          } else if (modalEl) {
            modalEl.querySelector('.modal-dialog').innerHTML = data.html;
            bindForms(); // Rebind in new content

            // Show inline validation errors if any
            if (data.errors) {
              const newForm = modalEl.querySelector('.ajax-form');
              showFormErrors(newForm, data.errors);
            }
          }
        })
        .catch(() => {
          showToast("Error", "Something went wrong. Please try again.", "danger");
        });
      });
    });
  }

  function bindButtons() {
    document.getElementById('openCreateModal')?.addEventListener('click', function () {
      const url = this.getAttribute('data-url');
      if (url) loadForm(url);
    });

    document.querySelectorAll('.openUpdateModal').forEach(btn => {
      btn.addEventListener('click', function () {
        const url = this.getAttribute('data-url');
        if (url) loadForm(url);
      });
    });

    document.querySelectorAll('.openDeleteModal').forEach(btn => {
      btn.addEventListener('click', function () {
        const url = this.getAttribute('data-url');
        if (url) loadForm(url);
      });
    });
  }

  bindButtons();
  bindForms();
});