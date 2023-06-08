from unittest.mock import patch, MagicMock
from io import StringIO
from main import parse_file, ItemHandler
from xml.sax import make_parser, parseString
from xml.sax.handler import ContentHandler
def parse_string(xml_str, scenario):
    handler = ItemHandler(scenario)
    parseString(xml_str, handler)
    return handler

def test_scenario_1():
    xml_str = '''<?xml version="1.0" encoding="utf-8"?>
                <export_full date="2022-03-29 07:01:28" version="20160107">
                    <items>
                        <item name='Test Item' code='1234'>
                        </item>
                    </items>
                </export_full>
                '''

    handler = parse_string(xml_str, 1)
    assert len(handler.root_items) == 1

def test_scenario_2():
    xml_str = '''<?xml version="1.0" encoding="utf-8"?>
                <root>
                    <items>
                        <item name='Test Item' code='1234'>
                        </item>
                    </items>
                </root>
                '''

    handler = parse_string(xml_str, 2)
    assert len(handler.root_items) == 1
    assert handler.root_items["1234"].name == "Test Item"

def test_scenario_3():
    xml_str = '''<?xml version="1.0" encoding="utf-8"?>
                <root>
                    <part partName='Náhradní díly' itemName='Test Part' id='5678'>
                        <item name='Test SubItem' code='9012'></item>
                    </part>
                </root>
                '''

    handler = parse_string(xml_str, 3)
    assert len(handler.part_items) == 1
    assert handler.part_items["Test Part 5678"][0] == "Test SubItem 9012"

def test_scenario_2_advanced():
    xml_str = '''<?xml version="1.0" encoding="utf-8"?>
                <root>
                    <items>
                        <item name='Test Item' code='1234'></item>
                        <item name='Test Item 2' code='5678'></item>
                    </items>
                </root>
                '''

    handler = parse_string(xml_str, 2)
    print(handler.root_items)
    print(handler.counter)
    assert len(handler.root_items) == 2
    assert handler.root_items["1234"].name == "Test Item"
    assert handler.root_items["5678"].name == "Test Item 2"

def test_scenario_3_advanced():
    xml_str = "<root><part partName='Náhradní díly' itemName='Test Part' id='5678'><item name='Test SubItem' code='9012'></item></part><part partName='Náhradní díly' itemName='Test Part 2' id='3456'><item name='Test SubItem 2' code='7890'></item></part></root>"
    handler = parse_string(xml_str, 3)
    assert len(handler.part_items) == 2
    assert handler.part_items["Test Part 5678"][0] == "Test SubItem 9012"
    assert handler.part_items["Test Part 2 3456"][0] == "Test SubItem 2 7890"