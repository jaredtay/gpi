import sys

from PyQt5.QtWidgets import QLabel

from gpi.widgets import terminalWidgets, simpleWidgets, standardWidgets

# Module that holds all the classes that can take nodes
thismodule = sys.modules[__name__]

def fetch(node,Multi=False,Simple=False):
    # Check if the caller wants a multiline edit
    if Multi:
        widget = terminalWidgets.MULTI_terminal()
        widget.setup(node)
        return widget , {id(widget):widget}

    elif Simple:
        # Check for comment
        if node.type == 'comment':
            return rb_comment(node)
        # Check for new line 
        elif node.type == 'endl':
            return rb_endl(node)
        # Otherwise, pass it to a single line edit
        else:
            return LE_handle(node)

    # If not, then 
    else:
        try:
            widget , log = getattr(thismodule,'rb_{}'.format(node.type))(node)
            # self.nodeDict[line.type](line)
        
        except Exception as e:
            print(e)
            print(node.dumps())
            
            # Fall back on a line edit
            widget , log = LE_handle(node)
        
        finally:
            pass
            
        
            
        return widget , log

def LE_handle(node):
    widget = terminalWidgets.LE_terminal()
    widget.setup(node)
    return widget , {id(widget):widget}
    

def rb_ifelseblock(node):
    widget, layout = simpleWidgets.simpleWidget(vertical=True)
    
    logs = {}
    
    for branch in node.value:
        subWidget , log = fetch(branch)
        logs.update( log )
        layout.addWidget(subWidget)

    return widget , logs

def rb_else(node):
    return rb_if(node, prepend='else')

def rb_elif(node):
    return rb_if(node, prepend='el')

def rb_if(node, prepend=''):
    widget, layout = simpleWidgets.simpleWidget(vertical=True)
    logs = {}
  
    if prepend != 'else':
        testWidget , testLayout = simpleWidgets.simpleWidget()
   
        # Add the if label
        testLayout.addWidget(simpleWidgets.simpleLabel(prepend + 'if '))
        
        # Add the test node
        subTestWidget , log = fetch(node.test)
        logs.update( log )
        testLayout.addWidget(subTestWidget)

        # Add the trailing colon:
        testLayout.addWidget(simpleWidgets.simpleLabel(':'))
        
        layout.addWidget(testWidget)
    
    else:
        testWidget , testLayout = simpleWidgets.simpleWidget()
        testLayout.addWidget(simpleWidgets.simpleLabel('else:'))
        layout.addWidget(testWidget)

    # Add the rest of the widgets that follow in the value section
    
    # Call back to the editAST class of astElements
    space_widget, space_layout = simpleWidgets.simpleWidget()
    space_layout.addSpacing(50)
    astElements_widget = standardWidgets.ASTWidget(node)
    space_layout.addWidget(astElements_widget)
    layout.addWidget(space_widget)

    # for branch in node.value:
    #     subWidget , log = fetch( branch )
    #     logs.update( log )
    #     layout.addWidget(subWidget)
    # print('Function Call')
    # print(logs)
    return widget , logs

def rb_comparison(node):
    return LE_handle(node)

def rb_def(node):
    widget = terminalWidgets.MULTI_terminal()
    widget.setup(node)
    return widget , {id(widget):widget}
    
def rb_for(node):
    widget, layout = simpleWidgets.simpleWidget(vertical=True)
    logs = {}

    # "For" line
    For_widget, For_layout = simpleWidgets.simpleWidget()

    # for
    For_layout.addWidget(simpleWidgets.simpleLabel('for'))

    # iterator
    # iterator , iterator_log = fetch(node.iterator)
    iterator , iterator_log = LE_handle(node.iterator)
    For_layout.addWidget(iterator)
    logs.update(iterator_log)

    # in
    For_layout.addWidget(simpleWidgets.simpleLabel('in'))

    # target
    # target , target_log = fetch(node.target)
    target , target_log = LE_handle(node.target)
    For_layout.addWidget(target)
    logs.update(target_log)

    # :
    For_layout.addWidget(simpleWidgets.simpleLabel(':'))
    layout.addWidget(For_widget)
   
    # Call back to the editAST class of astElements
    space_widget, space_layout = simpleWidgets.simpleWidget()
    space_layout.addSpacing(50)
    astElements_widget = standardWidgets.ASTWidget(node)
    space_layout.addWidget(astElements_widget)
    layout.addWidget(space_widget)

    # TODO: EditAST needs a way to pass the terminals in a way that makes sense
    terminals = []
    for branch in node:
        t = astElements_widget.branchID_2_terminals[id(branch)]
        logs.update(t)
    
    return widget , logs

def rb_assignment(node):
    # Make the main widget container
    widget, layout = simpleWidgets.simpleWidget()
    logs = {}
    # Left and right side of an equals sign
    # Check the target
    targetWidget , log = fetch(node.target)
    layout.addWidget(targetWidget)
    logs.update( log )

    # Place the equals sign
    layout.addWidget(simpleWidgets.simpleLabel('='))
    
    # Check the value
    valueWidget , log = fetch(node.value)
    logs.update( log )

    layout.addWidget( valueWidget)
    
    return widget , logs

def rb_name(node):
    return LE_handle(node)

def rb_endl(node):
    widget = terminalWidgets.ENDL_terminal()
    return widget , {id(widget):widget}

def rb_int(node):
    return LE_handle(node)

def rb_float(node):
    return LE_handle(node)

def rb_string(node):
    return LE_handle(node)

def rb_binary_operator(node):
    return LE_handle(node)

def rb_unitary_operator(node):
    return LE_handle(node)

def rb_comment(node):
    widget = terminalWidgets.COMMENT_terminal()
    widget.setup(node)
    return widget , {id(widget):widget}

def rb_float_exponant(node):
    return LE_handle(node)

def rb_name_as_name(node):
    return LE_handle(node)

def rb_tuple(node):
    return rb_tupList(node,['(',')'])

def rb_list(node):
    return rb_tupList(node,['[',']'])

def rb_tupList( node, bracketingSymbols):
    # Make the main widget container
    widget, layout = simpleWidgets.simpleWidget()
    logs = {}
    
    # Drop left bracket
    lbWidget = QLabel()
    lbWidget.setText(bracketingSymbols[0])
    layout.addWidget(lbWidget)
    
    n = len(node)
    for i in range(n):
        if i != 0:
            layout.addWidget(simpleWidgets.simpleLabel(','))
            
        child , log = fetch(node[i])
        logs.update( log )

        layout.addWidget( child )
        
    # Drop right bracket
    rbWidget = QLabel()
    rbWidget.setText(bracketingSymbols[1])
    layout.addWidget(rbWidget)
    
    return widget , logs


def rb_dict( node):
    # Make the main widget container
    widget, layout = simpleWidgets.simpleWidget()
    logs = {}

    # Drop left bracket
    layout.addWidget(simpleWidgets.simpleLabel('{'))
    
    n = len(node)
    for i in range(n):
        if i != 0:
            layout.addWidget(simpleWidgets.simpleLabel(','))

        child , log = fetch(node[i].key)
        layout.addWidget( child )
        logs.update( log )
        # Drop right colon
        layout.addWidget(simpleWidgets.simpleLabel(':'))
        
        child , log = fetch(node[i].value)
        layout.addWidget( child )
        logs.update( log )
        
    # Drop right bracket
    layout.addWidget(simpleWidgets.simpleLabel('}'))
    
    return widget , logs


def rb_atomtrailers(node):
    # Make the main widget container
    widget, layout = simpleWidgets.simpleWidget()
    logs = {}
    # Get the length of the tuple
    n = len(node)
    
    # Make a gui element for each entry, and add it to the main gui widget
    for i in range(n):
        child , log = fetch(node[i])
        layout.addWidget(child)
        logs.update( log )

        if (i < n-1):
            if (node[i+1].type == 'name'):
                layout.addWidget(simpleWidgets.simpleLabel('.'))

    return widget , logs


def rb_call(node):
    # Make the main widget container
    widget, layout = simpleWidgets.simpleWidget()
    logs = {}
    # Put parenthesis around this
    layout.addWidget(simpleWidgets.simpleLabel('('))
   
    # Loop through the number of arguments
    n = len(node)
    for i in range(n):
        child , log = fetch(node[i])
        layout.addWidget(child)
        logs.update( log )
        if i != (n-1):
            layout.addWidget(simpleWidgets.simpleLabel(','))
    
    # Put parenthesis around this
    layout.addWidget(simpleWidgets.simpleLabel(')'))

    return widget , logs


def rb_call_argument(node):
    # Make the main widget container
    widget, layout = simpleWidgets.simpleWidget()
    logs = {}
    if node.target:
        # Left and right side of an equals sign
        # Check the target
        targetWidget , log = fetch(node.target)
        layout.addWidget(targetWidget)
        logs.update( log )
        
        # Place the equals sign
        layout.addWidget(simpleWidgets.simpleLabel(' = '))
    
    # Check the value
    valueWidget , log = fetch(node.value)
    layout.addWidget( valueWidget)
    logs.update( log )
        
    return widget , logs


def rb_getitem(node):
    # Make the main widget container
    widget, layout = simpleWidgets.simpleWidget()
    logs = {}
    # Put parenthesis around this
    layout.addWidget(simpleWidgets.simpleLabel('['))
   
    n = len(node)
    
    # Loop through the number of arguments
    child , log = fetch(node.value)
    layout.addWidget(child)
    logs.update( log )
    # Put parenthesis around this
    layout.addWidget(simpleWidgets.simpleLabel(']'))

    return widget , logs

    
def rb_import(node):
    # Revert this type of import to a simply line edit 
    return LE_handle(node)
    # # Make the main widget container
    # widget, layout = simpleWidgets.simpleWidget()
    # # Structure to revert to traditional appearance
    # layout.addWidget(simpleWidgets.simpleLabel('import'))
    # # Check the value
    # child , log = fetch(node[0])
    # layout.addWidget( child )
    # logs.update( log )
    # 
    # return widget , logs


def rb_dotted_as_name(node):
    # Make the main widget container
    widget, layout = simpleWidgets.simpleWidget()
    logs = {} 

    # Check the value
    n = len(node)
    for i in range(n):
        if i != 0:
            layout.addWidget(simpleWidgets.simpleLabel('.'))
        
        child , log = fetch(node[i])
        layout.addWidget( child )
        logs.update( log )
        

    if node.target:
        layout.addWidget(simpleWidgets.simpleLabel(' as '))
        
        # Check the target
        targetWidget = terminalWidgets.LE_terminal()
        targetWidget.setup(node, target=True)
        log = {id(targetWidget):targetWidget}
        layout.addWidget(targetWidget)
        logs.update( log ) 
    
    return widget , logs


def rb_from_import(node):
    return LE_handle(node)
    # # Make the main widget container
    # widget, layout = simpleWidgets.simpleWidget()
    # logs = {}

    # importWidget = QLabel()
    # importWidget.setText('from')
    # layout.addWidget(importWidget)
    # 
    # # Go through the values
    # n = len(node.value)
    # for i in range(n):
    #     if i != 0:
    #         layout.addWidget(simpleWidgets.simpleLabel('.'))
    #     
    #     child , log = fetch(node.value[i])
    #     logs.update( log )
    #     
    #     layout.addWidget( child )
    # 
    # importWidget = QLabel()
    # importWidget.setText('import')
    # layout.addWidget(importWidget)
    # 
    # # Go through the targets
    # n = len(node.targets)
    # for i in range(n):
    #     if i != 0:
    #         layout.addWidget(simpleWidgets.simpleLabel(','))
    #     
    #     child , log = fetch(node.targets[i])
    #     logs.update( log )
    #     
    #     layout.addWidget( child )
    # 
    # return widget , logs

def rb_pass( node):
    widget, layout = simpleWidgets.simpleWidget()
    layout.addWidget(simpleWidgets.simpleLabel('pass'))
    # Set the status of the pass statement to be 1, a success
    widget.status = 1
    return widget , {id(widget):widget}

def rb_list_comprehension(node):
    return LE_handle(node)


