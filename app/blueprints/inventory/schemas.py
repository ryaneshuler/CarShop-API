from app.extensions import ma, db
from app.models import Inventory


class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True
        sqla_session = db.session


inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)
