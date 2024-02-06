import os
import psutil
import pandas as pd

class File:
    #constructor
    def __init__(self, path_file):
        self.path_file = path_file
        self.threshold_percentage = 0.3  # Default threshold percentage

    def set_threshold_percentage(self, threshold_percentage):
        """Set the threshold percentage."""
        if 0 < threshold_percentage <= 1:  # Ensure threshold percentage is between 0 and 1
            self.threshold_percentage = threshold_percentage
        else:
            raise ValueError("Threshold percentage should be between 0 and 1.")

    def check_threshold(self):
        """Checks if the size of the file is within the threshold or not"""
        total_memory_gb = psutil.virtual_memory().total / (1024 * 1024 * 1024)
        #print(f"total_memory_gb: {total_memory_gb:.2f} GB")
       
        file_size_gb = self.check_file_size()
        #print(f"File Size: {file_size_gb:.2f} GB")
        
        if (file_size_gb <= self.threshold_percentage *  total_memory_gb):
            return True
        else:
            return False
    
    #function to check the size of file.
    def check_file_size(self):
        """Check the size of the file in GB."""
        file_size_gb = os.path.getsize(self.path_file) / (1024 * 1024 * 1024)
        return file_size_gb
    


    #function for data wrangling
    def  cleanse_dataset(self, data_set:pd.DataFrame) -> pd.DataFrame:

        #remove duplicates and null values
        data_set = data_set.drop_duplicates().dropna()
        return data_set

    #function to read csv files
    def read_file(self):
        """Load the file if its size is within the calculated threshold."""
        
        try:
            within_threshold = self.check_threshold() 
            if(within_threshold):
                file = pd.read_csv(self.path_file)     
        
            else:
                print("File size exceeds the threshold. File not loaded.")
                        
        except FileNotFoundError as er:
            print(F"Error: {er.strerror}. Please ensure the csv files exist.")
            return
        except pd.errors.EmptyDataError:
            print("Error: csv files are empty.")
            return
        except pd.errors.ParserError:
            print("Error: Failed to parse csv files. Please check the file format")
            return
        except Exception as ex:
            print(F" An unexpected error occured: {str(ex)}")
            return
            
        # cleanse dataset 
        file = self.cleanse_dataset(file)

        #return clean datasets
        return within_threshold, file
   



