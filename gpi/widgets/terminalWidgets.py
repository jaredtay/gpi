from PyQt5.QtWidgets import QLineEdit, QComboBox, QWidget, QTextEdit
from PyQt5.QtGui import QColor, QFontMetrics

from gpi.helpers import astHelpers


class MULTI_terminal(QTextEdit):
    def __init__(self,*args):
        QTextEdit.__init__(self)

        # Set text to be monospace
        doc = self.document()
        font = doc.defaultFont()
        font.setFamily("Courier New")
        doc.setDefaultFont(font)
    
        # Set the background color to green
        palette = self.palette()
        palette.setColor( self.backgroundRole(), QColor(200, 255, 200))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Set the height of the box
        # 10 Lines tall
        nRows = 10
        doc = self.document()
        fm = QFontMetrics( doc.defaultFont() )
        margins = self.contentsMargins()
        height = fm.lineSpacing() * nRows + 2*(doc.documentMargin() + self.frameWidth()) + margins.top() + margins.bottom()
        self.setFixedHeight(height)

    def setup(self, node):
        self.node = node
        self.setPlainText(node.dumps())
        
        self.textChanged.connect( self.slot )
        
        # Start the status in the success state
        self.status = 1
        
    
    def slot(self):
        astHelpers.replace(self, self.node, self.toPlainText())
    
    def disable(self):
        self.textChanged.disconnect()

class LE_terminal(QLineEdit):
    def __init__(self,*args):
        QLineEdit.__init__(self)
        
        # Set the background color to green
        palette = self.palette()
        palette.setColor( self.backgroundRole() , QColor(200, 255, 200) );
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
    def setup(self, node, target=False):
        self.node = node

        self.setText(self.node.dumps())
       
        # If target is needed
        if target:
            self.textChanged.connect( self.slot_target )
        else:
            self.textChanged.connect( self.slot )

        # Start the status in the success state
        self.status = 1
    
    def slot(self):
        self.status = astHelpers.replace(self, self.node, self.text())
    
    def slot_target(self):
        self.status = astHelpers.replaceTarget(self, self.node, self.text())

    def disable(self):
        self.textChanged.disconnect()

class COMBO_terminal(QComboBox):
    def __init__(self,*args):
        QComboBox.__init__(self)
        
        # Set the background color to green
        palette = self.palette()
        palette.setColor( self.backgroundRole() , QColor(200, 255, 200) );
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Allow the user to add their own stuff
        self.setEditable(True) 
        
        # Do not add what the user added to the dropdown
        self.setInsertPolicy(0)

    def setup(self, node):
        self.node = node
        # print(node)

        self.insertItem(0,self.node.dumps())
        # self.editingFinished.connect( self.slot )
        self.currentTextChanged.connect( self.slot )
        # Start the status in the success state
        self.status = 1
    
    def slot(self):
        self.status = astHelpers.replace(self, self.node, self.currentText())
    
    def disable(self):
        self.currentTextChanged.disconnect()

class ENDL_terminal(QWidget):
    # This is a bare widget that has a 'slot' and 'disable' defined to allow an end line to be compatible
    def __init__(self,*args):
        QWidget.__init__(self)
        self.status = 1
    
    def slot(self):
        pass
    
    def disable(self):
        pass

class COMMENT_terminal(QLineEdit):
    def __init__(self,*args):
        QLineEdit.__init__(self)
        
        
    def setup(self, node, target=False):
        self.node = node
        nodeText = self.node.dumps() 

        if nodeText[:2] == '#!':
            #If the comment starts with '#!', this is a special comment, color it blue
            self.goodColor = QColor(100,200,255)
            self.badColor  = QColor(200,0,0)
        else:
            # Set the colors
            self.goodColor = QColor(200,200,200)
            self.badColor  = QColor(200,0,0)

        # Set the background color to gray, the good color
        palette = self.palette()
        palette.setColor( self.backgroundRole() , self.goodColor );
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
        self.setText(nodeText)
       
        # If target is needed
        self.textChanged.connect( self.slot )

        # Start the status in the success state
        self.status = 1
    
    def slot(self):
        self.status = astHelpers.replace(self, self.node, self.text(), gc=self.goodColor, bc=self.badColor)
    
    def disable(self):
        self.textChanged.disconnect()
