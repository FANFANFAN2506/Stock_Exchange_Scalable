from parse import *
from match_price import *
from addTodb import addTranscation
import time


def testMatch():
    addAccount(1, 100000)
    addAccount(2, 100000)
    addAccount(3, 100000)
    addAccount(4, 100000)
    addAccount(5, 100000)
    addAccount(6, 100000)
    addAccount(7, 100000)
    addPosition(1, 'X', 500)
    addPosition(2, 'X', 500)
    addPosition(3, 'X', 500)
    addPosition(4, 'X', 500)
    addPosition(5, 'X', 500)
    addPosition(6, 'X', 500)
    addPosition(7, 'X', 500)
    addPosition(6, 'Y', 500)

    addTranscation(1, 'X', 300, 125)
    # execute_order(1)
    addTranscation(2, 'X', -100, 130)
    addTranscation(3, 'X', 200, 127)
    # execute_order(3)
    addTranscation(4, 'X', -500, 128)
    addTranscation(5, 'X', -200, 140)
    time.sleep(1)
    addTranscation(6, 'X', 400, 125)
    time.sleep(1)
    addTranscation(6, 'Y', 400, 125)
    addTranscation(7, 'X', 300, 125)
    # execute_order(6)
    addTranscation(7, 'X', -400, 120)
    execute_order(7, 'X', -400, 120)


''' 
@func: This is the unit test and combination test for XML parser and adding to databse functions
'''


def testParse():
    xmlString = "<create><account id=\"1\" balance=\"50000\"/><account id=\"2\" balance=\"100000\"/><symbol sym=\"TESLA\"><account id=\"1\">200</account><account id=\"1\">500</account></symbol></create>"
    xmlString2 = "<transactions id=\"1\"><order sym=\"TESLA\" amount=\"-100\" limit=\"250\"/><order sym=\"TESLA\" amount=\"-200\" limit=\"300\"/><query id=\"1\"/><cancel id=\"1\"/><query id=\"2\"/></transactions>"
    xmlString3 = "<transactions id=\"0\"><order sym=\"TESLA\" amount=\"100\" limit=\"250\"/></transactions>"
    xmlString4 = "<transactions id=\"1\"><order sym=\"TESLA\" amount=\"100\" limit=\"250\"/></transactions>"
    parsing_XML(xmlString)
    parsing_XML(xmlString2)
    # parsing_XML(xmlString3)


''' 
@func: This is the unit test for adding to database function
'''


def testAdd():
    try:
        print("----Test 1 Failed: Account exist----")
        addAccount(1, 100000)
        addAccount(1, 200)
    except Exception as e:
        print(e)

    print("")
    try:
        print("----Test 2 Failed: Balance not sufficient----")
        addPosition(1, 'T5asdf', 200)
        addPosition(1, 'T5asdf', 300)
        addTranscation(1, 'T5asdf', 400, 125)
        addTranscation(1, 'T5asdf', 400, 125)
        addTranscation(1, 'T5asdf', 200, 125)

    except Exception as e:
        print(e)

    print("")
    try:
        print("----Test 3 Failed: amount not sufficient----")
        addAccount(2, 200)
        addPosition(2, 'T5asdf', 200)
        addTranscation(2, 'T5asdf', -400, 125)
    except Exception as e:
        print(e)
    try:
        addPosition(1, 'S&P', 300)
        addPosition(1, 'BTC', 100)
        addStatus(1, 'executed', 100, 100, getCurrentTime())
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
    # testMatch()

    # testParse()
    testAdd()


if __name__ == '__main__':
    main()
