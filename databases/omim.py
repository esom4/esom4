# work in progress

import pandas as pd
file_path = os.path.join(cwd, config_path)
df = pd.read_excel(file_path)

def OMIMquery(gene):
    '''
    OMIM query
    '''
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import configparser
    import time
    from tqdm import tqdm
    import pandas as pd 
    # Create a ConfigParser object
    configDriver = configparser.ConfigParser()

    # Read the configuration from the file
    configDriver.read('config.properties')

    # Get the value of the "driver_path" key
    driver_path = 'D:\DOTTORATO\projects\ProgettoEsoma\chromedriver_win32\chromedriver.exe'

    # create a new instance of the Chrome driver
    driver = webdriver.Chrome(executable_path=driver_path)
    
    # close the cookies 
    driver.get("https://www.omim.org/")
    try:
        driver.find_element(By.CLASS_NAME,"close").click()
    except:
        time.sleep(10)
        driver.find_element(By.CLASS_NAME,"close").click()
    
    # search-bar
    searchBar = driver.find_element(By.CLASS_NAME,"form-control")
    
    # iterate over genes 
    for gene in tqdm(df['Gene.refGene'].unique()):
    
        searchBar.send_keys(gene)
        searchBar.send_keys(Keys.ENTER)
        
        # Find the first search result link
        try:
            link = driver.find_element(By.PARTIAL_LINK_TEXT, gene)
            link.click()
        except:
            time.sleep(10)
            print('catch..')
            link = driver.find_element(By.PARTIAL_LINK_TEXT, gene)
            link.click()

        time.sleep(5) # load the page 
        tableOMIM = driver.find_element(By.CLASS_NAME, 'table')
        rawTable = tableOMIM.text.split(' ')
        break 
    return rawTable        
#         # search-bar - comment, but working!
#         searchBar = driver.find_element(By.CLASS_NAME,"form-control")
#         searchBar.clear()
    
    
    # wait for the page to load after login
    time.sleep(100)
    
    
rawTable = OMIMquery(gene)
    