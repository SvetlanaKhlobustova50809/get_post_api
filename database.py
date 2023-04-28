import pandas as pd
import datetime
import random
import itertools


from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table, select, func, text
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import  Integer, String, Column, DateTime, ForeignKey, Numeric

USERNAME = "augustru"  # замените на свой логин

connection_string = f"postgresql+psycopg2://{USERNAME}:@localhost:5433/{USERNAME}"
engine = create_engine(connection_string)

meta = MetaData() 
meta.reflect(bind = engine) 

customers = Table("customers", meta, autoload_with=engine) 
products = Table("products", meta, autoload_with=engine) 
stores = Table("stores", meta, autoload_with=engine) 
prices = Table("prices", meta, autoload_with=engine) 
sales = Table("sales", meta, autoload_with=engine) 

Base = automap_base() 
Base.prepare(autoload_with=engine) 

Customer = Base.classes.customers 
Product = Base.classes.products 
Store = Base.classes.stores 
Price = Base.classes.prices 
Sale = Base.classes.sales 

Session = sessionmaker(bind=engine)
session = Session()

session = Session(bind=engine)

def get_random_customers(count):
    customers = session.query(Customer).order_by(func.random()).limit(count).all() 
    return customers

def get_store_info(store_id):
    store = session.query(Store).filter_by(store_id=store_id).first() 
    if store:
        store_info = {
            "store_id": store.store_id,
            "address": store.address,
            "region": store.region
        }
    else:
        store_info = {} 
    return store_info


def get_max_price_product_id():
    stats = session.query(func.max(Price.price).label("max_price")).first()
    if stats:
        price = int(stats.max_price)
    product_id = session.query(Price.product_id).filter(Price.price == price).first()[-1]
    return product_id

def get_product_price_info():
    product_id = get_max_price_product_id()

    if product_id:
        return {
        "product_id": session.query(Product.product_id).filter(Product.product_id == product_id).first()[0],
        "name": session.query(Product.name).filter(Product.product_id == product_id).first()[0],
        "category": session.query(Product.category).filter(Product.product_id == product_id).first()[0],
        "brand": session.query(Product.brand).filter(Product.product_id == product_id).first()[0],
        "price": session.query(Price.price).filter(Price.product_id == product_id).first()[0],
        "start_date": str(session.query(Price.start_date).filter(Price.product_id == product_id).first()[0])
        }
    else:
        return {}


def get_price_stats(product_id):
# Запрос на получение статистики по ценам товара
    stats = session.query(
    func.count(Price.price).label("count"),
    func.count(Store.store_id.distinct()).label("stores_count"),
    func.max(Price.price).label("max_price"),
    func.min(Price.price).label("min_price"),
    func.avg(Price.price).label("avg_price")
    ).filter(Price.product_id == product_id).first()

    if stats:
        return {
        "count": stats.count,
        "stores_count": stats.stores_count,
        "max_price": stats.max_price,
        "min_price": stats.min_price,
        "avg_price": stats.avg_price
        }
    else:
        return {} # Возвращаем пустой словарь, если такого товара нет


def add_store(address,region):

    store = Store(address=address, region=region)
    session.add(store)
    session.commit()
    return {"store_id": store.store_id}


def delete_store(store_id):
    store = session.query(Store).filter_by(store_id=store_id).first()
    if store:
        session.delete(store)
        session.commit()
        return True 
    else:
        return False