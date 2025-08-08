from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import chromedriver_autoinstaller
import time
import re
import sys

# Get url as a string argument at execution and store it in web_url

web_url = str(sys.argv[1])

# Get Chrome Driver and instantiate Driver instance

chromedriver_autoinstaller.install()

service = Service('C:\\chromedriver-win64\\chromedriver.exe')

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(service = service, options=options)

driver.get(web_url)
time.sleep(10)

# Create Data Frame and scrape web element data to populate records

col_names = ['Team', 'Season', 'Time', 'Name', 'Status', 'Position', 'Market Value', 'Age', 'Fee']
transfer_stats = pd.DataFrame(columns = col_names)
main = driver.find_element(By.ID, 'tm-main')
tables = main.find_element(By.CLASS_NAME, 'row').find_element(By.TAG_NAME, 'div')

season = tables.find_element(By.CLASS_NAME, 'content-box-headline').text.split(" ")[2]
time = tables.find_element(By.CLASS_NAME, 'content-box-headline').text.split(" ")[0]

# Given the tag name, elementExists determines whether the element exists on the web page or not
def elementExists(parent, tag_name):
    try :
        thing = parent.find_elements(By.TAG_NAME, tag_name)
    except:
        return False
    return True

# Cycle through tables to get pertinent data

for box in tables.find_elements(By.CLASS_NAME,'box'):
	try:
		team = str(box.find_element(By.TAG_NAME, 'h2').find_element(By.TAG_NAME, 'a').get_attribute('title'))
		for table in box.find_elements(By.CLASS_NAME, 'responsive-table'):
			status = table.find_element(By.CLASS_NAME, 'spieler-transfer-cell').text
			
			for tr in table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr'):
				data = tr.find_elements(By.TAG_NAME, 'td')
				name = data[0].find_element(By.TAG_NAME, 'span').find_element(By.TAG_NAME, 'a').text
				age = data[1].text
				position = data[3].text
				market_value = data[5].text
				fee = data[8].text
				
				new_transfer = pd.DataFrame({'Team': [team], 'Season': [season], 'Time' : [time], 'Name': [name], 'Status': [status], 'Position': [position], 'Market Value' : [market_value], 'Age': [age], 'Fee': [fee]})
				transfer_stats = pd.concat([transfer_stats, new_transfer])
	except Exception as e:
		print("An error has occurred: ", e)
		pass	
	
		
print(transfer_stats.head())

# Create csv from Data Frame

file_name = 'premier_league_transfers_' + str(season).split('/')[0] + '-' + str(season).split('/')[1] + '-winter.csv'

driver.quit()

transfer_stats.to_csv(file_name, index = False)
print("File '" + file_name + "' created.")