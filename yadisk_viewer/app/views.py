import threading

from django.shortcuts import render, redirect
from django.views import View
from yadisk_viewer.utils.yadisk_api import YandexDiskAPI
from django.http import JsonResponse, FileResponse
import os


class FilterFilesView(View):
    def get(self, request):
        public_key = request.session.get('public_key')
        file_type = request.GET.get('type')
        current_path = request.GET.get('path', '')

        if not public_key or not file_type:
            return JsonResponse({'error': 'Missing parameters'}, status=400)

        data = YandexDiskAPI.get_folder_contents(public_key, current_path)
        if not data:
            return JsonResponse({'error': 'Failed to get files'}, status=500)

        filtered_files = YandexDiskAPI.filter_files_by_type(data, file_type)
        return JsonResponse({'files': filtered_files})


class DownloadMultipleView(View):
    def post(self, request):
        public_key = request.session.get('public_key')
        file_paths = request.POST.getlist('file_paths[]')

        if not public_key or not file_paths:
            return JsonResponse({'error': 'Параметры не переданы'}, status=400)

        zip_path = YandexDiskAPI.create_zip_from_files(public_key, file_paths)

        if not zip_path or not os.path.exists(zip_path):
            return JsonResponse({'error': 'Не удалось создать архив'}, status=500)

        response = FileResponse(open(zip_path, 'rb'), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="selected_files.zip"'

        # Удаление временного файла через поток, чтобы не блокировать ответ
        def cleanup():
            try:
                os.remove(zip_path)
                os.rmdir(os.path.dirname(zip_path))
            except Exception:
                pass

        threading.Thread(target=cleanup).start()

        return response


# Базовая страница (index.html)
class IndexView(View):

    template_name: str = 'app/index.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        public_key = request.POST.get('public_key', '').strip()

        if not public_key:
            return render(request, self.template_name, {
                'error': 'Пожалуйста, введите публичную ссылку'
            })

        # Сохраняем ссылку в сессии
        request.session['public_key'] = public_key
        return redirect('files_list')

# Страница показа файлов
class FilesListView(View):
    template_name = 'app/files_list.html'

    def get(self, request):
        public_key = request.session.get('public_key')
        current_path = request.GET.get('path', '')
        file_type = request.GET.get('type', '')

        if not public_key:
            return redirect('index')

        data = YandexDiskAPI.get_folder_contents(public_key, current_path)

        if not data or 'error' in data:
            return render(request, self.template_name, {
                'error': 'Не удалось получить содержимое папки. Проверьте ссылку.'
            })

        files = []
        breadcrumbs = []

        # Формируем хлебные крошки
        if current_path:
            parts = current_path.split('/')
            for i, part in enumerate(parts):
                if part:
                    breadcrumbs.append({
                        'name': part,
                        'path': '/'.join(parts[:i + 1])
                    })

        if '_embedded' in data and 'items' in data['_embedded']:
            for item in data['_embedded']['items']:
                files.append({
                    'name': item.get('name', ''),
                    'path': item.get('path', ''),
                    'type': item.get('type', 'file'),
                    'size': item.get('size', 0),
                    'modified': item.get('modified', ''),
                    'media_type': item.get('media_type', '')
                })

        return render(request, self.template_name, {
            'files': files,
            'public_key': public_key,
            'current_path': current_path,
            'breadcrumbs': breadcrumbs,
            'parent_path': '/'.join(current_path.split('/')[:-1]) if current_path else '',
            'selected_type': file_type
        })
# Загрузчик
class DownloadView(View):
    def get(self, request, path):
        public_key = request.session.get('public_key')

        if not public_key:
            return redirect('index')

        download_url = YandexDiskAPI.get_download_link(public_key, path)

        if not download_url:
            return render(request, 'app/files_list.html', {
                'error': 'Не удалось получить ссылку для скачивания'
            })

        return redirect(download_url)

