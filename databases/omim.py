def OMIMquery(df):
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
    link_url_list = list()
    for gene in tqdm(df['Gene.refGene'].unique()[0:5]):
    
        searchBar.send_keys(gene)
        searchBar.send_keys(Keys.ENTER)
        
        # Find the first search result link
        try:
            link = driver.find_element(By.PARTIAL_LINK_TEXT, gene)
            link_url = link.get_attribute("href")
            link_url_list.append(link_url)
            print(link_url)
        
        except:
            time.sleep(10)
            print('catch..')
            print('Gene:', gene)
            try:
                link = driver.find_element(By.PARTIAL_LINK_TEXT, gene)
                link_url = link.get_attribute("href")
                link_url_list.append(link_url)
                print(link_url)
            except:
                link_url_list.append('None')
                print('Not found, go to next gene.')
                # search-bar - comment, but working!
                searchBar = driver.find_element(By.CLASS_NAME,"form-control")
                searchBar.clear()  
                continue
                
        # search-bar - comment, but working!
        searchBar = driver.find_element(By.CLASS_NAME,"form-control")
        searchBar.clear()   
    # save output dataframe with omim links
    df_out = df[0:len(link_url_list)]    
    df_out['OMIM-Links'] = link_url_list 
    df_out.to_excel('omimTest.xlsx')

import pandas as pd
import os
# file_path = os.path.join(cwd, config_path)
df = pd.read_excel("D:\\DOTTORATO\\projects\\ProgettoEsomaRepo\\secondFolder\\esoma\\data\\920-22 + Merge.xlsx")

OMIMquery(df)
    