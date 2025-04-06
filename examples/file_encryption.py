#!/usr/bin/env python3
"""
File Encryption/Decryption Example
----------------------------------
Demonstrates how to:
1. Encrypt a file to .scrypt format
2. Decrypt back to original
"""

from sweetcrypt import GlycanCrypt
import json
import os

def encrypt_file(input_path: str, output_path: str, passphrase: str):
    """
    Encrypts a file and saves with .scrypt extension
    
    Args:
        input_path: Path to original file
        output_path: Where to save encrypted file
        passphrase: Secret passphrase
    """
    print(f"🔐 Encrypting {input_path}...")
    
    # Read file content
    with open(input_path, 'rb') as f:
        content = f.read()
    
    # Encrypt (handles both text and binary)
    crypto = GlycanCrypt(passphrase)
    encrypted = crypto.encrypt(content)
    
    # Save as JSON
    with open(output_path, 'w') as f:
        json.dump(encrypted, f)
    
    print(f"✅ Saved encrypted file to {output_path}")
    print(f"Generated {len(encrypted['symbols'])} glycan symbols")

def decrypt_file(input_path: str, output_path: str, passphrase: str):
    """
    Decrypts a .scrypt file back to original
    
    Args:
        input_path: Path to encrypted .scrypt file
        output_path: Where to save decrypted file  
        passphrase: Secret passphrase used for encryption
    """
    print(f"🔓 Decrypting {input_path}...")
    
    # Load encrypted data
    with open(input_path, 'r') as f:
        encrypted = json.load(f)
    
    # Decrypt
    crypto = GlycanCrypt(passphrase)
    decrypted = crypto.decrypt(encrypted)
    
    # Write bytes or text
    mode = 'wb' if isinstance(decrypted, bytes) else 'w'
    with open(output_path, mode) as f:
        f.write(decrypted)
    
    print(f"✅ Saved decrypted file to {output_path}")

if __name__ == "__main__":
    # Example usage
    PASSPHRASE = "AEON-418-Hackathon-2025"  # In real usage, get via input()
    ORIGINAL_FILE = "example.txt"
    ENCRYPTED_FILE = "example.scrypt"
    DECRYPTED_FILE = "example_decrypted.txt"
    
    # Create test file if doesn't exist
    if not os.path.exists(ORIGINAL_FILE):
        with open(ORIGINAL_FILE, 'w') as f:
            f.write("Secret data for 418 Hackathon\nLine 2\n")
    
    # Run encryption/decryption
    encrypt_file(ORIGINAL_FILE, ENCRYPTED_FILE, PASSPHRASE)
    decrypt_file(ENCRYPTED_FILE, DECRYPTED_FILE, PASSPHRASE)
    
    # Verify
    with open(ORIGINAL_FILE, 'r') as f1, open(DECRYPTED_FILE, 'r') as f2:
        assert f1.read() == f2.read(), "Decrypted content doesn't match original!"
    
    print("🔒🔓 Encryption/Decryption cycle completed successfully!")
