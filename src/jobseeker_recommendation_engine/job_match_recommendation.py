from typing import List, Dict
import pandas as pd
import multiprocessing as mp
from ..file_reader.read_files import File
from ..recommendation_engine.recommendation import RecommendationEngine

class JobMatchRecommendationEngine(RecommendationEngine):
    """
    A class for performing job matching recommendation to job seekers using sequential or parallel processing.

    Attributes:
    - path_file_jobs(str): Path to the file containing jobs data.
    - path_file_jobseeker(str): Path to the file containing jobseekers data.
    """

    def __init__(self, path_file_jobs: str, path_file_jobseeker: str):
        """
        Constructor for class JobMatchRecommendationEngine.

        Parameters:
        - path_file_jobs(str): Path to the file containing jobs data.
        - path_file_jobseeker(str): Path to the file containing jobseekers data.
        """
        self.path_file_jobs = path_file_jobs
        self.path_file_jobseeker = path_file_jobseeker

    
    def calculate_total_size_files(self) -> float:
        """
        Function for calculating the total size of the job and job seeker files in Giga Byte.

        Returns:
        - float: Total size of the files in Giga Bytes(GB).
        """
        try:
            # Calculating file size in bytes
            size_first_file = self.calculate_file_size(self.path_file_jobs)
            size_second_file = self.calculate_file_size(self.path_file_jobseeker)

            # Calculating total size of two files
            total_size_files = size_first_file + size_second_file

            # Converting bytes to Giga Bytes(GB)
            file_size_gb = total_size_files / (1024 * 1024 * 1024)  

            
            # Returning file size in GB
            return file_size_gb
        
        except Exception as ex:
            # Handling unexpected errors
            raise Exception(f"An unexpected error occurred while calculating total file size: {str(ex)}")
        
    def sequential_processing(self) -> List[Dict]:
        """
        Function for performing sequential processing to match job seekers with available jobs,specifically 
        used for the smaller size job and jobseeker files.

        It iterates over job seekers and jobs sequentially to find matches based on required skills. 
        It reads job and jobseeker data from CSV files, processes each job seeker against every available jobs, 
        and calculates matches based on common skills.

        Returns:
        - List[Dict]: List of matched job recommendations.
        Each dictionary contains the following keys:
        - 'jobseeker_id': ID of the job seeker.
        - 'jobseeker_name': Name of the job seeker.
        - 'job_id': ID of the matched job.
        - 'job_title': Title of the matched job.
        - 'matching_skill_count': Count of matching skills between the job seeker and job.
        - 'matching_skill_percent': Percentage of matching skills between the job seeker and job.
            """
        
        # Storing matched jobs as recommendations
        recommendations = []

        # Initializing file reader objects for job and jobseeker data
        jobs_obj = File(self.path_file_jobs)
        jobseekers_obj = File(self.path_file_jobseeker)

        # Reading files as panda data frames
        jobs_df = jobs_obj.read_file()
        jobseekers_df = jobseekers_obj.read_file()

        # Iterating over each job seeker 
        for _, jobseeker_row in jobseekers_df.iterrows():
            # Iterating over each job for the current job seeker
            for _,job_row in jobs_df.iterrows():
                # Calculating matching skills between job seeker and job
                matching_skill_count, matching_skill_percent = RecommendationEngine.calculate_matching_skills(jobseeker_row['skills'], job_row['required_skills'])
               
                # Checking the presence of at least one matching skill
                if ( matching_skill_count >=1):
                    # Creating a dictionary representing the matched job
                    matched_job = {
                    'jobseeker_id': jobseeker_row['id'],
                    'jobseeker_name': jobseeker_row['name'],
                    'job_id': job_row['id'],
                    'job_title': job_row['title'],
                    'matching_skill_count': matching_skill_count,
                    'matching_skill_percent': round(matching_skill_percent,2)
                    }
                    # Adding the matched job to the recommendations list
                    recommendations.append(matched_job)
        
        # Returning matched jobs as recommendations
        return recommendations
    
    def get_pool_size(self) -> int:
        """
        Function for determining the optimal number of CPU cores to allocate for multiprocessing.
        
        The main intention is to dynamically create a pool of worker processes for parallel execution
        of tasks based on the CPU cores.

        Returns:
        - int: Optimum number of worker processes for multiprocessing.   

        """
        try:
            # Getting the number of available CPU cores
            num_cores = mp.cpu_count()

            # Subtracting 1 CPU core to leave some overhead for system tasks. Setting Default value as 1
            pool_size = max(num_cores - 1, 1)  
            
            # Returning number of worker processes
            return pool_size
        
        except Exception as ex:
            # Handling unexpected errors
            raise ValueError("An error occurred while calculating the pool size:", str(ex))  


    def process_job_chunk(self, job_chunk: pd.DataFrame, jobseeker_row: pd.DataFrame) -> List[Dict]:
        """
        Function for processing each job chunk to find matching jobs for a specific job seeker.
        
        It processes each row in the job chunk for determining whether there are any matching jobs
        for the specified job seeker. For that, it calculates the matching skill count and percentage for each job,
        and adds the job to the list of recommendations if the matched jon is greater than or equal to 1.

        Parameters:
        - job_chunk(pd.DataFrame): One chunk of job data set.
        - jobseeker_row(pd.DataFrame): Information about one job seeker.

        Returns:
        - List[Dict]: List of dictionaries containing information of matching jobs for the specific job seeker.

        """ 
        try:  
            # Storing matched jobs as recommendations
            recommendations = []

            # Cleansing the job chunk to remove duplicates and null values
            job_chunk = File.cleanse_dataset(job_chunk)

            # Processing each job  in the job chunk
            for _, job_row in job_chunk.iterrows():
                # Calculating matching skills between a job and the job seeker
                matching_skill_count, matching_skill_percent = RecommendationEngine.calculate_matching_skills(str(jobseeker_row['skills']), str(job_row['required_skills']))
                # Adding the job to recommendations if there is at least one matching skill 
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
            
      
            # Returning matched jobs as recommendations
            return recommendations
        
        except Exception as ex:
            # Handling unexpected error
            raise ValueError("An unexpected error occurred while processing job chunk:", str(ex))
            

    def parallel_processing(self, jobseeker_chunk_size=1000, job_chunk_size=1000) -> List[Dict]:
        """
        Function for processing job data using multiprocessing to find matching jobs for job seekers.
        
        It reads job seeker data and divides it into chunks. Then for each job seeker data chunk, 
        job data in read in chunks as well. Then the process_job_chunk function is applied to 
        each combination of job chunk and job seeker in parallel.

        Parameters:
        - jobseeker_chunk_size(int): Size of each chunk of job seeker data to process. Set to 1000 rows by default.
        - job_chunk_size(int): Size of each chunk of job data to process. Set to 1000 rows by defaul.

        Returns:
        - List[Dict]: List of dictionaries containing information about matching jobs between jobseekers and jobs.

        """
        try:
            # Storing matched jobs as recommendations
            recommendations = []

            # Getting pool size to create pool of worker processes
            pool_size = self.get_pool_size()
            pool = mp.Pool(pool_size)

            # Processing each chunk of job seeker data
            for job_seekers_chunk in pd.read_csv(self.path_file_jobseeker, chunksize=jobseeker_chunk_size):
                # Cleansing the jobseekers chunk to remove duplicates and null values
                job_seekers_chunk = File.cleanse_dataset(job_seekers_chunk)
                # Iterating over each job seeker in the chunk
                for _, jobseeker_row in job_seekers_chunk.iterrows():
                    # Reading job data in chunks and process each chunk in parallel for current job seeker              
                    job_recommendations_per_seeker = pool.starmap(self.process_job_chunk, [(job_chunk, jobseeker_row) for job_chunk in pd.read_csv(self.path_file_jobs, chunksize=job_chunk_size)])     
                    
                    # Iterating through each job recommendation for current job seeker and add to recommendations list
                    for recommend in job_recommendations_per_seeker:
                        recommendations.extend(recommend)

            # Closing the multiprocessing pool and wait until all processes are finished.
            pool.close()
            pool.join()

            # Returning matched jobs as recommendations
            return recommendations
        
        except Exception as ex:
            # Handling unexpected errors
            raise ValueError(f"An unexpected error occurred during parallel processing: {ex}")


    def generate_recommendations(self) -> List[Dict]:
        """
        Function for generating recommendations based on the size of files.
        
        It calculates the total size of the job and jobseeker files and determines whether to use sequential or parallel
        processing as per the set threshold for parallel processing value. The job recommendations for each job seeker
        is generated accordingly.

        Returns:
        - List[Dict]: List of dictionaries containing recommended job matches.

        """
        try:
            # Calculating the total size of the jobs and jobseeker files
            total_size_files = self.calculate_total_size_files()
            
            # Determining the processing method based on file size
            if (round(total_size_files,2) < self.threshold_parallel_processing):
                # Activating sequential processing for small-sized files
                recommendations= self.sequential_processing()
            else:
                # Activating parallel processing for large-sized files
                recommendations= self.parallel_processing()
            
            # Returning matched jobs as recommendations
            return recommendations      
        
        # Handling unexpected errors
        except Exception as ex:
            raise ValueError(f"An unexpected error occurred: {str(ex)}")

          
    def sort_recommendations(self, recommendations: List[Dict]) -> pd.DataFrame:
        """
        Function for sorting recommendations based on jobseeker ID and matching skill percentage.
        
        It takes a list of recommendation dictionaries and sorts them based on jobseeker ID
        in ascending order and matching skill percentage in descending order.

        Parameters:
        - recommendations(List[Dict]): List of dictionaries containing recommended job matches.

        Returns:
        - pd.DataFrame: Pandas DataFrame containing sorted recommendations.
        """  
        try:
            # Checking if the recommendations list is empty
            if not recommendations:
                raise ValueError("Recommendation list is empty!")
            
            # Converting recommendations to a pandas DataFrame
            recommendations_df = pd.DataFrame(recommendations)   
            
            # Sorting recommendations by jobseeker ID and matching skill percentage
            sorted_recommendations = recommendations_df.sort_values(by=['jobseeker_id', 'matching_skill_percent'], ascending=[True, False])
            
            # Returning sorterd recommendations
            return sorted_recommendations
        
        except Exception as ex:
            # Handling  unexpected errors
            raise ValueError(f"An unexpected error occurred during sorting: {str(ex)}")
            