from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item
        return {'item': None}, 404 # the most popular interview question - 404 - not found.

    def post(self, name):
        data = request.get_json() # can use (force = True) or (silent = True)
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201 # code for created

class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port = 5000, debug = True)
