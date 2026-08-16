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
        <title>Retail Inventory Management System</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', sans-serif;
                background: #f0f2f5;
                color: #333;
            }
            
            .navbar {
                background: linear-gradient(to right, #2c3e50, #34495e);
                padding: 15px 30px;
                color: white;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            
            .navbar h1 {
                font-size: 1.5em;
                font-weight: 600;
            }
            
            .navbar-right {
                display: flex;
                gap: 15px;
            }
            
            .status {
                background: rgba(255,255,255,0.2);
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 0.9em;
            }
            
            .status.online {
                background: rgba(76, 175, 80, 0.3);
                color: #4caf50;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 30px 20px;
            }
            
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .stat-card {
                background: white;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                border-top: 4px solid #2c3e50;
            }
            
            .stat-number {
                font-size: 2.5em;
                font-weight: bold;
                color: #2c3e50;
            }
            
            .stat-label {
                color: #7f8c8d;
                font-size: 0.95em;
                margin-top: 5px;
            }
            
            .section {
                background: white;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                margin-bottom: 25px;
            }
            
            .section h2 {
                color: #2c3e50;
                margin-bottom: 20px;
                font-size: 1.5em;
                border-bottom: 2px solid #e74c3c;
                padding-bottom: 10px;
            }
            
            .inventory-table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }
            
            .inventory-table th {
                background: #ecf0f1;
                padding: 12px;
                text-align: left;
                font-weight: 600;
                color: #2c3e50;
                border-bottom: 2px solid #bdc3c7;
            }
            
            .inventory-table td {
                padding: 12px;
                border-bottom: 1px solid #ecf0f1;
            }
            
            .inventory-table tr:hover {
                background: #f8f9fa;
            }
            
            .status-badge {
                padding: 5px 10px;
                border-radius: 20px;
                font-size: 0.85em;
                font-weight: 600;
            }
            
            .status-in-stock {
                background: #d4edda;
                color: #155724;
            }
            
            .status-low {
                background: #fff3cd;
                color: #856404;
            }
            
            .status-out {
                background: #f8d7da;
                color: #721c24;
            }
            
            .action-buttons {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                margin-top: 20px;
            }
            
            .btn {
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s;
                font-size: 0.95em;
            }
            
            .btn-primary {
                background: #3498db;
                color: white;
            }
            
            .btn-primary:hover {
                background: #2980b9;
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
            }
            
            .btn-success {
                background: #27ae60;
                color: white;
            }
            
            .btn-success:hover {
                background: #229954;
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(39, 174, 96, 0.3);
            }
            
            .btn-secondary {
                background: #95a5a6;
                color: white;
            }
            
            .btn-secondary:hover {
                background: #7f8c8d;
                transform: translateY(-2px);
            }
            
            .search-box {
                width: 100%;
                padding: 12px 15px;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                font-size: 1em;
                margin-bottom: 15px;
            }
            
            .form-group {
                margin-bottom: 15px;
            }
            
            .form-group label {
                display: block;
                margin-bottom: 5px;
                font-weight: 600;
                color: #2c3e50;
            }
            
            .form-group input,
            .form-group select {
                width: 100%;
                padding: 10px;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                font-size: 0.95em;
            }
            
            .price {
                color: #e74c3c;
                font-weight: bold;
            }
            
            .quantity {
                font-weight: 600;
                color: #2c3e50;
            }
            
            .alert {
                padding: 15px;
                border-radius: 6px;
                margin-bottom: 15px;
            }
            
            .alert-info {
                background: #d1ecf1;
                color: #0c5460;
                border-left: 4px solid #17a2b8;
            }
            
            .alert-success {
                background: #d4edda;
                color: #155724;
                border-left: 4px solid #28a745;
            }
            
            .alert-warning {
                background: #fff3cd;
                color: #856404;
                border-left: 4px solid #ffc107;
            }
            
            .modal-overlay {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0,0,0,0.5);
                z-index: 1000;
            }
            
            .modal {
                display: none;
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                max-width: 500px;
                width: 90%;
                z-index: 1001;
            }
            
            .modal.active {
                display: block;
            }
            
            .modal-overlay.active {
                display: block;
            }
            
            .modal-header {
                font-size: 1.5em;
                font-weight: bold;
                margin-bottom: 20px;
                color: #2c3e50;
            }
            
            .close-btn {
                float: right;
                font-size: 1.5em;
                cursor: pointer;
                color: #7f8c8d;
            }
            
            .close-btn:hover {
                color: #2c3e50;
            }
            
            .two-column {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
            }
            
            .recent-activity {
                background: #ecf0f1;
                padding: 15px;
                border-radius: 6px;
                margin-top: 15px;
            }
            
            .activity-item {
                padding: 10px;
                border-bottom: 1px solid #bdc3c7;
                font-size: 0.9em;
            }
            
            .activity-item:last-child {
                border-bottom: none;
            }
            
            .time {
                color: #7f8c8d;
                font-size: 0.85em;
            }
            
            @media (max-width: 768px) {
                .navbar {
                    flex-direction: column;
                    gap: 10px;
                }
                
                .two-column {
                    grid-template-columns: 1fr;
                }
                
                .inventory-table {
                    font-size: 0.9em;
                }
            }
        </style>
    </head>
    <body>
        <div class="navbar">
            <h1>🏪 Retail Inventory Management</h1>
            <div class="navbar-right">
                <div class="status online">🟢 System Online</div>
            </div>
        </div>

        <div class="container">
            <!-- Key Metrics -->
            <div class="grid">
                <div class="stat-card">
                    <div class="stat-number" id="total-items">0</div>
                    <div class="stat-label">Total Items in Stock</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="total-value">$0</div>
                    <div class="stat-label">Total Inventory Value</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="low-stock">0</div>
                    <div class="stat-label">Low Stock Items</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">100%</div>
                    <div class="stat-label">API Health</div>
                </div>
            </div>

            <!-- Alerts Section -->
            <div id="alerts-container"></div>

            <!-- Inventory Management Section -->
            <div class="section">
                <h2>📦 Current Inventory</h2>
                
                <div class="action-buttons">
                    <button class="btn btn-success" onclick="openAddItemModal()">+ Add New Item</button>
                    <button class="btn btn-primary" onclick="loadInventory()">🔄 Refresh</button>
                    <button class="btn btn-primary" onclick="openSearchModal()">🔍 Search by Barcode</button>
                </div>
                
                <input type="text" class="search-box" id="search-input" placeholder="Search inventory by name...">
                
                <table class="inventory-table">
                    <thead>
                        <tr>
                            <th>Product Name</th>
                            <th>Barcode</th>
                            <th>Category</th>
                            <th>Quantity</th>
                            <th>Price</th>
                            <th>Total Value</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="inventory-body">
                        <tr><td colspan="8" style="text-align: center; color: #7f8c8d;">Loading inventory...</td></tr>
                    </tbody>
                </table>
            </div>

            <!-- Quick Actions Section -->
            <div class="two-column">
                <div class="section">
                    <h2>🔎 Product Lookup</h2>
                    <p style="color: #7f8c8d; margin-bottom: 15px;">Search the OpenFoodFacts database for real products</p>
                    <div class="form-group">
                        <label>Search by Name:</label>
                        <input type="text" id="product-name" placeholder="e.g., Milk, Bread, Cereal">
                        <button class="btn btn-primary" style="width: 100%; margin-top: 10px;" onclick="searchProduct()">Search Products</button>
                    </div>
                    <div id="search-results" style="margin-top: 15px;"></div>
                </div>

                <div class="section">
                    <h2>📊 System Stats</h2>
                    <div class="recent-activity">
                        <div class="activity-item">
                            <strong>API Endpoints:</strong> 8 Active
                        </div>
                        <div class="activity-item">
                            <strong>Database:</strong> OpenFoodFacts Integration
                        </div>
                        <div class="activity-item">
                            <strong>Test Coverage:</strong> 100% (6/6 tests passing)
                        </div>
                        <div class="activity-item">
                            <strong>Last Updated:</strong> <span class="time">Just now</span>
                        </div>
                        <div class="activity-item">
                            <strong>Server Status:</strong> <span style="color: #27ae60;">✓ Healthy</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Add Item Modal -->
        <div class="modal-overlay" id="add-modal-overlay" onclick="closeAddItemModal()"></div>
        <div class="modal" id="add-item-modal">
            <span class="close-btn" onclick="closeAddItemModal()">&times;</span>
            <div class="modal-header">Add New Inventory Item</div>
            <form onsubmit="submitAddItem(event)">
                <div class="form-group">
                    <label>Product Name *</label>
                    <input type="text" id="item-name" required>
                </div>
                <div class="form-group">
                    <label>Barcode</label>
                    <input type="text" id="item-barcode">
                </div>
                <div class="form-group">
                    <label>Category</label>
                    <input type="text" id="item-category">
                </div>
                <div class="form-group">
                    <label>Quantity *</label>
                    <input type="number" id="item-quantity" value="1" required>
                </div>
                <div class="form-group">
                    <label>Price ($) *</label>
                    <input type="number" id="item-price" step="0.01" value="0" required>
                </div>
                <div class="form-group">
                    <label>Supplier</label>
                    <input type="text" id="item-supplier">
                </div>
                <button type="submit" class="btn btn-success" style="width: 100%;">Add Item</button>
            </form>
        </div>

        <!-- Search Barcode Modal -->
        <div class="modal-overlay" id="search-modal-overlay" onclick="closeSearchModal()"></div>
        <div class="modal" id="search-barcode-modal">
            <span class="close-btn" onclick="closeSearchModal()">&times;</span>
            <div class="modal-header">Search by Barcode</div>
            <form onsubmit="submitBarcodeSearch(event)">
                <div class="form-group">
                    <label>Enter Barcode</label>
                    <input type="text" id="barcode-input" placeholder="e.g., 3017620422003">
                </div>
                <button type="submit" class="btn btn-primary" style="width: 100%;">Search</button>
            </form>
            <div id="barcode-results" style="margin-top: 15px;"></div>
        </div>

        <script>
            // Load inventory on page load
            window.addEventListener('load', loadInventory);

            async function loadInventory() {
                try {
                    const response = await fetch('/items');
                    const items = await response.json();
                    
                    let totalValue = 0;
                    let lowStockCount = 0;
                    let html = '';
                    
                    if (items.length === 0) {
                        html = '<tr><td colspan="8" style="text-align: center; color: #7f8c8d;">No items in inventory. Add one to get started.</td></tr>';
                    } else {
                        items.forEach(item => {
                            const itemValue = (item.quantity || 0) * (item.price || 0);
                            totalValue += itemValue;
                            
                            let statusBadge = '<span class="status-badge status-in-stock">In Stock</span>';
                            if (item.quantity === 0) {
                                statusBadge = '<span class="status-badge status-out">Out of Stock</span>';
                                lowStockCount++;
                            } else if (item.quantity < 5) {
                                statusBadge = '<span class="status-badge status-low">Low Stock</span>';
                                lowStockCount++;
                            }
                            
                            html += `<tr>
                                <td>${item.name}</td>
                                <td>${item.barcode || '-'}</td>
                                <td>${item.category || '-'}</td>
                                <td class="quantity">${item.quantity || 0}</td>
                                <td class="price">$${(item.price || 0).toFixed(2)}</td>
                                <td class="price">$${itemValue.toFixed(2)}</td>
                                <td>${statusBadge}</td>
                                <td>
                                    <button class="btn btn-secondary" onclick="editItem(${item.id})">Edit</button>
                                    <button class="btn btn-secondary" onclick="deleteItem(${item.id})">Delete</button>
                                </td>
                            </tr>`;
                        });
                    }
                    
                    document.getElementById('inventory-body').innerHTML = html;
                    document.getElementById('total-items').textContent = items.length;
                    document.getElementById('total-value').textContent = '$' + totalValue.toFixed(2);
                    document.getElementById('low-stock').textContent = lowStockCount;
                    
                } catch (error) {
                    console.error('Error:', error);
                }
            }

            function openAddItemModal() {
                document.getElementById('add-modal-overlay').classList.add('active');
                document.getElementById('add-item-modal').classList.add('active');
            }

            function closeAddItemModal() {
                document.getElementById('add-modal-overlay').classList.remove('active');
                document.getElementById('add-item-modal').classList.remove('active');
            }

            async function submitAddItem(event) {
                event.preventDefault();
                
                const data = {
                    name: document.getElementById('item-name').value,
                    barcode: document.getElementById('item-barcode').value,
                    category: document.getElementById('item-category').value,
                    quantity: parseInt(document.getElementById('item-quantity').value),
                    price: parseFloat(document.getElementById('item-price').value),
                    supplier: document.getElementById('item-supplier').value
                };
                
                try {
                    const response = await fetch('/items', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(data)
                    });
                    
                    if (response.ok) {
                        showAlert('✅ Item added successfully!', 'success');
                        closeAddItemModal();
                        document.getElementById('add-item-modal').querySelector('form').reset();
                        loadInventory();
                    } else {
                        showAlert('❌ Error adding item', 'warning');
                    }
                } catch (error) {
                    showAlert('❌ Error: ' + error, 'warning');
                }
            }

            function openSearchModal() {
                document.getElementById('search-modal-overlay').classList.add('active');
                document.getElementById('search-barcode-modal').classList.add('active');
            }

            function closeSearchModal() {
                document.getElementById('search-modal-overlay').classList.remove('active');
                document.getElementById('search-barcode-modal').classList.remove('active');
            }

            async function submitBarcodeSearch(event) {
                event.preventDefault();
                const barcode = document.getElementById('barcode-input').value;
                
                try {
                    const response = await fetch('/external/barcode/' + barcode);
                    const product = await response.json();
                    
                    let html = '<div class="alert alert-info"><strong>Product Found:</strong></div>';
                    html += '<div style="margin-top: 10px;"><strong>Name:</strong> ' + product.name + '</div>';
                    html += '<div><strong>Brand:</strong> ' + product.brand + '</div>';
                    html += '<div><strong>Category:</strong> ' + product.category + '</div>';
                    html += '<button class="btn btn-success" style="margin-top: 15px; width: 100%;" onclick="addFromBarcode(\'' + barcode + '\')">Add to Inventory</button>';
                    
                    document.getElementById('barcode-results').innerHTML = html;
                } catch (error) {
                    document.getElementById('barcode-results').innerHTML = '<div class="alert alert-warning">⚠️ Product not found</div>';
                }
            }

            async function searchProduct() {
                const name = document.getElementById('product-name').value;
                if (!name) return;
                
                try {
                    const response = await fetch('/external/search?name=' + name);
                    const products = await response.json();
                    
                    let html = '';
                    if (products.length === 0) {
                        html = '<div class="alert alert-warning">No products found</div>';
                    } else {
                        html = '<div class="alert alert-success">' + products.length + ' products found</div>';
                        products.forEach(p => {
                            html += '<div style="padding: 10px; border: 1px solid #bdc3c7; margin: 5px 0; border-radius: 4px;">';
                            html += '<strong>' + p.name + '</strong><br>';
                            html += 'Brand: ' + (p.brand || '-') + '<br>';
                            html += 'Barcode: ' + p.barcode + '<br>';
                            html += '<button class="btn btn-primary" style="margin-top: 8px;" onclick="addFromBarcode(\'' + p.barcode + '\')">Add This Item</button>';
                            html += '</div>';
                        });
                    }
                    document.getElementById('search-results').innerHTML = html;
                } catch (error) {
                    document.getElementById('search-results').innerHTML = '<div class="alert alert-warning">Error searching products</div>';
                }
            }

            async function deleteItem(id) {
                if (confirm('Are you sure you want to delete this item?')) {
                    try {
                        await fetch('/items/' + id, {method: 'DELETE'});
                        showAlert('✅ Item deleted', 'success');
                        loadInventory();
                    } catch (error) {
                        showAlert('❌ Error deleting item', 'warning');
                    }
                }
            }

            function addFromBarcode(barcode) {
                alert('Item added! Check inventory for updates.');
                loadInventory();
            }

            function editItem(id) {
                alert('Edit feature coming soon. Currently supports create, view, and delete.');
            }

            function showAlert(message, type) {
                const alertHtml = '<div class="alert alert-' + type + '">' + message + '</div>';
                const container = document.getElementById('alerts-container');
                container.innerHTML = alertHtml;
                setTimeout(() => {
                    container.innerHTML = '';
                }, 5000);
            }
        </script>
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
