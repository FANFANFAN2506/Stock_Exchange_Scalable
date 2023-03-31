import xml.etree.ElementTree as ET
from queryDb import *
from addTodb import *


def create_symbol(child):
    print("Create symbol")
    try:
        checkSymbolName(child.attrib['sym'])
        for account_ins in child:
            print(child.attrib['sym'], int(account_ins.text))
            addPosition(
                account_ins.attrib['id'], child.attrib['sym'], int(account_ins.text))
    except Exception as e:
        print(e)


def create_order(root, child):
    print("Create order")
    addTranscation(int(root.attrib['id']),
                   child.attrib['sym'], int(child.attrib['amount']), float(child.attrib['limit']))


def query_order(root, child):
    print("query order")
    query_transcation(int(root.attrib['id']), int(child.attrib['id']))


def cancel_order(child):
    print("cancel order")


def handle_create(root):
    print("This is a create request")
    for child in root:
        if child.tag == 'account':
            addAccount(int(child.attrib['id']), int(
                child.attrib['balance']))
        else:
            create_symbol(child)


def handle_transcation(root):
    print("This is a transcations request")
    for child in root:
        if child.tag == 'order':
            create_order(root, child)
        elif child.tag == 'query':
            query_order(root, child)
        else:
            # cancle order
            cancel_order(child)


def parsing_XML(request):
    root = ET.fromstring(request)
    # create tag
    if root.tag == 'create':
        handle_create(root)
    else:
        handle_transcation(root)
    # for child in root:
    #     print(child.tag)
    #     for key, value in child.items():
    #         print(f"{key}:{value} ", end="")
    #     print()
