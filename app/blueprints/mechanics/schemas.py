from app.extensions import ma, db
from app.models import Mechanic

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True
        sqla_session = db.session

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
