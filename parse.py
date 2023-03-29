import xml.etree.ElementTree as ET


def parsing_XML(request):
    root = ET.fromstring(request)
    print("The request is", root.tag)

    for child in root:
        print(child.tag)
        for key, value in child.items():
            print(f"{key}:{value} ", end="")
        print()


if __name__ == '__main__':
    xmlString = "<create><account id=\"ACCOUNT_ID\" balance=\"BALANCE\"/> #0 or more<symbol sym=\"SYM\"><account id=\"ACCOUNT_ID\">NUM</account> #1 or more</symbol></create>"
    xmlString2 = "<transactions id=\"ACCOUNT_ID\"><order sym=\"SYM\" amount=\"AMT\" limit=\"LMT\"/><query id=\"TRANS_ID\"/><cancel id=\"TRANS_ID\"/></transactions>"
    parsing_XML(xmlString)
    parsing_XML(xmlString2)
