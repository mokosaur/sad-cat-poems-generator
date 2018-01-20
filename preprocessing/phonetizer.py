import re


class StandardPhonetizer:
    def __init__(self):
        pass

    def transform(self, X):
        transformed = []
        for string in X:
            rep = {"a": "a",
                   "ó": "u",
                   "ęł": "eł",
                   "ęl": "el",
                   "ę ": "e ",
                   "cz": "č",
                   "sz": "š",
                   "prz": "pš",
                   "trz": "tš",
                   "krz": "kš",
                   "chrz": "χš",
                   r"\brz": "ž",
                   "ż": "ž",
                   "ch": "χ",
                   'wsz': "fš",
                   "ł":   "u̯",
                   "ci": "ć",
                   "si": "ś",
                   "ni": "ń",
                   "ia": "ja",
                   "io": "jo",
                   "iu": "ju",
                   "ie": "je",
                   "ąb": "omb",
                   "ąp": "omp",
                   "ą(^\b)": r"on",
                   "dz": "ʒ́",
                   r"ę\b": "e"
                   }
            for k, v in rep.items():
                pattern = re.compile(k)
                string = re.sub(pattern, v, string)
            transformed.append(string)
        return transformed
