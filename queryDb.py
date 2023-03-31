from dbTable import *
from sqlalchemy.orm import sessionmaker


def query_transcation(UID, TID):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        order = session.query(Status).join(Transaction).join(Account).filter(
            Account.id == UID).filter(Transaction.tid == TID)
        session.close()
        for tuple in order:
            if tuple.name == 'open':
                print(tuple.name, tuple.shares)
            elif tuple.name == 'canceled':
                print(tuple.name, tuple.shares, int(tuple.time.timestamp()))
            else:
                print(tuple.name, tuple.shares,
                      tuple.price, int(tuple.time.timestamp()))
        return order
    except Exception as e:
        print(e)
