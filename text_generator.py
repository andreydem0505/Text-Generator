from nltk.tokenize import regexp_tokenize
from collections import Counter
from collections import defaultdict
import random


def start_criteria(string):
    return string[0].isupper() and string[-1] not in '.!?'


class Model:
    sentences_size = 1
    sentence_size = 100

    def generate_text(self):
        pass


class Bigrams(Model):
    def __init__(self, tokens_list):
        super().__init__()
        self.model = defaultdict(Counter)
        for i in range(len(tokens_list) - 1):
            self.model[tokens_list[i]][tokens_list[i + 1]] += 1

    def generate_text(self):
        for i in range(self.sentences_size):
            last_token = ' '
            counter = 0
            while counter < self.sentence_size or last_token[-1] not in '.!?':
                if counter == 0:
                    last_token = random.choice(list(filter(start_criteria, list(self.model.keys()))))
                else:
                    keys = list(self.model[last_token].keys())
                    values = list(self.model[last_token].values())
                    last_token = random.choices(keys, values)[0]
                print(last_token, end=' ')
                counter += 1
            print()


class Trigrams(Model):
    def __init__(self, tokens_list):
        super().__init__()
        self.model = defaultdict(Counter)
        for i in range(len(tokens_list) - 2):
            self.model[f'{tokens_list[i]} {tokens_list[i + 1]}'][tokens_list[i + 2]] += 1

    def generate_text(self):
        for i in range(self.sentences_size):
            last_token = ' '
            counter = 0
            while counter < self.sentence_size - 1 or last_token[-1] not in '.!?':
                if counter == 0:
                    keys = list(self.model.keys())
                    last_token = random.choice(list(filter(lambda x: start_criteria(x.split()[0]), keys)))
                else:
                    keys = list(self.model[last_token].keys())
                    values = list(self.model[last_token].values())
                    last_token = f'{last_token.split()[1]} {random.choices(keys, values)[0]}'
                print(last_token.split()[0], end=' ')
                counter += 1
            print(last_token.split()[1])


if __name__ == '__main__':
    filename = input()
    file = open(filename, "r", encoding="utf-8")
    tokens = regexp_tokenize(file.read(), "\\S+")
    model = Trigrams(tokens)
    model.generate_text()
