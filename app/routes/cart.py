from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app import db
from app.models import CartItem, Product
from app.services.cart_service import CartService
from app.utils.vallidators import validate_quantity

cart_bp = Blueprint('cart', __name__)



@cart_bp.route('/', methods=['GET'])
@login_required
def get_cart():
    """Get user's cart"""
    # cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    #
    # # Total calculate qilish
    # total = sum(item.subtotal for item in cart_items)
    #
    # return jsonify({
    #     'items': [item.to_dict() for item in cart_items],
    #     'total': total,
    #     'item_count': len(cart_items)
    # }), 200
    # cart = CartService.get_user_cart(current_user.id)
    # return jsonify({
    #     'items': [item.to_dict() for item in cart['items']],
    #     'total': cart['total'],
    #     'item_count': cart['count']
    #
    # }), 200
    # Check if it's an AJAX request (JSON)
    if request.headers.get('Accept') == 'application/json' or request.is_json:
        # Return JSON for AJAX
        cart = CartService.get_user_cart(current_user.id)
        return jsonify({
            'items': [item.to_dict() for item in cart['items']],
            'total': cart['total'],
            'item_count': cart['count']
        }), 200

    # Return HTML page for browser
    return render_template('cart.html')


@cart_bp.route('/', methods=['POST'])
@login_required
def add_to_cart():
    """Add item to cart"""
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    # # Product mavjudmi tekshirish
    # product = Product.query.get_or_404(product_id)
    #
    # # Stock bormi tekshirish
    # if product.stock_quantity < quantity:
    #     return jsonify({'error': 'Not enough stock'}), 400

    # Validate
    is_valid, error = validate_quantity(quantity)
    if not is_valid:
        return jsonify({'error': error}), 400

    # Cart item mavjudmi tekshirish
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()

    if cart_item:
        # Agar mavjud bo'lsa, quantity ni update qilish
        cart_item.quantity += quantity
    else:
        # Yangi item yaratish
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)

    db.session.commit()

    return jsonify({
        'message': 'Item added to cart',
        'cart_item': cart_item.to_dict()
    }), 201


@cart_bp.route('/<int:item_id>', methods=['PUT'])
@login_required
def update_cart_item(item_id):
    """Update cart item quantity"""
    cart_item = CartItem.query.get_or_404(item_id)

    # Check ownership
    if cart_item.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    quantity = data.get('quantity')

    # Validate quantity
    if quantity <= 0:
        return jsonify({'error': 'Quantity must be greater than 0'}), 400

    # Check stock
    if cart_item.product.stock_quantity < quantity:
        return jsonify({'error': 'Not enough stock'}), 400

    cart_item.quantity = quantity
    db.session.commit()

    return jsonify({
        'message': 'Cart item updated',
        'cart_item': cart_item.to_dict()
    }), 200


@cart_bp.route('/<int:item_id>', methods=['DELETE'])
@login_required
def remove_from_cart(item_id):
    """Remove item from cart"""
    cart_item = CartItem.query.get_or_404(item_id)

    # Check ownership
    if cart_item.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({'message': 'Item removed from cart'}), 200


@cart_bp.route('/clear', methods=['DELETE'])
@login_required
def clear_cart():
    """Clear entire cart"""
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()

    return jsonify({'message': 'Cart cleared'}), 200