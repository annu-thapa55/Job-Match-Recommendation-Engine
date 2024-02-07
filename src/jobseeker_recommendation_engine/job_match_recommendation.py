import time
from typing import List, Dict
import pandas as pd
import multiprocessing as mp
from ..file_reader.read_files import File
from ..recommendation_engine.recommendation import RecommendationEngine

class JobMatchRecommendationEngine(RecommendationEngine):
    """
    A class to perform job matching recommendation for job seekers using sequential or parallel processing.
    """

    def __init__(self, path_file_jobs: str, path_file_jobseeker: str):
        """
        Constructor for class JobMatchRecommendationEngine.

        Parameters:
        - path_file_jobs (str): Path to the file containing job data.
        - path_file_jobseeker (str): Path to the file containing jobseeker data.
        """
        self.path_file_jobs = path_file_jobs
        self.path_file_jobseeker = path_file_jobseeker

    
    def calculate_total_size_files(self) -> float:
        """
        Function to calculate the total size of the job and job seeker files.

        Returns:
        - float: Total size of the files in gigabytes (GB).
        """
        try:
            size_first_file = self.calculate_file_size(self.path_file_jobs)
            size_second_file = self.calculate_file_size(self.path_file_jobseeker)
        
            total_size_files = size_first_file + size_second_file

            # Convert bytes to gigabytes (GB)
            file_size_gb = total_size_files / (1024 * 1024 * 1024)  

            print(f"Size of file: {file_size_gb:.2f} GB")
            return file_size_gb
        
        except Exception as ex:
            # Handle other unexpected errors
            raise Exception(f"An unexpected error occurred while calculating total file size: {str(ex)}")
        
    def sequential_processing(self) -> List[Dict]:
        """
        Function to perform sequential processing to match job seekers with available jobs.
        Especially used for the smaller size job and jobseeker files.

        The function iterates over job seekers and jobs sequentially to find matches
        based on required skills. It reads job and jobseeker data from CSV files,
        processes each job seeker against every job, and identifies matches based on
        shared skills.

        Returns:
        - List[Dict]: List of matched job recommendations.
        Each dictionary contains the following keys:
        - 'jobseeker_id': The ID of the job seeker.
        - 'jobseeker_name': The name of the job seeker.
        - 'job_id': The ID of the matched job.
        - 'job_title': The title of the matched job.
        - 'matching_skill_count': The count of matching skills between the job seeker and job.
        - 'matching_skill_percent': The percentage of matching skills between the job seeker and job.
            """
        recommendations = []

        # Initialize file reader objects for job and jobseeker data
        jobs_obj = File(self.path_file_jobs)
        jobseekers_obj = File(self.path_file_jobseeker)

        #read files as panda data frames
        jobs_df = jobs_obj.read_file()
        jobseekers_df = jobseekers_obj.read_file()

        # Iterate over each job seeker and jobs to find matches
        for _, jobseeker_row in jobseekers_df.iterrows():
            for _,job_row in jobs_df.iterrows():
                # Calculate matching skills between job seeker and job
                matching_skill_count, matching_skill_percent = RecommendationEngine.calculate_matching_skills(jobseeker_row['skills'], job_row['required_skills'])
               
                # Check if there is at least one matching skill
                if ( matching_skill_count >=1):
                    # Create a dictionary representing the matched job
                    matched_job = {
                    'jobseeker_id': jobseeker_row['id'],
                    'jobseeker_name': jobseeker_row['name'],
                    'job_id': job_row['id'],
                    'job_title': job_row['title'],
                    'matching_skill_count': matching_skill_count,
                    'matching_skill_percent': round(matching_skill_percent,2)
                    }
                    # Add the matched job to the recommendations list
                    recommendations.append(matched_job)
        return recommendations
    
    def get_pool_size(self) -> int:
        """
        Function to determine the optimal number of CPU cores to allocate for multiprocessing.
        
        Returns:
        - The number of CPU cores to use for multiprocessing.   

        """
        try:
            # Get the number of available CPU cores
            num_cores = mp.cpu_count()

            # Subtract a certain number of cores to leave some overhead for system tasks
            pool_size = max(num_cores - 1, 1)  

            # Ensure pool size is valid
            if pool_size <= 0:
                raise ValueError("Invalid pool size: Pool size must be greater than 0.")
            
            return pool_size
        
        except Exception as ex:
            # Handle unexpected errors
            print("An error occurred while calculating the pool size:", str(ex))
            # Default to using 1 CPU core if an error occurs
            return 1  


    def process_job_chunk(self, job_chunk: pd.DataFrame, jobseeker_row: pd.DataFrame) -> List[Dict]:
        """
        Function to process each job chunk to find matching jobs for a specific job seeker.
        It processes each row in the job chunk to determine if there are any matching jobs
        for the specified job seeker. It calculates the matching skill count and percentage for each job,
        and if the count is greater than or equal to 1, it adds the job to the list of recommendations.

        Parameters:
        - job_chunk(pd.DataFrame): A chunk of job data set.
        - jobseeker_row(pd.DataFrame): Information about the job seeker.

        Returns:
        - A list of dictionaries containing information about matching jobs for the specific job seeker.

        """ 
        try:  
            recommendations = []

            # Cleanse the job chunk to remove duplicates and null values
            job_chunk = File.cleanse_dataset(job_chunk)

            # Process each row in the job chunk
            for _, job_row in job_chunk.iterrows():
                # Calculate matching skills between a job and the job seeker
                matching_skill_count, matching_skill_percent = RecommendationEngine.calculate_matching_skills(jobseeker_row['skills'], job_row['required_skills'])

                # add the job to recommendations if there is at least one matching skill 
                if matching_skill_count >= 1:
                    matched_job = {
                        'jobseeker_id': jobseeker_row['id'],
                        'jobseeker_name': jobseeker_row['name'],
                        'job_id': job_row['id'],
                        'job_title': job_row['title'],
                        'matching_skill_count': matching_skill_count,
                        'matching_skill_percent': round(matching_skill_percent, 2)
                    }
                    recommendations.append(matched_job)
    
            return recommendations
        except Exception as ex:
            print("An unexpected error occurred while processing job chunk:", str(ex))
            return []

    def parallel_processing(self, jobseeker_chunk_size=1000, job_chunk_size=1000) -> List[Dict]:
        """
        Function to process job data in parallel to find matching jobs for job seekers.
        
        It processes job data in parallel using multiprocessing to find matching jobs for job seekers.
        It reads job seeker data and divides it into chunks, then for each chunk, it reads job data in chunks as well.
        It then applies the process_job_chunk function to each combination of job chunk and job seeker, in parallel.

        Parameters:
        - jobseeker_chunk_size: The size of each chunk of job seeker data to process.
        - job_chunk_size: The size of each chunk of job data to process.

        Returns:
        - A list of dictionaries containing information about matching jobs between jobseekers and jobs.

        """
        try:
            recommendations = []

            # Get pool size 
            pool_size = self.get_pool_size()
            pool = mp.Pool(pool_size)

            # Process each chunk of job seeker data
            for job_seekers_chunk in pd.read_csv(self.path_file_jobseeker, chunksize=jobseeker_chunk_size):
                # Iterate over each job seeker in the chunk
                for _, jobseeker_row in job_seekers_chunk.iterrows():
                    # Read job data in chunks and process each chunk in parallel for current job seeker              
                    job_recommendations_per_seeker = pool.starmap(self.process_job_chunk, [(job_chunk, jobseeker_row) for job_chunk in pd.read_csv(self.path_file_jobs, chunksize=job_chunk_size)])     
                    
                    for recommend in job_recommendations_per_seeker:
                        # Add recommendations for current job seeker
                        recommendations.extend(recommend)

            # Close the multiprocessing pool and wait until all processes are finished.
            pool.close()
            pool.join()

            return recommendations
        
        except Exception as ex:
            # Handle unexpected errors
            print(f"An unexpected error occurred during parallel processing: {ex}")
            return []

    def generate_recommendations(self) -> List[Dict]:
        """
        Function to generate recommendations based on the size of files.
        It calculates the total size of the files and determines whether to use sequential or parallel
        processing as per the threshold for parallel processing value. Then the recommendations
        is generated accordingly.

        Returns:
        - recommendations: A list of dictionaries containing recommended job matches.

        """
        try:
            # Calculate the total size of the jobs and jobseeker files
            total_size_files = self.calculate_total_size_files()
            
            # Determine the processing method based on file size
            if (total_size_files < self.threshold_parallel_processing):
                # Activate sequential processing for small files
                recommendations= self.sequential_processing()
            else:
                # Activate parallel processing for large files
                recommendations= self.parallel_processing()
            
            return recommendations
        # Handle FileNotFoundError
        except FileNotFoundError as err:
            raise ValueError(f"Error: {err.strerror}. Please ensure the CSV files exist.")
        
        # Handle EmptyDataError
        except pd.errors.EmptyDataError:
            raise ValueError("Error: CSV files are empty.")
        
        # Handle ParserError
        except pd.errors.ParserError:
            raise ValueError("Error: Failed to parse CSV files. Please check the file format.")
        
        # Handle other unexpected errors
        except Exception as ex:
            raise ValueError(f"An unexpected error occurred: {str(ex)}")

          
    def sort_recommendations(self, recommendations: List[Dict]) -> pd.DataFrame:
        """
        Function to sort recommendations based on jobseeker ID and matching skill percentage.
        It takes a list of recommendation dictionaries and sorts them based on jobseeker ID
        in ascending order and matching skill percentage in descending order.

        Parameters:
        - recommendations: A list of dictionaries containing recommended job matches.

        Returns:
        - sorted_recommendations(pd.DataFrame): A pandas DataFrame containing sorted recommendations.
        """  
        try:
            # Check if the recommendations list is empty
            if not recommendations:
                raise ValueError("Recommendations list is empty.")
            
            # Convert recommendations to a pandas DataFrame
            recommendations_df = pd.DataFrame(recommendations)   
            
            # Sort recommendations by jobseeker ID and matching skill percentage
            sorted_recommendations = recommendations_df.sort_values(by=['jobseeker_id', 'matching_skill_percent'], ascending=[True, False])
            
            return sorted_recommendations
        
        # Handle  unexpected errors
        except Exception as ex:
            raise ValueError(f"An unexpected error occurred during sorting: {str(ex)}")
            