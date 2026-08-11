import csv
import io
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, List, Optional
from app.database import db
from app.models.bill import Bill, BillItem, BillReturn
from app.models.product import Product
from app.models.category import Category
from app.models.customer import Customer
from app.models.supplier import Supplier

class ReportService:

    @staticmethod
    def parse_date_range(
        range_preset: Optional[str] = 'this_month',
        start_date_str: Optional[str] = None,
        end_date_str: Optional[str] = None
    ) -> Tuple[Optional[datetime], Optional[datetime], str]:
        """
        Parses date range options into (start_datetime, end_datetime, display_label).
        """
        now = datetime.utcnow()
        today_date = now.date()

        if range_preset == 'today':
            start_dt = datetime.combine(today_date, datetime.min.time())
            end_dt = datetime.combine(today_date, datetime.max.time())
            label = "Today"
        elif range_preset == 'this_week':
            start_week = today_date - timedelta(days=today_date.weekday())
            start_dt = datetime.combine(start_week, datetime.min.time())
            end_dt = datetime.combine(today_date, datetime.max.time())
            label = "This Week"
        elif range_preset == 'this_month':
            start_month = today_date.replace(day=1)
            start_dt = datetime.combine(start_month, datetime.min.time())
            end_dt = datetime.combine(today_date, datetime.max.time())
            label = "This Month"
        elif range_preset == 'last_month':
            first_this_month = today_date.replace(day=1)
            last_month_end = first_this_month - timedelta(days=1)
            first_last_month = last_month_end.replace(day=1)
            start_dt = datetime.combine(first_last_month, datetime.min.time())
            end_dt = datetime.combine(last_month_end, datetime.max.time())
            label = "Last Month"
        elif range_preset == 'custom' and start_date_str and end_date_str:
            try:
                s_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                e_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                start_dt = datetime.combine(s_date, datetime.min.time())
                end_dt = datetime.combine(e_date, datetime.max.time())
                label = f"{start_date_str} to {end_date_str}"
            except ValueError:
                # Fallback if invalid date string
                start_month = today_date.replace(day=1)
                start_dt = datetime.combine(start_month, datetime.min.time())
                end_dt = datetime.combine(today_date, datetime.max.time())
                label = "This Month"
        elif range_preset == 'all':
            start_dt = None
            end_dt = None
            label = "All Time"
        else:
            # Default to this month
            start_month = today_date.replace(day=1)
            start_dt = datetime.combine(start_month, datetime.min.time())
            end_dt = datetime.combine(today_date, datetime.max.time())
            label = "This Month"

        return start_dt, end_dt, label

    # -------------------------------------------------------------------------
    # 1. OVERVIEW ANALYTICS
    # -------------------------------------------------------------------------
    @staticmethod
    def get_overview_analytics(
        range_preset: str = 'this_month',
        start_date: str = None,
        end_date: str = None
    ) -> Dict[str, Any]:
        start_dt, end_dt, label = ReportService.parse_date_range(range_preset, start_date, end_date)

        bill_query = Bill.query.filter(Bill.status == 'Paid')
        return_query = BillReturn.query.filter(BillReturn.status == 'Completed')

        if start_dt and end_dt:
            bill_query = bill_query.filter(Bill.created_at >= start_dt, Bill.created_at <= end_dt)
            return_query = return_query.filter(BillReturn.created_at >= start_dt, BillReturn.created_at <= end_dt)

        bills = bill_query.all()
        returns = return_query.all()

        total_revenue = sum(b.net_amount for b in bills)
        total_refunds = sum(r.total_refund for r in returns)
        net_sales = max(0.0, total_revenue - total_refunds)

        total_bills = len(bills)
        total_discounts = sum(b.discount_amount for b in bills)
        total_tax = sum(b.tax_amount for b in bills)

        # Calculate COGS & Items Sold from BillItems
        bill_ids = [b.id for b in bills]
        items_sold = 0
        cogs = 0.0

        if bill_ids:
            bill_items = BillItem.query.filter(BillItem.bill_id.in_(bill_ids)).all()
            for bi in bill_items:
                effective_qty = max(0, bi.quantity - (bi.returned_quantity or 0))
                items_sold += effective_qty
                cost = (bi.product.purchase_price if bi.product and bi.product.purchase_price else 0.0)
                cogs += (effective_qty * cost)

        gross_profit = net_sales - cogs
        profit_margin = (gross_profit / net_sales * 100.0) if net_sales > 0 else 0.0

        # Build Chart Data: Daily Revenue & Cost Trend
        trend_labels = []
        trend_revenue = []
        trend_cost = []

        if start_dt and end_dt:
            curr = start_dt.date()
            stop = end_dt.date()
            delta_days = (stop - curr).days
            if delta_days <= 60:
                while curr <= stop:
                    c_start = datetime.combine(curr, datetime.min.time())
                    c_end = datetime.combine(curr, datetime.max.time())
                    day_bills = [b for b in bills if c_start <= b.created_at <= c_end]
                    day_returns = [r for r in returns if c_start <= r.created_at <= c_end]

                    day_rev = sum(b.net_amount for b in day_bills) - sum(r.total_refund for r in day_returns)
                    day_rev = max(0.0, day_rev)

                    d_bill_ids = [b.id for b in day_bills]
                    day_cost = 0.0
                    if d_bill_ids:
                        d_items = BillItem.query.filter(BillItem.bill_id.in_(d_bill_ids)).all()
                        for bi in d_items:
                            eqty = max(0, bi.quantity - (bi.returned_quantity or 0))
                            cost = (bi.product.purchase_price if bi.product and bi.product.purchase_price else 0.0)
                            day_cost += (eqty * cost)

                    trend_labels.append(curr.strftime('%b %d'))
                    trend_revenue.append(round(day_rev, 2))
                    trend_cost.append(round(day_cost, 2))
                    curr += timedelta(days=1)
            else:
                monthly_map = {}
                for b in bills:
                    m_key = b.created_at.strftime('%Y-%m')
                    monthly_map.setdefault(m_key, {'rev': 0.0, 'cost': 0.0})
                    monthly_map[m_key]['rev'] += b.net_amount

                for r in returns:
                    m_key = r.created_at.strftime('%Y-%m')
                    if m_key in monthly_map:
                        monthly_map[m_key]['rev'] -= r.total_refund

                if bill_ids:
                    all_bis = BillItem.query.filter(BillItem.bill_id.in_(bill_ids)).all()
                    for bi in all_bis:
                        m_key = bi.bill.created_at.strftime('%Y-%m')
                        if m_key in monthly_map:
                            eqty = max(0, bi.quantity - (bi.returned_quantity or 0))
                            cost = (bi.product.purchase_price if bi.product and bi.product.purchase_price else 0.0)
                            monthly_map[m_key]['cost'] += (eqty * cost)

                sorted_months = sorted(monthly_map.keys())
                for m in sorted_months:
                    try:
                        m_dt = datetime.strptime(m, '%Y-%m')
                        trend_labels.append(m_dt.strftime('%b %Y'))
                    except ValueError:
                        trend_labels.append(m)
                    trend_revenue.append(round(max(0.0, monthly_map[m]['rev']), 2))
                    trend_cost.append(round(monthly_map[m]['cost'], 2))

        # Sales by Category Breakdown
        cat_labels = []
        cat_values = []
        if bill_ids:
            all_bis = BillItem.query.filter(BillItem.bill_id.in_(bill_ids)).all()
            cat_totals: Dict[str, float] = {}
            for bi in all_bis:
                c_name = bi.product.category.name if (bi.product and bi.product.category) else 'Uncategorized'
                cat_totals[c_name] = cat_totals.get(c_name, 0.0) + bi.total_price

            for cname, val in sorted(cat_totals.items(), key=lambda x: x[1], reverse=True):
                cat_labels.append(cname)
                cat_values.append(round(val, 2))

        return {
            'date_label': label,
            'kpis': {
                'total_revenue': round(total_revenue, 2),
                'gross_profit': round(gross_profit, 2),
                'profit_margin': round(profit_margin, 2),
                'total_bills': total_bills,
                'items_sold': items_sold,
                'total_discounts': round(total_discounts, 2),
                'total_tax': round(total_tax, 2),
                'total_refunds': round(total_refunds, 2),
                'net_sales': round(net_sales, 2)
            },
            'charts': {
                'trend_labels': trend_labels,
                'trend_revenue': trend_revenue,
                'trend_cost': trend_cost,
                'cat_labels': cat_labels,
                'cat_values': cat_values
            }
        }

    # -------------------------------------------------------------------------
    # 2. SALES ANALYTICS
    # -------------------------------------------------------------------------
    @staticmethod
    def get_sales_analytics(
        range_preset: str = 'this_month',
        start_date: str = None,
        end_date: str = None,
        payment_method: str = None,
        category_id: int = None
    ) -> Dict[str, Any]:
        start_dt, end_dt, label = ReportService.parse_date_range(range_preset, start_date, end_date)

        query = Bill.query.filter(Bill.status == 'Paid')
        if start_dt and end_dt:
            query = query.filter(Bill.created_at >= start_dt, Bill.created_at <= end_dt)
        if payment_method:
            query = query.filter(Bill.payment_method == payment_method)

        bills = query.all()
        bill_ids = [b.id for b in bills]

        if category_id and bill_ids:
            cat_bill_ids = set(
                db.session.query(BillItem.bill_id)
                .join(Product, BillItem.product_id == Product.id)
                .filter(BillItem.bill_id.in_(bill_ids), Product.category_id == category_id)
                .all()
            )
            cat_bill_ids = {r[0] for r in cat_bill_ids}
            filtered_bills = [b for b in bills if b.id in cat_bill_ids]
        else:
            filtered_bills = bills

        f_bill_ids = [b.id for b in filtered_bills]

        total_sales = sum(b.net_amount for b in filtered_bills)
        num_bills = len(filtered_bills)
        avg_bill_value = (total_sales / num_bills) if num_bills > 0 else 0.0
        total_discounts = sum(b.discount_amount for b in filtered_bills)
        total_tax = sum(b.tax_amount for b in filtered_bills)

        items_sold = 0
        if f_bill_ids:
            items_query = BillItem.query.filter(BillItem.bill_id.in_(f_bill_ids))
            if category_id:
                items_query = items_query.join(Product, BillItem.product_id == Product.id).filter(Product.category_id == category_id)
            items_sold = sum(max(0, bi.quantity - (bi.returned_quantity or 0)) for bi in items_query.all())

        # Sales Growth vs previous period
        sales_growth = 0.0
        if start_dt and end_dt:
            duration = end_dt - start_dt
            prev_start = start_dt - duration
            prev_end = start_dt - timedelta(seconds=1)

            prev_bills = Bill.query.filter(
                Bill.status == 'Paid',
                Bill.created_at >= prev_start,
                Bill.created_at <= prev_end
            ).all()
            prev_sales = sum(b.net_amount for b in prev_bills)
            if prev_sales > 0:
                sales_growth = ((total_sales - prev_sales) / prev_sales) * 100.0

        # Payment Methods
        pay_methods: Dict[str, float] = {}
        for b in filtered_bills:
            pay_methods[b.payment_method] = pay_methods.get(b.payment_method, 0.0) + b.net_amount

        pay_labels = list(pay_methods.keys())
        pay_values = [round(v, 2) for v in pay_methods.values()]

        # Top categories & products
        cat_sales: Dict[str, float] = {}
        top_prods_map: Dict[str, Dict[str, Any]] = {}

        if f_bill_ids:
            bis = BillItem.query.filter(BillItem.bill_id.in_(f_bill_ids)).all()
            for bi in bis:
                if category_id and bi.product and bi.product.category_id != category_id:
                    continue
                c_name = bi.product.category.name if (bi.product and bi.product.category) else 'Uncategorized'
                cat_sales[c_name] = cat_sales.get(c_name, 0.0) + bi.total_price

                p_name = bi.product_name
                if p_name not in top_prods_map:
                    top_prods_map[p_name] = {'name': p_name, 'qty': 0, 'revenue': 0.0}
                top_prods_map[p_name]['qty'] += max(0, bi.quantity - (bi.returned_quantity or 0))
                top_prods_map[p_name]['revenue'] += bi.total_price

        sorted_top_prods = sorted(top_prods_map.values(), key=lambda x: x['revenue'], reverse=True)[:10]

        # Peak hours
        hourly_sales = [0.0] * 24
        for b in filtered_bills:
            if b.created_at:
                h = b.created_at.hour
                hourly_sales[h] += b.net_amount

        peak_hours = [
            {'hour': f"{h:02d}:00", 'sales': round(hourly_sales[h], 2)}
            for h in range(24)
        ]

        # Daily Trend
        trend_labels = []
        trend_sales = []
        if start_dt and end_dt:
            curr = start_dt.date()
            stop = end_dt.date()
            while curr <= stop:
                c_start = datetime.combine(curr, datetime.min.time())
                c_end = datetime.combine(curr, datetime.max.time())
                d_bills = [b for b in filtered_bills if c_start <= b.created_at <= c_end]
                trend_labels.append(curr.strftime('%b %d'))
                trend_sales.append(round(sum(b.net_amount for b in d_bills), 2))
                curr += timedelta(days=1)

        return {
            'date_label': label,
            'kpis': {
                'total_sales': round(total_sales, 2),
                'num_bills': num_bills,
                'items_sold': items_sold,
                'avg_bill_value': round(avg_bill_value, 2),
                'sales_growth': round(sales_growth, 2),
                'total_discounts': round(total_discounts, 2),
                'total_tax': round(total_tax, 2)
            },
            'charts': {
                'trend_labels': trend_labels,
                'trend_sales': trend_sales,
                'pay_labels': pay_labels,
                'pay_values': pay_values,
                'cat_labels': list(cat_sales.keys()),
                'cat_values': [round(v, 2) for v in cat_sales.values()],
                'top_products': sorted_top_prods,
                'peak_hours': peak_hours
            }
        }

    # -------------------------------------------------------------------------
    # 3. PRODUCTS ANALYTICS
    # -------------------------------------------------------------------------
    @staticmethod
    def get_product_analytics(
        range_preset: str = 'this_month',
        start_date: str = None,
        end_date: str = None,
        category_id: int = None,
        product_id: int = None
    ) -> Dict[str, Any]:
        start_dt, end_dt, label = ReportService.parse_date_range(range_preset, start_date, end_date)

        bill_query = Bill.query.filter(Bill.status == 'Paid')
        if start_dt and end_dt:
            bill_query = bill_query.filter(Bill.created_at >= start_dt, Bill.created_at <= end_dt)
        bills = bill_query.all()
        bill_ids = [b.id for b in bills]

        prod_query = Product.query
        if category_id:
            prod_query = prod_query.filter(Product.category_id == category_id)
        if product_id:
            prod_query = prod_query.filter(Product.id == product_id)
        products = prod_query.all()

        prod_stats = {}
        for p in products:
            prod_stats[p.id] = {
                'id': p.id,
                'name': p.name,
                'sku': p.sku,
                'category_name': p.category.name if p.category else 'Uncategorized',
                'purchase_price': p.purchase_price or 0.0,
                'selling_price': p.selling_price or 0.0,
                'units_sold': 0,
                'revenue': 0.0,
                'cogs': 0.0,
                'profit': 0.0,
                'margin_percent': 0.0
            }

        if bill_ids and products:
            target_pids = set(prod_stats.keys())
            bi_query = BillItem.query.filter(BillItem.bill_id.in_(bill_ids), BillItem.product_id.in_(target_pids))
            for bi in bi_query.all():
                pid = bi.product_id
                if pid in prod_stats:
                    eqty = max(0, bi.quantity - (bi.returned_quantity or 0))
                    rev = bi.total_price
                    cost = eqty * prod_stats[pid]['purchase_price']

                    prod_stats[pid]['units_sold'] += eqty
                    prod_stats[pid]['revenue'] += rev
                    prod_stats[pid]['cogs'] += cost

        table_rows = []
        total_revenue = 0.0
        total_cogs = 0.0
        total_units = 0

        for pid, stats in prod_stats.items():
            rev = stats['revenue']
            cogs = stats['cogs']
            profit = rev - cogs
            margin = (profit / rev * 100.0) if rev > 0 else 0.0

            stats['profit'] = round(profit, 2)
            stats['margin_percent'] = round(margin, 2)
            stats['revenue'] = round(rev, 2)
            stats['cogs'] = round(cogs, 2)

            table_rows.append(stats)
            total_revenue += rev
            total_cogs += cogs
            total_units += stats['units_sold']

        total_profit = total_revenue - total_cogs
        overall_margin = (total_profit / total_revenue * 100.0) if total_revenue > 0 else 0.0

        table_rows.sort(key=lambda x: x['revenue'], reverse=True)

        best_selling = table_rows[0]['name'] if (table_rows and table_rows[0]['units_sold'] > 0) else 'N/A'
        slow_moving_count = sum(1 for r in table_rows if r['units_sold'] == 0)

        cat_perf: Dict[str, Dict[str, Any]] = {}
        for r in table_rows:
            cname = r['category_name']
            if cname not in cat_perf:
                cat_perf[cname] = {'name': cname, 'units': 0, 'revenue': 0.0, 'profit': 0.0}
            cat_perf[cname]['units'] += r['units_sold']
            cat_perf[cname]['revenue'] += r['revenue']
            cat_perf[cname]['profit'] += r['profit']

        cat_list = list(cat_perf.values())
        cat_list.sort(key=lambda x: x['revenue'], reverse=True)

        return {
            'date_label': label,
            'kpis': {
                'best_selling': best_selling,
                'slow_moving_count': slow_moving_count,
                'total_revenue': round(total_revenue, 2),
                'total_cogs': round(total_cogs, 2),
                'total_profit': round(total_profit, 2),
                'overall_margin': round(overall_margin, 2),
                'total_units': total_units
            },
            'products_table': table_rows,
            'category_performance': cat_list
        }

    # -------------------------------------------------------------------------
    # 4. CUSTOMERS ANALYTICS
    # -------------------------------------------------------------------------
    @staticmethod
    def get_customer_analytics(
        range_preset: str = 'this_month',
        start_date: str = None,
        end_date: str = None
    ) -> Dict[str, Any]:
        start_dt, end_dt, label = ReportService.parse_date_range(range_preset, start_date, end_date)

        total_customers_count = Customer.query.count()

        new_customers_query = Customer.query
        if start_dt and end_dt:
            new_customers_query = new_customers_query.filter(Customer.created_at >= start_dt, Customer.created_at <= end_dt)
        new_customers_count = new_customers_query.count()

        bill_query = Bill.query.filter(Bill.status == 'Paid')
        if start_dt and end_dt:
            bill_query = bill_query.filter(Bill.created_at >= start_dt, Bill.created_at <= end_dt)
        bills = bill_query.all()

        cust_spend: Dict[int, Dict[str, Any]] = {}
        walkin_spend = 0.0
        walkin_bills = 0

        for b in bills:
            if b.customer_id:
                cid = b.customer_id
                if cid not in cust_spend:
                    cust_spend[cid] = {
                        'id': cid,
                        'name': b.customer.name if b.customer else 'Unknown',
                        'phone': b.customer.phone if b.customer else '',
                        'bill_count': 0,
                        'total_spend': 0.0,
                        'last_purchase': b.created_at
                    }
                cust_spend[cid]['bill_count'] += 1
                cust_spend[cid]['total_spend'] += b.net_amount
                if b.created_at and b.created_at > cust_spend[cid]['last_purchase']:
                    cust_spend[cid]['last_purchase'] = b.created_at
            else:
                walkin_spend += b.net_amount
                walkin_bills += 1

        active_registered_customers = len(cust_spend)
        total_customer_revenue = sum(c['total_spend'] for c in cust_spend.values()) + walkin_spend

        avg_spend = (total_customer_revenue / active_registered_customers) if active_registered_customers > 0 else 0.0

        top_customers = list(cust_spend.values())
        for c in top_customers:
            c['avg_spend'] = round(c['total_spend'] / c['bill_count'], 2) if c['bill_count'] > 0 else 0.0
            c['total_spend'] = round(c['total_spend'], 2)
            c['last_purchase_str'] = c['last_purchase'].strftime('%Y-%m-%d') if c['last_purchase'] else ''
            del c['last_purchase']

        top_customers.sort(key=lambda x: x['total_spend'], reverse=True)

        top_customer_name = top_customers[0]['name'] if top_customers else 'Walk-in Customers'

        all_customers = Customer.query.all()
        returning_customers_count = sum(1 for c in all_customers if len(c.bills) > 1)

        freq_dist = {'1 Visit': 0, '2-3 Visits': 0, '4-5 Visits': 0, '6+ Visits': 0}
        for c in top_customers:
            cnt = c['bill_count']
            if cnt == 1:
                freq_dist['1 Visit'] += 1
            elif 2 <= cnt <= 3:
                freq_dist['2-3 Visits'] += 1
            elif 4 <= cnt <= 5:
                freq_dist['4-5 Visits'] += 1
            else:
                freq_dist['6+ Visits'] += 1

        return {
            'date_label': label,
            'kpis': {
                'total_customers': total_customers_count,
                'new_customers': new_customers_count,
                'returning_customers': returning_customers_count,
                'total_customer_revenue': round(total_customer_revenue, 2),
                'avg_customer_spend': round(avg_spend, 2),
                'top_customer_name': top_customer_name
            },
            'top_customers': top_customers[:15],
            'frequency_distribution': freq_dist
        }

    # -------------------------------------------------------------------------
    # 5. SUPPLIERS ANALYTICS
    # -------------------------------------------------------------------------
    @staticmethod
    def get_supplier_analytics(
        range_preset: str = 'this_month',
        start_date: str = None,
        end_date: str = None,
        supplier_id: int = None
    ) -> Dict[str, Any]:
        start_dt, end_dt, label = ReportService.parse_date_range(range_preset, start_date, end_date)

        sup_query = Supplier.query
        if supplier_id:
            sup_query = sup_query.filter(Supplier.id == supplier_id)
        suppliers = sup_query.all()
        total_suppliers = len(suppliers)

        sup_data = {}
        for s in suppliers:
            prods = s.products
            inv_val = sum((p.quantity or 0) * (p.purchase_price or 0.0) for p in prods)
            prod_count = len(prods)

            sup_data[s.id] = {
                'id': s.id,
                'name': s.name,
                'phone': s.phone,
                'gst_number': s.gst_number or 'N/A',
                'product_count': prod_count,
                'inventory_value': round(inv_val, 2),
                'units_sold': 0,
                'revenue_generated': 0.0
            }

        bill_query = Bill.query.filter(Bill.status == 'Paid')
        if start_dt and end_dt:
            bill_query = bill_query.filter(Bill.created_at >= start_dt, Bill.created_at <= end_dt)
        bills = bill_query.all()
        bill_ids = [b.id for b in bills]

        if bill_ids and sup_data:
            bis = BillItem.query.filter(BillItem.bill_id.in_(bill_ids)).all()
            for bi in bis:
                if bi.product and bi.product.supplier_id in sup_data:
                    sid = bi.product.supplier_id
                    eqty = max(0, bi.quantity - (bi.returned_quantity or 0))
                    sup_data[sid]['units_sold'] += eqty
                    sup_data[sid]['revenue_generated'] += bi.total_price

        table_rows = list(sup_data.values())
        for r in table_rows:
            r['revenue_generated'] = round(r['revenue_generated'], 2)

        table_rows.sort(key=lambda x: x['revenue_generated'], reverse=True)

        total_purchase_value = sum(r['inventory_value'] for r in table_rows)
        total_store_revenue = sum(r['revenue_generated'] for r in table_rows)

        top_supplier = table_rows[0]['name'] if table_rows else 'N/A'

        chart_labels = [r['name'] for r in table_rows[:8]]
        chart_values = [r['revenue_generated'] for r in table_rows[:8]]

        return {
            'date_label': label,
            'kpis': {
                'total_suppliers': total_suppliers,
                'total_purchase_value': round(total_purchase_value, 2),
                'total_store_revenue': round(total_store_revenue, 2),
                'top_supplier': top_supplier
            },
            'suppliers_table': table_rows,
            'charts': {
                'labels': chart_labels,
                'values': chart_values
            }
        }

    # -------------------------------------------------------------------------
    # 6. FINANCE ANALYTICS
    # -------------------------------------------------------------------------
    @staticmethod
    def get_finance_analytics(
        range_preset: str = 'this_month',
        start_date: str = None,
        end_date: str = None
    ) -> Dict[str, Any]:
        start_dt, end_dt, label = ReportService.parse_date_range(range_preset, start_date, end_date)

        bill_query = Bill.query.filter(Bill.status == 'Paid')
        return_query = BillReturn.query.filter(BillReturn.status == 'Completed')

        if start_dt and end_dt:
            bill_query = bill_query.filter(Bill.created_at >= start_dt, Bill.created_at <= end_dt)
            return_query = return_query.filter(BillReturn.created_at >= start_dt, BillReturn.created_at <= end_dt)

        bills = bill_query.all()
        returns = return_query.all()

        gross_sales = sum(b.total_amount for b in bills)
        discounts = sum(b.discount_amount for b in bills)
        tax_collected = sum(b.tax_amount for b in bills)
        refunds = sum(r.total_refund for r in returns)

        net_sales = max(0.0, gross_sales - discounts - refunds)

        bill_ids = [b.id for b in bills]
        cogs = 0.0
        if bill_ids:
            bis = BillItem.query.filter(BillItem.bill_id.in_(bill_ids)).all()
            for bi in bis:
                eqty = max(0, bi.quantity - (bi.returned_quantity or 0))
                cost = (bi.product.purchase_price if bi.product and bi.product.purchase_price else 0.0)
                cogs += (eqty * cost)

        gross_profit = net_sales - cogs
        profit_margin = (gross_profit / net_sales * 100.0) if net_sales > 0 else 0.0
        net_revenue = net_sales + tax_collected

        trend_labels = []
        trend_net_sales = []
        trend_cogs = []
        trend_profit = []

        if start_dt and end_dt:
            curr = start_dt.date()
            stop = end_dt.date()
            while curr <= stop:
                c_start = datetime.combine(curr, datetime.min.time())
                c_end = datetime.combine(curr, datetime.max.time())
                d_bills = [b for b in bills if c_start <= b.created_at <= c_end]
                d_returns = [r for r in returns if c_start <= r.created_at <= c_end]

                d_gross = sum(b.total_amount for b in d_bills)
                d_disc = sum(b.discount_amount for b in d_bills)
                d_ref = sum(r.total_refund for r in d_returns)
                d_net = max(0.0, d_gross - d_disc - d_ref)

                d_bids = [b.id for b in d_bills]
                d_cogs = 0.0
                if d_bids:
                    d_bis = BillItem.query.filter(BillItem.bill_id.in_(d_bids)).all()
                    for bi in d_bis:
                        eqty = max(0, bi.quantity - (bi.returned_quantity or 0))
                        cost = (bi.product.purchase_price if bi.product and bi.product.purchase_price else 0.0)
                        d_cogs += (eqty * cost)

                d_profit = d_net - d_cogs

                trend_labels.append(curr.strftime('%b %d'))
                trend_net_sales.append(round(d_net, 2))
                trend_cogs.append(round(d_cogs, 2))
                trend_profit.append(round(d_profit, 2))
                curr += timedelta(days=1)

        return {
            'date_label': label,
            'kpis': {
                'gross_sales': round(gross_sales, 2),
                'discounts': round(discounts, 2),
                'tax_collected': round(tax_collected, 2),
                'refunds': round(refunds, 2),
                'net_sales': round(net_sales, 2),
                'cogs': round(cogs, 2),
                'gross_profit': round(gross_profit, 2),
                'profit_margin': round(profit_margin, 2),
                'net_revenue': round(net_revenue, 2)
            },
            'charts': {
                'trend_labels': trend_labels,
                'trend_net_sales': trend_net_sales,
                'trend_cogs': trend_cogs,
                'trend_profit': trend_profit
            }
        }

    # -------------------------------------------------------------------------
    # DYNAMIC CSV EXPORT FUNCTIONS
    # -------------------------------------------------------------------------
    @staticmethod
    def export_csv(submodule: str, filters: Dict[str, Any]) -> Tuple[str, str]:
        """
        Generates CSV content string and filename for given submodule.
        """
        now_str = datetime.utcnow().strftime('%Y-%m')
        preset = filters.get('range_preset', 'this_month')
        start_date = filters.get('start_date')
        end_date = filters.get('end_date')

        output = io.StringIO()
        writer = csv.writer(output)

        if submodule == 'overview':
            data = ReportService.get_overview_analytics(preset, start_date, end_date)
            k = data['kpis']
            writer.writerow(['SmartBilling - Overview Analytics Report', f"Period: {data['date_label']}"])
            writer.writerow([])
            writer.writerow(['Metric', 'Value'])
            writer.writerow(['Total Revenue (INR)', f"{k['total_revenue']:.2f}"])
            writer.writerow(['Gross Profit (INR)', f"{k['gross_profit']:.2f}"])
            writer.writerow(['Profit Margin (%)', f"{k['profit_margin']:.2f}%"])
            writer.writerow(['Total Bills', k['total_bills']])
            writer.writerow(['Items Sold', k['items_sold']])
            writer.writerow(['Total Discounts (INR)', f"{k['total_discounts']:.2f}"])
            writer.writerow(['Total Tax (INR)', f"{k['total_tax']:.2f}"])
            writer.writerow(['Total Refunds (INR)', f"{k['total_refunds']:.2f}"])
            writer.writerow(['Net Sales (INR)', f"{k['net_sales']:.2f}"])
            filename = f"overview-report-{now_str}.csv"

        elif submodule == 'sales':
            data = ReportService.get_sales_analytics(
                preset, start_date, end_date,
                filters.get('payment_method'), filters.get('category_id')
            )
            k = data['kpis']
            writer.writerow(['SmartBilling - Sales Analytics Report', f"Period: {data['date_label']}"])
            writer.writerow([])
            writer.writerow(['Metric', 'Value'])
            writer.writerow(['Total Sales (INR)', f"{k['total_sales']:.2f}"])
            writer.writerow(['Number of Bills', k['num_bills']])
            writer.writerow(['Items Sold', k['items_sold']])
            writer.writerow(['Average Bill Value (INR)', f"{k['avg_bill_value']:.2f}"])
            writer.writerow(['Sales Growth (%)', f"{k['sales_growth']:.2f}%"])
            writer.writerow(['Total Discounts (INR)', f"{k['total_discounts']:.2f}"])
            writer.writerow(['Total Tax (INR)', f"{k['total_tax']:.2f}"])
            writer.writerow([])
            writer.writerow(['Top Selling Products', 'Quantity Sold', 'Revenue (INR)'])
            for tp in data['charts']['top_products']:
                writer.writerow([tp['name'], tp['qty'], f"{tp['revenue']:.2f}"])
            filename = f"sales-report-{now_str}.csv"

        elif submodule == 'products':
            data = ReportService.get_product_analytics(
                preset, start_date, end_date,
                filters.get('category_id'), filters.get('product_id')
            )
            writer.writerow(['SmartBilling - Product Performance Report', f"Period: {data['date_label']}"])
            writer.writerow([])
            writer.writerow(['Product Name', 'SKU', 'Category', 'Purchase Price (INR)', 'Selling Price (INR)', 'Units Sold', 'Revenue (INR)', 'COGS (INR)', 'Profit (INR)', 'Margin (%)'])
            for row in data['products_table']:
                writer.writerow([
                    row['name'], row['sku'], row['category_name'],
                    f"{row['purchase_price']:.2f}", f"{row['selling_price']:.2f}",
                    row['units_sold'], f"{row['revenue']:.2f}", f"{row['cogs']:.2f}",
                    f"{row['profit']:.2f}", f"{row['margin_percent']:.2f}%"
                ])
            filename = f"product-performance-report-{now_str}.csv"

        elif submodule == 'customers':
            data = ReportService.get_customer_analytics(preset, start_date, end_date)
            writer.writerow(['SmartBilling - Customer Analytics Report', f"Period: {data['date_label']}"])
            writer.writerow([])
            writer.writerow(['Customer Name', 'Phone', 'Bills Count', 'Total Spend (INR)', 'Avg Spend (INR)', 'Last Purchase Date'])
            for row in data['top_customers']:
                writer.writerow([
                    row['name'], row['phone'], row['bill_count'],
                    f"{row['total_spend']:.2f}", f"{row['avg_spend']:.2f}", row['last_purchase_str']
                ])
            filename = f"customer-analytics-report-{now_str}.csv"

        elif submodule == 'suppliers':
            data = ReportService.get_supplier_analytics(preset, start_date, end_date, filters.get('supplier_id'))
            writer.writerow(['SmartBilling - Supplier Analytics Report', f"Period: {data['date_label']}"])
            writer.writerow([])
            writer.writerow(['Supplier Name', 'Phone', 'GST Number', 'Products Count', 'Inventory Value (INR)', 'Units Sold', 'Revenue Generated (INR)'])
            for row in data['suppliers_table']:
                writer.writerow([
                    row['name'], row['phone'], row['gst_number'], row['product_count'],
                    f"{row['inventory_value']:.2f}", row['units_sold'], f"{row['revenue_generated']:.2f}"
                ])
            filename = f"supplier-analytics-report-{now_str}.csv"

        elif submodule == 'finance':
            data = ReportService.get_finance_analytics(preset, start_date, end_date)
            k = data['kpis']
            writer.writerow(['SmartBilling - Finance Analytics Report', f"Period: {data['date_label']}"])
            writer.writerow([])
            writer.writerow(['Financial Metric', 'Amount (INR)'])
            writer.writerow(['Gross Sales', f"{k['gross_sales']:.2f}"])
            writer.writerow(['Discounts', f"{k['discounts']:.2f}"])
            writer.writerow(['Refunds', f"{k['refunds']:.2f}"])
            writer.writerow(['Net Sales', f"{k['net_sales']:.2f}"])
            writer.writerow(['Tax Collected', f"{k['tax_collected']:.2f}"])
            writer.writerow(['Net Revenue', f"{k['net_revenue']:.2f}"])
            writer.writerow(['Cost of Goods Sold (COGS)', f"{k['cogs']:.2f}"])
            writer.writerow(['Gross Profit', f"{k['gross_profit']:.2f}"])
            writer.writerow(['Profit Margin (%)', f"{k['profit_margin']:.2f}%"])
            filename = f"finance-report-{now_str}.csv"

        else:
            writer.writerow(['Invalid Report Type'])
            filename = f"report-{now_str}.csv"

        return output.getvalue(), filename
