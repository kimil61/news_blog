import os
import base64

def generate_secret_key(length=24):
    random_bytes = os.urandom(length)
    return base64.urlsafe_b64encode(random_bytes).decode('utf-8')

