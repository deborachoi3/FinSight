from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def auto_login(url, username, password):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)

    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

    print("Logged in successfully")
    driver.quit()
