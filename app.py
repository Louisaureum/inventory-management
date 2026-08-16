from flask import Flask, jsonify, request, abort
import requests

app = Flask(__name__)

# OpenFoodFacts wants a user agent so they know who's calling
HEADERS = {"User-Agent": "InventoryManagementSystem/1.0 (student@example.com)"}

# ---- Home route ----

@app.route('/')
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Inventory Management API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            h1 {
                color: #333;
                border-bottom: 3px solid #007bff;
                padding-bottom: 10px;
            }
            h2 {
                color: #007bff;
                margin-top: 30px;
            }
            .endpoint {
                background: white;
                padding: 12px;
                margin: 8px 0;
                border-left: 4px solid #28a745;
                border-radius: 4px;
                font-family: monospace;
            }
            .method {
                font-weight: bold;
                color: #007bff;
            }
            .description {
                color: #666;
                margin-left: 10px;
            }
            .section {
                background: white;
                padding: 20px;
                margin: 20px 0;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .test-link {
                color: #007bff;
                text-decoration: none;
                font-weight: bold;
            }
            .test-link:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>📦 Inventory Management API</h1>
        
        <div class="section">
            <h2>Welcome!</h2>
            <p>This is a Flask REST API for managing inventory items with integration to the OpenFoodFacts database.</p>
        </div>

        <div class="section">
            <h2>📋 CRUD Operations</h2>
            <div class="endpoint">
                <span class="method">GET</span> <code>/items</code>
                <span class="description">- List all inventory items</span>
            </div>
            <div class="endpoint">
                <span class="method">GET</span> <code>/items/&lt;id&gt;</code>
                <span class="description">- Get a specific item by ID</span>
            </div>
            <div class="endpoint">
                <span class="method">POST</span> <code>/items</code>
                <span class="description">- Create a new inventory item</span>
            </div>
            <div class="endpoint">
                <span class="method">PATCH</span> <code>/items/&lt;id&gt;</code>
                <span class="description">- Update an existing item</span>
            </div>
            <div class="endpoint">
                <span class="method">DELETE</span> <code>/items/&lt;id&gt;</code>
                <span class="description">- Delete an item</span>
            </div>
        </div>

        <div class="section">
            <h2>🔍 External API (OpenFoodFacts)</h2>
            <div class="endpoint">
                <span class="method">GET</span> <code>/external/barcode/&lt;barcode&gt;</code>
                <span class="description">- Search for product by barcode</span>
            </div>
            <div class="endpoint">
                <span class="method">GET</span> <code>/external/search?name=&lt;query&gt;</code>
                <span class="description">- Search for products by name</span>
            </div>
            <div class="endpoint">
                <span class="method">POST</span> <code>/external/add/&lt;barcode&gt;</code>
                <span class="description">- Fetch and add product to inventory</span>
            </div>
        </div>

        <div class="section">
            <h2>🚀 Quick Test</h2>
            <p>Try these links:</p>
            <ul>
                <li><a href="/items" class="test-link">View all items</a></li>
                <li><a href="/external/barcode/3017620422003" class="test-link">Search barcode 3017620422003</a></li>
                <li><a href="/external/search?name=milk" class="test-link">Search for "milk"</a></li>
            </ul>
        </div>

        <div class="section">
            <h2>💡 Example Data</h2>
            <p>Create an item with JSON POST to <code>/items</code>:</p>
            <pre>{
    "name": "Milk",
    "barcode": "123456",
    "category": "Dairy",
    "quantity": 5,
    "price": 3.99,
    "supplier": "Farm Fresh",
    "description": "Organic whole milk"
}</pre>
        </div>
    </body>
    </html>
    """
    return html

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
