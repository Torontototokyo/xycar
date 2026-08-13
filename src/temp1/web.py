from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from paddleocr import PaddleOCR
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


ocr = PaddleOCR(use_angle_cls=True, lang="eng")
# Create Chrome options (optional but recommended)
options = Options()
options.add_argument("--start-maximized")      # Start with full screen
# options.add_argument("--headless")           # Run without opening browser (uncomment if needed)
options.add_experimental_option("detach", True)  # Keep browser open after script ends

# Create the WebDriver
driver = webdriver.Chrome(options=options)

login = "https://yun.jslife.com.cn/jportal/index.html#/login"

my_password = env('password')
my_username = env('username')
# Open a website
driver.get(login)

wait = WebDriverWait(driver, 10)


password = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
password.send_keys(my_password)

username = wait.until(EC.element_to_be_clickable((
    By.XPATH, 
    "//input[@placeholder='用户名']"
)))
username.send_keys(my_username)


## solve captcha

# Get captcha image src or element
img_element = wait.until(EC.presence_of_element_located((By.XPATH, "//img[@class='img-random']")))
img_url = img_element.get_attribute("src")

# Solve captcha
print("Solving captcha...")
result = solver.normal(img_url)

code = result['code']
print("Solved code:", code)

# for element in elements:
#     if element.text.strip() == "Exact Text Here":   # or .lower() for case insensitive
#         element.click()
#         print("Clicked successfully!")
#         break
# else:
#     print("Element not found")



print("Chrome WebDriver created successfully!")