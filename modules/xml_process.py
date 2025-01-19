from abc import ABC, abstractmethod
from xml.etree.ElementTree import ElementTree, parse, ParseError
import re

# Абстрактный продукт для обработки XML
class XmlProcessor(ABC):
    @abstractmethod
    def process(self, root):
        pass

# Конкретный продукт: обработка XML с использованием eval
class EvalXmlProcessor(XmlProcessor):
    def process(self, root):
        if root is None:
            return None

        for element in root.iter():
            if element.text:
                text = element.text.strip()
                try:
                    result = eval(text)  # Используем eval для вычисления математических примеров
                    element.text = str(result)  # Заменяем текст тега на результат
                except Exception:
                    pass  # Если текст не является математическим выражением, пропускаем

        return root

# Конкретный продукт: обработка XML с использованием регулярных выражений
class RegexXmlProcessor(XmlProcessor):
    def process(self, root):
        if root is None:
            return None

        # Регулярное выражение для поиска математических выражений
        math_expression_pattern = r'^[\d+\-*/().\s]+$'

        for element in root.iter():
            if element.text:
                text = element.text.strip()
                if re.fullmatch(math_expression_pattern, text):
                    try:
                        result = eval(text)
                        element.text = str(result)  # Заменяем текст тега на результат
                    except Exception:
                        pass

        return root

# Абстрактная фабрика
class XmlProcessorFactory(ABC):
    @abstractmethod
    def create_processor(self):
        pass

# Конкретная фабрика: создание обработчика XML на основе eval
class EvalXmlProcessorFactory(XmlProcessorFactory):
    def create_processor(self):
        return EvalXmlProcessor()

# Конкретная фабрика: создание обработчика XML на основе регулярных выражений
class RegexXmlProcessorFactory(XmlProcessorFactory):
    def create_processor(self):
        return RegexXmlProcessor()

# Работа с XML файлами
class XmlFileManager:
    def __init__(self, processor_factory):
        self.processor = processor_factory.create_processor()

    def read_xml_file(self, file_path):
        try:
            tree = parse(file_path)
            root = tree.getroot()
            print(f"XML-файл успешно прочитан: {file_path}")
            return root
        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")
            return None
        except ParseError as e:
            print(f"Ошибка при разборе XML-файла: {e}")
            return None

    def write_to_xml_file(self, root, output_file_path):
        if root is None:
            print("Нет данных для записи.")
            return

        tree = ElementTree(root)
        try:
            tree.write(output_file_path, encoding='utf-8', xml_declaration=True)
            print(f"Результаты записаны в файл: {output_file_path}")
        except Exception as e:
            print(f"Ошибка при записи файла: {e}")

    def process_file(self, input_path, output_path):
        root = self.read_xml_file(input_path)
        if root:
            processed_root = self.processor.process(root)
            self.write_to_xml_file(processed_root, output_path)



