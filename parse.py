import xml.etree.ElementTree as ET
# from addTodb import *
from addTodb import *


def create_symbol(child):
    print("Create symbol")
    SYM = child.attrib['sym']
    print(SYM)
    for account_ins in child:
        print(account_ins.text)


def create_order(child):
    print("Create order")


def query_order(child):
    print("query order")


def cancel_order(child):
    print("cancel order")


def handle_create(root):
    print("This is a create request")
    for child in root:
        if child.tag == 'account':
            addAccount(int(child.attrib['id']), int(
                child.attrib['balance']), engine)
        else:
            create_symbol(child)


def handle_transcation(root):
    print("This is a transcations request")
    for child in root:
        if child.tag == 'open':
            create_order(child)
        elif child.tag == 'query':
            query_order(child)
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
