from typing import List
from sqlalchemy.orm import Mapped, mapped_column
from .extensions import db, Base

mechanic_ticket = db.Table(
    'mechanic_ticket',
    Base.metadata,
    db.Column('mechanic_id', db.ForeignKey('mechanics.id')),
    db.Column('ticket_id', db.ForeignKey('service_tickets.id'))
)

ticket_inventory = db.Table(
    'ticket_inventory',
    Base.metadata,
    db.Column('ticket_id', db.ForeignKey('service_tickets.id')),
    db.Column('inventory_id', db.ForeignKey('inventory.id'))
)

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)

    service_tickets: Mapped[List['ServiceTicket']] = db.relationship('ServiceTicket', back_populates='customer')

class Mechanic(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    salary: Mapped[float] = mapped_column(nullable=False)

    tickets: Mapped[List['ServiceTicket']] = db.relationship(secondary=mechanic_ticket, back_populates='mechanics')

class ServiceTicket(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(db.String(17), nullable=False)
    service_date: Mapped[str] = mapped_column(db.String(20), nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(255), nullable=False)
    customer_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'), nullable=True)

    mechanics: Mapped[List['Mechanic']] = db.relationship(secondary=mechanic_ticket, back_populates='tickets')
    parts: Mapped[List['Inventory']] = db.relationship(secondary=ticket_inventory, back_populates='tickets')
    customer: Mapped['User'] = db.relationship('User', back_populates='service_tickets')

class Inventory(Base):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(db.Float(), nullable=False)

    tickets: Mapped[List['ServiceTicket']] = db.relationship(secondary=ticket_inventory, back_populates='parts')

