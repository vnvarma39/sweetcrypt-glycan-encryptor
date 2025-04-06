from sweetcrypt.core import GlycanCrypt

def test_encryption_decryption():
    crypto = GlycanCrypt("test-passphrase")
    encrypted = crypto.encrypt("Hello AEON 2025")
    assert "🍬" in encrypted["symbols"][0]
    assert crypto.decrypt(encrypted) == "Hello AEON 2025"
