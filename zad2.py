"""
2. Opracować kod korygujący podwójny błąd bitowy dla wiadomości ośmiobitowych (1 bajt)

macierz r x n - (8x16) - r = bity parzystości, n = dane + bity parzystości

    obliczanie bitów parzystości
    dla każdego bitu parzystości bierzemy kolumne (kolumna ma 1 i 0)
        - tam gdzie jest 1 w kolumnie to tą pozycje wektora danych kontroluje
        - wykonywana jest operacja xor na danych żeby obliczyć wartość bitu parzystości

    Wykrywanie i korekcja błędów
    obliczany jest syndrom - iloczyn macierzy H ze słowem kodowym
        jeśli wynik syndromu wynosi 0 to nie ma błędu
        jeśli jest inny to sprwdzamy czy któraś z kolumn jest równa syndromowi - błąd dotyczy wtedy konkretnego bitu
        do wykrycia podwójnego błędu wymagane jest znalezienie 2 kolum których suma (oparcja xor) jest równa syndromowi
            jak zostaną znalezione oznacza że błędy są na bitach odpowiadającym indeksom kolumn

        -- jeśli syndrom jest różny od zera i jest równy którejś kolumnie to jest 1 błąd
        -- jeśli syndrom jest różny od zera i jest równy sumie (oparca xor) 2 kolumn to pozycja kolumn wskazuje bity błędu

Właściwości macierzy H dla korekcji 2 błędów
    1. Macierz nie może mieć kolumny zerowej
            żaden bit parzystości nie byłby powiązany z bitem wiadomości
    2. nie może mieć identycznych kolumn,
            dane 2 kolumny kontrolowałyby te same bity parzystości
                -- błędy na tych pozycjach sa nierozróżnialne
    3. suma 2 kolumn nie może się równać innej kolumnie
            nie bedzie można rozpoznać gdzie dokładnie błąd, bo syndrom będzie wyglądał tak samo dla róznych kolumn
    4. suma 2 kolum nie może się równać sumie 2 innych kolumn
            tak samo jak w poprzednim
"""
import numpy as np

H = [
    [1,1,1,1,0,0,0,0 ,1,0,0,0,0,0,0,0],
    [1,1,0,0,1,1,0,0 ,0,1,0,0,0,0,0,0],
    [1,0,1,0,1,0,1,0 ,0,0,1,0,0,0,0,0],
    [0,1,0,1,0,1,1,0 ,0,0,0,1,0,0,0,0],
    [1,1,1,0,1,0,0,1 ,0,0,0,0,1,0,0,0],
    [1,0,0,1,0,1,0,1 ,0,0,0,0,0,1,0,0],
    [0,1,1,1,1,0,1,1 ,0,0,0,0,0,0,1,0],
    [1,1,1,0,0,1,1,1 ,0,0,0,0,0,0,0,1]
]

def str_to_bin(message):
    return [format(ord(c), '08b') for c in message]

def bin_to_str(binary_list):
    return ''.join(chr(int(b, 2)) for b in binary_list)

# Funkcja kodująca wiadomość za pomocą macierzy H (dodaje bity parzystości)
def encode(message, H):
    H = np.array(H)
    encoded_msg = []  # Lista na zakodowane wiadomości
    for char in str_to_bin(message):  # Iteracja po każdym znaku w postaci binarnej
        data_bits = np.array([int(b) for b in char])  # Zamiana binarnego ciągu na listę bitów
        parity_bits = (H[:, :8] @ data_bits) % 2  # Obliczanie bitów parzystości
        codeword = np.concatenate((data_bits, parity_bits))  # Łączenie bitów danych i parzystości
        encoded_msg.append(codeword)  # Dodanie zakodowanego słowa do listy
    return np.array(encoded_msg)

# Funkcja obliczająca syndrom dla danego słowa kodowego
def syndrome_check(codeword, H):
    H = np.array(H)
    syndrome = (H @ codeword) % 2  # Obliczanie syndromu (H * codeword mod 2)
    return syndrome

# Funkcja korygująca błędy w zakodowanej wiadomości
def correct_errors(encoded_msg, H):
    H = np.array(H)
    corrected_msg = []  # Lista na poprawione wiadomości
    corrected_indices = []  # Lista na indeksy poprawionych bitów
    for codeword in encoded_msg:  # Iteracja po każdym słowie kodowym
        syndrome = syndrome_check(codeword, H)  # Obliczanie syndromu
        corrected_bits = []  # Lista na indeksy poprawionych bitów w tym słowie
        if np.any(syndrome):  # Jeśli syndrom nie jest zerowy, wystąpił błąd
            error_indices = [i for i in range(len(codeword)) if np.array_equal(H[:, i], syndrome)]
            if error_indices:  # Jeśli znaleziono pojedynczy błąd
                codeword[error_indices[0]] ^= 1  # Naprawa błędu przez odwrócenie bitu
                corrected_bits.append(error_indices[0])  # Dodanie indeksu poprawionego bitu
            else:  # Jeśli błąd jest bardziej złożony
                for i in range(len(H[0])):
                    for j in range(i + 1, len(H[0])):
                        if np.array_equal(H[:, i] ^ H[:, j], syndrome):  # Szukanie pary błędów
                            codeword[i] ^= 1
                            codeword[j] ^= 1
                            corrected_bits.extend([i, j])  # Dodanie indeksów poprawionych bitów
                            break
        corrected_msg.append(codeword[:8])  # Dodanie poprawionych bitów danych
        corrected_indices.append(corrected_bits)  # Dodanie indeksów poprawionych bitów dla tego słowa
    return np.array(corrected_msg), corrected_indices  # Zwrócenie poprawionej wiadomości i indeksów

# Funkcja dekodująca poprawioną wiadomość na oryginalny ciąg znaków
def decode(corrected_msg):
    binary_list = [''.join(map(str, bits)) for bits in corrected_msg]
    return bin_to_str(binary_list)

def bin_to_str(binary_list):
    return ''.join(chr(int(b, 2)) for b in binary_list)





message = input("Podaj wiadomość do zakodowania: (jeden znak to 8 bitów) ")
encoded_msg = encode(message, H)
print("Zakodowana wiadomość (w postaci binarnej):", encoded_msg.tolist())

bity_do_zmiany = []

for i in range(len(message)):  # Iterujemy przez każdy znak w wiadomości
    print(f"Zmiana bitów dla znaku: '{message[i]}'")
    bity = []
    for _ in range(2):  # Zmiana dwóch bitów
        bit_to_change = int(input(f"Podaj bit do zmiany dla znaku '{message[i]}': (0-15) "))
        bity.append(bit_to_change)
    bity_do_zmiany.append(bity)

for idx, bity in enumerate(bity_do_zmiany):
    for bit_index in bity:
        encoded_msg[idx][bit_index] ^= 1  # Zmiana bitu w odpowiednim słowie kodowym

for i in range(len(encoded_msg)):
    print(f"Słowo po zmianach bitów dla znaku '{message[i]}':")
    print("Binarne:", encoded_msg[i].tolist())
    print("Zwykłe:", decode([encoded_msg[i]]))

corrected_msg, corrected_indices = correct_errors(encoded_msg, H)

decoded_message = decode(corrected_msg)
print("Wiadomość po dekodowaniu i korekcji błędów:", decoded_message)

for idx, bity in enumerate(bity_do_zmiany):
    print(f"Zmienione bity dla znaku '{message[idx]}': {bity}")

print("Wiadomość odebrana: ", decode(corrected_msg))
