import os
import tempfile
import zipfile

import requests
from typing import Optional, Dict, List


class YandexDiskAPI:
    """
    Класс для работы с API Яндекс.Диска
    Документация: https://yandex.ru/dev/disk/api/
    """
    BASE_URL: str = 'https://cloud-api.yandex.net/v1/disk/public/resources'

    @staticmethod
    def get_files_list(public_key: str) -> Optional[Dict]:
        """
        Получает список файлов по публичной ссылке
        :param public_key: Публичная ссылка на папку/файл
        :return: Словарь с данными о файлах или None при ошибке
        """
        params: dict = {
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
        params: dict = {
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
        params: dict = {
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


    @staticmethod
    def filter_files_by_type(files_data: Dict, file_type: str) -> List[Dict]:
        """Фильтрует файлы по типу (image, document, etc.)"""
        type_mapping = {
            'image': ['image/jpeg', 'image/png', 'image/gif'],
            'document': ['application/pdf', 'application/msword',
                         'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
            'archive': ['application/zip', 'application/x-rar-compressed'],
            'video': ['video/mp4', 'video/avi']
        }

        if file_type not in type_mapping:
            return []

        filtered = []
        for item in files_data.get('_embedded', {}).get('items', []):
            if item['type'] == 'file' and item.get('media_type') in type_mapping[file_type]:
                filtered.append(item)
        return filtered


    @staticmethod
    def create_zip_from_files(public_key: str, file_paths: List[str]) -> Optional[str]:
        """Создает временный ZIP-архив из выбранных файлов"""
        if not file_paths:
            return None

        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, 'selected_files.zip')

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in file_paths:
                download_url = YandexDiskAPI.get_download_link(public_key, file_path)
                if download_url:
                    response = requests.get(download_url, stream=True)
                    if response.status_code == 200:
                        file_name = os.path.basename(file_path)
                        zipf.writestr(file_name, response.content)

        return zip_path