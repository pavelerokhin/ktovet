import os
import pickle
import unittest

from dump import dump, read_dump, clear_dump


class TestDumpAndReadDump(unittest.TestCase):
    def setUp(self):
        self.test_data = [1, 2, 3]
        self.dump_file = 'test_dump.pickle'

    def tearDown(self):
        if os.path.exists(self.dump_file):
            os.remove(self.dump_file)

    def test_dump_and_read_dump(self):
        dump(self.test_data, self.dump_file)
        loaded_data = read_dump(self.dump_file)
        self.assertEqual(loaded_data, self.test_data)

    def test_read_dump_file_not_found(self):
        non_existing_file = 'non_existing_file.pickle'
        loaded_data = read_dump(non_existing_file)
        self.assertEqual(loaded_data, None)

    def test_clear_dump(self):
        # Create some temporary pickle files for testing
        pickle.dump('data', open('file1.pickle', 'wb'))
        pickle.dump('data', open('file2.pickle', 'wb'))

        clear_dump()

        # Check if the pickle files have been deleted
        self.assertFalse(os.path.exists('file1.pickle'))
        self.assertFalse(os.path.exists('file2.pickle'))


if __name__ == '__main__':
    unittest.main()
