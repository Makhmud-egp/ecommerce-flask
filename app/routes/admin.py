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


# ========== ORDERS ==========

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
    if request.headers.get('Accept') == 'application/json':
        orders = Order.query.order_by(Order.created_at.desc()).all()
        return jsonify([order.to_dict() for order in orders])
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


# ========== PRODUCTS ==========

@admin_bp.route('/products')
@admin_required
def admin_products_page():
    """Admin products page or JSON API"""
    # Check if JSON request (from JavaScript fetch)
    if request.headers.get('Accept') == 'application/json':
        # Return all products (including inactive)
        products = Product.query.all()
        return jsonify([p.to_dict() for p in products])

    # Return HTML page
    return render_template('admin/products.html')


@admin_bp.route('/products', methods=['POST'])
@admin_required
def admin_create_product():
    """Create new product (Admin API)"""
    data = request.get_json()

    product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        stock_quantity=data.get('stock_quantity', 0),
        image_url=data.get('image_url', ''),
        category_id=data.get('category_id'),
        is_active=data.get('is_active', True)
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        'message': 'Product created successfully',
        'id': product.id
    }), 201


@admin_bp.route('/products/<int:id>', methods=['PUT'])
@admin_required
def admin_update_product(id):
    """Update product (Admin API)"""
    product = Product.query.get_or_404(id)
    data = request.get_json()

    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.stock_quantity = data.get('stock_quantity', product.stock_quantity)
    product.image_url = data.get('image_url', product.image_url)
    product.category_id = data.get('category_id', product.category_id)
    product.is_active = data.get('is_active', product.is_active)

    db.session.commit()

    return jsonify({'message': 'Product updated successfully'}), 200


@admin_bp.route('/products/<int:id>', methods=['DELETE'])
@admin_required
def admin_delete_product(id):
    """Delete product (Admin API - soft delete)"""
    product = Product.query.get_or_404(id)

    # Soft delete
    product.is_active = False
    db.session.commit()

    return jsonify({'message': 'Product deleted successfully'}), 200


# ========== CATEGORIES ==========

@admin_bp.route('/categories')
@admin_required
def admin_categories_page():
    """Admin categories page or JSON API"""
    # Check if JSON request
    if request.headers.get('Accept') == 'application/json':
        categories = Category.query.all()
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'description': c.description,
            'product_count': c.products.count()
        } for c in categories])

    # Return HTML page
    return render_template('admin/categories.html')


@admin_bp.route('/categories', methods=['POST'])
@admin_required
def admin_create_category():
    """Create new category (Admin API)"""
    data = request.get_json()

    # Check if exists
    if Category.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Category already exists'}), 400

    category = Category(
        name=data['name'],
        description=data.get('description', '')
    )

    db.session.add(category)
    db.session.commit()

    return jsonify({
        'message': 'Category created',
        'id': category.id
    }), 201