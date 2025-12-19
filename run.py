import os
from app import create_app, db

# Get environment (development yoki production)
config_name = 'development'


# App yaratish
app = create_app(config_name)

"""
### Agar table ni bunday har bir run.py da 
yaratsak. "flask db migrate" ishlamaydi. 

# Database tables yaratish
# with app.app_context():
#     db.create_all()
#     print("Database tables created!")
"""
# Server run qilish
if __name__ == '__main__':
    app.run(debug=True, port=5000)