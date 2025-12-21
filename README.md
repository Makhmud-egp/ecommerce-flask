# 🛒 E-Commerce Platform with Stripe Integration

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3+-green?style=for-the-badge&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Stripe](https://img.shields.io/badge/Stripe-API-blueviolet?style=for-the-badge&logo=stripe&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**[🌐 Live Demo](https://makhmudegp.pythonanywhere.com)** · **[📧 Report Bug](mailto:osonpy@gmail.com)** · **[💡 Request Feature](mailto:osonpy@gmail.com)**

</div>

---

## 📖 Project Haqida

To'liq funksional **e-commerce web platformasi** - mustaqil ishlab chiqilgan **MVP versiyasi**. Foydalanuvchilar mahsulotlarni ko'rishlari, savatga qo'shishlari va **Stripe** orqali xavfsiz to'lov amalga oshirishlari mumkin.

Bu loyiha **portfolio project** sifatida yaratilgan va backend development, payment integration, va full-stack development ko'nikmalarini namoyish qiladi.

---

## ✨ Asosiy Imkoniyatlar

### 🔐 User Authentication
- ✅ Ro'yxatdan o'tish (Registration)
- ✅ Kirish/Chiqish (Login/Logout)
- ✅ Password hashing & security
- ✅ Session management

### 🛍️ Shopping Experience
- ✅ Product catalog with categories
- ✅ Product search & filtering
- ✅ Detailed product pages
- ✅ Shopping cart functionality
- ✅ Real-time cart updates

### 💳 Payment Processing
- ✅ **Stripe payment integration**
- ✅ Secure checkout process
- ✅ Test mode enabled
- ✅ Payment confirmation
- ✅ Order receipt

### 📊 Order Management
- ✅ Order history
- ✅ Order status tracking
- ✅ Order details & receipts

### 👨‍💼 Admin Panel
- ✅ Product management (CRUD)
- ✅ Order overview
- ✅ User management
- ✅ Dashboard analytics

### 🎨 User Interface
- ✅ Responsive design (mobile-friendly)
- ✅ Bootstrap styling
- ✅ Intuitive navigation
- ✅ Professional look

---

## 🚀 Live Demo

**[Demo'ni ko'ring →](https://makhmudegp.pythonanywhere.com)**

### Test Credentials:

**Regular User:**
- Email: `test@example.com`
- Password: `test123`

**Admin User:**
- Email: `admin@shop.com`
- Password: `Admin123!`

### Test Payment:

Stripe test mode enabled. Ishlatish uchun:

```
Card Number: 4242 4242 4242 4242
Expiry Date: 12/25 (yoki istalgan kelajak sana)
CVC: 123 (yoki istalgan 3 raqam)
ZIP: 12345 (yoki istalgan 5 raqam)
```

---

## 🛠️ Technology Stack

### Backend
- **Python 3.10+** - Core programming language
- **Flask 2.3+** - Web framework
- **SQLAlchemy 2.0+** - ORM for database operations
- **Flask-Login** - User session management
- **Werkzeug** - Password hashing & security

### Database
- **SQLite** - Development database
- **PostgreSQL** - Production ready (can be configured)

### Payment
- **Stripe API** - Payment processing
- **Stripe Checkout** - Secure payment interface

### Frontend
- **HTML5/CSS3** - Structure & styling
- **Bootstrap 5** - Responsive framework
- **JavaScript** - Client-side interactivity
- **Jinja2** - Template engine

### Deployment
- **PythonAnywhere** - Hosting platform
- **WSGI** - Production server

---

## 📸 Screenshots

### Homepage
![Homepage](screenshots/homepage.png)


*Main landing page with featured products*

### Product Catalog
![Products](screenshots/products.png)
*Browse all products with categories*

### Product Details
![Product Detail](screenshots/product-detail.png)
*Detailed product information*

### Shopping Cart
![Cart](screenshots/cart.png)
*Review items before checkout*

### Stripe Checkout
![Checkout](screenshots/checkout.png)
*Secure payment with Stripe*

### Order Confirmation
![Confirmation](screenshots/confirmation.png)
*Order success & receipt*

### Admin Dashboard
![Admin](screenshots/admin.png)
*Admin panel for management*

---

## 🏃‍♂️ Local Setup

### Prerequisites

```bash
Python 3.10 or higher
pip (Python package manager)
Git
```

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/Makhmud-egp/ecommerce-flask.git
cd ecommerce-flask
```

2. **Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_APP=app.py
FLASK_ENV=development

# Database
DATABASE_URL=sqlite:///ecommerce.db

# Stripe Keys (Test Mode)
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key
STRIPE_SECRET_KEY=sk_test_your_secret_key

# Email (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

5. **Initialize database**
```bash
python
>>> from app import db, app
>>> with app.app_context():
...     db.create_all()
...     print("Database created!")
>>> exit()
```

6. **Run the application**
```bash
python app.py
```

Visit: `http://localhost:5000`

---

## 📁 Project Structure

```
ecommerce-flask/
│
├── app.py                  # Main application file
├── models.py               # Database models
├── routes.py               # Application routes
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
│
├── static/                 # Static files
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   └── images/            # Product images
│
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Homepage
│   ├── products.html      # Product listing
│   ├── product.html       # Product detail
│   ├── cart.html          # Shopping cart
│   ├── checkout.html      # Checkout page
│   ├── auth/              # Authentication templates
│   └── admin/             # Admin templates
│
├── migrations/             # Database migrations
├── instance/              # Instance-specific files
│   └── ecommerce.db       # SQLite database
│
└── screenshots/           # Project screenshots
```

---

## 🔧 Configuration

### Database Models

**User Model:**
```python
- id (Primary Key)
- username
- email (Unique)
- password_hash
- is_admin (Boolean)
- created_at
```

**Product Model:**
```python
- id (Primary Key)
- name
- description
- price
- category
- image_url
- stock
- created_at
```

**Order Model:**
```python
- id (Primary Key)
- user_id (Foreign Key)
- total_amount
- status
- stripe_payment_id
- created_at
```

**OrderItem Model:**
```python
- id (Primary Key)
- order_id (Foreign Key)
- product_id (Foreign Key)
- quantity
- price
```

---

## 🌐 Deployment

### Deploy to PythonAnywhere

1. Sign up at [PythonAnywhere](https://www.pythonanywhere.com)
2. Clone repository in Bash console
3. Create virtual environment and install dependencies
4. Configure Web app in Web tab
5. Set up WSGI file
6. Configure static files
7. Reload web app

Detailed deployment guide: [DEPLOYMENT.md](DEPLOYMENT.md)

### Environment Variables for Production

```bash
SECRET_KEY=strong-random-secret-key
DATABASE_URL=postgresql://user:password@host:port/database
STRIPE_PUBLISHABLE_KEY=your_live_publishable_key
STRIPE_SECRET_KEY=your_live_secret_key
FLASK_ENV=production
```

---

## 🧪 Testing

### Test Payment Cards

**Success:**
- `4242 4242 4242 4242` - Successful payment

**Decline:**
- `4000 0000 0000 0002` - Card declined
- `4000 0000 0000 9995` - Insufficient funds

**3D Secure:**
- `4000 0027 6000 3184` - Requires authentication

More test cards: [Stripe Testing](https://stripe.com/docs/testing)

---

## 🐛 Known Issues & Future Enhancements

### Current Limitations:
- ⚠️ Email notifications not implemented
- ⚠️ Advanced search filters limited
- ⚠️ No product reviews/ratings yet

### Planned Features:
- 🎯 Email confirmation for orders
- 🎯 Product reviews and ratings
- 🎯 Wishlist functionality
- 🎯 Advanced filtering (price range, sorting)
- 🎯 Multiple payment methods
- 🎯 Order tracking with shipping updates
- 🎯 Discount codes & promotions
- 🎯 Multi-language support

---

## 🤝 Contributing

Contributions are welcome! Agar siz bu proyektni yaxshilashga yordam bermoqchi bo'lsangiz:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Makhmud Djalolov**

- GitHub: [@Makhmud-egp](https://github.com/Makhmud-egp)
- LinkedIn: [Makhmud Djalolov](https://www.linkedin.com/in/makhmud-djalolov-8928b332b/)
- Email: [osonpy@gmail.com](mailto:osonpy@gmail.com)
- Portfolio: [makhmud-egp.github.io](https://makhmud-egp.github.io)
- Telegram: [@osonpython](https://t.me/osonpython)

---

## 🙏 Acknowledgments

- Flask documentation
- Stripe API documentation
- Bootstrap framework
- PythonAnywhere hosting
- Stack Overflow community

---

## 📊 Project Stats

- **Lines of Code:** ~2000+
- **Development Time:** 3 weeks
- **Technologies Used:** 10+
- **Features Implemented:** 15+

---

<div align="center">

### ⭐ Star this repository if you found it helpful!

### 💬 Questions? [Open an issue](https://github.com/Makhmud-egp/ecommerce-flask/issues)

---

**Made with ❤️ and Python**

*Last Updated: December 2024*

</div>
