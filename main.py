import pandas as pd
from src.recommendation_engine.recommendation import RecommendationEngine
from src.file_reader.read_files import *
from src.jobseeker_recommendation_engine.job_match_recommendation import *

#main function
def main():
    
    #reading jobs file
    path_file_jobs = 'csv_files/jobs.csv'
    path_file_jobseeker = 'csv_files/jobseekers.csv'
    obj_job_match = JobMatchRecommendationEngine(path_file_jobs,path_file_jobseeker)
    obj_job_match.set_threshold_parallel_processing(5)
    recommendations = obj_job_match.generate_recommendations()
    sorted_recommendation = obj_job_match.sort_recommendations(recommendations)
    print(sorted_recommendation)
  

if __name__ == "__main__":
    main()