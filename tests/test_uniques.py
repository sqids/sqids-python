from sqids import Sqids, DEFAULT_ALPHABET

upper = 10_000


def test_uniques_with_padding():
    sqids = Sqids(min_length=len(DEFAULT_ALPHABET))
    unique_set = set()

    for i in range(upper):
        numbers = [i]
        id_ = sqids.encode(numbers)
        unique_set.add(id_)
        assert sqids.decode(id_) == numbers

    assert len(unique_set) == upper


def test_uniques_low_ranges():
    sqids = Sqids()
    unique_set = set()

    for i in range(upper):
        numbers = [i]
        id_ = sqids.encode(numbers)
        unique_set.add(id_)
        assert sqids.decode(id_) == numbers

    assert len(unique_set) == upper


def test_uniques_high_ranges():
    sqids = Sqids()
    unique_set = set()

    for i in range(100_000_000, 100_000_000 + upper):
        numbers = [i]
        id_ = sqids.encode(numbers)
        unique_set.add(id_)
        assert sqids.decode(id_) == numbers

    assert len(unique_set) == upper


def test_uniques_multi():
    sqids = Sqids()
    unique_set = set()

    for i in range(upper):
        numbers = [i, i, i, i, i]
        id_ = sqids.encode(numbers)
        unique_set.add(id_)
        assert sqids.decode(id_) == numbers

    assert len(unique_set) == upper
