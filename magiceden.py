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
    def __init__(self, config, elements, translationConfig, language):
        self.config = config
        self.elements = elements
        self.translationConfig = translationConfig
        self.language = language

    def initWallet(self, driver):
        print(self.translationConfig[self.language]['statuses'][0])

        driver.switch_to.window(driver.window_handles[1])
        print(self.translationConfig[self.language]['event'])

        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, self.elements['phantom']['importButton'])))
        driver.find_element(By.XPATH, self.elements['phantom']['importButton']).click()

        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@id='word_0']")))
        for i in range(0, 12):
            driver.find_element(By.XPATH, f"//*[@id='word_{i}']").send_keys(self.config["seedPhrase"].split(' ')[i])
        driver.find_element(By.XPATH, self.elements['phantom']['submitButton']).click()

        time.sleep(5)
        driver.find_element(By.XPATH, self.elements['phantom']['submitButton']).click()

        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, self.elements['phantom']['passwordField'])))
        driver.find_element(By.XPATH, self.elements['phantom']['passwordField']).send_keys(self.config["password"])
        driver.find_element(By.XPATH, self.elements['phantom']['confirmPasswordField']).send_keys(self.config["password"])
        driver.find_element(By.XPATH, self.elements['phantom']['checkbox']).click()
        driver.find_element(By.XPATH, self.elements['phantom']['submitButton']).click()

        time.sleep(5)
        driver.find_element(By.XPATH, self.elements['phantom']['continueButton']).click()

        time.sleep(5)
        driver.find_element(By.XPATH, self.elements['phantom']['continueButton']).click()

        print(self.translationConfig[self.language]['statuses'][1])
        driver.switch_to.window(driver.window_handles[0])

    def selectWallet(self, driver):

        print(self.translationConfig[self.language]['statuses'][2])

        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, self.elements['magiceden']['connectWallet'])))
        main_wallet = driver.find_element(By.XPATH, self.elements['magiceden']['connectWallet'])
        main_wallet.click()

        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, self.elements['magiceden']['phantomWallet'])))
        phantomExtension = driver.find_element(By.XPATH, self.elements['magiceden']['phantomWallet'])
        phantomExtension.click()

        WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
        # phantomExtensionPage = driver.window_handles[1]
        # mintPage = driver.window_handles[0]

        driver.switch_to.window(driver.window_handles[1])

        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, self.elements['magiceden']['popup']['connectButton'])))
        popup = driver.find_element(By.XPATH, self.elements['magiceden']['popup']['connectButton'])
        popup.click()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(3)
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, self.elements['magiceden']['understandButton'])))
        agreeButton = driver.find_element(By.XPATH, self.elements['magiceden']['understandButton'])
        agreeButton.click()
        print(self.translationConfig[self.language]['statuses'][3])

    def awaitMint(self, driver):

        print(self.translationConfig[self.language]['statuses'][4])

        WebDriverWait(driver, 60 * 60 * 24).until(EC.presence_of_element_located((By.XPATH, self.elements['magiceden']['mintButton'])))
        print(self.translationConfig[self.language]['mint_button'])

        tries = self.config['project_settings']['tries']  # Default is 10 | Стандартное значение 10
        count = 0
        while count < tries:
            while True:
                mintButton = driver.find_element(By.XPATH, self.elements['magiceden']['mintButton'])
                driver.execute_script("arguments[0].click();", mintButton)

                if len(driver.window_handles) == 2:
                    break

            original_window = driver.current_window_handle
            WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    driver.switch_to.window(window_handle)
                    break
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, self.elements['magiceden']['popup']['approveButton'])))
            approveButton = driver.find_element(By.XPATH, self.elements['magiceden']['popup']['approveButton'])
            approveButton.click()
            count += 1

    @staticmethod
    def getDriver() -> webdriver.Chrome:

        options = Options()

        options.add_extension("Phantom.crx")
        options.add_argument("--disable-gpu")

        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        os.environ['WDM8LOCAL'] = '1'

        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
        return driver

    def start(self):

        print(self.translationConfig[self.language]['start'])

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
