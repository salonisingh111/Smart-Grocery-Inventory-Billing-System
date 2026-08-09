class POSBilling {
  constructor() {
    this.cart = [];
    this.products = window.posProducts || [];
    this.currency = window.posCurrency || '₹';
    this.discountAmount = 0.0;
    this.selectedCustomerId = null;
    this.paymentMethod = 'Cash';
    this.drawerOpen = false;

    this.currentSubtotal = 0.0;
    this.currentTax = 0.0;
    this.currentNet = 0.0;

    this.activeCategoryFilter = '';
    this.init();
  }

  init() {
    const searchInput = document.getElementById('posSearchInput');
    if (searchInput) {
      const resetSearch = () => {
        if (searchInput.value === 'admin' || searchInput.value === 'amul' || searchInput.matches(':-webkit-autofill')) {
          searchInput.value = '';
          this.applyFilters();
        }
      };
      searchInput.value = '';
      setTimeout(resetSearch, 50);
      setTimeout(resetSearch, 300);

      searchInput.addEventListener('focus', () => {
        searchInput.removeAttribute('readonly');
        resetSearch();
      });
    }
    this.bindEvents();
    this.renderCart();
  }

  bindEvents() {
    const searchInput = document.getElementById('posSearchInput');
    if (searchInput) {
      searchInput.addEventListener('input', () => this.applyFilters());
      
      // Barcode scanner auto submit on Enter
      searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          this.handleBarcodeScan(searchInput.value.trim());
        }
      });
    }

    const customerSelect = document.getElementById('posCustomerSelect');
    if (customerSelect) {
      customerSelect.addEventListener('change', (e) => {
        this.selectedCustomerId = e.target.value ? parseInt(e.target.value) : null;
      });
    }

    const discountInput = document.getElementById('posDiscountInput');
    if (discountInput) {
      discountInput.addEventListener('input', (e) => {
        this.discountAmount = parseFloat(e.target.value) || 0.0;
        this.renderCart();
      });
    }
  }

  filterByCategory(catQuery, btnElement) {
    this.activeCategoryFilter = catQuery ? catQuery.toLowerCase().trim() : '';

    if (btnElement) {
      document.querySelectorAll('#posCategoryChips .cat-chip').forEach(b => b.classList.remove('active'));
      btnElement.classList.add('active');
    }

    this.applyFilters();
  }

  applyFilters() {
    const grid = document.getElementById('posProductGrid');
    if (!grid) return;

    const searchInput = document.getElementById('posSearchInput');
    const q = searchInput ? searchInput.value.toLowerCase().trim() : '';
    const cat = this.activeCategoryFilter;

    const filtered = this.products.filter(p => {
      const matchSearch = !q || (
        p.name.toLowerCase().includes(q) ||
        (p.sku && p.sku.toLowerCase().includes(q)) ||
        (p.barcode && p.barcode.includes(q)) ||
        (p.brand && p.brand.toLowerCase().includes(q))
      );

      const categoryName = (p.category_name || '').toLowerCase();
      const matchCat = !cat || categoryName.includes(cat);

      return matchSearch && matchCat;
    });

    this.renderProductGrid(filtered);
  }

  handleSearch(query) {
    const searchInput = document.getElementById('posSearchInput');
    if (searchInput) searchInput.value = query;
    this.applyFilters();
  }

  handleBarcodeScan(code) {
    if (!code) return;
    const match = this.products.find(p => p.barcode === code || p.sku === code);
    if (match) {
      this.addToCart(match);
      document.getElementById('posSearchInput').value = '';
    } else {
      showToast(`No product found with barcode: ${code}`, 'warning');
    }
  }

  getCategoryMeta(catName) {
    const cat = (catName || '').toLowerCase();
    if (cat.includes('dairy')) return { icon: 'fa-wine-bottle', bg: 'linear-gradient(135deg, #3b82f6, #1d4ed8)', badgeClass: 'badge-primary' };
    if (cat.includes('bev')) return { icon: 'fa-glass-water', bg: 'linear-gradient(135deg, #06b6d4, #0284c7)', badgeClass: 'badge-info' };
    if (cat.includes('snack')) return { icon: 'fa-cookie-bite', bg: 'linear-gradient(135deg, #f59e0b, #d97706)', badgeClass: 'badge-warning' };
    if (cat.includes('fruit') || cat.includes('veg')) return { icon: 'fa-apple-whole', bg: 'linear-gradient(135deg, #10b981, #059669)', badgeClass: 'badge-success' };
    if (cat.includes('staple') || cat.includes('grain')) return { icon: 'fa-wheat-awn', bg: 'linear-gradient(135deg, #eab308, #ca8a04)', badgeClass: 'badge-secondary' };
    if (cat.includes('care') || cat.includes('clean')) return { icon: 'fa-pump-soap', bg: 'linear-gradient(135deg, #a855f7, #7e22ce)', badgeClass: 'badge-danger' };
    return { icon: 'fa-basket-shopping', bg: 'linear-gradient(135deg, #6366f1, #4338ca)', badgeClass: 'badge-secondary' };
  }

  renderProductGrid(items) {
    const grid = document.getElementById('posProductGrid');
    if (!grid) return;

    if (items.length === 0) {
      grid.innerHTML = '<div class="text-center p-4 text-muted" style="grid-column: 1 / -1;">No matching products found.</div>';
      return;
    }

    grid.innerHTML = items.map(p => {
      const meta = this.getCategoryMeta(p.category_name);
      let stockBadgeHtml = '';
      if (p.quantity <= 0) {
        stockBadgeHtml = `<span class="stock-pill stock-out"><i class="fas fa-circle-xmark"></i> Out</span>`;
      } else if (p.quantity <= p.min_stock) {
        stockBadgeHtml = `<span class="stock-pill stock-low"><i class="fas fa-triangle-exclamation"></i> ${p.quantity} ${p.unit}</span>`;
      } else {
        stockBadgeHtml = `<span class="stock-pill stock-ok"><i class="fas fa-check-circle"></i> ${p.quantity} ${p.unit}</span>`;
      }

      return `
        <div class="pos-product-card ${p.quantity <= 0 ? 'disabled' : ''}" onclick="posSystem.addToCartById(${p.id})">
          <span class="pos-cat-badge-overlay">${p.category_name || 'Grocery'}</span>
          <div class="pos-prod-img-wrap">
            ${p.image ? `<img src="/static/${p.image}" alt="${p.name}">` : `<div class="pos-prod-icon" style="background: ${meta.bg}; width: 44px; height: 44px; border-radius: var(--radius-sm); color: white; display: flex; align-items: center; justify-content: center; font-size: 1.2rem;"><i class="fas ${meta.icon}"></i></div>`}
          </div>
          <div class="pos-prod-details">
            <div class="pos-prod-brand">${p.brand || 'Grocery'}</div>
            <div class="pos-prod-name" title="${p.name}">${p.name}</div>
          </div>
          <div class="pos-prod-footer">
            <div class="pos-prod-price">${this.currency}${p.selling_price.toFixed(2)}</div>
            ${stockBadgeHtml}
          </div>
        </div>
      `;
    }).join('');
  }

  addToCartById(id) {
    const product = this.products.find(p => p.id === id);
    if (product) this.addToCart(product);
  }

  addToCart(product) {
    if (product.quantity <= 0) {
      showToast(`'${product.name}' is out of stock!`, 'danger');
      return;
    }

    const existing = this.cart.find(item => item.product_id === product.id);
    if (existing) {
      if (existing.quantity + 1 > product.quantity) {
        showToast(`Stock limit reached for '${product.name}'`, 'warning');
        return;
      }
      existing.quantity += 1;
    } else {
      this.cart.push({
        product_id: product.id,
        name: product.name,
        selling_price: product.selling_price,
        tax_percent: product.tax_percent || 0.0,
        quantity: 1,
        max_stock: product.quantity
      });
    }

    this.renderCart();
  }

  updateQuantity(index, delta) {
    const item = this.cart[index];
    if (!item) return;

    const newQty = item.quantity + delta;
    if (newQty <= 0) {
      this.cart.splice(index, 1);
    } else if (newQty > item.max_stock) {
      showToast(`Stock limit reached for '${item.name}'`, 'warning');
    } else {
      item.quantity = newQty;
    }

    this.renderCart();
  }

  removeFromCart(index) {
    this.cart.splice(index, 1);
    this.renderCart();
  }

  toggleCartDrawer() {
    const drawer = document.getElementById('posCartDrawer');
    const chevron = document.getElementById('drawerChevron');
    if (!drawer) return;

    this.drawerOpen = !this.drawerOpen;
    if (this.drawerOpen) {
      drawer.style.display = 'block';
      if (chevron) chevron.className = 'fas fa-chevron-down';
    } else {
      drawer.style.display = 'none';
      if (chevron) chevron.className = 'fas fa-chevron-up';
    }
  }

  renderCart() {
    const bottomBar = document.getElementById('posBottomBar');
    const tableBody = document.getElementById('posCartTableBody');

    if (this.cart.length === 0) {
      if (bottomBar) bottomBar.style.display = 'none';
      if (tableBody) tableBody.innerHTML = '<tr><td colspan="5" class="text-center p-3 text-muted">No items chosen yet</td></tr>';
      this.updateTotals(0, 0, 0, 0, 0);
      return;
    }

    if (bottomBar) bottomBar.style.display = 'flex';

    let subtotal = 0.0;
    let taxTotal = 0.0;
    let totalQty = 0;

    if (tableBody) {
      tableBody.innerHTML = this.cart.map((item, idx) => {
        const itemSubtotal = item.selling_price * item.quantity;
        const itemTax = (itemSubtotal * item.tax_percent) / 100.0;
        const itemTotal = itemSubtotal + itemTax;

        subtotal += itemSubtotal;
        taxTotal += itemTax;
        totalQty += item.quantity;

        return `
          <tr>
            <td><strong>${item.name}</strong></td>
            <td>${this.currency}${item.selling_price.toFixed(2)}</td>
            <td>
              <div class="cart-qty-ctrl">
                <button class="btn btn-sm btn-secondary" onclick="posSystem.updateQuantity(${idx}, -1)">-</button>
                <span style="font-weight: 700;">${item.quantity}</span>
                <button class="btn btn-sm btn-secondary" onclick="posSystem.updateQuantity(${idx}, 1)">+</button>
              </div>
            </td>
            <td><strong>${this.currency}${itemTotal.toFixed(2)}</strong></td>
            <td>
              <button class="btn btn-sm btn-danger" onclick="posSystem.removeFromCart(${idx})">
                <i class="fas fa-trash"></i>
              </button>
            </td>
          </tr>
        `;
      }).join('');
    }

    const gross = subtotal + taxTotal;
    const finalGross = Math.max(0.0, gross - this.discountAmount);
    const netAmount = Math.round(finalGross);

    this.updateTotals(subtotal, taxTotal, this.discountAmount, netAmount, totalQty);
  }

  updateTotals(subtotal, tax, discount, net, totalQty = 0) {
    this.currentSubtotal = subtotal;
    this.currentTax = tax;
    this.currentNet = net;

    const bottomItemCount = document.getElementById('bottomItemCount');
    const bottomTotalAmount = document.getElementById('bottomTotalAmount');

    if (bottomItemCount) bottomItemCount.textContent = `${totalQty} ${totalQty === 1 ? 'Item' : 'Items'}`;
    if (bottomTotalAmount) bottomTotalAmount.textContent = `${this.currency}${net.toFixed(2)}`;
  }

  openCheckoutModal() {
    if (this.cart.length === 0) {
      showToast('Cart is empty. Please select products first.', 'warning');
      return;
    }

    const modalSubtotal = document.getElementById('modalSubtotal');
    const modalTaxTotal = document.getElementById('modalTaxTotal');
    const modalNetTotal = document.getElementById('modalNetTotal');

    if (modalSubtotal) modalSubtotal.textContent = `${this.currency}${this.currentSubtotal.toFixed(2)}`;
    if (modalTaxTotal) modalTaxTotal.textContent = `${this.currency}${this.currentTax.toFixed(2)}`;
    if (modalNetTotal) modalNetTotal.textContent = `${this.currency}${this.currentNet.toFixed(2)}`;

    const modal = document.getElementById('posCheckoutModal');
    if (modal) modal.classList.add('show');
  }

  closeCheckoutModal() {
    const modal = document.getElementById('posCheckoutModal');
    if (modal) modal.classList.remove('show');
  }

  selectPaymentMethod(method, btnElement) {
    this.paymentMethod = method;
    document.querySelectorAll('.payment-btn').forEach(b => b.classList.remove('active'));
    if (btnElement) btnElement.classList.add('active');
  }

  async start3SecPaymentAnimation() {
    this.closeCheckoutModal();

    const overlay = document.getElementById('paymentOverlay');
    const spinner = document.getElementById('paymentSpinner');
    const checkmark = document.getElementById('paymentCheckmark');
    const title = document.getElementById('paymentTitle');
    const methodSpan = document.getElementById('paymentMethodName');

    if (!overlay || !spinner || !checkmark || !title) return;

    if (methodSpan) methodSpan.textContent = this.paymentMethod;

    // Reset Animation State
    spinner.style.display = 'block';
    checkmark.style.display = 'none';
    title.textContent = 'Processing Payment...';
    overlay.classList.add('show');

    // Step 1: 0ms - 1500ms (Pulsing Spinner)
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Step 2: 1500ms - 3000ms (Glowing Green Success Checkmark)
    spinner.style.display = 'none';
    checkmark.style.display = 'flex';
    title.textContent = 'Payment Completed!';

    await new Promise(resolve => setTimeout(resolve, 1500));

    // Step 3: Execute Backend Order Commit
    await this.processCheckout();
  }

  async processCheckout() {
    const payload = {
      customer_id: this.selectedCustomerId,
      items: this.cart,
      payment_method: this.paymentMethod,
      discount_amount: this.discountAmount,
      notes: ''
    };

    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;

    try {
      const response = await fetch('/billing/api/checkout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(payload)
      });

      const res = await response.json();
      const overlay = document.getElementById('paymentOverlay');
      if (overlay) overlay.classList.remove('show');

      if (res.success) {
        showToast(`Bill #${res.bill_number} created successfully!`, 'success');
        window.location.href = `/billing/invoice/${res.bill_id}`;
      } else {
        showToast(res.message || 'Checkout failed', 'danger');
      }
    } catch (err) {
      const overlay = document.getElementById('paymentOverlay');
      if (overlay) overlay.classList.remove('show');
      showToast('Network or server error occurred during checkout.', 'danger');
    }
  }

  async saveQuickCustomer() {
    const name = document.getElementById('quickCustName')?.value.trim();
    const phone = document.getElementById('quickCustPhone')?.value.trim();
    const email = document.getElementById('quickCustEmail')?.value.trim();

    if (!name || !phone) {
      showToast('Customer Name and Phone Number are required.', 'warning');
      return;
    }

    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
    try {
      const response = await fetch('/billing/api/quick-create-customer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ name, phone, email })
      });

      const res = await response.json();
      if (res.success) {
        const custSelect = document.getElementById('posCustomerSelect');
        if (custSelect && res.customer) {
          const opt = document.createElement('option');
          opt.value = res.customer.id;
          opt.textContent = `${res.customer.name} (${res.customer.phone})`;
          opt.selected = true;
          custSelect.appendChild(opt);
          this.selectedCustomerId = res.customer.id;
        }
        document.getElementById('posNewCustomerModal')?.classList.remove('show');
        showToast(res.message || 'Customer saved and selected!', 'success');
      } else {
        showToast(res.message || 'Failed to save customer', 'danger');
      }
    } catch (e) {
      showToast('Error saving quick customer.', 'danger');
    }
  }
}

let posSystem;
document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('posProductGrid')) {
    posSystem = new POSBilling();
  }
});
