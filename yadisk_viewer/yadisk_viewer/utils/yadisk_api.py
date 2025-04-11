import requests
from django.conf import settings
from typing import Optional, Dict, List


class YandexDiskAPI:
    """
    Класс для работы с API Яндекс.Диска
    Документация: https://yandex.ru/dev/disk/api/
    """
    BASE_URL = 'https://cloud-api.yandex.net/v1/disk/public/resources'

    @staticmethod
    def get_files_list(public_key: str) -> Optional[Dict]:
        """
        Получает список файлов по публичной ссылке
        :param public_key: Публичная ссылка на папку/файл
        :return: Словарь с данными о файлах или None при ошибке
        """
        params = {
            'public_key': public_key,
            'limit': 1000  # Максимальное количество файлов, можно изменить, но скорость поменяется
        }

        try:
            response = requests.get(YandexDiskAPI.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Ошибка при получении списка файлов: {e}")
            return None

    @staticmethod
    def get_download_link(public_key: str, path: str) -> Optional[str]:
        """
        Получает прямую ссылку для скачивания файла
        :param public_key: Публичная ссылка на папку
        :param path: Путь к файлу относительно публичной папки
        :return: Прямая ссылка для скачивания или None при ошибке
        """
        params = {
            'public_key': public_key,
            'path': path
        }

        try:
            response = requests.get(f"{YandexDiskAPI.BASE_URL}/download", params=params)
            response.raise_for_status()
            return response.json().get('href')
        except requests.RequestException as e:
            print(f"Ошибка при получении ссылки для скачивания: {e}")
            return None


    @staticmethod
    def get_folder_contents(public_key: str, path: str = '') -> Optional[Dict]:
        """
        Получает содержимое конкретной папки по публичной ссылке и пути
        :param public_key: Публичная ссылка на папку
        :param path: Путь внутри папки (относительный)
        :return: Словарь с данными о файлах или None при ошибке
        """
        params = {
            'public_key': public_key,
            'path': path,
            'limit': 1000
        }

        try:
            response = requests.get(YandexDiskAPI.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Ошибка при получении содержимого папки: {e}")
            return None