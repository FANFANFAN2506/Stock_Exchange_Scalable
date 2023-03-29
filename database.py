from sqlalchemy import create_engine, Integer, Float, Column, String, ForeignKey, TEXT
from sqlalchemy.orm import declarative_base


def createTable(Base):

    class Account(Base):
        __tablename__ = 'account'

        id = Column(Integer, primary_key=True, autoincrement=True)
        Balance = Column(Float)

    class Position(Base):
        __tablename__ = 'position'

        uid = Column(Integer, ForeignKey('account.id'), primary_key=True)
        SYM = Column(TEXT, primary_key=True)
        AMT = Column(Integer, autoincrement=False)


def main():
    engine = create_engine('postgresql://postgres:passw0rd@localhost:5432/hw4')
    Base = declarative_base()
    # Check if connected to the database
    try:
        C_success = engine.connect()
        print('Opened database successfully')
        C_success.close()
    except Exception as e:
        print("Can't open database", e)

    # Drop all the tables
    Base.metadata.drop_all(engine)
    createTable(Base)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()
