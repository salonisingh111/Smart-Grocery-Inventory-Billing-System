/* ==========================================================================
   suppliers.js — Vendor Management SPA Logic
   SmartBilling | Inventory Management Module
   Single-Page Application with hash-based routing (#list, #detail/:id)
   ========================================================================== */

'use strict';

// ============================================================
// 1. DATA LAYER — Master supplier & catalog data
// ============================================================
let suppliers = [
    {
        id: 'SUP-001',
        companyName: 'Hindustan Unilever Limited (HUL)',
        gst: '27AAACH1123A1Z2',
        contactPerson: 'Suresh Narayanan',
        phone: '+91 22 2824 8000',
        email: 'corporate.communication@hul.com',
        address: 'Unilever House, B. D. Sawant Marg, Chakala, Andheri (E)',
        city: 'Mumbai',
        paymentTerms: 'Net 30',
        status: 'Verified',
        isPreferred: true,
        logoUrl: 'https://images.unsplash.com/photo-1556742049-0a670fc8a5d7?w=128&auto=format&fit=crop&q=80',
        notes: 'Primary supplier for personal care and packaged food brands.',
        productsSupplied: ['Soap', 'Shampoo', 'Tea', 'Detergent', 'Ketchup'],
        catalog: [
            { id: 'PROD-001', name: 'Dove Cream Beauty Bathing Bar (75g)', category: 'Personal Care', price: 1.50, stock: 450 },
            { id: 'PROD-002', name: 'Sunsilk Black Shine Shampoo (650ml)', category: 'Personal Care', price: 5.20, stock: 180 },
            { id: 'PROD-003', name: 'Brooke Bond Red Label Tea (500g)', category: 'Beverages', price: 3.80, stock: 320 },
            { id: 'PROD-004', name: 'Surf Excel Easy Wash Detergent (1kg)', category: 'Household', price: 2.90, stock: 500 },
            { id: 'PROD-005', name: 'Kissan Fresh Tomato Ketchup (950g)', category: 'Packaged Foods', price: 2.10, stock: 210 }
        ]
    },
    {
        id: 'SUP-002',
        companyName: 'Nestlé India Ltd.',
        gst: '07AABCN9012D1Z1',
        contactPerson: 'Amit Khanna',
        phone: '+91 11 2341 8899',
        email: 'amit.khanna@nestle.in',
        address: 'Nestle House, Jacaranda Marg, DLF City Phase II',
        city: 'New Delhi',
        paymentTerms: 'Net 15',
        status: 'Verified',
        isPreferred: true,
        logoUrl: 'https://images.unsplash.com/photo-1542838132-92c53300491e?w=128&auto=format&fit=crop&q=80',
        notes: 'Packaged foods, beverages, and dairy supplies.',
        productsSupplied: ['Maggi Noodles', 'Coffee', 'Condensed Milk', 'Chocolate'],
        catalog: [
            { id: 'PROD-006', name: 'Maggi 2-Minute Masala Noodles (12 Pack)', category: 'Packaged Foods', price: 2.40, stock: 600 },
            { id: 'PROD-007', name: 'Nescafé Classic Instant Coffee (200g Jar)', category: 'Beverages', price: 6.50, stock: 140 },
            { id: 'PROD-008', name: 'Nestlé Milkmaid Sweetened Milk (400g)', category: 'Dairy', price: 2.80, stock: 220 },
            { id: 'PROD-009', name: 'KitKat 4-Finger Chocolate (38g)', category: 'Confectionery', price: 0.85, stock: 850 }
        ]
    },
    {
        id: 'SUP-003',
        companyName: 'Britannia Industries Ltd.',
        gst: '29AABCB5678C1Z3',
        contactPerson: 'Priya Menon',
        phone: '+91 80 4322 2345',
        email: 'priya.menon@britannia.in',
        address: '5/1A, Hungerford Street, Park Street Area',
        city: 'Bengaluru',
        paymentTerms: 'Net 15',
        status: 'Active',
        isPreferred: true,
        logoUrl: 'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=128&auto=format&fit=crop&q=80',
        notes: 'Biscuits, bakery, and dairy segments.',
        productsSupplied: ['Biscuits', 'Bread', 'Cheese Slices', 'Cakes'],
        catalog: [
            { id: 'PROD-010', name: 'Britannia Good Day Butter Biscuits (600g)', category: 'Bakery', price: 2.20, stock: 400 },
            { id: 'PROD-011', name: 'Britannia 100% Whole Wheat Bread (400g)', category: 'Bakery', price: 0.95, stock: 150 },
            { id: 'PROD-012', name: 'Britannia Cheese Slices (200g Pack)', category: 'Dairy', price: 2.10, stock: 280 }
        ]
    },
    {
        id: 'SUP-004',
        companyName: 'Amul Dairy (GCMMF)',
        gst: '24AAAAG1021K1Z3',
        contactPerson: 'Rajesh Patel',
        phone: '+91 26 9225 8506',
        email: 'sales@amul.coop',
        address: 'Amul Dairy Road, Anand',
        city: 'Anand',
        paymentTerms: 'Net 30',
        status: 'Verified',
        isPreferred: true,
        logoUrl: 'https://images.unsplash.com/photo-1527153857715-3908f2bae5e8?w=128&auto=format&fit=crop&q=80',
        notes: 'Main fresh milk, butter, and cheese supply line.',
        productsSupplied: ['Milk', 'Butter', 'Cheese', 'Paneer', 'Ghee'],
        catalog: [
            { id: 'PROD-013', name: 'Amul Butter Salted (500g Pack)', category: 'Dairy', price: 3.40, stock: 520 },
            { id: 'PROD-014', name: 'Amul Taaza Toned Milk (1 Litre Pouch)', category: 'Dairy', price: 0.90, stock: 900 },
            { id: 'PROD-015', name: 'Amul Fresh Paneer (200g Block)', category: 'Dairy', price: 1.60, stock: 310 },
            { id: 'PROD-016', name: 'Amul Pure Ghee (1 Litre Tin)', category: 'Dairy', price: 8.50, stock: 190 }
        ]
    },
    {
        id: 'SUP-005',
        companyName: 'Tata Consumer Products',
        gst: '27AAACT9087F1ZA',
        contactPerson: 'Vikram Singh',
        phone: '+91 22 6600 0700',
        email: 'customercare@tataconsumer.com',
        address: '11/13 Botawala Building, Horniman Circle',
        city: 'Mumbai',
        paymentTerms: 'Net 30',
        status: 'Active',
        isPreferred: false,
        logoUrl: 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=128&auto=format&fit=crop&q=80',
        notes: 'Salt, pulses, and tea beverages supply line.',
        productsSupplied: ['Tata Salt', 'Tata Tea Premium', 'Tata Sampann Pulses'],
        catalog: [
            { id: 'PROD-017', name: 'Tata Salt Vacuum Evaporated (1kg)', category: 'Staples', price: 0.50, stock: 1200 },
            { id: 'PROD-018', name: 'Tata Tea Premium Black Tea (500g)', category: 'Beverages', price: 3.60, stock: 340 },
            { id: 'PROD-019', name: 'Tata Sampann Unpolished Toor Dal (1kg)', category: 'Staples', price: 2.30, stock: 260 }
        ]
    }
];

// ============================================================
// 2. APP STATE
// ============================================================
let currentOrderCart = {}; // { productId: { product, qty } }
let selectedSearchQuery = '';
let selectedStatusFilter = '';
let activePaymentMethod = 'card'; // 'card' | 'qr'
let pendingOrderSupplier = null;

// ============================================================
// 3. UTILITY HELPERS
// ============================================================
const getEl = (id) => document.getElementById(id);

function escHtml(s) {
    if (s == null) return '';
    return String(s)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

function showToast(message, type = 'success') {
    const icons = { success: 'fa-circle-check', error: 'fa-circle-xmark', info: 'fa-circle-info' };
    const icon = icons[type] || 'fa-circle-info';

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.style.cssText = `
        position: fixed;
        bottom: 24px;
        right: 24px;
        background: ${type === 'error' ? '#ef4444' : '#10b981'};
        color: #ffffff;
        padding: 14px 20px;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 14px;
        font-weight: 500;
        z-index: 99999;
        transition: all 0.3s ease;
    `;
    toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${escHtml(message)}</span>`;

    const container = getEl('toastContainer') || document.body;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function addNotificationToDropdown(message) {
    const notifList = getEl('notificationList');
    const notifBadge = getEl('notificationBadge');
    if (!notifList) return;

    const emptyState = notifList.querySelector('.empty-state');
    if (emptyState) emptyState.remove();

    const notifItem = document.createElement('div');
    notifItem.className = 'notification-item unread';
    notifItem.style.padding = '12px 16px';
    notifItem.style.borderBottom = '1px solid rgba(0,0,0,0.05)';
    notifItem.style.display = 'flex';
    notifItem.style.justifyContent = 'space-between';
    notifItem.style.alignItems = 'center';
    notifItem.style.gap = '12px';
    notifItem.innerHTML = `
        <div style="flex:1;">
            <p style="margin:0; font-size:12.5px; font-weight:500; color:#1e293b;">${escHtml(message)}</p>
            <span style="font-size:10.5px; color:#94a3b8; display:block; margin-top:2px;">Just Now</span>
        </div>
        <span class="unread-dot" style="width:6px; height:6px; background-color:#2563eb; border-radius:50%; flex-shrink:0;"></span>
    `;
    notifList.prepend(notifItem);

    if (notifBadge) {
        const count = parseInt(notifBadge.textContent || '0') + 1;
        notifBadge.textContent = count;
        notifBadge.style.display = 'block';
    }
}

// ============================================================
// 4. ROUTER (#list vs #detail/:id)
// ============================================================
function handleRoute() {
    const hash = window.location.hash || '#list';
    const app = getEl('app');
    if (!app) return;

    if (hash.startsWith('#detail/') || hash.startsWith('#detail-')) {
        const id = hash.replace('#detail/', '').replace('#detail-', '');
        renderSupplierDetail(id);
    } else {
        renderSupplierList();
    }
}

window.addEventListener('hashchange', handleRoute);

// ============================================================
// 5. RENDER SINGLE-COLUMN SUPPLIER LIST
// ============================================================
function renderSupplierList() {
    const app = getEl('app');
    if (!app) return;

    let filtered = suppliers.filter(s => {
        const matchesQuery = !selectedSearchQuery ||
            s.companyName.toLowerCase().includes(selectedSearchQuery) ||
            s.contactPerson.toLowerCase().includes(selectedSearchQuery) ||
            s.city.toLowerCase().includes(selectedSearchQuery) ||
            s.id.toLowerCase().includes(selectedSearchQuery);

        const matchesStatus = !selectedStatusFilter || s.status === selectedStatusFilter;
        return matchesQuery && matchesStatus;
    });

    let html = `
        <!-- Workspace Header & Toolbar -->
        <div class="workspace-header">
            <div>
                <h1 class="workspace-title">Suppliers Directory</h1>
                <p class="workspace-subtitle">Manage partner directory, catalog inventories, and place stock replenishment orders.</p>
            </div>
        </div>

        <div class="workspace-toolbar">
            <div class="search-bar-wrapper">
                <i class="fa-solid fa-magnifying-glass search-icon"></i>
                <input type="text" id="toolbarSearchInput" class="search-bar-input" placeholder="Search suppliers by name, city, ID..." value="${escHtml(selectedSearchQuery)}">
                <button class="clear-btn" id="clearSearchBtn" style="${selectedSearchQuery ? 'display:block;' : 'display:none;'}"><i class="fa-solid fa-xmark"></i></button>
            </div>

            <div class="styled-select-wrapper">
                <select id="toolbarStatusFilter" class="styled-select">
                    <option value="">All Statuses</option>
                    <option value="Verified" ${selectedStatusFilter === 'Verified' ? 'selected' : ''}>Verified</option>
                    <option value="Active" ${selectedStatusFilter === 'Active' ? 'selected' : ''}>Active</option>
                    <option value="Pending" ${selectedStatusFilter === 'Pending' ? 'selected' : ''}>Pending</option>
                </select>
            </div>

            <button class="btn btn-outline" id="importBtn"><i class="fa-solid fa-file-import"></i> Import</button>
            <button class="btn btn-outline" id="exportBtn"><i class="fa-solid fa-file-export"></i> Export</button>
            <button class="btn btn-primary" id="addSupplierBtn"><i class="fa-solid fa-plus"></i> Add Supplier</button>
        </div>

        <!-- Supplier Single List -->
        <div class="supplier-single-list">
    `;

    if (filtered.length === 0) {
        html += `
            <div style="text-align:center; padding: 48px; background:#fff; border-radius:16px; color:#64748b;">
                <i class="fa-solid fa-folder-open" style="font-size:36px; margin-bottom:12px; color:#cbd5e1; display:block;"></i>
                <h3 style="font-size:16px; color:#0f172a; margin-bottom:4px;">No suppliers found</h3>
                <p style="font-size:13px;">Try adjusting your search criteria or status filter.</p>
            </div>
        `;
    } else {
        filtered.forEach(s => {
            const fallbackUrl = `https://ui-avatars.com/api/?name=${encodeURIComponent(s.companyName)}&background=2563eb&color=fff&size=128`;
            const logo = `<img src="${escHtml(s.logoUrl || fallbackUrl)}" alt="${escHtml(s.companyName)}" style="width:56px; height:56px; border-radius:12px; object-fit:cover;" onerror="this.onerror=null; this.src='${fallbackUrl}';">`;

            html += `
                <div class="supplier-list-card" onclick="window.location.hash='#detail/${s.id}'">
                    <div class="card-main-info">
                        <div class="supplier-avatar-box">${logo}</div>
                        <div class="supplier-title-group">
                            <h3 class="company-name">${escHtml(s.companyName)}</h3>
                            <div class="company-sub">
                                <span><i class="fa-solid fa-location-dot"></i> ${escHtml(s.city)}</span>
                                <span><i class="fa-solid fa-user"></i> ${escHtml(s.contactPerson)}</span>
                                <span><i class="fa-solid fa-envelope"></i> ${escHtml(s.email)}</span>
                            </div>
                        </div>
                    </div>

                    <div class="card-meta-cols">
                        <div class="meta-item">
                            <span class="meta-label">GST Number</span>
                            <span class="meta-val">${escHtml(s.gst || 'N/A')}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Payment Terms</span>
                            <span class="meta-val">${escHtml(s.paymentTerms)}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Status</span>
                            <span class="status-badge ${s.status.toLowerCase()}">${escHtml(s.status)}</span>
                        </div>
                        <button class="btn btn-outline" style="height:38px; font-size:13px;">
                            View Catalog & Order <i class="fa-solid fa-arrow-right" style="margin-left:4px;"></i>
                        </button>
                    </div>
                </div>
            `;
        });
    }

    html += `</div>`;
    app.innerHTML = html;

    // Attach Toolbar Event Listeners
    const searchInput = getEl('toolbarSearchInput');
    const clearBtn = getEl('clearSearchBtn');
    const statusSelect = getEl('toolbarStatusFilter');

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            selectedSearchQuery = e.target.value.toLowerCase();
            if (clearBtn) clearBtn.style.display = selectedSearchQuery ? 'block' : 'none';
            renderSupplierList();
        });
    }

    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            selectedSearchQuery = '';
            renderSupplierList();
        });
    }

    if (statusSelect) {
        statusSelect.addEventListener('change', (e) => {
            selectedStatusFilter = e.target.value;
            renderSupplierList();
        });
    }
}

// ============================================================
// 6. RENDER SUPPLIER DETAIL VIEW & PRODUCTS CATALOG
// ============================================================
function renderSupplierDetail(supplierId) {
    const app = getEl('app');
    if (!app) return;

    const s = suppliers.find(x => x.id === supplierId);
    if (!s) {
        app.innerHTML = `
            <div style="padding:48px; text-align:center;">
                <h2>Supplier Not Found</h2>
                <a href="#list" class="btn btn-primary" style="margin-top:16px;">Back to Directory</a>
            </div>
        `;
        return;
    }

    pendingOrderSupplier = s;
    currentOrderCart = {}; // Reset cart for this supplier

    const fallbackUrl = `https://ui-avatars.com/api/?name=${encodeURIComponent(s.companyName)}&background=2563eb&color=fff&size=128`;
    const logo = `<img src="${escHtml(s.logoUrl || fallbackUrl)}" alt="${escHtml(s.companyName)}" style="width:64px; height:64px; border-radius:14px; object-fit:cover;" onerror="this.onerror=null; this.src='${fallbackUrl}';">`;

    let catalogRows = '';
    const catalog = s.catalog || [];

    if (catalog.length === 0) {
        catalogRows = `<tr><td colspan="5" style="text-align:center; padding:24px; color:#94a3b8;">No products listed in wholesale catalog.</td></tr>`;
    } else {
        catalog.forEach(item => {
            catalogRows += `
                <tr data-prod-id="${item.id}">
                    <td>
                        <strong style="display:block; font-size:15px; color:#0f172a;">${escHtml(item.name)}</strong>
                        <span style="font-size:12px; color:#64748b;">${escHtml(item.category)}</span>
                    </td>
                    <td><strong>$${item.price.toFixed(2)}</strong> / unit</td>
                    <td><span class="status-badge ${item.stock > 0 ? 'verified' : 'pending'}">${item.stock} in stock</span></td>
                    <td>
                        <div class="qty-control">
                            <button class="qty-btn dec-btn" onclick="updateQty('${item.id}', -1)">-</button>
                            <input type="number" id="qty-input-${item.id}" class="qty-input" value="0" min="0" max="${item.stock}" onchange="setQty('${item.id}', this.value)">
                            <button class="qty-btn inc-btn" onclick="updateQty('${item.id}', 1)">+</button>
                        </div>
                    </td>
                    <td><strong id="subtotal-${item.id}" style="color:#2563eb;">$0.00</strong></td>
                </tr>
            `;
        });
    }

    let html = `
        <div class="supplier-detail-view">
            <!-- Back Navigation -->
            <div>
                <a href="#list" class="btn btn-outline" style="height:38px;"><i class="fa-solid fa-arrow-left"></i> Back to Suppliers Directory</a>
            </div>

            <!-- Full-Width Company Information Card -->
            <div class="detail-header-card">
                <div class="company-banner">
                    <div class="company-identity">
                        ${logo}
                        <div>
                            <h1 style="font-size:24px; font-weight:700; color:#0f172a; margin:0 0 6px 0;">${escHtml(s.companyName)}</h1>
                            <div style="display:flex; gap:12px; align-items:center;">
                                <span class="status-badge ${s.status.toLowerCase()}">${escHtml(s.status)}</span>
                                ${s.isPreferred ? '<span class="preferred-badge"><i class="fa-solid fa-star"></i> Preferred Supplier</span>' : ''}
                            </div>
                        </div>
                    </div>
                </div>

                <div class="company-info-grid">
                    <div class="info-cell">
                        <span class="label">GST Number</span>
                        <span class="val">${escHtml(s.gst || 'N/A')}</span>
                    </div>
                    <div class="info-cell">
                        <span class="label">Contact Person</span>
                        <span class="val">${escHtml(s.contactPerson)}</span>
                    </div>
                    <div class="info-cell">
                        <span class="label">Email Address</span>
                        <span class="val">${escHtml(s.email)}</span>
                    </div>
                    <div class="info-cell">
                        <span class="label">Phone Contact</span>
                        <span class="val">${escHtml(s.phone)}</span>
                    </div>
                    <div class="info-cell">
                        <span class="label">Payment Terms</span>
                        <span class="val">${escHtml(s.paymentTerms)}</span>
                    </div>
                    <div class="info-cell">
                        <span class="label">Registered Address</span>
                        <span class="val">${escHtml(s.address)}, ${escHtml(s.city)}</span>
                    </div>
                </div>
            </div>

            <!-- Products Catalog & Order Placement Section -->
            <div class="catalog-card">
                <div class="catalog-title">
                    <span><i class="fa-solid fa-boxes-stacked" style="color:#2563eb; margin-right:8px;"></i> Products Supplied & Wholesale Catalog</span>
                    <span style="font-size:13px; font-weight:500; color:#64748b;">${catalog.length} items available</span>
                </div>

                <table class="catalog-table">
                    <thead>
                        <tr>
                            <th>Product Name</th>
                            <th>Unit Price</th>
                            <th>Stock</th>
                            <th>Order Quantity</th>
                            <th>Subtotal</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${catalogRows}
                    </tbody>
                </table>

                <!-- Bottom Order Summary Sticky Bar -->
                <div class="order-summary-bar">
                    <div class="summary-details">
                        <div class="summary-item">
                            <span class="sum-lbl">Selected Products</span>
                            <span class="sum-val" id="summarySelectedCount">0 items</span>
                        </div>
                        <div class="summary-item">
                            <span class="sum-lbl">Total Payable Amount</span>
                            <span class="sum-val" id="summaryTotalAmount">$0.00</span>
                        </div>
                    </div>
                    <button class="btn btn-primary" id="placeOrderBtn" disabled onclick="openOrderModal()">
                        <i class="fa-solid fa-cart-shopping"></i> Place Order Now
                    </button>
                </div>
            </div>
        </div>
    `;

    app.innerHTML = html;
}

// Global Quantity Update Handlers
window.updateQty = function (productId, delta) {
    const input = getEl(`qty-input-${productId}`);
    if (!input) return;

    let currentVal = parseInt(input.value || '0', 10);
    let newVal = Math.max(0, Math.min(parseInt(input.max || '9999', 10), currentVal + delta));
    input.value = newVal;
    setQty(productId, newVal);
};

window.setQty = function (productId, value) {
    const qty = Math.max(0, parseInt(value || '0', 10));
    if (!pendingOrderSupplier || !pendingOrderSupplier.catalog) return;

    const prod = pendingOrderSupplier.catalog.find(p => p.id === productId);
    if (!prod) return;

    if (qty > 0) {
        currentOrderCart[productId] = { product: prod, qty: qty };
    } else {
        delete currentOrderCart[productId];
    }

    // Update Subtotal UI
    const subtotalEl = getEl(`subtotal-${productId}`);
    if (subtotalEl) {
        subtotalEl.textContent = `$${(prod.price * qty).toFixed(2)}`;
    }

    // Update Summary Bar UI
    updateCartSummary();
};

function updateCartSummary() {
    let totalItems = 0;
    let totalAmount = 0;

    Object.values(currentOrderCart).forEach(item => {
        totalItems += item.qty;
        totalAmount += item.product.price * item.qty;
    });

    const countEl = getEl('summarySelectedCount');
    const amountEl = getEl('summaryTotalAmount');
    const placeBtn = getEl('placeOrderBtn');

    if (countEl) countEl.textContent = `${totalItems} item${totalItems === 1 ? '' : 's'}`;
    if (amountEl) amountEl.textContent = `$${totalAmount.toFixed(2)}`;
    if (placeBtn) placeBtn.disabled = totalItems === 0;
}

// ============================================================
// 7. ORDER MODAL & PAYMENT FLOW
// ============================================================
window.openOrderModal = function () {
    const modal = getEl('orderModal');
    if (!modal) return;

    let total = 0;
    let itemsHtml = `
        <div style="margin-bottom:16px; max-height:200px; overflow-y:auto; border:1px solid #f1f5f9; border-radius:12px; padding:12px;">
    `;

    Object.values(currentOrderCart).forEach(item => {
        const sub = item.product.price * item.qty;
        total += sub;
        itemsHtml += `
            <div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid #f8fafc; font-size:13.5px;">
                <span>${escHtml(item.product.name)} (x${item.qty})</span>
                <strong>$${sub.toFixed(2)}</strong>
            </div>
        `;
    });

    itemsHtml += `
        </div>
        <div style="display:flex; justify-content:space-between; font-size:16px; font-weight:700; color:#0f172a; margin-bottom:20px;">
            <span>Total Payable Amount</span>
            <span style="color:#2563eb;">$${total.toFixed(2)}</span>
        </div>
    `;

    const detailsContainer = modal.querySelector('.order-details');
    if (detailsContainer) detailsContainer.innerHTML = itemsHtml;

    modal.classList.remove('hidden');
};

function initModalHandlers() {
    const closeOrderBtn = getEl('closeOrderModalBtn');
    const proceedPaymentBtn = getEl('proceedToPaymentBtn');
    const orderModal = getEl('orderModal');

    if (closeOrderBtn && orderModal) {
        closeOrderBtn.addEventListener('click', () => orderModal.classList.add('hidden'));
    }

    if (proceedPaymentBtn && orderModal) {
        proceedPaymentBtn.addEventListener('click', () => {
            orderModal.classList.add('hidden');
            openPaymentModal();
        });
    }

    const closePaymentBtn = getEl('closePaymentModalBtn');
    const paymentModal = getEl('paymentModal');

    if (closePaymentBtn && paymentModal) {
        closePaymentBtn.addEventListener('click', () => paymentModal.classList.add('hidden'));
    }

    const payCardBtn = getEl('payWithCardBtn');
    const payQrBtn = getEl('payWithQrBtn');
    const cardFormContainer = getEl('paymentFormContainer');
    const qrContainer = getEl('qrCodeContainer');

    if (payCardBtn && payQrBtn && cardFormContainer && qrContainer) {
        payCardBtn.addEventListener('click', () => {
            activePaymentMethod = 'card';
            payCardBtn.classList.add('active');
            payQrBtn.classList.remove('active');
            cardFormContainer.classList.remove('hidden');
            qrContainer.classList.add('hidden');
        });

        payQrBtn.addEventListener('click', () => {
            activePaymentMethod = 'qr';
            payQrBtn.classList.add('active');
            payCardBtn.classList.remove('active');
            qrContainer.classList.remove('hidden');
            cardFormContainer.classList.add('hidden');

            const canvas = getEl('qrCanvas');
            if (canvas && window.MockPayment) {
                window.MockPayment.renderQrCode(canvas, `ORDER-${Date.now()}`);
            }
        });
    }

    const confirmQrBtn = getEl('confirmQrPaymentBtn');
    if (confirmQrBtn) {
        confirmQrBtn.addEventListener('click', () => {
            executePayment('qr');
        });
    }

    // Card Form Submit
    const cardForm = getEl('cardPaymentForm');
    if (cardForm) {
        cardForm.addEventListener('submit', (e) => {
            e.preventDefault();
            executePayment('card', {
                cardNumber: getEl('cardNumber').value,
                cardExpiry: getEl('cardExpiry').value,
                cardCvc: getEl('cardCvc').value
            });
        });
    }
}

function openPaymentModal() {
    const modal = getEl('paymentModal');
    if (!modal) return;

    let totalAmount = 0;
    Object.values(currentOrderCart).forEach(i => totalAmount += i.product.price * i.qty);

    const payAmountEl = getEl('payAmount');
    if (payAmountEl) payAmountEl.textContent = totalAmount.toFixed(2);

    modal.classList.remove('hidden');
}

function executePayment(method, details = {}) {
    let totalAmount = 0;
    Object.values(currentOrderCart).forEach(i => totalAmount += i.product.price * i.qty);

    const paymentModal = getEl('paymentModal');

    // Show loading state
    showToast('Processing payment with bank gateway (5s)...', 'info');

    if (window.MockPayment) {
        window.MockPayment.processPayment(method, totalAmount, details)
            .then(res => {
                if (paymentModal) paymentModal.classList.add('hidden');
                
                // Show order confirmed toast
                showToast('Your order has been placed and you will get the confirmation soon.', 'success');
                addNotificationToDropdown(`Order placed with ${pendingOrderSupplier.companyName} for $${totalAmount.toFixed(2)}.`);

                // Reset cart & view
                currentOrderCart = {};
                window.location.hash = '#list';
            })
            .catch(err => {
                showToast(err.message, 'error');
            });
    }
}

// ============================================================
// 8. INIT APP
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
    initModalHandlers();
    handleRoute();
});
