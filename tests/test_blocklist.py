import pytest
from sqids import Sqids


def test_default_blocklist():
    sqids = Sqids()

    assert sqids.decode("aho1e") == [4572721]
    assert sqids.encode([4572721]) == "JExTR"


def test_empty_blocklist():
    sqids = Sqids(blocklist=set())

    assert sqids.decode("aho1e") == [4572721]
    assert sqids.encode([4572721]) == "aho1e"


def test_custom_blocklist():
    sqids = Sqids(blocklist={"ArUO"})

    assert sqids.decode("aho1e") == [4572721]
    assert sqids.encode([4572721]) == "aho1e"

    assert sqids.decode("ArUO") == [100000]
    assert sqids.encode([100000]) == "QyG4"
    assert sqids.decode("QyG4") == [100000]


def test_blocklist():
    sqids = Sqids(
        blocklist={
            "JSwXFaosAN",  # normal result of 1st encoding, block that word on purpose
            "OCjV9JK64o",  # result of 2nd encoding
            "rBHf",  # result of 3rd encoding is `4rBHfOiqd3`, let's block a substring
            "79SM",  # result of 4th encoding is `dyhgw479SM`, let's block the postfix
            "7tE6",  # result of 4th encoding is `7tE6jdAHLe`, let's block the prefix
        }
    )

    assert sqids.encode([1000000, 2000000]) == "1aYeB7bRUt"
    assert sqids.decode("1aYeB7bRUt") == [1000000, 2000000]


def test_decoding_blocklist_words():
    sqids = Sqids(blocklist={"86Rf07", "se8ojk", "ARsz1p", "Q8AI49", "5sQRZO"})

    assert sqids.decode("86Rf07") == [1, 2, 3]
    assert sqids.decode("se8ojk") == [1, 2, 3]
    assert sqids.decode("ARsz1p") == [1, 2, 3]
    assert sqids.decode("Q8AI49") == [1, 2, 3]
    assert sqids.decode("5sQRZO") == [1, 2, 3]


def test_match_against_short_blocklist_word():
    sqids = Sqids(blocklist={"pnd"})

    assert sqids.decode(sqids.encode([1000])) == [1000]


def test_blocklist_filtering_in_constructor():
    # lowercase blocklist in only-uppercase alphabet
    sqids = Sqids(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", blocklist={"sxnzkl"})

    id = sqids.encode([1, 2, 3])
    numbers = sqids.decode(id)

    # without blocklist, would've been "SXNZKL"
    assert id == "IBSHOZ"
    assert numbers == [1, 2, 3]


def test_max_encoding_attempts():
    alphabet = "abc"
    min_length = 3
    blocklist = {"cab", "abc", "bca"}

    sqids = Sqids(alphabet, min_length, blocklist)

    assert min_length == len(alphabet)
    assert min_length == len(blocklist)

    with pytest.raises(Exception):
        sqids.encode([0])
