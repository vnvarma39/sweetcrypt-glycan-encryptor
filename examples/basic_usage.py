from sweetcrypt import GlycanCrypt

# Basic usage
crypto = GlycanCrypt("my-secret")
encrypted = crypto.encrypt("418 Hackathon")
print(f"Glycan symbols: {encrypted['symbols'][:2]}...")
