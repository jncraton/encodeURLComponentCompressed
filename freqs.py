from collections import Counter, OrderedDict
from urllib.parse import quote, unquote
import re
import csv
import codecs

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
    pc = PrefixCoder(chars=".,!'GHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz?/:@-_~$&()*+;=", cutoff=64)

    for (i,row) in enumerate(csv.reader(f, delimiter=' ')):
        count = int(row[1])
        word = f' {row[2]}'
        ngrams[word] += count
        for n in [1,2,3,4,5,6,7,8,9,10]:
            if i > 24 or n < 2:
                for ngram in [word[i:i+n] for i in range(len(word)-n+1)]:
                    if ngram != word:
                        ngrams[ngram] += count

    ngram_list = ['.',',','?',"'",'( ',')','"','!']
    ngram_list += [ng[0] for ng in ngrams.most_common(pc.get_max())]

    # Remove 2 character ngrams encoded in two characters
    ngram_list = [ng for (i,ng) in enumerate(ngram_list) if i < pc.cutoff or len(ng) != 2]

    ngram_list = [quote(ng) for ng in ngram_list]

    # Remove duplicates
    ngram_list = list(OrderedDict.fromkeys(ngram_list))

    ngram_list[:pc.cutoff] = sorted(ngram_list[:pc.cutoff], key=lambda n: len(n))

    single_chars = [n for n in ngram_list[:pc.cutoff] if len(n) == 1]
    current_chars = list(pc.chars)
    new_chars = single_chars + [c for c in current_chars if c not in single_chars]
    pc.chars = ''.join(new_chars)
    for i, ngram in enumerate(ngram_list[:pc.get_max()]):
        decmap[pc.get_code(i)] = ngram
        encmap[ngram] = pc.get_code(i)
        #print(i, len(ngram) / len(pc.get_code(i)), pc.get_code(i), ngram)

def gen_js(filename=None):
    import sys
    out = sys.stdout
    out.write('let encmap = [')
    for i, ngram in enumerate(reversed(ngram_list[:pc.get_max()])):
        if ngram != pc.get_code(i):
            out.write(f'["{ngram}","{pc.get_code(i)}"],')
    out.write(']\n')

gen_js()    

def preprocess(text):
    def swap_sentence_case(m):
        return m.group(0).swapcase()

    p = re.compile('(^|\. +|\n)([A-Za-z])')
    text = p.sub(swap_sentence_case, text)

    text = text.replace('(', '( ')
    text = text.replace(' I ', ' i ')
    text = text.replace('"', '" ')

    #print(text)

    return text

def postprocess(text):
    def swap_sentence_case(m):
        return m.group(0).swapcase()

    p = re.compile('(^|\. +|\n)([A-Za-z])')
    text = p.sub(swap_sentence_case, text)

    text = text.replace(' i ', ' I ')
    text = text.replace('( ', '(')
    text = text.replace('" ', '"')

    return text

def encode(text):
    quoted = quote(preprocess(text))

    i = 0
    output = ""
    while i < len(quoted):
        m = re.match(r'%([A-F0-9][A-F0-9])', quoted[i:i+3])

        for j in range(10,0,-1):
            if quoted[i:i+j] in encmap:
                output += encmap[quoted[i:i+j]]
                i += j
                break
        else:
            if m:
                output += m.group(1)
                i += 3
            else:
                output += codecs.encode(quoted[i].encode('utf8'), 'hex').decode('utf8').upper()
                i += 1
            #raise ValueError(f"Invalid character {quoted[i:i+10]} position {i}")

    print(f'{len(output) / len(text):.2%} the size of plain text')
    print(f'{len(output) / len(quoted):.2%} the size of URL encoded text')

    return output

def decode(text):
    i = 0
    output = ""

    ngrams = Counter(encmap.keys())
    for k in ngrams.keys():
        ngrams[k] -= 1
    
    while i < len(text):
        m = re.match(r'[A-F0-9][A-F0-9]', text[i:i+2])

        if text[i] in decmap:
            output += decmap[text[i]]
            ngrams[decmap[text[i]]] += 1
            i += 1
        elif text[i:i+2] in decmap:
            output += decmap[text[i:i+2]]
            ngrams[decmap[text[i:i+2]]] += 1
            i += 2
        elif m:
            output += '%' + m.group(0)
            i += 2
        else:
            raise ValueError(f"Invalid character at position {i}")

    #print(ngrams.most_common(100))

    return postprocess(unquote(output))

with open('info-theory.txt') as f:
    text = f.read()
    compressed = encode(text)
    decoded = decode(compressed)


    errors = 0
    for i in range(len(text)):
        if text[i] != decoded[i]:
            print(i, text[i-10:i+10], decoded[i-10:i+10])
            errors += 1
            if (errors > 2): exit(1)
    assert(text == decoded)
