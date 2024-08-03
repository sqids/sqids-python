import sys

import sqids

from hypothesis import given, target, assume
import hypothesis.strategies as st


lists_of_integers = st.lists(
    elements=st.integers(min_value=0, max_value=sys.maxsize),
    min_size=1,
)
min_lengths = st.integers(min_value=0, max_value=255)
alphabets = st.text(
    alphabet=st.characters(min_codepoint=0, max_codepoint=0x7F),
    min_size=3,
)


@given(numbers=lists_of_integers, min_length=min_lengths, alphabet=alphabets)
def test_round_trip_encoding(numbers, min_length, alphabet):
    # Encourage hypothesis to find ideal alphabets
    # by giving unique alphabets a score of 1.0
    # and non-unique alphabets a lower score.
    target(len(set(alphabet)) / len(alphabet))
    # Reject non-unique alphabets without failing the test.
    assume(len(set(alphabet)) == len(alphabet))

    sqid_1 = sqids.Sqids(min_length=min_length, alphabet=alphabet, blocklist=[])
    id_1 = sqid_1.encode(numbers)
    assert sqid_1.decode(id_1) == numbers

    # If the ID is long enough, use it as a blocklist word and ensure it is blocked.
    if len(id_1) >= 3:  # pragma: nocover
        sqid_2 = sqids.Sqids(min_length=min_length, alphabet=alphabet, blocklist=[id_1])
        id_2 = sqid_2.encode(numbers)
        assert id_1 != id_2
        assert sqid_2.decode(id_2) == numbers
