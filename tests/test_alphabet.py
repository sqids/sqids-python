import pytest
from sqids import Sqids


def test_simple():
    sqids = Sqids(alphabet="0123456789abcdef")

    numbers = [1, 2, 3]
    id = "489158"

    assert sqids.encode(numbers) == id
    assert sqids.decode(id) == numbers


def test_short_alphabet():
    sqids = Sqids(alphabet="abc")

    numbers = [1, 2, 3]
    assert sqids.decode(sqids.encode(numbers)) == numbers


def test_long_alphabet():
    sqids = Sqids(
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+|{}[];:'\"/?.>,<`~"
    )

    numbers = [1, 2, 3]
    assert sqids.decode(sqids.encode(numbers)) == numbers


def test_multibyte_alphabet():
    with pytest.raises(Exception):
        Sqids(alphabet="ë1092")


def test_repeating_alphabet_characters():
    with pytest.raises(Exception):
        Sqids(alphabet="aabcdefg")


def test_too_short_alphabet():
    with pytest.raises(Exception):
        Sqids(alphabet="ab")
