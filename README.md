# Publication List - Get publication lists from URLs

Copy/pasting publications from different sources can be tedious. This Python script is designed to collect publication lists from websites like Google Scholar or universities' publication records using a list of profile URLs provided in a CSV file. It extracts publication title, authors, journal, and publication year, and outputs the information into a text file.

## Features

- Scrape publication information from any website that lists publications
- Output the first 10 publications per profile into a text file

## Requirements

To run this script, you will need Python 3.x and the following Python packages:

- `openai`
- `beautifulsoup4`
- `webdriver_manager`
- `selenium`

You can install the required packages using the following command:

```bash
pip install -r requirements.txt
```
## Usage
- Put authors and links to websites containing their publication lists in a csv file, like the included `input.csv`
- Run `python publication_list.py input.csv`
- Results are saved in `output.txt`