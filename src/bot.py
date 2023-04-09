from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json
from datetime import datetime

def login_and_reviews(sleep_time, email, password):

    opt = Options()
    opt.add_argument("start-maximized")
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])

    # start driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opt)

    # login
    driver.get('https://silabs.hungerbox.com/#/login')
    time.sleep(sleep_time)

    # inputs email id and password
    driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/div[1]/form/md-input-container[1]/input').send_keys(email)
    driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/div[1]/form/md-input-container[2]/input').send_keys(password)
    driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/div[3]/button').click()
    time.sleep(sleep_time)

    # review for breakfast
    try:
        # gives 4-star rating and clicks submit
        driver.find_element(by=By.XPATH, value='/html/body/div[8]/md-dialog/md-dialog-content/div[1]/div[3]/div[1]/div[3]/md-icon[4]').click()
        driver.find_element(by=By.XPATH, value='/html/body/div[8]/md-dialog/md-dialog-content/div[2]/div[2]').click()
        time.sleep(sleep_time)
    except:
        pass

    # review for lunch
    try:
        # gives 4-star rating and clicks submit
        driver.find_element(by=By.XPATH, value='/html/body/div[8]/md-dialog/md-dialog-content/div[1]/div[3]/div[1]/div[3]/md-icon[4]').click()
        driver.find_element(by=By.XPATH, value='/html/body/div[8]/md-dialog/md-dialog-content/div[2]/div[2]').click()
        time.sleep(sleep_time)
    except:
        pass

    return driver

def book(sleep_time, driver, dietary, meals):
    dayname = datetime.now().strftime('%a')

    # click on occasion
    driver.find_element(by=By.XPATH, value='/html/body/div[3]/div[1]/div[1]/div/div[8]/div[2]').click()

    # 0, for breakfast; 1, for lunch
    if meals == 0:
        # click on Pre-Order Breakfast
        driver.find_element(by=By.XPATH, value='/html/body/div[3]/div[1]/div[2]/div/div[2]/div[2]/div[2]/div[1]').click()
        time.sleep(sleep_time)
    elif meals == 1:
        # click on Pre-Order Lunch
        try:
            driver.find_element(by=By.XPATH, value='/html/body/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[1]').click()
        except:
            driver.find_element(by=By.XPATH, value='/html/body/div[3]/div[1]/div[2]/div/div[3]/div[2]/div[2]/div[1]').click()
        time.sleep(sleep_time)

    # click on main menu
    driver.find_element(by=By.XPATH, value='/html/body/div[3]/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div[2]/div/div[1]/div[1]').click()
    time.sleep(sleep_time)

    # click on add
    if(dietary == 0 and meals == 1 and (dayname == "Tue" or dayname == "Thu")):
        driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[3]/div[2]/div/div[3]/div[4]/div[2]/div/div[2]/div/menu-item/div/div[4]/button/span').click()
    else:
        driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[3]/div[2]/div/div[3]/div[4]/div[1]/div/div[2]/div/menu-item/div/div[4]/button/span').click()

    # click on view cart
    driver.find_element(by=By.XPATH, value='/html/body/div[4]/div/div/div[3]/div').click()
    time.sleep(sleep_time)

    # click on proceed to pay
    try:
        driver.find_element(by=By.XPATH, value='/html/body/div[3]/div[3]/div[2]/div[2]/div[2]/div[3]/button/span').click()
    except:
        driver.find_element(by=By.XPATH, value='/html/body/div[3]/div[3]/div[2]/div[2]/div[2]/div[2]/button/span').click()
    time.sleep(sleep_time)

def main():
    sleep_time = 5

    # loads the configuration json file
    with open(".\config\config.json", mode="r") as json_object:
        data = json.load(json_object)

    try:
        driver = login_and_reviews(sleep_time, data["email"], data["password"])

        # 0, for only breakfast; 1, for only lunch; 2, for both meals
        if data["meals"] == 0:
            book(sleep_time, driver, data["dietary"], 0)
        elif data["meals"] == 1:
            book(sleep_time, driver, data["dietary"], 1)
        elif data["meals"] == 2:
            book(sleep_time, driver, data["dietary"], 0)

            # click on back
            driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[1]/div/div[1]/div/button/md-icon').click()
            time.sleep(sleep_time)

            book(sleep_time, driver, data["dietary"], 1)

    finally:
        driver.quit()

    exit()

if __name__ == "__main__":
    main()