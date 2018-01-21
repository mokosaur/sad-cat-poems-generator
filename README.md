# Polish Poetry Generator

This project contains two classic approaches to text generation, i.e. Hidden Markov Model and LSTM. You can choose one of the implemented models and start playing with generationg new poems. 
We implemented some algorithms to cope with Polish language problems, such as phonetization of Polish words. If you want to generate poetry in your language, you should change these algorithms to ones working with your language of choice.

## Dependencies

- **Python 3**
- Downloading poems:
  - **BeautifulSoup**
  - **Requests**
- Working with LSTMs:
  - **Keras**
  - **Numpy**
 
## Quick start

1. Run `dataset/poemsminer.py` to download the dataset.
2. Load the data 
```python
from dataset.loader import load_author

poems = [value for value in load_author("kochanowski").values()]
```
3. Train a chosen model
```python
markov = Markov()
markov.fit(poems)
```
4. Generate your poems!
```python
print(markov.generate())
```