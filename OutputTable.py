# import things
from flask_table import Table, Col


# Declare your table
class ItemTable(Table):
    name = Col('Sample id')
    description = Col('Frequency of haplotypes without positive antigens')


# Get some objects
class Item(object):
    def __init__(self, id, freq):
        self.name = id
        self.description = freq


def get_output_table(outputs):
    items = []
    for pair in outputs:
        items.append(Item(pair[0], pair[1]))
    table = ItemTable(items)
    return table
