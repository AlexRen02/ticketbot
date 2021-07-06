from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import getpass
import time

# URL
url = 'https://www.ticketmaster.com/'

# Open Chrome
driver = webdriver.Chrome(ChromeDriverManager().install())

# Login
def login():
    # User Input Login Info
    email = input("Email:")
    password = getpass.getpass("Password:")

    # Open URL    
    driver.get(url)

    # Wait for page to load
    time.sleep(1)

    # Open Login Page
    login_page = driver.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div[2]/div/nav/div/div[2]/div/span[1]/button')
    login_page.click()
    time.sleep(1)

    # Locate login fields
    email_box = driver.find_element_by_xpath('//*[@id="email[objectobject]__input"]')
    pass_box = driver.find_element_by_xpath('//*[@id="password[objectobject]__input"]')
    login_button = driver.find_element_by_xpath('//*[@id="scrollContent"]/div[3]/div[2]/button')
    
    # Login
    email_box.send_keys(email)
    pass_box.send_keys(password)
    login_button.click()

def main():
    login()
    
if __name__ == '__main__':
    main()