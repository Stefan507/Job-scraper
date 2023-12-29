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

class IndeedScraper:

    def __init__(self, search_location, job_title, pages_to_scrape):

        self.search_location = search_location
        self.job_title = job_title
        self.pages_to_scrape = pages_to_scrape

        try:
            # set up a controllable Chrome instance
            # in headless mode
            service = Service()
            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")
            driver = webdriver.Chrome(
                service=service,
                # options=options
            )

            # open the target page  in the browser
            driver.get(f"https://nl.indeed.com/vacatures?q={job_title}&l={search_location}&lang=nl")
            # set the window size to make sure pages
            # will not be rendered in responsive mode
            driver.set_window_size(1920, 1080)
        except WebDriverException as e:
            print(f"Error: {e}")

        # a data structure where to store the job openings
        # scraped from the page
        jobs = []

        pages_scraped = 0
        jobs_counter = 0

        while pages_scraped < pages_to_scrape:
            # select the job posting cards on the page
            job_cards = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")

            for job_card in job_cards:
                # initialize a dictionary to store the scraped job data
                job = {}

                # initialize the job attributes to scrape
                posted_at = None
                title = None
                company_name = None
                company_rating = None
                company_reviews = None
                location = None
                location_type = None
                apply_link = None
                pay = None
                job_type = None
                description = None

                # close the google pop_up
                try:
                    dialog_element_google = driver.find_element(By.CLASS_NAME, "icl-Card")
                    close_button_google = dialog_element_google.find_element\
                        (By.CLASS_NAME, "icl-CloseButton icl-Card-close")
                    close_button_google.click()
                except NoSuchElementException:
                    pass

                # close the anti-scraping modal
                try:
                    dialog_element = driver.find_element(By.ID, "mosaic-desktopserpjapopup")
                    close_button = dialog_element.find_element(By.CSS_SELECTOR, "[aria-label='sluiten']")
                    close_button.click()
                except NoSuchElementException:
                    pass

                # get the general job data from the outline card
                try:
                    date_element = job_card.find_element(By.CSS_SELECTOR, ".date")
                    date_element_text = date_element.text
                    posted_at_text = date_element_text

                    if "•" in date_element_text:
                        date_element_text_array = date_element_text.split("•")
                        posted_at_text = date_element_text_array[0]

                    posted_at = posted_at_text \
                        .replace("Posted", "") \
                        .replace("Employer", "") \
                        .replace("Active", "") \
                        .strip()
                except NoSuchElementException:
                    pass


                # scroll the card in view
                driver.execute_script("arguments[0].scrollIntoView();", job_card)
                # load the job details card
                job_card.click()

                # wait for the job details section to load after the click
                try:
                    title_element = WebDriverWait(driver, 5) \
                        .until(EC.presence_of_element_located \
                            ((By.CSS_SELECTOR, ".jobsearch-JobInfoHeader-title")))
                    title = title_element.text.replace("\n- job post", "")
                except NoSuchElementException:
                    continue

                # extract the job details
                job_details_element = driver.find_element(By.CSS_SELECTOR, ".jobsearch-RightPane")

                try:
                    company_link_element = job_details_element.find_element \
                        (By.CSS_SELECTOR, "div[data-company-name='true'] a")
                    company_name = company_link_element.text
                except NoSuchElementException:
                    pass


                try:
                    company_rating_element = job_details_element.find_element \
                        (By.CSS_SELECTOR, "[data-testid='jobsearch-CompanyInfoContainer']")
                    company_rating = driver.find_element(By.CLASS_NAME, 'css-ln09g1').get_attribute('aria-label')
                    company_reviews_element = job_details_element.find_element \
                        (By.CSS_SELECTOR, "[data-testid='inlineHeader-companyReviewLink']")
                    company_reviews = company_reviews_element.text.replace(" reviews", "")
                except NoSuchElementException:
                    pass

                try:
                    company_location_element = job_details_element.find_element \
                        (By.CSS_SELECTOR, "[data-testid='inlineHeader-companyLocation']")
                    company_location_element_text = company_location_element.text

                    location = company_location_element_text

                    if "•" in company_location_element_text:
                        company_location_element_text_array = company_location_element_text.split("•")
                        location = company_location_element_text_array[0]
                        location_type = company_location_element_text_array[1]
                except NoSuchElementException:
                    pass

                try:
                    apply_link_element = job_details_element.find_element \
                        (By.CSS_SELECTOR, "#applyButtonLinkContainer button")
                    apply_link = apply_link_element.get_attribute("href")
                except NoSuchElementException:
                    pass

                for div in job_details_element.find_elements(By.CSS_SELECTOR, "#jobDetailsSection div"):
                    if div.text == "Salaris":
                        pay_element = div.find_element(By.XPATH, "following-sibling::*")
                        pay = pay_element.text
                    elif div.text == "Dienstverband":
                        job_type_element = div.find_element(By.XPATH, "following-sibling::*")
                        job_type = job_type_element.text

                try:
                    description_element = job_details_element.find_element(By.ID, "jobDescriptionText")
                    description = description_element.text
                except NoSuchElementException:
                    pass

                # store the scraped data
                job["posted_at"] = posted_at
                job["title"] = title
                job["company_name"] = company_name
                job["company_rating"] = company_rating
                job["company_reviews"] = company_reviews
                job["location"] = location
                job["location_type"] = location_type
                job["apply_link"] = apply_link
                job["pay"] = pay
                job["job_type"] = job_type
                job["description"] = description
                jobs.append(job)
                jobs_counter += 1

                # wait for a random number of seconds from 1 to 5
                # to avoid rate limiting blocks
                time.sleep(random.uniform(1, 5))

            # increment the scraping counter
            pages_scraped += 1

            # if this is not the last page, go to the next page
            # otherwise, break the while loop
            try:
                next_page_element = driver.find_element\
                    (By.CSS_SELECTOR, "[data-testid='pagination-page-next']")
                next_page_element.click()
            except NoSuchElementException:
                break

        # close the browser and free up the resources
        driver.quit()

        # produce the output object
        output = {
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "jobs": jobs
        }

        # export it to JSON
        with open("indeed_jobs.json", "w", encoding="utf-8") as file:
            json.dump(output, file, indent=4)

IndeedScraper("Den Haag", "Python developer", 1)