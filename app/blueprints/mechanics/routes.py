from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select, func
from app.extensions import db, limiter, cache
from app.models import Mechanic, mechanic_ticket
from . import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema


@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    try:
        mechanic = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.add(mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 201


@mechanics_bp.route('/', methods=['GET'])
@limiter.limit("100 per hour")
@cache.cached(timeout=60)
def get_mechanics():
    mechanics = db.session.execute(select(Mechanic)).scalars().all()
    return mechanics_schema.jsonify(mechanics), 200


@mechanics_bp.route('/most-worked', methods=['GET'])
def most_worked_mechanics():
    query = (
        select(Mechanic)
        .outerjoin(mechanic_ticket, Mechanic.id == mechanic_ticket.c.mechanic_id)
        .group_by(Mechanic.id)
        .order_by(func.count(mechanic_ticket.c.ticket_id).desc())
    )
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics), 200


@mechanics_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    try:
        mechanic = mechanic_schema.load(request.json, instance=mechanic, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


@mechanics_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic {id} deleted successfully."}), 200
