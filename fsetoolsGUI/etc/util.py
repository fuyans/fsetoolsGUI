import binascii
import hashlib
import urllib.request
import re
import json


def hash_simple(key: bytes, string: bytes, algorithm: str = 'sha512', length: int = 20):
    cipher = int(binascii.hexlify(hashlib.pbkdf2_hmac(algorithm, string, key, 100000)), 16) % (10 ** length)
    return cipher


def check_online_version(url: str) -> dict:
    contents = urllib.request.urlopen(url).read().decode()
    contents = json.loads(contents)
    return contents
