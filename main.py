from fastapi import FastAPI, Form
from pydantic import BaseModel, Field, HttpUrl
from typing import Set, List
from uuid import UUID
from datetime import date as Date, datetime, time, timedelta


class Event(BaseModel):
    evend_id: UUID 
    start_date: Date 
    start_time: datetime
    end_time: datetime
    repeat_time: time
    execute_after: timedelta

class Profile(BaseModel):
    name: str
    email: str
    age: int
    
class Image(BaseModel):
    url: HttpUrl
    name: str

class Product(BaseModel):
    name: str = Field(example="Phone")
    price: int = Field(title="Price of the item", description="The price must be greater than zero", gt=0)
    discount: int = Field(example=10)
    discounted_price: float
    tags: Set[str] = Field(example = ["electronics", "gadgets"], description="Tags for the product")
    image: List[Image]
    
    # class Config:
    #     json_schema_extra = {
    #         "example": {
    #             "name": "Sample Product",
    #             "price": 100,
    #             "discount": 10,
    #             "discounted_price": 0,
    #             "tags": ["electronics", "gadgets"],
    #             "image": [
    #                 {
    #                     "url": "http://example.com/image1.jpg",
    #                     "name": "Image 1"
    #                 }
    #             ]  
    #         }
    #     }

class Offer(BaseModel):
    name: str
    description: str
    price: float
    products: List[Product]

class User(BaseModel):
    name: str
    email: str
    
app = FastAPI()

@app.post('/login')
def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username, "password": password}

@app.post("/addevent")
def add_event(event: Event):
    return event

@app.post("/addoffer")
def add_offer(offer: Offer):
    return offer

@app.post("/purchase")
def purchase(user:User, product: Product):
    product.discounted_price = product.price - (product.price * product.discount / 100)
    return {
        "user": user,
        "product": product
    }

@app.post("/addproduct/{product_id}")
def add_product(product: Product, product_id: int, category: str):
    product.discounted_price = product.price - (product.price * product.discount / 100)
    return {"product_id": product_id, "product": product, "category": category}

@app.get("/user/admin")
def admin():
    return {"This is admin page"}

@app.post("/adduser")
def add_user(profile: Profile):
    return {
        "message": "User added successfully",
        "profile": profile
    }