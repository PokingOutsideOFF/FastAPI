from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..import schemas, models
from ..db import get_db
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from ..schemas import TokenData

SECRET_KEY = "0881b31c308a76fb3618a53ba3ab44d0be9549622bc70ae25713ac8170030034"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

router = APIRouter()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def generate_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth credentials", headers={"WWW-Authenticate: Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    seller = db.query(models.Seller).filter(models.Seller.username == request.username).first()
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username not found/ invalid username")
    if not pwd_context.verify(request.password, seller.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password")
    
    access_token = generate_access_token(
        data={"sub":seller.username}
    )
    return {"access_token": access_token, "token_type":"bearer"}

        
    