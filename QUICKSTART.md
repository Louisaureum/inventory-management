# Quick Start Guide

## Running the Flask Server

1. Activate the virtual environment:
   ```bash
   .\venv\Scripts\activate
   ```

2. Run the Flask app:
   ```bash
   python app.py
   ```

   The server will start at `http://127.0.0.1:5000`

## Testing the API with curl

Open a new terminal (with venv activated) and run:

**List all items:**
```bash
curl http://127.0.0.1:5000/items
```

**Create an item:**
```bash
curl -X POST http://127.0.0.1:5000/items -H "Content-Type: application/json" -d "{\"name\":\"Coffee\",\"quantity\":10,\"price\":12.99}"
```

**Get one item:**
```bash
curl http://127.0.0.1:5000/items/1
```

**Update an item:**
```bash
curl -X PATCH http://127.0.0.1:5000/items/1 -H "Content-Type: application/json" -d "{\"price\":14.99}"
```

**Delete an item:**
```bash
curl -X DELETE http://127.0.0.1:5000/items/1
```

**Search external API by barcode:**
```bash
curl http://127.0.0.1:5000/external/barcode/3017620422003
```

**Search external API by name:**
```bash
curl "http://127.0.0.1:5000/external/search?name=chocolate"
```

**Add product from external API to inventory:**
```bash
curl -X POST http://127.0.0.1:5000/external/add/3017620422003 -H "Content-Type: application/json" -d "{\"quantity\":5,\"price\":3.99}"
```

## Using the CLI

In a separate terminal (with venv activated):

```bash
# List all items
python cli.py list

# Get one item
python cli.py get 1

# Add a new item
python cli.py add --name "Chocolate" --quantity 20 --price 8.99

# Update an item
python cli.py update 1 --quantity 15

# Delete an item
python cli.py delete 1

# Search OpenFoodFacts by barcode
python cli.py search-barcode 3017620422003

# Search OpenFoodFacts by name
python cli.py search-name "coffee"

# Add external product to inventory
python cli.py add-external 3017620422003 --quantity 2 --price 3.99
```

## Running Tests

```bash
pytest test_app.py -v
```

All 6 tests should pass:
- `test_list_empty` - GET /items returns empty list
- `test_create_and_get` - POST creates item, GET retrieves it
- `test_update` - PATCH updates item fields
- `test_delete` - DELETE removes item
- `test_external_barcode_mock` - External API barcode search works
- `test_add_external_mock` - Adding external product to inventory works

## Project Structure

- `app.py` - Main Flask application with CRUD routes and external API integration
- `cli.py` - Command-line interface for the API
- `test_app.py` - Unit tests using pytest
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation
- `.gitignore` - Git ignore file
- `venv/` - Virtual environment (isolated Python packages)
