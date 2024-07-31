import sys

import sqids

from hypothesis import given, target, assume
import hypothesis.strategies as st


lists_of_integers = st.lists(elements=st.integers(min_value=0, max_value=sys.maxsize))
min_lengths = st.integers(min_value=0, max_value=255)
alphabets = st.text(
    alphabet=st.characters(min_codepoint=0, max_codepoint=0x7f),
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

    sqid = sqids.Sqids(min_length=min_length, alphabet=alphabet, blocklist=[])
    assert sqid.decode(sqid.encode(numbers)) == numbers
