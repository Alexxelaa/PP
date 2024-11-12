import json

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



data1 = read_json_file('input.json')
print(data1)
