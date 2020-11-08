import binascii
import hashlib
import json
import subprocess
from datetime import datetime

import requests


def hash_simple(key: bytes, string: bytes, algorithm: str = 'sha512', length: int = 20) -> int:
    hash_ = hashlib.pbkdf2_hmac(algorithm, string, key, 100000)
    hex_ = binascii.hexlify(hash_)
    cipher = int(hex_, 16) % (10 ** length)
    return cipher


def post_to_knack_user_usage_stats(
        user: str,
        version: str,
        date: str,
        content: str,
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
        'field_5': content,
    }

    rp = requests.post(
        ''.join([chr(ord(v) + i % 10) for i, v in enumerate(target)]),
        data=json.dumps(payload),
        headers={''.join([chr(ord(v) + i % 10) for i, v in enumerate(k)]): ''.join(
            [chr(ord(v) + i % 10) for i, v in enumerate(v)]) for k, v in headers.items()},
        timeout=10
    )

    return rp


def build_write(datetime_cls: datetime = datetime.now()):
    datetime_current = datetime.now()
    datetime_current.strftime('%y')


def build_read(datetime_str: str):
    pass


def _test_post_to_knack_user_usage_stats():
    r = post_to_knack_user_usage_stats(
        user='test',
        version='999',
        date='1991/01/01',
        content='0000'
    )
    print(r.status_code)
    assert r.status_code == 200


def get_machine_uid() -> str:
    uid_bytes: bytes = subprocess.check_output('wmic csproduct get uuid')
    uid_str: str = uid_bytes.decode('utf-8').replace('UUID', '').strip()
    return uid_str


if __name__ == '__main__':
    _test_post_to_knack_user_usage_stats()
