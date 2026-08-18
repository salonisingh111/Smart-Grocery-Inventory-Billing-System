import os
from app import create_app
from app.database import db
from app.models import Category, Supplier, Product

def seed_7_products_per_category():
    # Ensure Categories exist
    cat_map = {}
    categories_data = [
        ('Dairy & Bakery', 'CAT-DAIRY', 'Fresh milk, butter, cheese and baked goods'),
        ('Beverages & Drinks', 'CAT-BEV', 'Soft drinks, juices, tea and coffee'),
        ('Snacks & Packaged Food', 'CAT-SNK', 'Chips, biscuits, instant noodles and snacks'),
        ('Fruits & Vegetables', 'CAT-FVT', 'Fresh organic fruits and vegetables'),
        ('Staples & Grains', 'CAT-STP', 'Flour, rice, pulse, oil and spices'),
        ('Cleaning & Care', 'CAT-CARE', 'Soaps, detergents, shampoos and household care')
    ]

    for name, code, desc in categories_data:
        cat = Category.query.filter_by(code=code).first()
        if not cat:
            cat = Category(name=name, code=code, description=desc, status='Active')
            db.session.add(cat)
            db.session.flush()
        cat_map[code] = cat.id

    db.session.commit()

    # Ensure Default Supplier exists
    sup = Supplier.query.first()
    if not sup:
        sup = Supplier(name='Global Grocery Wholesalers', phone='+91 91234 56789', email='supply@grocery.com', status='Active')
        db.session.add(sup)
        db.session.flush()
        db.session.commit()

    sup_id = sup.id

    # List of at least 7 products per category (Total 42)
    products_master = [
        # 1. Dairy & Bakery
        {'name': 'Amul Taaza Toned Milk 1L', 'sku': 'MILK-001', 'barcode': '890126201001', 'code': 'CAT-DAIRY', 'brand': 'Amul', 'purchase': 60.0, 'selling': 66.0, 'tax': 0.0, 'qty': 50, 'unit': 'l'},
        {'name': 'Britannia Brown Bread 400g', 'sku': 'BRD-001', 'barcode': '890105800001', 'code': 'CAT-DAIRY', 'brand': 'Britannia', 'purchase': 35.0, 'selling': 40.0, 'tax': 0.0, 'qty': 30, 'unit': 'pkt'},
        {'name': 'Amul Pasteurised Butter 500g', 'sku': 'BTR-001', 'barcode': '890126202002', 'code': 'CAT-DAIRY', 'brand': 'Amul', 'purchase': 240.0, 'selling': 275.0, 'tax': 5.0, 'qty': 25, 'unit': 'pcs'},
        {'name': 'Amul Fresh Paneer 200g', 'sku': 'DAIRY-004', 'barcode': '890126203003', 'code': 'CAT-DAIRY', 'brand': 'Amul', 'purchase': 80.0, 'selling': 95.0, 'tax': 0.0, 'qty': 20, 'unit': 'pkt'},
        {'name': 'Mother Dairy Fresh Dahi 400g', 'sku': 'DAIRY-005', 'barcode': '890126204004', 'code': 'CAT-DAIRY', 'brand': 'Mother Dairy', 'purchase': 40.0, 'selling': 50.0, 'tax': 0.0, 'qty': 35, 'unit': 'pcs'},
        {'name': 'Nestlé Milkmaid Condensed Milk 400g', 'sku': 'DAIRY-006', 'barcode': '890105805005', 'code': 'CAT-DAIRY', 'brand': 'Nestle', 'purchase': 125.0, 'selling': 145.0, 'tax': 5.0, 'qty': 15, 'unit': 'pcs'},
        {'name': 'Britannia Cheese Slices 200g', 'sku': 'DAIRY-007', 'barcode': '890105806006', 'code': 'CAT-DAIRY', 'brand': 'Britannia', 'purchase': 110.0, 'selling': 130.0, 'tax': 5.0, 'qty': 18, 'unit': 'pkt'},

        # 2. Beverages & Drinks
        {'name': 'Coca-Cola 750ml Bottle', 'sku': 'BEV-001', 'barcode': '5449000000996', 'code': 'CAT-BEV', 'brand': 'Coca-Cola', 'purchase': 35.0, 'selling': 40.0, 'tax': 18.0, 'qty': 80, 'unit': 'pcs'},
        {'name': 'Brooke Bond Red Label Tea 500g', 'sku': 'BEV-002', 'barcode': '890103001002', 'code': 'CAT-BEV', 'brand': 'Red Label', 'purchase': 260.0, 'selling': 310.0, 'tax': 5.0, 'qty': 30, 'unit': 'pkt'},
        {'name': 'Nescafe Classic Coffee Jar 100g', 'sku': 'BEV-003', 'barcode': '890105802003', 'code': 'CAT-BEV', 'brand': 'Nescafe', 'purchase': 290.0, 'selling': 340.0, 'tax': 12.0, 'qty': 22, 'unit': 'pcs'},
        {'name': 'Tropicana 100% Orange Juice 1L', 'sku': 'BEV-004', 'barcode': '890208000004', 'code': 'CAT-BEV', 'brand': 'Tropicana', 'purchase': 110.0, 'selling': 135.0, 'tax': 12.0, 'qty': 24, 'unit': 'pcs'},
        {'name': 'Sprite Soft Drink 750ml', 'sku': 'BEV-005', 'barcode': '5449000000885', 'code': 'CAT-BEV', 'brand': 'Sprite', 'purchase': 35.0, 'selling': 40.0, 'tax': 18.0, 'qty': 60, 'unit': 'pcs'},
        {'name': 'Real Fruit Power Mango Juice 1L', 'sku': 'BEV-006', 'barcode': '890120700006', 'code': 'CAT-BEV', 'brand': 'Real', 'purchase': 105.0, 'selling': 130.0, 'tax': 12.0, 'qty': 28, 'unit': 'pcs'},
        {'name': 'Bournvita Chocolate Health Drink 500g', 'sku': 'BEV-007', 'barcode': '890123300007', 'code': 'CAT-BEV', 'brand': 'Cadbury', 'purchase': 210.0, 'selling': 245.0, 'tax': 5.0, 'qty': 20, 'unit': 'pcs'},

        # 3. Snacks & Packaged Food
        {'name': "Lay's Classic Salted Potato Chips 50g", 'sku': 'SNK-001', 'barcode': '890149110001', 'code': 'CAT-SNK', 'brand': "Lay's", 'purchase': 16.0, 'selling': 20.0, 'tax': 12.0, 'qty': 120, 'unit': 'pkt'},
        {'name': 'Maggi 2-Minute Masala Noodles 280g', 'sku': 'SNK-002', 'barcode': '890105886002', 'code': 'CAT-SNK', 'brand': 'Maggi', 'purchase': 42.0, 'selling': 48.0, 'tax': 5.0, 'qty': 90, 'unit': 'pkt'},
        {'name': 'Oreo Vanilla Cream Biscuits 120g', 'sku': 'SNK-003', 'barcode': '890126289003', 'code': 'CAT-SNK', 'brand': 'Oreo', 'purchase': 25.0, 'selling': 30.0, 'tax': 18.0, 'qty': 65, 'unit': 'pkt'},
        {'name': 'Kurkure Masala Munch 90g', 'sku': 'SNK-004', 'barcode': '890149120004', 'code': 'CAT-SNK', 'brand': 'Kurkure', 'purchase': 16.0, 'selling': 20.0, 'tax': 12.0, 'qty': 100, 'unit': 'pkt'},
        {'name': 'Parle-G Gold Biscuits 1kg', 'sku': 'SNK-005', 'barcode': '890103030005', 'code': 'CAT-SNK', 'brand': 'Parle', 'purchase': 110.0, 'selling': 130.0, 'tax': 5.0, 'qty': 40, 'unit': 'pkt'},
        {'name': "Haldiram's Nagpur Bhujia Sev 350g", 'sku': 'SNK-006', 'barcode': '890406320006', 'code': 'CAT-SNK', 'brand': "Haldiram's", 'purchase': 85.0, 'selling': 105.0, 'tax': 12.0, 'qty': 35, 'unit': 'pkt'},
        {'name': "Kellogg's Corn Flakes Honey Almond 300g", 'sku': 'SNK-007', 'barcode': '890108800007', 'code': 'CAT-SNK', 'brand': "Kellogg's", 'purchase': 165.0, 'selling': 195.0, 'tax': 5.0, 'qty': 22, 'unit': 'pkt'},

        # 4. Fruits & Vegetables
        {'name': 'Fresh Organic Bananas (1 Dozen)', 'sku': 'FVT-001', 'barcode': '890000001001', 'code': 'CAT-FVT', 'brand': 'FarmFresh', 'purchase': 40.0, 'selling': 55.0, 'tax': 0.0, 'qty': 35, 'unit': 'pcs'},
        {'name': 'Fresh Shimla Royal Apples 1kg', 'sku': 'FVT-002', 'barcode': '890000001002', 'code': 'CAT-FVT', 'brand': 'FarmFresh', 'purchase': 130.0, 'selling': 170.0, 'tax': 0.0, 'qty': 20, 'unit': 'kg'},
        {'name': 'Fresh Hybrid Tomatoes 1kg', 'sku': 'FVT-003', 'barcode': '890000001003', 'code': 'CAT-FVT', 'brand': 'FarmFresh', 'purchase': 25.0, 'selling': 35.0, 'tax': 0.0, 'qty': 50, 'unit': 'kg'},
        {'name': 'Fresh Farm Potatoes 1kg', 'sku': 'FVT-004', 'barcode': '890000001004', 'code': 'CAT-FVT', 'brand': 'FarmFresh', 'purchase': 20.0, 'selling': 30.0, 'tax': 0.0, 'qty': 60, 'unit': 'kg'},
        {'name': 'Fresh Red Onions 1kg', 'sku': 'FVT-005', 'barcode': '890000001005', 'code': 'CAT-FVT', 'brand': 'FarmFresh', 'purchase': 30.0, 'selling': 42.0, 'tax': 0.0, 'qty': 55, 'unit': 'kg'},
        {'name': 'Fresh Green Capsicum 500g', 'sku': 'FVT-006', 'barcode': '890000001006', 'code': 'CAT-FVT', 'brand': 'FarmFresh', 'purchase': 35.0, 'selling': 50.0, 'tax': 0.0, 'qty': 25, 'unit': 'pkt'},
        {'name': 'Fresh Sweet Alphonso Mangoes 1kg', 'sku': 'FVT-007', 'barcode': '890000001007', 'code': 'CAT-FVT', 'brand': 'FarmFresh', 'purchase': 220.0, 'selling': 280.0, 'tax': 0.0, 'qty': 15, 'unit': 'kg'},

        # 5. Staples & Grains
        {'name': 'Aashirvaad Shudh Chakki Atta 5kg', 'sku': 'STP-001', 'barcode': '890105899001', 'code': 'CAT-STP', 'brand': 'Aashirvaad', 'purchase': 210.0, 'selling': 245.0, 'tax': 0.0, 'qty': 40, 'unit': 'pkt'},
        {'name': 'Fortune Sunlite Sunflower Oil 1L', 'sku': 'STP-002', 'barcode': '890600728002', 'code': 'CAT-STP', 'brand': 'Fortune', 'purchase': 125.0, 'selling': 145.0, 'tax': 5.0, 'qty': 50, 'unit': 'l'},
        {'name': 'Tata Vacuum Evaporated Salt 1kg', 'sku': 'STP-003', 'barcode': '890105877003', 'code': 'CAT-STP', 'brand': 'Tata', 'purchase': 22.0, 'selling': 28.0, 'tax': 0.0, 'qty': 110, 'unit': 'pkt'},
        {'name': 'India Gate Basmati Rice Rozzana 5kg', 'sku': 'STP-004', 'barcode': '890105888004', 'code': 'CAT-STP', 'brand': 'India Gate', 'purchase': 380.0, 'selling': 450.0, 'tax': 0.0, 'qty': 30, 'unit': 'pkt'},
        {'name': 'Tata Sampann Toor / Arhar Dal 1kg', 'sku': 'STP-005', 'barcode': '890105899005', 'code': 'CAT-STP', 'brand': 'Tata Sampann', 'purchase': 140.0, 'selling': 165.0, 'tax': 0.0, 'qty': 40, 'unit': 'pkt'},
        {'name': 'Everest Garam Masala 100g', 'sku': 'STP-006', 'barcode': '890105877006', 'code': 'CAT-STP', 'brand': 'Everest', 'purchase': 68.0, 'selling': 82.0, 'tax': 5.0, 'qty': 45, 'unit': 'pcs'},
        {'name': 'Fortune Kachi Ghani Mustard Oil 1L', 'sku': 'STP-007', 'barcode': '890600728007', 'code': 'CAT-STP', 'brand': 'Fortune', 'purchase': 145.0, 'selling': 170.0, 'tax': 5.0, 'qty': 35, 'unit': 'l'},

        # 6. Cleaning & Care
        {'name': 'Dettol Original Liquid Handwash 250ml', 'sku': 'CARE-001', 'barcode': '890139600001', 'code': 'CAT-CARE', 'brand': 'Dettol', 'purchase': 85.0, 'selling': 99.0, 'tax': 18.0, 'qty': 30, 'unit': 'pcs'},
        {'name': 'Surf Excel Easy Wash Powder 1kg', 'sku': 'CARE-002', 'barcode': '890103077002', 'code': 'CAT-CARE', 'brand': 'Surf Excel', 'purchase': 120.0, 'selling': 140.0, 'tax': 18.0, 'qty': 45, 'unit': 'pkt'},
        {'name': 'Vim Dishwash Gel Lemon 500ml', 'sku': 'CARE-003', 'barcode': '890103088003', 'code': 'CAT-CARE', 'brand': 'Vim', 'purchase': 95.0, 'selling': 115.0, 'tax': 18.0, 'qty': 40, 'unit': 'pcs'},
        {'name': 'Harpic Power Plus Toilet Cleaner 500ml', 'sku': 'CARE-004', 'barcode': '890139611004', 'code': 'CAT-CARE', 'brand': 'Harpic', 'purchase': 80.0, 'selling': 96.0, 'tax': 18.0, 'qty': 35, 'unit': 'pcs'},
        {'name': 'Lizol Disinfectant Surface Cleaner 1L', 'sku': 'CARE-005', 'barcode': '890139622005', 'code': 'CAT-CARE', 'brand': 'Lizol', 'purchase': 180.0, 'selling': 215.0, 'tax': 18.0, 'qty': 25, 'unit': 'pcs'},
        {'name': 'Colgate Strong Teeth Toothpaste 200g', 'sku': 'CARE-006', 'barcode': '890131400006', 'code': 'CAT-CARE', 'brand': 'Colgate', 'purchase': 92.0, 'selling': 110.0, 'tax': 18.0, 'qty': 50, 'unit': 'pcs'},
        {'name': 'Dove Cream Beauty Bath Soap Bar 125g', 'sku': 'CARE-007', 'barcode': '890103099007', 'code': 'CAT-CARE', 'brand': 'Dove', 'purchase': 55.0, 'selling': 68.0, 'tax': 18.0, 'qty': 60, 'unit': 'pcs'},

        # --- Dedicated Demo Products for Stock Status Filters ---
        # Low Stock Demo (qty <= min_stock)
        {'name': 'Amul Fresh Cream 250ml', 'sku': 'DEMO-LOW-01', 'barcode': '890126299101', 'code': 'CAT-DAIRY', 'brand': 'Amul', 'purchase': 55.0, 'selling': 67.0, 'tax': 5.0, 'qty': 3, 'min_stock': 10, 'unit': 'pkt'},
        {'name': 'Tata Tea Gold Premium 250g', 'sku': 'DEMO-LOW-02', 'barcode': '890105899102', 'code': 'CAT-BEV', 'brand': 'Tata', 'purchase': 140.0, 'selling': 165.0, 'tax': 5.0, 'qty': 2, 'min_stock': 10, 'unit': 'pkt'},
        {'name': 'Epigamia Blueberry Greek Yogurt 85g', 'sku': 'DEMO-LOW-03', 'barcode': '890126299103', 'code': 'CAT-DAIRY', 'brand': 'Epigamia', 'purchase': 45.0, 'selling': 55.0, 'tax': 5.0, 'qty': 4, 'min_stock': 10, 'unit': 'pcs'},

        # Out of Stock Demo (qty = 0)
        {'name': 'Ferrero Rocher Chocolate Box 16 Pcs', 'sku': 'DEMO-OUT-01', 'barcode': '890126299201', 'code': 'CAT-SNK', 'brand': 'Ferrero', 'purchase': 450.0, 'selling': 540.0, 'tax': 18.0, 'qty': 0, 'min_stock': 5, 'unit': 'box'},
        {'name': 'Red Bull Energy Drink 250ml', 'sku': 'DEMO-OUT-02', 'barcode': '890126299202', 'code': 'CAT-BEV', 'brand': 'Red Bull', 'purchase': 100.0, 'selling': 125.0, 'tax': 18.0, 'qty': 0, 'min_stock': 10, 'unit': 'can'},
        {'name': 'Nivea Soft Refreshing Cream 200ml', 'sku': 'DEMO-OUT-03', 'barcode': '890126299203', 'code': 'CAT-CARE', 'brand': 'Nivea', 'purchase': 230.0, 'selling': 275.0, 'tax': 18.0, 'qty': 0, 'min_stock': 5, 'unit': 'pcs'},

        # Expired Demo (expiry_date < today)
        {'name': 'Fresh Organic Tofu Block 200g', 'sku': 'DEMO-EXP-01', 'barcode': '890126299301', 'code': 'CAT-DAIRY', 'brand': 'OrganicFresh', 'purchase': 60.0, 'selling': 75.0, 'tax': 0.0, 'qty': 8, 'min_stock': 5, 'unit': 'pkt', 'expired': True},
        {'name': 'Baskin Robbins Vanilla Pint 450ml', 'sku': 'DEMO-EXP-02', 'barcode': '890126299302', 'code': 'CAT-DAIRY', 'brand': 'Baskin Robbins', 'purchase': 220.0, 'selling': 270.0, 'tax': 5.0, 'qty': 5, 'min_stock': 5, 'unit': 'tub', 'expired': True},
        {'name': 'Farmfresh Organic Whole Milk 1L', 'sku': 'DEMO-EXP-03', 'barcode': '890126299303', 'code': 'CAT-DAIRY', 'brand': 'Farmfresh', 'purchase': 65.0, 'selling': 75.0, 'tax': 0.0, 'qty': 6, 'min_stock': 5, 'unit': 'l', 'expired': True},
    ]

    added_count = 0
    updated_count = 0

    from datetime import date

    for item in products_master:
        cat_id = cat_map.get(item['code'])
        if not cat_id:
            continue

        exp_date = date(2026, 7, 15) if item.get('expired') else None
        min_stk = item.get('min_stock', 10)

        existing = Product.query.filter_by(sku=item['sku']).first()
        if not existing:
            p = Product(
                name=item['name'],
                sku=item['sku'],
                barcode=item['barcode'],
                category_id=cat_id,
                supplier_id=sup_id,
                brand=item['brand'],
                purchase_price=item['purchase'],
                selling_price=item['selling'],
                tax_percent=item['tax'],
                quantity=item['qty'],
                min_stock=min_stk,
                max_stock=200,
                unit=item['unit'],
                expiry_date=exp_date,
                status='Active'
            )
            db.session.add(p)
            added_count += 1
        else:
            existing.category_id = cat_id
            existing.name = item['name']
            existing.brand = item['brand']
            existing.purchase_price = item['purchase']
            existing.selling_price = item['selling']
            existing.tax_percent = item['tax']
            existing.quantity = item['qty']
            existing.min_stock = min_stk
            existing.expiry_date = exp_date
            existing.unit = item['unit']
            existing.status = 'Active'
            updated_count += 1

    db.session.commit()
    print(f"Successfully seeded! Added {added_count} new products, updated {updated_count} existing products.")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_7_products_per_category()


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_7_products_per_category()

