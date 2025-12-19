from app import db
from app.models import CartItem, Product


class CartService:

    @staticmethod
    def get_user_cart(user_id):
        """Get user's cart with total"""
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        total = sum(item.subtotal for item in cart_items)

        return {
            'items': cart_items,
            'total': total,
            'count': len(cart_items)
        }

    @staticmethod
    def add_item(user_id, product_id, quantity=1):
        """Add or update cart item"""
        product = Product.query.get(product_id)

        if not product or product.stock_quantity < quantity:
            return None

        cart_item = CartItem.query.filter_by(
            user_id=user_id,
            product_id=product_id
        ).first()

        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)

        db.session.commit()
        return cart_item

    @staticmethod
    def clear_user_cart(user_id):
        """Clear user's cart"""
        CartItem.query.filter_by(user_id=user_id).delete()
        db.session.commit()