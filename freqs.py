from collections import Counter
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
            byte1 = self.chars[60 + num1]
            num2 = num % len(self.chars)
            byte2 = self.chars[num2] 
            return byte1 + byte2

with open('gsl.txt') as f:
    ngrams = Counter()
    pc = PrefixCoder()

    for row in csv.reader(f, delimiter=' '):
        count = int(row[1])
        word = f' {row[2]} '
        for n in [1,2,3,4,5,6,7]:
            for ngram in [word[i:i+n] for i in range(len(word)-n+1)]:
                ngrams[ngram] += count

    for i, ngram in enumerate(ngrams.most_common(100)):
        print(i, pc.get_code(i), ngram[0])
