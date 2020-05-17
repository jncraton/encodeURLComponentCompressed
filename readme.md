

Compression for English-language plain text snippets

Goals
-----

- Outperform URL percent encoding for all characters
- Outperform plain text for short English language text snippets
- Be as fast as possible for both encoding and decoding

Specs
-----

- Avoid binary mode operations, as these may not be natively available in all environments and could be challenging or 

The fragment portion of the URL that we are targeting can use the following characters:
    ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890?/:@-._~!$&'()*+,;=

Word List

Bauman's revised GSL

http://jbauman.com/gsl.html
