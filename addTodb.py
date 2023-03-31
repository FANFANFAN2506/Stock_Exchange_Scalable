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


def addPosition(UID, symbol, num):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        # If the account doesn't exist
        checkIfAccountExist(session, UID)
        checkSymbolName(symbol)
        if num < 0:
            print(num)
            raise ValueError(
                "Creation failed: The number should be larger than 0")
        # check if the symbol already exist
        check_sym = session.query(Position).filter(
            Position.uid == UID).filter(Position.SYM == symbol).first()
        if check_sym is None:
            # The symbol doesn't exist, add a new one
            position = Position(uid=UID, SYM=symbol, AMT=num)
            session.add(position)
        else:
            # Else update the amount
            check_sym.AMT += num
        session.commit()
    except Exception as e:
        print(e)
    session.close()


def addTranscation(UID, SYMBOL, AMOUNT, PRICE):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        # If the account doesn't exist
        account = checkIfAccountExist(session, UID)

        if AMOUNT > 0:
            # We need to check the balance
            if account.Balance < AMOUNT * PRICE:
                raise ValueError(
                    "Create Transcation rejected: The remaining balance is not sufficient")
            account.Balance -= AMOUNT * PRICE
        else:
            # It is a sell order:
            if_position = session.query(Position).filter(
                Position.uid == UID).filter(Position.SYM == SYMBOL).first()
            if if_position is None:
                # The symbol doesn't exist
                raise ValueError(
                    "Create Transcation rejected: The symbol doesn't exist")
            else:
                if if_position.AMT < abs(AMOUNT):
                    # The remaining shares are not sufficient
                    raise ValueError(
                        "Create Transcation rejected: The remaining shares are insufficient")
                if_position.AMT += AMOUNT
        transaction = Transaction(uid=UID, SYM=SYMBOL, AMT=AMOUNT, LIMIT=PRICE)
        session.add(transaction)
        session.commit()
        status = Status(tid=transaction.tid, name='open',
                        shares=AMOUNT, price=PRICE, time=getCurrentTime())
        session.add(status)
        session.commit()
    except Exception as e:
        print(e)
    session.close()


def addStatus(TID, NAME, SHARES, PRICE, TIME):
    # When we need to add status, we need to check the id before call this function
    Session = sessionmaker(bind=engine)
    session = Session()
    status = Status(tid=TID, name=NAME, shares=SHARES, price=PRICE, time=TIME)
    session.add(status)
    session.commit()
    session.close()


def checkTIme(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    saved_time = session.query(Status).first()
    # Convert datetime into seconds since epocha
    print(int(saved_time.time.timestamp()))
