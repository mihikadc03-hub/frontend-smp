from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

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

class Category(BaseModel):
    name: str

class CartItem(BaseModel):
    product_id: int
    quantity: int = 1

class Order(BaseModel):
    id: int
    items: List[CartItem]
    total_price: float
    status: str = "Pending"

class User(BaseModel):
    username: str
    password: str

products_db = {
    6: Product(id=6, name="Adjustable Desk Lamp", category="Furniture", price=27.99, image="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?q=80&w=1200&auto=format&fit=crop", description="Adjustable desk lamp with multiple brightness modes and USB charging."),
    7: Product(id=7, name="Wool Merino Beanie", category="Apparel", price=19.0, image="https://images.unsplash.com/photo-1521369909029-2afed882baee?q=80&w=1200&auto=format&fit=crop", description="Warm merino wool beanie with breathable ribbed knit."),
    8: Product(id=8, name="Bamboo Cutting Board", category="Kitchen", price=24.5, image="https://images.unsplash.com/photo-1509440159596-0249088772ff?q=80&w=1200&auto=format&fit=crop", description="Large antimicrobial bamboo cutting board with juice groove."),
    9: Product(id=9, name="Wireless Charger Pad", category="Electronics", price=18.0, image="https://images.unsplash.com/photo-1585338447937-7082f8fc763d?q=80&w=1200&auto=format&fit=crop", description="Slim Qi-compatible wireless charging pad with fast charging."),
    10: Product(id=10, name="Stainless Water Bottle", category="Outdoors", price=29.99, image="https://images.unsplash.com/photo-1602143407151-7111542de6e8?q=80&w=1200&auto=format&fit=crop", description="Vacuum insulated stainless steel bottle for hot and cold drinks."),
    11: Product(id=11, name="Canvas Tote Bag", category="Apparel", price=14.0, image="https://images.unsplash.com/photo-1542291026-7eec264c27ff?q=80&w=1200&auto=format&fit=crop", description="Heavy-duty canvas tote bag with reinforced handles."),
    12: Product(id=12, name="Adjustable Dumbbell 20kg", category="Fitness", price=79.0, image="https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=1200&auto=format&fit=crop", description="Compact adjustable dumbbell replacing multiple weights.")
}

users_db = {}
cart_db = {}
orders_db = {}
order_id_counter = 1

@app.post("/register")
def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User exists")
    users_db[user.username] = user.password
    return {"username": user.username}

@app.post("/login")
def login(user: User):
    if user.username not in users_db or users_db[user.username] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": user.username}

@app.get("/products", response_model=List[Product])
def get_products(category: Optional[str] = None, max_price: Optional[float] = None, search: Optional[str] = None):
    results = list(products_db.values())
    
    if category and category != "All":
        results = [p for p in results if p.category == category]
    if max_price is not None:
        results = [p for p in results if p.price <= max_price]
    if search:
        results = [p for p in results if search.lower() in p.name.lower()]
        
    return results

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return products_db[product_id]

@app.post("/products", response_model=Product)
def create_product(product: ProductBase):
    new_id = max(products_db.keys()) + 1 if products_db else 1
    new_product = Product(id=new_id, **product.model_dump())
    products_db[new_id] = new_product
    return new_product

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductBase):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    updated_product = Product(id=product_id, **product.model_dump())
    products_db[product_id] = updated_product
    return updated_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    del products_db[product_id]
    return {"detail": "Product deleted"}

@app.get("/categories", response_model=List[str])
def get_categories():
    categories = {"All"}
    for p in products_db.values():
        categories.add(p.category)
    return sorted(list(categories))

@app.post("/categories", response_model=str)
def create_category(category: Category):
    return category.name

@app.get("/cart", response_model=List[CartItem])
def get_cart():
    return list(cart_db.values())

@app.post("/cart/add/{product_id}", response_model=CartItem)
def add_to_cart(product_id: int):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product_id in cart_db:
        cart_db[product_id].quantity += 1
    else:
        cart_db[product_id] = CartItem(product_id=product_id, quantity=1)
    return cart_db[product_id]

@app.put("/cart/update/{product_id}")
def update_cart_quantity(product_id: int, quantity: int):
    if product_id not in cart_db:
        raise HTTPException(status_code=404, detail="Item not in cart")
    
    if quantity <= 0:
        del cart_db[product_id]
        return {"detail": "Item removed"}
        
    cart_db[product_id].quantity = quantity
    return cart_db[product_id]

@app.delete("/cart/remove/{product_id}")
def remove_from_cart(product_id: int):
    if product_id not in cart_db:
        raise HTTPException(status_code=404, detail="Item not in cart")
    del cart_db[product_id]
    return {"detail": "Item removed"}

@app.post("/orders", response_model=Order)
def create_order():
    global order_id_counter
    if not cart_db:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    total_price = sum(products_db[item.product_id].price * item.quantity for item in cart_db.values())
    new_order = Order(id=order_id_counter, items=list(cart_db.values()), total_price=total_price)
    
    orders_db[order_id_counter] = new_order
    order_id_counter += 1
    cart_db.clear()
    
    return new_order

@app.get("/orders", response_model=List[Order])
def get_orders():
    return list(orders_db.values())

@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders_db[order_id]