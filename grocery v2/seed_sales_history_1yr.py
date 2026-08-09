import os
import random
from datetime import datetime, timedelta
from app import create_app
from app.database import db
from app.models.product import Product
from app.models.user import User
from app.models.bill import Bill, BillItem
from app.models.setting import SystemSetting

app = create_app()

with app.app_context():
    print("Starting 1-Year Sales History Data Generator...")

    # 1. Fetch active products
    products = Product.query.filter_by(status='Active').all()
    if not products:
        print("No active products found! Running seed_products_7_each first...")
        from seed_products_7_each import seed_7_products_per_category
        seed_7_products_per_category()
        products = Product.query.filter_by(status='Active').all()

    print(f"Loaded {len(products)} active products for sales history generation.")

    # 2. Fetch default admin or first user
    user = User.query.first()
    if not user:
        print("No user found! Creating default admin user...")
        user = User(username='admin', full_name='System Admin', role='Admin')
        user.set_password('admin123')
        db.session.add(user)
        db.session.commit()

    # 3. Generate past 365 days of sales data
    today = datetime.now()
    start_date = today - timedelta(days=365)

    prefix = SystemSetting.get('INVOICE_PREFIX', 'INV')
    start_inv_num = 1001

    created_bills_count = 0
    created_items_count = 0

    payment_methods = ['Cash', 'UPI', 'Card']
    weights = [0.50, 0.35, 0.15]

    current_date = start_date
    bill_seq = start_inv_num

    # Batch commit every 500 bills for performance
    batch_count = 0

    while current_date <= today:
        is_weekend = current_date.weekday() in [5, 6]
        bills_today = random.randint(3, 7) if is_weekend else random.randint(2, 5)

        for _ in range(bills_today):
            hour = random.randint(8, 20)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            bill_time = current_date.replace(hour=hour, minute=minute, second=second)

            sample_size = min(len(products), random.randint(1, 4))
            chosen_products = random.sample(products, sample_size)

            total_amount = 0.0
            tax_amount = 0.0
            bill_items = []

            for p in chosen_products:
                qty = random.randint(1, 3)
                price = float(p.selling_price) if p.selling_price else 10.0
                item_total = price * qty
                p_tax = float(p.tax_rate) if hasattr(p, 'tax_rate') and p.tax_rate else 5.0
                item_tax = item_total * p_tax / 100.0

                total_amount += item_total
                tax_amount += item_tax

                b_item = BillItem(
                    product_id=p.id,
                    product_name=p.name,
                    unit_price=price,
                    quantity=qty,
                    returned_quantity=0,
                    tax_percent=p_tax,
                    tax_amount=round(item_tax, 2),
                    total_price=round(item_total, 2)
                )
                bill_items.append(b_item)
                created_items_count += 1

            discount = round(total_amount * 0.05, 2) if random.random() < 0.10 else 0.0
            net_amount = round(total_amount + tax_amount - discount, 2)
            round_off = 0.0
            pay_method = random.choices(payment_methods, weights=weights)[0]

            bill_no = f"{prefix}-{bill_seq:05d}"
            bill_seq += 1

            bill = Bill(
                bill_number=bill_no,
                customer_id=None,
                user_id=user.id,
                total_amount=round(total_amount, 2),
                tax_amount=round(tax_amount, 2),
                discount_amount=discount,
                round_off=round_off,
                net_amount=net_amount,
                payment_method=pay_method,
                status='Paid',
                created_at=bill_time
            )
            bill.items = bill_items
            db.session.add(bill)
            created_bills_count += 1
            batch_count += 1

            if batch_count >= 200:
                db.session.commit()
                batch_count = 0

        current_date += timedelta(days=1)

    SystemSetting.set('NEXT_INVOICE_NUMBER', str(bill_seq))
    db.session.commit()

    print(f"SUCCESS: Generated {created_bills_count} historical bills with {created_items_count} bill items across the past 365 days!")
