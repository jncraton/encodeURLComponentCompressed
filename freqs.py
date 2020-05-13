from collections import Counter

with open('words.txt') as f:
    words = f.read().replace('\n',' ')
    
    ngrams = Counter()

    for n in [1,2,3,4]:
        ngrams.update([words[i:i+n] for i in range(len(words)-n+1) if not ' ' in words[i:i+n]])

    print(ngrams.most_common(54+27*81-256))
    print(54+27*81-256)

"""
Format

trit 1
    0 - Lower 1 byte sequence
    1 - Upper 1 byte sequence
    2 - 2 Bytes sequence
"""
