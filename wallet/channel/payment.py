"""Author: Trinity Core Team 

MIT License

Copyright (c) 2018 Trinity

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
import base58
import binascii
from Crypto import Random
from eth_hash.backends.pysha3 import keccak256

from common.log import LOG
from common.console import console_log
from common.exceptions import GoTo
from common.singleton import SingletonClass
from wallet.utils import get_magic
from trinity import IS_SUPPORTED_ASSET_TYPE, SUPPORTED_ASSET_TYPE


class Payment(metaclass=SingletonClass):
    """

    """
    def __init__(self):
        pass

    @classmethod
    def generate_payment_code(cls, receiver, asset_type, value, hashcode, comments='', cli=False):
        """"""
        if 0 >= int(value):
            console_log.error('Not support negative number.')
            return

        if not IS_SUPPORTED_ASSET_TYPE(asset_type):
            text = 'AssetType: {} is not supported'.format(asset_type)
            LOG.error(text)
            if cli:
                console_log.error(text)

            return None

        asset_type = asset_type.replace('0x', '')
        if asset_type.upper() in SUPPORTED_ASSET_TYPE.keys():
            asset_type = asset_type.upper()

        hashcode = hashcode.strip()

        code = "{uri}&{net_magic}&{hashcode}&{asset_type}&{payment}&{comments}".format(uri=receiver,
                                                                                       net_magic=get_magic(),
                                                                                       hashcode=hashcode,
                                                                                       asset_type=asset_type,
                                                                                       payment=value,
                                                                                       comments=comments)
        base58_code = base58.b58encode(code.encode())
        try:
            return "TN{}".format(base58_code.decode())
        except Exception as error:
            LOG.debug('generate_payment_code error: {}'.format(error))
            return "TN{}".format(base58_code)

    @classmethod
    def hash_r(cls, r):
        return '0x'+keccak256(bytes.fromhex(r)).hex()

    @classmethod
    def decode_payment_code(cls, payment_code):
        if not payment_code.startswith("TN"):
            LOG.error("Payment code MUST start with TN")
            return False, None

        base58_code = payment_code[2:]
        code = base58.b58decode(base58_code).decode()
        info = code.split("&", 5)

        if 6 != len(info):
            return False, None

        keys = ['uri', 'net_magic', 'hashcode', 'asset_type', 'payment', 'comments']

        result = dict(zip(keys, info))

        return True, result

    @classmethod
    def create_hr(cls):
        rcode = binascii.b2a_hex(Random.get_random_bytes(32)).decode()
        hashcode = cls.hash_r(rcode)

        return hashcode, '0x'+rcode

    @classmethod
    def verify_hr(cls, hashcode, rcode):
        try:
            rcode = rcode.replace('0x', '').strip()
            return hashcode.__contains__(cls.hash_r(rcode).__str__())
        except Exception as error:
            raise GoTo('Invalid RCode<{}> for HashR<{}>. Exception: {}'.format(rcode, hashcode, error))

    @classmethod
    def is_valid_hash_r(cls, hashcode):
        return isinstance(hashcode, str) and hashcode.startswith('TN')
