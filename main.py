# custom read_files functionalities 
from src.file_reader.read_files import *
# custom job_match_recommendation functionalities 
from src.jobseeker_recommendation_engine.job_match_recommendation import *

# Main function
def main():
    
    # Reading jobs file
    path_file_jobs = 'csv_files/jobs.csv'
    path_file_jobseeker = 'csv_files/jobseekers.csv'

    # Creating an object of JobMatchRecommendationEngine
    obj_job_match = JobMatchRecommendationEngine(path_file_jobs,path_file_jobseeker)
    
    # Setting the threshold for parallel processing as 7 MB
    obj_job_match.set_threshold_parallel_processing(7.0)
    
    # Getting the generated job recommendations
    recommendations = obj_job_match.generate_recommendations()

    # Sorting the job recommendations
    sorted_recommendation = obj_job_match.sort_recommendations(recommendations)
    
    # Printing the sorted recommendation as an output 
    print(sorted_recommendation)

if __name__ == "__main__":
    main()