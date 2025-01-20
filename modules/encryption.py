"""Функции шифрования/дешифрования"""
def encrypt_file_shift(file_path):
    """
    Функция шифрует содержимое файла сдвигом символов на 1 в таблице ASCII.

    :param file_path: Путь к файлу, который нужно зашифровать
    """
    try:
        # Открываем исходный файл для чтения
        with open(file_path, 'r', encoding='utf-8') as file:
            file_data = file.read()

        # Применяем сдвиг на 1 к каждому символу в содержимом файле
        encrypted_data = ''.join([chr(ord(char) + 1) for char in file_data])

        # Записываем зашифрованные данные в новый файл
        encrypted_file_path = file_path + ".encrypted"
        with open(encrypted_file_path, 'w', encoding='utf-8') as encrypted_file:
            encrypted_file.write(encrypted_data)

        print(f"Файл был зашифрован и сохранен как {encrypted_file_path}")

    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def decrypt_file_shift(file_path):
    """
    Функция расшифровывает содержимое файла, сдвинув символы на 1 в таблице ASCII обратно.

    :param file_path: Путь к зашифрованному файлу
    """
    try:
        # Открываем зашифрованный файл для чтения
        with open(file_path, 'r', encoding='utf-8') as file:
            encrypted_data = file.read()

        # Применяем обратный сдвиг на 1 к каждому символу в содержимом файле
        decrypted_data = ''.join([chr(ord(char) - 1) for char in encrypted_data])

        # Записываем расшифрованные данные в новый файл
        decrypted_file_path = file_path.replace(".encrypted", ".decrypted")
        with open(decrypted_file_path, 'w', encoding='utf-8') as decrypted_file:
            decrypted_file.write(decrypted_data)

        print(f"Файл был расшифрован и сохранен как {decrypted_file_path}")

    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except Exception:
        print(f"Произошла ошибка: {Exception}")
