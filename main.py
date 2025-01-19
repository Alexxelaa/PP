'''import zipfile
import os
from modules.txt_process import *
from modules.json_process import *
from modules.xml_process import *
from modules.yaml_process import *


"""функции архивации/разархивация"""
def unzip_file(zip_file_path, output_dir):
    """
    Функция разархивирует ZIP-файл в указанную директорию.

    :param zip_file_path: Путь к ZIP-файлу
    :param output_dir: Директория, в которую нужно разархивировать файл
    """
    try:
        # Проверяем, существует ли выходная директория, если нет — создаем
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Открываем ZIP-файл
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            # Извлекаем все файлы в указанную директорию
            zip_ref.extractall(output_dir)
            print(f"Файлы успешно разархивированы в {output_dir}")
    except FileNotFoundError:
        print(f"Файл {zip_file_path} не найден.")
    except zipfile.BadZipFile:
        print(f"Файл {zip_file_path} не является валидным ZIP-архивом.")
    except Exception:
        print(f"Произошла ошибка: {Exception}")

def zip_file(file_path, zip_file_path):
    """
    Функция архивирует файл в ZIP.

    :param file_path: Путь к файлу, который нужно архивировать
    :param zip_file_path: Путь к конечному ZIP-файлу
    """
    try:
        # Проверяем, существует ли исходный файл
        if not os.path.exists(file_path):
            print(f"Файл {file_path} не найден.")
            return

        # Архивируем файл в ZIP
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_path, os.path.basename(file_path))  # Добавляем файл в архив
            print(f"Файл {file_path} успешно архивирован в {zip_file_path}")

    except Exception:
        print(f"Произошла ошибка при архивировании: {Exception}")



"""функции шифрования/дешифрования"""
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


def main():
    print("Программа для обработки файлов с математическими выражениями")

    # Запрашиваем у пользователя входной файл
    input_file = input("Введите путь к входному файлу: ")
    output_file = input("Введите путь для сохранения выходного файла: ")

    # Запрашиваем действия: архивировать и зашифровать ли файлы
    archive_output = input("Архивировать ли выходной файл? (да/нет): ").strip().lower() == 'да'
    encrypt_input = input("Зашифровать ли входной файл? (да/нет): ").strip().lower() == 'да'

    # Если входной файл является архивом, разархивируем его
    if input_file.endswith('.zip'):
        temp_dir = "temp_unzip"
        unzip_file(input_file, temp_dir)

        # Предполагаем, что в архиве один файл
        files = os.listdir(temp_dir)
        if files:
            input_file = os.path.join(temp_dir, files[0])
        else:
            print("Архив пуст.")
            return

    # Определяем формат входного файла по расширению
    if input_file.endswith('.txt'):
        content = read_txt_file(input_file)
        if content:
            processed_content = process_txt_reg(content)
            write_to_txt_file(output_file, processed_content)

    elif input_file.endswith('.json'):
        data = read_json_file(input_file)
        if data:
            processed_data = process_json_reg(data)
            write_to_json_file(output_file, processed_data)

    elif input_file.endswith('.xml'):
        root = read_xml_file(input_file)
        if root:
            processed_root = process_xml_reg(root)
            write_to_xml_file(processed_root, output_file)

    elif input_file.endswith('.yaml') or input_file.endswith('.yml'):
        data = read_yaml_file(input_file)
        if data:
            processed_data = process_yaml_reg(data)
            write_to_yaml(output_file, processed_data)

    else:
        print("Формат файла не поддерживается.")
        return

    # Архивируем выходной файл, если требуется
    if archive_output:
        zip_file_path = output_file + '.zip'
        zip_file(output_file, zip_file_path)

    # Шифруем входной файл, если требуется
    if encrypt_input:
        encrypt_file_shift(input_file)

    print("Обработка завершена.")

if __name__ == "__main__":
    main()'''

import sys
from modules.txt_process import *
from modules.json_process import *
from modules.xml_process import *
from modules.yaml_process import *

def main():
    print("Добро пожаловать в программу обработки файлов!")
    print("Выберите тип файла для обработки:")
    print("1. TXT")
    print("2. JSON")
    print("3. XML")
    print("4. YAML")

    file_type = input("Введите номер типа файла: ").strip()

    print("Выберите метод обработки:")
    print("1. Использование eval")
    print("2. Использование регулярных выражений")

    method = input("Введите номер метода обработки: ").strip()

    input_file = input("Введите путь к входному файлу: ").strip()
    output_file = input("Введите путь к выходному файлу: ").strip()

    file_manager = None

    # Выбор фабрики на основе типа файла и метода обработки
    if file_type == "1":  # TXT
        factory = EvalTxtProcessorFactory() if method == "1" else RegexTxtProcessorFactory()
        file_manager = TxtFileManager(factory)
    elif file_type == "2":  # JSON
        factory = EvalJsonProcessorFactory() if method == "1" else RegexJsonProcessorFactory()
        file_manager = JsonFileManager(factory)
    elif file_type == "3":  # XML
        factory = EvalXmlProcessorFactory() if method == "1" else RegexXmlProcessorFactory()
        file_manager = XmlFileManager(factory)
    elif file_type == "4":  # YAML
        factory = EvalYamlProcessorFactory() if method == "1" else RegexYamlProcessorFactory()
        file_manager = YamlFileManager(factory)
    else:
        print("Неверный выбор типа файла. Завершение работы программы.")
        sys.exit(1)

    # Обработка файла
    if file_manager:
        try:
            file_manager.process_file(input_file, output_file)
            print(f"Файл успешно обработан и сохранён в: {output_file}")
        except Exception as e:
            print(f"Произошла ошибка при обработке файла: {e}")

if __name__ == "__main__":
    main()
