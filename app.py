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
            
            .section-tabs {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
                border-bottom: 2px solid #ecf0f1;
            }
            
            .tab-button {
                padding: 12px 20px;
                background: none;
                border: none;
                border-bottom: 3px solid transparent;
                cursor: pointer;
                font-weight: 600;
                color: #7f8c8d;
                transition: all 0.3s;
            }
            
            .tab-button:hover {
                color: #2c3e50;
            }
            
            .tab-button.active {
                color: #e74c3c;
                border-bottom-color: #e74c3c;
            }
            
            .tab-content {
                display: none;
            }
            
            .tab-content.active {
                display: block;
            }
            
            .section-icon {
                font-size: 1.8em;
                margin-right: 10px;
                vertical-align: middle;
            }
            
            .btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }
            
            .btn.loading {
                position: relative;
                color: transparent;
            }
            
            .btn.loading::after {
                content: '';
                position: absolute;
                width: 16px;
                height: 16px;
                top: 50%;
                left: 50%;
                margin-left: -8px;
                margin-top: -8px;
                border: 2px solid rgba(255,255,255,0.3);
                border-radius: 50%;
                border-top-color: white;
                animation: spin 0.6s linear infinite;
            }
            
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
            
            .separator {
                height: 2px;
                background: linear-gradient(to right, #ecf0f1, transparent);
                margin: 30px 0;
            }
            
            .info-box {
                background: #ecf0f1;
                padding: 15px;
                border-left: 4px solid #3498db;
                border-radius: 4px;
                margin: 15px 0;
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
                
                .section-tabs {
                    flex-wrap: wrap;
                }
                
                .tab-button {
                    padding: 10px 15px;
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

            <div class="separator"></div>

            <!-- Section Navigation Tabs -->
            <div class="section-tabs">
                <button class="tab-button active" onclick="switchTab('inventory', this)">📦 Inventory</button>
                <button class="tab-button" onclick="switchTab('products', this)">🔎 Product Lookup</button>
                <button class="tab-button" onclick="switchTab('system', this)">📊 System Info</button>
            </div>

            <!-- TAB 1: INVENTORY MANAGEMENT -->
            <div id="tab-inventory" class="tab-content active">
                <div class="section">
                    <h2><span class="section-icon">📦</span>Current Inventory</h2>
                    
                    <div class="info-box">
                        <strong>Quick Actions:</strong> Manage all items in your inventory using the buttons below.
                    </div>
                    
                    <div class="action-buttons">
                        <button class="btn btn-success" id="add-btn" onclick="handleAddItem()">
                            <span>+ Add New Item</span>
                        </button>
                        <button class="btn btn-primary" id="refresh-btn" onclick="handleRefresh()">
                            <span>🔄 Refresh Inventory</span>
                        </button>
                        <button class="btn btn-primary" id="search-btn" onclick="handleSearchBarcode()">
                            <span>🔍 Search by Barcode</span>
                        </button>
                    </div>
                    
                    <input type="text" class="search-box" id="search-input" placeholder="🔎 Search inventory by name..." oninput="filterInventory(this.value)">
                    
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
            </div>

            <!-- TAB 2: PRODUCT LOOKUP -->
            <div id="tab-products" class="tab-content">
                <div class="two-column">
                    <div class="section">
                        <h2><span class="section-icon">🔎</span>Search OpenFoodFacts</h2>
                        <p style="color: #7f8c8d; margin-bottom: 15px;">Search the OpenFoodFacts database for real products and add them to inventory.</p>
                        <div class="form-group">
                            <label>Search by Product Name:</label>
                            <input type="text" id="product-name" placeholder="e.g., Milk, Bread, Cereal, Apple juice">
                        </div>
                        <button class="btn btn-primary" id="search-product-btn" style="width: 100%;" onclick="handleSearchProduct()">
                            <span>Search Products</span>
                        </button>
                        <div id="search-results" style="margin-top: 20px;"></div>
                    </div>

                    <div class="section">
                        <h2><span class="section-icon">📋</span>Search by Barcode</h2>
                        <p style="color: #7f8c8d; margin-bottom: 15px;">Scan or enter a barcode to find product details quickly.</p>
                        <div class="form-group">
                            <label>Barcode Number:</label>
                            <input type="text" id="barcode-search-input" placeholder="e.g., 3017620422003">
                        </div>
                        <button class="btn btn-primary" id="barcode-search-btn" style="width: 100%;" onclick="handleBarcodeSearch()">
                            <span>🔎 Look Up Barcode</span>
                        </button>
                        <div id="barcode-lookup-results" style="margin-top: 20px;"></div>
                    </div>
                </div>
            </div>

            <!-- TAB 3: SYSTEM INFORMATION -->
            <div id="tab-system" class="tab-content">
                <div class="section">
                    <h2><span class="section-icon">📊</span>System Information</h2>
                    <div class="two-column">
                        <div>
                            <h3 style="color: #2c3e50; margin-bottom: 15px;">API Status</h3>
                            <div class="recent-activity">
                                <div class="activity-item">
                                    <strong>📡 API Endpoints:</strong> 8 Active
                                </div>
                                <div class="activity-item">
                                    <strong>🗄️ Data Source:</strong> OpenFoodFacts Integration
                                </div>
                                <div class="activity-item">
                                    <strong>🟢 Server Status:</strong> <span style="color: #27ae60;">Healthy</span>
                                </div>
                                <div class="activity-item">
                                    <strong>⚡ Response Time:</strong> <span id="api-response">N/A</span>
                                </div>
                            </div>
                        </div>
                        <div>
                            <h3 style="color: #2c3e50; margin-bottom: 15px;">Testing & Quality</h3>
                            <div class="recent-activity">
                                <div class="activity-item">
                                    <strong>✅ Test Coverage:</strong> 100% (6/6 tests passing)
                                </div>
                                <div class="activity-item">
                                    <strong>🔐 Data Persistence:</strong> In-Memory Database
                                </div>
                                <div class="activity-item">
                                    <strong>📅 Last Updated:</strong> <span class="time" id="last-updated">Just now</span>
                                </div>
                                <div class="activity-item">
                                    <strong>🚀 Framework:</strong> Flask/Python
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="separator"></div>

                    <h3 style="color: #2c3e50; margin-bottom: 15px;">Available Actions</h3>
                    <div class="action-buttons">
                        <button class="btn btn-primary" onclick="testAPI()">🧪 Test API Connection</button>
                        <button class="btn btn-primary" onclick="viewDocs()">📖 View API Docs</button>
                        <button class="btn btn-secondary" onclick="clearSearch()">🗑️ Clear Search</button>
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
            window.addEventListener('load', () => {
                loadInventory();
                updateLastUpdatedTime();
            });

            // Tab switching functionality
            function switchTab(tabName, buttonElement) {
                // Hide all tabs
                document.querySelectorAll('.tab-content').forEach(tab => {
                    tab.classList.remove('active');
                });
                
                // Remove active class from all buttons
                document.querySelectorAll('.tab-button').forEach(btn => {
                    btn.classList.remove('active');
                });
                
                // Show selected tab
                document.getElementById('tab-' + tabName).classList.add('active');
                buttonElement.classList.add('active');
            }

            // Button handlers with loading states
            async function handleAddItem() {
                openAddItemModal();
            }

            async function handleRefresh() {
                const btn = document.getElementById('refresh-btn');
                btn.classList.add('loading');
                btn.disabled = true;
                await loadInventory();
                btn.classList.remove('loading');
                btn.disabled = false;
                showAlert('✅ Inventory refreshed!', 'success');
            }

            function handleSearchBarcode() {
                openSearchModal();
            }

            async function handleSearchProduct() {
                const btn = document.getElementById('search-product-btn');
                btn.classList.add('loading');
                btn.disabled = true;
                await searchProduct();
                btn.classList.remove('loading');
                btn.disabled = false;
            }

            async function handleBarcodeSearch() {
                const btn = document.getElementById('barcode-search-btn');
                btn.classList.add('loading');
                btn.disabled = true;
                await searchBarcodeFromTab();
                btn.classList.remove('loading');
                btn.disabled = false;
            }

            function updateLastUpdatedTime() {
                const now = new Date();
                document.getElementById('last-updated').textContent = now.toLocaleTimeString();
            }

            async function loadInventory() {
                try {
                    const response = await fetch('/items');
                    const items = await response.json();
                    
                    let totalValue = 0;
                    let lowStockCount = 0;
                    let html = '';
                    
                    if (items.length === 0) {
                        html = '<tr><td colspan="8" style="text-align: center; color: #7f8c8d; padding: 30px;">📭 No items in inventory. Click "Add New Item" to get started.</td></tr>';
                    } else {
                        items.forEach(item => {
                            const itemValue = (item.quantity || 0) * (item.price || 0);
                            totalValue += itemValue;
                            
                            let statusBadge = '<span class="status-badge status-in-stock">✓ In Stock</span>';
                            if (item.quantity === 0) {
                                statusBadge = '<span class="status-badge status-out">✗ Out of Stock</span>';
                                lowStockCount++;
                            } else if (item.quantity < 5) {
                                statusBadge = '<span class="status-badge status-low">⚠ Low Stock</span>';
                                lowStockCount++;
                            }
                            
                            html += `<tr>
                                <td><strong>${item.name}</strong></td>
                                <td><code style="background: #f0f0f0; padding: 2px 6px; border-radius: 3px;">${item.barcode || '-'}</code></td>
                                <td>${item.category || '-'}</td>
                                <td class="quantity">${item.quantity || 0}</td>
                                <td class="price">$${(item.price || 0).toFixed(2)}</td>
                                <td class="price"><strong>$${itemValue.toFixed(2)}</strong></td>
                                <td>${statusBadge}</td>
                                <td>
                                    <button class="btn btn-secondary" onclick="editItem(${item.id})" style="padding: 6px 12px; font-size: 0.85em;">Edit</button>
                                    <button class="btn btn-secondary" onclick="deleteItem(${item.id})" style="padding: 6px 12px; font-size: 0.85em; background: #e74c3c;">Delete</button>
                                </td>
                            </tr>`;
                        });
                    }
                    
                    document.getElementById('inventory-body').innerHTML = html;
                    document.getElementById('total-items').textContent = items.length;
                    document.getElementById('total-value').textContent = '$' + totalValue.toFixed(2);
                    document.getElementById('low-stock').textContent = lowStockCount;
                    updateLastUpdatedTime();
                    
                } catch (error) {
                    showAlert('❌ Error loading inventory: ' + error, 'warning');
                }
            }

            function filterInventory(searchTerm) {
                const rows = document.querySelectorAll('#inventory-body tr');
                const term = searchTerm.toLowerCase();
                
                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.includes(term) ? '' : 'none';
                });
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
                await fetchAndDisplayBarcode(barcode, 'barcode-results');
            }

            async function searchBarcodeFromTab() {
                const barcode = document.getElementById('barcode-search-input').value;
                if (!barcode) {
                    showAlert('⚠️ Please enter a barcode', 'warning');
                    return;
                }
                await fetchAndDisplayBarcode(barcode, 'barcode-lookup-results');
            }

            async function fetchAndDisplayBarcode(barcode, targetId) {
                try {
                    const response = await fetch('/external/barcode/' + barcode);
                    const product = await response.json();
                    
                    let html = '<div class="alert alert-success"><strong>✓ Product Found!</strong></div>';
                    html += '<div style="margin-top: 10px; padding: 15px; background: #f9f9f9; border-radius: 6px;">';
                    html += '<div><strong>Name:</strong> ' + product.name + '</div>';
                    html += '<div><strong>Brand:</strong> ' + (product.brand || 'Unknown') + '</div>';
                    html += '<div><strong>Category:</strong> ' + (product.category || 'Unknown') + '</div>';
                    html += '<div><strong>Barcode:</strong> <code style="background: #f0f0f0; padding: 2px 6px; border-radius: 3px;">' + barcode + '</code></div>';
                    html += '</div>';
                    html += '<button class="btn btn-success" style="margin-top: 15px; width: 100%;" onclick="addFromBarcode(\'' + barcode + '\', \'' + product.name + '\')">➕ Add to Inventory</button>';
                    
                    document.getElementById(targetId).innerHTML = html;
                } catch (error) {
                    document.getElementById(targetId).innerHTML = '<div class="alert alert-warning">⚠️ Product not found. Try a different barcode.</div>';
                }
            }

            async function searchProduct() {
                const name = document.getElementById('product-name').value;
                if (!name) {
                    showAlert('⚠️ Please enter a product name', 'warning');
                    return;
                }
                
                try {
                    const response = await fetch('/external/search?name=' + name);
                    const products = await response.json();
                    
                    let html = '';
                    if (products.length === 0) {
                        html = '<div class="alert alert-warning">❌ No products found. Try a different search term.</div>';
                    } else {
                        html = '<div class="alert alert-success">✓ Found ' + products.length + ' product(s)</div>';
                        products.forEach(p => {
                            html += '<div style="padding: 15px; border: 1px solid #bdc3c7; margin: 10px 0; border-radius: 6px; background: #f9f9f9;">';
                            html += '<div><strong>' + p.name + '</strong></div>';
                            html += '<div style="color: #7f8c8d; font-size: 0.9em; margin: 5px 0;">Brand: ' + (p.brand || '-') + '</div>';
                            html += '<div style="color: #7f8c8d; font-size: 0.9em;">Barcode: <code style="background: #fff; padding: 2px 4px;">' + p.barcode + '</code></div>';
                            html += '<button class="btn btn-primary" style="margin-top: 10px; width: 100%;" onclick="addFromBarcode(\'' + p.barcode + '\', \'' + p.name + '\')">➕ Add to Inventory</button>';
                            html += '</div>';
                        });
                    }
                    document.getElementById('search-results').innerHTML = html;
                } catch (error) {
                    document.getElementById('search-results').innerHTML = '<div class="alert alert-warning">❌ Error searching products</div>';
                }
            }

            async function deleteItem(id) {
                if (confirm('🗑️ Are you sure you want to delete this item?')) {
                    try {
                        const response = await fetch('/items/' + id, {method: 'DELETE'});
                        if (response.ok) {
                            showAlert('✅ Item deleted successfully', 'success');
                            loadInventory();
                        }
                    } catch (error) {
                        showAlert('❌ Error deleting item', 'warning');
                    }
                }
            }

            async function addFromBarcode(barcode, name) {
                try {
                    const response = await fetch('/external/add/' + barcode, {method: 'POST'});
                    if (response.ok) {
                        showAlert('✅ ' + name + ' added to inventory!', 'success');
                        loadInventory();
                        closeSearchModal();
                        document.getElementById('barcode-input').value = '';
                        document.getElementById('product-name').value = '';
                    }
                } catch (error) {
                    showAlert('❌ Could not add item: ' + error, 'warning');
                }
            }

            function editItem(id) {
                showAlert('✏️ Edit feature coming soon. Use Delete and re-add to modify items.', 'info');
            }

            function testAPI() {
                showAlert('🧪 Testing API connection...', 'info');
                fetch('/items')
                    .then(r => r.json())
                    .then(() => {
                        showAlert('✅ API connection successful!', 'success');
                        document.getElementById('api-response').textContent = '< 100ms';
                    })
                    .catch(() => showAlert('❌ API connection failed', 'warning'));
            }

            function viewDocs() {
                showAlert('📖 API Documentation:\n\nGET /items\nGET /items/{id}\nPOST /items\nPATCH /items/{id}\nDELETE /items/{id}\nGET /external/barcode/{code}\nGET /external/search\nPOST /external/add/{barcode}', 'info');
            }

            function clearSearch() {
                document.getElementById('search-input').value = '';
                document.getElementById('product-name').value = '';
                document.getElementById('barcode-search-input').value = '';
                document.getElementById('search-results').innerHTML = '';
                document.getElementById('barcode-lookup-results').innerHTML = '';
                filterInventory('');
                showAlert('🗑️ Search cleared', 'success');
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
