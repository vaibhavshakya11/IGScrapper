import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from subjects import subject_dict

def extract_all_links(site):
    html = requests.get(site).text
    soup = BeautifulSoup(html, "html.parser").find_all("a")
    links = [link.get("href") for link in soup]
    return links

def get_exam_year():
    while True:
        try:
            year = input(f"Enter the year you'll give your exams (e.g., {datetime.now().year+1}): ").strip()
            if not year.isdigit() or len(year) != 4 or int(year) not in range(datetime.now().year, datetime.now().year + 8):
                raise ValueError("Invalid input. Please enter a sensible four-digit year.")
            return int(year)
        except ValueError as ve:
            print(ve)

def get_past_paper_start_year():
    while True:
        try:
            year = input(f"Enter the start year for past papers download (e.g., {datetime.now().year-4}): ").strip()
            if not year.isdigit() or len(year) != 4 or int(year) not in range(2000, datetime.now().year + 1):
                raise ValueError("Invalid input. Please enter a sensible four-digit year.")
            return int(year)
        except ValueError as ve:
            print(ve)

def extract_years_from_url(url):
    match = re.search(r'(\d{6})-(\d{4})(-(\d{4}))?-syllabus\.pdf', url)
    if match:
        year1 = int(match.group(2))
        year2 = int(match.group(4)) if match.group(4) else None
        return year1, year2
    return None, None

def is_valid_syllabus_for_year(url, exam_year):
    year1, year2 = extract_years_from_url(url)
    if year1:
        if year1 == exam_year and year2 is None:
            return True
        if year1 < exam_year and year2 is None:
            return False
        if year1 <= exam_year and (year2 is None or year2 >= exam_year):
            return True
        if year1 > exam_year:
            return False
    return False

def extract_subject_name(subject_code):
    url_path = subject_dict[subject_code]
    match = re.search(r'/cambridge-igcse-(.*)-\d{4}/', url_path)
    if match:
        subject_name = match.group(1)
        if "9 1" in subject_name:
            subject_name = subject_name.replace("9 1", "9-1")
        return subject_name
    return "Unknown Subject"

def download_file(url, filename, foldername):
    display_name = filename if "Syllabus" in filename else url[-18:]
    foldername = foldername.replace("9 1 ", "")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        os.makedirs(foldername, exist_ok=True)
        filepath = os.path.join(foldername, filename)
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"{display_name}: Download Successful")
    else:
        print(f"{display_name}: Download Unsuccessful")

def download_syllabus(subject_url, subject_code, exam_year):
    year1, year2 = extract_years_from_url(subject_url)
    if year2:
        year_range = f"{year1}-{year2}"
    else:
        year_range = f"{year1}"
    
    subject_name = extract_subject_name(subject_code)
    filename = f"{subject_name.replace("-", " ").title().replace("9 1", "9-1")} {subject_code} ({year_range}) Syllabus.pdf"
    foldername = os.path.join("IGCSE Resources", f"{subject_name.replace("-", " ").title().replace("9 1", "9-1")} {subject_code}")
    download_file(subject_url, filename, foldername)

def get_series_suffix(series):
    return {'may june': 's', 'oct nov': 'w', 'feb march': 'm'}.get(series.lower(), '')

def check_paper_availability(subject_code, subject_name, series_suffix, year):
    if "-9-1" in subject_name:
        base_url = "https://bestexamhelp.com/exam/cambridge-igcse-9-1"
        subject_name = subject_name.replace("-9-1", "")
    else:
        base_url = "https://bestexamhelp.com/exam/cambridge-igcse"
    available_papers = []
    print("In the process of collecting valid components, please wait. This may take up to 2 minutes.")
        
    for paper_code in [f"{x}2" for x in range(1, 7)]:
        for paper_type in ['qp', 'ms', 'in']:
            url = f"{base_url}/{subject_name}-{subject_code}/{year}/{subject_code}_{series_suffix}{str(year)[-2:]}_{paper_type}_{paper_code}.pdf"
            response = requests.head(url)
            if response.status_code == 200:
                for code_extension in ['1', '2', '3']:
                    available_papers.append((paper_type, paper_code[0] + code_extension))
    if available_papers:
        print("Components found.")
    else:
        print("Components not found.")
    return available_papers

def download_past_papers(subject_code, subject_name, exam_year):
    current_year = datetime.now().year
    subject_foldername = os.path.join("IGCSE Resources", f"{subject_name.replace("-", " ").title().replace("9 1", "9-1")} {subject_code}")

    for year in range(exam_year, current_year + 1):
        for series in ['May June', 'Oct Nov', 'Feb March']:
            series_suffix = get_series_suffix(series)
            available_papers = check_paper_availability(subject_code, subject_name, series_suffix, year)
            if "-9-1" in subject_name:
                base_url = "https://bestexamhelp.com/exam/cambridge-igcse-9-1"
                subject_name = subject_name.replace("-9-1", "")
            else:
                base_url = "https://bestexamhelp.com/exam/cambridge-igcse"
            for paper_type, paper_code in available_papers:
                url = f"{base_url}/{subject_name}-{subject_code}/{year}/{subject_code}_{series_suffix}{str(year)[-2:]}_{paper_type}_{paper_code}.pdf"
                filename = f"{subject_code}_{series_suffix}{str(year)[-2:]}_{paper_type}_{paper_code}.pdf"
                foldername = os.path.join(subject_foldername, "Past Papers", str(year), series, f"Paper {paper_code}")
                download_file(url, filename, foldername)

def take_code_input():
    while True:
        try:
            code = input("Enter the four-digit course code (e.g., 0625): ").strip()
            if code == "0000":
                return None
            if len(code) != 4 or not code.isdigit():
                raise ValueError("Invalid input. Please enter a sensible four-digit numerical code.")
            if code not in subject_dict:
                raise KeyError("Course code not found. Please enter a valid course code.")
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        else:
            return code

def main():
    print("\nWelcome to IGScrapper!")
    print("Enter 0000 to exit once you're done!\n")
    exam_year = get_exam_year()
    start_year = get_past_paper_start_year()

    while True:
        subject_code = take_code_input()
        if subject_code is None:
            break
        subject_link = f"https://www.cambridgeinternational.org{subject_dict[subject_code]}"
        all_links = extract_all_links(subject_link)
        syllabus_available = False
        for val in all_links:
            if val is not None and "syllabus.pdf" in val:
                subject_url = f"https://www.cambridgeinternational.org{val}"
                if is_valid_syllabus_for_year(subject_url, exam_year):
                    download_syllabus(subject_url, subject_code, exam_year)
                    syllabus_available = True
        if not syllabus_available:
            print("Syllabus Unavailable.")

        subject_name = extract_subject_name(subject_code).lower()
        download_past_papers(subject_code, subject_name, start_year)
    print("\nExiting the program. \nThanks for using IGScrapper. \nRegards, Vaibhav Shakya.\n")

if __name__ == "__main__":
    main()
