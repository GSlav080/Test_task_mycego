from django.urls import path
from .views import IndexView, FilesListView, DownloadView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('files/', FilesListView.as_view(), name='files_list'),
    path('download/<path:path>/', DownloadView.as_view(), name='download'),
]
