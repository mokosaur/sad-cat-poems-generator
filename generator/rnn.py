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
    def __init__(self, preprocessor=CharTokenizer(), sequence_length=100,
                 num_epochs=300, num_units=256, num_layers=2, batch_size=128, reverse_generation=True):
        BaseGenerator.__init__(self, preprocessor)
        self.sequence_length = sequence_length
        self.model = None
        self.num_epochs = num_epochs
        self.num_layers = num_layers
        self.num_units = num_units
        self.batch_size = batch_size
        self.reverse_generation = reverse_generation

    def _fit_transformed(self, X):
        self.lookup = X['lookup']
        self.X = X['raw']
        X_train, y_train = self._sample_lines(X['raw'])
        X_train = np.reshape(X_train, (len(X_train), self.sequence_length, 1))
        X_train = X_train / len(self.lookup)
        y_train = np_utils.to_categorical(y_train)

        # define the LSTM model
        self.model = Sequential()
        self.model.add(LSTM(self.num_units, input_shape=(X_train.shape[1], X_train.shape[2]),
                            return_sequences=(self.num_layers > 1)))
        self.model.add(Dropout(0.2))
        for i in range(self.num_layers - 1):
            self.model.add(LSTM(self.num_units, return_sequences=(i < self.num_layers - 2)))
            self.model.add(Dropout(0.2))
        self.model.add(Dense(y_train.shape[1], activation='softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer='adam')

        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "models", "model-{epoch:02d}-{loss:.4f}.hdf5")
        checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
        callbacks_list = [checkpoint]

        self.model.fit(X_train, y_train, epochs=self.num_epochs, batch_size=self.batch_size, callbacks=callbacks_list)

    def _sample_lines(self, X):
        X_data = []
        y_data = []
        for x in X:
            x_rev = x[::-1] if self.reverse_generation else x
            for i in range(len(x_rev) - self.sequence_length):
                X_data.append([self.lookup[c.lower()] for c in x_rev[i:i + self.sequence_length]])
                y_data.append(self.lookup[x_rev[i + self.sequence_length].lower()])
        return X_data, y_data

    def generate(self, pattern=None, model_name=None, data=None, temperature=0.25):
        if model_name:
            self.model = load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", model_name))
        if data:
            data = self.preprocessor.transform(data)
            self.lookup = data['lookup']
            self.X = data['raw']
        lookup_inverse = {v: k for k, v in self.lookup.items()}
        if not pattern:
            pattern = self.X[0][:self.sequence_length]
        if self.reverse_generation:
            pattern = pattern[::-1]
        gentext = [x for x in pattern]
        pattern = [self.lookup[x.lower()] for x in pattern.zfill(self.sequence_length)]
        for i in range(1000):
            x = np.reshape(pattern, (1, len(pattern), 1))
            x = x / len(self.lookup)
            prediction = self.model.predict(x, verbose=0)
            index = self._get_prediction(prediction, temperature) if temperature else np.argmax(prediction)
            result = lookup_inverse[index]
            gentext.append(result)
            pattern.append(index)
            pattern = pattern[1:len(pattern)]
        if self.reverse_generation:
            gentext = gentext[::-1]
        return ''.join(gentext)

    def _get_prediction(self, softmax, temperature):
        softmax = softmax[0]
        softmax = np.log(softmax) / temperature
        dist = np.exp(softmax) / np.sum(np.exp(softmax))
        choices = range(len(softmax))
        return np.random.choice(choices, p=dist)
