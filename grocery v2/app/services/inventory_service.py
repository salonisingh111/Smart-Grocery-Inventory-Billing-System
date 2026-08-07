from app.database import db
from app.models.product import Product
from app.models.inventory import InventoryHistory

class InventoryService:
    @staticmethod
    def adjust_stock(product_id: int, quantity_change: int, change_type: str, reason: str, user_id: int) -> tuple[bool, str]:
        product = Product.query.get(product_id)
        if not product:
            return False, "Product not found."

        new_qty = product.quantity + quantity_change
        if new_qty < 0:
            return False, "Negative inventory is not allowed."

        product.quantity = new_qty
        
        # Record history log
        history_entry = InventoryHistory(
            product_id=product.id,
            change_type=change_type,
            quantity_changed=quantity_change,
            remaining_quantity=new_qty,
            reason=reason,
            performed_by_user_id=user_id
        )
        db.session.add(history_entry)
        db.session.commit()

        return True, f"Stock updated successfully. New quantity: {new_qty}"
