# tests/test_privacy_utils.py

import pytest
import hashlib
import src
from src.privacy_utils import PrivacyUtils

def test_hashstring_output():
    """
    Tests if the _hashstring method produces the correct SHA-256 hash.
    """
    privacy_handler = PrivacyUtils()
    test_string = "test_input_string_123"
    expected_hash = hashlib.sha256(test_string.encode()).hexdigest()

    # Call the method (it's an instance method now)
    actual_hash = privacy_handler.hashstring(test_string)

    # Assert that the actual output matches the expected output
    assert actual_hash == expected_hash

def test_hashstring_empty():
    """
    Tests the _hashstring method with an empty string.
    """
    privacy_handler = PrivacyUtils()
    test_string = ""
    expected_hash = hashlib.sha256(test_string.encode()).hexdigest()
    actual_hash = privacy_handler.hashstring(test_string)
    assert actual_hash == expected_hash


def test_truncator():
    privacy_handler = PrivacyUtils()
    original = "short"
    long_hash = "a"*64 # A long dummy hash
    expected_truncated = "a"*len(original) # Should be "aaaaa"
    actual_truncated = privacy_handler.truncator(original, long_hash)
    assert actual_truncated == expected_truncated
    assert len(actual_truncated) == len(original)