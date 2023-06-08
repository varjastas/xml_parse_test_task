import xml.sax
import os

class Item:
    def __init__(self, code, name):
        self.code = code
        self.name = name

def write_to_file(part_items):
    with open("resources/parts.txt", "w", encoding="UTF-8") as f:
        for i in part_items.keys():
            f.write(f"Item name: {i}\n")
            for j in part_items[i]:
                f.write(f"\tSubItemName: {j}\n")


class ItemHandler(xml.sax.ContentHandler):
    def __init__(self, scenario, write_results = False):
        self.scenario = scenario
        self.current_item = None
        self.root_items = {}
        self.counter = 0
        self.in_part = False
        self.part_items = {}
        self.current_part_item = None
        self.write_results = write_results
        self.in_items = False
        self.items_counter = 0

    def startElement(self, tag, attributes):
        if self.scenario in [1, 2]: 
            if tag == "items":
                self.in_items = True

            if tag == "item":
                if self.counter == 0 and self.in_items:
                    name = attributes.get("name")
                    code = attributes.get("code")
                    if self.scenario == 2:
                        if name and code:
                            self.current_item = Item(code, name)
                            self.root_items[code] = self.current_item
                    else:
                        self.items_counter += 1
                self.counter += 1

        if self.scenario == 3:
            if tag == "part" and attributes.get("partName") == "Náhradní díly":
                item_name = attributes.get("itemName")
                item_code = attributes.get("id")
                self.current_part_item = f"{item_name} {item_code}"

                self.in_part = True

                if not self.current_part_item in self.part_items:
                    self.part_items[self.current_part_item] = []
                else:
                    if self.tested:
                        write_to_file()
                    raise Exception(f"Parts {self.current_part_item} duplicated.")

            if tag == "item" and self.in_part:
                name = attributes.get("name")
                code = attributes.get("code")
                try:
                    self.part_items[self.current_part_item].append(f"{name} {code}")
                except:
                    if self.tested:
                        write_to_file(self.part_items)
                    raise Exception(f"Failed to append items to part {self.current_part_item}")
            
       
    def endElement(self, tag):
        
        if self.scenario in [1, 2]:
            if tag == "items":
                self.in_items = False

            if tag == "item":
                self.counter += 1
                if self.counter % 2 == 0: 
                    self.counter = 0
                    self.current_item = None

        if tag == "part" and self.scenario == 3:
            self.in_part = False
            self.current_part_item = None

    def endDocument(self):
        if self.write_results:
            if self.scenario == 1:
                with open("resources/items_count.txt", "w", encoding="UTF-8") as f:
                    f.write(f"Count of items: {self.items_counter}")
            elif self.scenario == 2:
                with open("resources/items.txt", "w", encoding="UTF-8") as f:
                    for item in self.root_items.values():
                        f.write(f"Item Name: {item.name}. Item code: {item.code}\n")
            elif self.scenario == 3:
                write_to_file(self.part_items)


def parse_file(file_path, scenario, write_results = False):
    parser = xml.sax.make_parser()
    handler = ItemHandler(scenario, write_results)
    parser.setContentHandler(handler)
    parser.parse(file_path)

    return handler
if __name__ == "__main__":
    scenario = int(input("Choose scenario:\n\t1 - count of products.\n\t 2 - all products names and codes.\n\t 3 - all spare parts\n"))
    
    write_results_or_print = int(input("If you want to write results type 1, if you want to write them to the file type 2"))

    if not scenario or write_results_or_print:
        raise TypeError("You haven`t passed any argument")  
    if scenario not in [1, 2, 3]:
        raise ValueError("Scenario argument is wrong. Pass number between 1 and 3")
    if write_results_or_print not in [1, 2]:
        raise ValueError("Write results argument is wrong. Pass number between 1 and 3")

    if write_results_or_print == 1:
        write_results_or_print = True
    else:
        write_results_or_print = False
    parse_file("resources/export_full.xml", scenario, write_results = False)