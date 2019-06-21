from PyQt5.QtWidgets import QAction 
# Generate new actions for the menus quickly 
def newAction(GUI , Name , Slot , Shortcut=None):
    # Pass the name of the action, the associated slot, and an optional shortcut, and the menu option will be generated
    action = QAction(Name, GUI)
    
    if Shortcut != None:
        action.setShortcut(Shortcut)
    
    action.triggered.connect( Slot )
    return action
