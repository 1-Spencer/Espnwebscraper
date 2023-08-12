from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
import os
import csv


class TestMethod:
    def test(self):
        teamname = ""
        driver = webdriver.Chrome(
            "/Users/spencerbaldwin/Desktop/vscodeProjects/Part-Picker-GamePlanner/Drivers/chromedriver_mac_arm64/chromedriver")
        driver.get("https://www.espn.com/college-football/players")
        # trying to keep chrome open
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        coding = SeleniumScraper(driver)
        
        # coding.click_button("Charlotte")
        # playerslist = coding.getListOfPlayers("Charlotte")
        # for x in playerslist:
        #     print(x)
        # coding.createcsv(playerslist,"Charlotte.csv")

        listofdivisions = coding.getteamsdiv()
        for i, x in enumerate(listofdivisions):
            divisions = x[0]
            x.remove(x[0])
            for int, y in enumerate(x):
                
                coding.click_button(y)
                coding.createfolder(divisions)
                playerlist = coding.getListOfPlayers(y)
                coding.createcsv(playerlist, "./divisions/" + divisions + "/" +
                                y + '.csv', divisions, y)
                
                time.sleep(5)

        
        driver.quit()


class SeleniumScraper:
    

    def __init__(self, driver):
        self.driver = driver

    # Selenium script to access webpage
    def click_button(self, classname):
        Clickteam = self.driver.find_element(
            By.LINK_TEXT, classname)
        Clickteam.click()

    def createfolder(self, div):
        if (os.path.isdir("./divisions/"+div)):
            return
        else:
            os.mkdir("./divisions/"+div)

    def getListOfPlayers(self, teamslist):
        allplayerlist = []
        playerwrapper = self.driver.find_element(
            By.CLASS_NAME, "Card__Content")
        playerelements = playerwrapper.find_elements(
            By.CLASS_NAME, 'Table__TR')
        print(len(allplayerlist))
        playerstring = []
        for element in playerelements:
            
            playerstring.append(element.text)
        # for elements in playerstring:
        #     print(playerstring)
        self.driver.back()


        return playerstring

    # gets list of teams and add to list of teams of specific division

    def getteamsdiv(self):
        teamslistlist = []
        divisonwrapper = self.driver.find_elements(
            By.CLASS_NAME, 'mod-teams-list-small')
        divsaver = ""
        for i, x in enumerate(divisonwrapper):

            divname = x.find_element(
                By.CLASS_NAME, 'colhead')
            teams = x.find_element(
                By.CLASS_NAME, 'small-logos')
            divsaver = divname.text
            tempteam = []
            tempteam = teams.text.splitlines()
            tempteam.insert(0, divsaver)
            teamslistlist.append(tempteam)
        return teamslistlist

    

    def createcsv(self, list, name, divisions, team):
        with open(name, 'w', newline='') as file:
            writer = csv.writer(file)
            
            for element in list:
                parts = element.split()
                try:
                    if(parts[0]!="NAME"):
                        parts.insert(3, divisions)
                        parts.insert(4, team)
                        lastName = parts[1]
                        if lastName[-1].isdigit():  # Check if the last character of the last name is a digit
                            lastName = lastName.rstrip('0123456789')
                        parts[1] = lastName
                        writer.writerow(parts)
                except:
                    print("error",parts)

run = TestMethod()
run.test()


