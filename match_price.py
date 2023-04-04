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


def check_matching_order(session, uid, amount, symbol, limit):
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
                                         Transaction.limit < limit,
                                         Transaction.amount < 0,
                                         Status.name == 'open')
        match_order = match_order.order_by(
            Transaction.limit, Status.time).all()
    # if it is a sell order, matching order will be buy orders with limit higher than this sell order's limit
    else:
        match_order = match_order.filter(Transaction.symbol == symbol,
                                         Transaction.limit > limit,
                                         Transaction.amount > 0,
                                         Status.name == 'open')
        match_order = match_order.order_by(
            Transaction.limit.desc(), Status.time).all()
    # print("check match order")
    # print_matching_order(match_order)
    return match_order


def execute_match_order(session, match_order, current_order_sid):
    current_order = session.query(Status).filter(
        Status.sid == current_order_sid).first()
    # print("In total matching order", len(match_order))
    for order in match_order:
        if abs(order.shares) == abs(current_order.shares):
            match_order_status = session.query(Status).filter(
                Status.sid == order.sid).first()
            match_order_status.name = 'executed'
            match_order_status.time = getCurrentTime()
            current_order.name = 'executed'
            current_order.price = match_order_status.price
            current_order.time = getCurrentTime()
            session.commit()
            # print_current_symbol_status()
            break
        elif abs(order.shares) > abs(current_order.shares):
            match_order_status = session.query(Status).filter(
                Status.sid == order.sid).first()
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
            session.commit()
            # print_current_symbol_status()
            break
        else:
            match_order_status = session.query(Status).filter(
                Status.sid == order.sid).first()
            match_order_status.name = 'executed'
            match_order_status.time = getCurrentTime()
            current_order.shares += match_order_status.shares
            current_executed_status = Status(tid=current_order.tid,
                                             name='executed',
                                             shares=(-match_order_status.shares),
                                             price=match_order_status.price,
                                             time=getCurrentTime())
            session.add(current_executed_status)
            session.commit()
            # print_current_symbol_status()


def execute_order(session, uid, sym, amt, price):
    current_transaction = session.query(Transaction).filter(Transaction.uid == uid,
                                                            Transaction.symbol == sym,
                                                            Transaction.amount == amt,
                                                            Transaction.limit == price).first()
    # TODO: each transaction should only have one status with name open?
    current_order = session.query(Status).filter(
        Status.tid == current_transaction.tid, Status.name == 'open').first()

    if current_order is None:
        raise ValueError(
            "Cannot find current status")
    if current_order.name != 'open':
        # print(current_order.sid, current_order.tid, current_order.name,
        #       current_order.shares, current_order.price, current_order.time)
        raise ValueError(
            "Current order is not open")
    match_order = check_matching_order(
        session, current_transaction.uid, current_transaction.amount, current_transaction.symbol, current_transaction.limit)
    execute_match_order(session, match_order, current_order.sid)
    session.commit()
