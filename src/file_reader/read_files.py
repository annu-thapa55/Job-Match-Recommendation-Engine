import pandas as pd

class File:

    """
    A class to handle file operations such as reading and cleansing CSV files.
    
    Attributes:
    - path_file (str): The path to the CSV file.
    """

    def __init__(self,path_file:str):
        """
        Constructor for class File.
        
        Parameters:
        - path_file (str):  the path to the CSV file.
        """
        self.path_file = path_file
        
 
    @staticmethod
    def  cleanse_dataset(data_set:pd.DataFrame) -> pd.DataFrame:
        """
        Static method for data wrangling.
        
        Cleans the dataset by removing duplicates and null values.
        
        Parameters:
        - data_set (pd.DataFrame): The dataset of type DataFrame to be cleansed.
        
        Returns:
        - pd.DataFrame: The cleansed dataset of type DataFrame.
        """
        #remove duplicates and null values
        data_set = data_set.drop_duplicates().dropna()
        return data_set


    def read_file(self) -> pd.DataFrame:
        """
        Function to read and cleanse CSV files.
        
        Loads the CSV file and performs data cleansing if no errors occur.
        
        Returns:
        - pd.DataFrame or None: The cleansed dataset if successful, else None.
        """
        try:
            # Attempt to read the CSV file
            file = pd.read_csv(self.path_file)

        except FileNotFoundError as er:
            # Handle FileNotFoundError
            raise ValueError(F"Error: {er.strerror}. Please ensure the CSV file exists.")
        
        except pd.errors.EmptyDataError:
            # Handle EmptyDataError
            raise ValueError("Error: CSV file is empty.")
          
        
        except pd.errors.ParserError:
            # Handle ParserError
            raise ValueError("Error: Failed to parse CSV file. Please check the file format.")
        
        except Exception as ex:
            # Handle other unexpected errors
            raise ValueError(F"An unexpected error occurred: {str(ex)}")
            
        # Cleanse the dataset
        file = self.cleanse_dataset(file)

        # Return the cleansed dataset
        return file

   



