import yaml
import re

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