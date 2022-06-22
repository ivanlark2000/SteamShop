import json

with open('test.json', 'r') as file:
    data = json.load(file)
buy_order_graph = data['buy_order_graph']
for key in buy_order_graph:
    print(key)