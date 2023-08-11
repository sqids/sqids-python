# [Sqids Python](https://sqids.org/python)

[![Github Actions](https://img.shields.io/github/actions/workflow/status/sqids/sqids-python/tests.yml)](https://github.com/sqids/sqids-python/actions)

Sqids (pronounced "squids") is a small library that lets you generate YouTube-looking IDs from numbers. It"s good for link shortening, fast & URL-safe ID generation and decoding back into numbers for quicker database lookups.

## Getting started

Install the module from PyPI, e. g. with pip:

```bash
pip install sqids
```

Import the constructor from the `sqids` module:

```python
from sqids import Sqids
sqids = Sqids()
```

## Examples

Simple encode & decode:

```python
sqids = Sqids()
id = sqids.encode([1, 2, 3]) # "8QRLaD"
numbers = sqids.decode(id) # [1, 2, 3]
```

Randomize IDs by providing a custom alphabet:

```python
sqids = Sqids(alphabet="FxnXM1kBN6cuhsAvjW3Co7l2RePyY8DwaU04Tzt9fHQrqSVKdpimLGIJOgb5ZE")
id = sqids.encode([1, 2, 3]) # "B5aMa3"
numbers = sqids.decode(id) # [1, 2, 3]
```

Enforce a *minimum* length for IDs:

```python
sqids = Sqids(min_length=10)
id = sqids.encode([1, 2, 3]) # "75JT1cd0dL"
numbers = sqids.decode(id) # [1, 2, 3]
```

Prevent specific words from appearing anywhere in the auto-generated IDs:

```python
sqids = Sqids(blocklist={"word1", "word2"})
id = sqids.encode([1, 2, 3]) # "8QRLaD"
numbers = sqids.decode(id) # [1, 2, 3]
```

## License

[MIT](LICENSE)
