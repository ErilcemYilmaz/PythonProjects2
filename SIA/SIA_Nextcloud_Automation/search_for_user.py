import csv
import os
import time

import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

load_dotenv()

username = os.environ["USERNAME_CLOUD"]
password = os.environ["PASSWORD_CLOUD"]


def read_new_user_list(csv_file):
    # na_filter=False to prevent empty strings from being read as NaN
    df = pd.read_csv(csv_file, delimiter=",", na_filter=False)
    df.columns = df.columns.str.strip()
    users = df.to_dict("records")
    return users


def login_nav_cloud(driver):
    driver.get("https://cloud.sia.ch/settings/users")
    username_field = driver.find_element("id", "user")
    password_field = driver.find_element("id", "password")
    login_button = driver.find_element(
        By.CSS_SELECTOR, "button[data-login-form-submit]"
    )
    login_button.click()

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()


def search_for_active_user(driver, user):

    menu_button = driver.find_element("id", "user-menu")
    menu_button.click()

    user_list = driver.find_element("id", "core_users")
    user_list.click()

    search_button = driver.find_element("id", "unified-search")
    search_button.click()

    search_input_field = driver.find_element("id", "unified-search__input")
    search_input_field.click()

    search_input_field.send_keys(user["member_id"])
    time.sleep(2)

    try:
        result = driver.find_element(By.XPATH, "/html/body/div[3]/main/div/div[2]")
        print(str(user["member_id"]) + " is in the system")

    except:
        print(str(user["member_id"]) + " is not in the system")
        return
    # reulsts = (
    #     print("is already in the system")
    #     if driver.find_element("id", user["member_id"]) == user["member_id"]
    #     else print(user["member_id"] + " is not in the system")
    # )

    # if result:
    #     print(user["member_id"] + " is already in the system")
    # else:


def create_new_user(driver, user):
    menu_button = driver.find_element("id", "user-menu")
    menu_button.click()

    user_list = driver.find_element("id", "core_users")
    user_list.click()

    add_user_button = driver.find_element("id", "new-user-button")
    add_user_button.click()

    member_id_field = driver.find_element("id", "newusername")
    displayname_field = driver.find_element("id", "newdisplayname")
    email_field = driver.find_element("id", "newemail")
    group_field = driver.find_element(
        By.XPATH, "//input[@placeholder='Benutzer der Gruppe hinzufügen']"
    )

    member_id_field.send_keys(user["member_id"])
    displayname_field.send_keys(user["username"])
    email_field.send_keys(user["email"])
    if user["group"] != "" or None:
        group_field.send_keys(user["group"])
        group_field.send_keys(Keys.ENTER)

        email_field = driver.find_element("id", "newemail")
        email_field.click()

    create_button = driver.find_element("id", "newsubmit")
    create_button.click()


def main(input_csv):
    driver = webdriver.Chrome()

    login_nav_cloud(driver)
    users = read_new_user_list(input_csv)

    for user in users:

        print(user)
        search_for_active_user(driver, user)
        time.sleep(10)  # Optional: Add delay between user creations

    # Close the browser
    driver.quit()


if __name__ == "__main__":
    main()
