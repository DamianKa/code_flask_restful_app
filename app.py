from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'secret'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

items = []

class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None) # we can use list or next
        return {'item': item}, 200 if item else 404 # the most popular interview question - 404 - not found.

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400 # 400 is bad request

        data = request.get_json() # can use (force = True) or (silent = True)
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201 # code for created

    #I can add @jwt_required() before every method here and it will mean that it will require JWT token
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name): # put is idempotent so I can call the funcktion many times and I will not end up with many items
        data = request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port = 5000, debug = True)
