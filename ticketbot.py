from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

# URL
url = 
# Open Chrome
driver = webdriver.Chrome(ChromeDriverManager().install())

# Open URL    
driver.get(url)