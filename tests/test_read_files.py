import os
import pandas as pd
import unittest
from unittest.mock import MagicMock, patch
from src.file_reader.read_files import File


class TestFileClass(unittest.TestCase):
    def setUp(self):
        self.test_csv_file = 'test_data.csv'
        # Create a test CSV file with some data
        self.create_test_csv()

        # Create a File instance for testing
        self.file_instance = File(self.test_csv_file)


if __name__ == '__main__':
    unittest.main()
