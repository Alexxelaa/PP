from abc import ABC, abstractmethod
import re

# Абстрактный продукт для обработки текста
class TextProcessor(ABC):
    @abstractmethod
    def process(self, text):
        pass

# Конкретный продукт: обработка текста с использованием eval
class EvalTextProcessor(TextProcessor):
    def process(self, text):
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
            if char.isdigit() or char in "+-*/.":  # Собираем символы математического выражения
                temp += char
            else:
                if temp.strip():  # Обработка накопленного выражения
                    if is_math_expression(temp.strip()):
                        result.append(evaluate_expression(temp.strip()))
                    else:
                        result.append(temp)
                    temp = ""
                result.append(char)

        if temp.strip():  # Обработка последнего накопленного выражения
            if is_math_expression(temp.strip()):
                result.append(evaluate_expression(temp.strip()))
            else:
                result.append(temp)

        return ''.join(result).replace(' ,', ',').replace(' .', '.')

# Конкретный продукт: обработка текста с использованием регулярных выражений
class RegexTextProcessor(TextProcessor):
    def process(self, text):
        def evaluate_expression(match):
            expression = match.group(0)
            try:
                result = eval(expression)
                return str(result)
            except Exception:
                return expression

        pattern = r"\b\d+(?:\.\d+)?\s*[+\-*/]\s*\d+(?:\.\d+)?\b"
        return re.sub(pattern, evaluate_expression, text)

# Абстрактная фабрика
class TextProcessorFactory(ABC):
    @abstractmethod
    def create_processor(self):
        pass

# Конкретная фабрика: создание обработчика на основе eval
class EvalTxtProcessorFactory(TextProcessorFactory):
    def create_processor(self):
        return EvalTextProcessor()

# Конкретная фабрика: создание обработчика на основе регулярных выражений
class RegexTxtProcessorFactory(TextProcessorFactory):
    def create_processor(self):
        return RegexTextProcessor()

# Управление текстовыми файлами
class TxtFileManager:
    def __init__(self, processor_factory):
        self.processor = processor_factory.create_processor()

    def read_txt_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def write_to_txt_file(self, file_path, content):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
        except Exception as e:
            print(f"Произошла ошибка при записи в файл: {e}")

    def process_file(self, input_path, output_path):
        text = self.read_txt_file(input_path)
        if text:
            processed_text = self.processor.process(text)
            self.write_to_txt_file(output_path, processed_text)
