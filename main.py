import re
import sys
from selenium import webdriver
import selenium

import csgoWildCoinFlip

#declare globally visible variables
initialBet = 0
multiplier = 0
maxBet = 0


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

#opens site in chrome
print('Opening %s' % bet.url)


driver = webdriver.Chrome("chromedriver.exe")
driver.get("http://" + bet.url)
driver.set_window_size(1850, 950)

#opens steam login
driver.find_element_by_css_selector("""href title="Sign In"]""").click()

input('\nSign in and press ENTER to continue: ')

#betting script
#while(true):

side = bet.chooseSide()
bet = initialBet



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
box = driver.find_element_by_class_name("""wager-input ember-view ember-text-field""")
box.clear()


