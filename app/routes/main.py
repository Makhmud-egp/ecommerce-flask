from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return {'message': 'Welcome to E-commerce API!'}

@main_bp.route('/health')
def health():
    return {'status': 'OK'}