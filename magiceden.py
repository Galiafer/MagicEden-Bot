import time
import os
import json
import pathlib
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from webdriver_manager.chrome import ChromeDriverManager


class MintBot():
    def __init__(self, config, translationConfig, language, isWindows):
        self.isWindows = isWindows
        self.config = config
        self.translationConfig = translationConfig
        self.language = language

    def initWallet(self, driver):
        phantomExtensionPage = driver.window_handles[1]
        mintPage = driver.window_handles[0]
        
        # Adding wallet to a wallet extension | Добавляем кошелек в расширение
        print(self.translationConfig[self.language]['statuses'][0])

        # Switch to Phantom extension window | Переключаемся на окно с расширением
        WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
        driver.switch_to.window(phantomExtensionPage)
        print(self.translationConfig[self.language]['event'])

        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(),'Use Secret Recovery Phrase')]")))
        _ = driver.find_element(
            By.XPATH, "//button[contains(text(),'Use Secret Recovery Phrase')]").click()
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//textarea[@placeholder='Secret phrase']")))
        _ = driver.find_element(
            By.XPATH, "//textarea[@placeholder='Secret phrase']").send_keys(self.config["seedPhrase"])
        _ = driver.find_element(
            By.XPATH, "//button[@class='sc-bdfBQB bzlPNH']").click()
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//input[@placeholder='Password']")))
        _ = driver.find_element(
            By.XPATH, "//input[@placeholder='Password']").send_keys(self.config["password"])
        _ = driver.find_element(
            By.XPATH, "//input[@placeholder='Confirm Password']").send_keys(self.config["password"])
        _ = driver.find_element(
            By.XPATH, "//input[@type='checkbox']").click()
        _ = driver.find_element(
            By.XPATH, "//button[@type='submit']").click()

        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(),'Continue')]")))
        continueButton = driver.find_element(
            By.XPATH, "//button[contains(text(),'Continue')]")
        # Pressing on Continue button | Нажимаем на кнопку Продолжить
        driver.execute_script("arguments[0].click();", continueButton)

        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(),'Finish')]")))
        finishInitializing = driver.find_element(
            By.XPATH, "//button[contains(text(),'Finish')]")
        # Finishing wallet initializing | Завершаем инициализацию кошелька
        driver.execute_script("arguments[0].click();", finishInitializing)

        print(self.translationConfig[self.language]['statuses'][1])
        driver.switch_to.window(mintPage)

    def selectWallet(self, driver):

        print(self.translationConfig[self.language]['statuses'][2])

        # Select Main Wallet | Выбираем основной кошелёк
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Select Wallet')]")))
        main_wallet = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Select Wallet')]")
        main_wallet.click()

        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(),'Phantom')]")))
        phantomExtension = driver.find_element(
            By.XPATH, "//button[contains(text(),'Phantom')]")
        phantomExtension.click()

        WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
        phantomExtensionPage = driver.window_handles[1]
        mintPage = driver.window_handles[0]

        driver.switch_to.window(phantomExtensionPage)

        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(),'Connect')]")))
        popup = driver.find_element(
            By.XPATH, "//button[contains(text(),'Connect')]")
        popup.click()
        driver.switch_to.window(mintPage)
        time.sleep(3)
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(),'I understand')]")))
        agreeButton = driver.find_element(
            By.XPATH, "//button[contains(text(),'I understand')]")
        agreeButton.click()
        print(self.translationConfig[self.language]['statuses'][3])

    def awaitMint(self, driver):
        # Waiting for Mint

        print(self.translationConfig[self.language]['statuses'][4])

        WebDriverWait(driver, 60 * 60 * 24).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Mint your token!')]")))
        print(self.translationConfig[self.language]['mint_button'])

        tries = self.config['project_settings']['tries']  # Default is 10 | Стандартное значение 10
        while tries < 10:
            mintButton = driver.find_element(
                By.XPATH, "//button[contains(text(), 'Mint your token!')]")
            driver.execute_script("arguments[0].click();", mintButton)
            print(self.translationConfig[self.language]['button'])

            original_window = driver.current_window_handle
            WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    driver.switch_to.window(window_handle)
                    break
            WebDriverWait(driver, 60).until(EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Approve')]")))
            approveButton = driver.find_element(
                By.XPATH, "//button[contains(text(), 'Approve')]")
            approveButton.click()
            tries += 1

    @staticmethod
    def getDriver() -> webdriver.Chrome:

        options = Options()

        options.add_extension("Phantom.crx")
        options.add_argument("--disable-gpu")

        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # options for chrome install | Разрешение на установку расширения
        os.environ['WDM8LOCAL'] = '1'

        driver = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(), options=options)
        return driver

    def start(self):

        print(self.translationConfig[self.language]['start'])
        if self.isWindows:
            print("OS : Windows")
        else:
            print("OS : Mac")

        driver = self.getDriver()
        print(self.translationConfig[self.language]['assertion'])

        # open the launchpad page
        driver.get(self.config['launchpadLink'])
        driver.maximize_window()

        self.initWallet(driver)
        self.selectWallet(driver)
        self.awaitMint(driver)

        print(self.translationConfig[self.language]['finish'])
        if self.config['project_settings']['close_browser_after_mint']:
            driver.close()
