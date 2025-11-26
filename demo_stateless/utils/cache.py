import hashlib
import json

def generate_etag(data):
    if isinstance(data, (dict, list)):
        # Dùng `sort_keys=True` là mấu chốt, bạn đã làm đúng!
        payload = json.dumps(data, sort_keys=True)
    else:
        # Tất cả các kiểu khác (int, bool, str)
        # đều được ép kiểu về string
        payload = str(data)
        
    return hashlib.md5(payload.encode("utf-8")).hexdigest()