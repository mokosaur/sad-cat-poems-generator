from generator.base import BaseGenerator
from preprocessing.tokenizer import CharTokenizer


class LSTMGenerator(BaseGenerator):
    def __init__(self, preprocessor, line_by_line=False, sequence_length=100):
        BaseGenerator.__init__(self, preprocessor)
        self.line_by_line = line_by_line
        self.sequence_length = sequence_length

    def _fit_transformed(self, X):
        self.lookup = X['lookup']
        samples = self._sample_lines(X['raw'])

    def _sample_lines(self, X):
        lines = []
        for x in X:
            X_data = []
            y_data = []
            if self.line_by_line:
                pass
            else:
                for i in range(len(x) - self.sequence_length):
                    X_data.append([self.lookup[c.lower()] for c in x[i:i + self.sequence_length]])
                    y_data.append(self.lookup[x[i + self.sequence_length].lower()])
            lines.append({'X': X_data, 'y': y_data})
        return lines

    def generate(self):
        pass


from dataset.loader import load_author

treny = ['\n'.join([v for v in load_author('kochanowski', ['treny']).values()])]
tokenizer = CharTokenizer()
lstm = LSTMGenerator(tokenizer)
lstm.fit(treny)
