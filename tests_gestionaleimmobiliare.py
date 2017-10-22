import tarfile
import unittest
from io import BufferedReader
from os.path import join

from gestionaleimmobiliare.sync_agenzia.fetch_remote import TarFile, TarGzFile
from gestionaleimmobiliare.sync_agenzia.agent import SyncInterpreter

relative_path = ['tests', 'resources']
test_archive_content = ['test-tar-archive',
                        'test-tar-archive/a-directory',
                        'test-tar-archive/a-directory/another-one',
                        'test-tar-archive/a-directory/another-one/file-1',
                        'test-tar-archive/a-directory/another-one/file-2',
                        'test-tar-archive/a-directory/another-one/very-deep.xml',
                        'test-tar-archive/a-directory/wrong-extension-xml.txt',
                        'test-tar-archive/a-directory/file-1',
                        'test-tar-archive/file-1',
                        'test-tar-archive/file-2',
                        'test-tar-archive/test-file.xml',
                        'test-tar-archive/README']
xml_note = '<?xml version="1.0" encoding="UTF-8" ?>\r\n' \
'<note>\r\n'                                             \
'\t<to>Tove</to>\r\n'                                    \
'\t<from>Jani</from>\r\n'                                \
'\t<heading>Reminder</heading>\r\n'                      \
'\t<body>Don\'t forget me this weekend!</body>\r\n'      \
'</note>'


class TarFileTests(unittest.TestCase):

    def test_wrong_archive_type(self) -> None:
        archive = self.mock_archive('test-tar-archive.tar.gz')
        with self.assertRaises(tarfile.ReadError):
            archive.list_content()

    def test_file_list(self) -> None:
        archive = self.mock_archive('test-tar-archive.tar')
        self.assertCountEqual(archive.list_content(),
                              test_archive_content,
                              'Test archive and expected files in it do not match')

    def test_open_xmls(self) -> None:
        archive = self.mock_archive('test-tar-archive.tar')
        xml_files = archive.extract_xml_files()

        self.assertEqual(len(xml_files), 2)

        for xml_buf in archive.extract_xml_files():
            self.assertIsInstance(xml_buf, BufferedReader,
                                  'Every returned file object should be a buffer')

        self.assertEqual(xml_files[1].read().decode('utf-8'), xml_note)
        archive.close()

    def mock_archive(self, archive_name: str) -> TarFile:
        with open(join(*relative_path, archive_name), 'rb') as f:
            return TarFile(f.read(), archive_name=archive_name)


class TarGzFileTests(unittest.TestCase):

    def test_wrong_archive_type(self) -> None:
        archive = self.mock_archive('test-tar-archive.tar')
        with self.assertRaises(tarfile.ReadError):
            archive.list_content()

    def test_file_list(self) -> None:
        archive = self.mock_archive('test-tar-archive.tar.gz')
        self.assertCountEqual(archive.list_content(),
                              test_archive_content,
                              'Test archive and expected files in it do not match')

    def test_open_xmls(self) -> None:
        archive = self.mock_archive('test-tar-archive.tar.gz')
        xml_files = archive.extract_xml_files()

        self.assertEqual(len(xml_files), 2)

        for xml_buf in archive.extract_xml_files():
            self.assertIsInstance(xml_buf, BufferedReader,
                                  'Every returned file object should be a buffer')

        self.assertEqual(xml_files[1].read().decode('utf-8'), xml_note)
        archive.close()

    def mock_archive(self, archive_name: str) -> TarGzFile:
        with open(join(*relative_path, archive_name), 'rb') as f:
            return TarGzFile(f.read(), archive_name=archive_name)


class GISyncInterpreterTests(unittest.TestCase):

    @staticmethod
    def mock_response(xml_name: str) -> str:
        with open(join(*relative_path, xml_name), 'r') as f:
            return f.read()

    def test_xml_parse(self) -> None:
        xml_content = self.mock_response('annuncio.xml')
        sync_agent = SyncInterpreter('http://domain.com')
        doc = sync_agent.parse_xml(xml_content)
        annuncio = doc.getroot()

        self.assertEqual(annuncio.info.agency_code, 'AP56')
        self.assertEqual(annuncio.info.ape.version, 2015)
        self.assertEqual(annuncio.info.ape.epgl_ren, 11.00)
        self.assertEqual(annuncio.info.ape.prestazione_estate, 'medio')
        self.assertFalse(annuncio.file_allegati.allegato[0].planimetria)
        self.assertTrue(annuncio.file_allegati.allegato[1].planimetria)
