from collections import Counter
import csv

def get_prefix_code(num,cutoff=60):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890?/:@-._~!$&'()*+,;="

    if (num < cutoff):
        return chars[num]
    else:
        num1 = int(num / len(chars))
        byte1 = chars[60 + num1]
        num2 = num % len(chars)
        byte2 = chars[num2] 
        return byte1 + byte2

with open('gsl.txt') as f:
    ngrams = Counter()

    for row in csv.reader(f, delimiter=' '):
        count = int(row[1])
        word = f' {row[2]} '
        for n in [1,2,3,4,5,6,7]:
            for ngram in [word[i:i+n] for i in range(len(word)-n+1)]:
                ngrams[ngram] += count

    for i, ngram in enumerate(ngrams.most_common(100)):
        print(i, get_prefix_code(i), ngram[0])
