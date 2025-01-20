import unittest
import json
from io import StringIO
from unittest.mock import patch
from modules.json_process import EvalJsonProcessorFactory, RegexJsonProcessorFactory

class TestJsonProcessor(unittest.TestCase):
    # Тестирование с использованием eval
    @patch('builtins.open', return_value=StringIO('{"operations": ["2 * 2", "3 * 3", "4 * 4", "5 * 5", "3 + a", "6 * 6"], "operations2": ["1+1", "2+2", "3+3"], "ewfewf": ["1+ 1000000"], "tertf": ["111 + 324"]}'))
    def test_eval_json_processor(self, mock_open):
        # Создаем фабрику обработчиков с использованием eval
        factory = EvalJsonProcessorFactory()
        processor = factory.create_processor()

        # Пример данных JSON
        input_data = {
            "operations": [
                "2 * 2", "3 * 3", "4 * 4", "5 * 5", "3 + a", "6 * 6"
            ],
            "operations2": [
                "1+1", "2+2", "3+3"
            ],
            "ewfewf": [
                "1+ 1000000"
            ],
            "tertf": [
                "111 + 324"
            ]
        }

        # Ожидаемый результат после обработки
        expected_result = {
            "operations": ["4", "9", "16", "25", "3 + a", "36"],
            "operations2": ["2", "4", "6"],
            "ewfewf": ["1000001"],
            "tertf": ["435"]
        }

        # Процесс обработки с использованием eval
        result = processor.process(input_data)

        # Проверка на корректность обработки
        self.assertEqual(result, expected_result)

    # Тестирование с использованием регулярных выражений
    @patch('builtins.open', return_value=StringIO('{"operations": ["2 * 2", "3 * 3", "4 * 4", "5 * 5", "3 + a", "6 * 6"], "operations2": ["1+1", "2+2", "3+3"], "ewfewf": ["1+ 1000000"], "tertf": ["111 + 324"]}'))
    def test_regex_json_processor(self, mock_open):
        # Создаем фабрику обработчиков с использованием регулярных выражений
        factory = RegexJsonProcessorFactory()
        processor = factory.create_processor()

        # Пример данных JSON
        input_data = {
            "operations": [
                "2 * 2", "3 * 3", "4 * 4", "5 * 5", "3 + a", "6 * 6"
            ],
            "operations2": [
                "1+1", "2+2", "3+3"
            ],
            "ewfewf": [
                "1+ 1000000"
            ],
            "tertf": [
                "111 + 324"
            ]
        }

        # Ожидаемый результат после обработки
        expected_result = {
            "operations": ["4", "9", "16", "25", "3 + a", "36"],
            "operations2": ["2", "4", "6"],
            "ewfewf": ["1000001"],
            "tertf": ["435"]
        }

        # Процесс обработки с использованием регулярных выражений
        result = processor.process(input_data)

        # Проверка на корректность обработки
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
