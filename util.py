import os 
import secrets

keys:list[str] = []

def generate_keys() -> list[str]:
    for i in range(10):
        keys.append(os.urandom(15).hex())
    return keys

def random_key() -> str:
    return secrets.choice(keys)

def is_key(key:str, keys:list[str]) -> bool:
    if key in keys:
        return True
    return False