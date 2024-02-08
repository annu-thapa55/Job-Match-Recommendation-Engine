REM Running the main function to display output
python main.py

REM Running the test cases for the functionalities in read_files.py, 
REM job_match_recommendation.py, and recommedation.py files.
python -m unittest tests.test_read_files
python -m unittest tests.test_job_match_recommendation
python -m unittest tests.test_recommendation

REM Pausing until the user presses any key
pause