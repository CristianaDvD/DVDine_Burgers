document.addEventListener("DOMContentLoaded", function () {
  let bootstrapModal = null;
  const modalContainerId = "modalContainer";

  function ensureModalContainer() {
    let container = document.getElementById(modalContainerId);
    if (!container) {
      container = document.createElement("div");
      container.id = modalContainerId;
      document.body.appendChild(container);
    }
    return container;
  }

  function showToast(title, message, type = "success") {
    const toastContainer =
      document.getElementById("toast-container") ||
      (() => {
        const container = document.createElement("div");
        container.id = "toast-container";
        container.className = "toast-container position-fixed bottom-0 end-0 p-3";
        document.body.appendChild(container);
        return container;
      })();

    const toastId = "toast-" + Math.floor(Math.random() * 10000);
    const toast = document.createElement("div");
    toast.className = `toast align-items-center text-white bg-${type} border-0 show`;
    toast.id = toastId;
    toast.role = "alert";
    toast.ariaLive = "assertive";
    toast.ariaAtomic = "true";
    toast.style.minWidth = "250px";
    toast.style.marginBottom = "0.5rem";
    toast.innerHTML = `
      <div class="d-flex">
        <div class="toast-body">
          <strong>${title}</strong><br>${message}
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
    `;
    toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.remove();
    }, 4000);
  }

  function loadModal(url) {
    fetch(url, {
      headers: { "X-Requested-With": "XMLHttpRequest" },
    })
      .then((response) => response.text())
      .then((html) => {
        const container = ensureModalContainer();
        container.innerHTML = html;

        const modalEl = container.querySelector("#modalForm");
        if (!modalEl) {
          console.error("Modal element not found in response.");
          return;
        }

        setTimeout(() => {
          if (bootstrapModal) bootstrapModal.dispose();
          bootstrapModal = new bootstrap.Modal(modalEl);
          bootstrapModal.show();
          bindForms(modalEl);
        }, 10);
      })
      .catch((err) => {
        console.error("Error loading modal:", err);
        showToast("Error", "Unable to load modal", "danger");
      });
  }

  function bindForms(modalEl) {
    modalEl.querySelectorAll(".ajax-form").forEach((form) => {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        fetch(form.action, {
          method: "POST",
          body: new FormData(form),
          headers: { "X-Requested-With": "XMLHttpRequest" },
        })
          .then((response) => response.text())
          .then((html) => {
            const container = ensureModalContainer();
            container.innerHTML = html;

            const newModalEl = container.querySelector("#modalForm");

            // If modal missing, assume full page and reload UI
            if (!newModalEl) {
              document.body.innerHTML = html;
              bindButtons();
              showToast("Success", "Booking updated", "success");
              return;
            }

            const formErrors = newModalEl.querySelector(".alert-danger");
            if (!formErrors) {
              bootstrapModal.hide();
              showToast("Success", "Action completed", "success");

              // Optional: full page reload if list was updated
              setTimeout(() => {
                window.location.href = window.location.href;
              }, 1000);
              return;
            }

            // Modal still has errors, rebinding form
            if (bootstrapModal) bootstrapModal.dispose();
            bootstrapModal = new bootstrap.Modal(newModalEl);
            bootstrapModal.show();
            bindForms(newModalEl);
            showToast("Error", "Please correct the form errors", "danger");
          })
          .catch((err) => {
            console.error("Form submission error:", err);
            showToast("Error", "Submission failed", "danger");
          });
      });
    });
  }

  function bindButtons() {
    document.getElementById("openCreateModal")?.addEventListener("click", function () {
      const url = this.getAttribute("data-url");
      if (url) loadModal(url);
    });

    document.querySelectorAll(".openUpdateModal").forEach((btn) => {
      btn.addEventListener("click", function () {
        const url = this.getAttribute("data-url");
        if (url) loadModal(url);
      });
    });

    document.querySelectorAll(".openDeleteModal").forEach((btn) => {
      btn.addEventListener("click", function () {
        const url = this.getAttribute("data-url");
        if (url) loadModal(url);
      });
    });
  }

  bindButtons(); // initial
});