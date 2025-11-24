document.addEventListener("DOMContentLoaded", function () {
  let currentModal = null;
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

  function loadModal(url) {
    fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
      .then((r) => r.text())
      .then((html) => {
        const container = ensureModalContainer();

        if (currentModal) {
          currentModal.hide();
          setTimeout(() => {
            currentModal.dispose();
            const oldModal = container.querySelector("#modalForm");
            if (oldModal) oldModal.remove();
          }, 200);
        }

        container.innerHTML = html;
        const modalEl = container.querySelector("#modalForm");
        if (!modalEl) return;

        currentModal = new bootstrap.Modal(modalEl);
        currentModal.show();

        // Bind form inside modal
        modalEl.querySelectorAll(".ajax-form").forEach((form) => {
          form.addEventListener("submit", function (e) {
            e.preventDefault();
            fetch(form.action, {
              method: "POST",
              body: new FormData(form),
              headers: { "X-Requested-With": "XMLHttpRequest" },
            })
              .then((r) => r.text())
              .then(() => {
                // On success, just reload the page
                window.location.reload();
              })
              .catch((err) => console.error("Form submit error:", err));
          });
        });
      })
      .catch((err) => console.error("Load modal error:", err));
  }

  function bindButtons() {
    document
      .getElementById("openCreateModal")
      ?.addEventListener("click", function () {
        loadModal(this.dataset.url);
      });

    document.querySelectorAll(".openUpdateModal").forEach((btn) => {
      btn.addEventListener("click", function () {
        loadModal(this.dataset.url);
      });
    });

    document.querySelectorAll(".openDeleteModal").forEach((btn) => {
      btn.addEventListener("click", function () {
        loadModal(this.dataset.url);
      });
    });
  }

  bindButtons();
});