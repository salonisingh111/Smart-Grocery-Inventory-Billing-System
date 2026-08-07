from datetime import datetime
from app.database import db
from app.models.bill import Bill, BillItem
from app.models.product import Product
from app.models.customer import Customer
from app.models.inventory import InventoryHistory
from app.models.setting import SystemSetting

class BillingService:
    @staticmethod
    def generate_bill_number() -> str:
        prefix = SystemSetting.get('INVOICE_PREFIX', 'INV')
        today_str = datetime.utcnow().strftime('%Y%m%d')
        last_bill = Bill.query.filter(Bill.bill_number.like(f"{prefix}-{today_str}-%")).order_by(Bill.id.desc()).first()
        
        if last_bill:
            try:
                seq = int(last_bill.bill_number.split('-')[-1]) + 1
            except ValueError:
                seq = 1
        else:
            seq = 1

        return f"{prefix}-{today_str}-{seq:04d}"

    @classmethod
    def create_checkout_bill(cls, customer_id: int, items_data: list, payment_method: str, discount_amount: float, notes: str, user_id: int) -> tuple[bool, str, Bill]:
        if not items_data:
            return False, "Cart is empty.", None

        bill_number = cls.generate_bill_number()
        total_subtotal = 0.0
        total_tax = 0.0

        bill_items_to_create = []

        for item in items_data:
            product_id = item.get('product_id')
            qty = int(item.get('quantity', 1))

            if qty <= 0:
                return False, f"Invalid quantity for item ID {product_id}.", None

            product = Product.query.get(product_id)
            if not product:
                return False, f"Product ID {product_id} not found.", None

            if product.quantity < qty:
                return False, f"Insufficient stock for '{product.name}'. Available: {product.quantity}, Requested: {qty}", None

            enable_tax = SystemSetting.get_bool('ENABLE_TAX', True)
            unit_price = product.selling_price
            item_subtotal = unit_price * qty
            tax_rate = (product.tax_percent or 0.0) if enable_tax else 0.0
            item_tax = (item_subtotal * tax_rate) / 100.0
            item_total = item_subtotal + item_tax

            total_subtotal += item_subtotal
            total_tax += item_tax

            bill_items_to_create.append({
                'product': product,
                'product_name': product.name,
                'unit_price': unit_price,
                'quantity': qty,
                'tax_percent': tax_rate,
                'tax_amount': item_tax,
                'total_price': item_total
            })

        enable_discount = SystemSetting.get_bool('ENABLE_DISCOUNT', True)
        applied_discount = discount_amount if enable_discount else 0.0
        gross_amount = total_subtotal + total_tax
        final_gross = max(0.0, gross_amount - applied_discount)
        rounded_net = round(final_gross)
        round_off = round(rounded_net - final_gross, 2)

        new_bill = Bill(
            bill_number=bill_number,
            customer_id=customer_id if customer_id else None,
            user_id=user_id,
            total_amount=round(total_subtotal, 2),
            tax_amount=round(total_tax, 2),
            discount_amount=round(discount_amount, 2),
            round_off=round_off,
            net_amount=rounded_net,
            payment_method=payment_method,
            status='Paid',
            notes=notes
        )

        db.session.add(new_bill)
        db.session.flush()  # get bill ID

        for b_item in bill_items_to_create:
            prod = b_item['product']
            # Deduct stock
            prod.quantity -= b_item['quantity']

            # Record Inventory History
            inv_log = InventoryHistory(
                product_id=prod.id,
                change_type='Sale',
                quantity_changed=-b_item['quantity'],
                remaining_quantity=prod.quantity,
                reason=f"POS Bill #{bill_number}",
                performed_by_user_id=user_id
            )
            db.session.add(inv_log)

            bill_item = BillItem(
                bill_id=new_bill.id,
                product_id=prod.id,
                product_name=b_item['product_name'],
                unit_price=b_item['unit_price'],
                quantity=b_item['quantity'],
                tax_percent=b_item['tax_percent'],
                tax_amount=b_item['tax_amount'],
                total_price=b_item['total_price']
            )
            db.session.add(bill_item)

        # Update customer purchases if associated
        if customer_id:
            customer = Customer.query.get(customer_id)
            if customer:
                customer.total_purchases = (customer.total_purchases or 0.0) + rounded_net

        db.session.commit()
        return True, "Bill generated successfully.", new_bill
