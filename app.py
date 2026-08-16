from flask import Flask, jsonify, request, abort
import requests

app = Flask(__name__)

# OpenFoodFacts wants a user agent so they know who's calling
HEADERS = {"User-Agent": "InventoryManagementSystem/1.0 (student@example.com)"}

# ---- Home route ----

@app.route('/')
def home():
    return {
        "message": "Inventory Management API",
        "endpoints": {
            "items": {
                "GET /items": "List all items",
                "GET /items/<id>": "Get item by ID",
                "POST /items": "Create new item",
                "PATCH /items/<id>": "Update item",
                "DELETE /items/<id>": "Delete item"
            },
            "external": {
                "GET /external/barcode/<barcode>": "Search by barcode",
                "GET /external/search?name=<query>": "Search by name",
                "POST /external/add/<barcode>": "Add product to inventory"
            }
        }
    }, 200

# store items in memory (resets when server restarts)
items = []
next_id = 1

def reset_inventory():
    """reset for tests"""
    global items, next_id
    items = []
    next_id = 1

def find_item(item_id):
    for item in items:
        if item['id'] == item_id:
            return item
    return None

# ---- CRUD routes ----

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = find_item(item_id)
    if item is None:
        abort(404, description="Item not found")
    return jsonify(item)

@app.route('/items', methods=['POST'])
def create_item():
    global next_id
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, description="Missing name")
    item = {
        'id': next_id,
        'name': data['name'],
        'barcode': data.get('barcode', ''),
        'category': data.get('category', ''),
        'quantity': data.get('quantity', 0),
        'price': data.get('price', 0.0),
        'supplier': data.get('supplier', ''),
        'description': data.get('description', '')
    }
    next_id += 1
    items.append(item)
    return jsonify(item), 201

@app.route('/items/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    item = find_item(item_id)
    if item is None:
        abort(404, description="Item not found")
    data = request.get_json()
    if not data:
        abort(400, description="Need JSON body")
    # only update fields that are present
    for field in ['name', 'barcode', 'category', 'quantity', 'price', 'supplier', 'description']:
        if field in data:
            item[field] = data[field]
    return jsonify(item)

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = find_item(item_id)
    if item is None:
        abort(404, description="Item not found")
    items.remove(item)
    return '', 204

# ---- external API routes ----

def fetch_product_by_barcode(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            return None, f"External API returned {resp.status_code}"
        data = resp.json()
        if data.get('status') != 1:
            return None, "Product not found"
        product = data.get('product', {})
        return {
            'barcode': barcode,
            'name': product.get('product_name') or "Unknown",
            'brand': product.get('brands') or '',
            'category': product.get('categories') or '',
            'description': product.get('ingredients_text') or ''
        }, None
    except requests.exceptions.RequestException as e:
        return None, str(e)

@app.route('/external/barcode/<barcode>', methods=['GET'])
def external_barcode(barcode):
    product, error = fetch_product_by_barcode(barcode)
    if error:
        if error == "Product not found":
            return jsonify({'error': error}), 404
        return jsonify({'error': error}), 502
    return jsonify(product)

@app.route('/external/search', methods=['GET'])
def external_search():
    query = request.args.get('name', '')
    if not query:
        return jsonify({'error': "Need name parameter"}), 400
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        'search_terms': query,
        'search_simple': True,
        'action': 'process',
        'json': 1,
        'page_size': 5
    }
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
        if resp.status_code != 200:
            return jsonify({'error': f"External API returned {resp.status_code}"}), 502
        products = resp.json().get('products', [])
        results = []
        for p in products:
            results.append({
                'barcode': p.get('code', ''),
                'name': p.get('product_name', 'Unknown'),
                'brand': p.get('brands', ''),
                'category': p.get('categories', '')
            })
        return jsonify(results)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 502

@app.route('/external/add/<barcode>', methods=['POST'])
def add_external(barcode):
    global next_id
    product, error = fetch_product_by_barcode(barcode)
    if error:
        if error == "Product not found":
            return jsonify({'error': error}), 404
        return jsonify({'error': error}), 502
    data = request.get_json(silent=True) or {}
    item = {
        'id': next_id,
        'name': product['name'],
        'barcode': product['barcode'],
        'category': product['category'],
        'quantity': data.get('quantity', 0),
        'price': data.get('price', 0.0),
        'supplier': product['brand'],
        'description': product['description']
    }
    next_id += 1
    items.append(item)
    return jsonify(item), 201

if __name__ == '__main__':
    app.run(debug=True)
