#Importing libraries:
import basketball_reference_scraper as brs
import sqlite3
import pandas as pd

def GetTeams():
    File = open("NBA Teams.txt",'r') # Creates file object to read list of NBA Teams from text file
    Teams = [] # This will storre the list of abbreviated NBA Teams to return
    line = File.readline() #Used to read first line of text file
    FinalChar = "" #will be used to store final character of final abbreviation of Teams
    while line != "": # Checks to see if the end of the file has been reached yet
        splitted = line.split(": ") #Used to split line so we can get the abbreviation wanted
        print(splitted)
        abbrev = splitted[1] # abbreviation is in second part of the string
        FinalChar = abbrev[-1] # assigns final character of abbreviation to finalchar
        abbrev = abbrev[:-1] # ignoress final character of abbreviation from abbreviation
        Teams.append(abbrev) # adds abbreviation to Teams
        line = File.readline() #checks next line'
    File.close() #closes text file to save memory
    FinalAbbrev = Teams[-1] + FinalChar #Adds final character of final abbreviation back to the abbreviation
    Teams[-1] = FinalAbbrev #assigns correct abbreviation to final item in Teams
    return Teams # returns list of abbreviated NBA teams
    
Teams = GetTeams() #Creates list of all NBA teams
print(Teams) #Testing to check if GetTeams returns the desired output

Connection = sqlite3.connect("NBA.db") # creates connection to database
Cursor = Connection.cursor() #Creates cursor object to execute SQL code from





#for season in range(1980,2025):  Iterates from each NBA season from the season that ended in 1980 to the season that ended in 2024
    

