from flask import Flask, jsonify,request
from database import get_random_customers, get_store_info, get_max_price_product_id\
,get_price_stats,get_product_price_info,add_store,delete_store
import json
import requests

app = Flask(__name__)

@app.route('/customers/show/', methods=['GET'])
def show_random_customers():
    customers = get_random_customers(10) 
    customers_list = []
    for customer in customers:
        customer_dict = {
            "customer_id": customer.customer_id,
            "name": customer.name,
            "surname": customer.surname
        }
        customers_list.append(customer_dict)
    jsdata= json.dumps(customers_list, indent=4, ensure_ascii=False)
    return jsdata

@app.route('/stores/<int:store_id>', methods=['GET'])
def get_store(store_id):
    store_info = get_store_info(store_id) 
    jsdata= json.dumps(store_info, indent=4, ensure_ascii=False)
    return jsdata

@app.route('/prices/max/', methods=['GET'])
def get_max_price():
    product_id = get_max_price_product_id() # Вызываем функцию из database.py для получения product_id товара с максимальной ценой
    if product_id:
        product_info = get_product_price_info() # Вызываем функцию из database.py для получения информации о товаре, цене и дате начала ее действия
    else:
        product_info={} 
    jsdata= json.dumps(product_info, indent=4, ensure_ascii=False)
    return jsdata

@app.route('/prices/stats/<int:product_id>', methods=['GET'])
def get_price_stats_by_product_id(product_id):
    price_stats = get_price_stats(product_id) # Вызываем функцию из database.py для получения статистики по ценам товара
    jsdata= json.dumps(price_stats, indent=4, ensure_ascii=False)
    return jsdata

@app.route("/stores/add", methods=['GET', 'POST'])
def add_store():
    if request.method == 'POST':
        address = request.json['address']
        region = request.json['region']
    else:
        address = request.args.get('address')
        region = request.args.get('region')
        result = add_store(address, region)
    return result

@app.route('/stores/delete/<int:store_id>', methods=['GET', 'POST'])
def delete_store_handler(store_id):
    result = delete_store(store_id) 
    if result:
        return jsonify({"status": "ok"}) 
    else:
        return jsonify({"status": "not found"}) 

app.run("0.0.0.0", port=8080)

