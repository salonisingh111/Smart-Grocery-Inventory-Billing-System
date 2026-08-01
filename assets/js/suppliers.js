/* ==========================================================================
   suppliers.js — Vendor Management Logic
   SmartBilling | Inventory Management Module
   ========================================================================== */

'use strict';

// ============================================================
// 1. DATA LAYER — Master supplier data
// ============================================================
let suppliers = [
    {
        id: 'SUP-001',
        companyName: 'Aashirvaad Foods Pvt. Ltd.',
        gst: '27AABCA1234B1Z5',
        contactPerson: 'Rajesh Sharma',
        phone: '+91 98201 11234',
        email: 'rajesh@aashirvaad.com',
        address: 'Plot 12, MIDC Industrial Area, Turbhe',
        city: 'Mumbai',
        paymentTerms: 'Net 30',
        status: 'Verified',
        isPreferred: true,
        logoUrl: '',
        notes: 'Preferred wheat and flour supplier. Reliable delivery.',
        createdAt: new Date('2026-01-15').toISOString(),
        activityLog: [
            { desc: 'Supplier Created', time: '15 Jan 2026, 10:00 AM' },
            { desc: 'GST Verified', time: '15 Jan 2026, 11:30 AM' }
        ]
    },
    {
        id: 'SUP-002',
        companyName: 'Britannia Industries Ltd.',
        gst: '29AABCB5678C1Z3',
        contactPerson: 'Priya Menon',
        phone: '+91 80432 22345',
        email: 'priya.menon@britannia.in',
        address: '5/1A, Hungerford Street, Park Street Area',
        city: 'Bengaluru',
        paymentTerms: 'Net 15',
        status: 'Active',
        isPreferred: true,
        logoUrl: '',
        notes: 'Biscuits and bakery segment. Always delivers on time.',
        createdAt: new Date('2026-02-10').toISOString(),
        activityLog: [
            { desc: 'Supplier Created', time: '10 Feb 2026, 09:15 AM' },
            { desc: 'Status Changed to Active', time: '10 Feb 2026, 10:00 AM' }
        ]
    },
    {
        id: 'SUP-003',
        companyName: 'Nestlé India Ltd.',
        gst: '07AABCN9012D1Z1',
        contactPerson: 'Amit Khanna',
        phone: '+91 11956 33456',
        email: 'amit.khanna@nestle.in',
        address: 'Nestle House, Jacaranda Marg, DLF City Phase II',
        city: 'New Delhi',
        paymentTerms: 'Credit',
        status: 'Pending',
        isPreferred: false,
        logoUrl: '',
        notes: 'Beverages and dairy products. Under corporate compliance checks.',
        createdAt: new Date('2026-03-05').toISOString(),
        activityLog: [
            { desc: 'Supplier Created', time: '05 Mar 2026, 02:45 PM' }
        ]
    },
    {
        id: 'SUP-004',
        companyName: 'ITC Limited — Foods Division',
        gst: '19AAACI1234E1Z8',
        contactPerson: 'Sunita Rao',
        phone: '+91 33734 44567',
        email: 'sunita.rao@itc.in',
        address: 'Virginia House, 37 J.L. Nehru Road',
        city: 'Kolkata',
        paymentTerms: 'Cash',
        status: 'Inactive',
        isPreferred: false,
        logoUrl: '',
        notes: 'Snacks and biscuits. Compliance documents pending renewal.',
        createdAt: new Date('2026-03-20').toISOString(),
        activityLog: [
            { desc: 'Supplier Created', time: '20 Mar 2026, 11:20 AM' },
            { desc: 'Status Changed to Inactive', time: '28 Mar 2026, 04:00 PM' }
        ]
    }
];

// ============================================================
// 2. STATE Variables
// ============================================================
let currentViewMode = 'list';
let selectedStatusFilter = '';
let pendingDeleteId = null;
let currentDetailSupplierId = null;

// ============================================================
// 3. LAZY DOM GETTERS
// ============================================================
const getEl = (id) => document.getElementById(id);

// ============================================================
// 4. UTILITY HELPERS
// ============================================================
function strToColor(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    const hue = Math.abs(hash) % 360;
    return `hsl(${hue}, 55%, 42%)`;
}

function getInitials(name) {
    const words = name.trim().split(/\s+/);
    if (words.length >= 2) {
        return (words[0][0] + words[1][0]).toUpperCase();
    }
    return name.substring(0, 2).toUpperCase();
}

function escHtml(s) {
    if (s == null) return '';
    return String(s)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

function generateSupplierId() {
    const existing = suppliers.map(s => parseInt(s.id.split('-')[1] || '0'));
    const max = existing.length > 0 ? Math.max(...existing) : 0;
    return 'SUP-' + String(max + 1).padStart(3, '0');
}

// ============================================================
// 5. TOAST NOTIFICATIONS
// ============================================================
function showToast(message, type = 'success') {
    const icons = { success: 'fa-circle-check', error: 'fa-circle-xmark', info: 'fa-circle-info' };
    const icon = icons[type] || 'fa-circle-info';

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <i class="fa-solid ${icon} toast-icon" style="font-size:18px;flex-shrink:0;"></i>
        <span class="toast-msg">${escHtml(message)}</span>`;

    const container = getEl('toastContainer');
    if (container) container.appendChild(toast);

    requestAnimationFrame(() => {
        requestAnimationFrame(() => toast.classList.add('show'));
    });

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 350);
    }, 3500);
}

// ============================================================
// 6. FILTER & SORT
// ============================================================
function getFilteredSuppliers() {
    const searchInput = getEl('searchInput');
    const query = (searchInput ? searchInput.value.trim().toLowerCase() : '');
    const status = selectedStatusFilter;

    return suppliers.filter(s => {
        const matchesQuery = !query ||
            s.companyName.toLowerCase().includes(query) ||
            s.id.toLowerCase().includes(query) ||
            s.contactPerson.toLowerCase().includes(query) ||
            s.city.toLowerCase().includes(query) ||
            (s.phone || '').toLowerCase().includes(query);

        const matchesStatus = !status || s.status === status;

        return matchesQuery && matchesStatus;
    });
}

// ============================================================
// 7. RENDER DIRECTORY (TABLE & GRID)
// ============================================================
function renderLogoHtml(logoUrl, companyName) {
    const initials = getInitials(companyName);
    const bg = strToColor(companyName);
    if (logoUrl && logoUrl.trim() !== '') {
        return `<img src="${escHtml(logoUrl)}" alt="${escHtml(companyName)}" class="supplier-logo-thumb"
                    onerror="this.style.display='none';this.nextElementSibling.style.display='flex';">
                <div class="logo-initials-sm" style="background:${bg};display:none;">${initials}</div>`;
    }
    return `<div class="logo-initials-sm" style="background:${bg};">${initials}</div>`;
}

function renderTable(list) {
    const body = getEl('supplierTableBody');
    if (!body) return;
    body.innerHTML = '';

    if (list.length === 0) {
        body.innerHTML = `
            <tr>
                <td colspan="10">
                    <div style="text-align: center; padding: 32px; color: #64748b;">
                        <i class="fa-solid fa-folder-open" style="font-size: 32px; margin-bottom: 8px;"></i>
                        <p>No vendors found matching criteria.</p>
                    </div>
                </td>
            </tr>`;
        return;
    }

    list.forEach((s, idx) => {
        const logo = renderLogoHtml(s.logoUrl, s.companyName);
        const preferredBadge = s.isPreferred ? `<span class="preferred-badge" style="margin-left: 6px;"><i class="fa-solid fa-star"></i> Preferred</span>` : '';
        const statusBadge = `<span class="status-badge ${s.status.toLowerCase()}">${s.status}</span>`;

        const tr = document.createElement('tr');
        tr.dataset.id = s.id;
        tr.style.animationDelay = `${idx * 40}ms`;
        tr.innerHTML = `
            <td>${logo}</td>
            <td>
                <div style="display: flex; align-items: center; font-weight: 600; color: var(--color-heading);">
                    ${escHtml(s.companyName)} ${preferredBadge}
                </div>
            </td>
            <td><span style="font-family: monospace; font-weight: 500;">${escHtml(s.id)}</span></td>
            <td>${escHtml(s.contactPerson)}</td>
            <td>${escHtml(s.phone)}</td>
            <td>${escHtml(s.email || '—')}</td>
            <td>${escHtml(s.city)}</td>
            <td><span class="terms-badge">${escHtml(s.paymentTerms)}</span></td>
            <td style="text-align: center;">${statusBadge}</td>
            <td style="text-align: center;" class="actions-cell">
                <div class="actions-wrapper" style="justify-content: center;">
                    <button class="icon-btn action-view-trigger" data-id="${s.id}" title="View Details"><i class="fa-regular fa-eye"></i></button>
                    <button class="icon-btn action-edit-trigger" data-id="${s.id}" title="Edit"><i class="fa-regular fa-pen-to-square"></i></button>
                    <div class="dropdown-trigger-container">
                        <button class="icon-btn-more action-menu-trigger" data-id="${s.id}"><i class="fa-solid fa-ellipsis-vertical"></i></button>
                        <div class="dropdown-menu-list" id="menu-${s.id}">
                            <a href="#" class="view-menu-item" data-id="${s.id}"><i class="fa-regular fa-eye"></i> View Factsheet</a>
                            <a href="#" class="edit-menu-item" data-id="${s.id}"><i class="fa-regular fa-pen-to-square"></i> Edit Vendor</a>
                            <a href="#" class="print-menu-item" data-id="${s.id}"><i class="fa-solid fa-print"></i> Print Profile</a>
                            <a href="#" class="export-menu-item" data-id="${s.id}"><i class="fa-solid fa-download"></i> Export CSV</a>
                            <a href="#" class="delete-menu-item delete-action" data-id="${s.id}"><i class="fa-regular fa-trash-can"></i> Delete Vendor</a>
                        </div>
                    </div>
                </div>
            </td>
        `;
        body.appendChild(tr);
    });
}

function renderGrid(list) {
    const grid = getEl('supplierGridBody');
    if (!grid) return;
    grid.innerHTML = '';

    if (list.length === 0) {
        grid.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 40px; color: #64748b;">
                <i class="fa-solid fa-folder-open" style="font-size: 36px; margin-bottom: 8px;"></i>
                <p>No vendors found matching criteria.</p>
            </div>`;
        return;
    }

    list.forEach((s, idx) => {
        const bg = strToColor(s.companyName);
        const initials = getInitials(s.companyName);
        const logo = s.logoUrl && s.logoUrl.trim()
            ? `<img src="${escHtml(s.logoUrl)}" alt="${escHtml(s.companyName)}" class="card-logo-img"
                   onerror="this.style.display='none';this.nextElementSibling.style.display='flex';">
               <div class="card-logo-initials" style="background:${bg};display:none;">${initials}</div>`
            : `<div class="card-logo-initials" style="background:${bg};">${initials}</div>`;

        const preferredBadge = s.isPreferred ? `<span class="preferred-badge"><i class="fa-solid fa-star"></i> Preferred</span>` : '';
        const statusBadge = `<span class="status-badge ${s.status.toLowerCase()}">${s.status}</span>`;

        const card = document.createElement('div');
        card.className = 'supplier-card';
        card.dataset.id = s.id;
        card.style.animationDelay = `${idx * 40}ms`;
        card.innerHTML = `
            <div class="supplier-card-header">
                <div class="card-logo-wrap">${logo}</div>
                <div class="card-company-info">
                    <div class="card-company-name">${escHtml(s.companyName)}</div>
                    <div class="card-contact-person"><i class="fa-regular fa-user" style="margin-right: 4px;"></i>${escHtml(s.contactPerson)}</div>
                </div>
            </div>
            <div class="supplier-card-body">
                <div class="card-info-row"><i class="fa-solid fa-phone"></i><span>${escHtml(s.phone)}</span></div>
                <div class="card-info-row"><i class="fa-solid fa-location-dot"></i><span>${escHtml(s.city)}</span></div>
                <div class="card-info-row"><i class="fa-solid fa-file-invoice"></i><span>Terms: ${escHtml(s.paymentTerms)}</span></div>
                <div class="card-info-row" style="font-size:12px; color:#64748b; font-style:italic; line-height:1.3; height:34px; overflow:hidden; text-overflow:ellipsis; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical;">
                    ${escHtml(s.notes || 'No description available.')}
                </div>
            </div>
            <div class="supplier-card-footer">
                ${statusBadge}
                ${preferredBadge}
            </div>
            <!-- absolute actions button area -->
            <div style="position: absolute; top: 12px; right: 12px; display: flex; gap: 4px;" class="actions-cell">
                <button class="icon-btn action-edit-trigger" data-id="${s.id}" style="width:26px; height:26px; font-size:11px;" title="Edit"><i class="fa-regular fa-pen-to-square"></i></button>
                <div class="dropdown-trigger-container">
                    <button class="icon-btn-more action-menu-trigger" data-id="${s.id}" style="width:26px; height:26px; font-size:11px;"><i class="fa-solid fa-ellipsis-vertical"></i></button>
                    <div class="dropdown-menu-list" id="menu-grid-${s.id}">
                        <a href="#" class="view-menu-item" data-id="${s.id}"><i class="fa-regular fa-eye"></i> View Factsheet</a>
                        <a href="#" class="edit-menu-item" data-id="${s.id}"><i class="fa-regular fa-pen-to-square"></i> Edit Vendor</a>
                        <a href="#" class="print-menu-item" data-id="${s.id}"><i class="fa-solid fa-print"></i> Print Profile</a>
                        <a href="#" class="export-menu-item" data-id="${s.id}"><i class="fa-solid fa-download"></i> Export CSV</a>
                        <a href="#" class="delete-menu-item delete-action" data-id="${s.id}"><i class="fa-regular fa-trash-can"></i> Delete Vendor</a>
                    </div>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });
}

function updateSummaryCards() {
    const total = suppliers.length;
    const active = suppliers.filter(s => s.status === 'Active').length;
    const inactive = suppliers.filter(s => s.status === 'Inactive').length;
    
    // "New" logic: Added in the last 30 days
    const thirtyDaysAgo = Date.now() - 30 * 24 * 60 * 60 * 1000;
    const newSupps = suppliers.filter(s => new Date(s.createdAt).getTime() >= thirtyDaysAgo).length;

    const statTotal = getEl('statTotal');
    const statActive = getEl('statActive');
    const statInactive = getEl('statInactive');
    const statNew = getEl('statNew');

    if (statTotal) statTotal.textContent = total;
    if (statActive) statActive.textContent = active;
    if (statInactive) statInactive.textContent = inactive;
    if (statNew) statNew.textContent = newSupps;
}

function renderAll() {
    const list = getFilteredSuppliers();
    if (currentViewMode === 'list') {
        renderTable(list);
    } else {
        renderGrid(list);
    }
    const info = getEl('paginationInfo');
    if (info) {
        info.textContent = `Showing ${list.length} Supplier${list.length !== 1 ? 's' : ''}`;
    }
}

// ============================================================
// 8. DRAWER MANAGEMENT (ADD / EDIT / VIEW Factsheet)
// ============================================================
function openDrawer(mode = 'add', id = null) {
    clearFormErrors();
    const drawer = getEl('supplierDrawer');
    const titleEl = getEl('drawerTitle');
    const saveBtn = getEl('saveSupplierBtn');
    const form = getEl('supplierForm');

    if (!drawer || !form) return;

    // Reset view class
    drawer.classList.remove('mode-view');

    // Select form controls
    const inputs = form.querySelectorAll('.form-control, input[type="checkbox"]');

    if (mode === 'view' && id) {
        const s = suppliers.find(x => x.id === id);
        if (!s) return;
        
        if (titleEl) titleEl.textContent = 'View Vendor Factsheet';
        drawer.classList.add('mode-view');

        // Populate fields
        getEl('formSupplierId').value = s.id;
        getEl('formLogoUrl').value = s.logoUrl || '';
        getEl('formCompanyName').value = s.companyName;
        getEl('formGst').value = s.gst || '';
        getEl('formContactPerson').value = s.contactPerson;
        getEl('formPhone').value = s.phone;
        getEl('formEmail').value = s.email || '';
        getEl('formCity').value = s.city;
        getEl('formPaymentTerms').value = s.paymentTerms;
        getEl('formStatus').value = s.status;
        getEl('formIsPreferred').checked = !!s.isPreferred;
        getEl('formAddress').value = s.address || '';
        getEl('formNotes').value = s.notes || '';

        // Disable input editing
        inputs.forEach(inp => inp.setAttribute('disabled', 'true'));
        if (saveBtn) saveBtn.style.display = 'none';

    } else if (mode === 'edit' && id) {
        const s = suppliers.find(x => x.id === id);
        if (!s) return;

        if (titleEl) titleEl.textContent = 'Edit Vendor Record';

        // Populate fields
        getEl('formSupplierId').value = s.id;
        getEl('formLogoUrl').value = s.logoUrl || '';
        getEl('formCompanyName').value = s.companyName;
        getEl('formGst').value = s.gst || '';
        getEl('formContactPerson').value = s.contactPerson;
        getEl('formPhone').value = s.phone;
        getEl('formEmail').value = s.email || '';
        getEl('formCity').value = s.city;
        getEl('formPaymentTerms').value = s.paymentTerms;
        getEl('formStatus').value = s.status;
        getEl('formIsPreferred').checked = !!s.isPreferred;
        getEl('formAddress').value = s.address || '';
        getEl('formNotes').value = s.notes || '';

        // Enable editing
        inputs.forEach(inp => inp.removeAttribute('disabled'));
        if (saveBtn) saveBtn.style.display = '';

    } else {
        // Add Mode
        if (titleEl) titleEl.textContent = 'Add New Vendor';
        form.reset();
        getEl('formSupplierId').value = '';
        getEl('formStatus').value = 'Active';
        getEl('formIsPreferred').checked = false;

        // Enable editing
        inputs.forEach(inp => inp.removeAttribute('disabled'));
        if (saveBtn) saveBtn.style.display = '';
    }

    drawer.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeDrawer() {
    const drawer = getEl('supplierDrawer');
    if (drawer) drawer.classList.remove('active');
    document.body.style.overflow = '';
}

function clearFormErrors() {
    const form = getEl('supplierForm');
    if (!form) return;
    form.querySelectorAll('.form-control').forEach(el => el.classList.remove('is-invalid'));
    form.querySelectorAll('.field-error-msg').forEach(el => el.style.display = 'none');
}

function validateSupplierForm() {
    let isValid = true;
    const name = getEl('formCompanyName').value.trim();
    const contact = getEl('formContactPerson').value.trim();
    const phone = getEl('formPhone').value.trim();
    const city = getEl('formCity').value.trim();

    if (!name) {
        showError('formCompanyName', 'Company name is required.');
        isValid = false;
    }
    if (!contact) {
        showError('formContactPerson', 'Contact person is required.');
        isValid = false;
    }
    if (!phone) {
        showError('formPhone', 'Phone number is required.');
        isValid = false;
    } else if (!/^\+?[\d\s-]{8,15}$/.test(phone)) {
        showError('formPhone', 'Enter a valid phone number.');
        isValid = false;
    }
    if (!city) {
        showError('formCity', 'City is required.');
        isValid = false;
    }
    return isValid;
}

function showError(inputId, msg) {
    const input = getEl(inputId);
    const err = getEl(`err-${inputId}`);
    if (input) input.classList.add('is-invalid');
    if (err) {
        err.textContent = msg;
        err.style.display = 'block';
    }
}

// ============================================================
// 9. SUPPLIER DETAILS PANEL LOADER (Split detail page)
// ============================================================
function showSupplierDetails(id) {
    const s = suppliers.find(x => x.id === id);
    if (!s) return;

    currentDetailSupplierId = id;
    const bg = strToColor(s.companyName);

    const avatar = getEl('detailAvatar');
    const name = getEl('detailName');
    const idDisp = getEl('detailIdDisplay');
    const badgeWrap = getEl('detailStatusBadgeWrapper');
    const prefWrap = getEl('detailPreferredWrapper');
    const contact = getEl('detailContact');
    const gst = getEl('detailGst');
    const phone = getEl('detailPhone');
    const email = getEl('detailEmail');
    const terms = getEl('detailTerms');
    const address = getEl('detailAddress');
    const notes = getEl('detailNotes');
    const timeline = getEl('detailActivityTimeline');

    if (avatar) {
        avatar.style.background = bg;
        avatar.textContent = getInitials(s.companyName);
    }
    if (name) name.textContent = s.companyName;
    if (idDisp) idDisp.textContent = `Supplier ID: ${s.id}`;
    if (badgeWrap) badgeWrap.innerHTML = `<span class="status-badge ${s.status.toLowerCase()}">${s.status}</span>`;
    if (prefWrap) prefWrap.innerHTML = s.isPreferred ? `<span class="preferred-badge"><i class="fa-solid fa-star"></i> Preferred Partner</span>` : '';

    if (contact) contact.textContent = s.contactPerson;
    if (gst) gst.textContent = s.gst || '—';
    if (phone) phone.textContent = s.phone;
    if (email) email.textContent = s.email || '—';
    if (terms) terms.textContent = s.paymentTerms;
    if (address) address.textContent = s.address || '—';
    if (notes) notes.textContent = s.notes || 'No notes added.';

    // Populate timeline log
    if (timeline) {
        timeline.innerHTML = '';
        const logs = s.activityLog || [];
        if (logs.length === 0) {
            timeline.innerHTML = `
                <div class="activity-item">
                    <div class="activity-marker"></div>
                    <div class="activity-info">
                        <div class="activity-desc">Dossier created</div>
                        <div class="activity-time">${new Date(s.createdAt).toLocaleString()}</div>
                    </div>
                </div>`;
        } else {
            logs.forEach(l => {
                const div = document.createElement('div');
                div.className = 'activity-item';
                div.innerHTML = `
                    <div class="activity-marker"></div>
                    <div class="activity-info">
                        <div class="activity-desc">${escHtml(l.desc)}</div>
                        <div class="activity-time">${escHtml(l.time)}</div>
                    </div>`;
                timeline.appendChild(div);
            });
        }
    }

    // Switch view
    const viewDir = getEl('view-dir-toggle');
    const viewDetail = getEl('view-detail-toggle');
    if (viewDir) viewDir.checked = false;
    if (viewDetail) viewDetail.checked = true;
}

// ============================================================
// 10. PRINTING VENDOR PROFILE
// ============================================================
function printSupplierProfile(id) {
    const s = suppliers.find(x => x.id === id);
    if (!s) return;

    const printWin = window.open('', '_blank');
    printWin.document.write(`
        <html>
        <head>
            <title>Supplier Profile - ${s.companyName}</title>
            <style>
                body { font-family: 'Poppins', sans-serif; padding: 40px; color: #1e293b; }
                h1 { border-bottom: 2px solid #2563eb; padding-bottom: 10px; margin-bottom: 30px; }
                .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-bottom: 30px; }
                .item { margin-bottom: 15px; }
                .label { font-size: 11px; font-weight: 600; color: #64748b; text-transform: uppercase; }
                .value { font-size: 15px; font-weight: 500; margin-top: 4px; }
                .badge { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; background: #e2e8f0; }
            </style>
        </head>
        <body>
            <h1>Vendor Factsheet</h1>
            <div class="grid">
                <div class="item"><div class="label">Company Name</div><div class="value">${s.companyName}</div></div>
                <div class="item"><div class="label">Supplier ID</div><div class="value">${s.id}</div></div>
                <div class="item"><div class="label">Contact Person</div><div class="value">${s.contactPerson}</div></div>
                <div class="item"><div class="label">GST Number</div><div class="value">${s.gst || '—'}</div></div>
                <div class="item"><div class="label">Phone</div><div class="value">${s.phone}</div></div>
                <div class="item"><div class="label">Email</div><div class="value">${s.email || '—'}</div></div>
                <div class="item"><div class="label">City</div><div class="value">${s.city}</div></div>
                <div class="item"><div class="label">Payment Terms</div><div class="value">${s.paymentTerms}</div></div>
                <div class="item"><div class="label">Status</div><div class="value"><span class="badge">${s.status}</span></div></div>
                <div class="item"><div class="label">Preferred Supplier</div><div class="value">${s.isPreferred ? 'Yes' : 'No'}</div></div>
            </div>
            <div class="item" style="border-top: 1px solid #e2e8f0; padding-top: 20px;">
                <div class="label">Address</div><div class="value">${s.address || '—'}</div>
            </div>
            <div class="item" style="margin-top: 20px;">
                <div class="label">Strategic Notes</div><div class="value">${s.notes || 'No additional notes.'}</div>
            </div>
            <script>window.onload = function() { window.print(); window.close(); }</script>
        </body>
        </html>
    `);
    printWin.document.close();
}

// ============================================================
// 11. EXPORT TO CSV
// ============================================================
function exportSupplierCSV(id = null) {
    const targets = id ? suppliers.filter(s => s.id === id) : getFilteredSuppliers();
    let csv = 'Supplier ID,Company Name,GST,Contact Person,Phone,Email,City,Payment Terms,Status,Preferred\n';
    targets.forEach(s => {
        csv += `"${s.id}","${s.companyName.replace(/"/g, '""')}","${s.gst || ''}","${s.contactPerson.replace(/"/g, '""')}","${s.phone}","${s.email || ''}","${s.city}","${s.paymentTerms}","${s.status}","${s.isPreferred ? 'TRUE' : 'FALSE'}"\n`;
    });

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', id ? `vendor_${id}_factsheet.csv` : 'vendor_visible_export.csv');
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast('Export file downloaded successfully!', 'success');
}

// ============================================================
// 12. PARSE CSV IMPORT
// ============================================================
function handleImportCSV(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const text = e.target.result;
            const lines = text.split('\n');
            let importedCount = 0;
            const nowStr = new Date().toLocaleString();

            for (let i = 1; i < lines.length; i++) {
                const line = lines[i].trim();
                if (!line) continue;
                
                // Simple CSV parser
                const parts = line.split(',').map(p => p.replace(/^"|"$/g, '').trim());
                if (parts.length < 2) continue;
                
                const newId = generateSupplierId();
                const newS = {
                    id: newId,
                    companyName: parts[1] || 'Imported Company',
                    gst: parts[2] || '',
                    contactPerson: parts[3] || 'Imported Contact',
                    phone: parts[4] || '+91 99999 88888',
                    email: parts[5] || '',
                    city: parts[6] || 'Imported City',
                    paymentTerms: parts[7] || 'Net 30',
                    status: parts[8] || 'Active',
                    isPreferred: parts[9] === 'TRUE',
                    address: '',
                    notes: 'Imported via CSV file upload.',
                    logoUrl: '',
                    createdAt: new Date().toISOString(),
                    activityLog: [
                        { desc: 'Supplier Imported via CSV Upload', time: nowStr }
                    ]
                };
                
                suppliers.unshift(newS);
                importedCount++;
            }
            
            renderAll();
            updateSummaryCards();
            showToast(`Successfully imported ${importedCount} vendors from CSV!`, 'success');
        } catch (err) {
            showToast('Error parsing CSV file format.', 'error');
        }
    };
    reader.readAsText(file);
}

// ============================================================
// 13. CONCRETE INITIALIZATION
// ============================================================
function initSuppliersPage() {
    updateSummaryCards();
    renderAll();

    // Close Modals
    document.querySelectorAll('.close-modal').forEach(btn => {
        btn.addEventListener('click', () => {
            const deleteModal = getEl('deleteConfirmModal');
            const importModal = getEl('importModal');
            if (deleteModal) deleteModal.classList.remove('active');
            if (importModal) importModal.classList.remove('active');
        });
    });

    // Sidebar navigation active highlight
    const inventoryNavItem = getEl('inventoryNavItem');
    if (inventoryNavItem) inventoryNavItem.classList.add('open');

    // Add Vendor Opens Drawer
    const openAddBtn = getEl('openAddSupplierModal');
    if (openAddBtn) {
        openAddBtn.addEventListener('click', () => openDrawer('add'));
    }

    // Close Drawer triggers
    const closeDrawerBtn = getEl('closeDrawerBtn');
    const closeDrawerBtn2 = getEl('closeDrawerBtn2');
    if (closeDrawerBtn) closeDrawerBtn.addEventListener('click', closeDrawer);
    if (closeDrawerBtn2) closeDrawerBtn2.addEventListener('click', closeDrawer);

    // Form Submit (Save / Edit)
    const form = getEl('supplierForm');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            if (!validateSupplierForm()) return;

            const id = getEl('formSupplierId').value;
            const nowStr = new Date().toLocaleString();

            if (id) {
                // Edit
                const idx = suppliers.findIndex(x => x.id === id);
                if (idx !== -1) {
                    const original = suppliers[idx];
                    const logs = [...(original.activityLog || [])];
                    
                    if (original.gst !== getEl('formGst').value.trim()) {
                        logs.push({ desc: 'GST Updated', time: nowStr });
                    }
                    if (original.status !== getEl('formStatus').value) {
                        logs.push({ desc: `Status Changed to ${getEl('formStatus').value}`, time: nowStr });
                    }
                    if (original.notes !== getEl('formNotes').value.trim()) {
                        logs.push({ desc: 'Notes Added/Updated', time: nowStr });
                    }

                    suppliers[idx] = {
                        ...original,
                        logoUrl: getEl('formLogoUrl').value.trim(),
                        companyName: getEl('formCompanyName').value.trim(),
                        gst: getEl('formGst').value.trim(),
                        contactPerson: getEl('formContactPerson').value.trim(),
                        phone: getEl('formPhone').value.trim(),
                        email: getEl('formEmail').value.trim(),
                        city: getEl('formCity').value.trim(),
                        paymentTerms: getEl('formPaymentTerms').value,
                        status: getEl('formStatus').value,
                        isPreferred: getEl('formIsPreferred').checked,
                        address: getEl('formAddress').value.trim(),
                        notes: getEl('formNotes').value.trim(),
                        activityLog: logs
                    };
                    showToast('Supplier updated successfully.', 'success');
                }
            } else {
                // Add
                const newId = generateSupplierId();
                const newS = {
                    id: newId,
                    companyName: getEl('formCompanyName').value.trim(),
                    gst: getEl('formGst').value.trim(),
                    contactPerson: getEl('formContactPerson').value.trim(),
                    phone: getEl('formPhone').value.trim(),
                    email: getEl('formEmail').value.trim(),
                    city: getEl('formCity').value.trim(),
                    paymentTerms: getEl('formPaymentTerms').value,
                    status: getEl('formStatus').value,
                    isPreferred: getEl('formIsPreferred').checked,
                    address: getEl('formAddress').value.trim(),
                    notes: getEl('formNotes').value.trim(),
                    logoUrl: getEl('formLogoUrl').value.trim(),
                    createdAt: new Date().toISOString(),
                    activityLog: [
                        { desc: 'Supplier Created', time: nowStr }
                    ]
                };
                suppliers.unshift(newS);
                showToast(`New Supplier ${newS.companyName} added.`, 'success');
            }

            closeDrawer();
            renderAll();
            updateSummaryCards();
        });
    }

    // Container click delegation for Details Page View
    const handleContainerClick = (e) => {
        const tr = e.target.closest('tr[data-id]');
        const card = e.target.closest('.supplier-card');
        const target = tr || card;

        if (target) {
            // Ignore click if it fell inside actions wrapper or any button/link
            if (e.target.closest('.actions-cell') || e.target.closest('button') || e.target.closest('a')) {
                return;
            }
            showSupplierDetails(target.dataset.id);
        }
    };

    const tableBody = getEl('supplierTableBody');
    const gridBody = getEl('supplierGridBody');
    if (tableBody) tableBody.addEventListener('click', handleContainerClick);
    if (gridBody) gridBody.addEventListener('click', handleContainerClick);

    // Direct action click events inside list table / grid
    const handleActionClick = (e) => {
        const viewBtn = e.target.closest('.action-view-trigger');
        const editBtn = e.target.closest('.action-edit-trigger');

        if (viewBtn) {
            e.stopPropagation();
            openDrawer('view', viewBtn.dataset.id);
        } else if (editBtn) {
            e.stopPropagation();
            openDrawer('edit', editBtn.dataset.id);
        }
    };

    if (tableBody) tableBody.addEventListener('click', handleActionClick);
    if (gridBody) gridBody.addEventListener('click', handleActionClick);

    // Dropdown Action Menu Triggers
    const handleMenuClick = (e) => {
        const trigger = e.target.closest('.action-menu-trigger');
        if (trigger) {
            e.stopPropagation();
            const id = trigger.dataset.id;
            
            // Close any currently active menus first
            document.querySelectorAll('.dropdown-menu-list').forEach(m => {
                if (m.id !== `menu-${id}` && m.id !== `menu-grid-${id}`) {
                    m.classList.remove('active');
                }
            });

            // Toggle target menu
            const tableMenu = getEl(`menu-${id}`);
            const gridMenu = getEl(`menu-grid-${id}`);
            if (tableMenu) tableMenu.classList.toggle('active');
            if (gridMenu) gridMenu.classList.toggle('active');
            return;
        }

        // Handle dropdown menu action links
        const link = e.target.closest('.dropdown-menu-list a');
        if (link) {
            e.preventDefault();
            e.stopPropagation();
            const id = link.dataset.id;
            const parentMenu = link.closest('.dropdown-menu-list');
            if (parentMenu) parentMenu.classList.remove('active');

            if (link.classList.contains('view-menu-item')) {
                openDrawer('view', id);
            } else if (link.classList.contains('edit-menu-item')) {
                openDrawer('edit', id);
            } else if (link.classList.contains('print-menu-item')) {
                printSupplierProfile(id);
            } else if (link.classList.contains('export-menu-item')) {
                exportSupplierCSV(id);
            } else if (link.classList.contains('delete-menu-item')) {
                const s = suppliers.find(x => x.id === id);
                if (s) {
                    pendingDeleteId = id;
                    const deleteName = getEl('deleteSupplierName');
                    const deleteModal = getEl('deleteConfirmModal');
                    if (deleteName) deleteName.textContent = s.companyName;
                    if (deleteModal) deleteModal.classList.add('active');
                }
            }
        }
    };

    document.addEventListener('click', (e) => {
        handleMenuClick(e);
        // Click outside closes dropdown menus
        if (!e.target.closest('.dropdown-trigger-container')) {
            document.querySelectorAll('.dropdown-menu-list').forEach(m => m.classList.remove('active'));
        }
    });

    // Confirm Delete Event
    const confirmDelete = getEl('confirmDeleteBtn');
    if (confirmDelete) {
        confirmDelete.addEventListener('click', () => {
            if (!pendingDeleteId) return;
            const idx = suppliers.findIndex(x => x.id === pendingDeleteId);
            if (idx !== -1) {
                const name = suppliers[idx].companyName;
                suppliers.splice(idx, 1);
                showToast(`Vendor ${name} has been removed.`, 'error');
                renderAll();
                updateSummaryCards();
                
                // If currently viewed detail is deleted, go back to list
                if (currentDetailSupplierId === pendingDeleteId) {
                    const backBtn = getEl('backToListBtn');
                    if (backBtn) backBtn.click();
                }
            }
            const deleteModal = getEl('deleteConfirmModal');
            if (deleteModal) deleteModal.classList.remove('active');
            pendingDeleteId = null;
        });
    }

    // Back to Directory list button logic
    const backBtn = getEl('backToListBtn');
    if (backBtn) {
        backBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const viewDir = getEl('view-dir-toggle');
            const viewDetail = getEl('view-detail-toggle');
            if (viewDir) viewDir.checked = true;
            if (viewDetail) viewDetail.checked = false;
            currentDetailSupplierId = null;
        });
    }

    // Detail page edit and print actions
    const detailPrint = getEl('detailPrintBtn');
    const detailEdit = getEl('detailEditBtn');
    if (detailPrint) {
        detailPrint.addEventListener('click', () => {
            if (currentDetailSupplierId) printSupplierProfile(currentDetailSupplierId);
        });
    }
    if (detailEdit) {
        detailEdit.addEventListener('click', () => {
            if (currentDetailSupplierId) openDrawer('edit', currentDetailSupplierId);
        });
    }

    // Search Input listeners
    const search = getEl('searchInput');
    const clearSearch = getEl('clearSearchBtn');
    if (search) {
        search.addEventListener('input', () => {
            const val = search.value.trim();
            if (clearSearch) clearSearch.style.display = val ? 'block' : 'none';
            renderAll();
        });
    }
    if (clearSearch) {
        clearSearch.addEventListener('click', () => {
            if (search) search.value = '';
            clearSearch.style.display = 'none';
            renderAll();
        });
    }

    // Status tabs filters logic
    document.querySelectorAll('.status-filters .filter-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.status-filters .filter-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            selectedStatusFilter = tab.dataset.status;
            renderAll();
        });
    });

    // View toggles list / grid
    const listBtn = getEl('listViewBtn');
    const gridBtn = getEl('gridViewBtn');
    const tableCont = getEl('supplierTableContainer');
    const gridCont = getEl('supplierGridContainer');

    if (listBtn) {
        listBtn.addEventListener('click', () => {
            listBtn.classList.add('active');
            if (gridBtn) gridBtn.classList.remove('active');
            if (tableCont) tableCont.style.display = '';
            if (gridCont) gridCont.style.display = 'none';
            currentViewMode = 'list';
            renderAll();
        });
    }
    if (gridBtn) {
        gridBtn.addEventListener('click', () => {
            gridBtn.classList.add('active');
            if (listBtn) listBtn.classList.remove('active');
            if (tableCont) tableCont.style.display = 'none';
            if (gridCont) gridCont.style.display = '';
            currentViewMode = 'grid';
            renderAll();
        });
    }

    // Refresh Action
    const refresh = getEl('refreshBtn');
    if (refresh) {
        refresh.addEventListener('click', () => {
            const icon = refresh.querySelector('i');
            if (icon) icon.classList.add('rotating');
            setTimeout(() => {
                // Reset inputs and tabs
                if (search) {
                    search.value = '';
                    if (clearSearch) clearSearch.style.display = 'none';
                }
                selectedStatusFilter = '';
                document.querySelectorAll('.status-filters .filter-tab').forEach(t => {
                    if (t.dataset.status === '') t.classList.add('active');
                    else t.classList.remove('active');
                });
                renderAll();
                updateSummaryCards();
                if (icon) icon.classList.remove('rotating');
                showToast('Vendor list updated.', 'success');
            }, 600);
        });
    }

    // Export Directory CSV
    const exportButton = getEl('exportBtn');
    if (exportButton) {
        exportButton.addEventListener('click', () => exportSupplierCSV());
    }

    // Import Dialog actions
    const importButton = getEl('importBtn');
    if (importButton) {
        importButton.addEventListener('click', () => {
            const fileInput = getEl('importFileInput');
            if (fileInput) fileInput.value = '';
            const importModal = getEl('importModal');
            if (importModal) importModal.classList.add('active');
        });
    }

    const confirmImport = getEl('confirmImportBtn');
    if (confirmImport) {
        confirmImport.addEventListener('click', () => {
            const fileInput = getEl('importFileInput');
            if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
                showToast('Please select a CSV file to upload.', 'error');
                return;
            }
            handleImportCSV(fileInput.files[0]);
            const importModal = getEl('importModal');
            if (importModal) importModal.classList.remove('active');
        });
    }
}

// Ensure execution is fired correctly on readystatechange or DomContentLoaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSuppliersPage);
} else {
    initSuppliersPage();
}
