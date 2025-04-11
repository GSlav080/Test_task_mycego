from django.shortcuts import render, redirect
from django.views import View
from yadisk_viewer.utils.yadisk_api import YandexDiskAPI

# Базовая страница (index.html)
class IndexView(View):

    template_name = 'app/index.html'

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

        if not public_key:
            return redirect('index')

        data = YandexDiskAPI.get_folder_contents(public_key, current_path)

        if not data or 'error' in data:
            return render(request, self.template_name, {
                'error': 'Не удалось получить содержимое папки. Проверьте ссылку.'
            })

        files = []
        breadcrumbs = []

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
            'parent_path': '/'.join(current_path.split('/')[:-1]) if current_path else ''
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