# unittest module for writing and running tests
import unittest
# patch function from unittest.mock module for mocking objects during testing
from unittest.mock import patch
# custom RecommendationEngine class for testing its functionalities
from src.recommendation_engine.recommendation import RecommendationEngine


class TestRecommendationEngine(unittest.TestCase):
    """
    Test suite for validating the functionalities of RecommendationEngine class.

    This test suite class contains individual test functions for various functionalities of the
    RecommendationEngine class to ensure its proper functioning under different scenarios and conditions..
    """

    # Patching the abstract methods of the RecommendationEngine class for testing its concrete methods.
    @patch.multiple(RecommendationEngine, __abstractmethods__=set())
    def setUp(self):
        """
        Function for setting up the test cases.

        It is called before performing each test case so as to set up necessary
        resources for testing.
        """
        self.engine = RecommendationEngine()



    def test_set_threshold_parallel_processing_valid(self):
        """
        Function for testing setting a valid threshold for parallel processing.

        It ensures that setting a valid threshold within the specified range is successful.
        """
        self.engine.set_threshold_parallel_processing(7.5)
        self.assertEqual(self.engine.threshold_parallel_processing, 7.5)



    def test_set_threshold_parallel_processing_invalid(self):
        """
        Function for testing setting an invalid threshold for parallel processing.

        It ensures that setting an invalid threshold, above 10 MB or below 5 MB, 
        raises a ValueError.
        """
        # Setting invalid threshold above 10 MB
        with self.assertRaises(ValueError):
            self.engine.set_threshold_parallel_processing(12.6)
        # Setting invalid threshold below 5 MB
        with self.assertRaises(ValueError):
            self.engine.set_threshold_parallel_processing(3.5)



    def test_set_threshold_parallel_processing_invalid_type(self):
        """
        Function for testing setting an invalid type for threshold for parallel processing.
        
        It ensures that setting an invalid input type, string, for the threshold 
        raises a TypeError.
        """
        #Setting invalid input type i.e. string 
        with self.assertRaises(TypeError):
            self.engine.set_threshold_parallel_processing("invalid")



    @patch("os.path.getsize")
    def test_calculate_file_size_existing_file(self, mock_getsize):
        """
        Function for testing calculating the size of an existing file.
        
        It uses mocking to test the calculate_file_size function 
        when provided with the path of an existing file.
        """
        mock_getsize.return_value = 1024
        file_size = self.engine.calculate_file_size("test_file.csv")
        self.assertEqual(file_size, 1024)



    @patch("os.path.getsize")
    def test_calculate_file_size_non_existing_file(self, mock_getsize):
        """
        Function for testing calculating the size of a non-existing file.

        It uses mocking to test the calculate_file_size function 
        when provided with the path of a non-existing file.
        """
        mock_getsize.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            self.engine.calculate_file_size("non_existing_file.csv")

            

    def test_calculate_matching_skills(self):
        """
        Function for testing calculating matching skills between required and present skills.
        
        It ensures the accuracy of calculate_matching_skills function to  calculate
        matching skills count and percentage.
        """
        matching_count, matching_percentage = self.engine.calculate_matching_skills("Python, React, MySQL", "Python, MySQL")
        self.assertEqual(matching_count, 2)
        self.assertEqual(round(matching_percentage,2), 66.67)

    

if __name__ == "__main__":
    unittest.main()
