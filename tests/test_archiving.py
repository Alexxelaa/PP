import unittest
from unittest.mock import patch, mock_open
import zipfile
import os
from modules.archiving import unzip_file, zip_file


class TestZipFunctions(unittest.TestCase):

    @patch("zipfile.ZipFile")
    def test_unzip_file_success(self, MockZipFile):
        """Тест успешной разархивации"""
        mock_zip = MockZipFile.return_value
        mock_zip.extractall.return_value = None  # Мокаем успешную работу функции extractall

        zip_file_path = "test.zip"
        output_dir = "output"

        unzip_file(zip_file_path, output_dir)

        MockZipFile.assert_called_once_with(zip_file_path, 'r')
        mock_zip.extractall.assert_called_once_with(output_dir)

    @patch("zipfile.ZipFile")
    def test_unzip_file_file_not_found(self, MockZipFile):
        """Тест для случая, когда ZIP файл не найден"""
        zip_file_path = "non_existent.zip"
        output_dir = "output"

        with self.assertRaises(FileNotFoundError):
            unzip_file(zip_file_path, output_dir)

    @patch("zipfile.ZipFile")
    def test_unzip_file_bad_zip(self, MockZipFile):
        """Тест для случая с невалидным ZIP файлом"""
        mock_zip = MockZipFile.return_value
        mock_zip.extractall.side_effect = zipfile.BadZipFile  # Имитируем ошибку BadZipFile

        zip_file_path = "bad.zip"
        output_dir = "output"

        with self.assertRaises(zipfile.BadZipFile):
            unzip_file(zip_file_path, output_dir)

    @patch("os.path.exists")
    @patch("os.makedirs")
    @patch("zipfile.ZipFile")
    def test_zip_file_success(self, MockZipFile, mock_makedirs, mock_exists):
        """Тест успешной архивации"""
        mock_exists.return_value = True  # Файл существует
        zip_file_path = "test.zip"
        file_path = "test.txt"

        zip_file(file_path, zip_file_path)

        MockZipFile.assert_called_once_with(zip_file_path, 'w', zipfile.ZIP_DEFLATED)
        MockZipFile.return_value.write.assert_called_once_with(file_path, os.path.basename(file_path))

    @patch("os.path.exists")
    def test_zip_file_file_not_found(self, mock_exists):
        """Тест для случая, когда файл для архивирования не найден"""
        mock_exists.return_value = False
        zip_file_path = "test.zip"
        file_path = "non_existent.txt"

        with self.assertRaises(FileNotFoundError):
            zip_file(file_path, zip_file_path)

    @patch("zipfile.ZipFile")
    def test_zip_file_exception(self, MockZipFile):
        """Тест для случая, когда происходит ошибка при архивировании"""
        MockZipFile.side_effect = Exception("Ошибка при архивировании")
        zip_file_path = "test.zip"
        file_path = "test.txt"

        with self.assertRaises(Exception):
            zip_file(file_path, zip_file_path)


if __name__ == "__main__":
    unittest.main()
