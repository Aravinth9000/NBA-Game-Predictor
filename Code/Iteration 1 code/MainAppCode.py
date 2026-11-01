#Importing dependencies
import sys
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
def SwitchTeamModifier():
    EmptyStack()
    TeamM = TeamModifier()
    Stack.addWidget(TeamM)


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
        
        
    #Add Actions for switching screens via Menu Bar
    def AddActions(self):
        self.MenuWelcomeScreen.addAction("Switch Welcome Screen", SwitchWelcomeScreen)
        self.MenuGamePredictor.addAction("Switch Game Predictor", SwitchGamePredictor)



        
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
#        self.SaveButton.clicked.connect(self.Save)
        for i in range(1,6)
        exec("self.Search"+str(i)+".clicked.connect(lambda: self.)")

    
        


#Team Modifier Code
class TeamModifier(QtWidgets.QWidget):
    #Creating Window
    def __init__(self):
        super().__init__()
        uic.loadUi("Team Modifier.ui",self)  #Loads ui file to use as current application
        self.SetButtons()

    #Currently for setting up return button
    def SetButtons(self):
        self.ReturnButton.clicked.connect(SwitchTeamDesigner)


        

#Setting up application        
App = QtWidgets.QApplication(sys.argv)

#Loading welcome screen and settign up stacked widget for switching
Welc = WelcomeScreen()
Stack = QtWidgets.QStackedWidget()
Stack.addWidget(Welc)

#Running application
Stack.show()
App.exec()
