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
        listofdivisions = coding.getteamsdiv()
        

        for i, x in enumerate(listofdivisions):
            divisions = x[0]
            x.remove(x[0])
            for y in x:
                
                coding.click_button(y)

                coding.createfolder(divisions)
                playerlist = coding.getListOfPlayers(y)
                coding.createcsv(playerlist, "./divisions/" + divisions + "/" +
                                y + '.csv')
                time.sleep(5)

        
        driver.quit()


class SeleniumScraper:
    # xpath for each element
    driver = ""
    listofcars = "//*[@id='pypvi_results']"
    car_card_wrappers = "//*[@class='pypvi_resultRow']"
    car_detail_wrapper = "//*[@class='pypvi_details text--small']"
    car_name = "//*[@class='pypvi_ymm']"

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

    

    def createcsv(self, list, name):
        with open(name, 'w', newline='') as file:
            writer = csv.writer(file)
            field = ["name", "position", "height",
                     "weight", "class", "birthplace"]

            for element in list:
                writer.writerow(element.split())


run = TestMethod()
run.test()


