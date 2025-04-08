import numpy as np

H = [
    [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]
]


def str_to_bin(message):
    # Zamienia każdy znak na 8-bitową reprezentację binarną
    return [format(ord(c), '08b') for c in message]


def bin_to_str(binary_list):
    # Zamienia listę binarnych ciągów na tekst
    return ''.join(chr(int(b, 2)) for b in binary_list)


def encode(message, H):
    H = np.array(H)
    encoded_msg = []
    for char in str_to_bin(message):
        data_bits = np.array([int(b) for b in char])
        parity_bits = (H[:, :8] @ data_bits) % 2  # Obliczanie bitów parzystości
        codeword = np.concatenate((data_bits, parity_bits))  # Łączenie bitów danych i parzystości
        encoded_msg.append(codeword)
    return np.array(encoded_msg)



def syndrome_check(codeword, H):
    H = np.array(H)
    syndrome = (H @ codeword) % 2  # Obliczanie syndromu (H * codeword mod 2)
    return syndrome


def correct_errors(encoded_msg, H):
    H = np.array(H)
    corrected_msg = []
    corrected_indices = []

    for codeword_str in encoded_msg:
        # Zamieniamy ciąg binarny na tablicę liczb (0, 1), co daje 16 bitów w sumie
        codeword = np.array([int(b) for b in codeword_str])

        syndrome = syndrome_check(codeword, H)
        corrected_bits = []

        # Jeśli syndrom nie jest zerowy, wystąpił błąd
        if np.any(syndrome):
            error_indices = [i for i in range(len(codeword)) if np.array_equal(H[:, i], syndrome)]
            if error_indices:
                codeword[error_indices[0]] ^= 1
                corrected_bits.append(error_indices[0])
            else:
                # Sprawdzamy, czy błąd jest bardziej złożony
                for i in range(len(H[0])):
                    for j in range(i + 1, len(H[0])):
                        if np.array_equal(H[:, i] ^ H[:, j], syndrome):
                            codeword[i] ^= 1
                            codeword[j] ^= 1
                            corrected_bits.extend([i, j])
                            break

        # Dodajemy tylko 8 pierwszych bitów (dane) do poprawionego słowa
        corrected_msg.append(codeword[:8])
        corrected_indices.append(corrected_bits)

    return np.array(corrected_msg), corrected_indices


def decode(corrected_msg):
    binary_list = [''.join(map(str, bits)) for bits in corrected_msg]
    return bin_to_str(binary_list)


def read_message_from_file(file_path):
    with open(file_path, 'r') as file:
        message = file.read().strip()  # Usuwa białe znaki na końcu
    # Sprawdzamy, czy wiadomość jest już w postaci binarnej, czy tekstowej
    if all(len(x) == 8 for x in message.splitlines()):  # Jeżeli każda linia ma 8 bitów
        return message.splitlines()  # Zwróć listę ciągów binarnych
    else:
        return message  # W przeciwnym przypadku zwróć tekst


def write_encoded_to_file(encoded_msg, file_path):
    with open(file_path, 'w') as file:
        for codeword in encoded_msg:
            file.write(''.join(map(str, codeword)) + '\n')


def write_decoded_to_file(decoded_msg, file_path):
    with open(file_path, 'w') as file:
        file.write(decoded_msg)

def main():
    input_file_path = 'message.txt'
    message = read_message_from_file(input_file_path)
    print(f"Wiadomość do zakodowania: {message}")

    encoded_msg = encode(message, H)
    encoded_file_path = 'encoded_message.txt'
    write_encoded_to_file(encoded_msg, encoded_file_path)
    input("Teraz jest czas na podmiane bitów w pliku encoded_message.txt, naciśnij Enter, aby kontynuować...")

    # Wczytujemy zmodyfikowaną zakodowaną wiadomość
    encoded_msg = read_message_from_file(encoded_file_path).splitlines()
    encoded_msg = decode(encoded_msg)
    print("Wynik zmian: ",encoded_msg)
    encoded_msg = read_message_from_file(encoded_file_path).splitlines()

    # Sprawdzanie i poprawianie błędów
    corrected_msg, corrected_indices = correct_errors(encoded_msg, H)

    # Dekodowanie poprawionej wiadomości
    decoded_message = decode(corrected_msg)
    print("Wiadomość po dekodowaniu i korekcji błędów:", decoded_message)

    # Zapisz poprawioną wiadomość
    decoded_file_path = 'decoded_message.txt'
    write_decoded_to_file(decoded_message, decoded_file_path)



if __name__ == '__main__':
    main()
