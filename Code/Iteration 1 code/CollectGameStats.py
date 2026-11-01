import json
from nba_api.live.nba.endpoints import boxscore
from nba_api.stats.endpoints.boxscoretraditionalv2 import BoxScoreTraditionalV2
import pandas as pd
from time import sleep

def OrderGameStats(ID,T1,T2): #T1 is home team, T2 is away Team

#Scraping web data using nba_api
    Game = BoxScoreTraditionalV2(ID)
    JVers = json.loads(Game.get_json()) 
                
#Setting up columns to take data from
    Cols = ['TEAM_ABBREVIATION','MIN','FG_PCT','FG3_PCT','FT_PCT','OREB', 'DREB','BLK']
    Headers = JVers['resultSets'][0]['headers']
    ColIndices = [Headers.index(Col) for Col in Cols]
    
#Accessing 2D array fo BoxScore statistics, and Obtaining relevant columns
    FullStats = JVers['resultSets'][0]['rowSet']
    GameStats = []
    for Row in FullStats:
        NewRow = [Row[i] for i in ColIndices]
        GameStats.append(NewRow)
        
#Data Cleaning by removing null data, and splitting data into two separate 2D arrays for the two teams
    T1Stats = [Row for Row in GameStats if (None not in Row) and (Row[0] == T1)]
    T2Stats = [Row for Row in GameStats if (None not in Row) and (Row[0] == T2)]
    
#Ordering players' statistics in order of which player played for longest time in each team
    try: #Integer form of minutes played
        T1Stats = sorted(T1Stats, key=lambda Row : float(Row[1][:5]), reverse = True)
        T2Stats = sorted(T2Stats, key=lambda Row : float(Row[1][:5]), reverse = True)
    except: # Minutes and seconds form of minutes played
        T1Stats = sorted(T1Stats, key=lambda Row : float(Row[1]), reverse = True)
        T2Stats = sorted(T2Stats, key=lambda Row : float(Row[1]), reverse = True)

#Checking if each team has at least 5 players without any null statistics from columns mentioned in Cols
    if len(T1Stats) > 4 and len(T2Stats) > 4:
        ReturnStats = []
        
        TempT1 = [Row[2:] for Row in T1Stats]
        TempT2 = [Row[2:] for Row in T2Stats]
        for i in range(5):
            ReturnStats = ReturnStats + TempT1[i] #Adds home team's statistics to ReturnStats

        for i in range(5):
            ReturnStats = ReturnStats + TempT2[i] #Adds away team's statistics to ReturnStats

        return ReturnStats #This contains 60 input values for a set of data to be passed into input nodes of perceptron
        sleep(0.6)
    else:
        print(T1Stats) #Shows that there is not enough rows of valid data for the data to be used for training perceptron
        return None

StatsColumns = ["DFIndex",'home1fgp', 'home13fgp', 'home1ftp', 'home1oreb', 'home1dreb', 'home1blk', 'home2fgp', 'home23fgp', 'home2ftp', 'home2oreb',
                'home2dreb', 'home2blk', 'home3fgp', 'home33fgp', 'home3ftp', 'home3oreb', 'home3dreb', 'home3blk', 'home4fgp', 'home43fgp',
                'home4ftp', 'home4oreb', 'home4dreb', 'home4blk', 'home5fgp', 'home53fgp', 'home5ftp', 'home5oreb', 'home5dreb', 'home5blk',
                'away1fgp', 'away13fgp', 'away1ftp', 'away1oreb', 'away1dreb', 'away1blk', 'away2fgp', 'away23fgp', 'away2ftp', 'away2oreb',
                'away2dreb', 'away2blk', 'away3fgp', 'away33fgp', 'away3ftp', 'away3oreb', 'away3dreb', 'away3blk', 'away4fgp', 'away43fgp',
                'away4ftp', 'away4oreb', 'away4dreb', 'away4blk', 'away5fgp', 'away53fgp', 'away5ftp', 'away5oreb', 'away5dreb', 'away5blk', "Win"]

GameInfo = pd.read_csv("game.csv")
Length = len(list(GameInfo.iterrows()))
Valid = True
GameStats = pd.DataFrame(columns = StatsColumns)
i = 64000

while Valid and i < Length:
#Try and except statement used to ctach any potential errors and prevent collected data from being lost
    try:

        Row = GameInfo.iloc[i]
        ID = '00' + str(Row["game_id"])
        T1 = Row["team_abbreviation_home"]
        T2 = Row["team_abbreviation_away"]

#Used to find if Home Team or away Team WIns
        Outcome = Row["wl_home"]
        End = []
        if Outcome == "W":
            End.append(1)
        else:
            End.append(0)

#Reading Statistics
        Stats = [i] + OrderGameStats(ID,T1,T2) + End
        print(Stats)
        GameStats.loc[len(GameStats)] = Stats 
        i += 1

#Exception used to notify me of error without causing program to crash
    except Exception as e: 
        print(e)
        Valid = False #Ends loop
        
    sleep(0.6) #Prevents/significantly delays Timeout error

GameStats.to_csv("GameStats.csv")
