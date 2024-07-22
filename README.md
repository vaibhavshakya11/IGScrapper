# IGScrapper

IGScrapper is a tool that enables you to mass download various IGCSE resources including syllabi, past papers, examiner reports, etc., locally.

## Features

- Download IGCSE syllabi and past papers for specified exam years
- Automatically names the downloaded files based on the subject and year
- Creates a structured directory for each subject, organizing syllabi and past papers by year and series
- Handles input validation and provides a robust user interface

## Requirements

- Python 3.x
- Requests library
- BeautifulSoup library

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/vaibhavshakya11/IGScrapper.git
    ```

2. Navigate to the project directory:

    ```bash
    cd IGScrapper
    ```

3. Install the required libraries:

    ```bash
    pip3 install -r requirements.txt
    ```

## Usage

1. Ensure that the `subjects.py` file is present in the same directory as your main script. This file contains the subject codes and their corresponding URLs.

2. Run the script:

    ```bash
    python3 main.py
    ```

3. Follow the prompts to enter the subject code, the year you will be taking the exams, and the start year for past papers download.

4. The script will create a structured directory called `IGCSE Resources`, with subdirectories for each subject containing syllabi and past papers organized by year and series.


## Notes

- Enter `0000` as the subject code to exit the program.
- Ensure you have a stable internet connection while using the script for downloading resources.

## Contribution

Feel free to contribute to the project by forking the repository and making pull requests. Ensure your code adheres to the existing style and include tests where appropriate.

## License

This project is licensed under the MIT License.

Thanks for using IGScrapper, Vaibhav Shakya.
