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

## Example poems

### Hidden Markov Models

Wargami o skały i krzaki szeptały własne imię pewno  
Całować było w ogrodzie zbyt śpiewno  
Klęczał niebiosów co tylko nocny lęk i ciężki lęku  
Jęli w parowie więcej niż dźwięku  
Widzę nie wiedziała jak nęcić jakim śmiechem pośmieszyć  
Poprawiał tak sobie nieroztropnie niby przypominasz dziecięce uwierzyć

Moje. I w dłoni mi próżno, jakby z roślin  
Ciągną w supły pochody dnem dolin  
W ciszy dzień brzeziną schodzi przez pole  
O, w dole i na stole  
Złoty wygina łuk i człowiek gdy z człowieka przemawia żywy  
Znów wydzwania. Nie żegnajcie. Morze opiło się wiatru, niespokojne szarpie grzywy  
Ulicami pochodnie, wiersz jest, żyłka słoneczna na ścianie. Zasłoń firanki  
Się rzeźbi cisza... spokojny gotyk blanki  

Gwiezdną która duszę z wszechświatem spokrewnią na nowo  
Tę parskał śmiechem dziadyga w kark poklękłej ułudy  
Domyśle puszyściał jej w ciasne nie zasklepię słowo  
I był, o cudzie nad cudy
Tuła na ból swój boczył się i trwogą uderza  
Wracam długiej rozłące dłonie twoje niecierpliwe  
Mogiłom zatajone w srebrze ukwiecenie odsłaniają swe jary wzgórza  
Głąb pałaców ku górze czyniąc kroki płochliwe

### LSTM

Zeswał sił ratowałem, usta, nie ciała do kaki,  
Chciała na mnie do niebie, y ności nie nie taki,  
I na to na pusyczana i w przeswanych stroku,  
Stali na nych śniadania, w rucimi na ściaku, 