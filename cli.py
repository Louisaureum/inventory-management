import argparse
import json
import requests

BASE_URL = "http://127.0.0.1:5000"

def print_response(resp):
    try:
        print(json.dumps(resp.json(), indent=2))
    except:
        print(resp.status_code)

def list_items(args):
    resp = requests.get(f"{BASE_URL}/items")
    print_response(resp)

def get_item(args):
    resp = requests.get(f"{BASE_URL}/items/{args.id}")
    print_response(resp)

def add_item(args):
    payload = {
        "name": args.name,
        "barcode": args.barcode,
        "category": args.category,
        "quantity": args.quantity,
        "price": args.price,
        "supplier": args.supplier,
        "description": args.description
    }
    resp = requests.post(f"{BASE_URL}/items", json=payload)
    print_response(resp)

def update_item(args):
    payload = {}
    for field in ["name", "barcode", "category", "quantity", "price", "supplier", "description"]:
        val = getattr(args, field, None)
        if val is not None:
            payload[field] = val
    resp = requests.patch(f"{BASE_URL}/items/{args.id}", json=payload)
    print_response(resp)

def delete_item(args):
    resp = requests.delete(f"{BASE_URL}/items/{args.id}")
    print_response(resp)

def search_barcode(args):
    resp = requests.get(f"{BASE_URL}/external/barcode/{args.barcode}")
    print_response(resp)

def search_name(args):
    resp = requests.get(f"{BASE_URL}/external/search", params={"name": args.name})
    print_response(resp)

def add_external(args):
    payload = {"quantity": args.quantity, "price": args.price}
    resp = requests.post(f"{BASE_URL}/external/add/{args.barcode}", json=payload)
    print_response(resp)

def main():
    parser = argparse.ArgumentParser(description="Inventory CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("list", help="List all items")
    p.set_defaults(func=list_items)

    p = sub.add_parser("get", help="Get one item")
    p.add_argument("id", type=int)
    p.set_defaults(func=get_item)

    p = sub.add_parser("add", help="Add item")
    p.add_argument("--name", required=True)
    p.add_argument("--barcode", default="")
    p.add_argument("--category", default="")
    p.add_argument("--quantity", type=int, default=0)
    p.add_argument("--price", type=float, default=0.0)
    p.add_argument("--supplier", default="")
    p.add_argument("--description", default="")
    p.set_defaults(func=add_item)

    p = sub.add_parser("update", help="Update item")
    p.add_argument("id", type=int)
    p.add_argument("--name")
    p.add_argument("--barcode")
    p.add_argument("--category")
    p.add_argument("--quantity", type=int)
    p.add_argument("--price", type=float)
    p.add_argument("--supplier")
    p.add_argument("--description")
    p.set_defaults(func=update_item)

    p = sub.add_parser("delete", help="Delete item")
    p.add_argument("id", type=int)
    p.set_defaults(func=delete_item)

    p = sub.add_parser("search-barcode", help="Search by barcode")
    p.add_argument("barcode")
    p.set_defaults(func=search_barcode)

    p = sub.add_parser("search-name", help="Search by name")
    p.add_argument("name")
    p.set_defaults(func=search_name)

    p = sub.add_parser("add-external", help="Add external product by barcode")
    p.add_argument("barcode")
    p.add_argument("--quantity", type=int, default=0)
    p.add_argument("--price", type=float, default=0.0)
    p.set_defaults(func=add_external)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
