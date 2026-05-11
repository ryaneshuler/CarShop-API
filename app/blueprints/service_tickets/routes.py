from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.extensions import db
from app.models import ServiceTicket, Mechanic, Inventory, User
from . import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema


@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    try:
        ticket = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.add(ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 201


@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    tickets = db.session.execute(select(ServiceTicket)).scalars().all()
    return service_tickets_schema.jsonify(tickets), 200


@service_tickets_bp.route('/<int:ticket_id>', methods=['PUT'])
def update_service_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    try:
        ticket = service_ticket_schema.load(request.json, instance=ticket, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


@service_tickets_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    if mechanic in ticket.mechanics:
        return jsonify({"error": "Mechanic already assigned to this ticket."}), 400

    ticket.mechanics.append(mechanic)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


@service_tickets_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    if mechanic not in ticket.mechanics:
        return jsonify({"error": "Mechanic not assigned to this ticket."}), 400

    ticket.mechanics.remove(mechanic)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


@service_tickets_bp.route('/<int:ticket_id>/edit', methods=['PUT'])
def edit_ticket_mechanics(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    data = request.json or {}
    add_ids = data.get('add_ids', [])
    remove_ids = data.get('remove_ids', [])

    for mechanic_id in add_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)

    for mechanic_id in remove_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)

    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


@service_tickets_bp.route('/<int:ticket_id>/assign-customer/<int:customer_id>', methods=['PUT'])
def assign_customer(ticket_id, customer_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    customer = db.session.get(User, customer_id)

    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    ticket.customer_id = customer_id
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


@service_tickets_bp.route('/<int:ticket_id>/add-part/<int:inventory_id>', methods=['PUT'])
def add_part_to_ticket(ticket_id, inventory_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    part = db.session.get(Inventory, inventory_id)

    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    if not part:
        return jsonify({"error": "Inventory item not found."}), 404
    if part in ticket.parts:
        return jsonify({"error": "Part already added to this ticket."}), 400

    ticket.parts.append(part)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200

# remove part from ticket
@service_tickets_bp.route('/<int:ticket_id>/remove-part/<int:inventory_id>', methods=['PUT'])
def remove_part_from_ticket(ticket_id, inventory_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    part = db.session.get(Inventory, inventory_id)

    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    if not part:
        return jsonify({"error": "Inventory item not found."}), 404
    if part not in ticket.parts:
        return jsonify({"error": "Part not associated with this ticket."}), 400

    ticket.parts.remove(part)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200

# route for remove customer from ticket
@service_tickets_bp.route('/<int:ticket_id>/remove-customer', methods=['PUT'])
def remove_customer(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)

    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    ticket.customer_id = None
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200
