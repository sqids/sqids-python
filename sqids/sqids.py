from typing import List, Sequence, Set, Tuple
import sys
from .constants import (
    DEFAULT_ALPHABET,
    DEFAULT_BLOCKLIST,
    DEFAULT_MIN_LENGTH,
    _exact_match,
    _match_at_ends,
    _match_anywhere,
)

DIGITS = set("0123456789")


class Sqids:
    def __init__(
        self,
        alphabet: str = DEFAULT_ALPHABET,
        min_length: int = DEFAULT_MIN_LENGTH,
        blocklist: List[str] = DEFAULT_BLOCKLIST,
    ):
        if any(ord(char) > 127 for char in alphabet):
            raise ValueError("Alphabet cannot contain multibyte characters")

        if len(alphabet) < 3:
            raise ValueError("Alphabet length must be at least 3")

        if len(set(alphabet)) != len(alphabet):
            raise ValueError("Alphabet must contain unique characters")

        if not isinstance(min_length, int) or isinstance(min_length, bool):
            raise TypeError("Minimum length must be an int")

        MIN_LENGTH_LIMIT = 255
        if min_length < 0 or min_length > MIN_LENGTH_LIMIT:
            raise ValueError(
                f"Minimum length has to be between 0 and {MIN_LENGTH_LIMIT}"
            )

        # When the blocklist and alphabet are defaults, use pre-filtered blocklists.
        if blocklist is DEFAULT_BLOCKLIST and alphabet is DEFAULT_ALPHABET:
            self.__blocklist_exact_match: Set[str] = _exact_match
            self.__blocklist_match_at_ends: Tuple[str, ...] = _match_at_ends
            self.__blocklist_match_anywhere: Set[str] = _match_anywhere
        else:
            alphabet_lower = set(alphabet.lower())
            exact_match: Set[str] = set()
            match_at_ends: Set[str] = set()
            match_anywhere: Set[str] = set()
            for word in blocklist:
                if len(word) < 3:
                    continue
                word_lower = word.lower()
                word_lower_set = set(word_lower)
                if word_lower_set & alphabet_lower != word_lower_set:
                    continue

                if len(word) == 3:
                    exact_match.add(word.lower())
                elif word_lower_set & DIGITS:
                    match_at_ends.add(word_lower)
                else:
                    match_anywhere.add(word_lower)

            self.__blocklist_exact_match = exact_match
            # When matching at the ends, `.startswith()` and `.endswith()` need a tuple.
            self.__blocklist_match_at_ends = tuple(match_at_ends)
            self.__blocklist_match_anywhere = match_anywhere

        self.__alphabet = self.__shuffle(alphabet)
        self.__min_length = min_length

    def encode(self, numbers: Sequence[int]) -> str:
        if not numbers:
            return ""

        if not all(0 <= number <= sys.maxsize for number in numbers):
            raise ValueError(f"Encoding supports numbers between 0 and {sys.maxsize}")

        return self.__encode_numbers(numbers, 0)

    def __encode_numbers(self, numbers: Sequence[int], increment: int = 0) -> str:
        if increment > len(self.__alphabet):
            raise ValueError("Reached max attempts to re-generate the ID")

        offset = sum(
            (
                ord(self.__alphabet[v % len(self.__alphabet)]) + i
                for i, v in enumerate(numbers)
            )
        )
        offset = (offset + len(numbers)) % len(self.__alphabet)
        offset = (offset + increment) % len(self.__alphabet)
        alphabet = self.__alphabet[offset:] + self.__alphabet[:offset]
        prefix = alphabet[0]
        alphabet = alphabet[::-1]

        ret = [prefix]

        for i, num in enumerate(numbers):
            ret.append(self.__to_id(num, alphabet[1:]))

            if i >= len(numbers) - 1:
                continue

            ret.append(alphabet[0])
            alphabet = self.__shuffle(alphabet)

        id_ = "".join(ret)

        if self.__min_length > len(id_):
            id_ += alphabet[0]

            while self.__min_length - len(id_) > 0:
                alphabet = self.__shuffle(alphabet)
                id_ += alphabet[: min(self.__min_length - len(id_), len(alphabet))]

        if len(id_) >= 3 and self.__is_blocked_id(id_):
            id_ = self.__encode_numbers(numbers, increment + 1)

        return id_

    def decode(self, id_: str) -> List[int]:
        ret: List[int] = []

        if not id_:
            return ret

        alphabet_chars = list(self.__alphabet)
        if any(c not in alphabet_chars for c in id_):
            return ret

        prefix = id_[0]
        offset = self.__alphabet.index(prefix)
        alphabet = self.__alphabet[offset:] + self.__alphabet[:offset]
        alphabet = alphabet[::-1]
        id_ = id_[1:]

        while id_:
            separator = alphabet[0]
            chunks = id_.split(separator)
            if not chunks[0]:
                return ret

            ret.append(self.__to_number(chunks[0], alphabet[1:]))
            if len(chunks) > 1:
                alphabet = self.__shuffle(alphabet)

            id_ = separator.join(chunks[1:])

        return ret

    def __shuffle(self, alphabet: str) -> str:
        chars = list(alphabet)

        i = 0
        j = len(chars) - 1
        while j > 0:
            r = (i * j + ord(chars[i]) + ord(chars[j])) % len(chars)
            chars[i], chars[r] = chars[r], chars[i]
            i += 1
            j -= 1

        return "".join(chars)

    def __to_id(self, num: int, alphabet: str) -> str:
        id_chars: List[str] = []
        result = num
        alphabet_length = len(alphabet)

        while True:
            id_chars.insert(0, alphabet[result % alphabet_length])
            result = result // alphabet_length
            if not result:
                break

        return "".join(id_chars)

    def __to_number(self, id_: str, alphabet: str) -> int:
        chars = list(alphabet)
        return sum(chars.index(c) * (len(chars) ** i) for i, c in enumerate(id_[::-1]))

    def __is_blocked_id(self, id_: str) -> bool:
        id_ = id_.lower()

        if len(id_) == 3:
            return id_ in self.__blocklist_exact_match

        if (
            id_.startswith(self.__blocklist_match_at_ends)
            or id_.endswith(self.__blocklist_match_at_ends)
        ):
            return True

        for word in self.__blocklist_match_anywhere:
            if word in id_:
                return True

        return False
