# ABC (Abstract Base Class) and abstractmethod from the abc module
from abc import ABC, abstractmethod
# os module for operating system functionalities
import os


class RecommendationEngine(ABC):
    """
    An abstract base class for recommendation engines.
    
    Attributes:
    - threshold_parallel_processing(float): Threshold for parallel processing in MB. Default is 5.00 GB.
                                             The main intention is to activate multiprocessing if the total size of 
                                             two CSV files is greater than the threshold. 
    """
    threshold_parallel_processing = 5.00  
    

    def set_threshold_parallel_processing(self, threshold_parallel_processing: float) -> None:
        """
        Function for setting the threshold for parallel processing.

        It allows to change the threshold within 5.00 to 10.00 GB.
        
        Parameters:
        - threshold_parallel_processing(float): Threshold for parallel processing in MB.
                                                
        """

        if not isinstance(threshold_parallel_processing, float):
            raise TypeError("Threshold must be a float")
        
        if 5.00<= threshold_parallel_processing <= 10.00: 
            self.threshold_parallel_processing = threshold_parallel_processing
        else:
            raise ValueError("Threshold for parallel processing should be between 5MB and 10 MB.")
    
        

    def calculate_file_size(self, path_file: str) -> int:
        """
        Function for calculating the size of the file in bytes.
        
        Parameters:
        - path_file(str): Path to the file.
        
        Returns:
        - int: Size of the file in bytes.
        """
        try:
            # Getting and returning the file size in bytes
            file_size_bytes = os.path.getsize(path_file)
            return file_size_bytes
        
        except FileNotFoundError:
            # Handling FileNotFoundError
            raise FileNotFoundError(f"File '{path_file}' not found. Please ensure the CSV file exists.")
        
        except Exception as ex:
            # Handling other unexpected errors
            raise Exception(f"An unexpected error occurred while calculating file size: {str(ex)}")
    


    @staticmethod
    def calculate_matching_skills(skills_required: str, set_skills_present: str) -> tuple:
        """
        Static method for calculating the total matching skills and percentage between the 
        required skills and the skills present.
        
        Parameters:
        - skills_required(str): Required skills.
        - set_skills_present(str): Skills present.
        
        Returns:
        - tuple: Tuple containing the matching skill count and the matching skills percentage.
        """
        try:
            # Converting the skills string into a set of unique skills to perform set operation 
            set_skills_required = set(skills_required.split(", "))
            set_skills_present = set(set_skills_present.split(", "))
            
            
            # Calculating matching skills using intersection
            matching_skills = set_skills_required.intersection(set_skills_present)
            # Calculating matching skill count
            matching_skill_count = len(matching_skills)

            # Calculating matching skills percentage
            if len(set_skills_required) > 0:
                matched_skills_percentage = (matching_skill_count / len(set_skills_required)) * 100
            else:
                matched_skills_percentage = 0

            return matching_skill_count,matched_skills_percentage
        
        except Exception as ex:
            # Handling unexpected errors
            raise Exception(f"Error calculating matching skills: {str(ex)}")

    

    @abstractmethod
    def generate_recommendations():
        """
        Abstract method for generating recommendations based on the implementation.
        """
        pass


    @abstractmethod
    def sort_recommendations(self, recommendations: list) -> list:
        """
        Abstract method for sorting recommendations based on certain criteria.
        
        Parameters:
        - recommendations(list): List of recommendations.
        
        Returns:
        - list: Sorted list of recommendations.
        """
        pass
