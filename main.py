import sys
import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui
import contextlib
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


import csgoWildCoinFlip

#declare globally visible variables
initialBet = 0
multiplier = 0
maxBet = 0

#stats
cumulativeGains = 0
numBets = 1

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
    global initialBet, multiplier, maxBet, userName

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
            elif "Username" in line:
                userName = line[10:]

    f.close()

    #confirms data
    print('Here are the current settings: \n')
    print('Initial Bet (float): %.2f' % initialBet)
    print('Loss Multiplier (float): %.2f' % multiplier)
    print('Max Bet (int): %d' % maxBet)
    print('Username (string): %s\n' % userName)
    response = input('Are you sure of these settings? (y/n): ')
    if ( response[0] != 'y' and response[0] != 'Y'):
        print('EXITING...\n')
        sys.exit

def gameWon( driver ):
    name = driver.find_element_by_id("winner-name").text
    if( userName in name ):
        return True
    else:
        return False


#==============================================================================
#main code
#==============================================================================

#get user settings and confirms
getSettings()

#instantiate betting website object
betPlatform = csgoWildCoinFlip.csgoWildCoinFlip()

#opens site
print('Opening %s' % betPlatform.url)

driver = webdriver.Firefox()
driver.maximize_window()

""" LOAD COOKIES...BUGGY
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

pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
"""

driver.get("http://" + betPlatform.url)
#start betting
input('\nSign in and press ENTER to get rich: ')

#initialize bet
side = betPlatform.chooseSide()
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

    #wait for bet to take place
    wait = ui.WebDriverWait(driver, 100000)
    wait.until(lambda driver: driver.find_element_by_class_name('ingame-coin'))

    if( gameWon( driver ) ):
        cumulativeGains += bet
        print("Bet #%d: you won $%d! |  Cumulative gains: $%d!\n" %
               (numBets, bet, cumulativeGains) )
        bet = initialBet
        side = betPlatform.chooseSide()
    else:
        cumulativeGains -= bet
        print("Bet #%d: you lost $%d! |  Cumulative gains: $%d!\n" %
              (numBets, bet, cumulativeGains ) )
        bet *= multiplier
    numBets++;

    driver.get("http://" + betPlatform.url)

    #checks for max bet condition
    if(bet > maxBet):
        break;

    driver.implicitly_wait(10)
