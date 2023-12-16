#Create a class for all the text colours
class c:
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    white = '\033[37m'
    red = '\033[91m'
    pink = '\u001b[35m'

#Import all dependencies
print(f"{c.blue}Importing dependencies\n{c.white}")
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from os import path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os.path
import requests
import time
import json
import os

#Gather previous image ids from the json file
print(f"{c.blue}Importing ID's of previous pics\nOpening WHavenIDs.json\n")
with open("WHavenIDs.json", 'r') as file:
    oldIDs = json.load(file)

#Set the options and create the profile
print("Setting up Header profile and associated options\n")

firefox_options = webdriver.FirefoxOptions()

#firefox_profile.set_preference("permissions.default.image", 2)
firefox_options.add_argument('-headless')

#Initiate the driver
print(f"Initiating the driver\n{c.white}")
driver = webdriver.Firefox(options=firefox_options)

#Initiate the tags list
userTagChoice = input("Tags:\n(1) Hard-coded\n(2) Define own tags\n")
if userTagChoice == '1':
    tags = ["air"]

    if len(tags) == 0:
        print(f"{c.yellow}There are no hard-coded tags...{c.white}")
        temp = input("\nType your own tags, use slashes to separate:\n")
        tags = temp.split("/")
else:
    temp = input("\nType your own tags, use slashes to separate:\n")
    tags = temp.split("/")

#This is for if the tags are two or more words, the + allows the tag to be used inside a URL
for x in tags:
    if " " in x:
        x.replace(" ", "+")

#Create the object for the menu choices, this gets looped through to display the menu items
choiceObject = {"categories" : ['General', 'Anime', 'People'], "purity" : ['SFW', 'Sketchy'], "sorting" : ['relevance', 'random', 'date_added', 'views', 'favorites', 'toplist', 'hot'], "order" : ['descending', 'ascending']}

#Create the object for the purity parameters for looping through
purityParamsIndex = ['categories', 'purity', 'sorting', 'order']
purityParams = {"categories": "", "purity": "", "sorting": "", "order": ""}

#Kry user input oor purity parameters
purityChoice = int(input("\nPurity parameters:\n(1) Default\n(2) Custom\n"))

#Modify purity parameters based on user's choice
if purityChoice == 1: #Default parameters
    purityParams["categories"] = "011"
    purityParams["purity"] = "010"
    purityParams["sorting"] = "relevance"
    purityParams["order"] = "desc"
else: #Custom parameters
    for x in purityParamsIndex:
        counter = 1

        #Print the individual parameter headings
        print(f"\n{x.capitalize()}: ")
        for p in choiceObject[x]:
            temp = p.capitalize()
            if "_" in temp:
                temp = temp.replace("_", " ")
            elif temp == "Sfw":
                temp = temp.upper()

            #Print the choices inside the parameter headings
            print(f"({counter}) {temp}")
            counter +=1
        choice = input()

        #Set the purity parameters according the user's choice
        if x == 'categories' or x == 'purity':
            for i in range(1, 4):
                if str(i) in choice:
                    purityParams[x] = purityParams[x] + "1"
                else:
                    purityParams[x] = purityParams[x] + "0"
        elif x == "order":
            if choice == "1":
                purityParams[x] = "desc"
            else:
                purityParams[x] = "asc"
        else:
            purityParams[x] = choiceObject[x][int(choice)-1]
print(f"{c.blue}\nSetting search parameters\n")
#Initiate the loop for the tags
print(f"Initiating the tag loop-through\n{c.white}")
folderExists = False
for tag in tags:
    #This if is for when the folder already exists
    if path.exists(tag.capitalize()):
        print("This folder already exists, continuing to use it...\n")

        #If the sec.json file exists, load it, otherwise create it. (This is only useful for folders that were created before this feature)
        if path.exists(f"{tag.capitalize()}/sec.json"):
            #Load the sec.json data
            with open(f"{tag.capitalize()}/sec.json", 'r') as secFile:
                secData = json.load(secFile)

        #This else is for when the program couldnt find the sec.json file
        else:
            #Create the sec.json file from the template.json file
            with open('template.json') as f:
                templateData = json.load(f)

            with open(f'{tag.capitalize()}/sec.json', 'w') as f:
                json.dump(templateData, f)
                print("\nsec.json created...")
            
            #Load the sec.json data
            with open(f"{tag.capitalize()}/sec.json", 'r') as secFile:
                secData = json.load(secFile)

        #Set the folderExists variable
        folderExists = True

    #This else is for when the folder doesnt exist
    else:
        os.makedirs(tag.capitalize())
        print(f"{c.green}Creating the directory folder for '{tag}'")

        #Create a sec.json from the template.json
        with open('template.json') as f:
            templateData = json.load(f)

        with open(f'{tag.capitalize()}/sec.json', 'w') as f:
            json.dump(templateData, f)
            print("\nsec.json created...")

        #Load the sec.json data
        with open(f"{tag.capitalize()}/sec.json", 'r') as secFile:
            secData = json.load(secFile)

    #Get the Wallhaven website with the above parameters
    print(f"Getting the preview webpage of the '{tag}' tag\n{c.white}")
    driver.get(f"https://wallhaven.cc/search?q={tag}&categories={purityParams['categories']}&purity={purityParams['purity']}&sorting={purityParams['sorting']}&order={purityParams['order']}&ai_art_filter=1") 
    time.sleep(2.75)

    #Get the amount of pictures
    num = driver.find_element(By.TAG_NAME, "h1").text
    numImagesDirty=num.split()
    numImagesUpdated=numImagesDirty[0].replace(",","")
    numImages=int(numImagesUpdated)

    #Show the amount of pictures that were found
    print(f"\n{num}\n")

    #Create the amount var
    amount=1

    #Load the sec.json data if the folder exists and set the variables accordingly
    if folderExists == True:
        #Set sec equal to the data, also set li = 1
        sec = secData["latestSec"]
        page = secData["latestPage"]
        print("The previous Section is: "+ str(sec))
        print("The previous Page is: "+ str(page)+ "\n")
        count = sec * 24 - 24
        li = 1

        #Get the correct page
        driver.get(f"https://wallhaven.cc/search?q={tag}&categories={purityParams['categories']}&purity={purityParams['purity']}&sorting={purityParams['sorting']}&order={purityParams['order']}&ai_art_filter=1&page={page}")

        #Scroll to the right section
        print(f"{c.green}Scrolling...\n{c.white}")
        for i in range(sec):
            m = i + 1
            #First Scroll
            element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="thumbs"]/section[{m}]/ul/li[1]/figure/a')))
            driver.execute_script("arguments[0].scrollIntoView();", element)

            #Second Scroll
            element2 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="thumbs"]/section[{m}]/ul/li[9]/figure/a')))
            driver.execute_script("arguments[0].scrollIntoView();", element2)

            #Third Scroll
            element3 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="thumbs"]/section[{m}]/ul/li[17]/figure/a')))
            driver.execute_script("arguments[0].scrollIntoView();", element3)
            print(f"Scrolled to section {c.blue}{m}{c.white}")
            time.sleep(2)
        print(f"\n{c.green}Done Scrolling...{c.white}\n")
    else:
        count = 1
        li=1
        sec=1
        page = 100
    # count = 1
    # li = 1
    # sec = 1
    # page = 100

    #Loop through all the preview pics and get their data-id's
    while amount<=numImages:
        
        #If you get to section 100, you'll get a sanity check, skip it by just reloading the page and resetting the section number to 1
        if sec == 101:
            print(f"{c.blue}Sanity Check Bypassed\n{c.white}")
            driver.get(f"https://wallhaven.cc/search?q={tag}&categories={purityParams['categories']}&purity={purityParams['purity']}&sorting={purityParams['sorting']}&order={purityParams['order']}&ai_art_filter=1&page={page}")

            #Reset the section and list item numbers, as well as the page number
            page += 100
            sec = 1
            li = 1

        #This try sometimes gives errors, add a few try/excepts and then n skip (break) if it doesn't wanna work
        try:
            imr = driver.find_element(By.XPATH, f'//*[@id="thumbs"]/section[{sec}]/ul/li[{li}]/figure/img').get_attribute('src')
        except:
            time.sleep(2)
            try:
                imr = driver.find_element(By.XPATH, f'//*[@id="thumbs"]/section[{sec}]/ul/li[{li}]/figure/img').get_attribute('src')
            except:
                time.sleep(4)
                try:
                    imr = driver.find_element(By.XPATH, f'//*[@id="thumbs"]/section[{sec}]/ul/li[{li}]/figure/img').get_attribute('src')
                except:
                    print(f"{c.red}Skipping image {amount}, it doesn't want to load{c.white}")
                    amount +=1
                    continue

        #Get the picture type
        try:
            picType = driver.find_element(By.XPATH, f'//*[@id="thumbs"]/section[{sec}]/ul/li[{li}]/figure/div/span[2]').get_attribute('class')
        except:
            picType = 'jpg'

        #Get the other data from the src
        data = imr[-10:]
        preChars = data[0:2]
        wallID = data[0:6]

        #Check if the wallID wasn't downloaded previously
        if wallID not in oldIDs["data"]:
            #Create the full view pic link according to the pattern
            link = f"https://w.wallhaven.cc/full/{preChars}/wallhaven-{wallID}.{picType}"
            now = datetime.now().strftime("%Y%m%d%H%M%S")
            
            if picType=='jpg' or picType=='jpeg':
                response=requests.get(link)
                with open(f"{tag}/{now}.{count}.jpg","wb") as file:
                    file.write(response.content)
                
                print(f"Download {c.blue}{count}{c.white} {c.green}successful{c.white} ({numImages-count}) - {round(count/numImages*100, 2)}% ")
                
            elif picType=='png':
                response=requests.get(link)
                with open(f"{tag}/{now}.{count}.png","wb") as file:
                    file.write(response.content)
                
                print(f"Download {c.blue}{count}{c.white} {c.green}successful{c.white} ({numImages-count}) - {round(count/numImages*100, 2)}% ")
                
            oldIDs["data"].append(wallID)
        else:
            print(f"Picture {c.blue}{count}{c.white} with wallID: {c.red}{wallID}{c.white} was {c.yellow}already{c.white} downloaded.")
        count+=1
        amount+=1

        #After every twelve pics scroll down
        if li == 12 or li == 24:
            element = driver.find_element(By.XPATH, f'//*[@id="thumbs"]/section[{sec}]/ul/li[{li}]/figure/img')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(1)
        
        #When starting a new section
        elif li == 1:
            element = driver.find_element(By.XPATH, f'//*[@id="thumbs"]/section[{sec}]/ul/li[{li}]/figure/img')
            driver.execute_script("arguments[0].scrollIntoView();", element)
        li+=1

        #After starting a new section, reset the li and increase the sec
        if li==25:
            li=1
            sec+=1
            #Update the latestSec variable and dump the data into the sec.json file
            secData["latestSec"] = sec
            secData["latestPage"] = page
            with open(f'{tag.capitalize()}/sec.json', 'w') as f:
                json.dump(secData, f)
                print(f"{c.blue}\nsec.json updated...{c.white}")

            time.sleep(1)
        
        #Sit n if statement in vir db update en maak dat die IDs dump en load elke 50 downloads.
        if amount % 50 == 0: 
            #Dump die IDs wat gedownload is
            print(f"\nDumping {c.pink}50{c.white} links into the JSON file for safekeeping\n")
            with open("WHavenIDs.json", 'w+') as file:
                json.dump(oldIDs , file)

            #Re-open die json en reload dit in die memory
            print(f"{c.blue}Re-importing ID's of previous pics\n{c.white}")
            with open("WHavenIDs.json", 'r') as file:
                oldIDs = json.load(file)

    print(f"{c.green}\n'{tag}' tag library successfully completed...{c.white}")
    print(f"{c.pink}Dumping links of {tag} into the JSON file\n{c.white}")
    with open("WHavenIDs.json", 'w+') as file:
        json.dump(oldIDs , file)
    print(f"{c.pink}Deleting sec.json file\n{c.white}")
    os.remove(f"{tag.capitalize()}/sec.json")
driver.close()
print(f"{c.blue}Downloading finished\nClosing JSON file\n\nClosing application{c.white}")
file.close()

#Improvements:
#   Fix: maak count gelyk aan die laaste image se naam se tweede helfte
#   Fix: Maak iets vir die error 502
#   New version: gebruik beautiful soup dalk? Dunno of dit n goeie idee is, dis net way te vinnig
#   Fix: Daar is n weird error by line 121. Base 10 error. Ek dink die webpage load nie reg nie, sit n try/except in
#   Use async/await where you can
#   Create functions instead of the procedural thing you got going on here
#   Use aiohttp module instead requests as requests is not awaitable and it won't work full speed
#   Mens kan die original Wallhaven se stappe asyncio doen
#   Gebruik die stappe wat WHaven 2.0 vinnig maak, maar maak n list van al die links om await te kan gebruik, en by elke time.sleep() kyk of jy daar n await of asyncio kan gebruik om dinge bietjie vinniger te maak
#   Limit die concurrent requests met asyncio se sempahore object???
#   Delete empty folders of moet hulle straight-up net nie maak nie
#   Sit n if statement in wat check vir lee WallIDs, as dit een kry, retry daai hele section sonder om doubles af te laai
#   Try BS4 gebruik om elke section se data te request...
#   Add feature waar die user kan kies hoeveel foto's van elke tag hy/sy wil aflaai en of hulle al die foto's van daai tag wil aflaai, maak dit ook n custom of default amount soos met die purity.