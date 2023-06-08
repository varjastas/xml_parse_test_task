import xml.sax

class Item:
    #Item class containing name and code of every item.
    def __init__(self, code, name):
        self.code = code
        self.name = name

def write_to_file(part_items):
    #Writing results of 3 scenario to file
    with open("resources/parts.txt", "w", encoding="UTF-8") as f:
        for i in part_items.keys():
            f.write(f"Item name: {i}\n")
            for j in part_items[i]:
                f.write(f"\tSubItemName: {j}\n")


class ItemHandler(xml.sax.ContentHandler):
    def __init__(self, scenario, write_results = False):
        self.scenario = scenario
        self.current_item = None # Current root item.
        self.root_items = {} # List of all items. Key is code, value is Item object
        self.counter = 0 # Counter is used to know, when root item is closed, because when using sax, you don`t know anything when you receive close tag.
        self.in_part = False # If True then parse all spare items.
        self.part_items = {} # List of all spare items
        self.current_part_item = None # Current item that contains spare items.
        self.write_results = write_results # If true write to file, else print
        self.in_items = False # If in tag items, then parse all items
        self.items_counter = 0

    def startElement(self, tag, attributes):
        if self.scenario in [1, 2]: 
            #Parsing items for scenario 1 and 2
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
            #Parsing items and their spare parts
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
        # If write results is True - write everything to files based on scenario
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
    #Creating parser and setting hadler. Then starting to parse. handler will contain all information collected during parser
    parser = xml.sax.make_parser()
    handler = ItemHandler(scenario, write_results)
    parser.setContentHandler(handler)
    parser.parse(file_path)

    return handler
if __name__ == "__main__":
    scenario = int(input("Choose scenario:\n\t1 - count of products.\n\t 2 - all products names and codes.\n\t 3 - all spare parts\n"))

    if not scenario:
        raise TypeError("You haven`t passed any argument")  
    if scenario not in [1, 2, 3]:
        raise ValueError("Scenario argument is wrong. Pass number between 1 and 3")
    
    parse_file("resources/export_full.xml", scenario, write_results = False)