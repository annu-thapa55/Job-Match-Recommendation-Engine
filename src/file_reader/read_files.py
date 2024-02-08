import pandas as pd

class File:

    """
    A class for handling file operations such as reading and cleansing CSV files.
    
    Attributes:
    - path_file(str): Path of the CSV file.
    """

    def __init__(self,path_file:str):
        """
        Constructor for class File.
        
        Parameters:
        - path_file(str):  Path to the CSV file.
        """
        self.path_file = path_file
        
 
    @staticmethod
    def  cleanse_dataset(data_set:pd.DataFrame) -> pd.DataFrame:
        """
        Static method for performing data wrangling.
        
        It cleans the dataset by removing duplicates and null values.
        
        Parameters:
        - data_set(pd.DataFrame): The dataset of type DataFrame to be cleansed.
        
        Returns:
        - pd.DataFrame: Cleansed dataset of type DataFrame.
        """
        # Removing duplicates and null values
        data_set = data_set.drop_duplicates().dropna()
        return data_set


    def read_file(self) -> pd.DataFrame:
        """
        Function for reading and cleansing CSV files.
        
        It loads the CSV file and performs data cleansing if no errors occur.
        
        Returns:
        - pd.DataFrame: Cleansed dataset of type DataFrame.
        """
        try:
            # Attempting to read the CSV file
            file = pd.read_csv(self.path_file)

        except FileNotFoundError as er:
            # Handling FileNotFoundError
            raise ValueError(F"Error: {er.strerror}. Please ensure the CSV file exists.")
        
        except pd.errors.EmptyDataError:
            # Handling EmptyDataError
            raise ValueError("Error: CSV file is empty.")          
        
        except pd.errors.ParserError:
            # Handling ParserError
            raise ValueError("Error: Failed to parse CSV file. Please check the file format.")
        
        except Exception as ex:
            # Handling other unexpected errors
            raise ValueError(F"An unexpected error occurred: {str(ex)}")
            
        # Cleansing the dataset
        file = self.cleanse_dataset(file)

        # Returning the cleansed dataset
        return file

   



