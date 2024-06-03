# yandex_storage.py
import requests
from django.conf import settings
from django.core.files.storage import Storage
from django.core.exceptions import ImproperlyConfigured
from urllib.parse import urljoin

class YandexDiskStorage(Storage):
    def __init__(self):
        self.oauth_token = settings.YANDEX_DISK_OAUTH_TOKEN
        self.api_url = settings.YANDEX_DISK_API_URL
        self.root_path = settings.YANDEX_DISK_ROOT_PATH

    def _get_headers(self):
        return {
            'Authorization': f'OAuth {self.oauth_token}'
        }

    def _get_upload_link(self, path):
        upload_url = urljoin(self.api_url, 'upload')
        params = {'path': path, 'overwrite': 'true'}
        response = requests.get(upload_url, headers=self._get_headers(), params=params)
        response.raise_for_status()
        return response.json()['href']

    def _get_download_link(self, path):
        download_url = urljoin(self.api_url, 'download')
        params = {'path': path}
        response = requests.get(download_url, headers=self._get_headers(), params=params)
        response.raise_for_status()
        return response.json()['href']

    def _save(self, name, content):
        path = f"{self.root_path}/{name}"
        upload_link = self._get_upload_link(path)
        response = requests.put(upload_link, files={'file': content})
        response.raise_for_status()
        return name

    def url(self, name):
        path = f"{self.root_path}/{name}"
        return self._get_download_link(path)

    def exists(self, name):
        path = f"{self.root_path}/{name}"
        response = requests.get(self.api_url, headers=self._get_headers(), params={'path': path})
        return response.status_code == 200
