from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import configparser

# create a new instance of the Chrome driver
driver = webdriver.Chrome()

# create a new instance of the ConfigParser class
config = configparser.ConfigParser()

# read the contents of the keystore.properties file
config.read('keystore.properties')

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

# close the browser window
driver.quit()
