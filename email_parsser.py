import re
import time
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsel import Selector
import csv
import time
import parameters

url = "https://www.linkedin.com/in/john-brown-6517692/?originalSubdomain=il"
EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""


def parse_email(url):
    session = HTMLSession()
    r = session.get(url)
    try:
        r.html.render(wait=2, retries=2)
    except:
        time.sleep(5)
        r.html.render(wait=2, retries=2)

    for re_match in re.finditer(EMAIL_REGEX, r.html.raw_html.decode()):
        return re_match.group()


def parse_email_using_page_source(page):
    sel = Selector(text=page)
    for re_match in re.finditer(EMAIL_REGEX, sel.get()):
        return re_match.group()

def login():
    driver = webdriver.Chrome(parameters.chrome_web_driver)
    driver.get(parameters.linkedin_url)
    time.sleep(2)
    

    username_input = driver.find_element(By.XPATH, "//*[@id='session_key']")
    password_input = driver.find_element(By.XPATH, "//*[@id='session_password']")
    
    username_input.send_keys(parameters.linkedin_username)
    password_input.send_keys(parameters.linkedin_password)
    
    login_button = driver.find_element(By.XPATH, "//*[@type='submit']")
    login_button.click()
    
    time.sleep(3)
    driver.get("https://www.linkedin.com/in/john-brown-6517692/?originalSubdomain=il")
    time.sleep(5)
    print(driver.page_source)
    print("--------------------------------------------------")
    print(parse_email_using_page_source(driver.page_source))
    print("--------------------------------------------------")
    print("--------------------------------------------------")
    
    print(parse_email(driver.current_url))
    print("--------------------------------------------------")
    

login()