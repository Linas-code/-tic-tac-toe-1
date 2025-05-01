
# 🎮 Kursinis darbas – „Tic Tac Toe“ žaidimas su dirbtiniu intelektu

## 📌 Įžanga (Introduction)

**Kas tai per programa?**  
Ši programa yra klasikinis kryžiukų-nuliukų („Tic Tac Toe“),
žaidimas sukurta naudojant `tkinter` grafinę vartotojo sąsają.
Žaidėjas gali pasirinkti, ar žaisti prieš kitą žmogų, ar prieš dirbtinio intelekto (AI) žaidėją.

**Kaip paleisti programą?**  
1. Įsitikinkite, kad turite įdiegtą `Python 3`.
2. Paleiskite failą:
   ```bash
   python main.py
   ```

**Kaip naudotis programa?**  
- Pasirinkite antrąjį žaidėją (žmogų arba AI).
- Pasirinkite žaidėjo simbolį (X arba O).
- Spauskite **Start Game**.
- Spauskite ant lentos langelių norėdami atlikti ėjimą. Žaidimas baigiasi, kai vienas žaidėjas laimi arba įvyksta lygiosios.

---

## 🔍 Analizė (Body/Analysis)

### 🧱 Objektinio programavimo principai (4 OOP principai)

**1. Inkapsuliacija (Encapsulation)**  
Naudojami „privatūs“ atributai su `_` ir `@property`, kad duomenys būtų saugomi klasės viduje:
```python
class Board:
    def __init__(self, size=3, win_length=3):
        self._size = size
        self._win_length = win_length
        self._board = [[" " for _ in range(size)] for _ in range(size)]

    @property
    def size(self):
        return self._size
```

**2. Abstrakcija (Abstraction)**  
Sukuriama abstrakti `Player` klasė, kuri reikalauja įgyvendinti metodą `make_move()`:
```python
class Player(abc.ABC):
    @abc.abstractmethod
    def make_move(self, board, row=None, col=None):
        pass
```

**3. Paveldėjimas (Inheritance)**  
Klasės `HumanPlayer` ir `HardAIPlayer` paveldi `Player`:
```python
class HumanPlayer(Player):
    def make_move(self, board, row, col):
        return board.make_move(row, col, self.symbol)
```

**4. Polimorfizmas (Polymorphism)**  
`make_move()` metodas veikia skirtingai priklausomai nuo žaidėjo tipo:
```python
# Human žaidėjo ėjimas
def make_move(self, board, row, col):
    return board.make_move(row, col, self.symbol)

# AI žaidėjo ėjimas su logika laimėti ar blokuoti
def make_move(self, board, row=None, col=None):
    # AI strategija čia
```

---

### 🎨 Naudotas dizaino šablonas (Design Pattern)

**🎯 Factory Method Pattern**  
Naudojama žaidėjų sukūrimui dinaminiu būdu:

```python
class PlayerFactory:
    @staticmethod
    def create_player(player_type, symbol, opponent_symbol="X"):
        if player_type == "human":
            return HumanPlayer(symbol)
        elif player_type == "AI":
            return HardAIPlayer(symbol, opponent_symbol)
```

**Kodėl šis šablonas tinkamas?**
- Lengva išplėsti: galima pridėti kitų žaidėjų rūšių (pvz. lengvesnį AI).
- Vartotojo pasirinkimai GUI perduodami šablonui, kuris grąžina tinkamą objektą.

---

### 🔧 Kompozicija ir/ar agregacija

- Klasė `Game` priklauso nuo kitų objektų (`Board`, `GUI`, `Players`) – jie perduodami kaip priklausomybės.
- Tai kompozicija: `Game` naudoja šiuos objektus, bet jų nekuria:
```python
class Game:
    def __init__(self, players, board, gui):
        self._players = players
        self._board = board
        self._gui = gui
```

---

### 📂 Failų skaitymas ir rašymas

- Naudojamas failas `results.txt`, kuriame saugomi žaidimo rezultatai.
- Jei failas neegzistuoja arba tuščias – rodoma žinutė „No previous results“.

```python
def save_result(self, winner):
    with open("results.txt", "a", encoding="utf-8") as file:
        if winner:
            file.write(f"Winner: {winner}\n")
        else:
            file.write("Draw\n")

def load_results(self):
    try:
        with open("results.txt", "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                return "No previous results."
        return content
    except FileNotFoundError:
        return "No previous results."
```

---

### ✅ Unit Testai

Testuojamos svarbiausios funkcijos su `unittest` moduliu:

- Lentelės funkcijos (`make_move`, `check_winner`, `undo_move`)
- `PlayerFactory` klasės kūrimo metodai
- GUI failų įkėlimo logika (naudojant `mock`)
- `Game` pradinė logika

```python
def test_check_winner_row(self):
    self.board.make_move(0, 0, 'X')
    self.board.make_move(0, 1, 'X')
    self.board.make_move(0, 2, 'X')
    self.assertEqual(self.board.check_winner(), 'X')
```

---

## ✅ Rezultatai (Results)

- ✅ Įgyvendinti visi keturi OOP principai aiškiai ir teisingai
- ✅ Pritaikytas „Factory Method“ dizaino šablonas
- ✅ Failų įrašymas/skaitymas veikia sklandžiai
- ✅ Testai padengia pagrindines funkcijas
- ✅ Vartotojo sąsaja funkcionali ir intuityvi
- ⚠️ AI logika pagrįsta paprasta strategija – galima patobulinti naudojant Minimax algoritmą

---

## 🧠 Išvados (Conclusions)

- Sukurtas „Tic Tac Toe“ žaidimas sėkmingai įgyvendina OOP principus bei dizaino šablonus.
- AI žaidėjas sugeba reaguoti į žaidėjo veiksmus (bando laimėti arba blokuoti).
- Programa palaiko rezultatų saugojimą ir testavimą.
- Plėtros kryptys:
  - Pridėti „Minimax“ AI algoritmą
  - Padidinti lentos dydį (5x5 ar kintamą)
  - Pridėti žaidimų istoriją su datomis
  - Pridėti daugiau žaidėjų arba kelių raundų režimą

---

## 📚 Naudoti šaltiniai (Resources)

- [PEP8 – Python stiliaus vadovas](https://peps.python.org/pep-0008/)
- [Python unittest dokumentacija](https://docs.python.org/3/library/unittest.html)
- [Refactoring Guru – Factory Pattern](https://refactoring.guru/design-patterns/factory-method)
- Asmeninė patirtis, dėstytojo skaidrės, Stack Overflow
