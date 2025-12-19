from flask import Blueprint, request, render_template, jsonify, redirect, url_for, current_app
from flask_login import login_required, current_user
from app.models import Order
from app.services.order_service import OrderService

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/<int:order_id>')
@login_required
def payment_page(order_id):
    """Payment page with Stripe Elements"""
    order = Order.query.get_or_404(order_id)

    # Check ownership
    if order.user_id != current_user.id:
        return redirect(url_for('main.index'))

    # Get client_secret from URL
    client_secret = request.args.get('client_secret')

    return render_template('payment.html',
                           order_id=order_id,
                           total_amount=float(order.total_amount),
                           client_secret=client_secret,
                           stripe_public_key = current_app.config['STRIPE_PUBLIC_KEY']
                           )

@payment_bp.route('/success')
@login_required
def payment_success():
    """Payment success page"""
    order_id = request.args.get('order_id')

    # Update order status to paid
    if order_id:
        OrderService.update_order_status(order_id, 'paid')

    return render_template('payment_success.html', order_id=order_id)


@payment_bp.route('/failure')
@login_required
def payment_failure():
    """Payment failure page"""
    return render_template('payment_failure.html')