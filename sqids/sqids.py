from typing import List, Set
import sys
from .constants import DEFAULT_ALPHABET, DEFAULT_BLOCKLIST, DEFAULT_MIN_LENGTH


class Sqids:
    def __init__(
        self,
        alphabet: str = DEFAULT_ALPHABET,
        min_length: int = DEFAULT_MIN_LENGTH,
        blocklist: List[str] = DEFAULT_BLOCKLIST,
    ):
        for char in alphabet:
            if ord(char) > 127:
                raise ValueError("Alphabet cannot contain multibyte characters")

        if len(alphabet) < 3:
            raise ValueError("Alphabet length must be at least 3")

        if len(set(alphabet)) != len(alphabet):
            raise ValueError("Alphabet must contain unique characters")

        if not isinstance(min_length, int):
            raise TypeError("Minimum length must be an int")

        MIN_LENGTH_LIMIT = 255
        if min_length < 0 or min_length > MIN_LENGTH_LIMIT:
            raise ValueError(
                f"Minimum length has to be between 0 and {MIN_LENGTH_LIMIT}"
            )

        filtered_blocklist: Set[str] = set()
        alphabet_lower = alphabet.lower()
        for word_lower in (w.lower() for w in blocklist if len(w) >= 3):
            intersection = [c for c in word_lower if c in alphabet_lower]
            if len(intersection) == len(word_lower):
                filtered_blocklist.add(word_lower)

        self.__alphabet = self.__shuffle(alphabet)
        self.__min_length = min_length
        self.__blocklist = filtered_blocklist

    def encode(self, numbers: List[int]) -> str:
        if not numbers:
            return ""

        in_range_numbers = [n for n in numbers if 0 <= n <= sys.maxsize]
        if len(in_range_numbers) != len(numbers):
            raise ValueError(f"Encoding supports numbers between 0 and {sys.maxsize}")

        return self.__encode_numbers(numbers, 0)

    def __encode_numbers(self, numbers: List[int], increment: int = 0) -> str:
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

        if self.__is_blocked_id(id_):
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
            if chunks:
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
        chars = list(alphabet)
        result = num

        while True:
            id_chars.insert(0, chars[result % len(chars)])
            result = result // len(chars)
            if result == 0:
                break

        return "".join(id_chars)

    def __to_number(self, id_: str, alphabet: str) -> int:
        chars = list(alphabet)
        return sum(chars.index(c) * (len(chars) ** i) for i, c in enumerate(id_[::-1]))

    def __is_blocked_id(self, id_: str) -> bool:
        id_ = id_.lower()

        for word in self.__blocklist:
            if len(word) > len(id_):
                continue
            if len(id_) <= 3 or len(word) <= 3:
                if id_ == word:
                    return True
            elif any(c.isdigit() for c in word):
                if id_.startswith(word) or id_.endswith(word):
                    return True
            elif word in id_:
                return True

        return False
