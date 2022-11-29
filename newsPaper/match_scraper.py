import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

#class to get all url accoring to the link given
class SelScraper():
    def __init__(self) -> None:
        self.option = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe",options=self.option)
        self.driver.implicitly_wait(0.5)
        self.driver.maximize_window()

    def scrap_data(self):
        keyword_list = ['climate change','corporate governance','ESG','social responsibility','sustainability']
        year_list =[2009 + i for i in range(11)]
        month_dictionary ={
            "jan":31,
            "feb":28,
            "march":31,
            "april":30,
            "may":31,
            "june":30,
            "july":31,
            "aug":31,
            "sep":30,
            "oct":31,
            "nov":30,
            "dec":31
        }
        dates = []
        climate_changes = []
        corporate_governances = []
        ESGs = []
        social_responsibilities = []
        sustainability = []
        links = []
        for year in year_list:
            month_index = 1
            for  month in month_dictionary:
                if (year%4==0) and month=='feb':
                    days = 29
                else:
                    days = month_dictionary[month]
                if month_index < 10:
                    month = f"0{month_index}"
                else:
                    month = str(month_index)
                for day in range(1,days+1):
                    if day <10:
                        day = f"0{day}"
                    else: 
                        day= str(day)
                    date = str(year) + '-' + month + '-' + day
                    dates.append(date)
                    for keyword in keyword_list:
                        temp_keyword = keyword.replace(' ','%20')
                        url = f'https://www.newspapers.com/search/?query={temp_keyword}&ymd={date}'
                        links.append(url)
                        self.driver.get(url)
                        print(url)
                        time.sleep(2)
                        matches_found = self.driver.find_element(By.TAG_NAME,'h1').find_element(By.TAG_NAME,'span').text
                        if 'Loading' in matches_found:
                            time.sleep(1)
                            matches_found = self.driver.find_element(By.TAG_NAME,'h1').find_element(By.TAG_NAME,'span').text
                        if 'Loading' in matches_found:
                            time.sleep(1)
                            matches_found = self.driver.find_element(By.TAG_NAME,'h1').find_element(By.TAG_NAME,'span').text
                        if keyword == 'climate change':
                            climate_changes.append(matches_found)
                        elif keyword =='corporate governance':
                            corporate_governances.append(matches_found)
                        elif keyword =='ESG':
                            ESGs.append(matches_found)
                        elif keyword =='social responsibility':
                            social_responsibilities.append(matches_found)
                        elif keyword =='sustainability':
                            sustainability.append(matches_found)
                        print(matches_found)
                month_index=month_index+1
               
        all_data = {
            "Date":dates,
            "climate change matches":climate_changes,
            "corporate governance matches":corporate_governances,
            "ESG matches":ESGs,
            "social responsibility matches":social_responsibilities,
            "sustainability matches":sustainability,
            }
        print(all_data)
        frame = pd.DataFrame(all_data)
        frame.to_csv('output.csv')
        self.close_driver()
        
            
                
                

    def close_driver(self):
        self.driver.close()

if "__main__"==__name__:
    obj = SelScraper()
    obj.scrap_data()

