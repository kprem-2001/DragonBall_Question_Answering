from bs4 import BeautifulSoup
import requests
import re
import os
import sys
from dataclasses import dataclass

from src.logger import logging
from src.exceptions import CustomException

@dataclass
class DataIngestionConfig:
    raw_data_path : str 
    clean_data_path :str 
    scraping_url: str = "https://dragonball.fandom.com/wiki/Special:AllPages"
    base_url : str ="https://dragonball.fandom.com"
    nav_tag: str = "mw-allpages-nav"
    body_tag: str = "mw-allpages-body"
    output_tag: str = "mw-parser-output"
    
class DataIngestion:
    def __init__(self , raw_data_path:str , clean_data_path :str):
        self.ingestion_config = DataIngestionConfig(raw_data_path= raw_data_path , clean_data_path= clean_data_path)
        
    def initiate_data_ingestion(self):
        logging.info("Initialized Data Ingestion")
        
        try:
           # self.initiate_data_scraping()
            self.initiate_data_cleaning()
            
            logging.info("Data Ingestion Completed")
            
            return (
                #self.ingestion_config.raw_data_path,
                self.ingestion_config.clean_data_path
            )
            
        except Exception as e:
            logging.error(e)
            raise CustomException(e,sys)
        
    def initiate_data_scraping(self):
        logging.info("Entered the Data Scraping method")
        
        try:
            response = requests.get(self.ingestion_config.scraping_url)
            if response.status_code != 200:
                logging.info("Could not connect to the SCRAPING URL: {}".format(self.ingestion_config.scraping_url))
                return
            
            soup = BeautifulSoup(response.text, 'html.parser')  # ✅ Fixed Initialization
            count = 0                    
            
            os.makedirs(self.ingestion_config.raw_data_path, exist_ok=True)
            while True:
                div_tag = soup.find('div', class_=self.ingestion_config.body_tag)
                if not div_tag:
                    logging.error(f"Could not find div with class: {self.ingestion_config.body_tag}")
                    break
                
                for tag in div_tag.find_all("a"):
                    title = re.sub(r"[^A-Za-z0-9]", "", tag["title"])  # ✅ Fixed regex
                    link = tag['href']
                    
                    with open(os.path.join(self.ingestion_config.raw_data_path, f'{title}.txt'), 'w', encoding='utf-8') as file:
                        page_response = requests.get(self.ingestion_config.base_url + link)
                        page_soup = BeautifulSoup(page_response.text, 'html.parser')
                        content_div = page_soup.find('div', class_=self.ingestion_config.output_tag)
                        if content_div:
                            for el in content_div.children:
                                if el.name in ['p', 'ul']:
                                    file.write(el.get_text())
                    
                    count += 1
                    if count % 500 == 0:
                        logging.info(f"Scraped {count} Data Articles")
                
                navs_div = soup.find('div', class_=self.ingestion_config.nav_tag)
                if not navs_div:
                    logging.info("No navigation div found, stopping scraping.")
                    break
                
                nav_links = navs_div.find_all('a')
                if not nav_links or 'Previous page' in nav_links[-1].text:
                    break  # Stop when there's no next page
                
                response = requests.get(self.ingestion_config.base_url + nav_links[-1]['href'])
                soup = BeautifulSoup(response.text, 'html.parser')
            
            logging.info(f'Total {count} data articles are scraped')
            logging.info('Scraping of data is completed')

            return (
                self.ingestion_config.raw_data_path,
                self.ingestion_config.clean_data_path
            )
                        
        except Exception as e:
            logging.error(e)
            raise CustomException(e, sys)

    
    
    def initiate_data_cleaning(self):
        '''
        Clean the scraped data in the raw data folder in the artifacts location
        Params:
            None
        Returns:
            Path to scraped data: str
            Path to cleaned data: str
        '''
        logging.info('Entered the data cleaning method or component.')
        
        try:
            count = 0
            
            os.makedirs(self.ingestion_config.clean_data_path, exist_ok=True)
            for filename in os.listdir(self.ingestion_config.raw_data_path):
                filepath = os.path.join(self.ingestion_config.raw_data_path, filename)
                with open(filepath, 'r', encoding='utf-8') as raw_file:
                    raw_data = raw_file.readlines()
                    
                data = [re.sub(r"\s+", " ", i) for i in raw_data if i != '\n']
                
                with open(os.path.join(self.ingestion_config.clean_data_path, filename), 'w', encoding='utf-8') as clean_file:
                    clean_file.writelines(data)
                    
                count += 1
                if count%500 == 0:
                    logging.info("Cleaned {} Data Articles".format(count))
            
            logging.info(f"Total {count} data articles are cleaned")
            logging.info("Data Cleaning is completed")
            
            return (
                self.ingestion_config.raw_data_path,
                self.ingestion_config.clean_data_path
            )
                    
        except Exception as e:
            raise CustomException(e, sys)