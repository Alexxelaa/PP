import unittest
from io import BytesIO
from unittest.mock import patch
from xml.etree.ElementTree import ElementTree, fromstring
from modules.xml_process import EvalXmlProcessorFactory, RegexXmlProcessorFactory, XmlFileManager


class TestXmlFileManager(unittest.TestCase):

    def test_eval_xml_processor(self):
        input_data = """<?xml version="1.0" encoding="UTF-8"?>
<calculations>
    <expression>5 + 3</expression>
    <expression>3 + 4 * (2 - 1) + 5 / 5</expression>
    <final>20 / 4</final>

    <examples>
    <example>2 + 2</example>
    <example>10 / 2</example>
    <example>5 * (3 + 2)</example>
    <example>8 - 3</example>
    <note>This is not a math example</note>
</examples>
</calculations>"""

        expected_output = """<?xml version="1.0" encoding="UTF-8"?>
<calculations>
    <expression>8</expression>
    <expression>7.0</expression>
    <final>5.0</final>

    <examples>
    <example>4</example>
    <example>5.0</example>
    <example>25</example>
    <example>5</example>
    <note>This is not a math example</note>
</examples>
</calculations>"""

        # Парсим входные данные XML
        root = fromstring(input_data)

        # Создаём менеджер файлов с использованием фабрики для EvalXmlProcessor
        factory = EvalXmlProcessorFactory()
        manager = XmlFileManager(factory)

        # Патчим open, чтобы работать с StringIO
        with patch('builtins.open', return_value=BytesIO(input_data.encode('utf-8'))):
            # Считываем данные из "файла" (BytesIO)
            root = manager.read_xml_file("input.xml")
            # Обрабатываем данные
            processed_root = manager.processor.process(root)
            # Преобразуем обработанный root обратно в строку XML в BytesIO
            output_data = BytesIO()
            ElementTree(processed_root).write(output_data, encoding='utf-8', xml_declaration=True)
            output_data.seek(0)  # Перемещаем указатель в начало BytesIO
            output_data = output_data.read().decode('utf-8')

            # Проверяем, что результат совпадает с ожидаемым, игнорируя лишние пробелы и пустые строки
            self.assertEqual(output_data.strip(), expected_output.strip())

    def test_regex_xml_processor(self):
        input_data = """<?xml version="1.0" encoding="UTF-8"?>
<calculations>
    <expression>5 + 3</expression>
    <expression>3 + 4 * (2 - 1) + 5 / 5</expression>
    <final>20 / 4</final>

    <examples>
    <example>2 + 2</example>
    <example>10 / 2</example>
    <example>5 * (3 + 2)</example>
    <example>8 - 3</example>
    <note>This is not a math example</note>
</examples>
</calculations>"""

        expected_output = """<?xml version="1.0" encoding="UTF-8"?>
<calculations>
    <expression>8</expression>
    <expression>7.0</expression>
    <final>5.0</final>

    <examples>
    <example>4</example>
    <example>5.0</example>
    <example>25</example>
    <example>5</example>
    <note>This is not a math example</note>
</examples>
</calculations>"""

        # Парсим входные данные XML
        root = fromstring(input_data)

        # Создаём менеджер файлов с использованием фабрики для RegexXmlProcessor
        factory = RegexXmlProcessorFactory()
        manager = XmlFileManager(factory)

        # Патчим open, чтобы работать с StringIO
        with patch('builtins.open', return_value=BytesIO(input_data.encode('utf-8'))):
            # Считываем данные из "файла" (BytesIO)
            root = manager.read_xml_file("input.xml")
            # Обрабатываем данные
            processed_root = manager.processor.process(root)
            # Преобразуем обработанный root обратно в строку XML в BytesIO
            output_data = BytesIO()
            ElementTree(processed_root).write(output_data, encoding='utf-8', xml_declaration=True)
            output_data.seek(0)  # Перемещаем указатель в начало BytesIO
            output_data = output_data.read().decode('utf-8')

            # Проверяем, что результат совпадает с ожидаемым, игнорируя лишние пробелы и пустые строки
            self.assertEqual(output_data.strip(), expected_output.strip())


if __name__ == "__main__":
    unittest.main()
