import math

PARITY_BITS = 8  # Liczba bitów parzystości
WORD_LENGTH = 16  # Długość bloku wiadomości


H = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
]


# Konwersja ciągu tekstowego na listę bitów
def string_to_bits(text):
    return [1 if char == '1' else 0 for char in text]


# Konwersja znaków na binarną reprezentację
def char_to_bits(text):
    bits = []
    for char in text:
        bin_value = ord(char)
        for i in range(8):
            bits.append(bin_value % 2)
            bin_value //= 2
    return bits


# Funkcja do zamiany listy bitów na znak
def bits_to_char(bits):
    char_value = 0
    for i in range(8):
        char_value += bits[i] * 2 ** i
    return chr(char_value)


# Obliczanie parzystości na podstawie macierzy H
def calculate_parity(message, row_number):
    return sum(H[row_number][i] * message[i] for i in range(len(message))) % 2


# Dodanie bitów parzystości do wiadomości
def add_parity_bits(message):
    for i in range(PARITY_BITS):
        message.append(calculate_parity(message, i))


# Kodowanie wiadomości
def encode_message(message):
    encoded = []
    parity_bits = []

    for i in range(len(message)):
        encoded.append(message[i])
        parity_bits.append(message[i])

        if (i + 1) % 8 == 0 and i != 0:
            add_parity_bits(parity_bits)
            encoded.extend(parity_bits[8:8 + PARITY_BITS])
            parity_bits.clear()

    return encoded


# Korekcja błędów w zakodowanej wiadomości
def correct_message(corrupted, error_vector):
    print("Korekcja błędu.")

    for i in range(WORD_LENGTH):
        to_correct = True
        for n in range(PARITY_BITS):
            if error_vector[n] != H[n][i]:
                to_correct = False
                break
        if to_correct:
            corrupted[i] = (corrupted[i] + 1) % 2


# Weryfikacja poprawności danych i korekcja błędów
def verify_and_correct(message, length):
    is_valid = True
    if len(message) != length:
        print(f"Błąd: Niezgodna ilość bitów ({len(message)}).")
        return

    error_vector = []
    for i in range(PARITY_BITS):
        parity = calculate_parity(message, i)
        error_vector.append(parity)
        if parity == 1:
            is_valid = False

    if is_valid:
        print("Brak błędów.")
    else:
        correct_message(message, error_vector)


# Główna funkcja
def main():
    # Wczytywanie wiadomości do zakodowania
    with open('input.txt', 'r') as file_in:
        message_text = file_in.read().strip()

    # Konwersja tekstu na bity
    message = char_to_bits(message_text)
    print(f'Wiadomość ("{message_text}") binarnie:')
    for i, bit in enumerate(message):
        print(bit, end=' ')
        if (i + 1) % 8 == 0:
            print()

    # Kodowanie wiadomości
    encoded_message = encode_message(message)
    print("\nZakodowana wiadomość:")
    for i, bit in enumerate(encoded_message):
        print(bit, end=' ')
        if (i + 1) % 16 == 0:
            print()

    # Zapis zakodowanej wiadomości do pliku
    with open("encoded_data.txt", "w") as file_out:
        for bit in encoded_message:
            file_out.write(str(bit))

    # Użytkownik może wprowadzić zmiany w pliku
    input("\nMozna przeprowadzić zmiane")

    # Wczytanie zmienionej wiadomości
    with open("encoded_data.txt", "r") as file_in:
        corrupted_message_text = file_in.read().strip()

    print("\n")
    corrupted_message = string_to_bits(corrupted_message_text)
    print("Po zmianie:")
    for i, bit in enumerate(corrupted_message):
        print(bit, end=' ')
        if (i + 1) % 16 == 0:
            print()
    print("\n")
    # Przygotowanie do weryfikacji i korekcji
    size = len(message_text)
    multi_vector = [[] for _ in range(size)]

    corrected_message = []
    for i in range(0, len(corrupted_message), 16):
        multi_vector[i // 16] = corrupted_message[i:i + 16]

    for vector in multi_vector:
        verify_and_correct(vector, len(encoded_message) // size)
        corrected_message.extend(vector)

    # Dekodowanie poprawionej wiadomości
    decoded_message = ''.join([bits_to_char(vector) for vector in multi_vector])

    # Zapisanie wiadomości do pliku
    with open("received_data.txt", "w") as file_out:
        file_out.write(decoded_message)

    print(f"\nWiadomość odebrana: {decoded_message}")


if __name__ == "__main__":
    main()
