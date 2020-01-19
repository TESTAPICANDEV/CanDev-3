from selenium import webdriver
import re
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from selenium.webdriver.support.ui import Select
driver = webdriver.Firefox()

driver.get("https://apps.cer-rec.gc.ca/REGDOCS/Search/Index/?filter=Attr_12629_16&dt=53&txthl=english&alt=1")

time.sleep(20)
itemsSelect = Select(driver.find_element_by_id('selNumberOfRecords'))
itemsSelect.select_by_visible_text('200')
time.sleep(5)
def getContents(driver):
    items = pd.DataFrame(columns = ['link','submitter','date','name'])
    flag = True
    while flag:
        buttons = driver.find_elements_by_tag_name('a')
        nextbuttons = [button for button in buttons if(button.get_attribute('rel')=='next')]

        nextButtons = None
        if len(nextbuttons) >0:
            nextButton = nextbuttons[0]
        else:
            flag = False
        
        tableresults = driver.find_elements_by_tag_name('tbody')
        header = driver.find_elements_by_tag_name('thead')
        

        for tr in tableresults:
            rows  = tr.find_elements_by_tag_name('tr')
            for row in rows:
                columns = row.find_elements_by_tag_name('td')
                item = {}
                for col in columns:
                    if col.find_elements_by_tag_name('a') != []:
                        name = col.text
                        link = col.find_elements_by_tag_name('a')[0].get_attribute('href')
                        item['name'] = name
                        item['link'] = link
                    else:
                        text = col.text
                        if(re.search('\d+-\d+-\d+',text)):
                           date = text
                           item['date'] = date
                        else:
                           submitter = text
                           item['submitter'] = submitter
                items = items.append(item,ignore_index = True)

                
        if(flag):
            nextButton.click()
            time.sleep(10)
    return items
results = getContents(driver)
