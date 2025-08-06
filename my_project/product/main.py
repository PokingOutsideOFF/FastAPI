from fastapi import FastAPI
from .import models
from .db import engine
from .routers import product, seller, login



app = FastAPI(
    title="Products API",
    description="Get details on products",
    terms_of_service="http:/www.google.com",
    contact={
        "Developer Name": "Shreyas",
        "website": "http:/www.google.com",
        "email": "s@gmail.com"
    }, 
)
app.include_router(product.router)
app.include_router(seller.router)
app.include_router(login.router)
models.Base.metadata.create_all(engine)



    
