from abc import ABC, abstractmethod

class RecommendationEngine(ABC):
    
    @staticmethod
    def calculate_matching_skills(skills_required, set_skills_present):
        # Convert skills to sets
        set_skills_required = set(skills_required.split(", "))
        set_skills_present = set(set_skills_present.split(", "))

        # Calculate matching skills
        matching_skills = set_skills_required.intersection(set_skills_present)

         # Calculate matching skill count
        matching_skill_count = len(matching_skills)

        # Calculate matching skills percentage
        if len(set_skills_required) > 0:
            matched_skills_percentage = (matching_skill_count / len(set_skills_required)) * 100
        else:
            matched_skills_percentage = 0


        return matching_skill_count,matched_skills_percentage
    
    @abstractmethod
    def generate_recommendations():
        pass

    @abstractmethod
    def sort_recommendations(recommendations):
        pass