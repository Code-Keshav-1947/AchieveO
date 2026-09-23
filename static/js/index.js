/**
 * AchieveO Order Management Software - Core Interactivity
 */

document.addEventListener("DOMContentLoaded", () => {
  // CSRF Helper
  function getCsrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta && meta.content) return meta.content;
    const input = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return input ? input.value : "";
  }

  // 1. Toast Notification System
  const toastEl = document.getElementById("toast");
  let toastTimer = null;

  window.showToast = function (message, type = "info", duration = 2800) {
    if (!toastEl) return;
    toastEl.textContent = message;
    toastEl.className = "toast";
    if (type === "success") toastEl.classList.add("toast-success");
    if (type === "error") toastEl.classList.add("toast-error");
    toastEl.classList.add("show");

    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toastEl.classList.remove("show");
    }, duration);
  };

  // 2. Modal Controller
  function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;
    modal.removeAttribute("hidden");
    modal.classList.add("active");
    document.body.style.overflow = "hidden";
  }

  function closeModal(modal) {
    if (typeof modal === "string") {
      modal = document.getElementById(modal);
    }
    if (!modal) return;
    modal.setAttribute("hidden", "true");
    modal.classList.remove("active");
    document.body.style.overflow = "";
  }

  // Close triggers
  document.querySelectorAll("[data-close-modal]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const modal = btn.closest(".modal-overlay");
      if (modal) closeModal(modal);
    });
  });

  document.querySelectorAll(".modal-overlay").forEach((modal) => {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) {
        closeModal(modal);
      }
    });
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      document.querySelectorAll(".modal-overlay.active, .modal-overlay:not([hidden])").forEach((m) => {
        closeModal(m);
      });
    }
  });

  // Modal Open Buttons
  const openOrderBtn = document.getElementById("openOrderModalBtn");
  if (openOrderBtn) {
    openOrderBtn.addEventListener("click", () => {
      openModal("orderModal");
      updateOrderCalculations();
    });
  }

  const openCustBtn = document.getElementById("openCustomerModalBtn");
  if (openCustBtn) {
    openCustBtn.addEventListener("click", () => openModal("customerModal"));
  }

  const openProdBtn = document.getElementById("openProductModalBtn");
  if (openProdBtn) {
    openProdBtn.addEventListener("click", () => openModal("productModal"));
  }

  const quickAddCust = document.getElementById("quickAddCustomerTrigger");
  if (quickAddCust) {
    quickAddCust.addEventListener("click", (e) => {
      e.preventDefault();
      openModal("customerModal");
    });
  }

  const quickAddProd = document.getElementById("quickAddProductTrigger");
  if (quickAddProd) {
    quickAddProd.addEventListener("click", (e) => {
      e.preventDefault();
      openModal("productModal");
    });
  }

  // 3. Live Price & Balance Calculations in New Order Modal
  const productSelect = document.getElementById("orderProductSelect");
  const quantityInput = document.getElementById("orderQuantityInput");
  const advanceInput = document.getElementById("orderAdvanceInput");
  const calcUnitPrice = document.getElementById("calcUnitPrice");
  const calcTotalValue = document.getElementById("calcTotalValue");
  const calcAdvance = document.getElementById("calcAdvance");
  const calcBalance = document.getElementById("calcBalance");

  function updateOrderCalculations() {
    if (!productSelect || !quantityInput || !advanceInput) return;
    const selectedOpt = productSelect.options[productSelect.selectedIndex];
    const unitPrice = selectedOpt ? parseFloat(selectedOpt.dataset.price) || 0 : 0;
    const quantity = parseInt(quantityInput.value) || 1;
    const advance = parseFloat(advanceInput.value) || 0;

    const totalValue = unitPrice * quantity;
    const balance = Math.max(0, totalValue - advance);

    if (calcUnitPrice) calcUnitPrice.textContent = `₹${unitPrice}`;
    if (calcTotalValue) calcTotalValue.textContent = `₹${totalValue}`;
    if (calcAdvance) calcAdvance.textContent = `₹${advance}`;
    if (calcBalance) calcBalance.textContent = `₹${balance}`;
  }

  if (productSelect) productSelect.addEventListener("change", updateOrderCalculations);
  if (quantityInput) quantityInput.addEventListener("input", updateOrderCalculations);
  if (advanceInput) advanceInput.addEventListener("input", updateOrderCalculations);

  // 4. AJAX Submission for Quick Customer Creation
  const quickCustomerForm = document.getElementById("quickCustomerForm");
  if (quickCustomerForm) {
    quickCustomerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(quickCustomerForm);
      try {
        const response = await fetch(quickCustomerForm.action + "?format=json", {
          method: "POST",
          headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCsrfToken(),
          },
          body: formData,
        });
        const data = await response.json();
        if (response.ok && data.status === "success") {
          // Add to order customer select
          const custSelect = document.getElementById("orderCustomerSelect");
          if (custSelect) {
            const opt = document.createElement("option");
            opt.value = data.id;
            opt.textContent = `${data.name} ${data.mobile_no ? `(${data.mobile_no})` : ""}`;
            opt.selected = true;
            custSelect.appendChild(opt);
          }
          quickCustomerForm.reset();
          closeModal("customerModal");
          showToast(`Customer "${data.name}" added successfully!`, "success");
        } else {
          showToast("Failed to save customer. Please check fields.", "error");
        }
      } catch (err) {
        showToast("Error saving customer.", "error");
      }
    });
  }

  // 5. AJAX Submission for Quick Product Creation
  const quickProductForm = document.getElementById("quickProductForm");
  if (quickProductForm) {
    quickProductForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(quickProductForm);
      try {
        const response = await fetch(quickProductForm.action + "?format=json", {
          method: "POST",
          headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCsrfToken(),
          },
          body: formData,
        });
        const data = await response.json();
        if (response.ok && data.status === "success") {
          // Add to order product select
          const prodSelect = document.getElementById("orderProductSelect");
          if (prodSelect) {
            const opt = document.createElement("option");
            opt.value = data.id;
            opt.dataset.price = data.price;
            opt.dataset.cost = data.cost_price;
            opt.textContent = `${data.name} (₹${data.price}/unit)`;
            opt.selected = true;
            prodSelect.appendChild(opt);
          }
          quickProductForm.reset();
          closeModal("productModal");
          updateOrderCalculations();
          showToast(`Product "${data.name}" added successfully!`, "success");
        } else {
          showToast("Failed to save product. Please check fields.", "error");
        }
      } catch (err) {
        showToast("Error saving product.", "error");
      }
    });
  }

  // 6. Real-time Search and Filtering for Orders Table
  const searchInput = document.getElementById("orderSearchInput");
  const statusFilter = document.getElementById("orderStatusFilter");
  const paymentFilter = document.getElementById("orderPaymentFilter");
  const resetFiltersBtn = document.getElementById("resetFiltersBtn");
  const orderRows = document.querySelectorAll(".order-row");
  const resultCount = document.getElementById("resultCount");
  const noResultsMsg = document.getElementById("noResultsMsg");

  function applyFilters() {
    if (!orderRows.length) return;
    const query = (searchInput ? searchInput.value : "").trim().toLowerCase();
    const statusVal = (statusFilter ? statusFilter.value : "").toLowerCase();
    const payVal = (paymentFilter ? paymentFilter.value : "").toLowerCase();

    let visibleCount = 0;

    orderRows.forEach((row) => {
      const customer = row.dataset.customer || "";
      const mobile = row.dataset.mobile || "";
      const job = row.dataset.job || "";
      const product = row.dataset.product || "";
      const status = (row.dataset.status || "").toLowerCase();
      const payment = (row.dataset.payment || "").toLowerCase();
      const orderId = row.dataset.orderId || "";

      const matchQuery =
        !query ||
        customer.includes(query) ||
        mobile.includes(query) ||
        job.includes(query) ||
        product.includes(query) ||
        orderId.includes(query);

      const matchStatus = !statusVal || status === statusVal;
      const matchPayment = !payVal || payment === payVal;

      if (matchQuery && matchStatus && matchPayment) {
        row.style.display = "";
        visibleCount++;
      } else {
        row.style.display = "none";
      }
    });

    if (resultCount) {
      resultCount.textContent = `${visibleCount} ${visibleCount === 1 ? "record" : "records"}`;
    }

    if (noResultsMsg) {
      noResultsMsg.style.display = visibleCount === 0 ? "block" : "none";
    }
  }

  if (searchInput) searchInput.addEventListener("input", applyFilters);
  if (statusFilter) statusFilter.addEventListener("change", applyFilters);
  if (paymentFilter) paymentFilter.addEventListener("change", applyFilters);

  if (resetFiltersBtn) {
    resetFiltersBtn.addEventListener("click", () => {
      if (searchInput) searchInput.value = "";
      if (statusFilter) statusFilter.value = "";
      if (paymentFilter) paymentFilter.value = "";
      applyFilters();
    });
  }

  // 7. View Switcher (Table vs Kanban)
  const tableViewToggle = document.getElementById("tableViewToggle");
  const kanbanViewToggle = document.getElementById("kanbanViewToggle");
  const tableView = document.getElementById("tableView");
  const kanbanView = document.getElementById("kanbanView");

  if (tableViewToggle && kanbanViewToggle && tableView && kanbanView) {
    tableViewToggle.addEventListener("click", () => {
      tableViewToggle.classList.add("active");
      kanbanViewToggle.classList.remove("active");
      tableView.style.display = "block";
      kanbanView.style.display = "none";
    });

    kanbanViewToggle.addEventListener("click", () => {
      kanbanViewToggle.classList.add("active");
      tableViewToggle.classList.remove("active");
      tableView.style.display = "none";
      kanbanView.style.display = "grid";
    });
  }

  // 8. Quick Status Update Handler
  const statusModal = document.getElementById("statusModal");
  const statusOrderIdInput = document.getElementById("statusModalOrderId");
  const targetStatusSelect = document.getElementById("targetStatusSelect");
  const statusModalSubtitle = document.getElementById("statusModalSubtitle");

  document.querySelectorAll(".quick-status-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const orderId = btn.dataset.orderId;
      const currentStatus = btn.dataset.currentStatus;
      const jobName = btn.dataset.jobName || `#${orderId}`;

      if (statusOrderIdInput) statusOrderIdInput.value = orderId;
      if (targetStatusSelect) targetStatusSelect.value = currentStatus;
      if (statusModalSubtitle) statusModalSubtitle.textContent = `Order #${orderId} - ${jobName}`;

      openModal("statusModal");
    });
  });

  const quickStatusForm = document.getElementById("quickStatusForm");
  if (quickStatusForm) {
    quickStatusForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const orderId = statusOrderIdInput.value;
      const newStatus = targetStatusSelect.value;
      if (!orderId || !newStatus) return;

      const formData = new FormData();
      formData.append("status", newStatus);

      try {
        const response = await fetch(`/orders/${orderId}/update-status/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": getCsrfToken(),
          },
          body: formData,
        });
        const data = await response.json();
        if (response.ok && data.status === "success") {
          closeModal("statusModal");
          showToast(`Order #${orderId} updated to ${data.status_display}!`, "success");
          // Reload slightly after to refresh pipeline stats cleanly
          setTimeout(() => window.location.reload(), 500);
        } else {
          showToast(data.message || "Failed to update status", "error");
        }
      } catch (err) {
        showToast("Error updating status.", "error");
      }
    });
  }

  // 9. Kanban Drag and Drop Status Updater
  const cards = document.querySelectorAll(".order-card");
  const dropLanes = document.querySelectorAll(".cards");

  cards.forEach((card) => {
    card.addEventListener("dragstart", (e) => {
      e.dataTransfer.setData("text/plain", card.dataset.orderId);
      card.classList.add("dragging");
    });
    card.addEventListener("dragend", () => {
      card.classList.remove("dragging");
    });
  });

  dropLanes.forEach((lane) => {
    lane.addEventListener("dragover", (e) => {
      e.preventDefault();
      lane.classList.add("drag-over");
    });
    lane.addEventListener("dragleave", () => {
      lane.classList.remove("drag-over");
    });
    lane.addEventListener("drop", async (e) => {
      e.preventDefault();
      lane.classList.remove("drag-over");
      const orderId = e.dataTransfer.getData("text/plain");
      const targetStatus = lane.dataset.status;

      if (!orderId || !targetStatus) return;

      const card = document.querySelector(`.order-card[data-order-id="${orderId}"]`);
      if (card) {
        lane.appendChild(card);
      }

      const formData = new FormData();
      formData.append("status", targetStatus);

      try {
        const response = await fetch(`/orders/${orderId}/update-status/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": getCsrfToken(),
          },
          body: formData,
        });
        const data = await response.json();
        if (response.ok && data.status === "success") {
          showToast(`Order #${orderId} moved to ${data.status_display}!`, "success");
        } else {
          showToast("Failed to move order.", "error");
        }
      } catch (err) {
        showToast("Network error moving order.", "error");
      }
    });
  });
});
