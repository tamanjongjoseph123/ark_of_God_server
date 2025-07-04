from ftplib import FTP, error_perm
from django.core.files.storage import Storage
from django.core.files.base import File
from django.conf import settings
from io import BytesIO
import os
from django.core.files.images import ImageFile

class FTPStorage(Storage):
    def __init__(self):
        opts = settings.FTP_STORAGE_OPTIONS
        self.host = opts["host"]
        self.username = opts["username"]
        self.password = opts["password"]
        self.base_path = opts.get("base_path", "/")
        self.port = opts.get("port", 21)
        self.passive = opts.get("passive", True)

    def _connect(self):
        ftp = FTP()
        ftp.connect(self.host, self.port)
        ftp.login(self.username, self.password)
        ftp.set_pasv(self.passive)
        ftp.cwd(self.base_path)
        return ftp

    def _save(self, name, content):
        ftp = self._connect()
        path_parts = name.split("/")
        for part in path_parts[:-1]:
            try:
                ftp.mkd(part)
            except error_perm:
                pass
            ftp.cwd(part)

        content.open('rb')  # Ensure binary mode
        content.file.seek(0)  # Ensure pointer is at start
        ftp.storbinary(f"STOR {path_parts[-1]}", content.file)
        ftp.quit()
        return name

    def open(self, name, mode='rb'):
        ftp = self._connect()
        path_parts = name.split("/")
        for part in path_parts[:-1]:
            ftp.cwd(part)

        file_data = BytesIO()
        ftp.retrbinary(f"RETR {path_parts[-1]}", file_data.write)
        ftp.quit()
        file_data.seek(0)

        # Dynamically choose return type based on file extension
        if name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
            return ImageFile(file_data, name)
        return File(file_data, name)

    def exists(self, name):
        try:
            ftp = self._connect()
            ftp.size(name)
            ftp.quit()
            return True
        except:
            return False

    def delete(self, name):
        try:
            ftp = self._connect()
            ftp.delete(name)
            ftp.quit()
        except:
            pass

    def size(self, name):
        try:
            ftp = self._connect()
            size = ftp.size(name)
            ftp.quit()
            return size
        except:
            return 0

    def listdir(self, path):
        ftp = self._connect()
        ftp.cwd(os.path.join(self.base_path, path))
        files = []
        dirs = []
        ftp.retrlines('LIST', lambda line: (dirs if line.startswith('d') else files).append(line.split()[-1]))
        ftp.quit()
        return dirs, files

    def url(self, name):
        return f"{settings.MEDIA_URL}{name}"
