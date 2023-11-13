# CHANGELOG

**v0.4.1**
- Compatibility with Python 3.6 (not officially supported)

**v0.4.0**
- Use double underscore convention to specify private methods
- Separate single module into a package for better readability
- Add [PEP 561](https://peps.python.org/pep-0561/) compatible type hints

**v0.3.0:** **⚠️ BREAKING CHANGE**
- **Breaking change**: IDs change. Algorithm has been fine-tuned for better performance [[Issue #11](https://github.com/sqids/sqids-spec/issues/11)]
- `alphabet` cannot contain multibyte characters
- `min_length` upper limit has increased from alphabet length to `255`
- Max blocklist re-encoding attempts has been capped at the length of the alphabet - 1
- Minimum alphabet length has changed from 5 to 3
- `min_value()` and `max_value()` functions have been removed
- Max integer encoding value is `sys.maxsize`

**v0.2.1:**
- Bug fix: spec update (PR #7): blocklist filtering in uppercase-only alphabet [[PR #7](https://github.com/sqids/sqids-spec/pull/7)]
- Lower uniques test from 1_000_000 to 10_000

**v0.2.0:**
- Bug fix: test for decoding an invalid ID with a [repeating reserved character](https://github.com/sqids/sqids-spec/commit/f52b57836b0463097018f984f853b284e50a5ce4)
- Build cleanup

**v0.1.0:**
- First implementation of [the spec](https://github.com/sqids/sqids-spec)
