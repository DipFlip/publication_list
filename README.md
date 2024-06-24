# Google Scholar Profile Scraper

This Python script is designed to scrape Google Scholar profiles for publication information using a list of profile URLs provided in a CSV file. It extracts details such as publication title, authors, journal, and publication year, and outputs the information into a text file.

## Features

- Fetch Google Scholar profile pages
- Parse publication information
- Sort publications by year
- Output the latest 10 publications per profile into a text file

## Requirements

To run this script, you will need Python 3.x and the following Python packages:

- `requests`
- `beautifulsoup4`
- `csv`
- `sys`

You can install the required packages using the following command:

```bash
pip install -r requirements.txt