import os
import sys
import random
from datetime import datetime, timedelta

# Ensure script directory is in sys.path for reliable module resolution
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from app import create_app
from app.database import db
from app.models.product import Product
from app.models.user import User
from app.models.bill import Bill, BillItem
from app.models.setting import SystemSetting


def seed_1yr_sales_history():
    print("Starting 1-Year Sales History Data Generator...")

    # 1. Fetch active products
    products = Product.query.filter_by(status='Active').all()
    if not products:
        print("No active products found! Running seed_products_7_each first...")
        from seed_products_7_each import seed_7_products_per_category
        seed_7_products_per_category()
        products = Product.query.filter_by(status='Active').all()

    if not products:
        print("ERROR: Still no active products available after seeding attempt.")
        return

    print(f"Loaded {len(products)} active products for sales history generation.")

    # 2. Fetch default admin or first user
    user = User.query.first()
    if not user:
        print("No user found! Creating default admin user...")
        user = User(
            username='admin',
            email='admin@grocery.com',
            full_name='System Admin',
            role='Admin',
            status='Active'
        )
        user.set_password('admin123')
        db.session.add(user)
        db.session.commit()

    # 3. Generate past 365 days of sales data
    today = datetime.now()
    start_date = today - timedelta(days=365)

    prefix = SystemSetting.get('INVOICE_PREFIX', 'INV')
    
    # Calculate starting invoice sequence from existing maximum bill sequence to avoid collisions
    existing_bills = db.session.query(Bill.bill_number).all()
    max_seq = 1000
    for (b_num,) in existing_bills:
        if b_num and '-' in b_num:
            parts = b_num.split('-')
            if parts[-1].isdigit():
                max_seq = max(max_seq, int(parts[-1]))
    max_bill_id = db.session.query(db.func.max(Bill.id)).scalar() or 0
    start_inv_num = max(max_seq + 1, 1001 + max_bill_id)

    created_bills_count = 0
    created_items_count = 0

    payment_methods = ['Cash', 'UPI', 'Card']
    weights = [0.50, 0.35, 0.15]

    current_date = start_date
    bill_seq = start_inv_num

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
                p_tax = float(p.tax_percent) if hasattr(p, 'tax_percent') and p.tax_percent is not None else 5.0
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
            gross_amount = max(0.0, total_amount + tax_amount - discount)
            net_amount = float(round(gross_amount))
            round_off = round(net_amount - gross_amount, 2)
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

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_1yr_sales_history()

