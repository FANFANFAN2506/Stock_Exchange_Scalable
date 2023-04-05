from dbTable import *
from utils import *


def checkIfAccountExist(UID):
    session = Session()
    # If the account doesn't exist
    if int(UID) < 1:
        raise ValueError(
            "Account ID shouldn't be less than 1")
    # account = session.query(Account).filter(
    #     Account.id == UID).with_for_update().first()
    account = session.query(Account).filter(
        Account.id == UID).first()
    if account is None:
        session.close()
        raise ValueError("Account doesn't exist")
    session.close()
    # return account


def checkSymbolName(symbol):
    if len(symbol) == 0 or symbol.isspace():
        raise ValueError("Symbol shouldn't be empty")


def addAccount(ID, BALANCE):
    session1 = Session()
    # Make sure ID is larger and equal than 1
    if ID < 1:
        session1.close()
        raise ValueError(
            "Account ID shouldn't be less than 1")

    if BALANCE < 0:
        session1.close()
        raise ValueError(
            "Account Balance shouldn't be negative")
    # Check if ID exist:
    account = session1.query(Account).filter(Account.id == ID).first()
    if account is not None:
        session1.close()
        raise ValueError("Account ID exists")
    try:
        account = Account(id=ID, balance=BALANCE)
        session1.add(account)
        session1.commit()
        session1.close()
    except:
        session1.flush()
        session1.close()
        raise ValueError("Accounts exists")


def addPosition(account_ID, sym, num):
    session = Session()
    # If the account doesn't exist
    checkIfAccountExist(account_ID)
    if num < 0:
        session.close()
        raise ValueError("The position should be positive")
    # check if the symbol already exist
    try:
        check_sym = session.query(Position).filter(
            Position.uid == account_ID).filter(Position.symbol == sym).with_for_update().first()
        if check_sym is None:
            # The symbol doesn't exist, add a new one
            position = Position(uid=account_ID, symbol=sym, amount=num)
            session.add(position)
        else:
            # Else update the amount
            # new_amount = check_sym.amount + num
            # session.execute(update(Position).where(
            #     Position.uid == account_ID).filter(Position.symbol == sym).values(amount=new_amount))
            check_sym.amount += num
        session.commit()
        session.close()
    except:
        # traceback.print_exc()
        # print("rollback")
        session.rollback()
        session.close()


def addTranscation(uid, sym, amt, price):
    print("transaction start")
    session = Session()
    # If the account doesn't exist
    checkIfAccountExist(uid)

    if amt > 0:
        # It is a buy order
        # We need to check the balance
        session.commit()
        account = session.query(Account).filter(
            Account.id == uid).with_for_update().first()
        if account.balance < amt * price:
            session.commit()
            session.close()
            raise ValueError(
                "The remaining balance is not sufficient")
        account.balance -= amt * price
        session.commit()
    else:
        # It is a sell order:
        session.commit()
        if_position = session.query(Position).filter(
            Position.uid == uid).filter(Position.symbol == sym).with_for_update().first()
        if if_position is None:
            # The symbol doesn't exist
            session.commit()
            session.close()
            raise ValueError(
                "The symbol doesn't exist")
        else:
            if if_position.amount < abs(amt):
                # The remaining shares are not sufficient
                session.commit()
                session.close()
                raise ValueError(
                    "The remaining shares are insufficient")
            if_position.amount += amt
    print("about adding to transaction")
    transaction = Transaction(uid=uid, symbol=sym, amount=amt, limit=price)
    session.add(transaction)
    session.commit()
    construct_tid = transaction.tid
    status = Status(tid=transaction.tid, name='open',
                    shares=amt, price=price, time=getCurrentTime())
    session.add(status)
    session.commit()
    session.close()
    # return transaction.tid
    return construct_tid


def addStatus(session, tid, name, shares, price, time):
    # When we need to add status, we need to check the id before call this function
    status = Status(tid=tid, name=name, shares=shares, price=price, time=time)
    session.add(status)
    session.commit()
    # session.close()
