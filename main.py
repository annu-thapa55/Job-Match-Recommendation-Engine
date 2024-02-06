import pandas as pd
from src.file_reader.read_files import *
from src.jobseeker_recommendation_engine.job_match_recommendation import *

#main function
def main():
    
    #reading jobs file
    path_file_jobs = 'csv_files/jobs.csv'
    jobs= File(path_file_jobs)
    within_threshold, jobs_cleansed = jobs.read_file()
    print("After Jobs")
    print(within_threshold)
    print(jobs_cleansed)

    #reading jobseekers file
    path_second_file = 'csv_files/jobseekers.csv'
    jobseeker= File(path_second_file)
    within_threshold,jobseeker_cleansed = jobseeker.read_file()
    print("After Job Seekers")
    print(within_threshold)
    print(jobseeker_cleansed)

    recommendations_obj = JobMatchRecommendationEngine(jobs_cleansed,jobseeker_cleansed,within_threshold)
    recommendations = recommendations_obj.generate_recommendations()
    sorted_recommendation = recommendations_obj.sort_recommendations(recommendations)
    print(sorted_recommendation)


if __name__ == "__main__":
    main()