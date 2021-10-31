from flask import Flask, redirect, render_template, request, session, abort
from pymongo import MongoClient
import json

from handle_db import Item, User, db_check

#Flask init
app = Flask("__name__")
app.secret_key = "Secret_Key"


#DB Connection init
client = MongoClient()
db = client.InventoryManagementSystem

#Tables
users = db.Users
items = db.Items

#Categories - Tags
tags_file = open("config.json", "r+")
tags_json = json.load(tags_file)

TAGS = []

for tag in tags_json["tags"]:
    TAGS = TAGS + [tag]


#Homepage
@app.route("/", methods=["POST", "GET"])
def homepage():
    if request.method == "POST":
        username = request.form["username"]
        pin = request.form["pin"]
        
        usr = User(str(username))

        if usr.login(int(pin)) == True:
            session["logged"] = True
            session["username"] = str(usr.username)

            return redirect("/dashboard")

        else: abort(401)

    else:
        return render_template("homepage.html")

#List of items
@app.route("/dashboard")
def all_items():
    if session["logged"] == True:

        items_list = []

        tag = request.args.get("tag", default=None, type=str)
        location = request.args.get("location", default=None, type=str)

        if tag != None:
            for item in items.find({"tag": str(tag)}):
                items_list = [item] + items_list
            
        elif location != None:
            for item in items.find({"location": str(location)}):
                items_list = [item] + items_list
            
        else:
            for item in items.find():
                items_list = [item] + items_list


        items_list = sorted(items_list, key=lambda d: d["name"])

        return render_template("dashboard/list_of_items.html", items_list=items_list)

    else: return redirect("/")


#Single item page
@app.route("/dashboard/item")
def single_item_page():
    if session["logged"] == True:

        itm = Item(request.args["code"])
        item = itm.query
        
        back_url = request.referrer

        return render_template("dashboard/single_item.html", item=item, back_url=back_url)
    
    else: return redirect("/")


#Take item by barcode
@app.route("/dashboard/assign-item")
def take_item_barcode():
    if session["logged"] == True:
        return render_template("/dashboard/assign_item.html")

    else: return redirect("/")

#Place item (to stock) by barcode
@app.route("/dashboard/stock-item")
def stock_item_barcode():
    if session["logged"] == True:
        return render_template("/dashboard/stock_item.html")

    else: return redirect("/")

#New item
@app.route("/dashboard/new-item", methods = ["POST", "GET"])
def new_item_page():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        tag = request.form["tag"]
        location = "Stock"
        code = request.form["code"]
        
        itm = Item(code)
        itm.add_new_item(
            name, location, tag, description
        )

        return redirect("/dashboard")


    else:
        return render_template("/dashboard/new_item.html", TAGS=TAGS)



#New user
@app.route("/dashboard/new-user", methods=["POST", "GET"])
def new_user_page():
    if session["logged"] == True:

        if request.method == "POST":
            usr = User(request.form["username"])

            if usr.new_user(request.form["pin"]) == True:
                return redirect("/dashboard")
            
            else: return abort(409)

    
        

        else:
            users_list = []

            for user in users.find():
                users_list = [user] + users_list

            return render_template("dashboard/new_user.html", users_list=users_list)

    else: return redirect("/")




#Functions
@app.route("/function/<func>", methods=["POST", "GET"])
def functions(func):
    #Check login status
    if session["logged"] == True:

        #Assign function
        if func == "assign":
            #Post method - Submiting by form
            if request.method == "POST":
                itm = Item(request.form["code"])

            else:
                #Args method - Submiting from "list of items"
                itm = Item(request.args["code"])

                stock_mode = request.args.get("stock", default=None, type=str)

                if stock_mode != None:
                    itm.change_item_location("Stock")

                    return redirect("/dashboard")

            itm.change_item_location(session["username"])

            return redirect("/dashboard")

        #Stock item
        if func == "stock":
            itm = Item(request.form["code"])

            itm.change_item_location("Stock")

            return redirect("/dashboard")


        #Logout function
        if func == "logout":
            session.pop("username", None)
            session.pop("logged", None)
            
            return redirect("/")

while __name__ == "__main__":
    db_check()
    app.run(debug=True)