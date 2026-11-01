import sqlite3
import pandas as pd
import numpy as np

def GetRanges():
    Range = pd.read_csv("Ranges.csv")
    Values = Range["0"]
    RangeVals = []
    for Val in Values:
        RangeVals.append(Val)
    return RangeVals

def FindSuggestions(Part):
    #Returns Empty List if input is empty:
    if Part == "":
        return []
    #Setting up connection to NBA.db
    DB = sqlite3.connect("NBA.db")
    Cursor = DB.cursor()
    #SQL Query selects any player whose name contains Part
    Query = "SELECT PlayerName,ID FROM PlayerTable WHERE PlayerName LIKE \"%"+Part+"%\";"
    #Running SQL Query and fetching player names and IDs given
    Cursor.execute(Query)
    Players = Cursor.fetchall()
    
    Options = []
    for P in Players: #Iterates through each row to concatenate information into one string
        Options.append(P[0] + " , " + str(P[1]))
    #Closing Database connection
    DB.commit()
    DB.close()
    
    return Options # Returns each player information as name concatenated with ID

def GetPlayerStats(Players):
    IDs = []
    for P in Players:
        IDString = P.split(' , ')[1]
        IDs.append(int(IDString))

    Inputs = []
    for ID in IDs:
        Stats = GetStats(ID)
        Inputs = Inputs + Stats
    StatArray = np.array(Inputs)
    return StatArray

def GetStats(ID):
    DB = sqlite3.connect("NBA.db")
    Cursor = DB.cursor()
    Cursor.execute("SELECT * FROM PlayerTable WHERE ID = ?",[ID])
    Stats = Cursor.fetchall()
    DB.commit()
    DB.close()
    Stats = list(Stats[0])[3:]
    for i in range(3,6):
        Stats[i] = Stats[i] / Stats[6]
    Stats = Stats[:6]
    return Stats

print(GetPlayerStats(["LeBron James , 2544"]*10))

