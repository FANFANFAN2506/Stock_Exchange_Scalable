from sqlalchemy import Integer, Float, Column, String, ForeignKey, TEXT, CHAR, TIMESTAMP
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
engine = create_engine(
    'postgresql://postgres:passw0rd@localhost:5432/hw4_568', poolclass=NullPool, isolation_level='SERIALIZABLE')
Base = declarative_base()


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True, autoincrement=False)
    balance = Column(Float)


class Position(Base):
    __tablename__ = 'position'

    uid = Column(Integer, ForeignKey('account.id'), primary_key=True)
    symbol = Column(TEXT, primary_key=True)
    amount = Column(Integer, autoincrement=False)


class Transaction(Base):
    __tablename__ = 'transaction'

    tid = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer, ForeignKey('account.id'))
    # Types could be checked using sign of amount
    # types = Column(CHAR(1))  # S for SELL, B for BUY
    # amount > 0 : buy order, amount < 0 : sell order
    amount = Column(Integer)
    limit = Column(Float)
    symbol = Column(TEXT)


class Status(Base):
    __tablename__ = 'status'

    sid = Column(Integer, primary_key=True, autoincrement=True)
    tid = Column(Integer, ForeignKey('transaction.tid'))
    name = Column(String)
    shares = Column(Integer)
    price = Column(Float, default=None, nullable=True)
    time = Column(TIMESTAMP, default=None, nullable=True)
