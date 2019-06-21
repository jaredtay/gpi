#! /usr/bin/python3

## Pure Python Imports
import sys

## PyQt5 Imports
from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar


from gpi import view
from gpi.helpers.menuHelpers import newAction


class mainWindow(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle( 'Instruction Set Editor' )

        ## Set Status Bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Welcome")

        ## Building the View
        self.view = view.view(self.statusBar)
        self.setCentralWidget(self.view)

        ## Set the menus
        mainMenu = self.menuBar()
        menuBuilder( self , self.view , mainMenu )
        
        # Size the gui
        self.resize(1000,700)

        ## Starting the Gui
        self.show()

    def closeApplication(self):
        sys.exit()

# Menus =================================================================================================
def menuBuilder(GUI , astGui, mainMenu):
    fileMenu = mainMenu.addMenu('&File')
    helpMenu = mainMenu.addMenu('&Help')

    fileMenu.addAction( newAction(GUI, '&New',   astGui.new                , Shortcut="Ctrl+N") )
    fileMenu.addAction( newAction(GUI, '&Open',   astGui.open               , Shortcut="Ctrl+O") )
    # fileMenu.addAction( newAction(GUI, '&Execute',astGui.execute            , Shortcut="Ctrl+E") )
    fileMenu.addAction( newAction(GUI, '&Save',   astGui.save               , Shortcut="Ctrl+s") )
    fileMenu.addAction( newAction(GUI, 'Save As', astGui.saveAs             , Shortcut="Ctrl+Shift+S") )
    fileMenu.addAction( newAction(GUI, '&Exit',   sys.exit                  , Shortcut="Ctrl+W") )

    # Developer helper, print the AST in its current state
    fileMenu.addAction( newAction(GUI, '&Print',  astGui.printer            , Shortcut="Ctrl+P") )

    AboutTitle = 'De-La-Mo Instruction Set Editor'
    AboutText  = 'Create new instruction sets\nfor De-La-Mo composite delamination modeller.\nDeveloped at the Center for Nondestructive Evaluation,\nIowa State University.'
    helpMenu.addAction( newAction(GUI, 'About',   lambda _ ,title=AboutTitle, text=AboutText :  dialogs.genDialog( title , text ) ) )

# Run the program
def run():
    # Start the application
    app = QApplication(sys.argv)

    # Create the GUI
    GUI = mainWindow()

    # Enter the application
    app.exec_()

    # Proper exiting of the application
    # sys.exit(app.exec_())

if __name__ == '__main__':
    run()
