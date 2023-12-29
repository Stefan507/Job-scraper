# Indeed Scraper
Indeed Scraper is a Python script that scrapes job openings from the Indeed website. It uses the Selenium library to automate the process of navigating through the website and extracting job details.

## Prerequisites
Before running the script, make sure you have the following installed:

- Python 3.x
- Selenium library
- Chrome web browser

## Installation
Clone the repository or download the script.
Install the required dependencies by running the following command:
pip install selenium
Make sure you have the Chrome web browser installed on your machine.
Usage
To use the Indeed Scraper, follow these steps:

Open the indeed_scraper.py file in a text editor.
Modify the following parameters in the IndeedScraper class constructor:
search_location: The location to search for job openings (e.g., "Den Haag").
job_title: The job title to search for (e.g., "Python developer").
pages_to_scrape: The number of pages to scrape.
Save the file.
Open a terminal or command prompt and navigate to the directory where the script is located.
Run the script using the following command:
python indeed_scraper.py
The script will start scraping job openings from the Indeed website and save the results in a JSON file named indeed_jobs.json.

## Output
The script will generate a JSON file named indeed_jobs.json that contains the scraped job data. The file will have the following structure:

{
  "date": "YYYY-MM-DD HH:MM:SS",
  "jobs": [
    {
      "posted_at": "Posted X days ago",
      "title": "Job title",
      "company_name": "Company name",
      "company_rating": "Company rating",
      "company_reviews": "Company reviews",
      "location": "Job location",
      "location_type": "Location type",
      "apply_link": "Apply link",
      "pay": "Job salary",
      "job_type": "Job type",
      "description": "Job description"
    },
    ...
  ]
}
## Contributing
Contributions to the Indeed Scraper project are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
The Indeed Scraper script was developed by Stefan. Special thanks to the authors of the Selenium library for providing a powerful tool for web scraping.