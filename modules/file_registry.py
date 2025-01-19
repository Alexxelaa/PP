class FileProcessorRegistry:
    _registry = {}

    @classmethod
    def register(cls, file_type, eval_factory, regex_factory):
        """
        Регистрирует фабрики для указанного типа файла.

        :param file_type: Тип файла (например, "TXT", "JSON")
        :param eval_factory: Класс фабрики для обработки методом eval
        :param regex_factory: Класс фабрики для обработки методом регулярных выражений
        """
        cls._registry[file_type.upper()] = {
            "eval": eval_factory,
            "regex": regex_factory,
        }

    @classmethod
    def get_registered_types(cls):
        """
        Возвращает список зарегистрированных типов файлов.

        :return: Список строк с типами файлов
        """
        return list(cls._registry.keys())

    @classmethod
    def get_factory(cls, file_type, use_eval):
        """
        Возвращает фабрику для указанного типа файла и метода обработки.

        :param file_type: Тип файла
        :param use_eval: использовать метод eval (True) или регулярные выражения (False)
        :return: Экземпляр фабрики
        """
        if file_type.upper() not in cls._registry:
            raise ValueError(f"Тип файла {file_type} не зарегистрирован.")
        key = "eval" if use_eval else "regex"
        return cls._registry[file_type.upper()][key]()
