from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine, MetaData, Table, select
from dbTable import *
from utils import *


def checkIfAccountExist(session, UID):
    # If the account doesn't exist
    account = session.query(Account).filter(Account.id == UID).first()
    if account is None:
        raise ValueError("Creation rejected: Account doesn't exist")
    return account


def checkSymbolName(symbol):
    if len(symbol) == 0 or symbol.isspace():
        raise ValueError("Rejected: Symbol shouldn't be empty")


def addAccount(ID, BALANCE):
    try:
        # Check if ID >= 1
        if ID < 1:
            raise ValueError(
                "Creation rejected: Account ID shouldn't be less than 1")
        if BALANCE < 0:
            raise ValueError(
                "Creation rejected: Account Balance shouldn't be negative")
        Session = sessionmaker(bind=engine)
        session = Session()

        # Check if ID exist:
        account = session.query(Account).filter(Account.id == ID).first()
        if account is not None:
            raise ValueError("Create rejected: Account ID exists")
        account = Account(id=ID, Balance=BALANCE)
        session.add(account)
        session.commit()
    except Exception as e:
        print(e)
    session.close()


def addPosition(account_ID, sym, num, engine):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()

        # If the account doesn't exist
        account = session.query(Account).filter(
            Account.id == account_ID).first()
        if account is None:
            raise ValueError("Create Symbol rejected: Account doesn't exist")

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
    except Exception as e:
        print(e)
    session.close()


def addTranscation(uid, sym, amt, price, engine):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        # If the account doesn't exist
        account = checkIfAccountExist(session, uid)

        if amt > 0:
            # We need to check the balance
            print(account.balance)
            if account.balance < amt * price:
                raise ValueError(
                    "Create Transcation rejected: The remaining balance is not sufficient")
            account.balance -= amt * price
        else:
            # It is a sell order:
            if_position = session.query(Position).filter(
                Position.uid == uid).filter(Position.symbol == sym).first()
            if if_position is None:
                # The symbol doesn't exist
                raise ValueError(
                    "Create Transcation rejected: The symbol doesn't exist")
            else:
                print(if_position.amount)
                if if_position.amount < abs(amt):
                    # The remaining shares are not sufficient
                    raise ValueError(
                        "Create Transcation rejected: The remaining shares are insufficient")
                if_position.amount += amt
        transaction = Transaction(uid=uid, symbol=sym, amount=amt, limit=price)
        session.add(transaction)
        session.commit()
        status = Status(tid=transaction.tid, name='open',
                        shares=amt, price=price, time=getCurrentTime())
        session.add(status)
        session.commit()
    except Exception as e:
        print(e)
    session.close()


def addStatus(tid, name, shares, price, time, engine):
    # When we need to add status, we need to check the id before call this function
    Session = sessionmaker(bind=engine)
    session = Session()
    status = Status(tid=tid, name=name, shares=shares, price=price, time=time)
    session.add(status)
    session.commit()
    session.close()


def checkTime(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    saved_time = session.query(Status).first()
    # Convert datetime into seconds since epocha
    print(int(saved_time.time.timestamp()))


def queryTransactions(tid, engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(Transaction.tid, Status.name, Status.shares,
                           Status.price, Status.time).filter(Transaction.tid == tid)
    result = result.all()


def cancelTransactions(TID, engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(Status).filter(
        Transaction.tid == TID, Status.name == 'open')
    for res in result:
        res.name = 'canceled'
    session.commit()
