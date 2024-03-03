from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def scrape_instahyre_jobs(url):
    chrome_options = Options() # creating chrome options
    chrome_options.add_argument('--headless') #running chrome in headless mode (without GUI)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    
    wait = WebDriverWait(driver, 10)
    job_listings = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'employer-block')))
    
    job_data = [] # initializing an empty list to store job data
    
    for job in job_listings:
        try:
            name = job.find_element(By.CLASS_NAME, 'company-name').text.strip()
            location = job.find_element(By.CLASS_NAME, 'info').text.strip()
            
            founded = None
            employees = None
            about_text = None
            skills = []
            link = job.find_element(By.XPATH, './/a[@id="employer-profile-opportunity"]').get_attribute('href')
            
            # extracting necessary details
            details = job.find_elements(By.XPATH, ".//div[@class='employer-info']/*")
            for detail in details:
                if 'Founded' in detail.text:
                    founded = detail.text.strip()
                elif 'employees' in detail.text.lower():
                    employees = detail.text.strip()
            
            about = job.find_elements(By.XPATH, ".//div[@class='employer-notes ng-binding ng-scope']")
            if about:
                about_text = about[0].text.strip()
            
            skills_elements = job.find_elements(By.XPATH, ".//div[@class='job-skills ng-scope']//li")
            
            for skill in skills_elements:
                skills.append(skill.text)
            
            
            job_data.append({
                'Name': name,
                'Location': location,
                'Founded': founded,
                'Employees': employees,
                'About': about_text,
                'Skills': ', '.join(skills),
                'Link': link
            })
        except Exception as e:
            print(f"Error: {e}")
    
    driver.quit()
    
    df = pd.DataFrame(job_data)
    df.to_csv('instahyre_jobs.csv', index=False)
    print('Data saved to instahyre_jobs.csv')

# job analysis scrape Instahyre
url = 'https://www.instahyre.com/python-jobs'

# scraping data and saving it to CSV
scrape_instahyre_jobs(url)
