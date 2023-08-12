import pytest
from sqids import Sqids


def test_simple():
    sqids = Sqids()
    numbers = [1, 2, 3]
    id_str = "8QRLaD"
    assert sqids.encode(numbers) == id_str
    assert sqids.decode(id_str) == numbers


def test_different_inputs():
    sqids = Sqids()
    numbers = [0, 0, 0, 1, 2, 3, 100, 1_000, 100_000, 1_000_000, sqids.max_value()]
    assert sqids.decode(sqids.encode(numbers)) == numbers


def test_incremental_numbers():
    sqids = Sqids()
    ids = {
        "bV": [0],
        "U9": [1],
        "g8": [2],
        "Ez": [3],
        "V8": [4],
        "ul": [5],
        "O3": [6],
        "AF": [7],
        "ph": [8],
        "n8": [9],
    }
    for id_str, numbers in ids.items():
        assert sqids.encode(numbers) == id_str
        assert sqids.decode(id_str) == numbers


def test_incremental_numbers_same_index_0():
    sqids = Sqids()
    ids = {
        "SrIu": [0, 0],
        "nZqE": [0, 1],
        "tJyf": [0, 2],
        "e86S": [0, 3],
        "rtC7": [0, 4],
        "sQ8R": [0, 5],
        "uz2n": [0, 6],
        "7Td9": [0, 7],
        "3nWE": [0, 8],
        "mIxM": [0, 9],
    }
    for id_str, numbers in ids.items():
        assert sqids.encode(numbers) == id_str
        assert sqids.decode(id_str) == numbers


def test_incremental_numbers_same_index_1():
    sqids = Sqids()
    ids = {
        "SrIu": [0, 0],
        "nbqh": [1, 0],
        "t4yj": [2, 0],
        "eQ6L": [3, 0],
        "r4Cc": [4, 0],
        "sL82": [5, 0],
        "uo2f": [6, 0],
        "7Zdq": [7, 0],
        "36Wf": [8, 0],
        "m4xT": [9, 0],
    }
    for id_str, numbers in ids.items():
        assert sqids.encode(numbers) == id_str
        assert sqids.decode(id_str) == numbers


def test_multi_input():
    sqids = Sqids()
    numbers = list(range(100))
    output = sqids.decode(sqids.encode(numbers))
    assert numbers == output


def test_encoding_no_numbers():
    sqids = Sqids()
    assert sqids.encode([]) == ""


def test_decoding_empty_string():
    sqids = Sqids()
    assert sqids.decode("") == []


def test_decoding_bad_id_with_repeating_reserved_chars():
    sqids = Sqids()
    assert sqids.decode("fff") == []


def test_decoding_invalid_character():
    sqids = Sqids()
    assert sqids.decode("*") == []


def test_encode_out_of_range_numbers():
    sqids = Sqids()
    with pytest.raises(ValueError):
        sqids.encode([sqids.min_value() - 1])
    with pytest.raises(ValueError):
        sqids.encode([sqids.max_value() + 1])
