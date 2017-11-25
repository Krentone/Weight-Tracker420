#Author: DevDoggo

import sqlite3
import datetime

#=========== Database Section =======================================================

database = "weightDb"
#database = "testDB"
database = database + ".db"
connection = sqlite3.connect(database)
cursor = connection.cursor()

def connect():
    cursor.execute("CREATE TABLE IF NOT EXISTS weights (id INTEGER PRIMARY KEY, date text, weight REAL)")
    connection.commit()

def addWeight(date, weight):
    if dateEntryExists(date):
        print("\nAn entry for this date already exists. Use the 'update' command to change the current entry.")
    else:
        weight = float(weight)*1.00
        cursor.execute("INSERT INTO weights VALUES (NULL, ?, ?)", (date, weight)) 
        connection.commit()
        print("Add successful.")

def updateWeight(date, weight):
    if dateEntryExists(date):
        cursor.execute("UPDATE weights SET weight=? WHERE date=?", (weight, date))
        connection.commit()
        print("Update successful.")
    else:
        print("\nAn entry for this date doesn't exist. Use the 'add' command to add a new entry.")

def getEntries():
    cursor.execute("SELECT date, weight FROM weights")
    rows = cursor.fetchall()
    return rows

def show():
    print(getEntries())

#=========== Statistics Section =====================================================

def getStats(x):
    if not isValidNumberOfDays(x):
        return("Incorrect number format!")
    op = resultInXDays(x) 
    dates = op[0]
    weights = op[1]
    weekly = ""
    monthly = ""
    x = int(x)
    entriesTotal = len(getEntries())
    if entriesTotal >= 7: 
        op7 = resultInXDays(7)
        dates7 = op7[0]
        weights7 = op7[1]
        weekly = "\nLast 7 days: " + str(weights[0] - weights7[0]) + "kg.\n"
    if entriesTotal >= 30:
        op30 = resultInXDays(30)
        dates30 = op30[0]
        weights30 = op30[1]
        monthly = "Last 30 days: " + str(weights[0] - weights30[0]) + "kg.\n"

    outputString = ""
    outputString += "\n\n\n\n\n" + "="*50 +"\n" 
    outputString += str(dates[1].date()) + " - " + str(weights[1]) + "kg.\n"
    outputString += str(dates[0].date()) + " - " + str(weights[0]) + "kg.\n"
    outputString += "Difference: " + str(weights[0] - weights[1]) + "kg.\n"
    outputString += "Average difference per day: " + str(int(weights[0] - weights[1])/int(x)) + "kg for " + str(x) + " days.\n"
    outputString += weekly + monthly
    outputString += "="*50 
    return outputString


def resultInXDays( x ):
    x = int(x)
    entryList = makeDateAndWeightLists(getEntries())
    dateList = entryList[0]
    weightList = entryList[1]

    dateObjectList = []
    for date in dateList:
        dateArr = date.split("-")
        dateObj = datetime.datetime(int(dateArr[0]), int(dateArr[1]), int(dateArr[2]))
        dateObjectList.append(dateObj)

    curDate = dateObjectList[-1]
    i = len(dateObjectList) -1 
    while (curDate-dateObjectList[i]).days < x and i > 0 :
        i = i -1
    dates = [dateObjectList[-1], dateObjectList[i]]
    weights = [weightList[-1], weightList[i]]
    return(dates, weights, x)


def makeDateAndWeightLists(inpList):
    i = 0
    dateList = []
    weightList = []
    while i < len(inpList):
        dateList.append(inpList[i][0])
        weightList.append(inpList[i][1])
        i = i + 1 
    return (dateList, weightList)


def printListAll():
    allEntries = getEntries()
    print("\n\n\n\n\n  Date - Weight\n")
    for entry in allEntries:
        print(str(entry[0]) + " - " + str(entry[1]))
    
def isValidNumberOfDays(num):
    try: 
        int(num)
        return True
    except:
        print("\nInvalid input of number of days.")
        return False


#===========  Misc. Section =====================================================


def dateEntryExists(date):
    for ent in getEntries():
        if ent[0] == date:
            return True
    return False

def formatDate(dateObject):
    dateOutput = dateObject.date()
    return str(dateOutput)

def formatInput(inp):
    inp = inp.replace(" ", "")
    return inp
        
def isValidWeightInput(inp):
    try: 
        float(inp)
        return True
    except:
        print("\nThe input is not a valid number!")
        return False

def fillEmptyDays():
    lastEntry = getEntries()[-1]
    lDate = lastEntry[0]
    lWeight = lastEntry[1]
    today = str(datetime.datetime.now().date())
    if lDate != today:
        print("Filling in empty days...\n")
    while lDate != today:
        dateSplit = lDate.split("-")
        lDate= datetime.datetime(int(dateSplit[0]), int(dateSplit[1]), int(dateSplit[2]))
        lDate += datetime.timedelta(days=1)
        lDate = formatDate(lDate)
        print(lDate)
        addWeight(lDate, lWeight)

def clearPage():
    print(200*"\n")


#============ DEBUGGING =============================================
def createFakeEntriesForDebugging(): 
    newWeight = 42
    day = 10
    while True:
        day = day +1 
        if day != 19:
            newDate = datetime.datetime(2017, 11, day)
            newWeight = newWeight + 2
            addWeight(formatDate(newDate), newWeight)
        else:
            break

#===================================================================

def main(date):
    connect()
    print("\n"*100)
    #createFakeEntriesForDebugging()
    fillEmptyDays()
    print("\n" + "="*50 + "\n" + "type 'help' for commands and explanations" + "\n" + "="*50)

    while True:
        xInput = formatInput(input("\nInput: [add, update, compare, print, clear]: "))
        clearPage()

        if xInput == "add":
            print("Leave blank to cancel.")
            weight = formatInput(input("Today's weight [kg]: "))
            if weight == "":
                print("Nothing was changed.")
                continue
            if isValidWeightInput(weight):
                addWeight(date, weight)

        if xInput == "update":
            print("Leave blank to cancel.")
            weight = formatInput(input("Today's weight [kg]: "))
            if weight == "":
                print("Nothing was changed.")
                continue
            if isValidWeightInput(weight):
                updateWeight(date, weight)


        if xInput == "compare":
            days = formatInput(input("How many days back do you want to compare?: "))
            if isValidNumberOfDays(days):
                if len(getEntries()) >= int(days) and int(days) > 0:
                    print(getStats(days))
                elif int(days) <= 0:
                    print("Unuseable input number!")
                else:
                    print("\nThat many days have not been logged!")
            else:
                print("Bad input!")

        if xInput == "clear":
            clearPage()
        if xInput == "print":
           printListAll()


        if xInput == "x":
            break

dateObj = datetime.datetime.now()
date = formatDate(dateObj)
main(date)
