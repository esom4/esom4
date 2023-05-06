from utils.install_dependencies import try_install_missing_packages
# list of required packages
packages = ['requests', 'beautifulsoup4', 'pandas', 'selenium', 'openpyxl', 'tqdm']

# install missing packages if possible
try_install_missing_packages(packages)

from selenium.webdriver.common.by import By
from tqdm import tqdm
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
import configparser
import time
import pandas as pd
import os
from typing import List
import json

STRING_RESULT = '_results'
EXCEL_FILE_EXTENSION = '.xlsx'
FRANKLIN_CLASSIFICATION = 'Franklin Classification'


def printReceivedInput(elaboratedInput) -> None:
    print('Input received:')
    if elaboratedInput == []:
        print('Nothing selected')
    else:
        print(elaboratedInput)
    print()  # leave a line of space before the next print


def getUserInput() -> str:
    userInput = input("Write here:")
    return userInput


def getUserInputList() -> List[str]:
    userInput = getUserInput()
    if userInput == '':
        return []
    else:
        return userInput.split(",")


def getUserInputListFromNumberedList(elementList: List[str]) -> List[str]:
    # the user will insert the selected elements as 1,2,3 as the position in the option list starting from 1 (e.g. 1 is elementList[0])
    userInput = getUserInputList()
    if len(userInput) == 0:  # if input is empty
        return userInput
    # otherwise:
    selectedElements = []
    for number in list(map(lambda x: int(x), userInput)):
        selectedElements.append(elementList[number-1])
    return selectedElements


def printNumberedList(list: List[str]) -> None:
    for i in range(0, len(list)):
        print(str(i + 1) + "-" + list[i])


def isNumber(string : str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False


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


cwd = os.getcwd()  # get the current working directory

# create a new instance of the ConfigParser class
config = configparser.ConfigParser()

# read the contents of the keystore.properties file
config.read(os.path.join(cwd, 'config.properties'))


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

print('Loading file...')
df = pd.read_excel(file_path)
print('Completed.')

# if the previous execution did not terminate, get the saved filters, ask the user to select them otherwise
prev_filter_file = os.path.join(cwd, 'tmp_filters.json')

if os.path.isfile(prev_filter_file):
    askFilters = False
    # get saved filters
    with open(prev_filter_file) as json_file:
        savedFilters = json.load(json_file)
        selectedMutations = savedFilters['selectedMutations']
        genesToExclude = savedFilters['genesToExclude']
        causEffToExclude = savedFilters['causEffToExclude']
        selectedCutOff = savedFilters['selectedCutOff']
else:
    askFilters = True

### DATASET FILTERS

# filter 1
print("Which mutations do you want to analyze?")
if askFilters is True:
    print('Write your input as (example) 1,2,5,12 (with no space around commas)')
    optionInputMutations = df['Func.refGene'].unique()  # options to select
    printNumberedList(optionInputMutations)
    selectedMutations = getUserInputListFromNumberedList(optionInputMutations)
printReceivedInput(selectedMutations)
df = df.loc[df['Func.refGene'].isin(selectedMutations)]

# filter 2
print("Genes to exclude:")
if askFilters is True:
    print("Write the list here(as gene1,gene2,gene3) with no space around commas")
    print("Press Enter to include all.")
    genesToExclude = getUserInputList()
printReceivedInput(genesToExclude)
df = df[~df['Gene.refGene'].str.startswith(tuple(genesToExclude))]

# filter 3
print('Causative effects to exclude:')
if askFilters is True:
    optionInputCausEff = df['ExonicFunc.refGene'].dropna().unique()  # options to select (removing emtpy cells from options)
    # if there are options to select, ask what to select and then apply filter, do not even ask otherwise
    if len(optionInputCausEff) > 0:
        print("Write the list here (like 2,3,14) with no space around commas")
        print("Press Enter to include all.")
        printNumberedList(optionInputCausEff)
        causEffToExclude = getUserInputListFromNumberedList(optionInputCausEff)
    else:
        causEffToExclude = []
        print('No selectable options for this filter (considering the filters selected above).\n')
    printReceivedInput(causEffToExclude)
    df = df.loc[~ df['ExonicFunc.refGene'].isin(causEffToExclude)]

# filter 4
print('Cutoff:')
if askFilters is True:
    print('(example: to set cutoff to 15%, insert 0.15 or 0,15)')
    selectedCutOff = getUserInput()
    selectedCutOff = selectedCutOff.replace(',', '.')
    if not isNumber(selectedCutOff):
        raise Exception('The cut off is not a valid number')
    selectedCutOff = float(selectedCutOff) # convert string in actual number
printReceivedInput(selectedCutOff)
# generate the column of true values for the values to be filtered
df['filtro1000G'] = df['1000G_ALL'].apply(lambda x: checkFrequency1000GAll(x, selectedCutOff))
# update dataframe
df=df[df['filtro1000G']==True]
# drop undesired column
df.drop('filtro1000G',axis=1,inplace=True)

if askFilters is True:
    # save filters (in case the execution stops and must be restarted from where it stopped)
    filters_json = {
        "selectedMutations": selectedMutations,
        "genesToExclude": genesToExclude,
        "causEffToExclude": causEffToExclude,
        "selectedCutOff": selectedCutOff
    }

    # Serializing json
    json_string = json.dumps(filters_json, indent=4)
    with open(prev_filter_file, 'w') as outfile:
        outfile.write(json_string)

# extract raw file name fo the  input file
rawName = file_path.split('\\')[-1]
inputFileName = rawName.split('.')[0]
output_filename = os.path.join(cwd, 'output', inputFileName + STRING_RESULT + EXCEL_FILE_EXTENSION)

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
searchBar = driver.find_element(By.CLASS_NAME, "ng-pristine")

# run over variants
classification_list = list()
scaleLen = 605 # scale length in pixels for VUS classification
tol = 10
for item in tqdm(df['Merge']):
    
    searchBar.send_keys(item)
    searchBar.send_keys(Keys.ENTER)
    
    time.sleep(5)
    # identify the element of the classification of the mutation
    try:
        mutationCategory = driver.find_element(By.CLASS_NAME, "indicator-text")
    except:
        time.sleep(10)
        mutationCategory = driver.find_element(By.CLASS_NAME, "indicator-text")

    # sub-classification of VUS
    if mutationCategory.text == "VUS":
            try:
                arrow = driver.find_element(By.CSS_SELECTOR, "polyline[fill='#18244a'][stroke='#d5d7db'][stroke-width='1']")
            except:
                time.sleep(10)
                arrow = driver.find_element(By.CSS_SELECTOR, "polyline[fill='#18244a'][stroke='#d5d7db'][stroke-width='1']")

            xPosition = arrow.location['x'] # arrow position 
            scalePosition = driver.find_element(By.CLASS_NAME,"scale").location['x']
            
            # print('scala:'+str(scalePosition))
            # print('arrow:'+str(xPosition))
            # print(mutationCategory.text)
            # print(item)
            
            if xPosition > (scalePosition + scaleLen/2)+tol:
                classification = 'VUS*'
            elif (xPosition >= (scalePosition + scaleLen/2)-tol) and (xPosition <= (scalePosition + scaleLen/2)+tol): 
                classification = 'VUS'
            elif xPosition < (scalePosition + scaleLen/2)-tol:              
                classification = 'VUS-LB'
            # print(classification)
    
    else: # not VUS 
        classification = mutationCategory.text


    classification_list.append(classification)

    # search the next variant - we have to find a different element to do the search in the already searched page
    searchBar = driver.find_element(By.CLASS_NAME, "search-input")
    # clear the content of the bar
    searchBar.clear()

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

# remove the temporary file that backs up the filters (in case the execution stops and must restart from where it stopped)
os.remove(prev_filter_file)

# close the browser window
driver.quit()