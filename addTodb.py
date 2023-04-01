from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine, MetaData, Table, select
from dbTable import *
from utils import *


def checkIfAccountExist(session, UID):
    # If the account doesn't exist
    if int(UID) < 1:
        raise ValueError(
            "Account ID shouldn't be less than 1")
    account = session.query(Account).filter(Account.id == UID).first()
    if account is None:
        raise ValueError("Account doesn't exist")
    return account


def checkSymbolName(symbol):
    if len(symbol) == 0 or symbol.isspace():
        raise ValueError("Symbol shouldn't be empty")


def addAccount(ID, BALANCE):
    # Make sure ID is larger and equal than 1
    if ID < 1:
        raise ValueError(
            "Account ID shouldn't be less than 1")

    if BALANCE < 0:
        raise ValueError(
            "Account Balance shouldn't be negative")
    Session = sessionmaker(bind=engine)
    session = Session()

    # Check if ID exist:
    account = session.query(Account).filter(Account.id == ID).first()
    if account is not None:
        raise ValueError("Account ID exists")
    account = Account(id=ID, balance=BALANCE)
    session.add(account)
    session.commit()
    session.close()


def addPosition(account_ID, sym, num):
    Session = sessionmaker(bind=engine)
    session = Session()

    # If the account doesn't exist
    checkIfAccountExist(session, account_ID)

    if num < 0:
        raise ValueError("The position should be positive")
    # check if the symbol already exist
    check_sym = session.query(Position).filter(
        Position.uid == account_ID).filter(Position.symbol == sym).first()
    if check_sym is None:
        # The symbol doesn't exist, add a new one
        position = Position(uid=account_ID, symbol=sym, amount=num)
        session.add(position)
    else:
        # Else update the amount
        check_sym.amount += num
    session.commit()
    session.close()


def addTranscation(uid, sym, amt, price):
    Session = sessionmaker(bind=engine)
    session = Session()

    # If the account doesn't exist
    account = checkIfAccountExist(session, uid)

    if amt > 0:
        # We need to check the balance
        if account.balance < amt * price:
            raise ValueError(
                "The remaining balance is not sufficient")
        account.balance -= amt * price
    else:
        # It is a sell order:
        if_position = session.query(Position).filter(
            Position.uid == uid).filter(Position.symbol == sym).first()
        if if_position is None:
            # The symbol doesn't exist
            raise ValueError(
                "The symbol doesn't exist")
        else:
            print(if_position.amount)
            if if_position.amount < abs(amt):
                # The remaining shares are not sufficient
                raise ValueError(
                    "The remaining shares are insufficient")
            if_position.amount += amt
    transaction = Transaction(uid=uid, symbol=sym, amount=amt, limit=price)
    session.add(transaction)
    session.commit()
    status = Status(tid=transaction.tid, name='open',
                    shares=amt, price=price, time=getCurrentTime())
    session.add(status)

    session.commit()
    session.close()


def addStatus(tid, name, shares, price, time):
    # When we need to add status, we need to check the id before call this function
    Session = sessionmaker(bind=engine)
    session = Session()
    status = Status(tid=tid, name=name, shares=shares, price=price, time=time)
    session.add(status)
    session.commit()
    session.close()


def checkTime():
    Session = sessionmaker(bind=engine)
    session = Session()

    saved_time = session.query(Status).first()
    # Convert datetime into seconds since epocha
    print(int(saved_time.time.timestamp()))
