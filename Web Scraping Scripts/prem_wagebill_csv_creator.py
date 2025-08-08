from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import chromedriver_autoinstaller
import time
import re
import sys

# Take string argument for a url at time of execution and store it in web_url
web_url = str(sys.argv[1])

# Install Chrome Driver automatically and instantiate Driver
chromedriver_autoinstaller.install()
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')


driver = webdriver.Chrome(options=options)

driver.get(web_url)
time.sleep(10)

# Create Dataframe and cycle through table data to populate records

col_names = ['Team', 'Player Count', 'Weekly Wages', 'Annual Wages']
wage_stats = pd.DataFrame(columns = col_names)
wage_table= driver.find_element(By.ID, 'squad_wages')
meta_container = driver.find_element(By.ID, 'info').find_element(By.ID, 'meta')
season = meta_container.find_elements(By.TAG_NAME, 'div')[1].find_element(By.TAG_NAME, 'h1').text.split(" ")[0]
	
for tr in wage_table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr'):
	table_data = tr.find_elements(By.TAG_NAME, 'td')
	team_name = table_data[0].text
	player_count = table_data[1].text
	weekly_wages = table_data[2].text
	annual_wages = table_data[3].text

	new_wage_item = pd.DataFrame({'Team': [team_name], 'Player Count': [player_count], 'Weekly Wages' : [weekly_wages], 'Annual Wages' : [annual_wages]})
	wage_stats = pd.concat([wage_stats, new_wage_item])


print(wage_stats.head())

# Create file name, close driver, and create csv from Data Frame
file_name = 'premier_league_wagebill_' + str(season) + '.csv'

driver.quit()


wage_stats.to_csv(file_name, index = False)
print("File '" + file_name + "' created.")