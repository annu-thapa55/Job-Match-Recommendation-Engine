# Job Match Recommendation Engine
A basic recommendation engine for a job-matching platform. The main target of the engine is to suggest jobs to job seekers based on their skills and the required skills for each job.

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#description">Description</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
    </li>
    <li><a href="#output">Output</a></li>
    <li>
      <a href="#evaluation">Evaluation</a>
    </li>
  </ol>
</details>

## Description
The module for the job match recommendation engine reads two CSV files: one for available jobs and another for job seekers and generates a list of recommendations for each job seeker. The recommendation is made by finding the common skills between the skills required by a job and the skills possessed by a job seeker. Each recommendation includes jobseeker_id, jobseeker_name, job_id, job_title, matching_skill_count, matching_skill_percent.

To ensure that the program can handle large CSV files, the program performs job matching in either of the following ways:
1. Sequential Processing: for small CSV files
2. Parallel Processing: for large CSV files

## Getting Started

### Prerequisites
* [Python ≥ 3.10.5](https://www.python.org/downloads/)
  
### Installation 
1. Clone the repo if you have git.
```
git clone https://github.com/annu-thapa55/Job-Match-Recommendation-Engine.git
```
Or press Code➝Download ZIP.

2. You can create a separate Python virtual environment to isolate and decouple Python installs and associated pip packages. For that, create a folder (YOUR-PROJECT-FOLDER) and run the following commands:
```
pip install virtualenv 
python -m venv NAME-OF-YOUR-VIRTUAL-ENVIRONMENT
```
3. Run the following command (from the path of PROJECT-FOLDER) to install all the necessary packages. 
```
pip install -r requirements.txt
```
4. Folder structure should be:
```
|----->YOUR-PROJECT-FOLDER
      |----->NAME-OF-YOUR-VIRTUAL-ENVIRONMENT
            |----->Include
            |----->.....
      |----->requirements.txt
      |----->Job-Match-Recommendation-Engine-main
``` 
## Usage
### Starting the Script
There are multiple ways of starting the application.
#### With RUN.cmd Script
1. If you have Windows, and your security settings permit it, you can double-click the provided RUN.cmd file to run the main.py and all the test case files. 
#### With Command Line
1. Open the command line interface.
2. Navigate to the folder containing the main.py file.
```
cd PATH_TO_PROJECT
```
3. Enter the following command to run the main program:
```
python main.py
```
3. Enter the following commands to run the test case files:
```
python -m unittest tests.test_read_files
python -m unittest tests.test_job_match_recommendation
python -m unittest tests.test_recommendation
```
#### Changing CSV files
Since the program is reading the CSV files for jobs and job seekers from the folder "csv_file", the new files should replace the existing once. However, the name of the files should be the same as the name of the existing files. 

## Output
The program prints the output as the job recommendations. For each job seeker, the matched jobs and relevant information are listed. The entire output is sorted first by jobseeker ID and then by the percentage of matching skills in descending order. As a result, jobs with the highest percentage of matching skills are listed first. If two jobs have the same matching skill percentage, they are sorted by job ID in ascending order.

## Evaluation
### Correctness: Does the program correctly match job seekers to jobs based on their skills?
The program provides the correct output by accurately matching the job seekers to jobs based on their skills. Moreover, the entire job recommendations list is sorted as per the aforementioned sorting requirements.

### Code Quality: Is the code easy to understand and maintain?
To ensure code quality, the following measures have been implemented:
1. The summaries for each Class and function and comments on important statements are provided to make the code easy to comprehend. 
2. Standard and consistent variable naming conventions have been followed.
3. Test cases are provided for all classes and functions. Also, the normal execution of the program is maintained using exception handling. 

 ### Extendibility: If we needed to add additional functionality, how difficult would this be?
 The SOLID principles have been applied to ensure that the program is maintainable and extensible. The implementation of each principle is summarized below:
 1. Single Responsibility Principle (S): To ensure that each class has one responsibility, without being responsible for unrelated tasks, three modules for File, Recommendation Engine, and JobMatchRecommendationEngine are created, and class-specific functions are implemented.
    
 2. Open/Close Principle (O): The new functionality can be added by extending the existing code. For instance, there might be a scenario where decisions on upskilling current human resources have to be taken for aligning to the company's strategic planning. In such a case, the current program can be extended to find the skills that each employee needs to learn and upskill based on the future requirements of jobs. For that, another class can be created, say UpskillRecommendationEngine, that inherits the abstract class named RecommendationEngine. With such an approach, the new UpskillRecommendationEngine class can use the concretely implemented general functions of the abstract class and implement the abstract methods as per the underlying requirements.
    
 3. Liskov Substitution Principle (L): The subclass JobMatchRecommendationEngine can be used in place of its superclass RecommendationEngine without any problems.
    
 4. Interface Segregation Principle (I): Although the abstract class is deployed instead of the interface, the program still ensures that unrelated methods are not included and implemented in any of the classes.
    
 5. Dependency Inversion Principle (D): To implement this principle for achieving a decoupled and maintainable codebase, abstraction instead of concrete implementations is implemented in the program.

### Efficiency: How well does the program handle large inputs?
The program is designed to handle both small and large inputs. For that, sequential processing is activated for the small input CSV files whereas multiprocessing is activated for the CSV files of large size. The decision on which processing to conduct depends on the threshold for parallel processing. This threshold is set to a default value of 5 GB, meaning that parallel processing is employed if the total size of two input files is greater than 5 GB. This threshold can also be set by the user within the range of 5GB to 10 GB. 

In addition, the pool size (number of worker processes) in parallel processing is determined dynamically based on the available CPU processor. Equally important, the pandas's data frame is used for manipulating the contents of CSV files, which further guarantees the ability of the program to handle large inputs. 

### Tests: Is the code covered by automated tests?
Python unittest module has been deployed to create automated test cases to guarantee the robustness of the program against corner cases.  
