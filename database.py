from sqlalchemy import create_engine
from addTodb import *


def main():
    engine = create_engine(
        'postgresql://postgres:passw0rd@localhost:5432/hw4')
    # Check if connected to the database
    try:
        C_success = engine.connect()
        print('Opened database successfully')
        C_success.close()
    except Exception as e:
        print("Can't open database", e)

    # Drop all the tables
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    try:
        addAccount(1, 100000, engine)
        addAccount(1, 200, engine)
    except Exception as e:
        print(e)
    try:
        addPosition(1, 'T5asdf', 200, engine)
        addPosition(1, 'T5asdf', 300, engine)
        addTranscation(1, 'T5asdf', 400, 125, engine)
        addTranscation(1, 'T5asdf', 400, 125, engine)
        addTranscation(1, 'T5asdf', 200, 125, engine)
        addTranscation(1, 'T5asdf', -300, 125, engine)
        addStatus(1, 'executed', 100, 125.3, getCurrentTime(), engine)
        # checkTIme(engine)
        addTranscation(1, 'T5asdf', -300, 125, engine)
        addTranscation(2, 'T5asdf', -400, 125, engine)
        addPosition(1, 'S&P', 300, engine)
        addPosition(1, 'BTC', 100, engine)
        addPosition(2, 'T5asdf', 200, engine)
        addAccount(0, 100, engine)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
