# csv module for reading and writing CSV files
import csv
# unittest module for writing and running unit tests
import unittest
# pandas module for data manipulation and analysis
import pandas as pd
# os module for operating system functionalities
import os
# multiprocessing module for parallel processing
import multiprocessing as mp
# patch function from unittest.mock module for mocking objects during testing
from unittest.mock import patch
# custom JobMatchRecommendationEngine class for testing its functions
from src.jobseeker_recommendation_engine.job_match_recommendation import JobMatchRecommendationEngine


class TestJobMatchRecommendationEngineClass(unittest.TestCase):
    """
    Test suite for validating the functionality of the JobMatchRecommendationEngine class.

    This test suite class contains tests for various functions of the JobMatchRecommendationEngine 
    class to ensure its proper functioning under different scenarios and conditions.
    """    

    def setUp(self):
        """
        Function for setting up the test cases.

        It is called before performing each test case so as to set up necessary
        resources for testing. 
        """
        # Sampling data files for testing
        self.jobs_file_path = 'jobs_sample.csv'
        self.jobseeker_file_path = 'jobseekers_sample.csv'

        # Sampling data for jobs file
        job_fields = ['id', 'title', 'required_skills']
        # data rows of csv file
        job_rows = [['1', 'Software Engineer', 'Python, R'],
                ['2', 'Data Scientist', 'Python, Java'],
                ['3', 'Web Developer', 'Docker, React']]
        with open(self.jobs_file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            # writing the job fields
            csvwriter.writerow(job_fields)

            # writing the job rows
            csvwriter.writerows(job_rows)

        # Sampling data for job seekers file
        jobseeker_fields = ['id', 'name', 'skills']
        # data rows of csv file
        jobseeker_rows = [['1', 'Michelle', 'Python, SQL'],
                ['2', 'Andrew', 'Java, Python']] 
        
        with open(self.jobseeker_file_path, 'w',newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            # writing the job fields
            csvwriter.writerow(jobseeker_fields)

            # writing the job rows
            csvwriter.writerows(jobseeker_rows)


       
    def tearDown(self):
        """
        Function for cleaning up after performing each test case.

        It is called after each test case for removing any resources created during testing.
        """
        # Removing sample data files  
        os.remove(self.jobs_file_path)
        os.remove(self.jobseeker_file_path)



    @patch("os.path.getsize")
    def test_calculate_total_size_files(self, mock_getsize):
        """
        Function for testing calculating the total size of job and jobseeker files.

        It ensures the accurate calculation of the total size of job and jobseeker files in Giga Bytes(GB).
        """
        # Mocking file sizes in bytes
        mock_getsize.side_effect = [1024, 2048]  
        engine = JobMatchRecommendationEngine(self.jobs_file_path, self.jobseeker_file_path)
        total_size = engine.calculate_total_size_files()
        # Converting bytes to GB for comparison
        self.assertAlmostEqual(round(total_size,2), round(0.0029296875,2))  



    def test_sequential_processing(self):
        """
        Function for testing the accuracy of sequential_processing function.

        It ensures that the job recommendation is accurately done based on the skills matched
        between the job seeker and jobs when performing sequential processing
        """
        engine = JobMatchRecommendationEngine(self.jobs_file_path, self.jobseeker_file_path)
        recommendations = engine.sequential_processing()       

        # Checking if recommendations are not empty
        self.assertTrue(recommendations)
       
        # Checking the correctness of recommendations
        # Two job seekers should have Four matching jobs. The job "Web Developer" should have no matching. Hence 4 recommendations
        self.assertEqual(len(recommendations), 4)  
        self.assertEqual(recommendations[0]['jobseeker_id'], 1)
        self.assertEqual(recommendations[0]['jobseeker_name'], 'Michelle')
        self.assertEqual(recommendations[0]['job_id'], 1)
        self.assertEqual(recommendations[0]['job_title'], 'Software Engineer')
        self.assertEqual(recommendations[0]['matching_skill_count'], 1)  # Number of matching skills
        self.assertAlmostEqual(recommendations[0]['matching_skill_percent'], 50.0)  # Matching skill percentage



    def test_get_pool_size_valid(self):
        """
        Function for testing the pool size calculation with valid CPU count.

        It ensures that the pool size for the multiprocessing is set as per the CPU
        count.
        """
        # Creating a JobMatchRecommendationEngine instance
        engine = JobMatchRecommendationEngine(self.jobs_file_path, self.jobseeker_file_path)

        # Setting the expected pool size based on the CPU count of the system
        expected_pool_size = max(mp.cpu_count() - 1, 1)  

        # Calling the get_pool_size method
        actual_pool_size = engine.get_pool_size()

        # Checking whether the actual pool size matches the expected pool size or not
        self.assertEqual(actual_pool_size, expected_pool_size)



    def test_get_pool_size_default(self):
        """
        Function for testing the pool size calculation with invalid CPU count.

        It ensures that the pool size for the multiprocessing is set as 1 by default
        """
        # Creating a JobMatchRecommendationEngine instance
        engine = JobMatchRecommendationEngine(self.jobs_file_path, self.jobseeker_file_path)

        # Setting the CPU count to 0 to verify whether the default value of 1 is returned as pool size or not
        with patch('multiprocessing.cpu_count', return_value=0):
            # Checking if the pool size is 1
            self.assertEqual(engine.get_pool_size(), 1)



    def test_parallel_processing(self):
        """
        Function for testing the parallel processing of job matching.

        It ensures that the parallel processing function returns the matched job with the 
        recommendation keys as 'jobseeker_id', 'jobseeker_name', 'job_id', 'job_title', 'matching_skill_count', 'matching_skill_percent'.
        """
       
        # Creating JobMatchRecommendationEngine instance
        engine = JobMatchRecommendationEngine(self.jobs_file_path, self.jobseeker_file_path)

        # Executing parallel processing
        recommendations = engine.parallel_processing()

        # Asserting that recommendations is a list
        self.assertIsInstance(recommendations, list)

        # Asserting that each recommendation is a dictionary
        for recommendation in recommendations:
            self.assertIsInstance(recommendation, dict)

        # Asserting that recommendations list contain the expected keys
        expected_keys = ['jobseeker_id', 'jobseeker_name', 'job_id', 'job_title', 'matching_skill_count', 'matching_skill_percent']
        for recommendation in recommendations:
            self.assertTrue(all(key in recommendation for key in expected_keys))



    def test_generate_recommendations(self):
        """
        Function for testing generation of recommendations.

        It ensures that recommendation generated, irrespective of sequential or multiprocessing, the list of matched jobs has the 
        keys as 'jobseeker_id', 'jobseeker_name', 'job_id', 'job_title', 'matching_skill_count', 'matching_skill_percent'.
        """
        # Instantiating JobMatchRecommendationEngine
        engine = JobMatchRecommendationEngine(self.jobs_file_path, self.jobseeker_file_path)

        # Executing generate recommendations
        recommendations = engine.generate_recommendations()

        # Asserting that recommendations is a list
        self.assertIsInstance(recommendations, list)

        # Asserting that each recommendation is a dictionary
        for recommendation in recommendations:
            self.assertIsInstance(recommendation, dict)

        # Asserting that recommendations contain the expected keys
        expected_keys = ['jobseeker_id', 'jobseeker_name', 'job_id', 'job_title', 'matching_skill_count', 'matching_skill_percent']
        for recommendation in recommendations:
            self.assertTrue(all(key in recommendation for key in expected_keys))



    def test_sort_recommendations(self):
        """
        Function for testing sorting recommendations.

        It ensures that the job recommendations (output) is sorted first by jobseeker ID 
        and then by the percentage of matching skills in descending order (so that jobs with the highest percentage of matching skills are listed first). 
        If two jobs have the same matching skill percentage, they are sorted by job ID in ascending order.
        """
        # Instantiating JobMatchRecommendationEngine
        engine = JobMatchRecommendationEngine(self.jobs_file_path, self.jobseeker_file_path)

        # Sampling recommendations
        recommendations = [
            {'jobseeker_id': 1, 'jobseeker_name': 'Michelle', 'job_id': 1, 'job_title': 'Software Engineer', 'matching_skill_count': 2, 'matching_skill_percent': 80.0},
            {'jobseeker_id': 1, 'jobseeker_name': 'Michelle', 'job_id': 2, 'job_title': 'Data Scientist', 'matching_skill_count': 2, 'matching_skill_percent': 75.0},
            {'jobseeker_id': 2, 'jobseeker_name': 'Andrew', 'job_id': 1, 'job_title': 'Software Engineer', 'matching_skill_count': 2, 'matching_skill_percent': 70.0},
            {'jobseeker_id': 2, 'jobseeker_name': 'Andrew', 'job_id': 2, 'job_title': 'Web Developer', 'matching_skill_count': 1, 'matching_skill_percent': 50.0},
            {'jobseeker_id': 2, 'jobseeker_name': 'Andrew', 'job_id': 3, 'job_title': 'Web Developer', 'matching_skill_count': 1, 'matching_skill_percent': 50.0}
        ]

        # Sorting recommendations
        sorted_recommendations = engine.sort_recommendations(recommendations)

        # Asserting  that sorted_recommendations is a Pandas DataFrame
        self.assertIsInstance(sorted_recommendations, pd.DataFrame)

        # Asserting that the DataFrame has the correct columns
        expected_columns = ['jobseeker_id', 'jobseeker_name', 'job_id', 'job_title', 'matching_skill_count', 'matching_skill_percent']
        self.assertListEqual(list(sorted_recommendations.columns), expected_columns)

        # Asserting that list is sorted first by jobseeker ID 
        expected_order = [1, 1, 2, 2,2]
        self.assertListEqual(list(sorted_recommendations['jobseeker_id']), expected_order)

        
        # Asserting that the DataFrame is sorted by matching_skill_percent in descending order within each jobseeker_id
        self.assertTrue(all(sorted_recommendations.groupby('jobseeker_id')['matching_skill_percent'].apply(lambda x: x.is_monotonic_decreasing)))

        # Asserting that the DataFrame is sorted correctly if two jobs have the same matching skill percentage, they should be sorted by job ID in ascending order.
        expected_order = [1, 2, 1, 2,3]
        self.assertListEqual(list(sorted_recommendations['job_id']), expected_order)


if __name__ == '__main__':
    unittest.main()
