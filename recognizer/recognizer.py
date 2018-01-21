import random
import re
from enum import Enum, auto

from preprocessing.phonetizer import StandardPhonetizer


class Recognizer:
    def analyze(self, text):
        text = re.sub('[^\w \n]+', '', text)
        text = text.lower()
        to_analyze = []
        for line in text.split("\n"):
            if line != "":
                if len(line.split()[-1]) < 7:
                    to_analyze.append((" ".join(line.split()[-2:])))
                else:
                    to_analyze.append(line.split()[-1])
        patterns = self.check_for_patterns(to_analyze)
        parzyste = self.check_if_rymy_parzyste(patterns)
        przeplatane = self.check_if_rymy_przeplatane(patterns)
        okalajace = self.check_if_rymy_okalajace(patterns)
        if parzyste > 0.5 and parzyste >= przeplatane and parzyste >= okalajace:
            return RhymeType.PARZYSTE
        elif przeplatane > 0.5 and przeplatane >= parzyste and przeplatane >= okalajace:
            return RhymeType.PRZEPLATANE
        elif okalajace > 0.5 and okalajace >= parzyste and okalajace >= przeplatane:
            return RhymeType.OKALAJCE
        else:
            return RhymeType.INNE

    def check_if_rymy_parzyste(self, patterns):
        counter = 0
        all_pairs = 0
        for (a, b) in zip(patterns[:-1:2], patterns[1::2]):
            if a == b:
                counter += 1
            all_pairs += 1
        # print("Rymy parzyste: ", counter, all_pairs)
        return counter / all_pairs

    def check_if_rymy_przeplatane(self, patterns):
        counter = 0
        all_pairs = 0
        for (a, b) in zip(patterns[0:], patterns[2:]):
            if a == b:
                counter += 1
            all_pairs += 1
        # print("Rymy przeplatane: ", counter, all_pairs)
        return counter / all_pairs

    def check_if_rymy_okalajace(self, patterns):
        counter = 0
        all_fours = 0
        for (a, b, c, d) in zip(patterns[0::4], patterns[3::4], patterns[1::4], patterns[2::4]):
            if a == b and c == d:
                counter += 1
            all_fours += 1
        # print("Rymy okalające: ", counter, all_fours)
        return counter / all_fours

    def are_rhymes(self, a, b, match=2):
        return a[-match:] == b[-match:]

    def check_for_patterns(self, to_analyze):
        patterns = ['_' for i in range(len(to_analyze))]
        current_letter = ord("a")
        for i in range(len(to_analyze)):
            if patterns[i] == "_":
                patterns[i] = chr(current_letter)
                current_letter += 1
                for j in range(i+1, len(to_analyze)):
                    if self.are_rhymes(to_analyze[i], to_analyze[j]):
                        patterns[j] = patterns[i]
        return patterns

    def find_rhyme_for_word(self, word, word_list):
        word_list = StandardPhonetizer().transform(word_list)
        rhymes = []
        for i, potential in enumerate(word_list):
            if word != potential and self.are_rhymes(word, potential, match=3):
                rhymes.append(i)
        if len(rhymes) > 1:
            return random.choice(rhymes)
        else:
            return None


class RhymeType(Enum):
    PARZYSTE = auto()
    OKALAJCE = auto()
    PRZEPLATANE = auto()
    INNE = auto()