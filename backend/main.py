from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from database import engine, get_db, Base
from models import ProductModel, CartItemModel, OrderModel
from pydantic import BaseModel
from typing import List, Optional

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProductBase(BaseModel):
    name: str
    category: str
    price: float
    image: str
    description: str

class Product(ProductBase):
    id: int
class Order(BaseModel):
    id: int
    total_price: float
    status: str
class Category(BaseModel):
    name: str

class CartItem(BaseModel):
    product_id: int
    quantity: int



@app.get("/products", response_model=List)
def get_products(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()

@app.get("/cart", response_model=List[CartItem])
def get_cart(db: Session = Depends(get_db)):
    return db.query(CartItemModel).all()

@app.post("/cart/add/{product_id}")
def add_to_cart(product_id: int, db: Session = Depends(get_db)):
    
    item = db.query(CartItemModel).filter(CartItemModel.product_id == product_id).first()
    if item:
        item.quantity += 1
    else:
        item = CartItemModel(product_id=product_id, quantity=1)
        db.add(item)
    db.commit()
    return {"message": "Added to cart"}

@app.post("/orders")
def create_order(db: Session = Depends(get_db)):
    cart_items = db.query(CartItemModel).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    
    total = 0
    for item in cart_items:
        prod = db.query(ProductModel).filter(ProductModel.id == item.product_id).first()
        total += prod.price * item.quantity
    
    new_order = OrderModel(total_price=total)
    db.add(new_order)
    db.query(CartItemModel).delete() 
    db.commit()
    return new_order

@app.get("/orders", response_model=List[Order])
def get_orders():
    return list(orders_db.values())

@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders_db[order_id]