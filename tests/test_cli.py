import pytest
from unittest.mock import patch, mock_open
from sweetcrypt.cli import main
import json

# Test data
TEST_PASSPHRASE = "hackathon418"
TEST_PLAINTEXT = "AEON 2025 Secret Message"
TEST_ENCRYPTED = {
    "iv": "base64iv==",
    "salt": "base64salt==",
    "symbols": ["ABC123🍬", "XYZ789🍬"],
    "ciphertext": "base64ciphertext==",
    "tag": "base64tag=="
}

def test_cli_encryption(capsys):
    """Test encryption via CLI"""
    with patch('builtins.input', return_value=TEST_PASSPHRASE), \
         patch('sweetcrypt.core.GlycanCrypt.encrypt', return_value=TEST_ENCRYPTED):
        
        # Simulate: sweetcrypt --encrypt "AEON 2025 Secret Message"
        with patch('argparse.ArgumentParser.parse_args', 
                  return_value=argparse.Namespace(
                      encrypt=TEST_PLAINTEXT,
                      decrypt=None
                  )):
            main()
            
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        
        assert output["symbols"] == TEST_ENCRYPTED["symbols"]
        assert len(output["ciphertext"]) > 0

def test_cli_decryption(capsys):
    """Test decryption via CLI"""
    with patch('builtins.input', return_value=TEST_PASSPHRASE), \
         patch('sweetcrypt.core.GlycanCrypt.decrypt', return_value=TEST_PLAINTEXT):
        
        # Simulate: sweetcrypt --decrypt encrypted_file.scrypt
        with patch('argparse.ArgumentParser.parse_args',
                  return_value=argparse.Namespace(
                      encrypt=None,
                      decrypt="encrypted_file.scrypt"
                  )), \
             patch("builtins.open", mock_open(read_data=json.dumps(TEST_ENCRYPTED))):
            
            main()
            
        captured = capsys.readouterr()
        assert TEST_PLAINTEXT in captured.out

def test_cli_no_args(capsys):
    """Test CLI with no arguments shows help"""
    with patch('argparse.ArgumentParser.parse_args',
              return_value=argparse.Namespace(
                  encrypt=None,
                  decrypt=None
              )):
        main()
        
    captured = capsys.readouterr()
    assert "usage:" in captured.out.lower()

def test_cli_invalid_file(capsys):
    """Test handling of invalid input files"""
    with patch('argparse.ArgumentParser.parse_args',
              return_value=argparse.Namespace(
                  encrypt=None,
                  decrypt="nonexistent.scrypt"
              )), \
         patch("builtins.open", side_effect=FileNotFoundError):
            
        main()
        
    captured = capsys.readouterr()
    assert "error" in captured.out.lower()
