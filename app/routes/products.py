from flask import Blueprint, request, jsonify, render_template
from flask_login import current_user

from app import db
from app.models import Product, Category
from app.utils.decorators import admin_required

product_bp = Blueprint('products', __name__)


@product_bp.route('/', methods=['GET'])
def get_products():
    """Get all products with optional category filter"""
    # Get selected category from query string
    category_id = request.args.get('category', type=int)

    # Get all categories for filter buttons
    categories = Category.query.all()

    # Base product query - show only active products
    products_query = Product.query.filter_by(is_active=True)

    # Apply category filter if provided
    if category_id:
        products_query = products_query.filter_by(category_id=category_id)

    # Get all products
    products = products_query.all()

    return render_template(
        'products.html',
        products=products,
        categories=categories,
        selected_category=category_id
    )


@product_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    """Get single product detail page"""
    product = Product.query.get_or_404(id)
    return render_template('product_detail.html', product=product, current_user=current_user)


@product_bp.route('/', methods=['POST'])
@admin_required
def create_product():
    """Create new product (Admin only)"""
    data = request.get_json()

    product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        stock_quantity=data.get('stock_quantity', 0),
        image_url=data.get('image_url', ''),
        category_id=data.get('category_id')
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({'message': 'Product created', 'id': product.id}), 201


@product_bp.route('/<int:id>', methods=['PUT'])
@admin_required
def update_product(id):
    """Update product (Admin only)"""
    product = Product.query.get_or_404(id)
    data = request.get_json()

    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.stock_quantity = data.get('stock_quantity', product.stock_quantity)
    product.image_url = data.get('image_url', product.image_url)
    product.category_id = data.get('category_id', product.category_id)

    db.session.commit()

    return jsonify({'message': 'Product updated'}), 200


@product_bp.route('/<int:id>', methods=['DELETE'])
@admin_required
def delete_product(id):
    """Delete product (Admin only)"""
    product = Product.query.get_or_404(id)

    # Soft delete (is_active = False)
    product.is_active = False
    db.session.commit()

    return jsonify({'message': 'Product deleted'}), 200


@product_bp.route('/search', methods=['GET'])
def search_products():
    """Search products by name or category (API endpoint)"""
    query = request.args.get('q', '')
    category_id = request.args.get('category_id', type=int)

    # Start with active products only
    products = Product.query.filter_by(is_active=True)

    # Apply search query if provided
    if query:
        products = products.filter(Product.name.ilike(f'%{query}%'))

    # Apply category filter if provided
    if category_id:
        products = products.filter_by(category_id=category_id)

    return jsonify([p.to_dict() for p in products.all()]), 200