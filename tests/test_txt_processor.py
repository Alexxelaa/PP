import unittest
from io import StringIO
from unittest.mock import patch

from modules.txt_process import EvalTxtProcessorFactory, RegexTxtProcessorFactory, TxtFileManager

class TestTxtFileManager(unittest.TestCase):

    def test_eval_txt_processor(self):
        # Условие для обработки текста
        input_text = "Вычислите 2 + 2, 5 * 6 и 8 / 4. Не трогайте 3 + x."
        expected_output = "Вычислите4,30и2.0Не трогайте 3 + x."

        # Создаём менеджер файлов с использованием фабрики для EvalTextProcessor
        factory = EvalTxtProcessorFactory()
        manager = TxtFileManager(factory)

        # Патчим open, чтобы работать с StringIO
        with patch('builtins.open', return_value=StringIO(input_text)):
            # Считываем текст из "файла" (StringIO)
            text = manager.read_txt_file("input.txt")
            # Обрабатываем текст
            result = manager.processor.process(text)
            # Проверяем, что результат совпадает с ожидаемым
            self.assertEqual(result, expected_output)

    def test_regex_txt_processor(self):
        # Условие для обработки текста
        input_text = "Вычислите 2 + 2, 5 * 6 и 8 / 4. Не трогайте 3 + x."
        expected_output = "Вычислите 4, 30 и 2.0. Не трогайте 3 + x."

        # Создаём менеджер файлов с использованием фабрики для RegexTextProcessor
        factory = RegexTxtProcessorFactory()
        manager = TxtFileManager(factory)

        # Патчим open, чтобы работать с StringIO
        with patch('builtins.open', return_value=StringIO(input_text)):
            # Считываем текст из "файла" (StringIO)
            text = manager.read_txt_file("input.txt")
            # Обрабатываем текст
            result = manager.processor.process(text)
            # Проверяем, что результат совпадает с ожидаемым
            self.assertEqual(result, expected_output)

if __name__ == "__main__":
    unittest.main()
