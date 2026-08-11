from app.database import db
from app.models.product import Product
from app.models.inventory import InventoryHistory

class InventoryService:
    @staticmethod
    def adjust_stock(product_id: int, quantity_change: int, change_type: str, reason: str, user_id: int, remarks: str = '') -> tuple[bool, str]:
        if not product_id:
            return False, "Invalid product selection."

        if abs(quantity_change) == 0:
            return False, "Quantity must be greater than 0."

        try:
            # DB Transaction: Retrieve current product stock
            product = Product.query.get(product_id)
            if not product:
                return False, "Product not found in system."

            if product.status != 'Active':
                return False, f"Product '{product.name}' is currently inactive."

            previous_stock = product.quantity or 0

            if change_type == 'Stock Out':
                qty_abs = abs(quantity_change)
                if qty_abs > previous_stock:
                    return False, f"Insufficient stock. Current stock is {previous_stock} {product.unit}."
                qty_delta = -qty_abs
            else:  # Stock In
                qty_delta = abs(quantity_change)

            new_stock = previous_stock + qty_delta
            if new_stock < 0:
                return False, "Stock quantity cannot be negative."

            # Update product stock
            product.quantity = new_stock

            # Insert audit record
            history_entry = InventoryHistory(
                product_id=product.id,
                change_type=change_type,
                quantity_changed=qty_delta,
                previous_stock=previous_stock,
                remaining_quantity=new_stock,
                reason=reason or 'Manual Stock Adjustment',
                remarks=remarks or '',
                performed_by_user_id=user_id
            )
            db.session.add(history_entry)
            db.session.flush()
            history_entry.reference_code = f"MANUAL-ADJ-{history_entry.id:04d}"

            db.session.commit()

            return True, f"Stock updated successfully. {product.name}: {previous_stock} → {new_stock}"

        except Exception as e:
            db.session.rollback()
            return False, f"Failed to record stock audit adjustment: {str(e)}"
