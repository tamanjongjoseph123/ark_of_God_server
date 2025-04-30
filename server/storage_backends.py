from ftplib import FTP
from django.core.files.storage import Storage
import os
from django.conf import settings

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
        print("Entered here dude")
        ftp = self._connect()
        path_parts = name.split("/")
        for part in path_parts[:-1]:
            try:
                ftp.mkd(part)
            except:
                pass
            ftp.cwd(part)

        content.open()
        ftp.storbinary(f"STOR {path_parts[-1]}", content.file)
        ftp.quit()
        return name

    def exists(self, name):
        try:
            ftp = self._connect()
            ftp.size(name)
            ftp.quit()
            return True
        except:
            return False

    def url(self, name):
        return f"{settings.MEDIA_URL}{name}"
