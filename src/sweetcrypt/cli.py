import argparse
from .core import GlycanCrypt

def main():
    parser = argparse.ArgumentParser(description="SweetCrypt CLI")
    parser.add_argument("--encrypt", help="Text to encrypt")
    parser.add_argument("--decrypt", help="File to decrypt")
    args = parser.parse_args()
    
    if args.encrypt:
        crypto = GlycanCrypt(input("Passphrase: "))
        print(crypto.encrypt(args.encrypt))
    
    elif args.decrypt:
        crypto = GlycanCrypt(input("Passphrase: "))
        print(crypto.decrypt(args.decrypt))
