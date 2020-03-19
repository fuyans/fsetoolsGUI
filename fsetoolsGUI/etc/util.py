import binascii
import hashlib
import json

import requests


def hash_simple(key: bytes, string: bytes, algorithm: str = 'sha512', length: int = 20):
    cipher = int(binascii.hexlify(hashlib.pbkdf2_hmac(algorithm, string, key, 100000)), 16) % (10 ** length)
    return cipher


def post_to_knack_user_usage_stats(
        user: str,
        version: str,
        date: str,
        action: str,
        target: str = "hsrmo5)(Ygi-ik]^e'[fm.mcn*jZ_\\s.q`ai_X)&vhcto*pb]n_1-oa^ik\\j"
):
    headers = {
        "X-Knack-Application-Id": "5e739d0676d1dc0017fdd1d5",
        "X-Knack-REST-API-Key": "knack",
        "Content-Type": "application/json",
    }
    payload = {
        'field_2': user,
        'field_3': version,
        'field_4': date,
        'field_5': action,
    }

    rp = requests.post(
        ''.join([chr(ord(v) + i % 10) for i, v in enumerate(target)]),
        data=json.dumps(payload),
        headers=headers
    )

    return rp
