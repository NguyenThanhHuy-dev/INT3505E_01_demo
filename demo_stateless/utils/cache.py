import hashlib
import json

def generate_etag(data):
    if isinstance(data, dict):
        payload = json.dumps(data, sort_keys=True)
    elif isinstance(data, list):
        payload = json.dumps(data, sort_keys=True)
    elif not isinstance(data, str):
        payload = str(data)
    else :
        payload = str(data)
    return hashlib.md5(payload.encode("utf-8")).hexdigest()