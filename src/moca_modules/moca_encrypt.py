# Ω*
#               ■          ■■■■■  
#               ■         ■■   ■■ 
#               ■        ■■     ■ 
#               ■        ■■       
#     ■■■■■     ■        ■■■      
#    ■■   ■■    ■         ■■■     
#   ■■     ■■   ■          ■■■■   
#   ■■     ■■   ■            ■■■■ 
#   ■■■■■■■■■   ■              ■■■
#   ■■          ■               ■■
#   ■■          ■               ■■
#   ■■     ■    ■        ■■     ■■
#    ■■   ■■    ■   ■■■  ■■■   ■■ 
#     ■■■■■     ■   ■■■    ■■■■■


"""
Copyright (c) 2020.5.28 [el.ideal-ideas]
This software is released under the MIT License.
see LICENSE.txt or following URL.
https://www.el-ideal-ideas.com/MocaSystem/LICENSE/
"""

# -- Imports --------------------------------------------------------------------------

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto import Random
from base64 import b64encode, b64decode
from typing import *
from pathlib import Path
from .moca_base_class import MocaClassCache, MocaNamedInstance

# -------------------------------------------------------------------------- Imports --

# -- Private Functions --------------------------------------------------------------------------


def __create_aes(password: str,
                 iv: bytes):
    """
    create aes object
    :param password: password
    :param iv: initialization vector
    :return: aes object
    """
    sha256_hash = SHA256.new()
    sha256_hash.update(password.encode())
    hashed_key = sha256_hash.digest()
    return AES.new(hashed_key, AES.MODE_CFB, iv)


# -------------------------------------------------------------------------- Private Functions --

# -- Public Functions --------------------------------------------------------------------------


def encrypt(data: bytes,
            password: str) -> bytes:
    """
    encrypt data
    :param data: plain data
    :param password: password
    :return: encrypted data
    """
    iv = Random.new().read(AES.block_size)
    return iv + __create_aes(password, iv).encrypt(data)


def decrypt(data: bytes,
            password: str) -> bytes:
    """
    decrypt data
    :param data: encrypted data
    :param password: password
    :return: plain data
    """
    iv, cipher = data[:AES.block_size], data[AES.block_size:]
    return __create_aes(password, iv).decrypt(cipher)


def encrypt_string(text: str,
                   password: str) -> Optional[str]:
    """
    encrypt string data.
    :param text: target string.
    :param password: password.
    :return: encrypted string.
    """
    encrypted_bytes = encrypt(text.encode(), password)
    return b64encode(encrypted_bytes).decode()


def decrypt_string(text: str,
                   password: str) -> Optional[str]:
    """
    decrypt string data.
    :param text: encrypted string.
    :param password: password.
    :return: plain string. if password is incorrect, return None
    """
    try:
        plain_bytes = decrypt(b64decode(text), password)
        return plain_bytes.decode()
    except UnicodeDecodeError:
        return None


# -------------------------------------------------------------------------- Public Functions --

# -- MocaAES --------------------------------------------------------------------------


class MocaAES(MocaClassCache, MocaNamedInstance):
    """
    AES encryption.

    Attributes
    ----------
    self._pass: bytes
        the password.
    """

    def __init__(self, password: Union[str, bytes]):
        MocaClassCache.__init__(self)
        MocaNamedInstance.__init__(self)
        sha256_hash = SHA256.new()
        sha256_hash.update(password if isinstance(password, bytes) else password.encode())
        hashed_key = sha256_hash.digest()
        self._pass: bytes = hashed_key

    def encrypt(self, data: bytes, mode: int = 9) -> bytes:
        """
        MODE_ECB = 1
        MODE_CBC = 2
        MODE_CFB = 3
        MODE_OFB = 5
        MODE_CTR = 6
        MODE_OPENPGP = 7
        MODE_CCM = 8
        MODE_EAX = 9
        MODE_SIV = 10
        MODE_GCM = 11
        MODE_OCB = 12
        """
        cipher = AES.new(self._pass, mode)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        data = cipher.nonce + tag + ciphertext
        return data

    def decrypt(self, data: bytes, mode: int = 9) -> bytes:
        """
        MODE_ECB = 1
        MODE_CBC = 2
        MODE_CFB = 3
        MODE_OFB = 5
        MODE_CTR = 6
        MODE_OPENPGP = 7
        MODE_CCM = 8
        MODE_EAX = 9
        MODE_SIV = 10
        MODE_GCM = 11
        MODE_OCB = 12
        """
        nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
        cipher = AES.new(self._pass, mode, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        return data


# -------------------------------------------------------------------------- MocaAES --

# -- Moca RSA --------------------------------------------------------------------------


class MocaRSA(MocaNamedInstance, MocaClassCache):
    """
    RSA encryption.
    
    Attributes
    ----------
    self._passphrase: Optional[str]
        the passphrase.
    self._private_key: Optional[bytes]
        the private key.
    self._public_key: Optional[bytes]
        the public key.
    self._key: Optional[RsaKey]
        the RsaKey object.
    """

    def __init__(self, passphrase: Optional[str] = None):
        MocaClassCache.__init__(self)
        MocaNamedInstance.__init__(self)
        self._passphrase: Optional[str] = passphrase
        self._private_key: Optional[bytes] = None
        self._public_key: Optional[bytes] = None
        self._key: Optional[RsaKey] = None

    def generate_new_key(self) -> Tuple[bytes, bytes]:
        key = RSA.generate(2048)
        private_key = key.export_key(passphrase=self._passphrase, pkcs=8,
                                     protection="scryptAndAES128-CBC")
        public_key = key.publickey().export_key()
        self._private_key = private_key
        self._public_key = public_key
        self._key = key
        return private_key, public_key

    @classmethod
    def generate_key(cls) -> Tuple[bytes, bytes]:
        key = RSA.generate(2048)
        private_key = key.export_key(pkcs=8, protection="scryptAndAES128-CBC")
        public_key = key.publickey().export_key()
        return private_key, public_key

    def get_key_object(self) -> RsaKey:
        if self._key is None:
            self.generate_new_key()
        return self._key

    def get_public_key(self) -> bytes:
        if self._public_key is None:
            return self.generate_new_key()[1]
        else:
            return self._public_key

    def get_private_key(self) -> bytes:
        if self._private_key is None:
            return self.generate_new_key()[0]
        else:
            return self._private_key

    def get_keys(self) -> Tuple[bytes, bytes]:
        if self._private_key is None:
            return self.generate_new_key()
        else:
            return self._private_key, self._public_key

    def save_private_key(self, filename: Union[Path, str]):
        with open(str(filename), mode='wb') as f:
            f.write(self.get_private_key())

    def save_public_key(self, filename: Union[Path, str]):
        with open(str(filename), mode='wb') as f:
            f.write(self.get_public_key())

    def load_key(self, filename: Union[Path, str]):
        with open(str(filename), mode='rb') as f:
            key = RSA.importKey(f.read(), passphrase=self._passphrase)
            private_key = key.export_key(passphrase=self._passphrase, pkcs=8,
                                         protection="scryptAndAES128-CBC")
            public_key = key.publickey().export_key()
            self._private_key = private_key
            self._public_key = public_key
            self._key = key
            return private_key, public_key

    def encrypt(self, data: bytes) -> bytes:
        # Encrypt the session key with the public RSA key
        session_key = Random.get_random_bytes(16)
        cipher_rsa = PKCS1_OAEP.new(self.get_key_object())
        enc_session_key = cipher_rsa.encrypt(session_key)
        # Encrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(data)
        return enc_session_key + cipher_aes.nonce + tag + ciphertext

    def decrypt(self, data: bytes) -> bytes:
        size = self.get_key_object().size_in_bytes()
        enc_session_key, nonce, tag, ciphertext = \
            data[:size], data[size:size + 16], data[size + 16:size + 32], data[size + 32:]
        # Decrypt the session key with the private RSA key
        cipher_rsa = PKCS1_OAEP.new(self.get_key_object())
        session_key = cipher_rsa.decrypt(enc_session_key)
        # Decrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        return data

    def signature(self, data: bytes) -> bytes:
        hash_data = SHA256.new(data)
        signature = pkcs1_15.new(self.get_key_object()).sign(hash_data)
        return signature

    def verify(self, data: bytes, signature: bytes) -> bool:
        hash_data = SHA256.new(data)
        try:
            pkcs1_15.new(self.get_key_object()).verify(hash_data, signature)
            verified = True
        except ValueError:
            verified = False
        return verified

# -------------------------------------------------------------------------- Moca RSA --
