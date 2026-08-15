# SmartBilling

> A full-stack Grocery Store Management System for managing inventory, billing, customers, suppliers, returns, and business operations from a centralized platform.

---

## 📌 About the Project

**SmartBilling** is a web-based Grocery Store Management System designed to simplify and organize the daily operations of a grocery business.

The system provides a centralized platform where an administrator can manage products and inventory, create and manage bills, maintain customer and supplier information, process returns and refunds, and view business reports.

The main objective is to reduce manual work, maintain accurate records, and provide a structured way to manage store operations.

---

## 🎯 Key Objectives

- Centralize grocery store operations in one system.
- Maintain accurate product and inventory records.
- Simplify billing and sales management.
- Manage customers, suppliers, returns, and refunds.
- Provide useful business reports and analytics.
- Maintain secure administrator access.
- Keep store data organized and easy to manage.

---

## 🏗️ System Structure

SmartBilling is divided into separate functional modules. Each module handles a specific area of grocery store operations.

```text
                         SmartBilling
                              │
             ┌────────────────┴────────────────┐
             │                                 │
        Admin Authentication              Main System
                                               │
        ┌──────────────┬──────────────┬────────┴──────────────┐
        │              │              │                       │
   Inventory      Billing & Sales   Customers          Suppliers
        │              │
        │              ├── Billing
        │              ├── Billing History
        │              ├── Returns & Refunds
        │              └── Sales
        │
        ├── Products
        ├── Categories
        ├── Suppliers
        ├── Stock Alerts
        └── Stock Audit
                    ┌─────────────────────┐
                    │ Reports & Analytics │
                    └─────────────────────┘
                    ┌─────────────────────┐
                    │      Settings       │
                    └─────────────────────┘
```

---

## 📦 Main Modules

### 1. Inventory Management
Handles product and stock management.

Includes:
- Product Catalog
- Product Categories
- Supplier Directory
- Stock Alerts
- Stock Audit and Adjustments

This module helps the administrator maintain accurate inventory information and monitor stock movement.

### 2. Billing & Sales
Handles the store's sales and billing operations.

Includes:
- Billing Dashboard
- Create Bill
- Billing History
- Returns & Refunds
- Sales Reports

Bills, payments, sales records, returns, and related transactions are managed through this module.

### 3. Customer Management
Maintains customer-related information and purchase records.

It allows the administrator to manage customer details and view relevant transaction information.

### 4. Reports & Analytics
Provides business-level information generated from the system's operational data.

It focuses on understanding business performance and providing useful reports rather than performing daily inventory or billing operations.

### 5. Settings
Contains system and store configuration options that are separate from daily inventory and billing operations.

---

## 🔐 Authentication

The current system uses **Admin Authentication**.

The administrator has access to the main management modules of the system.

Manager and Staff/Cashier accounts are not part of the current implementation.

---

## 🛠️ Technology Stack

| Layer     | Technology              |
|-----------|--------------------------|
| Frontend  | HTML, CSS, JavaScript    |
| Backend   | Python, Flask            |
| Database  | MySQL                    |
| ORM       | SQLAlchemy               |

> ⚠️ **Note:** If the project is still running on `smart_grocery.db` (SQLite) rather than a live MySQL instance, update the Database row above to reflect that until the MySQL migration is actually complete — keeping this table accurate matters for anyone setting up the project locally.

---

## 🔄 Application Architecture

```text
┌──────────────────────────────┐
│          Frontend            │
│     HTML + CSS + JavaScript  │
└──────────────┬───────────────┘
               │
               │ HTTP Requests
               ▼
┌──────────────────────────────┐
│           Backend            │
│       Python + Flask         │
│                              │
│  Authentication              │
│  Business Logic              │
│  Validation                  │
│  API / Routes                │
└──────────────┬───────────────┘
               │
               │ Database Operations
               ▼
┌──────────────────────────────┐
│           Database           │
│            MySQL             │
│                              │
│  Products                    │
│  Users                       │
│  Customers                   │
│  Suppliers                   │
│  Bills & Sales                │
│  Returns & Refunds            │
│  Inventory Records            │
└──────────────────────────────┘
```

---

## 🔁 Basic Workflow

```text
Admin Login
     ↓
Dashboard
     ↓
Manage Store Data
     ↓
Inventory / Billing / Customers / Suppliers
     ↓
Transactions & Records
     ↓
Reports & Analytics
```

---

## ✨ System Highlights

- Centralized grocery store management
- Structured inventory control
- Integrated billing and sales management
- Customer and supplier records
- Return and refund processing
- Stock monitoring and audit records
- Business reporting and analytics
- Admin-based authentication
- Responsive web interface
- Light and dark theme support

---

## 📌 Project Information

| Detail          | Information                  |
|------------------|-------------------------------|
| Project Name     | SmartBilling                 |
| Project Type     | Full-Stack Web Application    |
| Domain           | Grocery Store Management      |
| Frontend         | HTML, CSS, JavaScript         |
| Backend          | Python, Flask                 |
| Database         | MySQL                         |
| Authentication   | Admin                         |

---

## 👩‍💻 Project Structure

```text
SmartBilling
│
├── Authentication
├── Inventory Management
├── Billing & Sales
├── Returns & Refunds
├── Customer Management
├── Reports & Analytics
└── Settings
```

---

## 🎯 Purpose

SmartBilling aims to provide a simple, centralized, and organized solution for grocery store management by bringing inventory, billing, customers, suppliers, returns, and business reporting together in a single web application.
