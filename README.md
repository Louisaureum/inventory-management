# Inventory Management System

This is a Flask REST API for managing inventory. It has CRUD operations and can fetch product info from OpenFoodFacts.

## Setup

1. Clone the repo.
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run the app: `python app.py`

## API Endpoints

- `GET /items` - list all items
- `GET /items/<id>` - get one item
- `POST /items` - create item (JSON body with `name` required)
- `PATCH /items/<id>` - update item fields
- `DELETE /items/<id>` - delete item
- `GET /external/barcode/<barcode>` - fetch product by barcode from OpenFoodFacts
- `GET /external/search?name=<name>` - search products by name
- `POST /external/add/<barcode>` - fetch product and add to inventory

## CLI

Run the Flask app first, then use these commands:

```
python cli.py list
python cli.py get 1
python cli.py add --name "Coffee" --quantity 10 --price 12.99
python cli.py update 1 --quantity 15
python cli.py delete 1
python cli.py search-barcode 3017620422003
python cli.py search-name "chocolate"
python cli.py add-external 3017620422003 --quantity 2 --price 3.99
```

## Tests

Run `pytest` to execute unit tests.

## Notes

- Inventory is stored in memory; restarting the server resets it.
- The external API calls use a User-Agent header; change it if needed.
