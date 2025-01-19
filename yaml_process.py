from abc import ABC, abstractmethod
import yaml
import re

# Абстрактный продукт для обработки YAML
class YamlProcessor(ABC):
    @abstractmethod
    def process(self, data):
        pass

# Конкретный продукт: обработка YAML с использованием eval
class EvalYamlProcessor(YamlProcessor):
    def process(self, data):
        if isinstance(data, dict):
            return {key: self.process(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.process(item) for item in data]
        elif isinstance(data, str):
            try:
                result = eval(data.strip())
                if isinstance(result, (int, float)):
                    return str(result)
                else:
                    return data
            except Exception:
                return data
        else:
            return data

# Конкретный продукт: обработка YAML с использованием регулярных выражений
class RegexYamlProcessor(YamlProcessor):
    def process(self, data):
        math_expression_pattern = r'^[\d+\-*/().\s]+$'

        if isinstance(data, dict):
            return {key: self.process(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.process(item) for item in data]
        elif isinstance(data, str):
            if re.fullmatch(math_expression_pattern, data.strip()):
                try:
                    return str(eval(data.strip()))
                except Exception:
                    return data
            else:
                return data
        else:
            return data

# Абстрактная фабрика
class YamlProcessorFactory(ABC):
    @abstractmethod
    def create_processor(self):
        pass

# Конкретная фабрика: создание обработчика YAML на основе eval
class EvalYamlProcessorFactory(YamlProcessorFactory):
    def create_processor(self):
        return EvalYamlProcessor()

# Конкретная фабрика: создание обработчика YAML на основе регулярных выражений
class RegexYamlProcessorFactory(YamlProcessorFactory):
    def create_processor(self):
        return RegexYamlProcessor()

# Работа с YAML файлами
class YamlFileManager:
    def __init__(self, processor_factory):
        self.processor = processor_factory.create_processor()

    def read_yaml_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                print("YAML-файл успешно прочитан.")
                return data
        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")
        except yaml.YAMLError as e:
            print(f"Ошибка при разборе YAML-файла: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def write_to_yaml(self, file_path, data):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                yaml.dump(data, file, default_flow_style=False, allow_unicode=True)
                print(f"Данные успешно записаны в файл: {file_path}")
        except Exception as e:
            print(f"Произошла ошибка при записи в файл: {e}")

    def process_file(self, input_path, output_path):
        data = self.read_yaml_file(input_path)
        if data is not None:
            processed_data = self.processor.process(data)
            self.write_to_yaml(output_path, processed_data)


