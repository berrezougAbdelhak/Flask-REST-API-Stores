from flask import Flask,jsonify,request,render_template

app = Flask(__name__)

stores = [{"name": "My Wonderful Store", "items": [
    {"name": "MyItem", "Price": 12.99}]}]

@app.route("/")
def home():
    return render_template("index.html")

# POST /store data: {name:}

@app.route("/store", methods=["POST"])
def create_store():
    request_data=request.get_json()
    new_store={"name":request_data["name"],"items":[]}
    stores.append(new_store)
    return jsonify(new_store)


# GET /store/<string: name>

@app.route("/store/<string:name>")
def get_store(name):
    #Iterate over stores
    for s in stores:
        if s["name"]==name:
            return jsonify(s["name"])
    return  jsonify({"Message":"Not exist"})



#GET /store
@app.route("/store")
def get_stores():
    return jsonify({"stores":stores})

# POST /store/<string:name>/item {name:, price:}


@app.route("/store/<string:name>/item", methods=["POST"])
def create_item_in_store(name):
    new_item=request.get_json()
    for store in stores:
        if store["name"]==name:
            print(new_item)
            store["items"].append({"name":new_item["name"],"price":new_item["price"]})
            return jsonify(store)
    
    return jsonify({"message":"store not found"})
    
# GET /store/<string: name>/item


@app.route("/store/<string:name>/item")
def get_item_in_store(name):
    for store in stores:
        if store["name"]==name:
            return jsonify(store["items"])
    return jsonify({"message":" Store does not exist"})

app.run(port=5000)
