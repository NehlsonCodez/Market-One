from datetime import datetime, timedelta
import os
from jose import jwt
from dotenv import load_dotenv

#Load my .env data into this environment
load_dotenv()

#get data from my .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


#Create access token for logged in user
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    #update the data dictionary to include expire or add iat time stamp
    to_encode.update({"exp": expire})

    #Generate jwt signed token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt
