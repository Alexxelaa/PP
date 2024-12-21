import os
import json
import yaml
import ast
from xml.etree.ElementTree import *


def process_json_file_eval(input_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        examples = data.get("operations", [])
        answers = []

        for expr in examples:
            try:
                result = eval(compile(ast.parse(expr, mode='eval'), '', mode='eval'))
                answers.append(result)
            except Exception as e:
                print(f"Ошибка при обработке выражения '{expr}': {e}")

        data_to_write = {"answers": [str(answer) for answer in answers]}
        with open("output.json", 'w', encoding='utf-8') as file:
            json.dump(data_to_write, file, ensure_ascii=False, indent=4)

        print(f"Результаты успешно записаны в output.json.")

    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_file}' не найден.")
    except json.JSONDecodeError:
        print(f"Ошибка: Некорректный JSON в файле '{input_file}'.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def process_txt_files_eval(input_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        answers = []
        for line in lines:
            line = line.strip()
            if line:
                try:
                    result = eval(line)
                    answers.append(str(result))
                except (SyntaxError, NameError):
                    continue

        with open("output.txt", 'w', encoding='utf-8') as file:
            for answer in answers:
                file.write(answer + '\n')

        print(f"Решения успешно записаны в output.txt.")

    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_file}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def process_xml_file_eval(input_file):
    try:
        tree = parse(input_file)
        root = tree.getroot()

        for elem in root.iter():
            if elem.text:
                expression = elem.text.strip()
                try:
                    result = eval(compile(ast.parse(expression, mode='eval'), '', mode='eval'))
                    elem.text = str(result)
                except Exception:
                    continue

        tree.write("output.xml", encoding="utf-8", xml_declaration=True)
        print(f"Результаты успешно записаны в output.xml.")

    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_file}' не найден.")
    except ParseError:
        print(f"Ошибка: Некорректный XML в файле '{input_file}'.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def process_yaml_file_eval(input_file):
    def evaluate_expressions(data):
        if isinstance(data, dict):
            for key, value in data.items():
                evaluate_expressions(value)
        elif isinstance(data, list):
            for i in range(len(data)):
                if isinstance(data[i], str):
                    try:
                        result = eval(data[i])
                        data[i] = result
                    except Exception:
                        pass
                else:
                    evaluate_expressions(data[i])

    with open(input_file, 'r') as file:
        data = yaml.safe_load(file)

    evaluate_expressions(data)

    with open("output.yaml", 'w') as file:
        yaml.dump(data, file)


def main():
    input_file = input("Введите название файла: ")

    if input_file.endswith('.json'):
        process_json_file_eval(input_file)
    elif input_file.endswith('.txt'):
        process_txt_files_eval(input_file)
    elif input_file.endswith('.xml'):
        process_xml_file_eval(input_file)
    elif input_file.endswith('.yaml'):
        process_yaml_file_eval(input_file)

if __name__ == "__main__":
    main()
