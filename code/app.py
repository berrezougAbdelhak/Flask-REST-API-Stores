from flask import Flask,request
from  flask_restful import Resource, Api 

app=Flask(__name__)

api=Api(app)
items=[] 
class Item(Resource):
    def get(self,name):
        #next give us the first item of the list (that returns only one item)
        #If does't exist next returns None
        item=next(filter(lambda x:x["name"]==name,items),None) 
        return {"item":item},200 if item  else 404
    
    def post(self,name):
        if next(filter(lambda x:x["name"]==name,items),None) is not None:
            return {"message":"An item with name {} already exists.".format(name)},400
        data=request.get_json()
        item={"name":name,"price":data}
        items.append(item)
        return item,201
class ItemList(Resource):
    def get(self):
        return {"items":items}
         
api.add_resource(Item,"/item/<string:name>") 

api.add_resource(ItemList,"/items")

app.run()