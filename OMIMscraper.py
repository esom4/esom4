gene = 'AGRN'
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
    for item in tqdm(df['Gene.refGene'].unique()):
    
        searchBar.send_keys(item)
        searchBar.send_keys(Keys.ENTER)
        # search-bar
        searchBar = driver.find_element(By.CLASS_NAME,"form-control")
        searchBar.clear()
    
    
    # wait for the page to load after login
    time.sleep(100)
    
    
OMIMquery(gene)
    