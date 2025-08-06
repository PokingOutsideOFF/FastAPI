from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..import schemas
from ..import models
from ..db import get_db

router = APIRouter(
    tags=['Seller']
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/sellers", response_model=schemas.DisplaySeller)
def create_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(request.password)
    new_seller = models.Seller(username=request.username, email=request.email, password=hashed_password)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller