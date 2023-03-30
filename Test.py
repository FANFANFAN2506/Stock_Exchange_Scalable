from parse import *


def testParse():
    xmlString = "<create><account id=\"123\" balance=\"100000\"/><symbol sym=\"TESLA\"><account id=\"123\">200</account></symbol></create>"
    xmlString2 = "<transactions id=\"ACCOUNT_ID\"><order sym=\"SYM\" amount=\"AMT\" limit=\"LMT\"/><query id=\"TRANS_ID\"/><cancel id=\"TRANS_ID\"/></transactions>"
    parsing_XML(xmlString)
    parsing_XML(xmlString2)


def testAdd(engine):
    try:
        addAccount(1, 100000, engine)
        addAccount(1, 200, engine)
    except Exception as e:
        print(e)
    try:
        addPosition(1, 'T5asdf', 200, engine)
        addPosition(1, 'T5asdf', 300, engine)
        # addTranscation(1, 'T5asdf', 400, 125, engine)
        # addTranscation(1, 'T5asdf', 400, 125, engine)
        # addTranscation(1, 'T5asdf', 200, 125, engine)
        # addTranscation(1, 'T5asdf', -300, 125, engine)
        # addStatus(1, 'executed', 100, 125.3, getCurrentTime(), engine)
        # # checkTIme(engine)
        # addTranscation(1, 'T5asdf', -300, 125, engine)
        # addTranscation(2, 'T5asdf', -400, 125, engine)
        # addPosition(1, 'S&P', 300, engine)
        # addPosition(1, 'BTC', 100, engine)
        # addPosition(2, 'T5asdf', 200, engine)
        # addAccount(0, 100, engine)
    except Exception as e:
        print(e)


def main():
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
    testParse()


if __name__ == '__main__':
    main()
