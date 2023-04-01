from dbTable import *
from utils import construct_node
import xml.etree.ElementTree as ET
from sqlalchemy.orm import sessionmaker


def query_transcation(UID, TID):
    status_node = ET.Element("status")
    status_node.set('id', str(TID))
    Session = sessionmaker(bind=engine)
    session = Session()
    order = session.query(Status).join(Transaction).join(Account).filter(
        Account.id == UID).filter(Transaction.tid == TID)
    if order.count() == 0:
        Msg = 'The transcation ID does not exist'
        attributes = {'id': str(TID)}
        return construct_node('error', Msg, **attributes)
    else:
        for tuple in order:
            if tuple.name == 'open':
                attributes = {'shares': str(tuple.shares)}
                status_node.append(construct_node('open', None, **attributes))
            elif tuple.name == 'canceled':
                attributes = {'shares': str(tuple.shares),
                              'time': str(tuple.time.timestamp())}
                status_node.append(construct_node(
                    'canceled', None, **attributes))
            else:
                attributes = {'shares': tuple.shares,
                              'price': tuple.price, 'time': str(tuple.time.timestamp())}
                status_node.append(construct_node(
                    'executed', None, **attributes))
    session.close()
    return status_node
