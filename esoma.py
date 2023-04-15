from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
import configparser
import time
import pandas as pd
import os

STRING_RESULT = '_results'
EXCEL_FILE_EXTENSION = '.xlsx'
FRANKLIN_CLASSIFICATION = 'Franklin Classification'


def checkFrequency1000GAll(x, thr: float) -> bool:
    '''
    Function that saves all and only the values that are not greater than the desired threshold, that are nans and that are '.'
    '''
    import math

    if (type(x) == float):
        if not math.isnan(x):
            if (x <= thr):
                return True
            else:
                return False

    if type(x) == str:
        return True

    if math.isnan(x):
        return True

# create a new instance of the ConfigParser class
config = configparser.ConfigParser()

# read the contents of the keystore.properties file
config.read('config.properties')

# Get the current working directory to use relative paths in properties file
cwd = os.getcwd()

# Get the value of the source file path
config_path = config['DEFAULT']['source_file_path']
file_path = os.path.join(cwd, config_path)

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

df = pd.read_excel(file_path)

### DATASET FILTERS

df = df.loc[df['Func.refGene'].isin(['exonic', 'exonic;splicing', 'splicing'])]
df = df.loc[~ df['ExonicFunc.refGene'].isin(['synonymous SNV', 'unknown'])]
# generate the column of true values for the values to be filtered
df['filtro1000G'] = df['1000G_ALL'].apply(lambda x: checkFrequency1000GAll(x,0.02))
# update dataframe
df=df[df['filtro1000G']==True]
# drop undesired column
df.drop('filtro1000G',axis=1,inplace=True)
# remove 'HLA' and 'MUC' genes 
df = df[~df['Gene.refGene'].str.startswith(('HLA', 'MUC'))]


# extract raw file name fo the  input file
rawName = file_path.split('\\')[-1]
inputFileName = rawName.split('.')[0]
output_filename = os.path.join('output', inputFileName + STRING_RESULT + EXCEL_FILE_EXTENSION)

'''
if output file already exists, get the number of already written rows
and remove them from the filtered dataframe received from the input file 
'''
df_out_start = None
if os.path.exists(output_filename):
    df_out_start = pd.read_excel(output_filename)
    rows_loaded_before = len(df_out_start.index)
    df = df.tail(-rows_loaded_before)
    print('The first ' + str(rows_loaded_before) + ' rows were already inserted.')
else:
    rows_loaded_before = 0

# search for the bar
driver.get("https://franklin.genoox.com/")
barraRicerca = driver.find_element(By.CLASS_NAME, "ng-pristine")

# run over variants
classification_list = list()
for item in tqdm(df['Merge']):
    
    barraRicerca.send_keys(item)
    barraRicerca.send_keys(Keys.ENTER)
    
    time.sleep(5)
    # identify the element of the classification of the mutation
    try:
        categoriaMutazione = driver.find_element(By.CLASS_NAME, "indicator-text")
    except:
        time.sleep(10)
        categoriaMutazione = driver.find_element(By.CLASS_NAME, "indicator-text")

    classification_list.append(categoriaMutazione.text)
    # search the next variant - we have to find a different element to do the search in the already searched page
    barraRicerca = driver.find_element(By.CLASS_NAME, "search-input")
    # clear the content of the bar
    barraRicerca.clear()

    # save the output filtered dataframe
    df_out = df[0:len(classification_list)]
    df_out[FRANKLIN_CLASSIFICATION] = classification_list

    '''
    if the output file already contained something, adds that on top (otherwise the previous lines would be overwritten)
    '''
    if df_out_start is not None:
        df_out.append(df_out_start)
        df_out = pd.concat([df_out_start, df_out])

    df_out.to_excel(output_filename, index=False)

    
print(classification_list)

# close the browser window
driver.quit()