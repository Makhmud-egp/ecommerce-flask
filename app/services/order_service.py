from app import db
from app.models import Order, OrderItem, CartItem, Product


class OrderService:

    @staticmethod
    def create_order_from_cart(user_id, shipping_address):
        """Create order from user's cart"""
        # Get cart items
        cart_items = CartItem.query.filter_by(user_id=user_id).all()

        if not cart_items:
            return None, "Cart is empty"

        # Calculate total
        total = sum(item.subtotal for item in cart_items)

        # Check stock for all items
        for item in cart_items:
            if item.product.stock_quantity < item.quantity:
                return None, f"Not enough stock for {item.product.name}"

        # Create order
        order = Order(
            user_id=user_id,
            total_amount=total,
            shipping_address=shipping_address,
            status='pending'
        )
        db.session.add(order)
        db.session.flush()  # Get order.id

        # Create order items and reduce stock
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_time=item.product.price
            )
            db.session.add(order_item)

            # Reduce stock
            item.product.stock_quantity -= item.quantity

        # Clear cart
        CartItem.query.filter_by(user_id=user_id).delete()

        db.session.commit()
        return order, None

    @staticmethod
    def update_order_status(order_id, status, payment_id=None):
        """Update order status"""
        order = Order.query.get(order_id)
        if not order:
            return False

        order.status = status
        if payment_id:
            order.stripe_payment_id = payment_id

        db.session.commit()
        return True