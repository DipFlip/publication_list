from bs4 import BeautifulSoup
from openai import OpenAI
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


client = OpenAI()


def fetch_website_content(url):
    # Setup Chrome with Selenium WebDriver Manager
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Uncomment if you don't want the browser to open up
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(5)  # Wait for the page to load. Adjust time as necessary.

    # Now the page's JavaScript has been executed and content should be loaded
    html_content = driver.page_source

    driver.quit()  # Close the browser
    return html_content


def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(separator="\n", strip=True)


def generate_publications_text(html_text):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": 'Extract all publications with title, authors, journal, and year from given text. You return text like Title: [title]\nAuthors: [author name, author name, author names including "..."]\nJournal: [journal]\nYear: [year] for up to 10 publications. Dont make anything bold or add any other formatting or numbers, just list like instructed.',
            },
            {"role": "user", "content": html_text},
        ],
    )

    return completion.choices[0].message.content


def process_publications_from_csv(input_csv, output_filename):
    with open(input_csv, newline="") as csvfile, open(
        output_filename, "w"
    ) as output_file:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(f"Processing {row['name']}...")
            name = row["name"]
            link = row["link"]
            html_content = fetch_website_content(link)
            html_text = extract_text_from_html(html_content)
            publications_text = generate_publications_text(html_text)
            output_file.write(
                f"{name}\n\n{publications_text}\n\n------------------------------\n\n"
            )


if __name__ == "__main__":
    import sys

    input_csv = sys.argv[1]  # Get CSV filename from command line argument
    output_filename = "output.txt"  # Define your output filename
    process_publications_from_csv(input_csv, output_filename)
    print(f"Processed publications saved to {output_filename}")
