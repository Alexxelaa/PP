import zipfile
import os

"""функции архивации/разархивация"""
def unzip_file(zip_file_path, output_dir):
    """
    Функция разархивирует ZIP-файл в указанную директорию.

    :param zip_file_path: Путь к ZIP-файлу
    :param output_dir: Директория, в которую нужно разархивировать файл
    """
    try:
        # Проверяем, существует ли выходная директория, если нет — создаем
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Открываем ZIP-файл
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            # Извлекаем все файлы в указанную директорию
            zip_ref.extractall(output_dir)
            print(f"Файлы успешно разархивированы в {output_dir}")
    except FileNotFoundError:
        print(f"Файл {zip_file_path} не найден.")
    except zipfile.BadZipFile:
        print(f"Файл {zip_file_path} не является валидным ZIP-архивом.")
    except Exception:
        print(f"Произошла ошибка: {Exception}")

def zip_file(file_path, zip_file_path):
    """
    Функция архивирует файл в ZIP.

    :param file_path: Путь к файлу, который нужно архивировать
    :param zip_file_path: Путь к конечному ZIP-файлу
    """
    try:
        # Проверяем, существует ли исходный файл
        if not os.path.exists(file_path):
            print(f"Файл {file_path} не найден.")
            return

        # Архивируем файл в ZIP
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_path, os.path.basename(file_path))  # Добавляем файл в архив
            print(f"Файл {file_path} успешно архивирован в {zip_file_path}")

    except Exception:
        print(f"Произошла ошибка при архивировании: {Exception}")