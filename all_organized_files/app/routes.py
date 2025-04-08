from flask import Blueprint, request, jsonify
from .models import Supplier, Good, Products, Order

routes_bp = Blueprint('routes', __name__)


def get_supplier(company_name):
    return Supplier.query.filter_by(company_name=company_name).first()


@routes_bp.route('/')
def home():
    return jsonify({"message": "ברוכים הבאים למערכת ניהול ספקים והזמנות!"})


@routes_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        if get_supplier(data['company_name']):
            return jsonify({'message': 'Supplier already exists'}), 400

        new_supplier = Supplier(
            company_name=data['company_name'],
            phone=data['phone'],
            representative=data.get('representative'),
        )

        db.session.add(new_supplier)
        db.session.commit()

        # for item in data['goods']:
        for item in data.get('goods', []):
            good = Good(
                name=item['name'],
                price=item['price'],
                min_quantity=item['min_quantity'],
                supplier_id=new_supplier.id
            )
            db.session.add(good)
        db.session.commit()

        return jsonify({'massage': 'supplier and goods registered successfully.'}), 201
    except Exception as e:
        app.logger.error(f"Error during registration: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500


@routes_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if get_supplier(data['company_name']):
        return jsonify({'message': 'Login succesful'}), 200
    else:
        return jsonify({'message': 'Supplier not found'}), 404


@routes_bp.route('/orders', methods=['GET'])
def view_orders_for_supplier():
    supplier_id = request.args.get('supplier_id')
    supplier = Supplier.query.get(supplier_id)

    if supplier:
        orders = Order.query.filter_by(supplier_id=supplier.id).all()
        orders_list = [order.convert_to_dict() for order in orders]

        return jsonify(orders_list), 200
    else:
        return jsonify({'message': 'Supplier not found'})


@routes_bp.route('/approve_order/<int:order_id>', methods=['PUT'])
def approve_order(order_id):
    order = Order.query.get(order_id)

    if order:
        order.status = 'In Process'
        db.session.commit()
        return jsonify({'message:': 'Order status updated to "In Process"'}), 200
    else:
        return jsonify({'message:''Order not found'}), 404


def order_goods(supplier, good_name, order_quantity, manual=False):
    good = None
    for item in supplier.goods:
        if item.name == good_name:
            good = item
            break
        if not good:
            return jsonify({'message': f"Good not found in supplier's offerings"}), 404

    if order_quantity < good.min_quantity and manual:
        return jsonify({'message': f"Order quantity must be at least {good.min_quantity}"}), 404
    elif order_quantity < good.min_quantity and not manual:
        order_quantity = good.min_quantity

    new_order = Order(
        supplier_id=supplier.id,
        product_name=good.name,
        quantity=order_quantity,
        status="pending"
    )
    db.session.add(new_order)
    db.session.commit()

    return new_order


@routes_bp.route('/order_goods', methods=['POST'])
def order_goods_manual():
    data = request.get_json()

    comany_name = data['company_name']
    good_name = data['good_name']
    order_quantity = data['order_quantity']

    supplier = get_supplier(comany_name)
    if not supplier:
        return jsonify({'message': 'Supplier not found'}), 404
    else:
        new_order = order_goods(supplier, good_name, order_quantity, manual=True)
        return jsonify({"message": "Order placed successfully", "order_id": new_order.id}), 201


@routes_bp.route('/confirm_order/<int:order_id>', methods=['PUT'])
def confirm_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"message": "Order not found"}), 404

    order.status = 'completed'
    db.session.commit()
    return jsonify({"message": f"Order {order_id} confirmed as completed"}), 200


@routes_bp.route('/current_orders', methods=['GET'])
def current_orders():
    orders = Order.query.filter(Order.status != "completed").all()

    order_list = [order.convert_to_dict() for order in orders]

    return jsonify(order_list), 200


@routes_bp.route('/all_orders', methods=['GET'])
def all_orders():
    orders = Order.query.all()
    orders_list = [order.convert_to_dict() for order in orders]

    return jsonify(orders_list), 200


def get_cheapest(product):  # returning cheapest supplier and cheapest good for a specific product
    cheap_good = (
        Good.query
        .filter_by(name=product.name)
        .order_by(Good.price.asc()).first()
    )

    if not cheap_good:
        return None

    supplier_id = cheap_good.supplier_id
    supplier = Supplier.query.get(supplier_id)

    return supplier, cheap_good


def order_goods_automatic(product):
    des_quantity = product.min_quantity - product.curr_quantity

    supplier, cheap_good = get_cheapest(product)

    order_quantity = des_quantity if des_quantity >= cheap_good.min_quantity else cheap_good.min_quantity

    new_order = order_goods(supplier.supplier_name, product.name, order_quantity)
    return new_order


@routes_bp.route('/purchase', methods=['POST'])
def add_purchase():
    data = request.get_json()

    for product_name, quantity in data:
        product = Products.query.get(product_name="product_name").first()
        product.current_quantity -= quantity
        db.session.commit()

        if product.current_quantity < product.min_quantity:
            new_order = order_goods_automatic(product)

            if not new_order:
                return jsonify({"message": "No suitable supplier found for this product."}), 400

            return jsonify({"message": "Order placed successfully",
                            "order_id": new_order.id,
                            "product": new_order.product_name,
                            "quantity": new_order.quantity}), 201
