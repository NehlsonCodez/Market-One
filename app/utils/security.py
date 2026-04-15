from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password:str) -> str :
    
    #Encoding the password to salt before hashing so it will have a length of 64 char
    password = hashlib.sha256(password.encode()).hexdigest()

    return pwd_context.hash(password)

def verify_password(plain_password : str, hashed_password : str) -> bool:

    plain_password = hashlib.sha256(plain_password.encode()).hexdigest()
    return pwd_context.verify(plain_password, hashed_password)

password = hash_password("nelson345")
print(len(password))