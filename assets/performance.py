import sqids
import timeit

number = 100_000

print(f"Iterations: {number:,d}")

print(
    "{0:<20s} {1:7.3f}".format(
        "Instantiate:",
        timeit.timeit(
            stmt="sqids.Sqids()",
            globals={"sqids": sqids},
            number=number,
        )
    )
)

print(
    "{0:<20s} {1:7.3f}".format(
        "Encode [0]:",  # [0] -> 'bM'
        timeit.timeit(
            stmt="squid.encode([0])",
            globals={"squid": sqids.Sqids()},
            number=number,
        )
    )
)

print(
    "{0:<20s} {1:7.3f}".format(
        "Encode [0, 1, 2]:",  # [0, 1, 2] -> 'rSCtlB'
        timeit.timeit(
            stmt="squid.encode([0, 1, 2])",
            globals={"squid": sqids.Sqids()},
            number=number,
        )
    )
)

print(
    "{0:<20s} {1:7.3f}".format(
        "Decode 'bM':",  # 'bM' -> [0]
        timeit.timeit(
            stmt="squid.decode('bM')",
            globals={"squid": sqids.Sqids()},
            number=number,
        )
    )
)

print(
    "{0:<20s} {1:7.3f}".format(
        "Decode 'rSCtlB':",  # 'rSCtlB' -> [0, 1, 2]
        timeit.timeit(
            stmt="squid.decode('rSCtlB')",
            globals={"squid": sqids.Sqids()},
            number=number,
        )
    ),
)
