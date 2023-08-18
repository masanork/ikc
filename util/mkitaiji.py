# Importing necessary libraries
import os
import random
import string
import csv
import urllib.request
from bs4 import BeautifulSoup

# Reading the HTML file
url = 'https://wwwap.hi.u-tokyo.ac.jp/ships/itaiji_list.jsp'

# Generate a random string of 10 characters
random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# Use the random string as the temporary file name
file_path = f'{random_string}.html'

# Download the file from the URL
urllib.request.urlretrieve(url, file_path)

# Read the HTML content from the file
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Delete the temporary file
os.remove(file_path)

# Parsing the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Finding the table that contains the data
table = soup.find('table')

# Previewing the first few rows of the table to understand the structure
rows_preview = []
for row in table.find_all('tr')[:5]:
    columns = [col.text.strip() for col in row.find_all('td')]
    rows_preview.append(columns)

# Path to save the CSV file
csv_file_path = 'itaiji.csv'

# Extracting the characters and writing to CSV
with open(csv_file_path, 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['正字', '異体字']) # Writing the header
    
    # Iterating through the rows and extracting the characters
    for row in table.find_all('tr')[1:]: # Skipping the first empty row
        columns = [col.text.strip() for col in row.find_all('td')]
        if len(columns) == 3:
            regular_character = columns[1]
            variant_characters = columns[2].split()
            for variant_character in variant_characters:
                writer.writerow([regular_character, variant_character])
