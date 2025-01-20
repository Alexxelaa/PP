import unittest
from unittest.mock import mock_open, patch
from modules.encryption import encrypt_file_shift, decrypt_file_shift

class TestEncryptionFunctions(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data="hello"))
    @patch("os.path.exists", return_value=False)  # Избегаем реальной проверки существования файлов
    def test_encrypt_file_shift(self, mock_exists, mock_open):
        # Путь к файлу для теста
        file_path = "test.txt"

        # Запускаем функцию шифрования
        encrypt_file_shift(file_path)

        # Проверка, что файл был записан с расширением .encrypted
        encrypted_file_path = file_path + ".encrypted"

        # Проверяем, что файл был открыт для записи
        mock_open.assert_called_with(encrypted_file_path, 'w', encoding='utf-8')

        # Проверяем, что данные были зашифрованы
        encrypted_data = mock_open().write.call_args[0][0]
        self.assertEqual(encrypted_data, "ifmmp")

    @patch("builtins.open", mock_open(read_data="ifmmp"))
    @patch("os.path.exists", return_value=False)  # Избегаем реальной проверки существования файлов
    def test_decrypt_file_shift(self, mock_exists, mock_open):
        # Путь к зашифрованному файлу для теста
        encrypted_file_path = "test.txt.encrypted"

        # Запускаем функцию дешифрования
        decrypt_file_shift(encrypted_file_path)

        # Проверка, что файл был расшифрован и сохранен как .decrypted
        decrypted_file_path = encrypted_file_path.replace(".encrypted", ".decrypted")

        # Проверяем, что файл был открыт для записи
        mock_open.assert_called_with(decrypted_file_path, 'w', encoding='utf-8')

        # Проверяем, что данные были расшифрованы
        decrypted_data = mock_open().write.call_args[0][0]
        self.assertEqual(decrypted_data, "hello")

    @patch("builtins.open", mock_open(read_data="hello"))
    @patch("os.path.exists", return_value=False)  # Избегаем реальной проверки существования файлов
    def test_encrypt_decrypt_cycle(self, mock_exists, mock_open):
        # Путь к файлу для теста
        file_path = "test.txt"

        # Запускаем шифрование
        encrypt_file_shift(file_path)

        # Проверяем, что файл был зашифрован
        encrypted_file_path = file_path + ".encrypted"
        mock_open.assert_called_with(encrypted_file_path, 'w', encoding='utf-8')

        encrypted_data = mock_open().write.call_args[0][0]
        self.assertEqual(encrypted_data, "ifmmp")

        # Теперь запускаем дешифрование
        decrypt_file_shift(encrypted_file_path)

        # Проверяем, что файл был расшифрован в исходное состояние
        decrypted_file_path = encrypted_file_path.replace(".encrypted", ".decrypted")
        mock_open.assert_called_with(decrypted_file_path, 'w', encoding='utf-8')

        decrypted_data = mock_open().write.call_args[0][0]
        self.assertEqual(decrypted_data, "hello")


if __name__ == "__main__":
    unittest.main()
