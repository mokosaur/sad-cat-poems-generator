from abc import ABC, abstractmethod


class BaseGenerator(ABC):
    def __init__(self, preprocessor):
        self.preprocessor = preprocessor

    def fit(self, X):
        X_transformed = self.preprocessor.transform(X)
        self._fit_transformed(X_transformed)

    @abstractmethod
    def _fit_transformed(self, X):
        ...

    def fit_generate(self, X, *args, **kwargs):
        self.fit(X)
        return self.generate(*args, **kwargs)

    @abstractmethod
    def generate(self):
        ...
