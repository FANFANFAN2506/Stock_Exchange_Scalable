from parse import *


def testParse():
    xmlString = "<create><account id=\"1\" balance=\"50000\"/><account id=\"2\" balance=\"100000\"/><symbol sym=\"TESLA\"><account id=\"1\">200</account><account id=\"1\">-500</account></symbol></create>"
    xmlString2 = "<transactions id=\"1\"><order sym=\"TESLA\" amount=\"100\" limit=\"250\"/><order sym=\"TESLA\" amount=\"-200\" limit=\"300\"/><query id=\"0\"/><cancel id=\"0\"/><query id=\"1\"/></transactions>"
    xmlString3 = "<transactions id=\"0\"><order sym=\"TESLA\" amount=\"100\" limit=\"250\"/></transactions>"
    xmlString4 = "<transactions id=\"1\"><order sym=\"TESLA\" amount=\"100\" limit=\"250\"/></transactions>"
    parsing_XML(xmlString)
    parsing_XML(xmlString2)
    parsing_XML(xmlString3)


def testAdd():
    try:
        addAccount(1, 100000)
        addAccount(1, 200)
    except Exception as e:
        print(e)
    try:
        addPosition(1, 'T5asdf', 200)
        addPosition(1, 'T5asdf', 300)
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
    # testAdd()


if __name__ == '__main__':
    main()
