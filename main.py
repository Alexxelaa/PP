import tkinter as tk
from tkinter import filedialog, messagebox
import os
from modules.txt_process import *
from modules.json_process import *
from modules.xml_process import *
from modules.yaml_process import *
from modules.archiving import zip_file, unzip_file
from modules.encryption import encrypt_file_shift, decrypt_file_shift


class FileManagerFactory:
    def create(self, file_type, method):
        raise NotImplementedError("Метод create должен быть реализован.")


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


class FileProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Файл Обработчик")

        self.file_type = tk.StringVar()
        self.method = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Добро пожаловать в программу обработки файлов!", font=("Arial", 14)).grid(row=0, column=0, columnspan=3, pady=10)

        tk.Label(self.root, text="Выберите тип файла:").grid(row=1, column=0, sticky="w", padx=10)
        file_type_menu = tk.OptionMenu(self.root, self.file_type, "1: TXT", "2: JSON", "3: XML", "4: YAML")
        file_type_menu.grid(row=1, column=1, sticky="w")

        tk.Label(self.root, text="Выберите метод обработки:").grid(row=2, column=0, sticky="w", padx=10)
        method_menu = tk.OptionMenu(self.root, self.method, "1: EVAL", "2: РЕГУЛЯРНЫЕ ВЫРАЖЕНИЯ")
        method_menu.grid(row=2, column=1, sticky="w")

        tk.Label(self.root, text="Выберите входной файл:").grid(row=3, column=0, sticky="w", padx=10)
        self.input_file_entry = tk.Entry(self.root, width=50)
        self.input_file_entry.grid(row=3, column=1, padx=10)
        tk.Button(self.root, text="Выбрать файл", command=self.select_input_file).grid(row=3, column=2, padx=10)

        tk.Label(self.root, text="Выберите выходной файл:").grid(row=4, column=0, sticky="w", padx=10)
        self.output_file_entry = tk.Entry(self.root, width=50)
        self.output_file_entry.grid(row=4, column=1, padx=10)
        tk.Button(self.root, text="Сохранить файл как", command=self.select_output_file).grid(row=4, column=2, padx=10)

        tk.Button(self.root, text="Обработать файл", command=self.process_file).grid(row=5, column=0, columnspan=3, pady=10)

        self.archive_choice = tk.BooleanVar()
        self.encrypt_choice = tk.BooleanVar()

        tk.Checkbutton(self.root, text="Хотите заархивировать выходной файл?", variable=self.archive_choice).grid(row=6, column=0, columnspan=2, sticky="w", padx=10)
        tk.Checkbutton(self.root, text="Хотите зашифровать выходной файл?", variable=self.encrypt_choice).grid(row=7, column=0, columnspan=2, sticky="w", padx=10)

    def select_input_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.input_file_entry.delete(0, tk.END)
            self.input_file_entry.insert(0, filename)

    def select_output_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"),
                                                                                   ("JSON files", "*.json"),
                                                                                   ("XML files", "*.xml"),
                                                                                   ("YAML files", "*.yaml")])
        if filename:
            self.output_file_entry.delete(0, tk.END)
            self.output_file_entry.insert(0, filename)

    def process_file(self):
        file_type = self.file_type.get().split(":")[0]
        method = self.method.get().split(":")[0]
        input_file = self.input_file_entry.get()
        output_file = self.output_file_entry.get()

        if not file_type or not method or not input_file or not output_file:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
            return

        # Расшифровка, если файл зашифрован
        if input_file.endswith(".encrypted"):
            try:
                decrypt_file_shift(input_file)
                input_file = input_file.replace(".encrypted", ".decrypted")
                messagebox.showinfo("Успех", f"Файл {input_file} успешно расшифрован.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при расшифровке файла: {e}")
                return

        # Разархивирование, если файл является ZIP-архивом
        if input_file.endswith(".zip"):
            extracted_dir = "extracted_files"
            try:
                unzip_file(input_file, extracted_dir)
                extracted_files = os.listdir(extracted_dir)
                if not extracted_files:
                    messagebox.showerror("Ошибка", "Архив пуст.")
                    return
                input_file = os.path.join(extracted_dir, extracted_files[0])
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при разархивировании файла: {e}")
                return

        file_manager_creator = FileManagerCreator()

        try:
            file_manager = file_manager_creator.get_file_manager(file_type, method)
            file_manager.process_file(input_file, output_file)
            messagebox.showinfo("Успех", f"Файл успешно обработан и сохранён в: {output_file}")

            if self.archive_choice.get():
                zip_file(output_file, f"{output_file}.zip")
                messagebox.showinfo("Успех", f"Файл {output_file} успешно заархивирован в {output_file}.zip")

            if self.encrypt_choice.get():
                encrypt_file_shift(output_file)
                messagebox.showinfo("Успех", f"Файл {output_file} успешно зашифрован.")

        except ValueError as ve:
            messagebox.showerror("Ошибка", str(ve))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при обработке файла: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileProcessingApp(root)
    root.mainloop()
