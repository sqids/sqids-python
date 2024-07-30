import pytest
import sys
from sqids import Sqids
from sqids.constants import DEFAULT_ALPHABET


def test_simple():
    sqids = Sqids(min_length=len(DEFAULT_ALPHABET))

    numbers = [1, 2, 3]
    id_str = "86Rf07xd4zBmiJXQG6otHEbew02c3PWsUOLZxADhCpKj7aVFv9I8RquYrNlSTM"

    assert sqids.encode(numbers) == id_str
    assert sqids.decode(id_str) == numbers


@pytest.mark.parametrize(
    "min_length, expected_id",
    (
        (6, "86Rf07"),
        (7, "86Rf07x"),
        (8, "86Rf07xd"),
        (9, "86Rf07xd4"),
        (10, "86Rf07xd4z"),
        (11, "86Rf07xd4zB"),
        (12, "86Rf07xd4zBm"),
        (13, "86Rf07xd4zBmi"),
        (
            len(DEFAULT_ALPHABET) + 0,
            "86Rf07xd4zBmiJXQG6otHEbew02c3PWsUOLZxADhCpKj7aVFv9I8RquYrNlSTM",
        ),
        (
            len(DEFAULT_ALPHABET) + 1,
            "86Rf07xd4zBmiJXQG6otHEbew02c3PWsUOLZxADhCpKj7aVFv9I8RquYrNlSTMy",
        ),
        (
            len(DEFAULT_ALPHABET) + 2,
            "86Rf07xd4zBmiJXQG6otHEbew02c3PWsUOLZxADhCpKj7aVFv9I8RquYrNlSTMyf",
        ),
        (
            len(DEFAULT_ALPHABET) + 3,
            "86Rf07xd4zBmiJXQG6otHEbew02c3PWsUOLZxADhCpKj7aVFv9I8RquYrNlSTMyf1",
        ),
    )
)
def test_incremental(min_length, expected_id):
    numbers = [1, 2, 3]
    sqids = Sqids(min_length=min_length)

    assert sqids.encode(numbers) == expected_id
    assert len(sqids.encode(numbers)) == min_length
    assert sqids.decode(expected_id) == numbers


@pytest.mark.parametrize(
    "id_str, numbers",
    (
        ("SvIzsqYMyQwI3GWgJAe17URxX8V924Co0DaTZLtFjHriEn5bPhcSkfmvOslpBu", [0, 0]),
        ("n3qafPOLKdfHpuNw3M61r95svbeJGk7aAEgYn4WlSjXURmF8IDqZBy0CT2VxQc", [0, 1]),
        ("tryFJbWcFMiYPg8sASm51uIV93GXTnvRzyfLleh06CpodJD42B7OraKtkQNxUZ", [0, 2]),
        ("eg6ql0A3XmvPoCzMlB6DraNGcWSIy5VR8iYup2Qk4tjZFKe1hbwfgHdUTsnLqE", [0, 3]),
        ("rSCFlp0rB2inEljaRdxKt7FkIbODSf8wYgTsZM1HL9JzN35cyoqueUvVWCm4hX", [0, 4]),
        ("sR8xjC8WQkOwo74PnglH1YFdTI0eaf56RGVSitzbjuZ3shNUXBrqLxEJyAmKv2", [0, 5]),
        ("uY2MYFqCLpgx5XQcjdtZK286AwWV7IBGEfuS9yTmbJvkzoUPeYRHr4iDs3naN0", [0, 6]),
        ("74dID7X28VLQhBlnGmjZrec5wTA1fqpWtK4YkaoEIM9SRNiC3gUJH0OFvsPDdy", [0, 7]),
        ("30WXpesPhgKiEI5RHTY7xbB1GnytJvXOl2p0AcUjdF6waZDo9Qk8VLzMuWrqCS", [0, 8]),
        ("moxr3HqLAK0GsTND6jowfZz3SUx7cQ8aC54Pl1RbIvFXmEJuBMYVeW9yrdOtin", [0, 9]),
    )
)
def test_incremental_numbers(id_str, numbers):
    sqids = Sqids(min_length=len(DEFAULT_ALPHABET))

    assert sqids.encode(numbers) == id_str
    assert sqids.decode(id_str) == numbers


@pytest.mark.parametrize("min_length", (0, 1, 5, 10, len(DEFAULT_ALPHABET)))
@pytest.mark.parametrize(
    "numbers",
    (
        [0],
        [0, 0, 0, 0, 0],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [100, 200, 300],
        [1000, 2000, 3000],
        [1000000],
        [sys.maxsize],
    ),
)
def test_min_lengths(min_length, numbers):
    sqids = Sqids(min_length=min_length)

    id_str = sqids.encode(numbers)
    assert len(id_str) >= min_length
    assert sqids.decode(id_str) == numbers


def test_out_of_range_invalid_min_length():
    with pytest.raises(ValueError):
        Sqids(min_length=-1)

    with pytest.raises(ValueError):
        Sqids(min_length=256)


@pytest.mark.parametrize("min_length", ("bogus", {}, True))
def test_min_length_type(min_length):
    """Verify that non-integer min_length values are rejected.

    `True` is a unique case; Python bools are subclasses of int.
    """

    with pytest.raises(TypeError, match="must be an int"):
        Sqids(min_length=min_length)
