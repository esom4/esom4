def OMIMquery(df,driver):
    '''
    OMIM query
    '''
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    import time
    from tqdm import tqdm 

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
    for gene in tqdm(df['Gene.refGene'].unique()):
    
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

    return df_out
    