import pytest
import sys
from sqids import Sqids


def test_simple():
    sqids = Sqids()
    numbers = [1, 2, 3]
    id_str = "86Rf07"
    assert sqids.encode(numbers) == id_str
    assert sqids.decode(id_str) == numbers


def test_different_inputs():
    sqids = Sqids()
    numbers = [0, 0, 0, 1, 2, 3, 100, 1_000, 100_000, 1_000_000, sys.maxsize]
    assert sqids.decode(sqids.encode(numbers)) == numbers


@pytest.mark.parametrize(
    "id_str, numbers",
    (
        ("bM", [0]),
        ("Uk", [1]),
        ("gb", [2]),
        ("Ef", [3]),
        ("Vq", [4]),
        ("uw", [5]),
        ("OI", [6]),
        ("AX", [7]),
        ("p6", [8]),
        ("nJ", [9]),
    )
)
def test_incremental_numbers(id_str, numbers):
    sqids = Sqids()
    assert sqids.encode(numbers) == id_str
    assert sqids.decode(id_str) == numbers


@pytest.mark.parametrize(
    "id_str, numbers",
    (
        ("SvIz", [0, 0]),
        ("n3qa", [0, 1]),
        ("tryF", [0, 2]),
        ("eg6q", [0, 3]),
        ("rSCF", [0, 4]),
        ("sR8x", [0, 5]),
        ("uY2M", [0, 6]),
        ("74dI", [0, 7]),
        ("30WX", [0, 8]),
        ("moxr", [0, 9]),
    )
)
def test_incremental_numbers_same_index_0(id_str, numbers):
    sqids = Sqids()
    assert sqids.encode(numbers) == id_str
    assert sqids.decode(id_str) == numbers


@pytest.mark.parametrize(
    "id_str, numbers",
    (
        ("SvIz", [0, 0]),
        ("nWqP", [1, 0]),
        ("tSyw", [2, 0]),
        ("eX68", [3, 0]),
        ("rxCY", [4, 0]),
        ("sV8a", [5, 0]),
        ("uf2K", [6, 0]),
        ("7Cdk", [7, 0]),
        ("3aWP", [8, 0]),
        ("m2xn", [9, 0]),
    )
)
def test_incremental_numbers_same_index_1(id_str, numbers):
    sqids = Sqids()
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


def test_decoding_invalid_character():
    sqids = Sqids()
    assert sqids.decode("*") == []


def test_encode_out_of_range_numbers():
    sqids = Sqids()
    with pytest.raises(ValueError):
        sqids.encode([-1])
    with pytest.raises(ValueError):
        sqids.encode([sys.maxsize + 1])
