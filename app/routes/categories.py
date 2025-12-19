from flask import Blueprint, request, jsonify
from app import db
from app.models import Category
from app.utils.decorators import admin_required

category_bp = Blueprint('categories', __name__)


@category_bp.route('/', methods=['GET'])
def get_categories():
    """Get all categories"""
    categories = Category.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description,
        'product_count': c.products.count()
    } for c in categories]), 200


@category_bp.route('/', methods=['POST'])
@admin_required
def create_category():
    """Create new category (Admin only)"""
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

    return jsonify({'message': 'Category created', 'id': category.id}), 201


@category_bp.route('/<int:id>', methods=['GET'])
def get_category(id):
    """Get single category with products"""
    category = Category.query.get_or_404(id)

    return jsonify({
        'id': category.id,
        'name': category.name,
        'description': category.description,
        'products': [p.to_dict() for p in category.products]
    }), 200