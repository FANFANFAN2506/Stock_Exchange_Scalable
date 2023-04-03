from datetime import datetime
import xml.etree.ElementTree as ET
from dbTable import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, Table, MetaData


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
@func: Print out all the accounts and their related positons
@param: {}
@return: {}
'''


def printAccountPosition():
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


def printOrderStatus():
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
