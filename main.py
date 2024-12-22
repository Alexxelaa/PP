import json
import yaml
from xml.etree.ElementTree import *
import zipfile
import os
import re


def read_txt_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except Exception:
        print(f"Произошла ошибка: {Exception}")

def process_txt_eval(text):
    """
    Находит в тексте математические выражения, решает их и возвращает текст с результатами.
    Поддерживаемые операции: + - * /.

    :param text: Строка, содержащая математические выражения
    :return: строка с подставленными результатами вычислений
    """
    def is_math_expression(expr):
        try:
            evaluated = eval(expr)
            return isinstance(evaluated, (int, float))
        except Exception:
            return False

    def evaluate_expression(expr):
        try:
            return str(eval(expr))
        except Exception:
            return expr

    result = []
    temp = ""

    for char in text:
        if char.isdigit() or char in "+-*/.":
            temp += char
        else:
            if temp.strip():
                if is_math_expression(temp.strip()):
                    result.append(evaluate_expression(temp.strip()))
                else:
                    result.append(temp)
                temp = ""
            result.append(char)

    if temp.strip():
        if is_math_expression(temp.strip()):
            result.append(evaluate_expression(temp.strip()))
        else:
            result.append(temp)

    return ''.join(result).replace(' ,', ',').replace(' .', '.')

def process_txt_reg(text):
    """
    Находит в тексте математические выражения, решает их и возвращает текст с результатами.
    Поддерживаемые операции: + - * /.

    :param text: Строка, содержащая математические выражения
    :return: строка с подставленными результатами вычислений
    """
    def evaluate_expression(match):
        # Извлекаем найденное выражение
        expression = match.group(0)
        try:
            # Вычисляем значение выражения
            result = eval(expression)
            return str(result)
        except Exception as e:
            # В случае ошибки оставляем выражение без изменений
            return expression

    # Регулярное выражение для поиска математических примеров
    pattern = r"\b\d+(?:\.\d+)?\s*[+\-*/]\s*\d+(?:\.\d+)?\b"

    # Заменяем все найденные примеры их решениями
    return re.sub(pattern, evaluate_expression, text)

def write_to_txt_file(file_path, content):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception:
        print(f"Произошла ошибка при записи в файл: {Exception}")



def read_json_file(file_path):
    """
        Функция считывает JSON-файл и возвращает его содержимое.

        :param file_path: Путь к JSON-файлу
        :return: Данные, прочитанные из файла (словарь)
        """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except json.JSONDecodeError:
        print(f"Ошибка при чтении JSON-файла: {json.JSONDecodeError}")
    except Exception:
        print(f"Произошла ошибка: {Exception}")

def process_json_eval(input_dict):
    """
    Пробегает по всем значениям словаря, проверяет, являются ли они математическими примерами,
    решает их и возвращает новый словарь с ответами.

    :param input_dict: Словарь, где каждому ключу присвоен массив строк
    :return: новый словарь с решёнными примерами
    """
    def is_math_expression(expr):
        try:
            evaluated = eval(expr)
            return isinstance(evaluated, (int, float))
        except Exception:
            return False

    def evaluate_expression(expr):
        try:
            return str(eval(expr))
        except Exception:
            return expr

    output_dict = {}

    for key, values in input_dict.items():
        solved_values = []
        for value in values:
            if is_math_expression(value):
                solved_values.append(evaluate_expression(value))
            else:
                solved_values.append(value)
        output_dict[key] = solved_values

    return output_dict

def process_json_reg(input_dict):
    """
    Пробегает по всем значениям словаря, проверяет, являются ли они математическими примерами с использованием регулярных выражений,
    решает их и возвращает новый словарь с ответами.

    :param input_dict: Словарь, где каждому ключу присвоен массив строк
    :return: новый словарь с решёнными примерами
    """
    def is_math_expression(expr):
        # Проверяем, является ли строка математическим выражением
        pattern = r"^\s*\d+(?:\.\d+)?\s*[+\-*/]\s*\d+(?:\.\d+)?\s*$"
        return re.match(pattern, expr) is not None

    def evaluate_expression(expr):
        try:
            return str(eval(expr))
        except Exception:
            return expr

    output_dict = {}

    for key, values in input_dict.items():
        solved_values = []
        for value in values:
            if is_math_expression(value):
                solved_values.append(evaluate_expression(value))
            else:
                solved_values.append(value)
        output_dict[key] = solved_values

    return output_dict

def write_to_json_file(file_path, data):
    """
        Функция записывает словарь в JSON-файл.

        :param file_path: Путь к JSON-файлу
        :param data: Словарь для записи
        """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    except TypeError:
        print(f"Ошибка: данные не могут быть переведены в JSON. {TypeError}")
    except Exception:
        print(f"Произошла ошибка: {Exception}")



def read_xml_file(file_path):
    """
    Функция считывает XML-файл и возвращает корневой элемент.

    :param file_path: Путь к XML-файлу
    :return: Корневой элемент XML-документа
    """
    try:
        tree = parse(file_path)
        root = tree.getroot()
        print(f"XML-файл успешно прочитан: {file_path}")
        return root
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return None
    except ParseError:
        print(f"Ошибка при разборе XML-файла: {ParseError}")
        return None

def process_xml_eval(root):
    """
    Функция находит математические примеры в тегах и решает их.

    :param root: Корневой элемент XML-документа
    :return: Обновленный корневой элемент с решениями
    """
    if root is None:
        return None

    for element in root.iter():
        if element.text:
            text = element.text.strip()
            try:
                # Попытка вычислить значение выражения
                result = eval(text)  # Используем eval для вычисления математических примеров
                element.text = str(result)  # Заменяем текст тега на результат
            except Exception:
                pass  # Если текст не является математическим выражением, пропускаем

    return root

def process_xml_reg(root):
    """
    Функция находит математические примеры в тегах с использованием регулярных выражений
    и решает их.

    :param root: Корневой элемент XML-документа
    :return: Обновленный корневой элемент с решениями
    """
    if root is None:
        return None

    # Регулярное выражение для поиска математических выражений
    math_expression_pattern = r'^[\d+\-*/().\s]+$'

    for element in root.iter():
        if element.text:
            text = element.text.strip()
            # Проверяем, соответствует ли текст математическому выражению
            if re.fullmatch(math_expression_pattern, text):
                try:
                    result = eval(text)
                    element.text = str(result)  # Заменяем текст тега на результат
                except Exception:
                    pass

    return root

def write_to_xml_file(root, output_file_path):
    """
    Функция записывает обновленный XML в выходной файл.

    :param root: Корневой элемент XML-документа
    :param output_file_path: Путь к выходному файлу
    """
    if root is None:
        print("Нет данных для записи.")
        return

    tree = ElementTree(root)
    try:
        tree.write(output_file_path, encoding='utf-8', xml_declaration=True)
        print(f"Результаты записаны в файл: {output_file_path}")
    except Exception:
        print(f"Ошибка при записи файла: {Exception}")



def read_yaml_file(file_path):
    """
    Функция считывает YAML-файл и возвращает его содержимое.

    :param file_path: Путь к YAML-файлу
    :return: Данные, считанные из YAML-файла
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            print("YAML-файл успешно прочитан.")
            return data
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except yaml.YAMLError:
        print(f"Ошибка при разборе YAML-файла: {yaml.YAMLError}")
    except Exception:
        print(f"Произошла ошибка: {Exception}")
        return None

def process_yaml_eval(data):
    """
    Рекурсивная функция, которая обходит словарь, пытается вычислить все строки
    как математические выражения с использованием eval.

    :param data: Словарь с данными
    :return: Словарь с вычисленными математическими выражениями
    """
    if isinstance(data, dict):
        # Если текущий объект — словарь, обходим его пары ключ-значение
        return {key: process_yaml_eval(value) for key, value in data.items()}
    elif isinstance(data, list):
        # Если текущий объект — список, обходим его элементы
        return [process_yaml_eval(item) for item in data]
    elif isinstance(data, str):
        try:
            # Попытка вычислить строку как математическое выражение
            result = eval(data.strip())
            if isinstance(result, (int, float)):
                return str(result)
            else:
                return data
        except Exception:
            return data
    else:
        return data

def process_yaml_reg(data):
    """
    Рекурсивная функция, которая обходит словарь, ищет математические выражения
    в значениях и заменяет их на результаты вычислений, используя регулярное выражение.

    :param data: Словарь с данными
    :return: Словарь с вычисленными математическими выражениями
    """
    # Регулярное выражение для проверки математических выражений
    math_expression_pattern = r'^[\d+\-*/().\s]+$'

    if isinstance(data, dict):
        # Если текущий объект — словарь, обходим его пары ключ-значение
        return {key: process_yaml_reg(value) for key, value in data.items()}
    elif isinstance(data, list):
        # Если текущий объект — список, обходим его элементы
        return [process_yaml_reg(item) for item in data]
    elif isinstance(data, str):
        # Если текущий объект — строка, проверяем, является ли она математическим выражением
        if re.fullmatch(math_expression_pattern, data.strip()):
            try:
                return str(eval(data.strip()))
            except Exception:
                return data
        else:
            return data
    else:
        return data

def write_to_yaml(file_path, data):
    """
    Функция записывает данные из словаря в YAML файл.

    :param file_path: Путь к YAML-файлу
    :param data: Словарь, который нужно записать в файл
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, default_flow_style=False, allow_unicode=True)
            print(f"Данные успешно записаны в файл: {file_path}")
    except Exception:
        print(f"Произошла ошибка при записи в файл: {Exception}")


'''функции архивации/разархивация'''
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
    main()









