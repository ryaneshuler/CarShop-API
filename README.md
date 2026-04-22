# Car Shop API

A Flask REST API for a car/mechanic shop using the Application Factory Pattern.

## Project Structure

```
Car Shop API/
├── run.py
├── config.py
└── app/
    ├── __init__.py          # App factory, registers blueprints, creates tables
    ├── extensions.py        # db, ma, Base
    ├── models.py            # Mechanic, ServiceTicket, mechanic_ticket join table
    └── blueprints/
        ├── mechanics/
        │   ├── __init__.py  # mechanics_bp
        │   ├── routes.py    # POST /, GET /, PUT /<id>, DELETE /<id>
        │   └── schemas.py   # MechanicSchema
        └── service_tickets/
            ├── __init__.py  # service_tickets_bp
            ├── routes.py    # POST /, GET /, PUT assign/remove mechanic
            └── schemas.py   # ServiceTicketSchema
```

## Setup

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy
```

## Running the App

```bash
python run.py
```

The server runs on `http://127.0.0.1:5001` (port 5001 to avoid conflicts with other services).

The SQLite database (`car_shop.db`) is created automatically on first run inside the `instance/` folder.

## Endpoints

### Mechanics `/mechanics`

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/` | Create a new mechanic |
| GET | `/` | Get all mechanics |
| PUT | `/<id>` | Update a mechanic |
| DELETE | `/<id>` | Delete a mechanic |

### Service Tickets `/service-tickets`

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/` | Create a new service ticket |
| GET | `/` | Get all service tickets |
| PUT | `/<ticket_id>/assign-mechanic/<mechanic_id>` | Assign a mechanic to a ticket |
| PUT | `/<ticket_id>/remove-mechanic/<mechanic_id>` | Remove a mechanic from a ticket |
