import requests
import os
from bs4 import BeautifulSoup
from subjects import subject_dict
import re
from datetime import datetime

def extract_all_links(site):
    html = requests.get(site).text
    soup = BeautifulSoup(html, "html.parser").find_all("a")
    links = [link.get("href") for link in soup]
    return links

def get_exam_year():
    while True:
        try:
            year = input("Enter the year you will give your exams (e.g., 2025): ").strip()
            if not year.isdigit() or len(year) != 4 or int(year) not in range(datetime.now().year, datetime.now().year + 8):
                raise ValueError("Invalid input. Please enter a valid four-digit year.")
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
        subject_name = match.group(1).replace('-', ' ').title()
        if "9 1" in subject_name:
            subject_name = subject_name.replace("9 1", "9-1")
        return subject_name
    return "Unknown Subject"

def download_syllabus(subject_url, subject_code, folder="IGCSE Syllabi"):
    year1, year2 = extract_years_from_url(subject_url)
    if year2:
        year_range = f"{year1}-{year2}"
    else:
        year_range = f"{year1}"
    
    subject_name = extract_subject_name(subject_code)
    filename = f"{subject_name} {subject_code} ({year_range}) Syllabus.pdf"
    
    response = requests.get(subject_url, stream=True)
    if response.status_code == 200:
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, filename)

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Syllabus downloaded successfully: {filepath}")
    else:
        print(f"Error downloading syllabus: {subject_url} \nStatus code: {response.status_code}")

def take_code_input():
    while True:
        try:
            code = input("Enter the four-digit course code (e.g., 0625): ").strip()
            if code == "0000":
                return None
            if len(code) != 4 or not code.isdigit():
                raise ValueError("Invalid input. Please enter a four-digit numerical code.")
            if code not in subject_dict:
                raise KeyError("Course code not found. Please enter a valid course code.")
        except ValueError as ve:
            print(str(ve))
        except KeyError as ke:
            print(str(ke))
        else:
            return code

def main():
    print("\nWelcome to IGScrapper!")
    print("Enter 0000 to exit once you're done!\n")
    exam_year = get_exam_year()
    while True:
        subject_code = take_code_input()
        if subject_code is None: break
        subject_link = f"https://www.cambridgeinternational.org{subject_dict[subject_code]}"
        all_links = extract_all_links(subject_link)
        syllabus_available = False
        for val in all_links:
            if val is not None and "syllabus.pdf" in val:
                subject_url = f"https://www.cambridgeinternational.org{val}"
                if is_valid_syllabus_for_year(subject_url, exam_year):
                    download_syllabus(subject_url, subject_code)
                    syllabus_available = True
        if not syllabus_available:
            print("Syllabus Unavailable.")
    print("\nExiting the program. \nThanks for using IGScrapper. \nRegards, Vaibhav Shakya.\n")

if __name__ == "__main__":
    main()
