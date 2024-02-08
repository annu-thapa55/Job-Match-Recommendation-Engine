import os
import pandas as pd
import unittest
from src.file_reader.read_files import File


class TestFileClass(unittest.TestCase):
    """
    Test suite for validating the functionalities of File class.

    This test suite class contains individual test methods for various functionalities of the
    File class to ensure its proper functioning under different scenarios and conditions.
    """
    def setUp(self):
        """
        Function for setting up the test cases.

        It is called before performing each test case so as to set up necessary
        resources for testing.
        """

        # Creating a sample CSV file for testing
        self.path_test_file = 'test_file.csv'
        self.sample_data = {
            'A': [5, 10, 15],
            'B': [20, 25, 30],
            'C': ['apple', 'lemon', 'pine apple']
        }
        pd.DataFrame(self.sample_data).to_csv(self.path_test_file, index=False)
        
    def tearDown(self):
        """
        Function for cleaning up after performing each test case.

        It is called after each test case for removing any resources created during testing.
        """
        os.remove(self.path_test_file)

    def test_read_file_success(self):
        """
        Function for testing reading a valid CSV file functionality.

        It tests whether the read_file function of the File class reads a valid CSV 
        file and returns a pandas DataFrame correctly.
        """

        file_handler = File(self.path_test_file)
        result = file_handler.read_file()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), len(self.sample_data['A']))

    def test_read_file_nonexistent_file(self):
        """
        Function for testing reading a non-existent file.

        It tests whether the read_file function raises a ValueError when attempting to read
        a non-existent file.
        """

        file_handler = File('non_existent_file.csv')
        with self.assertRaises(ValueError):
            file_handler.read_file()
    
    def test_read_file_empty_file(self):
        """
        Function for testing reading an empty CSV file.

        It tests whether the read_file function raises a ValueError when attempting to read
        an empty CSV file.
        """

        empty_file_path = 'empty_file.csv'      
        # Creating an empty file
        open(empty_file_path, 'a').close()  
        file_handler = File(empty_file_path)
        with self.assertRaises(ValueError):
            file_handler.read_file()
        # Removing empty file
        os.remove(empty_file_path)  
    
    def test_cleanse_dataset(self):
        """
        Function for testing cleansing a DataFrame functionality.

        It tests the cleanse_dataset function by providing a DataFrame
        with duplicate and null values and ensuring that these duplicate and
        null values are successfully removed.
        """
        data = {
            'A': [1, 2, 2, None],
            'B': ['enjoying', 'coding', 'challenge', 'challenge']
        }
        df = pd.DataFrame(data)
        cleansed_df = File.cleanse_dataset(df)
        # Checking for removal of duplicates and null values
        self.assertEqual(len(cleansed_df), 3)  

if __name__ == '__main__':
    unittest.main()
