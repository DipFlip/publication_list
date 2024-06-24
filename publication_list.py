import requests
from bs4 import BeautifulSoup
import csv
import sys

def get_google_scholar_profile(public_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(public_url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve the profile.")
        return None

    return response.text

def parse_publications(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    publications = []

    for row in soup.find_all('tr', class_='gsc_a_tr'):
        title_element = row.find('a', class_='gsc_a_at')
        title = title_element.text if title_element else "N/A"

        authors_element = row.find('div', class_='gs_gray')
        authors = authors_element.text if authors_element else "N/A"

        journal_element = row.find_all('div', class_='gs_gray')[1]
        journal = journal_element.text if len(row.find_all('div', class_='gs_gray')) > 1 else "N/A"

        year_element = row.find('span', class_='gsc_a_h')
        year = year_element.text if year_element else "N/A"

        try:
            year = int(year)
        except ValueError:
            year = 0

        publications.append({
            'title': title,
            'authors': authors,
            'journal': journal,
            'year': year
        })

    return publications

def process_scholar_profiles(csv_file_path):
    with open(csv_file_path, newline='') as csvfile, open('output.txt', 'w') as output_file:
        reader = csv.DictReader(csvfile)
        for row in reader:
            output_file.write(f"Name: {row['name']}\n\n")
            html_content = get_google_scholar_profile(row['link'])
            if html_content:
                publications = parse_publications(html_content)
                latest_publications = sorted(publications, key=lambda x: x['year'], reverse=True)[:10]
                for publication in latest_publications:
                    output_file.write(f"Title: {publication['title']}\n")
                    output_file.write(f"Authors: {publication['authors']}\n")
                    output_file.write(f"Journal: {publication['journal']}\n")
                    output_file.write(f"Year: {publication['year']}\n")
                    output_file.write("-" * 80 + "\n")
            output_file.write("\n")  # Add a newline for spacing between scholars

def main():
    if len(sys.argv) < 2:
        print("Usage: python scrape_scholars.py input.csv")
        sys.exit(1)
    csv_file_path = sys.argv[1]
    process_scholar_profiles(csv_file_path)

if __name__ == "__main__":
    main()