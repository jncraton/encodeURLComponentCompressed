from collections import Counter, OrderedDict
from urllib.parse import quote, unquote
import csv

class PrefixCoder:
    def __init__(self, cutoff=77, chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789?/:@-._~!$&'()*+,;="):
        self.cutoff = cutoff
        self.chars = chars
        
    def get_code(self, num):
        if (num < self.cutoff):
            return self.chars[num]
        else:
            num1 = int(num / len(self.chars))
            byte1 = self.chars[self.cutoff + num1]
            num2 = (num - self.cutoff) % len(self.chars)
            byte2 = self.chars[num2] 
            return byte1 + byte2

    def get_max(self):
        return self.cutoff + (len(self.chars) - self.cutoff - 1) * len(self.chars)

encmap = {}
decmap = {}
with open('gsl.txt') as f:
    ngrams = Counter()
    pc = PrefixCoder()

    for (i,row) in enumerate(csv.reader(f, delimiter=' ')):
        count = int(row[1])
        word = f' {row[2]}'
        ngrams[word] += count
        for n in [1,2,3,4,5,6,7,8,9,10]:
            if i > 1000 or n <= 2:
                for ngram in [word[i:i+n] for i in range(len(word)-n+1)]:
                    if ngram != word:
                        ngrams[ngram] += count

    ngram_list = ['.',',']
    ngram_list += [ng[0] for ng in ngrams.most_common(pc.get_max())]

    ngram_list = [quote(ng) for ng in ngram_list]

    # Add all URL encoded byte values
    for i in range(128):
        ngram_list.insert(pc.cutoff, quote(chr(i)))

    for i in range(128,256):
        ngram_list.insert(pc.cutoff, '%' + hex(i)[-2:].upper())

    # Remove duplicates
    ngram_list = list(OrderedDict.fromkeys(ngram_list))

    # Remove 2 character ngrams encoded in two characters
    ngram_list = [ng for (i,ng) in enumerate(ngram_list) if i < pc.cutoff or len(ng) != 2]

    for i, ngram in enumerate(ngram_list[:pc.get_max()]):
        decmap[pc.get_code(i)] = ngram
        encmap[ngram] = pc.get_code(i)
        #print(i, pc.get_code(i), ngram)

def encode(text):
    quoted = quote(text)

    i = 0
    output = ""
    while i < len(quoted):
        for j in range(10,0,-1):
            if quoted[i:i+j] in encmap:
                output += encmap[quoted[i:i+j]]
                i += j
                break
        else:
            raise ValueError(f"Invalid character {quoted[i:i+10]} position {i}")

    print(f'{len(output) / len(text):.2%} the size of plain text')
    print(f'{len(output) / len(quoted):.2%} the size of URL encoded text')

    return output

def decode(text):
    i = 0
    output = ""
    while i < len(text):
        for j in range(1,3):
            if text[i:i+j] in decmap:
                output += decmap[text[i:i+j]]
                i += j
                break
        else:
            raise ValueError(f"Invalid character at position {i}")

    return unquote(output)

with open('info-theory.txt') as f:
    text = f.read()
    compressed = encode(text)
    decoded = decode(compressed)

    errors = 0
    for i in range(len(text)):
        if text[i] != decoded[i]:
            print(i, text[i-10:i+10], decoded[i-10:i+10])
            errors += 1
            if (errors > 10): exit(1)
    assert(text == decoded)
