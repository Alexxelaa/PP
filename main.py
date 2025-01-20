from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

from modules.txt_process import *
from modules.json_process import *
from modules.xml_process import *
from modules.yaml_process import *
from modules.archiving import unzip_file, zip_file  # Импортируем уже существующие функции
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


app = Flask(__name__)

# Папки для загрузки и обработки файлов
UPLOAD_FOLDER = 'input_data'
OUTPUT_FOLDER = 'output_data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process_file():
    try:
        # Получаем данные из формы
        file = request.files['file']
        file_type = request.form['file_type']
        method = request.form['method']
        output_filename = request.form['output_filename']

        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'No file selected'})

        # Сохраняем загруженный файл
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)

        # Проверяем, является ли файл архивом, и разархивируем его
        if input_path.endswith(".zip"):
            output_dir = os.path.join(UPLOAD_FOLDER, "unzipped")
            try:
                unzip_file(input_path, output_dir)
                # После разархивирования берем первый файл
                input_path = os.path.join(output_dir, os.listdir(output_dir)[0])
                print(f"Архив {filename} разархивирован.")
            except Exception as e:
                return jsonify({'status': 'error', 'message': f"Ошибка при разархивировании: {str(e)}"})

        # Проверяем, зашифрован ли файл, и расшифровываем его
        if input_path.endswith(".encrypted"):
            try:
                decrypt_file_shift(input_path)
                input_path = input_path.replace(".encrypted", ".decrypted")
                print(f"Файл расшифрован: {input_path}")
            except Exception as e:
                return jsonify({'status': 'error', 'message': f"Ошибка при расшифровке: {str(e)}"})

        # Создание экземпляра FileManager для обработки
        file_manager_creator = FileManagerCreator()
        file_manager = file_manager_creator.get_file_manager(file_type, method)

        # Обработка файла
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        file_manager.process_file(input_path, output_path)

        # Спрашиваем, нужно ли заархивировать
        zip_output = request.form.get('zip', 'no') == 'yes'
        if zip_output:
            zip_file(output_path, f"{output_path}.zip")
            output_path = f"{output_path}.zip"

        # Спрашиваем, нужно ли зашифровать
        encrypt_output = request.form.get('encrypt', 'no') == 'yes'
        if encrypt_output:
            encrypt_file_shift(output_path)
            output_path = f"{output_path}.encrypted"

        return jsonify({
            'status': 'success',
            'message': f"Файл успешно обработан.",
            'download_url': f"/download/{os.path.basename(output_path)}"
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
