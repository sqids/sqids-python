import pathlib
import sys
from typing import Set, Tuple


repo_root = pathlib.Path(__file__).parent.parent
this_file = pathlib.Path(__file__).relative_to(repo_root)
constants_path = repo_root / "sqids/constants.py"
import sqids.constants  # noqa


DIGITS = set("0123456789")


def filter_blocklist() -> Tuple[Set[str], Set[str], Set[str]]:
    """Pre-filter the blocklist and update the constants file."""

    exact_match = set()
    match_at_ends = set()
    match_anywhere = set()

    for word in sqids.constants.DEFAULT_BLOCKLIST:
        if len(word) == 3:
            exact_match.add(word)
        elif set(word) & DIGITS:
            match_at_ends.add(word)
        else:
            match_anywhere.add(word)

    return exact_match, match_at_ends, match_anywhere


def generate_new_constants_file(
    exact_match: Set[str],
    match_at_ends: Set[str],
    match_anywhere: Set[str],
) -> str:
    """Generate the text of a new constants file."""

    lines = [
        f'DEFAULT_ALPHABET = "{sqids.constants.DEFAULT_ALPHABET}"',
        f"DEFAULT_MIN_LENGTH = {sqids.constants.DEFAULT_MIN_LENGTH}",
        "",
        "# =======",
        "#  NOTE",
        "# =======",
        "#",
        f"# When updating the blocklist, run {this_file} to pre-filter constants.",
        "# This is critical for performance.",
        "#",
        "",
        "DEFAULT_BLOCKLIST = [",
    ]
    # Output a sorted blocklist.
    for word in sorted(sqids.constants.DEFAULT_BLOCKLIST):
        lines.append(f'    "{word}",')
    lines.append("]")

    # Output exact-match blocklist words.
    lines.append("")
    lines.append("_exact_match = {")
    for word in sorted(exact_match):
        lines.append(f'    "{word}",')
    lines.append("}")

    # Output match-at-ends blocklist words.
    lines.append("")
    lines.append("_match_at_ends = (")
    for word in sorted(match_at_ends):
        lines.append(f'    "{word}",')
    lines.append(")")

    # Output match-anywhere blocklist words.
    lines.append("")
    lines.append("_match_anywhere = {")
    for word in sorted(match_anywhere):
        lines.append(f'    "{word}",')
    lines.append("}")

    return "\n".join(lines).rstrip() + "\n"  # Include a trailing newline.


def main() -> int:
    text = constants_path.read_text()

    exact_match, match_at_ends, match_anywhere = filter_blocklist()
    new_text = generate_new_constants_file(exact_match, match_at_ends, match_anywhere)

    if text == new_text:
        print("No changes necessary")
        return 0

    print(f"Updating {constants_path.relative_to(repo_root)}")
    constants_path.write_text(new_text, newline="\n", encoding="utf-8")
    return 1


if __name__ == "__main__":
    sys.exit(main())
