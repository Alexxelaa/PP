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