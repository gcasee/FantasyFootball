
from bs4 import BeautifulSoup
import requests
import pandas as pd


# Function to scrape a specific table from the given site
def extract_table(url, table_index):
    '''
    **Parameters**
        url: *str*
            The website url to scrape data tables from
        table_index: *int*
            Table on the website to scrape
    **Returns**
        table: *bs4.element.Tag*
            BeautifulSoup object containing the extracted table's information
    '''
    page = requests.get(url)
    soup = BeautifulSoup(page.text, features='lxml')
    table = soup.find_all('table')[table_index]
    return table


# Function to extract the column names from the table of interest
def get_column_names(table, header_index):
    '''
    **Parameters**
        table: *bs4.element.Tag*
            BeautifulSoup object containing the extracted table's information
        header_index: *int*
            Row in which the column names reside
    **Returns**
        table: *bs4.element.Tag*
            BeautifulSoup object containing the extracted table's information
    '''
    header_row = table.findAll('tr')[header_index]
    columns = header_row.findAll('td')
    columns = [x.text.strip() for x in columns]
    return columns


# Function to extract table data
def get_table_data(table, data_start_index):
    '''
    **Parameters**
        table: *bs4.element.Tag*
            BeautifulSoup object containing the extracted table's information
        data_start_index: *int*
            Row in which the data begins
    **Returns**
        data: *list of strings*
            Values within the table data tags of the given table
    '''
    data = []
    for row in table.findAll('tr')[data_start_index:]:
        columns = row.findAll('td')
        columns = [x.text.strip() for x in columns]
        data.append(columns)
    return data


num_weeks = 17
num_pages = 2

data_table = None
for week in range(1, num_weeks+1):
    for page in range(0, num_pages):
        
        # Update the url with the week and page numbers
        url = 'https://www.fftoday.com/stats/playerstats.php?Season=2020&GameWeek={}&PosID=20&' \
              'LeagueID=26955&order_by=FFPts&sort_order=DESC&cur_page={}'.format(week, page)
        table = extract_table(url, 8)
        
        # Gets the column names on the first pass
        if data_table is None:
            columns = get_column_names(table, 1)
            columns[0] = 'Player'
        
        # Extract the data and add a week column
        data = get_table_data(table, 2)
        df = pd.DataFrame(data=data, columns=columns)
        df['Week'] = week
        
        # Create the data table or append to it
        if data_table is None:
            data_table = df.copy()
        else:
            data_table = data_table.append(df, ignore_index=True)


# Final cleanup and write to file
data_table['Player'] = data_table['Player'].str.strip('0123456789.')
data_table.to_csv('RB2020.csv', index=False)

