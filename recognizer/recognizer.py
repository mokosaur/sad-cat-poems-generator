import re

tren1 = "Wszytki płacze, wszytki łzy Heraklitowe \n" \
        "I lamenty, i skargi Symonidowe,\n" \
        "Wszytki troski na świecie, wszytki wzdychania\n" \
        "I żale, i frasunki, i rąk łamania,\n" \
        "Wszytki a wszytki za raz w dom się mój noście,\n" \
        "A mnie płakać mej wdzięcznej dziewki pomożcie,\n" \
        "Z którą mię niepobożna śmierć rozdzieliła\n" \
        "I wszytkich moich pociech nagle zbawiła.\n" \
        "Tak więc smok, upatrzywszy gniazdko kryjome,\n" \
        "Słowiczki liche zbiera, a swe łakome\n" \
        "Gardło pasie; tymczasem matka szczebiece\n" \
        "Uboga, a na zbójcę coraz się miece,\n" \
        "Prózno ! bo i na sarnę okrutnik zmierza,\n" \
        "A ta nieboga ledwe umyka pierza.\n" \
        "Prózno płakać - podobno drudzy rzeczecie.\n" \
        "Cóż, prze Bóg żywy, nie jest prózno na świecie?\n" \
        "Wszytko prózno! Macamy, gdzie miękcej w rzeczy,\n" \
        "A ono wszędy ciśnie! Błąd - wiek człowieczy!\n" \
        "Nie wiem, co lżej : czy w smutku jawnie żałować,\n" \
        "Czyli się z przyrodzeniem gwałtem mocować?"

toast = "Nie ma nic prócz tych liści, co na drzewach zmarły,\n" \
        "Nic nie ma prócz tych wichrów, którymi przewiało,\n" \
        "Nic prócz śladów świetności, co się już zatarły\n" \
        "Nie stanie się nic więcej. Już wszystko się stało."

koniec_wieku = "Przekleństwo-... tylko dziki, kiedy się skaleczy,\n" \
               "złorzeczy swemu bogu, skrytemu w przestworze.\n" \
               "Ironia-... Lecz największe z szyderstw czyż się może\n" \
               "równać z ironią biegu najzwyklejszych rzeczy"

class Recognizer:
    def analyze(self, text):
        text = re.sub('[.,!?]+', '', text)
        to_analyze = []
        for line in text.split("\n"):
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
recognizer.analyze(tren1)
recognizer.analyze(toast)
recognizer.analyze(koniec_wieku)