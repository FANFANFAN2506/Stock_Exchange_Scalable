from datetime import datetime
import xml.etree.ElementTree as ET


def getCurrentTime():
    current_time = datetime.now()
    time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
    return time_str


''' 
* @func: Construct an element node
* @param: {Msg, **attributes} Msg is the message, attributes are a set of key-value pair
* @return: {child_node} node to be append 
'''


def construct_node(Name, Msg, **attributes):
    child_node = ET.Element(Name)
    if Msg:
        child_node.text = Msg
    for key, value in attributes.items():
        child_node.set(key, value)
    return child_node
