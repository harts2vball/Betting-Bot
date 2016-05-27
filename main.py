import sys
import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


import csgoWildCoinFlip

#declare globally visible variables
initialBet = 0
multiplier = 0
maxBet = 0

dummy_url = '/404error'

#==============================================================================
#helper methods
#==============================================================================

"""
This method reads in the settings from Settings.txt and
confirms them with the user.
"""
def getSettings():

    #define global vars to edit
    global initialBet, multiplier, maxBet

    #open file and read data
    with open('Settings.txt', 'r') as f:
        for line in f:
            if "Initial Bet" in line:
                list = re.findall('\d+', line)
                initialBet = float(list[0])
            elif "Loss Multiplier" in line:
                list = re.findall('\d+', line)
                multiplier = float(list[0])
            elif "Maximum Bet" in line:
                list = re.findall('\d+', line)
                maxBet = int(list[0])
    f.close()

    #confirms data
    print('Here are the current settings: \n')
    print('Initial Bet (float): %.2f' % initialBet)
    print('Loss Multiplier (float): %.2f' % multiplier)
    print('Max Bet (int): %d\n' % maxBet)
    response = input('Are you sure of these settings? (y/n): ')
    if ( response[0] != 'y' and response[0] != 'Y'):
        print('EXITING...\n')
        sys.exit


#==============================================================================
#main code
#==============================================================================

#get user settings and confirms
getSettings()

#instantiate betting website object
bet = csgoWildCoinFlip.csgoWildCoinFlip()

#opens site
print('Opening %s' % bet.url)

profile = webdriver.FirefoxProfile(
    r"""C:\Users\Charlay\AppData\Roaming\Mozilla\Firefox\Profiles\nz1v5nfx.Selenium""")
driver = webdriver.Firefox(profile)
driver.maximize_window()

driver.get("http://" + bet.url + dummy_url)
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    try:
        driver.add_cookie(cookie)
    except Exception:
        print()

driver.get("https://steamcommunity.com/" + dummy_url)
for cookie in cookies:
    try:
        driver.add_cookie(cookie)
    except Exception:
        print()

driver.get("http://" + bet.url)


#start betting
input('\nSign in and press ENTER to continue: ')

pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

#initialize bet
side = bet.chooseSide()
bet = initialBet

while True:

#1. ALWAYS STARTS ON MAIN COIN FLIP PAGE

    #clicks on create game
    driver.find_element_by_xpath("""//*[@id="create-game-action"]""").click()

    #clicks on either t or ct based on side
    if(side == 0):
        driver.find_element_by_xpath("""// *[ @ id = "terrorist-popup"]
        """).click()
    else:
        driver.find_element_by_xpath("""// *[ @ id = "counterterrorist-popup"]
        """).click()

    #bet the proper amount
    action = ActionChains(driver)
    driver.implicitly_wait(100)
    textBox = driver.find_element_by_class_name("wager-input")
    textBox.click()
    textBox.send_keys(Keys.BACK_SPACE)
    textBox.send_keys(Keys.BACK_SPACE)
    textBox.send_keys(Keys.BACK_SPACE)
    textBox.send_keys(Keys.BACK_SPACE)
    textBox.send_keys(Keys.BACK_SPACE)
    textBox.send_keys(Keys.BACK_SPACE)
    textBox.send_keys(str(bet))
    textBox = driver.find_element_by_class_name("primary-button")
    textBox.click()


    break;

