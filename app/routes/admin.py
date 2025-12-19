from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import login_required
from app import db
from app.models import Order, Product, User, Category
from app.utils.decorators import admin_required
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
@admin_required
def admin_index():
    """Redirect to dashboard"""
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard page"""
    return render_template('admin/dashboard.html')


@admin_bp.route('/stats')
@admin_required
def get_stats():
    """Get dashboard statistics"""
    total_orders = Order.query.count()
    total_revenue = db.session.query(func.sum(Order.total_amount)).scalar() or 0
    total_products = Product.query.count()
    total_users = User.query.count()

    return jsonify({
        'total_orders': total_orders,
        'total_revenue': float(total_revenue),
        'total_products': total_products,
        'total_users': total_users
    })


@admin_bp.route('/orders/api')
@admin_required
def orders_api():
    """Get orders as JSON (for dashboard)"""
    limit = request.args.get('limit', type=int)
    query = Order.query.order_by(Order.created_at.desc())

    if limit:
        query = query.limit(limit)

    orders = query.all()
    return jsonify([order.to_dict() for order in orders])


@admin_bp.route('/orders')
@admin_required
def orders_page():
    """Admin orders page or JSON API"""
    # Check if it's an AJAX/JSON request
    if request.headers.get('Accept') == 'application/json':
        # Return JSON for API calls
        orders = Order.query.order_by(Order.created_at.desc()).all()
        return jsonify([order.to_dict() for order in orders])

    # Return HTML page for browser
    return render_template('admin/orders.html')


@admin_bp.route('/orders/<int:id>/status', methods=['PUT'])
@admin_required
def admin_update_order_status(id):
    """Update order status"""
    order = Order.query.get_or_404(id)
    data = request.get_json()

    order.status = data.get('status', order.status)
    db.session.commit()

    return jsonify({'message': 'Order updated'})


@admin_bp.route('/products')
@admin_required
def products_page():
    """Admin products management page"""
    if request.headers.get('Accept') == 'application/json':
        products = Product.query.all()
        return jsonify([p.to_dict() for p in products])
    return render_template('admin/products.html')


@admin_bp.route('/categories')
@admin_required
def categories_page():
    """Admin categories page"""
    return render_template('admin/categories.html')