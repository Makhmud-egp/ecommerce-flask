from app import db
from datetime import datetime


class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='cart_items')
    product = db.relationship('Product', backref='cart_items')

    # Unique constraint: bir user bir productni faqat 1 marta qo'shadi
    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='unique_user_product'),
    )

    @property
    def subtotal(self):
        """Bu item ning total narxi"""
        return float(self.product.price) * self.quantity

    def to_dict(self):
        return {
            'id': self.id,
            'product': self.product.to_dict(),
            'quantity': self.quantity,
            'subtotal': self.subtotal
        }

    def __repr__(self):
        return f'<CartItem User:{self.user_id} Product:{self.product_id}>'