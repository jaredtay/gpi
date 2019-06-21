# Dialogs

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit

class printDialog(QDialog):
    def __init__(self,pBranches):
        QDialog.__init__(self)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Label
        label = QLabel()
        text = 'There are errors in the following branch(es):\n'
        for w in pBranches:
            text += 'Branch {}\n'.format(w)
        label.setText(text)
        layout.addWidget(label)
        
        # Button
        
        # Title
        self.setWindowTitle( 'Printing Error' )
        
        self.exec_()

class genDialog(QDialog):
    """
    General Dialog box
    """
    def __init__(self,title,text):
        """
        INPUTS:
        title: title of the window
        text: text in the window
        """

        QDialog.__init__(self)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Label
        # label = QLabel()
        # label.setText(text)
        # layout.addWidget(label)
        
        #Text Edit
        TE = QTextEdit()
        TE.setWordWrapMode(1)
        TE.setReadOnly(1)
        TE.setPlainText(text)
        layout.addWidget(TE)
        # Title
        self.setWindowTitle( title )
        
        self.exec_()
