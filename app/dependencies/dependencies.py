from database import session
from core import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from crud import get_user_by_id


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str = payload.get("sub")
        if user_id is None:
            raise credential_exception
        
    except JWTError:
        raise credential_exception
    
    user = get_user_by_id(db, user_id)

    if user is None:
        raise credential_exception
    
    return user