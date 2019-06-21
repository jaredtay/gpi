from PyQt5.QtWidgets import QHBoxLayout , QFrame , QLabel
import copy

class nodeHandler(QFrame):
    """
    Parent class to all other widgets.
    Holds the important structure to unify the appearance before being 
    inserted into the window.
    """
    incompatible = 0

    def __init__( self , trueNode , astTools ):
        """
        This is the generic structure of the ast widgets.
        """
        QFrame.__init__(self)

        # Bounding box stuff
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)

        # Set the layout
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        
        # Add a dummy label for a line number to be added later
        self.line_number = QLabel()
        self.line_number.setText('#')
        self.line_number.setToolTip('Line Number(s)')
        self.layout.addWidget(self.line_number)
        
        # Run the bijective test every time the widget is created 
        # print('BijectiveTest')
        self.nH_bijectiveTest(trueNode, astTools)
        
        # If the we are still going, the test passed, and a widget can be made from the trueNode
        # print('Real Thing')
        widget , terminals = self.nH_widgetBuilder(trueNode, astTools)
       
        # Add the widget to the layout
        self.layout.addWidget(widget)
        
        # Add the trueNode and terminals to the widget for use later
        self.node  = trueNode
        self.terminals = terminals
        self.widget = widget

    @classmethod
    def nH_getPriority(cls,node, astTools):
        # Priority here is defined as if it works it has a set priority, if it doesn't work, it isn't
        # compatible. 
        # widget , terminals = cls.nH_widgetBuilder(node)
        try:
            # print('Get Priority')
            widget , terminals = cls.nH_widgetBuilder(node, astTools)
            return cls.value
        except ValueError:
            return cls.incompatible
 
    # Need the class method to allow getPriority to run without a self object
    @classmethod
    def nH_bijectiveTest(cls, trueNode, astTools):
        # Get the appropriate widget for the copy of the node
        testNode = copy.copy(trueNode)
        widget , terminals = cls.nH_widgetBuilder(testNode, astTools)
        
        # Execute all slots in the GUI
        # assert len(terminals) > 0
        for key in terminals:
            terminals[key].slot()

        # Check that nothing has changed and raise if it has
        failed = ( trueNode.dumps() != testNode.dumps() )
        if failed:
            raise ValueError('Bijective Test Failed at \"{}\"'.format(trueNode.dumps())) 
        pass 
    
    @classmethod
    def nH_widgetBuilder(cls , node, astTools):
        raise NotImplementedError('Node handler \'{}\' needs a widgetBuilder method.'.format(cls))


