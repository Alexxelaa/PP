from modules.txt_process import *
from modules.json_process import *
from modules.xml_process import *
from modules.yaml_process import *
from modules.archiving import *
from modules.encryption import *
import os

# Абстракция для выбора фабрики в зависимости от типа файла
class FileManagerFactory:
    def create(self, file_type, method):
        raise NotImplementedError("Метод create должен быть реализован.")

# Фабрики для разных типов файлов
class TxtFileManagerFactory(FileManagerFactory):
    def create(self, file_type, method):
        factory = EvalTxtProcessorFactory() if method == "1" else RegexTxtProcessorFactory()
        return TxtFileManager(factory)

class JsonFileManagerFactory(FileManagerFactory):
    def create(self, file_type, method):
        factory = EvalJsonProcessorFactory() if method == "1" else RegexJsonProcessorFactory()
        return JsonFileManager(factory)

class XmlFileManagerFactory(FileManagerFactory):
    def create(self, file_type, method):
        factory = EvalXmlProcessorFactory() if method == "1" else RegexXmlProcessorFactory()
        return XmlFileManager(factory)

class YamlFileManagerFactory(FileManagerFactory):
    def create(self, file_type, method):
        factory = EvalYamlProcessorFactory() if method == "1" else RegexYamlProcessorFactory()
        return YamlFileManager(factory)

# Менеджер для выбора фабрики
class FileManagerCreator:
    def __init__(self):
        self._factories = {
            "1": TxtFileManagerFactory(),
            "2": JsonFileManagerFactory(),
            "3": XmlFileManagerFactory(),
            "4": YamlFileManagerFactory(),
        }

    def get_file_manager(self, file_type, method):
        factory = self._factories.get(file_type)
        if factory:
            return factory.create(file_type, method)
        else:
            raise ValueError(f"Неверный тип файла: {file_type}")

def main():
    print("Добро пожаловать в программу обработки файлов!")
    print("Выберите тип файла для обработки:")
    print("1. TXT")
    print("2. JSON")
    print("3. XML")
    print("4. YAML")

    file_type = input("Введите номер типа файла: ").strip()

    print("Выберите метод обработки:")
    print("1. Использование eval")
    print("2. Использование регулярных выражений")

    method = input("Введите номер метода обработки: ").strip()

    input_file = input("Введите путь к входному файлу (или ZIP-архиву): ").strip()

    # Проверяем, нужно ли расшифровать входной файл
    if input_file.endswith(".encrypted"):
        decrypt_choice = input("Этот файл зашифрован. Хотите расшифровать его? (да/нет): ").strip().lower()
        if decrypt_choice in ["да", "yes", "y"]:
            try:
                decrypt_file_shift(input_file)
                input_file = input_file.replace(".encrypted", ".decrypted")
                print(f"Файл расшифрован: {input_file}")
            except Exception as e:
                print(f"Ошибка при расшифровке файла: {e}")
                return

    # Если входной файл - архив, разархивируем его
    if input_file.endswith(".zip"):
        output_dir = "unzipped_input"
        try:
            unzip_file(input_file, output_dir)
            print(f"Архив {input_file} разархивирован в директорию {output_dir}.")
            input_file = os.path.join(output_dir, os.listdir(output_dir)[0])  # Берём первый файл в директории
        except Exception as e:
            print(f"Ошибка при разархивировании файла: {e}")
            return

    output_file = input("Введите путь к выходному файлу: ").strip()

    file_manager_creator = FileManagerCreator()

    try:
        file_manager = file_manager_creator.get_file_manager(file_type, method)
        file_manager.process_file(input_file, output_file)
        print(f"Файл успешно обработан и сохранён в: {output_file}")

        # Спрашиваем, нужно ли заархивировать выходной файл
        archive_choice = input("Хотите заархивировать выходной файл? (да/нет): ").strip().lower()
        if archive_choice in ["да", "yes", "y"]:
            zip_file(output_file, f"{output_file}.zip")
            print(f"Файл {output_file} успешно заархивирован в {output_file}.zip")

        # Спрашиваем, нужно ли зашифровать выходной файл
        encrypt_choice = input("Хотите зашифровать выходной файл? (да/нет): ").strip().lower()
        if encrypt_choice in ["да", "yes", "y"]:
            encrypt_file_shift(output_file)
            print(f"Файл {output_file} успешно зашифрован.")

    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"Произошла ошибка при обработке файла: {e}")

if __name__ == "__main__":
    main()
