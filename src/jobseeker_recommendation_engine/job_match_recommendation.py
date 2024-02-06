import pandas as pd
from ..recommendation_engine.recommendation import RecommendationEngine

class JobMatchRecommendationEngine(RecommendationEngine):

    def __init__(self, jobs_df, jobseekers_df,within_threshold):
        self.jobs_df = jobs_df
        self.jobseekers_df = jobseekers_df
        self.within_threshold =within_threshold

    def generate_recommendations(self):
        print ("Hey this is working!")
        recommendations = []

        if(self.within_threshold):
            for _, jobseeker_row in self.jobseekers_df.iterrows():
                for _,job_row in self.jobs_df.iterrows():
                    matching_skill_count, matching_skill_percent = RecommendationEngine.calculate_matching_skills(jobseeker_row['skills'], job_row['required_skills'])
                    if ( matching_skill_count >=1):
                        matched_job = {
                        'jobseeker_id': jobseeker_row['id'],
                        'jobseeker_name': jobseeker_row['name'],
                        'job_id': job_row['id'],
                        'job_title': job_row['title'],
                        'matching_skill_count': matching_skill_count,
                        'matching_skill_percent': round(matching_skill_percent,2)
                        }
                        recommendations.append(matched_job)
            return recommendations
          
    def sort_recommendations(self,recommendations):
        recommendations_df = pd.DataFrame(recommendations)
        sorted_recommendations = recommendations_df.sort_values(by=['jobseeker_id', 'matching_skill_percent'], ascending=[True, False])
        return sorted_recommendations