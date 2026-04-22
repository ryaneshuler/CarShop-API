from app.extensions import ma, db
from app.models import ServiceTicket
from marshmallow_sqlalchemy.fields import Nested

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        sqla_session = db.session
        include_relationships = True

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
