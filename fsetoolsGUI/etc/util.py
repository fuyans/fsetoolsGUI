import binascii
import hashlib
import json
from os.path import isfile

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
        "X,Ik]^e&9gpkg`]ochf$Ic": "5d505_*//-d0b`,++0^[d0b2",
        "X,Ik]^e&J<SS+>LD'D]p": "km_`g",
        "Cnlqain&Lppd": "aonie^[mafn.hpki",
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
        headers={''.join([chr(ord(v) + i % 10) for i, v in enumerate(k)]): ''.join(
            [chr(ord(v) + i % 10) for i, v in enumerate(v)]) for k, v in headers.items()},
        timeout=10
    )

    return rp


if __name__ == '__main__':
    pass
