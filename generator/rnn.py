from generator.base import BaseGenerator
from preprocessing.tokenizer import CharTokenizer
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
import numpy as np
import os


class LSTMGenerator(BaseGenerator):
    def __init__(self, preprocessor=CharTokenizer(), line_by_line=False, sequence_length=100):
        BaseGenerator.__init__(self, preprocessor)
        self.line_by_line = line_by_line
        self.sequence_length = sequence_length
        self.model = None

    def _fit_transformed(self, X):
        self.lookup = X['lookup']
        self.X = X['raw']
        X_train, y_train = self._sample_lines(X['raw'])
        X_train = np.reshape(X_train, (len(X_train), self.sequence_length, 1))
        X_train = X_train / len(self.lookup)
        y_train = np_utils.to_categorical(y_train)

        # define the LSTM model
        self.model = Sequential()
        self.model.add(LSTM(256, input_shape=(X_train.shape[1], X_train.shape[2])))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(y_train.shape[1], activation='softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer='adam')

        # define the checkpoint
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "models", "model-{epoch:02d}-{loss:.4f}.hdf5")
        checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
        callbacks_list = [checkpoint]

        self.model.fit(X_train, y_train, epochs=20, batch_size=128, callbacks=callbacks_list)

    def _sample_lines(self, X):
        X_data = []
        y_data = []
        for x in X:
            if self.line_by_line:
                pass
            else:
                for i in range(len(x) - self.sequence_length):
                    X_data.append([self.lookup[c.lower()] for c in x[i:i + self.sequence_length]])
                    y_data.append(self.lookup[x[i + self.sequence_length].lower()])
        return X_data, y_data

    def generate(self, pattern, model_name=None, data=None, temperature=0.25):
        if model_name:
            self.model = load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", model_name))
        if data:
            data = self.preprocessor.transform(data)
            self.lookup = data['lookup']
            self.X = data['raw']
        lookup_inverse = {v: k for k, v in self.lookup.items()}
        pattern = [self.lookup[x.lower()] for x in self.X[0][0:100]]
        gentext = []
        for i in range(1000):
            x = np.reshape(pattern, (1, len(pattern), 1))
            x = x / len(self.lookup)
            prediction = self.model.predict(x, verbose=0)
            index = self._get_prediction(prediction, temperature) if temperature else np.argmax(prediction)
            result = lookup_inverse[index]
            seq_in = [lookup_inverse[value] for value in pattern]
            # sys.stdout.write(result)
            gentext.append(result)
            pattern.append(index)
            pattern = pattern[1:len(pattern)]
        return ''.join(gentext)

    def _get_prediction(self, softmax, temperature):
        softmax = softmax[0]
        softmax = np.log(softmax) / temperature
        dist = np.exp(softmax) / np.sum(np.exp(softmax))
        choices = range(len(softmax))
        return np.random.choice(choices, p=dist)
