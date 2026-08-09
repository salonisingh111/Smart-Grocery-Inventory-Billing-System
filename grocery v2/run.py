import os
from app import create_app
from app.database import db
from app.models import User, Category, Supplier, Customer, Product, SystemSetting, PaymentMethod, UserNotification

app = create_app()

def init_seed_data():
    """Seeds the database with essential default production data if empty."""
    instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    with app.app_context():
        # Dynamic schema migration for missing columns
        try:
            with db.engine.connect() as conn:
                result = conn.execute(db.text("PRAGMA table_info(users)")).fetchall()
                columns = [row[1] for row in result]
                if 'last_login_at' not in columns:
                    conn.execute(db.text("ALTER TABLE users ADD COLUMN last_login_at DATETIME"))
                if 'last_login_ip' not in columns:
                    conn.execute(db.text("ALTER TABLE users ADD COLUMN last_login_ip VARCHAR(45)"))
                
                # Check bill_items table
                bitem_res = conn.execute(db.text("PRAGMA table_info(bill_items)")).fetchall()
                bitem_cols = [r[1] for r in bitem_res]
                if 'returned_quantity' not in bitem_cols and len(bitem_cols) > 0:
                    conn.execute(db.text("ALTER TABLE bill_items ADD COLUMN returned_quantity INTEGER DEFAULT 0"))
                conn.commit()
        except Exception as e:
            print("Schema migration check:", e)

        db.create_all()

        # Sync stock alert notifications on startup
        try:
            from app.utils.notifications import initial_sync_all_stock_alerts
            initial_sync_all_stock_alerts()
        except Exception as e:
            print(f"Notification sync skipped: {e}")

        # Seed Default Admin User
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@grocery.com',
                full_name='System Admin',
                role='Admin',
                status='Active'
            )
            admin.set_password('admin123')
            db.session.add(admin)

        # Seed System Settings
        default_settings = [
            ('STORE_NAME', 'Smart Grocery Supermarket', 'Store Display Name'),
            ('GST_NUMBER', '27AAACG1234F1Z5', 'GST Registration Number'),
            ('STORE_PHONE', '+91 98765 43210', 'Store Phone Number'),
            ('STORE_EMAIL', 'support@smartgrocery.com', 'Store Email Address'),
            ('STORE_ADDRESS', '123 Main High Street, Market City', 'Store Full Address'),
            ('CURRENCY_CODE', 'INR', 'Currency Code'),
            ('CURRENCY', '₹', 'Currency Symbol'),
            ('TIMEZONE', 'Asia/Kolkata', 'System Timezone'),
            ('DATE_FORMAT', 'DD/MM/YYYY', 'Date Format'),
            ('TAX_PERCENTAGE', '5.0', 'Default Tax %'),
            ('INVOICE_PREFIX', 'INV', 'Invoice Prefix'),
            ('NEXT_INVOICE_NUMBER', '1001', 'Next Invoice Serial Number'),
            ('ENABLE_TAX', 'on', 'Enable Tax Calculation'),
            ('ENABLE_DISCOUNT', 'on', 'Enable Item Discounts'),
            ('PRINT_LOGO_ON_INVOICE', 'on', 'Print Logo on Invoice'),
            ('INVOICE_FOOTER_MSG', 'Thank you for shopping with Smart Grocery Supermarket!', 'Invoice Footer Message'),
            ('INVOICE_FORMAT', '80mm Thermal Receipt', 'Invoice Paper Format'),
            ('DEFAULT_PAYMENT_METHOD', 'Cash', 'Default Checkout Payment Method'),
            ('LOW_STOCK_THRESHOLD', '10', 'Low Stock Alert Threshold'),
            ('ENABLE_EXPIRY_TRACKING', 'on', 'Enable Expiry Date Tracking'),
            ('AUTO_GENERATE_SKU', 'on', 'Auto Generate SKU Codes'),
            ('ALLOW_NEGATIVE_STOCK', 'off', 'Allow Negative Inventory Stock'),
            ('DEFAULT_PRODUCT_UNIT', 'pcs', 'Default Product Unit'),
            ('SESSION_TIMEOUT_MINS', '30', 'Session Timeout Minutes'),
            ('REQUIRE_PWD_CONFIRM_DELETE', 'on', 'Require Password Confirmation for Delete'),
            ('NOTIF_LOW_STOCK', 'on', 'Low Stock Alert Notifications'),
            ('NOTIF_EXPIRY', 'on', 'Expiry Warning Notifications'),
            ('NOTIF_SALES', 'on', 'Sales Milestone Notifications'),
            ('NOTIF_SYSTEM', 'on', 'System Security Notifications')
        ]
        for key, val, desc in default_settings:
            if not SystemSetting.query.filter_by(setting_key=key).first():
                db.session.add(SystemSetting(setting_key=key, setting_value=val, description=desc))

        # Seed Payment Methods
        methods = [
            ('Cash', 'Cash Payment'),
            ('UPI', 'UPI / QR Code'),
            ('Card', 'Credit / Debit Card')
        ]
        for code, name in methods:
            if not PaymentMethod.query.filter_by(code=code).first():
                db.session.add(PaymentMethod(code=code, name=name, is_active=True))

        # Seed Default Categories if none
        if Category.query.count() == 0:
            c1 = Category(name='Dairy & Bakery', code='CAT-DAIRY', description='Fresh milk, butter, cheese and baked goods', status='Active')
            c2 = Category(name='Beverages & Drinks', code='CAT-BEV', description='Soft drinks, juices, tea and coffee', status='Active')
            c3 = Category(name='Snacks & Packaged Food', code='CAT-SNK', description='Chips, biscuits, instant noodles and snacks', status='Active')
            c4 = Category(name='Fruits & Vegetables', code='CAT-FVT', description='Fresh organic fruits and vegetables', status='Active')
            c5 = Category(name='Staples & Grains', code='CAT-STP', description='Flour, rice, pulse, oil and spices', status='Active')
            c6 = Category(name='Cleaning & Care', code='CAT-CARE', description='Soaps, detergents, shampoos and household care', status='Active')
            db.session.add_all([c1, c2, c3, c4, c5, c6])
            db.session.flush()
        else:
            c1 = Category.query.filter_by(code='CAT-DAIRY').first() or Category.query.first()
            c2 = Category.query.filter_by(code='CAT-BEV').first() or c1
            c3 = Category.query.filter_by(code='CAT-SNK').first() or c1
            c4 = Category.query.filter_by(code='CAT-FVT').first() or c1
            c5 = Category.query.filter_by(code='CAT-STP').first() or Category(name='Staples & Grains', code='CAT-STP', description='Flour, rice, pulse, oil and spices', status='Active')
            c6 = Category.query.filter_by(code='CAT-CARE').first() or Category(name='Cleaning & Care', code='CAT-CARE', description='Soaps, detergents, household care', status='Active')
            if not c5.id:
                db.session.add(c5)
            if not c6.id:
                db.session.add(c6)
            db.session.flush()

        # Seed Default Supplier
        if Supplier.query.count() == 0:
            sup = Supplier(name='Global Foods Ltd', phone='+91 91234 56789', email='supply@globalfoods.com', gst_number='27AAACG9999F1Z1', address='Warehouse #4, City Industrial Area', status='Active')
            db.session.add(sup)
            db.session.flush()
        else:
            sup = Supplier.query.first()

        # Seed Default Products if count < 10
        if Product.query.count() < 10:
            seed_items = [
                # Dairy & Bakery
                Product(name='Amul Taaza Toned Milk 1L', sku='MILK-001', barcode='890126201001', category_id=c1.id, supplier_id=sup.id, brand='Amul', purchase_price=60.0, selling_price=66.0, tax_percent=0.0, quantity=45, min_stock=10, max_stock=200, unit='l', status='Active'),
                Product(name='Britannia Brown Bread 400g', sku='BRD-001', barcode='890105800001', category_id=c1.id, supplier_id=sup.id, brand='Britannia', purchase_price=35.0, selling_price=40.0, tax_percent=0.0, quantity=25, min_stock=5, max_stock=100, unit='pkt', status='Active'),
                Product(name='Amul Pasteurised Butter 500g', sku='BTR-001', barcode='890126202002', category_id=c1.id, supplier_id=sup.id, brand='Amul', purchase_price=240.0, selling_price=275.0, tax_percent=5.0, quantity=18, min_stock=5, max_stock=50, unit='pcs', status='Active'),

                # Beverages
                Product(name='Coca-Cola 750ml Bottle', sku='BEV-001', barcode='5449000000996', category_id=c2.id, supplier_id=sup.id, brand='Coca-Cola', purchase_price=35.0, selling_price=40.0, tax_percent=18.0, quantity=80, min_stock=15, max_stock=300, unit='pcs', status='Active'),
                Product(name='Brooke Bond Red Label Tea 500g', sku='BEV-002', barcode='890103001002', category_id=c2.id, supplier_id=sup.id, brand='Red Label', purchase_price=260.0, selling_price=310.0, tax_percent=5.0, quantity=30, min_stock=8, max_stock=100, unit='pkt', status='Active'),
                Product(name='Nescafe Classic Coffee Jar 100g', sku='BEV-003', barcode='890105802003', category_id=c2.id, supplier_id=sup.id, brand='Nescafe', purchase_price=290.0, selling_price=340.0, tax_percent=12.0, quantity=22, min_stock=5, max_stock=80, unit='pcs', status='Active'),

                # Snacks & Packaged Food
                Product(name='Lay\'s Classic Salted Potato Chips 50g', sku='SNK-001', barcode='890149110001', category_id=c3.id, supplier_id=sup.id, brand='Lay\'s', purchase_price=16.0, selling_price=20.0, tax_percent=12.0, quantity=120, min_stock=20, max_stock=500, unit='pkt', status='Active'),
                Product(name='Maggi 2-Minute Masala Noodles 280g', sku='SNK-002', barcode='890105886002', category_id=c3.id, supplier_id=sup.id, brand='Maggi', purchase_price=42.0, selling_price=48.0, tax_percent=5.0, quantity=90, min_stock=15, max_stock=300, unit='pkt', status='Active'),
                Product(name='Oreo Vanilla Cream Biscuits 120g', sku='SNK-003', barcode='890126289003', category_id=c3.id, supplier_id=sup.id, brand='Oreo', purchase_price=25.0, selling_price=30.0, tax_percent=18.0, quantity=65, min_stock=10, max_stock=200, unit='pkt', status='Active'),

                # Staples & Grains
                Product(name='Aashirvaad Shudh Chakki Atta 5kg', sku='STP-001', barcode='890105899001', category_id=c5.id, supplier_id=sup.id, brand='Aashirvaad', purchase_price=210.0, selling_price=245.0, tax_percent=0.0, quantity=40, min_stock=10, max_stock=150, unit='pkt', status='Active'),
                Product(name='Fortune Sunlite Sunflower Oil 1L', sku='STP-002', barcode='890600728002', category_id=c5.id, supplier_id=sup.id, brand='Fortune', purchase_price=125.0, selling_price=145.0, tax_percent=5.0, quantity=50, min_stock=12, max_stock=200, unit='l', status='Active'),
                Product(name='Tata Vacuum Evaporated Salt 1kg', sku='STP-003', barcode='890105877003', category_id=c5.id, supplier_id=sup.id, brand='Tata', purchase_price=22.0, selling_price=28.0, tax_percent=0.0, quantity=110, min_stock=25, max_stock=400, unit='pkt', status='Active'),

                # Fruits & Vegetables
                Product(name='Fresh Organic Bananas (1 Dozen)', sku='FVT-001', barcode='890000001001', category_id=c4.id, supplier_id=sup.id, brand='FarmFresh', purchase_price=40.0, selling_price=55.0, tax_percent=0.0, quantity=35, min_stock=5, max_stock=80, unit='pcs', status='Active'),
                Product(name='Fresh Shimla Royal Apples 1kg', sku='FVT-002', barcode='890000001002', category_id=c4.id, supplier_id=sup.id, brand='FarmFresh', purchase_price=130.0, selling_price=170.0, tax_percent=0.0, quantity=20, min_stock=5, max_stock=60, unit='kg', status='Active'),

                # Cleaning & Care
                Product(name='Dettol Original Liquid Handwash 250ml', sku='CARE-001', barcode='890139600001', category_id=c6.id, supplier_id=sup.id, brand='Dettol', purchase_price=85.0, selling_price=99.0, tax_percent=18.0, quantity=30, min_stock=6, max_stock=100, unit='pcs', status='Active'),
                Product(name='Surf Excel Easy Wash Powder 1kg', sku='CARE-002', barcode='890103077002', category_id=c6.id, supplier_id=sup.id, brand='Surf Excel', purchase_price=120.0, selling_price=140.0, tax_percent=18.0, quantity=45, min_stock=10, max_stock=150, unit='pkt', status='Active'),
            ]
            for item in seed_items:
                if not Product.query.filter_by(sku=item.sku).first():
                    db.session.add(item)

        # Seed Default Walk-in Customer
        if Customer.query.count() == 0:
            cust = Customer(name='Walk-in Customer', phone='0000000000', email='walkin@grocery.com', address='Counter Checkout', total_purchases=0.0, outstanding_amount=0.0, status='Active')
            db.session.add(cust)

        db.session.commit()
        print("Database schema verified and default seed data loaded cleanly.")

if __name__ == '__main__':
    init_seed_data()
    print("Launching Smart Grocery Inventory & Billing System v2 server on http://127.0.0.1:5000 ...")
    app.run(host='0.0.0.0', port=5000, debug=True)
