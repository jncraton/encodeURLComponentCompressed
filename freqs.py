from collections import Counter
from urllib.parse import quote
import csv

class PrefixCoder:
    def __init__(self, cutoff=60, chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890?/:@-._~!$&'()*+,;="):
        self.cutoff = cutoff
        self.chars = chars
        
    def get_code(self, num):
        if (num < self.cutoff):
            return self.chars[num]
        else:
            num1 = int(num / len(self.chars))
            byte1 = self.chars[self.cutoff + num1]
            num2 = num % len(self.chars)
            byte2 = self.chars[num2] 
            return byte1 + byte2

    def get_max(self):
        return (len(self.chars) - self.cutoff) * len(self.chars)

encmap = {}
decmap = {}
with open('gsl.txt') as f:
    ngrams = Counter()
    pc = PrefixCoder()

    for row in csv.reader(f, delimiter=' '):
        count = int(row[1])
        word = f' {row[2]}'
        ngrams[word] += count
        for n in [1,2,3,4,5,6,7,8,9,10]:
            for ngram in [word[i:i+n] for i in range(len(word)-n+1)]:
                if ngram != word:
                    ngrams[ngram] += count

    ngram_list = ['.',',','!','?',' ','  ','    ']
    ngram_list += [ng[0] for ng in ngrams.most_common(pc.get_max())]

    ngram_list = [quote(ng) for ng in ngram_list]

    # Add all URL encoded byte values
    for i in range(128):
        text = quote(chr(i))
        if not text in ngram_list:
            ngram_list.insert(pc.cutoff, text)

    for i in range(128,256):
        text = '%' + hex(i)[-2:].upper()
        if not text in ngram_list:
            ngram_list.insert(pc.cutoff, text)        

    for i, ngram in enumerate(ngram_list[:pc.get_max()]):
        decmap[pc.get_code(i)] = ngram
        encmap[ngram] = pc.get_code(i)

with open('pride-and-prejudice.txt') as f:
    text = f.read()
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
            raise ValueError("Invalid character at position " + i)

print(f'{len(output) / len(text):.0%} the size of plain text')
print(f'{len(output) / len(quoted):.0%} the size of URL encoded text')