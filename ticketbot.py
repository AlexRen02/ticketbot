from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import getpass
import time

# URL
url = 'https://www.ticketmaster.com/'
ticketweb = 'https://www.ticketweb.com/'

# Webdriver options
# Add later to run as background program
# options = webdriver.ChromeOptions()
# options.add_argument('headless')

# Open Chrome
driver = webdriver.Chrome(ChromeDriverManager().install())

# Login
def login(email, password):
    # Open URL    
    driver.get(url)
    time.sleep(1)

    # Open Login Page
    login_page = driver.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div[2]/div/nav/div/div[2]/div/span[1]/button')
    time.sleep(1)
    login_page.click()
    time.sleep(2)

    # Locate login fields
    email_box = driver.find_element_by_xpath('//*[@id="email[objectobject]__input"]')
    pass_box = driver.find_element_by_xpath('//*[@id="password[objectobject]__input"]')
    login_button = driver.find_element_by_xpath('//*[@id="scrollContent"]/div[3]/div[2]/button')
    
    # Login
    email_box.send_keys(email)
    pass_box.send_keys(password)
    time.sleep(2)
    login_button.click()

# Search for tickets
def ticket_search(location, start_date, end_date, artist):
    location_box = driver.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div[2]/div/section/div[1]/header/span/div[2]/div/div[1]/div[2]/div/div/div/div[1]/div/div/label/input')
    location_box.send_keys(location)
    time.sleep(1)

    date_dropdown = driver.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div[2]/div/section/div[1]/header/span/div[2]/div/div[1]/div[2]/div/div/div/div[2]/div/div/label')
    
    date_dropdown.click()
    time.sleep(1)

    date_range = driver.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div[2]/div/section/div[1]/header/span/div[2]/div/div[1]/div[2]/div[2]/div/div[1]/div[2]/div/div/div/div/span[3]')

    date_range.click()
    time.sleep(1)

    start_box = driver.find_element_by_xpath('//*[@id="startDate__input"]')
    end_box = driver.find_element_by_xpath('//*[@id="endDate__input"]')
    
    start_box.send_keys(start_date)
    end_box.send_keys(end_date)
    time.sleep(1)

    submit_button = driver.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div[2]/div/section/div[1]/header/span/div[2]/div/div[1]/div[3]/div/div/div[2]/div/div[2]/div/div/div[4]/div[2]/div[2]/button')
    submit_button.click()
    time.sleep(1)

    search_box = driver.find_element_by_xpath('//*[@id="SearchSuggestWithFilters"]/div[1]/input')
    search_box.send_keys(artist)
    time.sleep(1)

    search_button = driver.find_element_by_xpath('//*[@id="SearchSuggestWithFilters"]/div[2]/button')
    search_button.click()
    time.sleep(1)

    ticket_page = driver.find_element_by_xpath('//*[@id="tab--1"]/div/div[2]/div/div[1]/div/div[1]/div[2]/a')
    ticket_page.click()

# Ticketweb purchase tickets
def ticketweb_input_info(guests):
    select = False
    ticket_dropdown = driver.find_element_by_class_name('number theme-title theme-mod ng-binding')
    ticket_dropdown.click()

    number_selection = driver.find_elements_by_class_name('number theme-title ng-binding')
    while select == False:
        i = 0
        if int(number_selection[i].innerHTML) == guests:
            select = True
            number_selection[i].click()
        i += 1
    
    try:
        recaptcha = driver.find_element_by_xpath('//*[@id="recaptcha-anchor"]')
        recaptcha.click()
    except Exception:
        pass
    
    checkout_button = driver.find_element_by_xpath('//*[@id="edp_checkout_btn"]')
    checkout_button.click()

def main():
    # User Input Login Info
    email = input("Email:")
    password = getpass.getpass("Password:")

    # Ticket info
    location = input("Location:")
    start_date = input("Start date (MMDDYYYY):")
    end_date = input("End_date (MMDDYYYY):")
    artist = input("Search for artists, venues, and events:")
    guests = input("Number of guests:")
    
    login(email, password)
    ticket_search(location, start_date, end_date, artist)
    ticketweb_input_info(guests)
    
if __name__ == '__main__':
    main()