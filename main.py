from Reader import  Reader
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import datetime
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

rd = Reader()
rd.openExplorer()
path = rd.getPath()
df = pd.read_csv(path, sep = ";")

wkns = df.iloc[:, 2].to_list()

driver = webdriver.Chrome()


driver.get("https://www.ariva.de/user/login")

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="CONTENT"]/div[3]/form/table/tbody/tr/td[2]/input'))).send_keys("wild.marco@online.de")

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[8]/div[3]/form/input'))).click()

WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "username"))
    ).send_keys("wild.marco@online.de")

WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "password"))
    ).send_keys("#2021!qsT+_")

WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "submit"))
    ).click()

final_list = []
for wkn in wkns:
    try:
        driver.get("https://www.ariva.de")
    except:
        continue
    try:
        WebDriverWait(driver, 1).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "sp_message_iframe_909171"))
        )
    except:
        pass

    try:
        WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@title='Akzeptieren und weiter' and contains(@class, 'message-button')]"))
        ).click()
        driver.switch_to.default_content()
    except Exception as e:
        print("Fehler beim Finden oder Klicken des Cookie-Buttons:", e)

    try:
        suchfeld = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "main-search"))
        )
        # Suchbegriff in das Suchfeld eingeben
        suchfeld.send_keys(wkn)
    except:
        continue

    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main-search-search-icon"]'))).click()
    except:
        print("Suchbutton konnte nicht gedrückt werden!")
        continue
    time.sleep(1)
    try:
        url = driver.current_url[:-6]
        url_historie = url + "/kurse" + "/historische-kurse"
        driver.get(url_historie)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
    except:
        continue

    try:
        secu_input = soup.find('input', {'name': 'secu'})
        secu_id = secu_input.get('value')
    except:
        continue

    # print(soup.select(".snapshotInfo")[1].text.strip().split(":")[2])
    time.sleep(0.5)

    final_list.append([wkn, url, url_historie, secu_id])

dataframe = pd.DataFrame(final_list, columns=["WKN", "URL", "URL_Historie", "Secu_ID"])
# folder = os.path.dirname(__file__)
filename = "Ariva_" + datetime.datetime.strftime(datetime.datetime.now(), "%d.%m.%y_%H%M") + ".csv"
#dataframe.to_csv(os.path.join(folder, filename), sep=";", index = False, encoding = "utf-8")

dataframe.to_csv(os.path.join("//Master/F/User/Microsoft Excel/Privat/Börse/Ariva_Names/" + filename), sep=";", index = False, encoding = "utf-8")