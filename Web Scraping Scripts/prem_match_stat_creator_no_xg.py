from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import chromedriver_autoinstaller
import time
import re
import sys

web_url = str(sys.argv[1])

chromedriver_autoinstaller.install()

service = Service('C:\\chromedriver-win64\\chromedriver.exe')

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')


driver = webdriver.Chrome(service = service, options=options)

driver.get(web_url)
time.sleep(10)

col_names = ['Date', 'homeTeam', 'awayTeam', 'homeGoals', 'awayGoals', 'result']
match_stats = pd.DataFrame(columns = col_names)
body = driver.find_element(By.ID, 'all_sched')
table = body.find_element(By.TAG_NAME, 'table')
table_body = table.find_element(By.TAG_NAME, 'tbody')

i = 0
for row in table_body.find_elements(By.TAG_NAME,'tr'):
	i += 1
	if (row.get_attribute("class") == "spacer partial_table result_all" or row.get_attribute("class") == "thead"):
		#skip unimportant spacer rows
		pass
	else:
		score = row.find_elements(By.TAG_NAME, "td")[4].text.split("–")
		home_goals = int(score[0])
		away_goals = int(score[1])
		if (home_goals > away_goals):
			result = "H"
		elif (away_goals > home_goals):
			result = "A"
		else:
			result = "D"
		new_match = pd.DataFrame({"Date": [row.find_elements(By.TAG_NAME, "td")[1].text], "homeTeam" : [row.find_elements(By.TAG_NAME, "td")[3].text], "awayTeam": [row.find_elements(By.TAG_NAME, "td")[5].text], "homeGoals": [home_goals], "awayGoals": [away_goals], "result" : [result]})
		match_stats = pd.concat([match_stats, new_match])
		
print(match_stats.head())

start_year = str(match_stats['Date'][0]).split('-')[0].split("    ")[1]
print(start_year)
file_name = 'premier_league_match_stats_' + start_year + '-' + str(int(start_year)+1)+ '.csv'
print(file_name)
driver.quit()


match_stats.to_csv(file_name, index = False)