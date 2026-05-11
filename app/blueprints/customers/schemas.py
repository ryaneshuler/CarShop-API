from app.extensions import ma, db
from app.models import User
from marshmallow import fields


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        exclude = ('service_tickets',)


class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class EditCustomerSchema(ma.Schema):
    add_customer_ids = fields.List(fields.Int(), required=True)
    remove_customer_ids = fields.List(fields.Int(), required=True)


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_schema = LoginSchema()
edit_customer_schema = EditCustomerSchema()
