import random
import re

from dataset.loader import load_author
from generator.base import BaseGenerator
from recognizer.recognizer import Recognizer, RhymeType


class Markov(BaseGenerator):
    def __init__(self, preprocessor=None, recognizer=Recognizer()):
        super().__init__(preprocessor)
        self.word_size = 0
        self.words = []
        self.cache = {}
        self.recognizer = recognizer

    def triples(self):
        if len(self.words) < 3:
            return

        for i in range(len(self.words) - 2):
            yield (self.words[i], self.words[i + 1], self.words[i + 2])

    def database(self):
        for w1, w2, w3 in self.triples():
            key = (w1, w2)
            if key in self.cache:
                self.cache[key].append(w3)
            else:
                self.cache[key] = [w3]

    def _fit_transformed(self, X):
        base_text = ""
        for poem in X:
            poem = re.sub('[^\w \n]+', '', poem)
            poem = poem.lower()
            poem = " ".join(list(reversed(poem.split())))
            base_text += poem
        self.words = base_text.split()
        self.word_size = len(self.words)
        self.database()

    def generate(self, rhyme_type):
        size = random.randint(4, 7)
        generated_text = []
        current_size = 0
        while current_size < size:
            next_word, seed_word = self.get_seed_word()
            rhyme_index = self.recognizer.find_rhyme_for_word(seed_word, self.words)
            if rhyme_index is not None:
                generated_line = self.generate_line(seed_word, next_word)
                generated_line += "\n"
                generated_text.append(generated_line)
                seed_word, next_word = self.words[rhyme_index], self.words[rhyme_index + 1]
                generated_line = self.generate_line(seed_word, next_word)
                generated_line += "\n"
                generated_text.append(generated_line)
                current_size += 1
        return self.match_rhyme_pattern(generated_text, rhyme_type)

    def get_seed_word(self):
        seed_len = 0
        while seed_len <= 3:
            seed = random.randint(0, self.word_size - 3)
            seed_len = len(self.words[seed])
        seed_word, next_word = self.words[seed], self.words[seed + 1]
        return next_word, seed_word

    def generate_line(self, w1, w2):
        size = random.randint(4, 8)
        gen_words = []
        for i in range(size):
            gen_words.append(w1)
            w1, w2 = w2, random.choice(self.cache[(w1, w2)])
        gen_words.append(w2)
        print(gen_words)
        return ' '.join(list(reversed(gen_words)))

    def match_rhyme_pattern(self, line_list, rhyme_type):
        if rhyme_type == RhymeType.PARZYSTE:
            return ''.join(line_list)
        elif rhyme_type == RhymeType.PRZEPLATANE:
            final = ""
            for (a, b, c, d) in zip(line_list[0::4], line_list[1::4], line_list[2::4], line_list[3::4]):
                final += a
                final += c
                final += b
                final += d
            return final
        elif rhyme_type == RhymeType.OKALAJCE:
            final = ""
            for (a, b, c, d) in zip(line_list[0::4], line_list[1::4], line_list[2::4], line_list[3::4]):
                final += a
                final += c
                final += d
                final += b
            return final