import json
import sys

DEFAULT_ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
DEFAULT_MIN_LENGTH = 0

with open("blocklist.json", "r") as json_file:
    DEFAULT_BLOCKLIST = json.load(json_file)


class Sqids:
    def __init__(self, alphabet=None, min_length=None, blocklist=None):
        if alphabet is None:
            alphabet = DEFAULT_ALPHABET
        if min_length is None:
            min_length = DEFAULT_MIN_LENGTH
        if blocklist is None:
            blocklist = DEFAULT_BLOCKLIST

        if len(alphabet) < 5:
            raise ValueError("Alphabet length must be at least 5")

        if len(set(alphabet)) != len(alphabet):
            raise ValueError("Alphabet must contain unique characters")

        if (
            not isinstance(min_length, int)
            or min_length < self.min_value()
            or min_length > len(alphabet)
        ):
            min = self.min_value()
            max = len(alphabet)
            raise ValueError(
                f"Minimum length has to be between {min} and {max}"
            )

        filtered_blocklist = set()
        alphabet_chars = list(alphabet)
        for word in blocklist:
            if len(word) >= 3:
                word_chars = list(word)
                intersection = [c for c in word_chars if c in alphabet_chars]
                if len(intersection) == len(word_chars):
                    filtered_blocklist.add(word.lower())

        self.alphabet = self.shuffle(alphabet)
        self.min_length = min_length
        self.blocklist = filtered_blocklist

    def encode(self, numbers):
        if not numbers:
            return ""

        in_range_numbers = [
            n for n in numbers if self.min_value() <= n <= self.max_value()
        ]
        if len(in_range_numbers) != len(numbers):
            min = self.min_value()
            max = self.max_value()
            raise ValueError(
                f"Encoding supports numbers between {min} and {max}"
            )

        return self.encode_numbers(numbers, False)

    def encode_numbers(self, numbers, partitioned=False):
        offset = sum(
            (
                ord(self.alphabet[v % len(self.alphabet)]) + i
                for i, v in enumerate(numbers)
            ),
            start=len(numbers),
        ) % len(self.alphabet)
        alphabet = self.alphabet[offset:] + self.alphabet[:offset]
        prefix = alphabet[0]
        partition = alphabet[1]
        alphabet = alphabet[2:]

        ret = [prefix]

        for i, num in enumerate(numbers):
            alphabet_without_separator = alphabet[:-1]
            ret.append(self.to_id(num, alphabet_without_separator))

            if i < len(numbers) - 1:
                separator = alphabet[-1]
                if partitioned and i == 0:
                    ret.append(partition)
                else:
                    ret.append(separator)

                alphabet = self.shuffle(alphabet)

        id_str = "".join(ret)

        if self.min_length > len(id_str):
            if not partitioned:
                numbers = [0] + numbers
                id_str = self.encode_numbers(numbers, True)

            if self.min_length > len(id_str):
                id_str = (
                    id_str[:1] + alphabet[: self.min_length - len(id_str)] + id_str[1:]
                )

        if self.is_blocked_id(id_str):
            if partitioned:
                if numbers[0] + 1 > self.max_value():
                    raise ValueError("Ran out of range checking against the blocklist")
                else:
                    numbers[0] += 1
            else:
                numbers = [0] + numbers
            id_str = self.encode_numbers(numbers, True)

        return id_str

    def decode(self, id_str):
        ret = []

        if not id_str:
            return ret

        alphabet_chars = list(self.alphabet)
        if any(c not in alphabet_chars for c in id_str):
            return ret

        prefix = id_str[0]
        offset = self.alphabet.index(prefix)
        alphabet = self.alphabet[offset:] + self.alphabet[:offset]
        partition = alphabet[1]
        alphabet = alphabet[2:]
        id_str = id_str[1:]

        partition_index = id_str.find(partition)
        if 0 < partition_index < len(id_str) - 1:
            id_str = id_str[partition_index + 1 :]
            alphabet = self.shuffle(alphabet)

        while id_str:
            separator = alphabet[-1]
            chunks = id_str.split(separator)
            if chunks:
                alphabet_without_separator = alphabet[:-1]
                ret.append(self.to_number(chunks[0], alphabet_without_separator))

                if len(chunks) > 1:
                    alphabet = self.shuffle(alphabet)

            id_str = separator.join(chunks[1:])

        return ret

    @staticmethod
    def min_value():
        return 0

    @staticmethod
    def max_value():
        return sys.maxsize

    def shuffle(self, alphabet):
        chars = list(alphabet)

        i = 0
        j = len(chars) - 1
        while j > 0:
            r = (i * j + ord(chars[i]) + ord(chars[j])) % len(chars)
            chars[i], chars[r] = chars[r], chars[i]
            i += 1
            j -= 1

        return "".join(chars)

    def to_id(self, num, alphabet):
        id_str = []
        chars = list(alphabet)
        result = num

        while True:
            id_str.insert(0, chars[result % len(chars)])
            result = result // len(chars)
            if result == 0:
                break

        return "".join(id_str)

    def to_number(self, id_str, alphabet):
        chars = list(alphabet)
        return sum(
            chars.index(c) * (len(chars) ** i) for i, c in enumerate(id_str[::-1])
        )

    def is_blocked_id(self, id_str):
        id_str = id_str.lower()

        for word in self.blocklist:
            if len(word) <= len(id_str):
                if len(id_str) <= 3 or len(word) <= 3:
                    if id_str == word:
                        return True
                elif any(c.isdigit() for c in word):
                    if id_str.startswith(word) or id_str.endswith(word):
                        return True
                elif word in id_str:
                    return True

        return False
