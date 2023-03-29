#include <iostream>

#include "rapidxml-1.13/rapidxml.hpp"
#include "rapidxml-1.13/rapidxml_utils.hpp"

using namespace rapidxml;

void parsing_XML(std::string request) {
  xml_document<> doc;
  doc.parse<0>(&request[0]);

  xml_node<> * rootNode = doc.first_node();
  std::cout << "rootnode name is " << rootNode->name() << std::endl;
  while (rootNode->first_node()) {
    xml_node<> * firstNode = rootNode->first_node();
    xml_attribute<> * firstAttr = firstNode->first_attribute();
    while (firstAttr) {
      std::cout << "Attribute name: " << firstAttr->name()
                << " Attribute value: " << firstAttr->value() << std::endl;
      firstAttr = firstAttr->next_attribute();
    }
    rootNode = firstNode;
  }
  doc.clear();
}

int main() {
  // XML string to parse
  std::string xmlString =
      "<create><account id=\"ACCOUNT_ID\" balance=\"BALANCE\"/> #0 or more<symbol "
      "sym=\"SYM\"><account id=\"ACCOUNT_ID\">NUM</account> #1 or more</symbol></create>";
  std::string xmlString2 =
      "<transactions id=\"ACCOUNT_ID\"><order sym=\"SYM\" amount=\"AMT\" "
      "limit=\"LMT\"/><query id=\"TRANS_ID\"/><cancel id=\"TRANS_ID\"/></transactions>";

  parsing_XML(xmlString);
  parsing_XML(xmlString2);

  return 0;
}
