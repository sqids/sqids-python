from sqids import Sqids


def test_default_blocklist():
    sqids = Sqids()

    assert sqids.decode("sexy") == [200044]
    assert sqids.encode([200044]) == "d171vI"


def test_empty_blocklist():
    sqids = Sqids(blocklist=set())

    assert sqids.decode("sexy") == [200044]
    assert sqids.encode([200044]) == "sexy"


def test_custom_blocklist():
    sqids = Sqids(blocklist={"AvTg"})

    assert sqids.decode("sexy") == [200044]
    assert sqids.encode([200044]) == "sexy"

    assert sqids.decode("AvTg") == [100000]
    assert sqids.encode([100000]) == "7T1X8k"
    assert sqids.decode("7T1X8k") == [100000]


def test_blocklist():
    sqids = Sqids(blocklist={"8QRLaD", "7T1cd0dL", "RA8UeIe7", "WM3Limhw", "LfUQh4HN"})

    assert sqids.encode([1, 2, 3]) == "TM0x1Mxz"
    assert sqids.decode("TM0x1Mxz") == [1, 2, 3]


def test_decoding_blocklist_words():
    sqids = Sqids(blocklist={"8QRLaD", "7T1cd0dL", "RA8UeIe7", "WM3Limhw", "LfUQh4HN"})

    assert sqids.decode("8QRLaD") == [1, 2, 3]
    assert sqids.decode("7T1cd0dL") == [1, 2, 3]
    assert sqids.decode("RA8UeIe7") == [1, 2, 3]
    assert sqids.decode("WM3Limhw") == [1, 2, 3]
    assert sqids.decode("LfUQh4HN") == [1, 2, 3]


def test_match_against_short_blocklist_word():
    sqids = Sqids(blocklist={"pPQ"})

    assert sqids.decode(sqids.encode([1000])) == [1000]
