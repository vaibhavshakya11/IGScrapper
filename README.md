# IGScrapper

IGScrapper is a tool that enables you to mass download various IGCSE resources including syllabi, past papers, examiner reports, etc., locally.

## Features

- Download IGCSE syllabi for a specified exam year
- Automatically names the downloaded files based on the subject and year
- Handles input validation and provides a robust user interface
- Downloads past papers as specified by the user (feature rolling out soon) 

## Requirements

- Python 3.x
- Requests library
- BeautifulSoup library

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/IGScrapper.git
    ```

2. Navigate to the project directory:

    ```bash
    cd IGScrapper
    ```

3. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Ensure that the `subject_dict.py` file is present in the same directory as your main script. This file contains the subject codes and their corresponding URLs.

2. Run the script:

    ```bash
    python main.py
    ```

3. Follow the prompts to enter the subject code and the year you will be taking the exams.

## Example

```bash
Enter the four-digit course code (e.g., 0625): 0625
Enter the year you will be taking the exam (e.g., 2024): 2024
Syllabus downloaded successfully: IGCSE Syllabi/Physics 0625 (2023-2025) Syllabus.pdf

Do you want to download another subject's syllabus? (Y/N): N
