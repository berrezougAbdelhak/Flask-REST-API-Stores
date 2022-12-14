from typing_extensions import Required
from flask import Flask,request
from  flask_restful import Resource, Api, reqparse
from flask_jwt import JWT,jwt_required
from security import authenticate,identity


app=Flask(__name__)
app.secret_key="jose"
api=Api(app)

jwt=JWT(app,authenticate,identity)


items=[] 
class Item(Resource):
    parser=reqparse.RequestParser() #initialise a new object which we can use to parse the request 
    parser.add_argument("price",type=float,required=True,help="This field cannot be left blank ")
    @jwt_required()
    def get(self,name):
        #next give us the first item of the list (that returns only one item)
        #If does't exist next returns None
        item=next(filter(lambda x:x["name"]==name,items),None) 
        return {"item":item},200 if item  else 404
    
    def post(self,name):
        if next(filter(lambda x:x["name"]==name,items),None) is not None:
            return {"message":"An item with name {} already exists.".format(name)},400
        data=Item.parser.parse_args()
        item={"name":name,"price":data["price"]}
        items.append(item)
        return item,201
    
    def delete(self,name):
        global items
        items=list(filter(lambda x:x["name"]!=name,items))
        return {"Message": "Item deleted"}
    
    def put(self,name):

        data=Item.parser.parse_args()
        print(data["another"])
        item=next(filter(lambda x:x["name"]==name,items),None)
        if item is None:
            item={"name":name,"price":data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item 
 
class ItemList(Resource):
    def get(self):
        return {"items":items}
         
api.add_resource(Item,"/item/<string:name>") 

api.add_resource(ItemList,"/items")


app.run()