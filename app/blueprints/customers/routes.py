from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from app.blueprints.customers import customer_bp
from app.models import User, ServiceTicket
from app.extensions import db
from .schemas import customer_schema, customers_schema, login_schema
from app.utils.util import encode_token, token_required


@customer_bp.route('/', methods=['POST'])
def create_customer():
    try:
        customer = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.add(customer)
    db.session.commit()
    return customer_schema.jsonify(customer), 201


@customer_bp.route('/login', methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    email = credentials['email']
    password = credentials['password']

    query = select(User).where(User.email == email)
    customer = db.session.execute(query).scalar_one_or_none()

    if customer and customer.password == password:
        auth_token = encode_token(customer.id)
        response = {
            "status": "success",
            "message": "Successfully Logged In",
            "auth_token": auth_token
        }
        return jsonify(response), 200
    else:
        return jsonify({'message': "Invalid email or password"}), 401


@customer_bp.route('/my-tickets', methods=['GET'])
@token_required
def get_my_tickets(customer_id):
    query = select(ServiceTicket).where(ServiceTicket.customer_id == int(customer_id))
    tickets = db.session.execute(query).scalars().all()

    from app.blueprints.service_tickets.schemas import service_tickets_schema
    return service_tickets_schema.jsonify(tickets), 200


@customer_bp.route('/', methods=['GET'])
def get_customers():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        query = select(User)
        customers = db.paginate(query, page=page, per_page=per_page).items
        return customers_schema.jsonify(customers), 200
    except Exception:
        query = select(User)
        customers = db.session.execute(query).scalars().all()
        return customers_schema.jsonify(customers), 200


@customer_bp.route('/<int:customer_id>', methods=['PUT'])
@token_required
def update_customer(_token_customer_id, customer_id):
    customer = db.session.get(User, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    try:
        updates = customer_schema.load(request.json, instance=customer, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.commit()
    return customer_schema.jsonify(updates), 200


@customer_bp.route('/', methods=['DELETE'])
@token_required
def delete_customer(customer_id):
    customer = db.session.get(User, int(customer_id))
    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted customer {customer_id}"}), 200
