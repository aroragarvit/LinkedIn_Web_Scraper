from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsel import Selector
import csv
import time
import parameters
import email_parsser


driver = webdriver.Chrome(parameters.chrome_web_driver)
driver.get(parameters.linkedin_url)

# Login
username_input = driver.find_element(By.XPATH, "//*[@id='session_key']")
password_input = driver.find_element(By.XPATH, "//*[@id='session_password']")

username_input.send_keys(parameters.linkedin_username)
password_input.send_keys(parameters.linkedin_password)

login_button = driver.find_element(By.XPATH, "//*[@type='submit']")
login_button.click()

time.sleep(3)
driver.get("https://www.linkedin.com/in/john-brown-6517692/?originalSubdomain=il")
time.sleep(5)
email= email_parsser.parse_email_using_page_source(driver.page_source)
time.sleep(3)
print(email)

# Get company URLs
driver.get(parameters.linkedInnSearch)
time.sleep(3)

linkedin_urls = [url.get_attribute("href") for url in driver.find_elements_by_css_selector(".scaffold-finite-scroll__content li a")]
print("Links:", linkedin_urls)

# Extract data from profiles
data = []


for url in linkedin_urls:
    driver.get(url)
    time.sleep(5)

    # Parse email using page source
    email = email_parsser.parse_email_using_page_source(driver.page_source)

    # Extract person data using XPath selectors
    sel = Selector(text=driver.page_source)

    name = sel.xpath('normalize-space(//*[starts-with(@class, "text-heading-xlarge inline t-24 v-align-middle break-words")]/text())').get()
    job_title = sel.xpath('normalize-space(//*[starts-with(@class, "text-body-medium break-words")]/text())').get()
    company = sel.xpath('normalize-space(//*[starts-with(@aria-label, "Current company")]/text())').get()
    college = sel.xpath('normalize-space(//*[starts-with(@aria-label, "Education")]/text())').get()
    location = sel.xpath('normalize-space(//*[starts-with(@class, "text-body-small inline t-black--light break-words")]/text())').get()

    person_data = [name, job_title, company, college, location, url, email]
    data.append(person_data)

# Write data to CSV file
header = ['Name', 'Job Title', 'Company', 'College', 'Location', 'URL', 'Email']

with open(parameters.employee_details, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)

driver.quit()

