#importing libraries
import sqlite3
import json
from time import sleep
from nba_api.stats.endpoints import playercareerstats

# Setting up database connection and collecting all players' information
Conn = sqlite3.connect("NBA.db")
Cursor = Conn.cursor()
Cursor.execute("SELECT * FROM PlayerTable")
Players = Cursor.fetchall()

# Iterating through each player
i = 0
Valid = True
while i < len(Players) and Valid:
    
    try:
# Accessing a player's information an their full statistics
        PlayerInfo = Players[i] 
        ID = PlayerInfo[2]
        Career = playercareerstats.PlayerCareerStats(player_id=ID)
        Stats = json.loads(Career.get_json())
        AllRows = Stats["resultSets"]
        RegularSeasonStats = [row for row in AllRows if row["name"] == "SeasonTotalsRegularSeason"][0]

#Collecting value of Games Played
        GPIndex = RegularSeasonStats["headers"].index("GP") #GP = Games Played, finding position of value for GP
        LatestStats = RegularSeasonStats["rowSet"][-1]
        GP = LatestStats[GPIndex]

#Updating Value of Games Played in Database
        Cursor.execute("UPDATE PlayerTable SET GamesPlayed = ? WHERE ID = ?", (GP,ID))
        print((i, GP))
        i += 1
    except Exception as e: #Except statement used to catch error and save changes to database without crash in program
        print(e)
        Valid = False
    sleep(0.6)

#Save changes to NBA.db
Conn.commit()
Conn.close()
