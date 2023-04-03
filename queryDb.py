from dbTable import *
from utils import construct_node
import xml.etree.ElementTree as ET
from sqlalchemy.orm import sessionmaker


def query_status(node, order):
    for tuple in order:
        if tuple.name == 'open':
            attributes = {'shares': str(abs(tuple.shares))}
            node.append(construct_node('open', None, **attributes))
        elif tuple.name == 'canceled':
            attributes = {'shares': str(abs(tuple.shares)),
                          'time': str(tuple.time.timestamp())}
            node.append(construct_node(
                'canceled', None, **attributes))
        else:
            attributes = {'shares': str(abs(tuple.shares)),
                          'price': str(tuple.price), 'time': str(tuple.time.timestamp())}
            node.append(construct_node(
                'executed', None, **attributes))


def query_transcation(UID, TID):
    status_node = ET.Element("status")
    status_node.set('id', str(TID))
    Session = sessionmaker(bind=engine)
    session = Session()
    order = session.query(Status).join(Transaction).join(Account).filter(
        Account.id == UID).filter(Transaction.tid == TID).order_by(Status.sid.asc())
    if order.count() == 0:
        Msg = 'The transcation ID does not exist'
        attributes = {'id': str(TID)}
        return construct_node('error', Msg, **attributes)
    else:
        query_status(status_node, order)
    session.close()
    return status_node
