from flask import Blueprint, jsonify, request
from datetime import date
from . import db
from .models import Product, Location, ProductMovement, Summary
import uuid

main = Blueprint('main', __name__)

@main.route('/products')
def products():
    product_list = Product.query.all()
    products = []
    for product in product_list:
        products.append({'id':product.product_id, 'name':product.product_name})
    return jsonify({'products': products})

@main.route('/products', methods=['POST'])
def add_products():
    product_data = request.get_json()
    new_product = Product(product_id=product_data['id'], product_name=product_data['name'])
    db.session.add(new_product)
    db.session.commit()
    return 'Adding products Done'

@main.route('/products', methods=['PUT'])
def edit_products():
    product = Product.query.filter_by(product_id='bnudb6rr').first()
    product.product_name= 'glasses'
    db.session.commit()
    return jsonify({'name':product.product_name})

@main.route('/locations')
def locations():
    location_list = Location.query.all()
    locations = []
    for location in location_list:
        locations.append({'id':location.location_id, 'name':location.location_name})
    return jsonify({'locations': locations})

@main.route('/locations', methods=['POST'])
def add_locations():
    location_data = request.get_json()
    new_location = Location(location_id=location_data['id'], location_name=location_data['name'])
    db.session.add(new_location)
    db.session.commit()
    return 'Adding locations Done'

@main.route('/locations', methods=['PUT'])
def edit_locations():
    location = Location.query.filter_by(location_name='C').first()
    # lid = location.location_id
    location.location_id='ubhfbfiuhf'
    db.session.commit()
    # movement = ProductMovement.query.filter_by(from_location=lid).first()
    # movement.from_location= location.location_id='rbfjrebf'
    
    return jsonify({'name':location.location_name})

@main.route('/product-movement')
def movemment():
    movement_list = ProductMovement.query.all()
    movements = []
    for movement in movement_list:
        movements.append({'id':movement.movement_id,
                            'timestamp': movement.timestamp,
                            'from': movement.from_location,
                            'to': movement.to_location,
                            'product_id': movement.product_id,
                            'quantity': movement.qty})
    return jsonify({'movements': movements})

@main.route('/product-movement', methods=['POST'])
def add_movement():
    movement_data = request.get_json()
    if movement_data["from"] == "":
        movement_data['from']=None
    if movement_data["to"] == "":
        movement_data['to']=None
    new_movement = ProductMovement(movement_id=movement_data['id'], 
                                    timestamp=date.today(), 
                                    from_location=movement_data['from'], 
                                    to_location=movement_data['to'], 
                                    product_id=movement_data['product_id'], 
                                    qty=movement_data['quantity'])
    report = Summary.query.filter_by(product_id=movement_data['product_id']).all()
    # print(report)    
    if report== [] and movement_data['to']!= None:
        print('yele idiot')
        new_report = Summary(report_id=str(uuid.uuid1()), product_id=movement_data['product_id'], warehouse=movement_data['to'], qty = movement_data['quantity'])
        db.session.add(new_report)
    
    else:
        for i in range(len(report)):
            destination = report[i].warehouse
            if movement_data['from']==destination:
                report[i].qty = report[i].qty-int(movement_data['quantity'])
            elif movement_data['to']==destination:
                report[i].qty = report[i].qty+int(movement_data['quantity'])
            else:
                new_report = Summary(report_id=str(uuid.uuid1()), product_id=movement_data['product_id'], warehouse=movement_data['to'], qty = movement_data['quantity'])
                db.session.add(new_report)

    
    db.session.add(new_movement)
    db.session.commit()
    return 'Adding movements Done'

@main.route('/product-movement', methods=['PUT'])
def edit_movements():
    move = ProductMovement.query.filter_by(movement_id='rjrtno').first()
    move.movement_id = 'iuehfurf78'
    db.session.commit()
    return jsonify({'pid':move.from_location, 'id':move.movement_id})
    # return 'Movement updated'

@main.route('/summary')
def summary():
    report_list = Summary.query.all()
    reports = []
    for report in report_list:
        reports.append({'id':report.report_id,
                            'pid':report.product_id,
                            'warehouse':report.warehouse,
                            'quantity':report.qty,
                        })
    return jsonify({'report': reports})