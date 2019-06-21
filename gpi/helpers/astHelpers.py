# Helper functions for interacting with the abstract syntax tree
from PyQt5.QtGui import QColor
from redbaron import RedBaron as RB

def replace( widget , node , text, gc=QColor(200, 255, 200), bc=QColor(255, 0, 0)):
    # Takes the place of the replace function that is native to the red baron ast structure
    # This function will handle bad input and not crash the software
    
    palette = widget.palette()
    success = 1
    fail = 0
    
    try:
        if len(RB(text)) > 1: raise ValueError
        # Check the input
        node.replace(text)
        # Input passed, turn the widget green
        palette.setColor( widget.backgroundRole() , gc );
        widget.setPalette(palette)
        return success
        
    except :
        # Input failed, give the widget a red outline
        palette.setColor( widget.backgroundRole() , bc );
        widget.setPalette(palette)
        return fail

def replaceTarget( widget , target , text ):
    # Takes the place of the replace function that is native to the red baron ast structure
    # This function will handle bad input and not crash the software
    
    palette = widget.palette()
    
    try:
        # Check the input
        widget.node.target = text 
        # Input passed, turn the widget green
        palette.setColor( widget.backgroundRole() , QColor(200, 255, 200) );
        widget.setPalette(palette)
        pass
        
    except :
        # Input failed, give the widget a red outline
        palette.setColor( widget.backgroundRole() , QColor(255, 0, 0) );
        widget.setPalette(palette)
        pass

class tools:
    def __init__(self, AST):
        # print('tools')
        self.AST = AST

    # def getLayers():
    #     list_o_layers = ['thing1','thing2']
    #     return list_o_layers

# =============================================================================
def getAST(fileName):
    with open(fileName) as module_file:
        string_python = module_file.read()
    ast = RB(string_python)
    return ast
# =============================================================================
def lineNumbers(node):
    # Get the absolute bounding box
    abs_bb = node.absolute_bounding_box

    # Make the string to drop in the label
    if node.type == 'endl':
        end_line = abs_bb.bottom_right.line
        lineNumberString = str(end_line)
        return lineNumberString
    else:
        start_line = abs_bb.top_left.line
        end_line = abs_bb.bottom_right.line

    if end_line == start_line:
        lineNumberString = str(end_line)
    else:
        lineNumberString = '{} to {}'.format(start_line,end_line)
    return lineNumberString
# =============================================================================
