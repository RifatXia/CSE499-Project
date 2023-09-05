import requests
from bs4 import BeautifulSoup
import csv

# URL to scrape
url = "https://impact.dbmi.columbia.edu/~friedma/Projects/DiseaseSymptomKB/index.html"

# Fetch HTML content from the URL
response = requests.get(url)
html_content = response.content

# Create a BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

# Extract data from <td> elements
data_rows = []
current_row = []
for td in soup.find_all('td'):
    # Get text and remove leading/trailing spaces
    text = td.get_text(strip=True)
    text = ' '.join(text.split())   # Remove extra internal spaces
    text = text.replace('"', '')    # Remove quotes

    # Split text by underscores "_" and take the last element
    words = text.split('_')
    word = words[-1] if words else ""
    current_row.append(word)

    if len(current_row) == 3:  # Each row has 3 columns
        if len(current_row[0]) > 0:
            cap_word = current_row[0].title()
            current_row[0] = cap_word
        data_rows.append(current_row)
        current_row = []

# Create a CSV file and write the cleaned data
csv_filename = "dataset/data_3.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Column 1", "Column 2", "Column 3"])  # Write header

    for row in data_rows:
        csv_writer.writerow(row)
