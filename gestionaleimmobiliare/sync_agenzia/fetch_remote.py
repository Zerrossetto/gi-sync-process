import sys
import tarfile
from asyncio import coroutine
from io import BytesIO

from aiohttp import ClientSession, Timeout


class TarFile:

    def __init__(self, bytes_in: bytes, archive_name: str=None):
        self.bytes_in = bytes_in
        self.compression_mode = 'r:'
        self.archive_name = archive_name
        self.archive_buffer = None

    @property
    def closed(self):
        return self.archive_buffer is None or self.archive_buffer.closed

    def open(self):
        self.archive_buffer = tarfile.open(fileobj=BytesIO(self.bytes_in), mode=self.compression_mode)
        return self.archive_buffer

    def close(self):
        if self.archive_buffer is None:
            raise IOError('Archive already closed')
        else:
            self.archive_buffer.close()

    def extract_xml_files(self):
        tar = self.open() if self.closed else self.archive_buffer
        return [tar.extractfile(file_name)
                for file_name in tar.getnames()
                if file_name.endswith('.xml')]

    def list_content(self):
        tar = self.open() if self.closed else self.archive_buffer
        file_names = tar.getnames()
        tar.close()
        return file_names

    def __repr__(self):
        if self.archive_name is None:
            return '<{}>'.format(self.__class__.__name__)
        else:
            return '<{} name="{}">'.format(self.__class__.__name__, self.archive_name)


class TarGzFile(TarFile):

    def __init__(self, bytes_in: bytes, archive_name: str=None):
        super(TarGzFile, self).__init__(bytes_in, archive_name)
        self.compression_mode = 'r:gz'


class GIFetch:

    def __init__(self, endpoint_url: str, connection_timeout:int = 10):
        self.session = ClientSession()
        self.endpoint_url = endpoint_url
        self.connection_timeout = connection_timeout

    @coroutine
    def fetch_all(self,):
        tarball = TarGzFile
        pass

    @coroutine
    def get_remote_tarball(self):
        with Timeout(self.timeout):
            response = yield from self.session.get(self.url)
            try:
                return response.read()  # returns binary data
            finally:
                if sys.exc_info()[0] is not None:
                    response.close()
                else:
                    response.release()
