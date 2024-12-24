from xml.etree.ElementTree import *
import re

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
