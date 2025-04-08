"""
zad 1 - opracowanie programu do korekcji jednego błędu bitowego w 8 bitowym słowie

Wykrycie i korekcja 1 błędu wymaga dodania 4 bitów parzystości do 8 bitowego słowa
bity parzystości dodawane są na indeksach odpowiadających potęg 2
1,2,4,8 - indeksy to 0,1,3,7

Bity wiadomości
d0,d1,d2,d3,d4,d5,d6,d7
    dodajemy bity parzystości
p0,p1,d1,p2,d2,d3,d4,p3,d5,d6,d7

Każdy bit parzystości kontroluje indeksy, których rozkład binarnie ma 1 na odpowiednim miejscu patrząc od końca (najmłodszy bit)
np:
1   = 0001 ✅
2   = 0010 ❌
3   = 0011 ✅
4   = 0100 ❌
5   = 0101 ✅
6   = 0110 ❌
7   = 0111 ✅
8   = 1000 ❌
9   = 1001 ✅
10  = 1010 ❌
11  = 1011 ✅
12  = 1100 ❌
analogicznie kolejne
Każdy bit obliczany w taki sposób że wszystkie te wartości są xorowane
P1 = XOR(wartości na tych pozycjach) - P8 = D5 ⊕ D6 ⊕ D7 ⊕ D8

Sprawdzanie błędu:
Obliczany ponownie xory dla każdego bitu parzystości
porównujemy je z poprzednimi - jesli są takie same to wynik jest 0, jeśli różne to 1
np. (policzone XOR-y)
    P1 = 1
    P2 = 1
    P4 = 0
    P8 = 0

Syndrom = 0b0011 = 3 - wskazuje pozycje na której jest błąd - przy używaniu 0base trzeba odjąć 1

"""


def calculate_parity_bits(data_bits):
    # data_bits to lista 8 bitów (np. [1, 0, 1, 0, 1, 1, 0, 0])
    hamming = [0] * 12
    j = 0
    for i in range(12):
        # Pozycje 1, 2, 4, 8 (indeksy 0, 1, 3, 7) to bity parzystości
        if i in [0, 1, 3, 7]:
            continue
        hamming[i] = data_bits[j]
        j += 1

    # Obliczanie bitów parzystości
    hamming[0] = hamming[2] ^ hamming[4] ^ hamming[6] ^ hamming[8] ^ hamming[10]
    hamming[1] = hamming[2] ^ hamming[5] ^ hamming[6] ^ hamming[9] ^ hamming[10]
    hamming[3] = hamming[4] ^ hamming[5] ^ hamming[6] ^ hamming[11]
    hamming[7] = hamming[8] ^ hamming[9] ^ hamming[10] ^ hamming[11]

    return hamming


def detect_and_correct(hamming):
    # Obliczanie pozycji błędu
    p1 = hamming[0] ^ hamming[2] ^ hamming[4] ^ hamming[6] ^ hamming[8] ^ hamming[10]
    p2 = hamming[1] ^ hamming[2] ^ hamming[5] ^ hamming[6] ^ hamming[9] ^ hamming[10]
    p3 = hamming[3] ^ hamming[4] ^ hamming[5] ^ hamming[6] ^ hamming[11]
    p4 = hamming[7] ^ hamming[8] ^ hamming[9] ^ hamming[10] ^ hamming[11]

    error_position = p4 << 3 | p3 << 2 | p2 << 1 | p1

    if error_position != 0:
        print(f"Błąd wykryty na indeksie: {error_position -1}")
        hamming[error_position - 1] ^= 1  # Korekcja błędu
    else:
        print("Brak błędów.")

    # Odczyt danych (pomijamy bity parzystości)
    data = []
    for i in range(12):
        if i not in [0, 1, 3, 7]:
            data.append(hamming[i])

    return data


def char_to_bits(char):
    bits = format(ord(char), '08b')
    return [int(bit) for bit in bits]



# komunikacja z użytkownikiem
#
text = input("Podaj tekst do zakodowania - 1 znak to 8 bitów, czyli jedno słowo: ")
char_table = []
for char in text:
    char_table.append(char)
print(char_table)
for char in char_table:
    print("Znak: ", char)
    bit_list = char_to_bits(char)
    print("Binarnie: ", bit_list)
    bit_list = calculate_parity_bits(bit_list)
    print("Zakodowane: ", bit_list)
    change_bit = int(input("Podaj indeks do symulacji błędu: (0-11 , wpisanie 12 pominie błąd): "))
    if change_bit == 12:
        print("Pominięcie wpisania błedu")
    elif change_bit < 0 or change_bit > 12:
        print("Zły indeks")
    else:
        bit_list[change_bit] ^= 1
        print("Z błędem: ", bit_list)
    corrected_data = detect_and_correct(bit_list)
    print("Wiadomość bez błędów: ", corrected_data)





