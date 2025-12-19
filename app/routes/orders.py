from flask import Blueprint, request, jsonify, current_app, redirect, url_for, render_template
from flask_login import login_required, current_user
from app import db
from app.models import Order
from app.services.cart_service import CartService
from app.services.order_service import OrderService
from app.services.payment_service import PaymentService

order_bp = Blueprint('orders', __name__)


@order_bp.route('/checkout', methods=['GET'])
@login_required
def checkout_page():
    """Render checkout page"""
    cart = CartService.get_user_cart(current_user.id)

    # If cart is empty, redirect to products
    if not cart['items']:
        return redirect(url_for('product.get_products'))

    return render_template('checkout.html')


@order_bp.route('/', methods=['GET'])
@login_required
def get_orders():
    """Get user's orders"""
    # Check if it`s an AJAX request
    if request.headers.get('Accept') == 'application/json' or request.is_json:
        # Return
        orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.id.desc()).all()
        return jsonify([order.to_dict() for order in orders]), 200

    # Return Html page for browser
    return render_template('orders.html')

@order_bp.route('/<int:id>', methods=['GET'])
@login_required
def get_order(id):
    """Get single order"""
    order = Order.query.get_or_404(id)

    # Check ownership
    if order.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify(order.to_dict()), 200


@order_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    """Create order and payment intent"""
    data = request.get_json()
    shipping_address = data.get('shipping_address')

    if not shipping_address:
        return jsonify({'error': 'Shipping address required'}), 400

    # Create order from cart
    order, error = OrderService.create_order_from_cart(
        user_id=current_user.id,
        shipping_address=shipping_address
    )

    if error:
        return jsonify({'error': error}), 400

    # Create Stripe payment intent
    payment_intent = PaymentService.create_payment_intent(
        amount=float(order.total_amount)
    )

    if not payment_intent:
        return jsonify({'error': 'Payment initialization failed'}), 500

    # Update order with payment intent
    order.stripe_payment_id = payment_intent.id
    db.session.commit()

    return jsonify({
        'order_id': order.id,
        'client_secret': payment_intent.client_secret,
        'total_amount': float(order.total_amount)
    }), 201


@order_bp.route('/<int:id>/status', methods=['PUT'])
@login_required
def update_order_status(id):
    """Update order status (for testing)"""
    order = Order.query.get_or_404(id)

    # Check ownership
    if order.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    status = data.get('status')

    if status not in ['pending', 'paid', 'processing', 'shipped', 'delivered', 'cancelled']:
        return jsonify({'error': 'Invalid status'}), 400

    order.status = status
    db.session.commit()

    return jsonify({'message': 'Order status updated'}), 200