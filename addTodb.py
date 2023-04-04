from match_price import *
from dbTable import *
from utils import *


def checkIfAccountExist(session, UID):
    # If the account doesn't exist
    if int(UID) < 1:
        raise ValueError(
            "Account ID shouldn't be less than 1")
    # account = session.query(Account).filter(
    #     Account.id == UID).with_for_update().first()
    account = session.query(Account).filter(
        Account.id == UID).first()
    if account is None:
        raise ValueError("Account doesn't exist")
    # return account


def checkSymbolName(symbol):
    if len(symbol) == 0 or symbol.isspace():
        raise ValueError("Symbol shouldn't be empty")


def addAccount(ID, BALANCE):
    session1 = Session()
    # Make sure ID is larger and equal than 1
    if ID < 1:
        raise ValueError(
            "Account ID shouldn't be less than 1")

    if BALANCE < 0:
        raise ValueError(
            "Account Balance shouldn't be negative")
    # Check if ID exist:
    account = session1.query(Account).filter(Account.id == ID).first()
    if account is not None:
        raise ValueError("Account ID exists")
    try:
        account = Account(id=ID, balance=BALANCE)
        session1.add(account)
        session1.commit()
        session1.close()
    except:
        session1.flush()
        raise ValueError("Accounts exists")


def addPosition(session, account_ID, sym, num):
    session1 = Session()
    # If the account doesn't exist
    checkIfAccountExist(session1, account_ID)
    if num < 0:
        raise ValueError("The position should be positive")
    # check if the symbol already exist
    try:
        check_sym = session1.query(Position).filter(
            Position.uid == account_ID).filter(Position.symbol == sym).with_for_update().first()
        if check_sym is None:
            # The symbol doesn't exist, add a new one
            position = Position(uid=account_ID, symbol=sym, amount=num)
            session1.add(position)
        else:
            # Else update the amount
            # new_amount = check_sym.amount + num
            # session.execute(update(Position).where(
            #     Position.uid == account_ID).filter(Position.symbol == sym).values(amount=new_amount))
            check_sym.amount += num
        session1.commit()
        session1.close()
    except:
        print("rollback")
        session1.rollback()
        session1.close()


def addTranscation(uid, sym, amt, price):
    session = Session()
    # If the account doesn't exist
    checkIfAccountExist(session, uid)

    if amt > 0:
        # It is a buy order
        # We need to check the balance
        account = session.query(Account).filter(
            Account.id == uid).with_for_update().first()
        if account.balance < amt * price:
            raise ValueError(
                "The remaining balance is not sufficient")
        account.balance -= amt * price
    else:
        # It is a sell order:
        if_position = session.query(Position).filter(
            Position.uid == uid).filter(Position.symbol == sym).with_for_update().first()
        if if_position is None:
            # The symbol doesn't exist
            raise ValueError(
                "The symbol doesn't exist")
        else:
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
    execute_order(session, int(uid), sym, int(
        amt), float(price))
    session.close()


def addStatus(session, tid, name, shares, price, time):
    # When we need to add status, we need to check the id before call this function
    status = Status(tid=tid, name=name, shares=shares, price=price, time=time)
    session.add(status)
    session.commit()
    # session.close()
