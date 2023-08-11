import pytest
from sqids import Sqids, DEFAULT_ALPHABET


def test_simple():
    sqids = Sqids(min_length=len(DEFAULT_ALPHABET))

    numbers = [1, 2, 3]
    id_str = "75JILToVsGerOADWmHlY38xvbaNZKQ9wdFS0B6kcMEtnRpgizhjU42qT1cd0dL"

    assert sqids.encode(numbers) == id_str
    assert sqids.decode(id_str) == numbers


def test_incremental_numbers():
    sqids = Sqids(min_length=len(DEFAULT_ALPHABET))

    ids = {
        "jf26PLNeO5WbJDUV7FmMtlGXps3CoqkHnZ8cYd19yIiTAQuvKSExzhrRghBlwf": [0, 0],
        "vQLUq7zWXC6k9cNOtgJ2ZK8rbxuipBFAS10yTdYeRa3ojHwGnmMV4PDhESI2jL": [0, 1],
        "YhcpVK3COXbifmnZoLuxWgBQwtjsSaDGAdr0ReTHM16yI9vU8JNzlFq5Eu2oPp": [0, 2],
        "OTkn9daFgDZX6LbmfxI83RSKetJu0APihlsrYoz5pvQw7GyWHEUcN2jBqd4kJ9": [0, 3],
        "h2cV5eLNYj1x4ToZpfM90UlgHBOKikQFvnW36AC8zrmuJ7XdRytIGPawqYEbBe": [0, 4],
        "7Mf0HeUNkpsZOTvmcj836P9EWKaACBubInFJtwXR2DSzgYGhQV5i4lLxoT1qdU": [0, 5],
        "APVSD1ZIY4WGBK75xktMfTev8qsCJw6oyH2j3OnLcXRlhziUmpbuNEar05QCsI": [0, 6],
        "P0LUhnlT76rsWSofOeyRGQZv1cC5qu3dtaJYNEXwk8Vpx92bKiHIz4MgmiDOF7": [0, 7],
        "xAhypZMXYIGCL4uW0te6lsFHaPc3SiD1TBgw5O7bvodzjqUn89JQRfk2Nvm4JI": [0, 8],
        "94dRPIZ6irlXWvTbKywFuAhBoECQOVMjDJp53s2xeqaSzHY8nc17tmkLGwfGNl": [0, 9],
    }

    for id_str, numbers in ids.items():
        assert sqids.encode(numbers) == id_str
        assert sqids.decode(id_str) == numbers


def test_min_lengths():
    for min_length in [0, 1, 5, 10, len(DEFAULT_ALPHABET)]:
        for numbers in [
            [Sqids.min_value()],
            [0, 0, 0, 0, 0],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [100, 200, 300],
            [1000, 2000, 3000],
            [1000000],
            [Sqids.max_value()],
        ]:
            sqids = Sqids(min_length=min_length)

            id_str = sqids.encode(numbers)
            assert len(id_str) >= min_length
            assert sqids.decode(id_str) == numbers


def test_out_of_range_invalid_min_length():
    with pytest.raises(ValueError):
        Sqids(min_length=-1)

    with pytest.raises(ValueError):
        Sqids(min_length=len(DEFAULT_ALPHABET) + 1)
