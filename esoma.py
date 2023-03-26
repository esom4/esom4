from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
import configparser
import time
import pandas as pd

# create a new instance of the ConfigParser class
config = configparser.ConfigParser()

# read the contents of the keystore.properties file
config.read('config.properties')

# Get the value of the source file path
source_file_path = config['DEFAULT']['source_file_path']

# create a new instance of the Chrome driver
try: # try with environment variable
    driver = webdriver.Chrome()
except: # otherwise use the local path
    # Get the value of the "driver_path" key
    driver_path = config['DEFAULT']['driver_path']
    driver = webdriver.Chrome(executable_path=driver_path)

# navigate to the login page
driver.get("https://franklin.genoox.com/login")

# enter the username and password
username = config.get('FRANKLIN', 'username')
password = config.get('FRANKLIN', 'password')

username_field = driver.find_element(By.ID, "email")
password_field = driver.find_element(By.ID, "password")

username_field.send_keys(username)
password_field.send_keys(password)

# submit the login form
password_field.send_keys(Keys.RETURN)

# wait for the page to load after login
time.sleep(3)

# navigate to the page with the data
driver.get("https://franklin.genoox.com/clinical-db/home")

# get the HTML content of the page and parse it with BeautifulSoup
html_content = driver.page_source
soup = BeautifulSoup(html_content, "html.parser")

# extract the relevant data from the HTML code using BeautifulSoup
# ...

## SEARCH THE VARIANTS

df = pd.read_excel(source_file_path)

# search for the bar
driver.get("https://franklin.genoox.com/")
barraRicerca = driver.find_element(By.CLASS_NAME, "ng-pristine")

# run over variants
classification_list = list()
#TODO: after the test with 10 rows, remove the .values[:10] to get all the values
for item in df['Merge'].values[:10]: 
    
    barraRicerca.send_keys(item)
    barraRicerca.send_keys(Keys.ENTER)
    
    time.sleep(5)
    # identify the element of the classification of the mutation
    categoriaMutazione = driver.find_element(By.CLASS_NAME, "indicator-text")
    classification_list.append(categoriaMutazione.text)
    # search the next variant - we have to find a different element to do the search in the already searched page
    barraRicerca = driver.find_element(By.CLASS_NAME, "search-input")
    # clear the content of the bar
    barraRicerca.clear()
    
    
print(classification_list)

# close the browser window
driver.quit()