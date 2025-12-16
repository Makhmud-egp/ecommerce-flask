from app import create_app, db

# App yaratish
app = create_app()

# Database tables yaratish
with app.app_context():
    db.create_all()
    print("Database tables created!")

# Server run qilish
if __name__ == '__main__':
    app.run(debug=True, port=5000)