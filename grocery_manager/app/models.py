from . import db


class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    representative = db.Column(db.String(100))

    goods = db.relationship('Good', backref='supplier', cascade="all,delete-orphan", lazy=True)
    orders = db.relationship('Order', backref='supplier_order', lazy=True)


class Good(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    min_quantity = db.Column(db.Integer, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    current_quantity = db.Column(db.Integer, nullable=False)
    min_quantity = db.Column(db.Integer, nullable=False)


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    product_name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')

    supplier = db.relationship('Supplier', backref=db.backref('his_orders', lazy=True))

    def convert_to_dict(self):
        return {
            'id': self.id,
            'supplier_id': self.supplier_id,
            'product_name': self.product_name,
            'quantity': self.quantity,
            'status': self.status
        }
