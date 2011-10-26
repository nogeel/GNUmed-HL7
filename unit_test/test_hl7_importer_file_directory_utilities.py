from datetime import datetime
import os
import shutil
import tempfile


import unittest
from mock import patch
from hl7_importer_file_directory_utilities import process_directory, create_output_path, handle_processed_file

class ProcessDirectoryTest(unittest.TestCase):

    @patch("hl7_importer_file_directory_utilities.glob")
    def test_list_files(self, mock_glob):
        expected = ['/temp/a.sds', '/temp/b.sds', '/test/c.sds']
        mock_glob.return_value = expected
        result = process_directory('sds', '/temp')
        mock_glob.assert_called_with('/temp/*.sds')
        self.assertEqual(result, expected)

class CreateOutputPathTest(unittest.TestCase):

    fake_path = '/path/to/file/file.sds'
    new_extension = 'new'
    test_out_directory = '/path/to/where/to/put'

    def test_create_output_path(self):
        expected = "/path/to/where/to/put/file.new"

        result = create_output_path(self.new_extension, self.fake_path, self.test_out_directory)
        self.assertEqual(expected, result)
        result = create_output_path(self.new_extension, self.fake_path, self.test_out_directory+"/")
        self.assertEqual(expected, result)

    @patch("hl7_importer_file_directory_utilities.datetime")
    def test_create_output_path_with_date(self, mock_datetime):
        expected =  "/path/to/where/to/put/file-2011-10-06 09:21:20.724603.new"
        mock_datetime.now.return_value = datetime(2011, 10, 6, 9, 21, 20,724603)
        result = create_output_path(self.new_extension, self.fake_path, self.test_out_directory, True)
        self.assertEqual(expected, result)
        result = create_output_path(self.new_extension, self.fake_path, self.test_out_directory+"/", True)
        self.assertEqual(expected, result)


    def test_handle_processed_file_px(self):
        dir_name = tempfile.mkdtemp()
        expected_file = os.path.join(dir_name, "test_file.asd.px")
        temp_file_path = os.path.join(dir_name, "test_file.asd")
        file_temp = open(temp_file_path,'w')
        file_temp.close()

        handle_processed_file(file_temp.name)
        self.assertTrue(os.path.exists(expected_file))

        #clean_up
        shutil.rmtree(dir_name)


    def test_handle_processed_file_move(self):
        dir_name = tempfile.mkdtemp()
        move_dir_name = tempfile.mkdtemp()

        expected_file = os.path.join(move_dir_name, "test_file.asd")
        temp_file_path = os.path.join(dir_name, "test_file.asd")

        file_temp = open(temp_file_path,'w')
        file_temp.close()

        handle_processed_file(file_temp.name, move_dir_name)
        self.assertFalse(os.path.exists(temp_file_path))
        self.assertTrue(os.path.exists(expected_file))

        #clean_up
        shutil.rmtree(dir_name)
        shutil.rmtree(move_dir_name)




if __name__ == '__main__':
    unittest.main()