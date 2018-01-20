class CharTokenizer:
    def transform(self, X):
        letters = sorted(list(set('\n'.join(X).lower())))
        lookup = {c: i for i, c in enumerate(letters)}
        return {'raw': X, 'lookup': lookup}
