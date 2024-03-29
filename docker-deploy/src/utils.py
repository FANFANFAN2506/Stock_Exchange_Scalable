from datetime import datetime
import xml.etree.ElementTree as ET
from dbTable import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, Table, MetaData
'''
@func: Drop all the tables
'''


def init_Engine():
    Base.metadata.drop_all(engine)
    print('Drop tables successfully')
    Base.metadata.create_all(engine)


def createEngine():
    Base.metadata.drop_all(engine)
    print('Drop tables successfully')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


'''
@func: Get current time
'''


def getCurrentTime():
    current_time = datetime.now()
    time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
    return time_str


'''
* @func: Construct an element node
* @param: {Msg, **attributes} Msg is the message, attributes are a set of key-value pair
* @return: {child_node} node to be append
'''


def construct_node(Name, Msg, **attributes):
    child_node = ET.Element(Name)
    if Msg:
        child_node.text = Msg
    for key, value in attributes.items():
        child_node.set(key, value)
    return child_node


''' 
@func: Construct a <create> request for client
@param: uid: user account id wants to create;
        balance: The balance for this user
        position: {symbol:num, symbol:num}The position to be added to the specified account 
@return: <create> request encoded in utf-8
'''


def createRequest(uid, balance, position):
    uid = str(uid)
    balance = str(balance)
    root = ET.Element("create")
    account_node = ET.Element("account")
    account_node.set("id", uid)
    account_node.set("balance", balance)
    root.append(account_node)
    for sym, num in position.items():
        sym = str(sym)
        num = str(num)
        symbol_node = construct_node("symbol", None, **{"sym": sym, })
        symbol_node.append(construct_node(
            "account", num, **{"id": uid, }))
        root.append(symbol_node)
    request = str(len(ET.tostring(root))) + "\n" + \
        str(ET.tostring(root).decode())
    return request.encode("utf-8")


''' 
@func: Construct a <transaction> request for client
@param: uid: user account id to query;
        order: a set of order tuples including sym, amt, limit [(s1,a1,l1),(s2, a2,l2)]
        query: a set of query tuples, including the transaction id, [1,2,3,4]
        cancle: a set of cancel tuples, including the transaction id, [1,2,3,4]
@return: <transaction> request encoded in utf-8
'''


def transactionRequest(uid, order, query, cancel):
    uid = str(uid)
    root = ET.Element("transactions")
    root.set("id", uid)
    if order:
        for sym, amt, limit in order:
            root.append(construct_node("order", None, **
                        {"sym": str(sym), "amount": str(amt), "limit": str(limit)}))
    if query:
        for tid in query:
            root.append(construct_node("query", None, **{"id": str(tid), }))
    if cancel:
        for tid in cancel:
            root.append(construct_node("cancel", None, **{"id": str(tid), }))
    request = str(len(ET.tostring(root))) + "\n" + \
        str(ET.tostring(root).decode())
    return request.encode("utf-8")


'''
@func: Print out all the accounts and their related positons
@param: {}
@return: {}
'''


def printAccountPosition(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    metadata = MetaData()
    account_table = Table('account', metadata, autoload_with=engine)
    position_table = Table('position', metadata, autoload_with=engine)
    query = select(account_table.c.id, account_table.c.balance, position_table.c.symbol, position_table.c.amount).select_from(
        account_table.join(position_table, account_table.c.id == position_table.c.uid)).order_by(account_table.c.id)
    result = session.execute(query).fetchall()
    print("id | balance| symbol | amount")
    for row in result:
        for value in row:
            print(value, end=" ")
        print()
    session.close()


def printquery(session, query):
    result = session.execute(query).fetchall()
    for row in result:
        for value in row:
            print(value, end=" ")
        print()


def printOrderStatus(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    metadata = MetaData()
    order_table = Table('transaction', metadata, autoload_with=engine)
    status_table = Table('status', metadata, autoload_with=engine)
    query = select(order_table.c.tid, order_table.c.uid, order_table.c.amount, order_table.c.limit, order_table.c.symbol, status_table.c.sid,
                   status_table.c.name, status_table.c.shares, status_table.c.price, status_table.c.time).select_from(order_table.join(status_table, order_table.c.tid == status_table.c.tid))

    print("tid | uid | amount | limit | symbol | sid |  name   | shares | price | time ")
    print("open orders:")
    print("sell orders:")
    sell_order = query.filter(status_table.c.name == 'open').filter(order_table.c.amount < 0).order_by(
        order_table.c.limit.desc())
    printquery(session, sell_order)
    print("buy orders:")
    buy_order = query.filter(status_table.c.name == 'open').filter(order_table.c.amount > 0).order_by(
        order_table.c.limit.asc())
    printquery(session, buy_order)
    print("Executed orders:")
    executed_order = query.filter(status_table.c.name == 'executed')
    printquery(session, executed_order)
    print("Canceled orders:")
    cancel_order = query.filter(status_table.c.name == 'canceled')
    printquery(session, cancel_order)
    session.close()


if __name__ == "__main__":
    # def transactionRequest(uid, order, query, cancel):
    print(createRequest(1, 2000, {"TELSA": 2000, "X": 1000}))
    # print(transactionRequest(
    #     1, [("TELSA", 10, 10), ("X", -10, 5)], [1, 2], [1, 2]))
