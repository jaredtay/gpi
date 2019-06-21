#! /usr/bin/python3

## Pure Python Imports
import os
import sys
import traceback

## PyQt5 Imports
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel , QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

## 3rd Party Imports
from redbaron import RedBaron as RB

from gpi.helpers import astHelpers, dialogs
from gpi.widgets import standardWidgets


# find script directory
class test(object):
    pass

# GUI View ====================================================================
class view(QWidget):
    ast = None
    fileName = None
    # fileChanged = False
    
    def __init__( self , statusBar):
        QWidget.__init__(self)

        scriptdir=os.path.abspath(os.path.split(sys.modules[test.__module__].__file__)[0])
        
        # Main View
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        
        # Make the main area scrollable
        self.area = QScrollArea()
        self.area.setWidgetResizable(True)
        mainLayout.addWidget(self.area)

        # Save the statusBar
        self.statusBar = statusBar

        # # FUTURE: Rename the system and give it its own welcome page
        # # Drop in a friendly welcome to the gui
        # Welcome = QWidget()
        # layout = QVBoxLayout()
        # Welcome.setLayout(layout)

        # # Draw the picture
        # imageLabel = QLabel()
        # imageLabel.setAlignment(Qt.AlignCenter)
        # pic = QPixmap(os.path.join(scriptdir,'assets','welcome.png'))
        # imageLabel.setPixmap(pic)
        # layout.addWidget(imageLabel)

        # self.area.setWidget(Welcome)

    def open(self):
        openName = QFileDialog.getOpenFileName()
        
        # If no filename is selected, an empty string is placed in self.fileName
        self.fileName = openName[0]
        
        # TODO:
        # if self.fileChanged:
        # Ask the user if they want to save before opening
        
        # If the fileName is blank, stop
        if self.fileName == '':
            self.fileName = None
            return

        # Check the file
        #   Give an error if it doesn't exist
        if not os.path.isfile(self.fileName):
            dialogs.genDialog('Open Error', 'Could not find\n{}'.format(self.fileName))
            return

        #   Give an error if it isn't a python file
        extension = self.fileName[-3:]
        if extension != '.py':
            dialogs.genDialog('Open Error', '{}\nIsn\'t a python file.'.format(self.fileName))
            return

        #   Give an error RB can't parse it in its current state, give a window with the error message from RB
        try:
            self.ast = astHelpers.getAST(self.fileName)
            self.editWidget = standardWidgets.ASTWidget(self.ast)
            self.area.setWidget(self.editWidget)
        except Exception as err:
            dialogs.genDialog('Open Error', 'Trace:\n{}'.format(err))
            traceback.print_exc()
            return

        # Show a status message
        self.statusBar.showMessage("Successfully opened {}".format(self.fileName))
   
    def new(self):
        # Create a new script without a fileName
        self.fileName = None
        self.newAST()

    def newAST(self):
        # Make a new ast
        try:
            self.editWidget.setParent(None)
        except:
            pass
        finally:
            self.ast = RB('# New Script')
            self.editWidget = standardWidgets.ASTwidget(self.ast)
            self.area.setWidget(self.editWidget)
    """ 
    def execute(self):
        # If there is no file yet, call saveAs
        if self.fileName == None:
            self.open()

        # Show Modal announcement to the user if the gui isn't right
        problemBranches = self.editWidget.testStatus()
        
        if problemBranches:
            dialogs.printDialog(problemBranches)
            return
        
        # Call the python script
        subprocess.call(self.fileName, shell=True)
        pass
    # """
        

    def printer(self):
        print(self.ast)
        
        # Show Modal announcement to the user that the gui isn't right
        problemBranches = self.editWidget.testStatus()
        
        if problemBranches:
            dialogs.printDialog(problemBranches)
        
    
    def save(self):
        # If there is no file yet, call saveAs
        if self.fileName == None:
            self.saveAs()
            return

        if self.ast == None:
            # If there is no ast loaded, create a new file here
            self.newAST()


        # Save the AST as the fileName
        try:
            with open(self.fileName,'w+') as file:
                file.write(self.ast.dumps())
        except TypeError:
            self.saveAs()
            return
        
        # Show a status message
        self.statusBar.showMessage("Successfully saved {}".format(self.fileName))
        
        pass

    def saveAs(self):
        # Open a file
        saveName = QFileDialog.getSaveFileName()
        
        # If no filename is selected, an empty string is placed in self.fileName
        self.fileName = saveName[0]
        
        # If the fileName is blank, stop
        if self.fileName == '':
            self.fileName = None
            return

        # Save the file
        self.save()
        pass

