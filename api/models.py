from . import db
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import relationship

class Product(db.Model):
    product_id = db.Column(db.String, primary_key=True)
    product_name = db.Column(db.String)
    productmovements = db.relationship("ProductMovement", cascade="all, delete", backref='product', lazy=True)

class Location(db.Model):
    location_id = db.Column(db.String, primary_key=True)
    location_name = db.Column(db.String, nullable=False)
    productmovements_from = db.relationship("ProductMovement", cascade="all,delete", backref='f_location', lazy=True, foreign_keys = 'ProductMovement.from_location')
    productmovements_to = db.relationship("ProductMovement", cascade="all, delete", backref='t_location', lazy=True, foreign_keys = 'ProductMovement.to_location')


class ProductMovement(db.Model):
    movement_id = db.Column(db.String, primary_key=True)
    timestamp = db.Column(db.Date)
    from_location = db.Column(db.String, 
                    db.ForeignKey('location.location_id'), 
                    nullable=True)
    to_location = db.Column(db.String, 
                            db.ForeignKey('location.location_id'), 
                            nullable=True)
    product_id = db.Column(db.String, 
                            db.ForeignKey('product.product_id'), 
                            nullable=False)
    qty = db.Column(db.Integer, nullable=False)

class Summary(db.Model):
    report_id = db.Column(db.String, primary_key=True)
    product_id = db.Column(db.String)
    warehouse = db.Column(db.String)
    qty = db.Column(db.Integer)
