from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required, current_user
from app.utils.decorators import admin_required

from app.models import Category, Product

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Home page"""
    # return {'message': 'Welcome to E-commerce API!'}
    categories = Category.query.all()
    return render_template('index.html', categories=categories)


# @main_bp.route('/dashboard')
# @login_required
# def dashboard():
#     return {
#         'message': f'Welcome {current_user.email}!',
#         'user': current_user.id
#     }

# @main_bp.route('/admin/dashboard')
# @admin_required
# def admin_dashboard():
#     return {'message': 'Admin Dashboard'}


@main_bp.route('/products')
def products():
    """Products list page"""
    categories=Category.query.all()
    selected_category=request.args.get('category', type=int)

    query=Product.query.filter_by(category_id=selected_category)
    if selected_category:
        query = query.filter_by(category_id=selected_category)

    products = query.all()

    return render_template('products.html',
                           products=products,
                           categories=categories,
                           selected_category=selected_category)

@main_bp.route('/products/<int:id>')
def product_detail(id):
    """Product detail page"""
    product = Product.query.get_or_404(id)
    return render_template('product_detail.html', product=product)


@main_bp.route('/checkout')
@login_required
def checkout():
    """Checkout page"""
    return render_template('checkout.html')

@main_bp.route('/orders')
@login_required
def orders_page():
    """Orders list page"""
    return render_template('orders.html')

@main_bp.route('/health')
def health_check():
    """Health check for monitoring"""
    return jsonify({'status': 'healthy'}), 200

