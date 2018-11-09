import xml.etree.ElementTree as ET
import sys

tree = ET.parse(sys.argv[1])
root = tree.getroot()
for child in root:
    print(child.tag, child.attrib)

