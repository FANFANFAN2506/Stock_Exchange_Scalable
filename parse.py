import xml.etree.ElementTree as ET
from queryDb import *
from addTodb import *


def create_symbol(child):
    print("Create symbol")
    try:
        checkSymbolName(child.attrib['sym'])
        for account_ins in child:
            attributes = {
                'sym': child.attrib['sym'], 'id': account_ins.attrib['id']}
            try:
                addPosition(
                    account_ins.attrib['id'], child.attrib['sym'], int(account_ins.text))
                return construct_node('created', None, **attributes)
            except Exception as e:
                return construct_node('error', str(e), **attributes)
    except Exception as e:
        print(e)


def order_Transcation(root, child):
    print("Create order")
    addTranscation(int(root.attrib['id']),
                   child.attrib['sym'], int(child.attrib['amount']), float(child.attrib['limit']))


def query_Transcation(root, child):
    print("query order")
    query_transcation(int(root.attrib['id']), int(child.attrib['id']))


def cancel_Transcation(root, child):
    print("cancel order")
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        all_status = session.query(Status).join(Transaction).join(Account).filter(
            Account.id == int(root.attrib['id'])).filter(Transaction.tid == child.attrib['id'])
        open_status = all_status.filter(Status.name == 'open').first()
        open_status.name = 'canceled'
        open_status.time = getCurrentTime()
        session.commit()
        session.close()
    except Exception as e:
        print(e)


def handle_create(root, response):
    print("This is a create request")
    for child in root:
        if child.tag == 'account':
            attributes = {'id': child.attrib['id']}
            try:
                addAccount(int(child.attrib['id']), int(
                    child.attrib['balance']))
                response.append(construct_node('created', None, **attributes))
            except Exception as e:
                response.append(construct_node(
                    'error', str(e), **attributes))
        else:
            response.append(create_symbol(child))


def handle_transcation(root, response):
    print("This is a transcations request")
    for child in root:
        if child.tag == 'order':
            order_Transcation(root, child)
        elif child.tag == 'query':
            query_Transcation(root, child)
        else:
            # cancle order
            cancel_Transcation(root, child)


def parsing_XML(request):
    root = ET.fromstring(request)
    response = ET.Element("result")
    # create tag
    if root.tag == 'create':
        handle_create(root, response)
    else:
        handle_transcation(root, response)
    print(ET.tostring(response).decode())
