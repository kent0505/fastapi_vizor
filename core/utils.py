import time

def get_timestamp() -> int:
    return int(time.time() * 1000)

def get_format(value: str) -> str:
    return value.split('.')[-1]

