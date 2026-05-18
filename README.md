# Car Shop API

A Flask REST API for a car/mechanic shop using the Application Factory Pattern, deployed on Render with a CI/CD pipeline via GitHub Actions.

## Live API

Base URL: `https://carshop-api-nzlc.onrender.com`

Interactive Swagger docs: `https://carshop-api-nzlc.onrender.com/docs`

## Project Structure

```
Car Shop API/
├── flask_app.py             # App entry point (ProductionConfig)
├── config.py                # DevelopmentConfig, TestingConfig, ProductionConfig
├── requirements.txt         # Python dependencies
├── .env                     # Local environment variables (not committed)
├── .gitignore
├── .github/
│   └── workflows/
│       └── main.yaml        # CI/CD pipeline (build → test → deploy)
├── tests/
│   ├── test_customers.py
│   ├── test_mechanics.py
│   ├── test_servicetickets.py
│   └── test_inventory.py
└── app/
    ├── __init__.py          # App factory, registers blueprints, creates tables
    ├── extensions.py        # db, ma, limiter, cache
    ├── models.py            # User, Mechanic, ServiceTicket, Inventory, join tables
    ├── static/
    │   └── swagger.yaml     # OpenAPI 2.0 documentation
    ├── utils/
    │   └── util.py          # JWT encode_token(), token_required decorator
    └── blueprints/
        ├── customers/
        │   ├── __init__.py  # customer_bp
        │   ├── routes.py    # POST /, POST /login, GET /, GET /my-tickets, PUT /<id>, DELETE /
        │   └── schemas.py   # CustomerSchema, LoginSchema
        ├── mechanics/
        │   ├── __init__.py  # mechanics_bp
        │   ├── routes.py    # POST /, GET /, GET /most-worked, PUT /<id>, DELETE /<id>
        │   └── schemas.py   # MechanicSchema
        ├── service_tickets/
        │   ├── __init__.py  # service_tickets_bp
        │   ├── routes.py    # POST /, GET /, PUT /<id>, assign/remove mechanic, assign/remove customer, add/remove part
        │   └── schemas.py   # ServiceTicketSchema
        └── inventory/
            ├── __init__.py  # inventory_bp
            ├── routes.py    # POST /, GET /, GET /<id>, PUT /<id>, DELETE /<id>
            └── schemas.py   # InventorySchema
```

## Local Setup

**1. Activate virtual environment**

Mac:
```bash
source "venv (Mac)/bin/activate"
```

Windows:
```bash
& "venv (PC)/Scripts/Activate.ps1"
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Create a `.env` file in the project root**

```
SQLALCHEMY_DATABASE_URI=your_database_uri_here
SECRET_KEY=your_secret_key_here
```

**4. Run locally**

```bash
python flask_app.py
```

The server runs on `http://127.0.0.1:5000`.

## Production Deployment

The app is deployed on Render using Gunicorn:

```bash
gunicorn flask_app:app
```

Environment variables (`SQLALCHEMY_DATABASE_URI` and `SECRET_KEY`) are configured in the Render dashboard.

## CI/CD Pipeline

Every push to the `Main` branch triggers the GitHub Actions workflow (`.github/workflows/main.yaml`):

1. **build** — checks out the code
2. **test** — installs dependencies and runs the full test suite
3. **deploy** — deploys to Render (requires `SERVICE_ID` and `RENDER_API_KEY` GitHub secrets)

## API Documentation

Interactive Swagger UI docs:

```
https://carshop-api-nzlc.onrender.com/docs
```

## Authentication

Protected routes require a JWT token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Obtain a token by logging in at `POST /customers/login`. Tokens expire after 1 hour.

## Endpoints

### Customers `/customers`

| Method | Route            | Auth Required | Description                                      |
| ------ | ---------------- | :-----------: | ------------------------------------------------ |
| POST   | `/`              |      No       | Create a new customer                            |
| POST   | `/login`         |      No       | Login — returns JWT token                        |
| GET    | `/`              |      No       | Get all customers (supports `?page=&per_page=`)  |
| GET    | `/my-tickets`    |      Yes      | Get the authenticated customer's service tickets |
| PUT    | `/<customer_id>` |      Yes      | Update a customer                                |
| DELETE | `/`              |      Yes      | Delete the authenticated customer                |

### Mechanics `/mechanics`

| Method | Route          | Auth Required | Description                                          |
| ------ | -------------- | :-----------: | ---------------------------------------------------- |
| POST   | `/`            |      No       | Create a new mechanic                                |
| GET    | `/`            |      No       | Get all mechanics (rate limited: 100/hr, cached 60s) |
| GET    | `/most-worked` |      No       | Get mechanics sorted by number of tickets            |
| PUT    | `/<id>`        |      No       | Update a mechanic                                    |
| DELETE | `/<id>`        |      No       | Delete a mechanic                                    |

### Service Tickets `/service-tickets`

| Method | Route                                        | Auth Required | Description                                          |
| ------ | -------------------------------------------- | :-----------: | ---------------------------------------------------- |
| POST   | `/`                                          |      No       | Create a new service ticket                          |
| GET    | `/`                                          |      No       | Get all service tickets                              |
| PUT    | `/<ticket_id>`                               |      No       | Update a service ticket                              |
| PUT    | `/<ticket_id>/assign-mechanic/<mechanic_id>` |      No       | Assign a mechanic to a ticket                        |
| PUT    | `/<ticket_id>/remove-mechanic/<mechanic_id>` |      No       | Remove a mechanic from a ticket                      |
| PUT    | `/<ticket_id>/edit`                          |      No       | Batch add/remove mechanics (`add_ids`, `remove_ids`) |
| PUT    | `/<ticket_id>/assign-customer/<customer_id>` |      No       | Assign a customer to a ticket                        |
| PUT    | `/<ticket_id>/remove-customer`               |      No       | Remove the customer from a ticket                    |
| PUT    | `/<ticket_id>/add-part/<inventory_id>`       |      No       | Add an inventory part to a ticket                    |
| PUT    | `/<ticket_id>/remove-part/<inventory_id>`    |      No       | Remove an inventory part from a ticket               |

### Inventory `/inventory`

| Method | Route        | Auth Required | Description       |
| ------ | ------------ | :-----------: | ----------------- |
| POST   | `/`          |      No       | Create a new part |
| GET    | `/`          |      No       | Get all parts     |
| GET    | `/<part_id>` |      No       | Get a single part |
| PUT    | `/<part_id>` |      No       | Update a part     |
| DELETE | `/<part_id>` |      No       | Delete a part     |

## Running Tests

With the virtual environment activated, run all tests from the project root:

```bash
python -m unittest discover tests
```

Or run a single test file:

```bash
python -m unittest tests/test_customers.py
```