from abc import ABC, abstractmethod
import os

class RecommendationEngine(ABC):
    """
    An abstract base class for recommendation engines.
    
    Attributes:
    - threshold_parallel_processing (float): The threshold for parallel processing in MB. Default is 5.00 MB.
                                             The main intention is to activate multiprocessing if the size of two CSV files 
                                             is greater than the threshold. 
    """
    threshold_parallel_processing = 5.00  

    def set_threshold_parallel_processing(self, threshold_parallel_processing: float) -> None:
        """
        Function to set the threshold for parallel processing.
        
        Parameters:
        - threshold_parallel_processing (float): The threshold for parallel processing in MB.
                                                 Must be between 5.00 and 10.00 MB.
        """
        if 5.00<= threshold_parallel_processing <= 10.00: 
            self.threshold_percentage = threshold_parallel_processing
        else:
            raise ValueError("Threshold for parallel processing should be between 5MB and 10 MB.")
    

    def calculate_file_size(self, path_file: str) -> int:
        """
        Function to calculate the size of the file in bytes.
        
        Parameters:
        - path_file (str): The path to the file.
        
        Returns:
        - int: The size of the file in bytes.
        """
        try:
            file_size_bytes = os.path.getsize(path_file)
            return file_size_bytes
        
        except FileNotFoundError:
            # Handle FileNotFoundError
            raise FileNotFoundError(f"File '{path_file}' not found. Please ensure the CSV file exists.")
        
        except Exception as ex:
            # Handle other unexpected errors
            raise Exception(f"An unexpected error occurred while calculating file size: {str(ex)}")
    

    @staticmethod
    def calculate_matching_skills(skills_required: str, set_skills_present: str) -> tuple:
        """
        Function to calculate the total matching skills and percentage between the 
        required skills and the skills present.
        
        Parameters:
        - skills_required (str): The required skills.
        - set_skills_present (str): The skills present.
        
        Returns:
        - tuple: A tuple containing the matching skill count and the matching skills percentage.
        """
        try:
            # Convert the skills string into a set of unique skills to perform set operation 
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
        
        except Exception as ex:
            # Handle other unexpected errors
            raise Exception(f"Error calculating matching skills: {str(ex)}")

    
    @abstractmethod
    def generate_recommendations():
        """
        Abstract function to generate recommendations based on the implementation.
        """
        pass

    @abstractmethod
    def sort_recommendations(self, recommendations: list) -> list:
        """
        Abstract function to sort recommendations based on certain criteria.
        
        Parameters:
        - recommendations (list): A list of recommendations.
        
        Returns:
        - list: A sorted list of recommendations.
        """
        pass