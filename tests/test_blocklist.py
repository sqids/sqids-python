import pathlib
import sys

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


@pytest.mark.parametrize("word", ("ab!", "abc!", "xyz"))
def test_alphabet_is_not_superset_of_blocklist_word_characters(word):
    """Verify that a non-subset blocklist word is ignored."""

    sqids = Sqids(alphabet="abc", blocklist=[word])
    assert sqids._Sqids__blocklist_exact_match == set()
    assert sqids._Sqids__blocklist_match_at_ends == tuple()
    assert sqids._Sqids__blocklist_match_anywhere == set()


def test_max_encoding_attempts():
    alphabet = "abc"
    min_length = 3
    blocklist = {"cab", "abc", "bca"}

    sqids = Sqids(alphabet, min_length, blocklist)

    assert min_length == len(alphabet)
    assert min_length == len(blocklist)

    with pytest.raises(Exception):
        sqids.encode([0])


def test_small_words_are_ignored():
    """Blocklist words shorter than 3 characters must be ignored."""

    id_ = Sqids().encode([0])
    assert id_ == "bM"
    id_ = Sqids(blocklist=[id_]).encode([0])
    assert id_ == "bM"


def test_constants_file_is_pristine():
    """Verify the constants file is pristine."""

    repo_root = pathlib.Path(__file__).parent.parent
    sys.path.append(str(repo_root / "assets"))
    import filter_blocklist

    sets = filter_blocklist.filter_blocklist()
    new_text = filter_blocklist.generate_new_constants_file(*sets)
    error_message = "You must run assets/filter_blocklist.py!"
    assert filter_blocklist.constants_path.read_text() == new_text, error_message
