from abc import ABC, abstractmethod
import json
import re

# Абстрактный продукт для обработки JSON
class JsonProcessor(ABC):
    @abstractmethod
    def process(self, input_dict):
        pass

# Конкретный продукт: обработка JSON с использованием eval
class EvalJsonProcessor(JsonProcessor):
    def process(self, input_dict):
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

# Конкретный продукт: обработка JSON с использованием регулярных выражений
class RegexJsonProcessor(JsonProcessor):
    def process(self, input_dict):
        def is_math_expression(expr):
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

# Абстрактная фабрика
class JsonProcessorFactory(ABC):
    @abstractmethod
    def create_processor(self):
        pass

# Конкретная фабрика: создание обработчика JSON на основе eval
class EvalJsonProcessorFactory(JsonProcessorFactory):
    def create_processor(self):
        return EvalJsonProcessor()

# Конкретная фабрика: создание обработчика JSON на основе регулярных выражений
class RegexJsonProcessorFactory(JsonProcessorFactory):
    def create_processor(self):
        return RegexJsonProcessor()

# Работа с JSON файлами
class JsonFileManager:
    def __init__(self, processor_factory):
        self.processor = processor_factory.create_processor()

    def read_json_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")
        except json.JSONDecodeError as e:
            print(f"Ошибка при чтении JSON-файла: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def write_to_json_file(self, file_path, data):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except TypeError as e:
            print(f"Ошибка: данные не могут быть переведены в JSON. {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def process_file(self, input_path, output_path):
        data = self.read_json_file(input_path)
        if data:
            processed_data = self.processor.process(data)
            self.write_to_json_file(output_path, processed_data)


