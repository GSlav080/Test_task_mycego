from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('files/', FilesListView.as_view(), name='files_list'),
    path('download/<path:path>/', DownloadView.as_view(), name='download'),
    path('filter/', FilterFilesView.as_view(), name='filter_files'),
    path('download-multiple/', DownloadMultipleView.as_view(), name='download_multiple'),
]