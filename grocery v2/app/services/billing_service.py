from datetime import datetime, timedelta
from sqlalchemy import func
from app.database import db
from app.models.bill import Bill, BillItem, BillReturn, BillReturnItem
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

    @staticmethod
    def generate_return_number() -> str:
        today_str = datetime.utcnow().strftime('%Y%m%d')
        last_ret = BillReturn.query.filter(BillReturn.return_number.like(f"RET-{today_str}-%")).order_by(BillReturn.id.desc()).first()
        if last_ret:
            try:
                seq = int(last_ret.return_number.split('-')[-1]) + 1
            except ValueError:
                seq = 1
        else:
            seq = 1
        return f"RET-{today_str}-{seq:04d}"

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
        db.session.flush()

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

        if customer_id:
            customer = Customer.query.get(customer_id)
            if customer:
                customer.total_purchases = (customer.total_purchases or 0.0) + rounded_net

        db.session.commit()
        return True, "Bill generated successfully.", new_bill

    @classmethod
    def get_billing_dashboard_stats(cls) -> dict:
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Today's Bills
        today_bills_query = Bill.query.filter(Bill.created_at >= today_start, Bill.status != 'Cancelled')
        today_bills = today_bills_query.all()
        
        today_total_sales = sum(b.net_amount for b in today_bills)
        today_bill_count = len(today_bills)
        today_items_sold = sum(sum(item.quantity for item in b.items) for b in today_bills)
        avg_bill_value = (today_total_sales / today_bill_count) if today_bill_count > 0 else 0.0
        today_discounts = sum(b.discount_amount for b in today_bills)
        today_tax = sum(b.tax_amount for b in today_bills)

        # Sales by Payment Method
        cash_sales = sum(b.net_amount for b in today_bills if b.payment_method == 'Cash')
        upi_sales = sum(b.net_amount for b in today_bills if b.payment_method == 'UPI')
        card_sales = sum(b.net_amount for b in today_bills if b.payment_method == 'Card')

        # Top Selling Products (Overall)
        top_products_query = db.session.query(
            BillItem.product_name,
            func.sum(BillItem.quantity).label('total_qty'),
            func.sum(BillItem.total_price).label('total_revenue')
        ).group_by(BillItem.product_name).order_by(db.desc('total_qty')).limit(5).all()

        top_products = [
            {'name': row[0], 'quantity': row[1], 'revenue': round(row[2] or 0.0, 2)}
            for row in top_products_query
        ]

        # Recent Bills
        recent_bills = Bill.query.order_by(Bill.created_at.desc()).limit(8).all()

        # 7-day Sales Trend Chart Data
        chart_labels = []
        chart_values = []
        for i in range(6, -1, -1):
            day_date = (datetime.utcnow() - timedelta(days=i)).date()
            d_start = datetime.combine(day_date, datetime.min.time())
            d_end = datetime.combine(day_date, datetime.max.time())
            
            day_sum = db.session.query(func.sum(Bill.net_amount)).filter(
                Bill.created_at >= d_start,
                Bill.created_at <= d_end,
                Bill.status != 'Cancelled'
            ).scalar() or 0.0
            
            chart_labels.append(day_date.strftime('%b %d'))
            chart_values.append(round(float(day_sum), 2))

        return {
            'today_total_sales': round(today_total_sales, 2),
            'today_bill_count': today_bill_count,
            'today_items_sold': today_items_sold,
            'avg_bill_value': round(avg_bill_value, 2),
            'today_discounts': round(today_discounts, 2),
            'today_tax': round(today_tax, 2),
            'payment_split': {
                'Cash': round(cash_sales, 2),
                'UPI': round(upi_sales, 2),
                'Card': round(card_sales, 2)
            },
            'top_products': top_products,
            'recent_bills': recent_bills,
            'chart': {
                'labels': chart_labels,
                'amounts': chart_values
            }
        }

    @classmethod
    def process_return(cls, bill_id: int, items_data: list, refund_method: str, reason: str, user_id: int) -> tuple[bool, str, BillReturn]:
        bill = Bill.query.get(bill_id)
        if not bill:
            return False, "Original Bill not found.", None

        if bill.status == 'Cancelled':
            return False, "Cannot process return for a cancelled bill.", None

        if not items_data:
            return False, "No items selected for return.", None

        return_number = cls.generate_return_number()
        total_refund_amount = 0.0
        return_items_to_create = []

        for item in items_data:
            bill_item_id = item.get('bill_item_id')
            return_qty = int(item.get('return_quantity', 0))

            if return_qty <= 0:
                continue

            bill_item = BillItem.query.get(bill_item_id)
            if not bill_item or bill_item.bill_id != bill.id:
                return False, f"Invalid bill item reference ID {bill_item_id}.", None

            already_returned = bill_item.returned_quantity or 0
            max_allowed = bill_item.quantity - already_returned

            if return_qty > max_allowed:
                return False, f"Return quantity {return_qty} exceeds maximum returnable limit of {max_allowed} for '{bill_item.product_name}'.", None

            unit_refund = bill_item.unit_price + (bill_item.tax_amount / bill_item.quantity if bill_item.quantity else 0.0)
            item_refund = unit_refund * return_qty
            total_refund_amount += item_refund

            return_items_to_create.append({
                'bill_item': bill_item,
                'return_qty': return_qty,
                'unit_price': bill_item.unit_price,
                'refund_amount': item_refund
            })

        if not return_items_to_create:
            return False, "No valid items selected for return.", None

        new_return = BillReturn(
            return_number=return_number,
            bill_id=bill.id,
            customer_id=bill.customer_id,
            user_id=user_id,
            total_refund=round(total_refund_amount, 2),
            refund_method=refund_method,
            reason=reason or 'Customer Product Return'
        )

        db.session.add(new_return)
        db.session.flush()

        for r_item in return_items_to_create:
            b_item = r_item['bill_item']
            ret_qty = r_item['return_qty']

            # 1. Update BillItem returned_quantity
            b_item.returned_quantity = (b_item.returned_quantity or 0) + ret_qty

            # 2. Increase returned product quantity back into inventory
            product = Product.query.get(b_item.product_id)
            if product:
                product.quantity += ret_qty
                # 3. Create inventory history entry
                inv_log = InventoryHistory(
                    product_id=product.id,
                    change_type='Return',
                    quantity_changed=ret_qty,
                    remaining_quantity=product.quantity,
                    reason=f"Return for Bill #{bill.bill_number} (Ref: {return_number})",
                    performed_by_user_id=user_id
                )
                db.session.add(inv_log)

            # Create BillReturnItem
            return_item_rec = BillReturnItem(
                return_id=new_return.id,
                bill_item_id=b_item.id,
                product_id=b_item.product_id,
                product_name=b_item.product_name,
                quantity=ret_qty,
                unit_price=b_item.unit_price,
                refund_amount=round(r_item['refund_amount'], 2)
            )
            db.session.add(return_item_rec)

        # Update overall Bill Status
        all_items_fully_returned = all(
            (bi.returned_quantity or 0) >= bi.quantity for bi in bill.items
        )
        if all_items_fully_returned:
            bill.status = 'Returned'
        else:
            bill.status = 'Partially Returned'

        db.session.commit()
        return True, f"Return processed successfully. Refund Total: {SystemSetting.get('CURRENCY', '₹')}{round(total_refund_amount, 2)}", new_return
