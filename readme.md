encodeURLComponentCompressed
----------------------------

This project provides an alternative to the Javascript encodeURLComponent function. It encoded all bytes in two characters or fewer (URL encoding uses 3 for percent escaped bytes). It also implements a simple prefix coder to more efficiently common Enlish-language text string.

Common English-language strings can be reduced in size by 30-40% compared to plain text, and can be reduced by about 50% compared to the baseline encodeURLComponent function.

Goals
-----

- Outperform URL percent encoding for all characters
- Outperform plain text for short English language text snippets
- Be as fast as possible for both encoding and decoding

Word List
---------

Bauman's revised GSL

http://jbauman.com/gsl.html
