from flask import Blueprint, request, jsonify, render_template, url_for, redirect, flash
from app import db
from app.models.user import User
from flask_login import login_user, logout_user, current_user, login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # JSON data olish (JavaScript fetch uchun)
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400

        user = User(email=email, first_name=first_name)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'Registration successful'}), 201

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # JSON data olish
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return jsonify({'message': 'Login successful'}), 200

        return jsonify({'error': 'Invalid email or password'}), 401

    return render_template('auth/login.html')


@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('Logged out successfully', 'success')
    # return jsonify({'message': 'Logged out successfully'}), 200
    return redirect(url_for('main.home'))


@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Get current logged in user"""
    if current_user.is_authenticated:
        return jsonify({
            'id': current_user.id,
            'email': current_user.email,
            'first_name': current_user.first_name,
            'is_admin': current_user.is_admin
        }), 200

    return jsonify({'error': 'Not authenticated'}), 401
