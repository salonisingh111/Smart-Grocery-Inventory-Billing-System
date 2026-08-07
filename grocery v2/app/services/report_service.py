import csv
import io
from datetime import datetime
from app.models.bill import Bill, BillItem
from app.models.product import Product
from app.models.customer import Customer
from app.models.supplier import Supplier

class ReportService:
    @staticmethod
    def generate_sales_csv(start_date: str = None, end_date: str = None) -> str:
        query = Bill.query.filter(Bill.status == 'Paid')
        if start_date:
            query = query.filter(Bill.created_at >= datetime.strptime(start_date, '%Y-%m-%d'))
        if end_date:
            query = query.filter(Bill.created_at <= datetime.strptime(end_date + ' 23:59:59', '%Y-%m-%d %H:%M:%S'))

        bills = query.order_by(Bill.created_at.desc()).all()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Bill Number', 'Date', 'Customer', 'Items Count', 'Subtotal', 'Tax', 'Discount', 'Net Amount', 'Payment Method', 'Biller'])

        for b in bills:
            writer.writerow([
                b.bill_number,
                b.created_at.strftime('%Y-%m-%d %H:%M'),
                b.customer.name if b.customer else 'Walk-in Customer',
                len(b.items),
                f"{b.total_amount:.2f}",
                f"{b.tax_amount:.2f}",
                f"{b.discount_amount:.2f}",
                f"{b.net_amount:.2f}",
                b.payment_method,
                b.user.full_name if b.user else ''
            ])

        return output.getvalue()

    @staticmethod
    def generate_inventory_csv() -> str:
        products = Product.query.order_by(Product.name).all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['SKU', 'Product Name', 'Category', 'Supplier', 'Quantity', 'Min Stock', 'Purchase Price', 'Selling Price', 'Stock Value', 'Status'])

        for p in products:
            writer.writerow([
                p.sku,
                p.name,
                p.category.name if p.category else '',
                p.supplier.name if p.supplier else '',
                p.quantity,
                p.min_stock,
                f"{p.purchase_price:.2f}",
                f"{p.selling_price:.2f}",
                f"{(p.quantity * p.purchase_price):.2f}",
                p.status
            ])

        return output.getvalue()
