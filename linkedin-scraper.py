import random
import time
from datetime import datetime
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

# Does not work, gonna fix this later

class LinkedinScraper:

    def __init__(self, search_location: str, job_title: str, job_offers_to_scrape: int):
        
        self.search_location = search_location
        self.job_title = job_title
        self.job_offers_to_scrape = job_offers_to_scrape


        if ' ' in search_location:
            search_location = search_location.replace(" ", "%2B")
        if ' ' in job_title:
            job_title = job_title.replace(" ", "%20")
        
        url = (f"https://www.linkedin.com/jobs/search?keywords={job_title}&location={search_location}&trk=public_jobs_jobs-search-bar_search-submit&currentJobId=3786032585&position=1&pageNum=0")
        print(url)
        try:
            # set up a controllable Chrome instance
            # in headless mode
            service = Service()
            options = webdriver.ChromeOptions()
            # options.add_argument("--headless=new")
            options.add_argument("--incognito")
            driver = webdriver.Chrome(
                service=service,
                options=options
            )
            print("Webdriver initialized")

            while True:
                # open the target page in the browser
                driver.get(url)
                print("URL succesfully opened")

                # Check if the current page is the login page
                if "Redirect" in driver.current_url:
                    print("Redirected to sign-up page. Retrying...")
                    time.sleep(5)  # Wait for a few seconds
                    driver.get(url)  # Refresh the page
                else:
                    break  # Break out of the loop if the correct page is loaded

            # set the window size to make sure pages will not be rendered in responsive mode
            driver.set_window_size(1920, 1080)
        except WebDriverException as e:
            print(f"Error: {e}")

        # make a data structure to store job openings
        jobs = []

        job_offers_scraped = 0
        
        while job_offers_scraped < job_offers_to_scrape:
            
            job_cards = driver.find_elements(By.CLASS_NAME, "base-card__full-link")

            for job_card in job_cards:
                # initialize a dictionary to store the scraped job data
                job = {}

                # initialize the job attributes to scrape
                posted_at = None
                title = None
                company_name = None
                location = None
                apply_link = None
                applicants = None
                job_type = None
                description = None
                seniority_level = None
                job_function = None

                WebDriverWait(driver, 4)
                # TODO: Close all pop_ups that appear
                try:
                    sign_in_element = driver.find_element(By.XPATH, '/html/body/div[5]')
                    sign_in_button = sign_in_element.find_element(By.XPATH, '/html/body/div[5]/button')
                    driver.implicitly_wait(2)
                    sign_in_button.click()
                except NoSuchElementException:
                    pass

                try:
                    cookie_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div/div[2]')
                    cookie_button = cookie_element.find_element(By.XPATH, '/html/body/div[1]/div/section/div/div[2]/button[2]')
                    cookie_button.click()
                except NoSuchElementException:
                    pass

                # click on the list item
                # driver.execute_script("arguments[0].scrollIntoView();", job_card)
                WebDriverWait(driver, 3)
                job_card.click()

                # Expand the information displayed
                # try:    
                #     show_more_element = driver.find_element(By.XPATH, '/html/body/div[3]/div/section/div[2]/div/section[1]/div/div')
                #     show_more_button = show_more_element.find_element(By.XPATH, '/html/body/div[3]/div/section/div[2]/div/section[1]/div/div/section/button[1]/icon')
                #     show_more_button.click()
                #     # WebDriverWait(driver, 4)
                # except NoSuchElementException:
                #     pass

                # wait for the job details to load after the click
                try:
                    title_element = driver.find_element(By.XPATH,  "/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/a/h2") #'/html/body/div[3]/div/section/div[2]/section/div/div[1]/div/a/h2')
                    title = title_element.text                                                                                          
                except NoSuchElementException:                      
                    continue

                # Get the data from the header
                try:
                    header_element = driver.find_element(By.XPATH, '/html/body/div[3]/div/section/div[2]/section/div/div[1]/div')
                    posted_at_element = header_element.find_element(By.XPATH, '/html/body/div[3]/div/section/div[2]/section/div/div[1]/div/h4/div[2]/span')
                    posted_at = posted_at_element.text
                    company_name_element = header_element.find_element(By.XPATH, '/html/body/div[3]/div/section/div[2]/section/div/div[1]/div/h4/div[1]/span[1]/a')
                    company_name = company_name_element.text
                    location = header_element.find_element(By.CLASS_NAME, "topcard__flavor topcard__flavor--bullet").text
                    apply_link = header_element.find_element(By.ID, "applyUrl").get_attribute("textContent")
                    applicants = header_element.find_element(By.CLASS_NAME, "num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet").text
                    if applicants == "Be among the first 25 applicants":
                        applicants = ">25"
                except NoSuchElementException:
                    pass

                # try:
                #     posted_at = header_element.find_element(By.CLASS_NAME, "posted-time-ago__text topcard__flavor--metadata").text
                # except NoSuchElementException:
                #     pass

                # try:
                #     company_name = header_element.find_element(By.CLASS_NAME, "topcard__org-name-link topcard__flavor--black-link").text
                # except NoSuchElementException:
                #     pass
                    
                # try:
                #     location = header_element.find_element(By.CLASS_NAME, "topcard__flavor topcard__flavor--bullet").text
                # except NoSuchElementException:
                #     pass

                # try:
                #     apply_link = header_element.find_element(By.ID, "applyUrl").get_attribute("textContent")
                # except NoSuchElementException:
                #     pass

                # try:
                #     applicants = header_element.find_element(By.CLASS_NAME, "num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet").text
                #     if applicants == "Be among the first 25 applicants":
                #         applicants = ">25"
                # except NoSuchElementException:
                #     pass

                try:
                    description_element = driver.find_element(By.CLASS_NAME, "description__text description__text--rich")
                    description = description_element.text
                except NoSuchElementException:
                    pass

                try:
                    extra_info_element = driver.find_element(By.CLASS_NAME, "description__job-criteria-list")
                    job_type = extra_info_element.find_element(By.CLASS_NAME, "description__job-criteria-text description__job-criteria-text--criteria").text
                    seniority_level = extra_info_element.find_element(By.CLASS_NAME, "description__job-criteria-text description__job-criteria-text--criteria").text
                    job_function = extra_info_element.find_element(By.CLASS_NAME, "description__job-criteria-text description__job-criteria-text--criteria").text
                except NoSuchElementException:
                    pass


                # Store the scraped data
                job["posted_at"] = posted_at 
                job["title"] = title
                job["function"] = job_function
                job["company_name"] = company_name 
                job["location"] = location
                job["apply_link"] = apply_link 
                job["applicants"] = applicants
                job["job_type"] = job_type
                job["description"] = description
                job["seniority_level"] = seniority_level
                jobs.append(job)
                job_offers_scraped += 1

                # Wait for a random number of seconds to avoid blocks
                time.sleep(random.uniform(1, 5))

                if job_offers_scraped >= int(job_offers_to_scrape):
                    break

        # close the browser and free up resources
        driver.quit()

        # Produce the output object
        output = {
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "jobs": jobs
        }

        # export it to JSON
        with open("linkedin_jobs.json", "w", encoding="utf-8") as file:
            json.dump(output, file, indent=4)

LinkedinScraper("den haag", "python developer", 2)