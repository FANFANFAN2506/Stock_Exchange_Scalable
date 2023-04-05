from dbTable import *
from utils import *
from sqlalchemy.orm import sessionmaker


def print_matching_order(match_order):
    print("StatusID, TID, name, shares, price, time")
    for status in match_order:
        print(status.sid, status.tid, status.name,
              status.shares, status.price, status.time)
    print()


def print_current_symbol_status(session):
    symbol = 'X'
    all_transaction = session.query(Transaction).filter(
        Transaction.symbol == symbol)
    all_status = session.query(Status).filter(Status.tid == Transaction.tid,
                                              Transaction.symbol == symbol)
    # print("TransID, accountID, amount, limit, symbol")
    # for trans in all_transaction:
    #     print(trans.tid, trans.uid, trans.amount, trans.limit, trans.symbol)
    # print()
    print("StatusID, TID, name, shares, price, time")
    for status in all_status:
        print(status.sid, status.tid, status.name,
              status.shares, status.price, status.time)
    # session.close()

def print_Account(current_Account, match_Account):
    print("Current account")
    print("AccountID, balance")
    print(current_Account.id, current_Account.balance)
    print("Match account")
    print("AccountID, balance")
    print(match_Account.id, match_Account.balance)

def print_Account_Positon(current_Account, current_Position, match_Account, match_Position):
    print_Account(current_Account, match_Account)
    print("Current Position")
    if not current_Position is None:
        print("PositionID, symbol, amount")
        print(current_Position.uid, current_Position.symbol, current_Position.amount)
    print("Match position")
    if not match_Position is None:
        print("PositionID, symbol, amount")
        print(match_Position.uid, match_Position.symbol, match_Position.amount)
    print()
    

def check_matching_order(uid, amount, symbol, limit):
    session = Session()
    match_order = session.query(Status).join(
        Transaction).filter(Status.tid == Transaction.tid)
    # print("before matching")
    # print_matching_order(match_order)
    if amount == 0:
        raise ValueError(
            "Order amount cannot be 0")
    # if it is a buy order, matching order will be sell orders with limit lower than this buy order's limit
    elif amount > 0:
        match_order = match_order.filter(Transaction.symbol == symbol,
                                         Transaction.limit <= limit,
                                         Transaction.amount < 0,
                                         Status.name == 'open').with_for_update()
        match_order = match_order.order_by(
            Transaction.limit, Status.time).all()
    # if it is a sell order, matching order will be buy orders with limit higher than this sell order's limit
    else:
        match_order = match_order.filter(Transaction.symbol == symbol,
                                         Transaction.limit >= limit,
                                         Transaction.amount > 0,
                                         Status.name == 'open').with_for_update()
        match_order = match_order.order_by(
            Transaction.limit.desc(), Status.time).all()
    # print("check match order")
    # print_matching_order(match_order)
    session.close()
    return match_order


def execute_match_order(match_order, current_order_sid):
    session = Session()
    current_order = session.query(Status).filter(
        Status.sid == current_order_sid).with_for_update().first()
    current_transaction = session.query(Transaction).filter(
        Transaction.tid == current_order.tid).first()
    current_Account = session.query(Account).filter(
        Account.id == current_transaction.uid).with_for_update().first()
    current_position = session.query(Position).filter(Position.uid==current_Account.id,
                                                    Position.symbol==current_transaction.symbol).with_for_update().first()
    # if current_order.shares > 0:
    #     print("current balance ", current_Account.balance)
    # print("In total matching order", len(match_order))
    for order in match_order:
        match_transaction = session.query(Transaction).filter(
            Transaction.tid == order.tid).first()
        match_Account = session.query(Account).filter(
            Account.id == match_transaction.uid).with_for_update().first()
        match_position = session.query(Position).filter(Position.uid==match_Account.id,
                                                                  Position.symbol==match_transaction.symbol).with_for_update().first()
        print("before execute")
        print_Account_Positon(current_Account, current_position, match_Account, match_position)
        if abs(order.shares) == abs(current_order.shares):
            match_order_status = session.query(Status).filter(
                Status.sid == order.sid).with_for_update().first()
            match_order_status.name = 'executed'
            match_order_status.time = getCurrentTime()
            current_order.name = 'executed'
            current_order.price = match_order_status.price
            current_order.time = getCurrentTime()

            #modify position and refund for account balance for buyer
            if(current_order.shares > 0):
                current_Account.balance -= (match_order_status.price -
                                            current_transaction.limit) * abs(current_order.shares)
                if current_position is None:
                    addPosition(current_Account.id, current_transaction.symbol, abs(current_order.shares))
                else:
                    current_position.amount += abs(current_order.shares)
            #modify account balance for seller
            else:
                current_Account.balance += match_order_status.price * abs(current_order.shares)
                if match_position is None:
                    addPosition(match_Account.id, current_transaction.symbol, abs(current_order.shares))
                else:
                    match_position.amount += abs(current_order.shares)

            # print("current balance ", current_Account.balance)
            session.commit()
            print("after execute")
            print_current_symbol_status(session)
            print_Account_Positon(current_Account, current_position, match_Account, match_position)
            break
        elif abs(order.shares) > abs(current_order.shares):
            match_order_status = session.query(Status).filter(
                Status.sid == order.sid).with_for_update().first()
            match_order_status.shares += current_order.shares
            match_executed_status = Status(tid=match_order_status.tid,
                                           name='executed',
                                           shares=(-current_order.shares),
                                           price=match_order_status.price,
                                           time=getCurrentTime())
            session.add(match_executed_status)
            current_order.name = 'executed'
            current_order.price = match_order_status.price
            current_order.time = getCurrentTime()
            #modify position and refund for account balance for buyer
            if(current_order.shares > 0):
                current_Account.balance -= (match_order_status.price -
                                            current_transaction.limit) * abs(current_order.shares)
                if current_position is None:
                    addPosition(current_Account.id, current_transaction.symbol, abs(current_order.shares))
                else:
                    current_position.amount += abs(current_order.shares)
            #modify account balance for seller
            else:
                current_Account.balance += match_order_status.price * abs(current_order.shares)
                if match_position is None:
                    addPosition(match_Account.id, current_transaction.symbol, abs(current_order.shares))
                else:
                    match_position.amount += abs(current_order.shares)

                # print("current balance ", current_Account.balance)
            session.commit()
            print("after execute")
            print_Account_Positon(current_Account, current_position, match_Account, match_position)
            print_current_symbol_status(session)
            break
        else:
            match_order_status = session.query(Status).filter(
                Status.sid == order.sid).with_for_update().first()
            match_order_status.name = 'executed'
            match_order_status.time = getCurrentTime()
            current_order.shares += match_order_status.shares
            current_executed_status = Status(tid=current_order.tid,
                                             name='executed',
                                             shares=(-match_order_status.shares),
                                             price=match_order_status.price,
                                             time=getCurrentTime())
            if(current_order.shares > 0):
                current_Account.balance -= (match_order_status.price -
                                            current_transaction.limit) * abs(match_order_status.shares)
                if current_position is None:
                    addPosition(current_Account.id, current_transaction.symbol, abs(match_order_status.shares))
                else:
                    current_position.amount += abs(current_order.shares)
            #modify account balance for seller
            else:
                current_Account.balance += match_order_status.price * abs(match_order_status.shares)
                if match_position is None:
                    addPosition(match_Account.id, current_transaction.symbol, abs(match_order_status.shares))
                else:
                    match_position.amount += abs(match_order_status.shares)
                # print("current balance ", current_Account.balance)
            session.add(current_executed_status)
            session.commit()
            print("after execute")
            print_Account_Positon(current_Account, current_position, match_Account, match_position)
            print_current_symbol_status(session)
    session.close()


def execute_order(tid):
    session = Session()
    current_transaction = session.query(
        Transaction).filter(Transaction.tid == tid).first()
    # TODO: each transaction should only have one status with name open?
    current_order = session.query(Status).filter(
        Status.tid == current_transaction.tid, Status.name == 'open').first()
    # print(current_order.sid, current_order.tid, current_order.name)
    if current_order is None:
        raise ValueError(
            "Cannot find current status")
    if current_order.name != 'open':
        # print(current_order.sid, current_order.tid, current_order.name,
        #       current_order.shares, current_order.price, current_order.time)
        raise ValueError(
            "Current order is not open")
    match_order = check_matching_order(
        current_transaction.uid, current_transaction.amount, current_transaction.symbol, current_transaction.limit)
    execute_match_order(match_order, current_order.sid)
    session.commit()
    session.close()
