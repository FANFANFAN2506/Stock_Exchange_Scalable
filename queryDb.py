from dbTable import *
from sqlalchemy.orm import sessionmaker


def query_transcation(UID, TID):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        order = session.query(Status).join(Transaction).join(Account).filter(
            Account.id == UID).filter(Transaction.tid == TID)
        for tuple in order:
            print(tuple.name, tuple.shares, tuple.price, tuple.time.timestamp())
    except Exception as e:
        print(e)
