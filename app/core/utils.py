import time
import random
import bcrypt

def get_timestamp() -> int:
    return int(time.time() * 1000)

def generate_code() -> int:
    return random.randint(10000, 99999)

def hash_password(password: str):
    hashed = bcrypt.hashpw(
        password.encode("utf-8"), 
        bcrypt.gensalt(),
    ).decode()
    return hashed

def check_password(
    password1: str, 
    password2: str,
) -> bool:
    try:
        hashed = bcrypt.checkpw(
            password1.encode("utf-8"), 
            password2.encode("utf-8")
        )
        return hashed
    except:
        return False
