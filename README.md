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

2. Navigate to the location of the requirements file on your system and install the requirements.
```
cd PATH_TO_PROJECT
pip install -r requirements.txt
```

## Usage
### Starting the Application
There are multiple ways of starting the application.
#### With RUN.cmd Script
1. If you have Windows, and your security settings permit it, you can double-click the provided RUN.cmd file to run the main.py and all the test case files. 
#### With Command Line
1. Open the command line interface.
2. Navigate to the folder containing the main.py file.
```
cd PATH_TO_PROJECT
```
3. Enter the following command:
```
python main.py
```

### Output
The program prints the output as the job recommendations. For each job seeker, the matched jobs and relevant information are listed. The entire output is sorted first by jobseeker ID and then by the percentage of matching skills in descending order. As a result, jobs with the highest percentage of matching skills are listed first. If two jobs have the same matching skill percentage, they are sorted by job ID in ascending order.

### Evaluation


