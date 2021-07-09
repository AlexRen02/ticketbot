# Selenium Libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException   
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options

# Recaptcha libraries
import speech_recognition as sr
import ffmpy
import requests
import urllib
import pydub

# System libraries
import os
import random
import getpass
import time

# URL
#url = 'https://www.ticketmaster.com/'
url = 'https://www.google.com/recaptcha/api2/demo'
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
    delay()

    # Open Login Page
    login_page = driver.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div[2]/div/nav/div/div[2]/div/span[1]/button')
    delay()
    login_page.click()
    delay()

    # Locate login fields
    email_box = driver.find_element_by_xpath('//*[@id="email[objectobject]__input"]')
    pass_box = driver.find_element_by_xpath('//*[@id="password[objectobject]__input"]')
    login_button = driver.find_element_by_xpath('//*[@id="scrollContent"]/div[3]/div[2]/button')
    
    # Login
    email_box.send_keys(email)
    pass_box.send_keys(password)
    delay()
    login_button.click()

# Search for tickets
def ticket_search(location, start_date, end_date, artist):
    # Find location search box
    location_box = driver.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div[2]/div/section/div[1]/header/span/div[2]/div/div[1]/div[2]/div/div/div/div[1]/div/div/label/input')
    
    # Input location to be searched
    location_box.send_keys(location)
    delay()

    # Find date search dropdown
    date_dropdown = driver.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div[2]/div/section/div[1]/header/span/div[2]/div/div[1]/div[2]/div/div/div/div[2]/div/div/label')
    
    # Click on date dropdown
    date_dropdown.click()
    delay()

    # Find date range search
    date_range = driver.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div[2]/div/section/div[1]/header/span/div[2]/div/div[1]/div[2]/div[2]/div/div[1]/div[2]/div/div/div/div/span[3]')

    # Click on date range search
    date_range.click()
    delay()

    # Find start date and end date search boxes
    start_box = driver.find_element_by_xpath('//*[@id="startDate__input"]')
    end_box = driver.find_element_by_xpath('//*[@id="endDate__input"]')
    
    # Input start date and end date
    start_box.send_keys(start_date)
    end_box.send_keys(end_date)
    delay()

    # Find date submit button
    submit_button = driver.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div[2]/div/section/div[1]/header/span/div[2]/div/div[1]/div[3]/div/div/div[2]/div/div[2]/div/div/div[4]/div[2]/div[2]/button')
    submit_button.click()
    delay()

    # Find main search box
    search_box = driver.find_element_by_xpath('//*[@id="SearchSuggestWithFilters"]/div[1]/input')
    
    # Search for event
    search_box.send_keys(artist)
    delay()

    # Find search button
    search_button = driver.find_element_by_xpath('//*[@id="SearchSuggestWithFilters"]/div[2]/button')
    
    # Click on search button
    search_button.click()
    delay()

    # Select top ticket match
    ticket_page = driver.find_element_by_xpath('//*[@id="tab--1"]/div/div[2]/div/div[1]/div/div[1]/div[2]/a')
    ticket_page.click()

# Ticketweb purchase tickets
def ticketweb_input_info(guests):
    # Find increase ticket count button
    ticket_add = driver.find_elements_by_class_name('btn-circle')[1]

    # Get current ticket total
    num_tickets = int(driver.find_element_by_xpath('//span[@class="number theme-title theme-mod ng-binding"]').get_attribute('innerHTML'))
    
    # Add tickets until correct number is added
    while num_tickets != guests:
        ticket_add.click()
        num_tickets = int(driver.find_element_by_xpath('//span[@class="number theme-title theme-mod ng-binding"]').get_attribute('innerHTML'))
    delay()

    # Solve recaptcha if exists
    try:
        recaptcha_solver()
    except Exception:
        pass
    driver.switch_to.default_content()
    delay()

    # Go to checkout
    checkout_button = driver.find_element_by_xpath('//*[@id="edp_checkout_btn"]')
    checkout_button.click()

def recaptcha_solver():
    #switch to recaptcha frame
    frames=driver.find_elements_by_tag_name("iframe")
    driver.switch_to.frame(frames[0])
    delay()

    #click on checkbox to activate recaptcha
    recaptcha = driver.find_element_by_xpath('//*[@id="recaptcha-anchor"]')
    recaptcha.click()
    delay()

    #switch to recaptcha audio control frame
    driver.switch_to.default_content()
    frames=driver.find_elements_by_xpath("//iframe[@title='recaptcha challenge']")
    driver.switch_to.frame(frames[0])
    delay()

    #click on audio challenge
    driver.find_element_by_id("recaptcha-audio-button").click()
    
    #switch to recaptcha audio challenge frame
    driver.switch_to.default_content()
    frames= driver.find_elements_by_tag_name("iframe")
    driver.switch_to.frame(frames[-1])
    delay()

    #click on the play button
    driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button").click()

    #get the mp3 audio file
    src = driver.find_element_by_id("audio-source").get_attribute("src")
    print("[INFO] Audio src: %s"%src)

    #download the mp3 audio file from the source
    urllib.request.urlretrieve(src, os.getcwd()+"\\sample.mp3")
    delay()

    #Convert from MP3 to WAV
    # Error
    sound = pydub.AudioSegment.from_mp3(os.getcwd()+"\\sample.mp3")
    sound.export(os.getcwd()+"\\sample.wav", format="wav")
    sample_audio = sr.AudioFile(os.getcwd()+"\\sample.wav")

    #translate audio to text with google voice recognition
    key=sr.recognize_google(sample_audio)
    print("[INFO] Recaptcha Passcode: %s"%key)

    #key in results and submit
    driver.find_element_by_id("audio-response").send_keys(key.lower())
    driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
    driver.switch_to.default_content()
    delay()
    driver.find_element_by_id("recaptcha-demo-submit").click()
    delay()

def delay ():
    time.sleep(random.randint(2,3))

def main():
    driver.get(url)
    # User Input Login Info
    #email = input("Email:")
    #password = getpass.getpass("Password:")

    # Ticket info
    #location = input("Location:")
    #start_date = input("Start date (MMDDYYYY):")
    #end_date = input("End_date (MMDDYYYY):")
    #artist = input("Search for artists, venues, and events:")
    #guests = int(input("Number of guests:"))
    
    #login(email, password)
    #ticket_search(location, start_date, end_date, artist)
    #ticketweb_input_info(guests)\
    recaptcha_solver()
    
if __name__ == '__main__':
    main()