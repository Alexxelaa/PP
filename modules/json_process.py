import json
import re

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