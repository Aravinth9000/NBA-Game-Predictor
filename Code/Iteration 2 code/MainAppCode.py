#
#Notes: Changed data type of team table
#

#Importing dependencies
import sys
import sqlite3
import ExtraFuncs as EF # My code
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic

#Removes any current screens from stack of widgets
def EmptyStack():
    for i in range(Stack.count()): #Iterates through each widget in stack to remove each one
        Stack.widget(0).deleteLater() #Removes widget from memeory to save memory
        Stack.removeWidget(Stack.widget(0))    

#Set Welcome Screen as current Screen of stack
def SwitchWelcomeScreen():
    EmptyStack()
    WelcS = WelcomeScreen()
    Stack.addWidget(WelcS)

#Sets Team Designer as current screen of stack
def SwitchTeamDesigner():
    EmptyStack()
    TeamDes = TeamDesigner()
    Stack.addWidget(TeamDes)

#Sets Game Predictor as current screen of stack
def SwitchGamePredictor():
    EmptyStack()
    GameP = GamePredictor()
    Stack.addWidget(GameP)

#Sets Team Creator as current screen of stack
def SwitchTeamCreator():
    EmptyStack()
    TeamC = TeamCreator()
    Stack.addWidget(TeamC)

#Sets Team Modifier as current screen of stack
def SwitchTeamModifier(Team):
    EmptyStack()
    TeamM = TeamModifier(Team)
    Stack.addWidget(TeamM)


def Various(Team,Wid):
    Mode = Wid.ModeDropdown.currentText()
    if Mode == "Modify":
        SwitchTeamModifier(Team)
    


#Welcome Screen code
class WelcomeScreen(QtWidgets.QMainWindow):
    #Creating Window
    def __init__(self):
        super().__init__() 
        uic.loadUi("Welcome Page.ui",self) #Loads ui file to use as current application
        self.AddActions()#Assigns actions to Menu Bar
    #Add Actions for switching screens to Menu Bar
    def AddActions(self):
        self.MenuTeamDesigner.addAction("Switch Team Designer", SwitchTeamDesigner)
        self.MenuGamePredictor.addAction("Switch Game Predictor", SwitchGamePredictor)

#Team Designer Code
class TeamDesigner(QtWidgets.QMainWindow):
    #Creating Window
    def __init__(self):
        super().__init__()
        self.Mode = "View" #Sets default mode to View
        uic.loadUi("Team Designer.ui",self)  #Loads ui file to use as current application
        self.AddActions()#Assigns actions to Menu Bar
        self.CreateButton.clicked.connect(SwitchTeamCreator) #Allows user to switch to Team Creator
        self.ScrollAppend()
        
    #Add Actions for switching screens via Menu Bar
    def AddActions(self):
        self.MenuWelcomeScreen.addAction("Switch Welcome Screen", SwitchWelcomeScreen)
        self.MenuGamePredictor.addAction("Switch Game Predictor", SwitchGamePredictor)

    def ScrollAppend(self):
        #Setting up connection ot NBA.db
        DB = sqlite3.connect("NBA.db")
        Cursor = DB.cursor()
        #Fetching name of every team
        Cursor.execute("SELECT TeamName FROM TeamTable")
        Teams = [Team[0] for Team in Cursor.fetchall()] #Cursor gives 2d array, so I must extract team from each row
        #Closing connection
        DB.commit()
        DB.close()
        self.Form = QtWidgets.QFormLayout()
        self.Group = QtWidgets.QGroupBox("Teams")
        
        for T in Teams:
            Button = QtWidgets.QPushButton(T)
            Button.clicked.connect(lambda: Various(T,self))
            self.Form.addRow(Button)
            
        self.Group.setLayout(self.Form)
        self.ScrollArea.setWidget(self.Group)
        self.Layout = QtWidgets.QVBoxLayout()
        self.Layout.addWidget(self.ScrollArea)
        


        
#Game Predictor code
class GamePredictor(QtWidgets.QMainWindow):
    #Creating Window:
    def __init__(self):
        super().__init__() 
        uic.loadUi("Game Predictor.ui",self)  #Loads ui file to use as current application
        self.AddActions()#Assigns actions to Menu Bar
        
    #Add Actions for switching screens via Menu Bar
    def AddActions(self):
        self.MenuWelcomeScreen.addAction("Switch Welcome Screen", SwitchWelcomeScreen)
        self.MenuTeamDesigner.addAction("Switch Team Designer", SwitchTeamDesigner)

#Team Creator Code
class TeamCreator(QtWidgets.QWidget):
    #Creating Window:
    def __init__(self):
        super().__init__() 
        uic.loadUi("Team Creator.ui",self)  #Loads ui file to use as current application
        self.SetButtons()
        
        
    #Currently for setting up return button
    def SetButtons(self):
        #Return Button Code
        self.ReturnButton.clicked.connect(SwitchTeamDesigner)

        #For search buttons
        self.Search1.clicked.connect(lambda: self.GiveOptions(1))
        self.Search2.clicked.connect(lambda: self.GiveOptions(2))
        self.Search3.clicked.connect(lambda: self.GiveOptions(3))
        self.Search4.clicked.connect(lambda: self.GiveOptions(4))
        self.Search5.clicked.connect(lambda: self.GiveOptions(5))

        #For Save Button
        self.SaveButton.clicked.connect(self.Save)


    def GiveOptions(self, Num):
        Entries = [self.P1Entry.text(),
         self.P2Entry.text(),
         self.P3Entry.text(),
         self.P4Entry.text(),
         self.P5Entry.text()]
        Part = Entries[Num-1]
        Suggestions = EF.FindSuggestions(Part)

        #Reduce number of options so that it is easier for User to find players
        if len(Suggestions) > 50:
            Suggestions = Suggestions[:50]
        
        #Removing every option except current option    
        exec("CurrItem = self.Sugg"+str(Num)+".currentText()")
        exec("self.Sugg"+str(Num)+".clear()")
        exec("self.Sugg"+str(Num)+".addItem(CurrItem)")

        #Adding new options
        exec("self.Sugg"+str(Num)+".addItems(Suggestions)")

    def Save(self):
        #Getting data for each column of TeamTable
        Data = (self.TeamEntry.text(),self.Sugg1.currentText(),self.Sugg2.currentText(),
                self.Sugg3.currentText(),self.Sugg4.currentText(),self.Sugg5.currentText())
        #Running SQL query, which inserts collected data into TeamTable
        Query = "INSERT INTO TeamTable VALUES (?,?,?,?,?,?)"
        DB = sqlite3.connect("NBA.db")
        Cursor = DB.cursor()
        Cursor.execute(Query,Data)
        DB.commit()
        DB.close()
        try:
            SwitchTeamDesigner() #Returns to Team Designer
        except Exception as e:
            print(str(e))

            
         

            
        
        


#Team Modifier Code
class TeamModifier(QtWidgets.QWidget):
    #Creating Window
    def __init__(self,Team):
        super().__init__()
        uic.loadUi("Team Modifier.ui",self)  #Loads ui file to use as current application
        self.SetButtons()
        self.OGTeamName = Team
        self.CurrTeamName = Team
        self.SetUp()

    #Currently for setting up return button
    def SetButtons(self):
        self.ReturnButton.clicked.connect(SwitchTeamDesigner)

        #For search buttons
        self.Search1.clicked.connect(lambda: self.GiveOptions(1))
        self.Search2.clicked.connect(lambda: self.GiveOptions(2))
        self.Search3.clicked.connect(lambda: self.GiveOptions(3))
        self.Search4.clicked.connect(lambda: self.GiveOptions(4))
        self.Search5.clicked.connect(lambda: self.GiveOptions(5))

        #For Save Button
        self.SaveButton.clicked.connect(self.Save)

    def GiveOptions(self, Num):
        Entries = [self.P1Entry.text(),
         self.P2Entry.text(),
         self.P3Entry.text(),
         self.P4Entry.text(),
         self.P5Entry.text()]
        Part = Entries[Num-1]
        Suggestions = EF.FindSuggestions(Part)

        #Reduce number of options so that it is easier for User to find players
        if len(Suggestions) > 50:
            Suggestions = Suggestions[:50]
        
        #Removing every option except current option    
        exec("CurrItem = self.Sugg"+str(Num)+".currentText()")
        exec("self.Sugg"+str(Num)+".clear()")
        exec("self.Sugg"+str(Num)+".addItem(CurrItem)")

        #Adding new options
        exec("self.Sugg"+str(Num)+".addItems(Suggestions)")        

    def SetUp(self):
        self.OriginalTeam.setText("Original Team Name: " + self.OGTeamName)

        DB = sqlite3.connect("NBA.db")
        Cursor = DB.cursor()
        
        Cursor.execute("SELECT * FROM TeamTable WHERE TeamName == \"" + self.OGTeamName + "\";")
        Data = Cursor.fetchall()[0][1:]
        
        self.Sugg1.addItem(Data[0])
        self.Sugg2.addItem(Data[1])
        self.Sugg3.addItem(Data[2])
        self.Sugg4.addItem(Data[3])
        self.Sugg5.addItem(Data[4])
        
        DB.commit()
        DB.close()

    def Save(self):
        if self.TeamEntry.text() != "":
            self.CurrTeamName = self.TeamEntry.text()
        Data = (self.CurrTeamName,self.Sugg1.currentText(),self.Sugg2.currentText(),
                self.Sugg3.currentText(),self.Sugg4.currentText(),self.Sugg5.currentText(), self.OGTeamName)

        DB = sqlite3.connect("NBA.db")
        Cursor = DB.cursor()
        Query ='''UPDATE TeamTable
SET TeamName = ?, Priority1 = ?, Priority2 = ?, Priority3 = ?, Priority4 = ?, Priority5 = ?
WHERE TeamName = ?'''
        Cursor.execute(Query,Data)
        DB.commit()
        DB.close()
        SwitchTeamDesigner()



#Setting up application        
App = QtWidgets.QApplication(sys.argv)

#Loading welcome screen and settign up stacked widget for switching
Welc = WelcomeScreen()
Stack = QtWidgets.QStackedWidget()
Stack.addWidget(Welc)

#Running application
Stack.show()
App.exec()
