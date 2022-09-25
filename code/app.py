from flask import Flask,request
from  flask_restful import Resource, Api 

app=Flask(__name__)

api=Api(app)
items=[] 
class Item(Resource):
    def get(self,name):
        # for item in items:
        #     if item["name"]==name:
        #         return item
        item=filter(lambda item:item["name"]==name,items)
        # return {"Message":"item doesn't exist"},404
        return item
    
    def post(self,name):
        data=request.get_json()
        item={"name":name,"price":data["price"]}
        items.append(item)

        return item,201
class ItemList(Resource):
    def get(self):
        return {"items":items}
         
api.add_resource(Item,"/item/<string:name>") 

api.add_resource(ItemList,"/items")

app.run()