import json
import os

def read_json_file(file):
    try:
        with open(file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            examples = data.get("operations", [])
            answers = []
            for i in examples:
                try:
                    result = eval(i)
                    answers.append(result)
                except (SyntaxError, NameError):
                    continue
            return answers

    except FileNotFoundError:
        print(f"Ошибка: Файл '{file}' не найден.")
    except json.JSONDecodeError:
        print(f"Ошибка: Не удалось декодировать JSON из файла '{file}'.")


def write_answers_to_json_file(answers, output_file):
    try:
        data_to_write = {"answers": [str(answer) for answer in answers]}

        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data_to_write, file, ensure_ascii=False, indent=4)
        print(f"Результаты успешно записаны в '{output_file}'.")

    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")

def read_and_solve_math_problems(input_file):
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


def main():
    input_file = input("Введите название файла: ")  # например, input.json, input.txt and etc.

    if input_file.endswith('.json'):
        base_name = os.path.splitext(input_file)[0]
        output_file = "output.json"
        answers = read_json_file(input_file)
        if answers is not None:
            write_answers_to_json_file(answers, output_file)

    elif input_file.endswith('.txt'):
        read_and_solve_math_problems(input_file)


if __name__ == "__main__":
    main()

