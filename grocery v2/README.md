# Smart Grocery Inventory & Billing System v2

A commercial-grade, full-stack, enterprise web application designed for supermarket, grocery store, and retail management. Built with Python Flask, SQLAlchemy ORM, Flask-Login, Flask-WTF, MySQL/SQLite DB, Vanilla HTML5/CSS3/JS (ES6+), and Font Awesome icons.

---

## Table of Contents

1. [Overview & Architecture](#overview--architecture)
2. [Technology Stack](#technology-stack)
3. [Folder Structure](#folder-structure)
4. [Database Design & Schema](#database-design--schema)
5. [System Modules Breakdown](#system-modules-breakdown)
6. [Security & Password Confirmation](#security--password-confirmation)
7. [Installation & Setup Guide](#installation--setup-guide)
8. [Default Admin Credentials](#default-admin-credentials)

---

## Overview & Architecture

**Smart Grocery Inventory & Billing System v2** follows Clean Architecture principles separating data persistence, business logic, validation, and visual rendering. It delivers a fast, responsive, SaaS-grade experience comparable to commercial ERPs (such as Zoho Inventory, Shopify Admin, Vyapar, and Marg ERP).

```
+-----------------------------------------------------------------+
|                        Browser Frontend                         |
|   HTML5 + Vanilla CSS3 (Variables, Cards, Glassmorphism, Toast)  |
|   Vanilla JavaScript (ES6+, POS Terminal, Barcode, Password Modal)|
+-----------------------------------------------------------------+
                                | HTTP REST / CSRF AJAX
                                v
+-----------------------------------------------------------------+
|                         Flask Backend                           |
|  App Factory (app/__init__.py)                                  |
|  11 Blueprints (Auth, Dashboard, Products, Categories, POS...)  |
|  Services Layer (Auth, Billing, Inventory, Reports)              |
|  Validators Layer (Flask-WTF forms & password checks)           |
+-----------------------------------------------------------------+
                                | SQLAlchemy ORM
                                v
+-----------------------------------------------------------------+
|                        Database Engine                          |
|  MySQL (Production) / SQLite (Zero-Config Development Fallback) |
+-----------------------------------------------------------------+
```

---

## Technology Stack

- **Frontend**: HTML5, Vanilla CSS3 (Custom 8px grid system, dark/light contrast), Vanilla JavaScript (ES6+), Font Awesome 6, Chart.js.
- **Backend**: Python 3.8+, Flask, Flask Blueprints, Flask-Login (session security), Flask-WTF (CSRF & form validation), bcrypt (password hashing), Werkzeug.
- **Database**: MySQL (via SQLAlchemy & PyMySQL) with automatic SQLite zero-config development fallback.
- **Reporting**: Python `csv` module, ReportLab (PDF), openpyxl (Excel export).

---

## Folder Structure

```
grocery v2/
│
├── run.py                    # Application Entry Point & Auto Seed Generator
├── config.py                 # Security, Database URIs, Uploads & Cookie Config
├── requirements.txt          # Python dependencies
├── README.md                 # Complete documentation
│
└── app/
    ├── __init__.py           # Flask App Factory & Blueprint Registration
    │
    ├── database/
    │   └── __init__.py       # SQLAlchemy db instance
    │
    ├── models/               # SQLAlchemy DB Models
    │   ├── __init__.py
    │   ├── user.py           # User model with bcrypt hashing
    │   ├── category.py       # Category model with deletion protection
    │   ├── supplier.py       # Supplier model
    │   ├── customer.py       # Customer CRM model
    │   ├── product.py        # Product model (SKU, Barcode, Stock, Expiry)
    │   ├── bill.py           # Bill, BillItem, and PaymentMethod models
    │   ├── inventory.py      # InventoryHistory audit trail model
    │   └── setting.py        # SystemSetting key-value configuration
    │
    ├── services/             # Business Logic Layer
    │   ├── auth_service.py      # Sensitive action password verification
    │   ├── inventory_service.py # Stock adjustment & audit logs
    │   ├── billing_service.py   # Invoice sequence, GST, & inventory deduction
    │   └── report_service.py    # CSV/Excel/PDF export engine
    │
    ├── validators/
    │   └── forms.py          # WTForms validation & sensitive action forms
    │
    ├── middleware/
    │   └── auth_middleware.py # Admin route guards & permission checks
    │
    ├── utils/
    │   └── helpers.py        # Safe image upload utilities
    │
    ├── routes/               # Flask Blueprints
    │   ├── auth_routes.py
    │   ├── dashboard_routes.py
    │   ├── product_routes.py
    │   ├── category_routes.py
    │   ├── supplier_routes.py
    │   ├── customer_routes.py
    │   ├── inventory_routes.py
    │   ├── billing_routes.py
    │   ├── report_routes.py
    │   ├── setting_routes.py
    │   └── profile_routes.py
    │
    ├── static/
    │   ├── css/
    │   │   └── main.css      # Complete CSS Design System & Theme
    │   ├── js/
    │   │   ├── main.js       # Toast notifications & Password Confirmation Modal
    │   │   ├── pos.js        # POS Terminal Live Billing & Barcode Reader
    │   │   └── charts.js     # Dashboard Chart.js Integration
    │   └── uploads/          # Uploaded product and profile images
    │
    └── templates/            # Jinja2 HTML Templates
        ├── base.html         # Master layout (Sidebar, Navbar, Toasts, Modal)
        ├── auth/login.html
        ├── dashboard/index.html
        ├── products/index.html & form.html
        ├── categories/index.html
        ├── suppliers/index.html
        ├── customers/index.html
        ├── inventory/index.html
        ├── billing/pos.html & invoice.html
        ├── reports/index.html
        ├── settings/index.html
        ├── profile/index.html
        └── errors/404.html, 500.html, 403.html
```

---

## Database Design & Schema

The database is normalized into 10 key tables with foreign keys, indexes, and cascades:

1. **`users`**: Stores user credentials, roles (`Admin`, `Manager`, `Cashier`), bcrypt hashes, profile pictures.
2. **`categories`**: Stores product categories. Linked to `products`.
3. **`suppliers`**: Stores supplier contact details, GSTIN, and address.
4. **`customers`**: Customer CRM storing total purchase spend and contact numbers.
5. **`products`**: Contains product SKU, barcode, brand, purchase/selling price, tax %, stock levels (min/max), manufacturing/expiry dates, unit of measure, and image.
6. **`bills`**: Master invoice header (Bill Number, Subtotal, Tax, Discount, Round Off, Net Amount, Payment Method, User ID, Customer ID).
7. **`bill_items`**: Line items per bill (Product ID, Product Name, Unit Price, Quantity, Tax %, Line Total).
8. **`inventory_history`**: Audit trail of every stock change (Stock In, Stock Out, Sale, Adjustment) with user ID, timestamp, and remaining quantity.
9. **`system_settings`**: Key-value settings (Store Name, GST, Phone, Email, Currency Symbol, Invoice Prefix, Default Tax %).
10. **`payment_methods`**: Payment mode lookup table (`Cash`, `UPI`, `Card`).

---

## System Modules Breakdown

1. **Dashboard Overview**:
   - KPIs for Today's Sales, Monthly Sales, Total Revenue, Total Products.
   - Live Alert Cards for Low Stock, Out of Stock, and Expired Products.
   - Interactive Chart.js graphs for 7-day sales trends & category distributions.
   - Recent Bills and Inventory Audit feeds.

2. **Product Management**:
   - Comprehensive CRUD with Name, SKU, Barcode, Category, Brand, Supplier, Purchase Price, Selling Price, Tax %, Stock, Min/Max alerts, Expiry date, Unit, Image upload.
   - Instant Search, Category Filter, Stock Level Filter (Low/Out/Expired), Pagination.
   - CSV Export & Price change protection.

3. **Category Management**:
   - Category creation, editing, status toggling.
   - **Protection Guard**: Deletion is blocked if active products are assigned to the category.

4. **Supplier Management**:
   - Wholesale supplier CRM with Phone, Email, GST Number, Address.

5. **Customer Management**:
   - Retail customer tracking with phone number uniqueness, total spend aggregation.

6. **Inventory Management & Audit Logs**:
   - Stock adjustments (`Stock In`, `Stock Out`, `Audit Correction`).
   - Automated stock deduction during POS Checkout.
   - Real-time audit history log tracking who changed what and when.

7. **POS Billing & Checkout**:
   - Barcode Scanner integration (auto item add on Enter).
   - Live client cart calculation (Subtotal, GST Tax, Discount, Round Off, Net Total).
   - Customer selection (Default: Walk-in).
   - Payment method toggle (Cash, UPI, Card).
   - Printable HTML Tax Invoice generation (`/billing/invoice/<id>`).

8. **Reports & Business Analytics**:
   - Sales Reports, Stock Reports, Low Stock Reports, Expired Product Reports, Customer Insights.
   - CSV download exports.

9. **System Settings**:
   - Store branding, GST registration, Invoice Prefix, Currency symbol, Default tax percentage.

10. **User Profile & Account Security**:
    - Profile name, email, avatar image, password updates.

---

## Security & Password Confirmation

- **Password Confirmation Modal**: Whenever a sensitive/destructive action is performed:
  - Delete Product / Delete Category / Delete Supplier / Delete Customer / Delete Bill
  - Manual Inventory Adjustment
  - Changing Product Selling Price
  - Modifying System Settings
  
  The system displays a password confirmation modal. Without entering the user's correct account password, the request is rejected immediately by the backend `verify_sensitive_password()` service.

- **Session & CSRF**: All forms are secured using Flask-WTF CSRF tokens and HttpOnly session cookies. Direct URL access after logout is strictly prevented.

---

## Installation & Setup Guide

### 1. Clone & Navigate
```bash
cd "grocery v2"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Configuration (Optional)
By default, the application runs on **SQLite** (`instance/smart_grocery.db`) with zero external database setup required.

To connect to a **MySQL** server, set environment variables:
```bash
export MYSQL_HOST="localhost"
export MYSQL_USER="root"
export MYSQL_PASSWORD="your_password"
export MYSQL_DB="smart_grocery_db"
export DATABASE_URL="mysql+pymysql://root:your_password@localhost:3306/smart_grocery_db"
```

### 4. Run Server
```bash
python run.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## Default Admin Credentials

Upon initial launch, `run.py` automatically initializes tables and seeds default admin credentials:

- **Username**: `admin`
- **Password**: `admin123`
- **Role**: `Admin`
