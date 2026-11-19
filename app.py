from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

class Product:
    def __init__(self,id,name,barcode,brands,ingredients_text):
        self.id = id
        self.name = name
        self.barcode = barcode
        self.brands = brands
        self.ingredients_text = ingredients_text

    def to_dict(self):
        return{
               "id" :self.id,
               "name": self.name, 
               "barcode" : self.barcode,
               "brands": self.brands,
               "ingredients_text" : self.ingredients_text
              }

mock_db = [
    Product(1, "Organic Almond Milk","123456789", "Silk", "Filtered water, almonds, cane sugar"),
    Product(2, "Nutella", "3017620422003","Ferrero", "Sugar, palm oil, hazelnuts")
]
def find_product(product_id):
    for p in mock_db:
        if p.id == product_id:
            return p
    return None

def fetch_from_api(barcode):
    barcode = str(barcode).strip().replace('"','').replace("'","")
    url = f"https://world.openfoodfacts.org/api/v3/product/{barcode}.json"
    headers = {"User-Agent": "InventoryApp/1.0 (john.doe@email.com)"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
               return data.get("product")
        return None
    except:
        return None


@app.route("/product", methods = ["GET"])
def get_all_products():
     return jsonify([p.to_dict() for p in mock_db]), 200

@app.route("/product/<int:product_id>", methods = ["GET"])
def get_product(product_id):
    p = find_product(product_id)
    if p is not None:
        return jsonify(p.to_dict()),200
    else:
        return jsonify({"Error": "Product not found"}),404

@app.route("/product", methods = ["POST"])
def add_product():
    data = request.get_json(silent =True)

    if not data or "barcode" not in data:
        return jsonify({"Error":"Barcode required to add product"}), 400

    barcode = data ["barcode"]

    api_data = fetch_from_api(barcode)

    if api_data is None:
       return jsonify({"Error": "Barcode not found in Open Food Facts API"}), 404 

    try:
        new_id = mock_db[-1].id+1
        
    except IndexError:
        new_id = 1

    new_Product =Product(
                    id = new_id, 
                    name = api_data.get ("product_name","Unknown Product"), 
                    brands = api_data.get("brands","Unknown Brand"),
                    barcode = barcode,
                    ingredients_text = api_data.get("ingredients_text", "No ingredients listed")
                    )
    mock_db.append(new_Product)
    return jsonify(new_Product.to_dict()), 201

@app.route("/product/<int:product_id>", methods = ["PATCH"])
def update_product(product_id):
    data = request.get_json(silent =True)
    if not data or "name" not in data:
       return jsonify({"Error":"Product Name required"}), 400
    
    p = find_product(product_id)
    if p is None:
        return jsonify({"Error": "Product not found"}),404

    p.name = data["name"]
    return jsonify(p.to_dict()),200


@app.route("/product/<int:product_id>", methods = ["DELETE"])
def  delete_product(product_id):
    p = find_product(product_id)
    if p is None:
        return jsonify({"Error" :" Product not found"}),404
    
    mock_db.remove(p)
    return "",204

if __name__ == '__main__':
    app.run(debug=True)

