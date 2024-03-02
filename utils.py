from typing import List

from ebooklib import epub
import argparse
import ebookmeta


def get_book_data() -> List:
    """
    Извлекает метаданные из epub/fb2 и возвращает список типа
    ["Название книги", [Автор/авторы], "Издательство", "Дата издания"]
    """

    # Парсим путь к файлу из командной строки

    parser = argparse.ArgumentParser(description='Parser for EPUB and FB2 files')
    parser.add_argument('file', metavar='FILE', type=str, help='Path to the file to parse')
    args = parser.parse_args()
    file_path = args.file

    file_extention = file_path.split('.')[1]  # Определяем тип файла

    # Если файл расширения epub - извлекаем метаданные

    if file_extention.lower() == "epub":
        book = epub.read_epub(file_path)
        title = book.get_metadata('DC', 'title')[0][0]
        creator_data = book.get_metadata('DC', 'creator')
        publisher_data = book.get_metadata('DC', 'publisher')

        # Если автора нет

        if not creator_data:
            author = 'Автор неизвестен'

        # Записываем автора/авторов в список
        else:
            author = [author[0] for author in creator_data]


        date_data = book.get_metadata('DC', 'date')

        # Если нет даты издательства книги

        if not date_data:
            date = "Дата издания не указана"
        else:
            date = book.get_metadata('DC', 'date')[0][0]

        # Если нет информации об издательстве

        if not publisher_data:
            publisher = "Информация об издательстве - отсутствует"
        else:
            publisher = book.get_metadata('DC', 'publisher')[0][0].split(",")[0]

    # Если файл расширения fb2 - извлекаем метаданные, аналогично

    elif file_extention.lower() == "fb2":

        meta = ebookmeta.get_metadata(file_path)
        creator_data = meta.author_list
        title = meta.title
        publisher_data = meta.publish_info.publisher
        date_data = meta.publish_info.year


        if not creator_data:
            author = 'Автор неизвестен'
        else:
            author = meta.author_list

        if not publisher_data:
            publisher = "Информация об издательстве - отсутствует"
        else:
            publisher = meta.publish_info.publisher

        if not date_data:
            date = "Дата издания не указана"
        else:
            date = meta.publish_info.year

    return [title, author, publisher, date]
