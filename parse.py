import xml.etree.ElementTree as ET
from queryDb import *
from addTodb import *


def create_symbol(session, child):
    return_node = ET.Element("temp")
    try:
        checkSymbolName(child.attrib['sym'])
        for account_ins in child:
            attributes = {
                'sym': child.attrib['sym'], 'id': account_ins.attrib['id']}
            try:
                addPosition(session,
                            account_ins.attrib['id'], child.attrib['sym'], int(account_ins.text))
                return_node.append(construct_node(
                    'created', None, **attributes))
            except Exception as e:
                return_node.append(construct_node(
                    'error', str(e), **attributes))
    except Exception as e:
        attributes = {'sym': child.attrib['sym']}
        return_node.append(construct_node('error', str(e), **attributes))
    return return_node.getchildren()


def order_Transcation(session, root, child, response):
    attributes = {'sym': child.attrib['sym'], 'amount':
                  str(int(child.attrib['amount'])), 'limit': child.attrib['limit']}
    try:
        if int(child.attrib['limit']) <= 0:
            raise ValueError("Price should be positive")
        addTranscation(int(root.attrib['id']),
                       child.attrib['sym'], int(child.attrib['amount']), float(child.attrib['limit']))
        # execute_order(session, int(root.attrib['id']), child.attrib['sym'], int(
        #     child.attrib['amount']), float(child.attrib['limit']))
        attributes['id'] = root.attrib['id']
        response.append(construct_node('opened', None, **attributes))
    except Exception as e:
        response.append(construct_node('error', str(e), **attributes))


def query_Transcation(session, root, child, response):
    response.append(query_transcation(session,
                                      int(root.attrib['id']), int(child.attrib['id'])))


def cancel_Transcation(session, root, child, response):
    cancel_node = ET.Element("canceled")
    cancel_node.set('id', str(child.attrib['id']))
    all_status = session.query(Status).join(Transaction).join(Account).filter(
        Account.id == int(root.attrib['id'])).filter(Transaction.tid == child.attrib['id'])
    if all_status.count() == 0:
        Msg = "Transcation id doesn't exist"
        attributes = {'id': str(child.attrib['id'])}
        response.append(construct_node('error', Msg, **attributes))
        return
    open_status = all_status.filter(
        Status.name == 'open').with_for_update().first()
    open_status.name = 'canceled'
    open_status.time = getCurrentTime()
    session.commit()
    order = session.query(Status).join(Transaction).join(Account).filter(
        Account.id == int(root.attrib['id'])).filter(Transaction.tid == child.attrib['id']).order_by(Status.sid.asc())
    query_status(cancel_node, order)
    response.append(cancel_node)


def handle_create(session, root, response):
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
            for nodes in create_symbol(session, child):
                response.append(nodes)


def handle_transcation(session, root, response):
    try:
        checkIfAccountExist(session, int(root.attrib['id']))
        for child in root:
            if child.tag == 'order':
                order_Transcation(session, root, child, response)
            elif child.tag == 'query':
                query_Transcation(session, root, child, response)
            else:
                # cancle order
                cancel_Transcation(session, root, child, response)
    except Exception as e:
        for child in root:
            attributes = {'id': str(root.attrib['id'])}
            response.append(construct_node('error', str(e), **attributes))


def parsing_XML(session, request):
    root = ET.fromstring(request)
    response = ET.Element("result")
    # create tag
    if root.tag == 'create':
        handle_create(session, root, response)
    else:
        handle_transcation(session, root, response)
    print(ET.tostring(response).decode())
    return ET.tostring(response).decode()
