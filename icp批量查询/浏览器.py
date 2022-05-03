from selenium import webdriver

option = webdriver.ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])  # webdriver防检测
option.add_argument("--no-sandbox")
option.add_argument("--disable-dev-usage")
# option.add_argument('--headless')
option.add_argument('--disable-gpu')
option.add_argument("--disable-blink-features=AutomationControlled")
# driver = webdriver.Chrome(executable_path='tool/chromedriver.exe')

browser = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=option)

with open('icp.js', 'r') as f:
    js = f.read()

print(browser.execute_script(js))