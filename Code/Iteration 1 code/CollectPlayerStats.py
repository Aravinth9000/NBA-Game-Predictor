#importing libraries needed
import json
import pandas as pd
from nba_api.stats.endpoints import playercareerstats
from time import sleep
import sqlite3

#Stroing table of basic player information in a pandas dataframe from the csv file
PlayerDF = pd.read_csv('player.csv')

#Creating connection to NBA.db
Conn = sqlite3.connect('NBA.db')
Cursor = Conn.cursor()

#iterate through each row of dataframe
NumRows = len(list(PlayerDF.iterrows()))
i = 0
valid = True # Valid is used to check if timeout error has occurred
while i < NumRows and valid:
    
    try:    #if timeout error doesn't occur
#Accessing Regular Season statistics of each NBA player
        PlayerID = PlayerDF.iloc[[i]]['id'] 
        Career = playercareerstats.PlayerCareerStats(player_id=PlayerID)
        Player = json.loads(Career.get_json()) #Player statistics are stored in a dictionary
        AllRows = Player["resultSets"]
        RegularSeasonStats = [row for row in AllRows if row["name"] == "SeasonTotalsRegularSeason"][0] # Checks that statistics collected are from Regular Season
    
# Will be used to collect the correct statistics by checking index of statistics in header
        Headers = RegularSeasonStats["headers"]
        Indices = []
        StatsNeeded = ['FG_PCT','FG3_PCT','FT_PCT','OREB', 'DREB', 'BLK']
        for Stat in StatsNeeded:
            Indices.append(Headers.index(Stat))
        PlayerName = PlayerDF.iloc[[i]]['full_name'].item()
#Adding the name, id and statisitics to a row to store as record in database
        if RegularSeasonStats["rowSet"]:
            LatestStats = RegularSeasonStats["rowSet"][-1]
            NewRow = [i,PlayerName,PlayerID.item()] 
            for ind in Indices:
                NewRow.append(LatestStats[ind])
#Cleaning data by ignoring rows with null values
            if None not in NewRow:
                print(NewRow)
                Cursor.execute("INSERT INTO PlayerTable VALUES (?,?,?,?,?,?,?,?,?)", NewRow)
        sleep(0.6)
        i += 1

    except Exception as e: #if timeout error does occur
        print(e)
        valid = False  

#Save changes to database after while loop
Conn.commit()
Conn.close()



# Note: will use PlayerID now in database to uniquely identify NBA players as this information is now available to me
# Will also be able to change name from PlayerSeasonTable to PlayerTable
# need to if statement to see if rowset is empty
