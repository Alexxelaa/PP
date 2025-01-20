import unittest
import yaml
from io import StringIO
from unittest.mock import patch
from modules.yaml_process import EvalYamlProcessorFactory, RegexYamlProcessorFactory, YamlFileManager


class TestYamlFileManager(unittest.TestCase):

    def test_eval_yaml_processor(self):
        input_data = {
            'operations': [
                "2 + 3",
                "10 * 5",
                "100 / 4",
                "15 - 7",
                "3 ** 2"
            ],
            'operations2': [
                "5 + 5",
                "10 + 10",
                "100 + 100"
            ],
            'govno': [
                "2+2+2+2+2"
            ]
        }

        expected_output = {
            'operations': [
                "5",
                "50",
                "25.0",
                "8",
                "9"
            ],
            'operations2': [
                "10",
                "20",
                "200"
            ],
            'govno': [
                "10"
            ]
        }

        # Создаём менеджер файлов с использованием фабрики для EvalYamlProcessor
        factory = EvalYamlProcessorFactory()
        manager = YamlFileManager(factory)

        # Патчим open, чтобы работать с StringIO
        with patch('builtins.open', return_value=StringIO(yaml.dump(input_data))):
            # Считываем данные из "файла" (StringIO)
            data = manager.read_yaml_file("input.yaml")
            # Обрабатываем данные
            processed_data = manager.processor.process(data)
            # Проверяем, что результат совпадает с ожидаемым
            self.assertEqual(processed_data, expected_output)

    def test_regex_yaml_processor(self):
        input_data = {
            'operations': [
                "2 + 3",
                "10 * 5",
                "100 / 4",
                "15 - 7",
                "3 ** 2"
            ],
            'operations2': [
                "5 + 5",
                "10 + 10",
                "100 + 100"
            ],
            'govno': [
                "2+2+2+2+2"
            ]
        }

        expected_output = {
            'operations': [
                "5",
                "50",
                "25.0",
                "8",
                "9"
            ],
            'operations2': [
                "10",
                "20",
                "200"
            ],
            'govno': [
                "10"
            ]
        }

        # Создаём менеджер файлов с использованием фабрики для RegexYamlProcessor
        factory = RegexYamlProcessorFactory()
        manager = YamlFileManager(factory)

        # Патчим open, чтобы работать с StringIO
        with patch('builtins.open', return_value=StringIO(yaml.dump(input_data))):
            # Считываем данные из "файла" (StringIO)
            data = manager.read_yaml_file("input.yaml")
            # Обрабатываем данные
            processed_data = manager.processor.process(data)
            # Проверяем, что результат совпадает с ожидаемым
            self.assertEqual(processed_data, expected_output)


if __name__ == "__main__":
    unittest.main()
