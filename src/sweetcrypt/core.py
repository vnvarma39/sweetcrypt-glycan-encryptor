import zlib
import base64
import secrets
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class GlycanCrypt:
    """Glycan-inspired encryption with visual symbolization."""
    
    def __init__(self, passphrase):
        self.passphrase = passphrase
        self.key, self.salt = self._derive_key(passphrase)
        self.position_counter = 0

    def _derive_key(self, passphrase):
        """Generate a key using scrypt with random salt."""
        salt = secrets.token_bytes(16)
        key = hashlib.scrypt(
            password=passphrase.encode(),
            salt=salt,
            n=2**14,
            r=8,
            p=1,
            dklen=64
        )
        return key[:32], salt

    def _glycan_encode(self, chunk: bytes, position: int) -> str:
        """Generate a glycan symbol for a data chunk."""
        hmac = hashlib.blake2b(
            key=self.key[16:], 
            digest_size=12
        )
        hmac.update(position.to_bytes(4, 'big'))
        hmac.update(chunk)
        return base64.b32encode(hmac.digest())[:10].decode() + '🍬'

    def encrypt(self, plaintext: str) -> dict:
        """Encrypt data with glycan symbolization."""
        if not isinstance(plaintext, bytes):
            plaintext = zlib.compress(plaintext.encode(), level=9)

        iv = secrets.token_bytes(12)
        cipher = Cipher(
            algorithms.AES(self.key[:32]),
            modes.GCM(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        symbols = []
        for i in range(0, len(ciphertext), 32):
            chunk = ciphertext[i:i+32]
            symbols.append(self._glycan_encode(chunk, self.position_counter))
            self.position_counter += 1

        return {
            'iv': base64.b64encode(iv).decode(),
            'salt': base64.b64encode(self.salt).decode(),
            'symbols': symbols,
            'ciphertext': base64.b64encode(ciphertext).decode(),
            'tag': base64.b64encode(encryptor.tag).decode()
        }

    def decrypt(self, encrypted_data: dict) -> str:
        """Decrypt glycan-encoded data."""
        iv = base64.b64decode(encrypted_data['iv'])
        tag = base64.b64decode(encrypted_data['tag'])
        ciphertext = base64.b64decode(encrypted_data['ciphertext'])

        cipher = Cipher(
            algorithms.AES(self.key[:32]),
            modes.GCM(iv, tag),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        try:
            return zlib.decompress(plaintext).decode()
        except:
            return plaintext.decode()
