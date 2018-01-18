import re

from dataset.loader import load_author

class Recognizer:
    def analyze(self, text):
        text = re.sub('[.,!?]+', '', text)
        to_analyze = []
        for line in text.split("\n"):
            if line != "":
                if len(line.split()[-1]) < 7:
                    to_analyze.append((" ".join(line.split()[-2:])))
                else:
                    to_analyze.append(line.split()[-1])
        self.check_if_rymy_parzyste(to_analyze)
        self.check_if_rymy_przeplatane(to_analyze)
        self.check_if_rymy_okalajace(to_analyze)

    def check_if_rymy_parzyste(self, to_analyze):
        counter = 0
        all_pairs = 0
        for (a, b) in zip(to_analyze[:-1:2], to_analyze[1::2]):
            if self.are_rhymes(a, b):
                counter += 1
            all_pairs += 1
        if counter / all_pairs > 0.5:
            print("Wiersz ma rymy parzyste")
        return counter / all_pairs > 0.5

    def check_if_rymy_przeplatane(self, to_analyze):
        counter = 0
        all_pairs = 0
        for (a, b) in zip(to_analyze[0:], to_analyze[2:]):
            if self.are_rhymes(a, b):
                counter += 1
            all_pairs += 1
        if counter / all_pairs > 0.5:
            print("Wiersz ma rymy przeplatane")
        return counter / all_pairs > 0.5

    def check_if_rymy_okalajace(self, to_analyze):
        counter = 0
        all_fours = 0
        for (a, b, c, d) in zip(to_analyze[0::4], to_analyze[3::4], to_analyze[1::4], to_analyze[2::4]):
            if self.are_rhymes(a, b) and self.are_rhymes(c, d):
                counter += 1
            all_fours += 1
        if counter / all_fours > 0.5:
            print("Wiersz ma rymy okalające")
        return counter / all_fours > 0.5

    def are_rhymes(self, a, b):
        counter = 0
        for (el_a, el_b) in zip(a[::-1], b[::-1]):
            if el_a == el_b:
                counter += 1
        return counter >= 3


recognizer = Recognizer()
recognizer.analyze(load_author("lesmian", ["poems"])["Tęcza - Bolesław Leśmian"])