import traceback
import importlib
import pkgutil

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame , QMenu
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from gpi.widgets import terminalWidgets, simpleWidgets
from gpi.widgets.templateWidget import nodeHandler

from gpi.helpers import astHelpers, menuHelpers, dialogs , plugins


def getWidgets():
    return [
            fallbackMulti,
            fallbackLE,
            assignmentCallWidget,
            callWidget,
            emptyLineCatch,
            commentCatch,
            forLoopCatch,
            ifelseCatch,
           ]
# ======================================================================================================
# Available widgets to follow
# ======================================================================================================

# ===========================================================================================
class assignmentCallWidget(nodeHandler):
    # This is a widget framework specialized for assignment widgets
    # It works by identifying an assignment node in the first level of the ast
    # Makes a vertical layout, titles it with a label with the function name in it
    # Drops output labels and line edits, one for each output
    # Drops input labels and line edits, one for each input
    value = 4
    def __init__(self, trueNode, astTools):
        nodeHandler.__init__(self , trueNode, astTools)

    @classmethod
    def nH_getPriority(cls,node, astTools):

        condition1 = False
        condition2 = False

        try:
            condition1 = node.type == 'assignment'
            condition2 = node.value[-1].type == 'call'

        except AttributeError:
            # The node didn't have the values in the right places
            pass
        except IndexError:
            # The node didn't have enough arguments
            pass
        except TypeError:
            # Object doesn't support indexing
            pass

        if condition1 and condition2:
            return cls.value
        else:
            return 0


    @classmethod
    def nH_widgetBuilder(cls, node, astTools):
        # Make the frame
        widget = QFrame()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        terminalsDict = {}

        # Build the widget from the assignment node
        # Set up the title
        titleString = ''
        if len(node.value) == 1:
            titleString = node.value.value
        else:
            for i in range(len(node.value) - 1):
                if i==0:
                    pass
                else:
                    titleString += '.'
                titleString += node.value[i].value

        titleLabel = simpleWidgets.simpleLabel(titleString)
        titleLabel.setAlignment(Qt.AlignHCenter)
        titleLabel.setToolTip(node.dumps())
        layout.addWidget(titleLabel)

        # Add a horizontal widget to put the input and output widgets into
        # Output vertical layout
        input_output_widget = QWidget()
        input_output_layout = QHBoxLayout()
        input_output_widget.setLayout(input_output_layout)

        # Add the outputs
        # If there is just one target, put it in a list
        n = len(node.target)
        if n == 1:
            outputs = [node.target]
        else:
            outputs = node.target

        # Output vertical layout
        output_widget = QWidget()
        output_layout = QVBoxLayout()
        output_widget.setLayout(output_layout)

        outputTitleLabel= simpleWidgets.simpleLabel('Outputs')
        outputTitleLabel.setAlignment(Qt.AlignHCenter)
        output_layout.addWidget(outputTitleLabel)

        for i in range(len(outputs)):
            eachWidget , eachLayout = simpleWidgets.simpleWidget()
            eachLabel = simpleWidgets.simpleLabel('Output {} :'.format(i + 1))
            eachLE    = terminalWidgets.LE_terminal()
            # eachLE    = terminalWidgets.COMBO_terminal()
            eachLE.setup(outputs[i])
            eachLayout.addWidget(eachLabel)
            eachLayout.addWidget(eachLE,1)
            # eachLayout.addStretch(1)
            output_layout.addWidget(eachWidget,1)
            terminalsDict.update({id(eachLE):eachLE})

        input_output_layout.addWidget(output_widget,1)

        # Add the inputs
        inputs = node.value[-1]
        # input vertical layout
        input_widget = QWidget()
        input_layout = QVBoxLayout()
        input_widget.setLayout(input_layout)

        inputTitleLabel= simpleWidgets.simpleLabel('Inputs')
        inputTitleLabel.setAlignment(Qt.AlignHCenter)
        input_layout.addWidget(inputTitleLabel)

        for i, eachInput in enumerate(inputs):
            eachWidget , eachLayout = simpleWidgets.simpleWidget()
            if eachInput.target: # Check for keyword arguments
                input_label = '{} : '.format(eachInput.target)
            else:
                input_label = 'Argument {} : '.format(i+1) # No kwargs
            eachLabel = simpleWidgets.simpleLabel(input_label)
            eachLE    = terminalWidgets.LE_terminal()
            # eachLE    = terminalWidgets.COMBO_terminal()
            eachLE.setup(eachInput.value)
            eachLayout.addWidget(eachLabel)
            eachLayout.addWidget(eachLE,1)
            # eachLayout.addStretch(1)
            input_layout.addWidget(eachWidget,1)
            terminalsDict.update({id(eachLE):eachLE})

        input_output_layout.addWidget(input_widget,1)
        layout.addWidget(input_output_widget,1)

        return widget , terminalsDict

# ===========================================================================================
class callWidget(nodeHandler):
    # This is a widget framework specialized for assignment widgets
    # It works by identifying an assignment node in the first level of the ast
    # Makes a vertical layout, titles it with a label with the function name in it
    # Drops output labels and line edits, one for each output
    # Drops input labels and line edits, one for each input
    value = 4
    def __init__(self, trueNode, astTools):
        nodeHandler.__init__(self,trueNode, astTools)

    @classmethod
    def nH_getPriority(cls,node, astTools):

        condition1 = False
        condition2 = False

        try:
            condition1 = node.type == 'atomtrailers'
            condition2 = node.value[-1].type == 'call'

        except AttributeError:
            # The node didn't have the values in the right places
            pass
        except IndexError:
            # The node didn't have enough arguments
            pass
        except TypeError:
            # Object doesn't support indexing
            pass

        if condition1 and condition2:
            return cls.value
        else:
            return 0


    @classmethod
    def nH_widgetBuilder(cls, node, astTools):
        # Make the frame
        widget = QFrame()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        terminalsDict = {}

        # Build the widget from the assignment node
        # Set up the title
        titleString = ''
        if len(node.value) == 1:
            titleString = node.value.value
        else:
            for i in range(len(node.value) - 1):
                if i==0:
                    pass
                else:
                    titleString += '.'
                titleString += node.value[i].value

        titleLabel = simpleWidgets.simpleLabel(titleString)
        titleLabel.setAlignment(Qt.AlignHCenter)
        titleLabel.setToolTip(node.dumps())
        layout.addWidget(titleLabel)

        # Add the inputs
        inputs = node.value[-1]

        if len(inputs) == 0:
            pass
        else:
            inputTitleLabel= simpleWidgets.simpleLabel('Inputs')
            inputTitleLabel.setAlignment(Qt.AlignHCenter)
            layout.addWidget(inputTitleLabel)

            for i, eachInput in enumerate(inputs):
                eachWidget , eachLayout = simpleWidgets.simpleWidget()
                if eachInput.target: # Check for keyword arguments
                    input_label = '{} : '.format(eachInput.target)
                else:
                    input_label = 'Argument {} : '.format(i+1) # No kwargs
                eachLabel = simpleWidgets.simpleLabel(input_label)
                eachLE    = terminalWidgets.LE_terminal()
                # eachLE    = terminalWidgets.COMBO_terminal()
                eachLE.setup(eachInput.value)
                eachLayout.addWidget(eachLabel)
                eachLayout.addWidget(eachLE,1)
                # eachLayout.addStretch(1)
                layout.addWidget(eachWidget,1)
                terminalsDict.update({id(eachLE):eachLE})

        return widget , terminalsDict
# ======================================================================================================
class fallbackMulti(nodeHandler):
    # The value of the widget dictates its priority
    value = 2

    def __init__(self, trueNode, astTools):
        nodeHandler.__init__(self , trueNode, astTools)

    @classmethod
    def nH_widgetBuilder(cls, node, astTools):
        widget = terminalWidgets.MULTI_terminal()
        widget.setup(node)
        return widget , {id(widget):widget}
# ======================================================================================================
class fallbackLE(nodeHandler):
    # The value of the widget dictates its priority
    value = 3

    def __init__(self, trueNode, astTools):
        nodeHandler.__init__(self , trueNode, astTools)

    @classmethod
    def nH_widgetBuilder(cls, node, astTools):
        widget = terminalWidgets.LE_terminal()
        widget.setup(node)
        return widget , {id(widget):widget}
# ======================================================================================================
class commentCatch(nodeHandler):
    # The value of the widget dictates its priority
    value = 10

    def __init__(self, trueNode, astTools):
        nodeHandler.__init__(self , trueNode, astTools)

    @classmethod
    def nH_getPriority(cls,node, astTools):
        # If the node is a comment, return a value for this gui
        if node.type == 'comment':
            return cls.value
        else:
            return 0

    @classmethod
    def nH_widgetBuilder(cls, node, astTools):
        widget = terminalWidgets.COMMENT_terminal()
        widget.setup(node)
        return widget , {id(widget):widget}
# ======================================================================================================
class emptyLineCatch(nodeHandler):
    # The value of the widget dictates its priority
    value = 10

    def __init__(self, trueNode, astTools):
        nodeHandler.__init__(self, trueNode, astTools)

    @classmethod
    def nH_getPriority(cls,node, astTools):
        # If the node is an empty line, return a value for this gui
        if node.type == 'endl':
            return cls.value
        else:
            return 0

    @classmethod
    def nH_widgetBuilder(cls, node, astTools):
        widget = terminalWidgets.ENDL_terminal()
        return widget , {id(widget):widget}
# ======================================================================================================
class forLoopCatch(nodeHandler):
    # The value of the widget dictates its priority
    value = 10

    def __init__(self, trueNode, astTools):
        nodeHandler.__init__(self , trueNode, astTools)

    @classmethod
    def nH_getPriority(cls,node, astTools):
        # If the node is an empty line, return a value for this gui
        if node.type == 'for':
            return cls.value
        else:
            return 0

    @classmethod
    def nH_widgetBuilder(cls, node, astTools):
        widget, layout = simpleWidgets.simpleWidget(vertical=True)
        logs = {}

        # "For" line
        For_widget, For_layout = simpleWidgets.simpleWidget()

        # for
        For_layout.addWidget(simpleWidgets.simpleLabel('for'))

        # Get the appropriate widget and add it to the layout
        sub_widget = terminalWidgets.LE_terminal()
        sub_widget.setup(node.iterator)
        For_layout.addWidget(sub_widget)
        logs.update( {id(sub_widget):sub_widget} )

        # in
        For_layout.addWidget(simpleWidgets.simpleLabel('in'))

        # Get the appropriate widget and add it to the layout
        sub_widget = terminalWidgets.LE_terminal()
        sub_widget.setup(node.target)
        For_layout.addWidget(sub_widget)
        logs.update( {id(sub_widget):sub_widget} )

        # :
        For_layout.addWidget(simpleWidgets.simpleLabel(':'))
        layout.addWidget(For_widget)

        # Draw up a new ASTWidget to handle the branch
        space_widget, space_layout = simpleWidgets.simpleWidget()
        space_layout.addSpacing(50)
        ASTWidget_widget = ASTWidget(node)
        space_layout.addWidget(ASTWidget_widget)
        layout.addWidget(space_widget)

        # TODO: EditAST needs a way to pass the terminals in a way that makes sense
        for branch in node:
            t = ASTWidget_widget.branchID_2_terminals[id(branch)]
            logs.update(t)

        return widget , logs
# """
class ifelseCatch(nodeHandler):
    # The value of the widget dictates its priority
    value = 10

    def __init__(self, trueNode, astTools):
        nodeHandler.__init__(self, trueNode, astTools)

    @classmethod
    def nH_getPriority(cls, node, astTools):
        # If the node is an empty line, return a value for this gui
        if node.type == 'ifelseblock':
            return cls.value
        else:
            return 0

    @classmethod
    def nH_widgetBuilder(cls, node, astTools):
        widget, layout = simpleWidgets.simpleWidget(vertical=True)
        logs = {}

        ## First if statement ==========================================================================================
        ifnode = node.value[0]
        if_widget , space_widget , new_logs = cls.if_elif_func(ifnode,'if')
        layout.addWidget(if_widget)
        layout.addWidget(space_widget)
        ## =============================================================================================================

        if len(node.value) > 0:
            for i in range(len(node.value)):
                if i == 0:
                    pass
                elif node.value[i].type == 'elif':
                    elifnode = node.value[i]
                    if_widget , space_widget , new_logs = cls.if_elif_func(elifnode,'elif')
                    layout.addWidget(if_widget)
                    layout.addWidget(space_widget)
                else:
                    elsenode = node.value[i]
                    if_widget , space_widget , new_logs = cls.if_elif_func(elsenode)
                    layout.addWidget(if_widget)
                    layout.addWidget(space_widget)

        return widget, logs

    @staticmethod
    def if_elif_func(node, label):
        logs = {}
        # "if" line
        if_widget, if_layout = simpleWidgets.simpleWidget()

        # if
        if_layout.addWidget(simpleWidgets.simpleLabel(label))

        # condition
        sub_widget = terminalWidgets.LE_terminal()
        sub_widget.setup(node.test)
        if_layout.addWidget(sub_widget)
        logs.update({id(sub_widget): sub_widget})

        # :
        if_layout.addWidget(simpleWidgets.simpleLabel(':'))

        # Draw up a new ASTWidget to handle the branch
        space_widget, space_layout = simpleWidgets.simpleWidget()
        space_layout.addSpacing(50)
        ASTWidget_widget = ASTWidget(node)
        space_layout.addWidget(ASTWidget_widget)

        for branch in node:
            t = ASTWidget_widget.branchID_2_terminals[id(branch)]
            logs.update(t)

        return if_widget , space_widget , logs

    @staticmethod
    def else_func(node):
        logs = {}
        # "if" line
        else_widget, else_layout = simpleWidgets.simpleWidget()

        # if
        else_layout.addWidget(simpleWidgets.simpleLabel('else'))

        # :
        else_layout.addWidget(simpleWidgets.simpleLabel(':'))

        # Draw up a new ASTWidget to handle the branch
        space_widget, space_layout = simpleWidgets.simpleWidget()
        space_layout.addSpacing(50)
        ASTWidget_widget = ASTWidget(node)
        space_layout.addWidget(ASTWidget_widget)

        for branch in node:
            t = ASTWidget_widget.branchID_2_terminals[id(branch)]
            logs.update(t)

        return else_widget , space_widget , logs

# """
# ======================================================================================================


class ASTWidget(QFrame):
    # One Dictionary to have all the widgets with their branch id's as keys
    # Calls to 'getWidget' add widgets to this dictionary

    # Make a list of all the plugins
    widgetList = getWidgets()
    plugin_widgetList , intro_widgets = plugins.parse_plugin_widgets()

    # Add the plugin list to the main list
    widgetList.extend(plugin_widgetList)

    def __init__(self, AST):
        QFrame.__init__(self)

        # Bounding box stuff
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)

        # Set the widget information
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # This is the primary copy of the abstract syntax tree
        self.AST = AST

        # This dictionary can be used to make sure widgets are destroyed upon removal
        self.branchID_2_widget = {}
        self.branchID_2_terminals = {}

        # TODO: This is the place to include an object for tracking the AST as a whole
        self.astTools = astHelpers.tools(self.AST)

        self.populate()

    def populate(self, intro=True):
        # =====================================================================
        # Include a section for checking the intro stuff ----------------------

        # Check to see if an intro is possible:
        if intro and len(self.intro_widgets):
            try:
                widget = self.getByPriority(self.AST, self.intro_widgets, self.astTools)

                self.last_intro_node = widget.widget.last_intro_node

                introAstID = id( self.AST[0] )

                # Set up the context menu for the widget
                widget.setContextMenuPolicy(Qt.CustomContextMenu)
                widget.customContextMenuRequested.connect( lambda pos , astID = introAstID : self.introLineNumCMenu( astID , pos ) )

                # Save the widget and the widgets terminals in two dictionaries
                for i , astBranch in enumerate(self.AST):
                    if i > self.last_intro_node:
                        pass
                    else:
                        astID = id( astBranch )
                        self.branchID_2_widget[astID] = widget
                        self.branchID_2_terminals[astID] = widget.terminals

                self.layout.addWidget(widget)

            except Exception as err:
                # dialogs.genDialog('Open Error', 'Trace:\n{}'.format(err))
                traceback.print_exc()
                last_intro_node = 0
                self.last_intro_node = last_intro_node

        else:
            last_intro_node = 0
            self.last_intro_node = last_intro_node


        # Handles for the rest of the AST -------------------------------------
        # Pick the right widget for the ast node
        # for node in rest_of_ast:
        for i , node in enumerate(self.AST):
            if i < self.last_intro_node:
                pass
            else:
                widget , terminals = self.getWidget(node,self.astTools)
                # print(widget)
                # input()

                self.layout.addWidget(widget)
        # =====================================================================

        # Add a stretch to the end so that the widgets will bunch up on the top of the window if there are few widgets drawn.
        # Without this the few widgets will expand and take up entire screen with lots of blank space inside widgets
        self.layout.addStretch(1)

        # Update the line numbers as nodes change
        self.updateLineNo()

    # Right now it is defined because of how the gui is tested
    def slot(self):
        pass

    def testStatus(self):
        # Check for failed gui elements
        problemBranches = []
        fail = 0
        success = 1

        # Look through each branch at the root list
        for i , branch in enumerate(self.AST):
            t = self.branchID_2_terminals[id(branch)]

            # Check for failed statuses in the terminals
            statuses = [t[key].status for key in t]

            # Return the branch number on the root
            if fail in statuses: problemBranches.append( self.AST.index(branch) )

        return problemBranches

    def branchID_2_branch(self):
        # A list with all the branch ids in order
        # Created at function call, it is intimately tied to the AST status at function call
        return  [ id(branch) for branch in self.AST ]

    def removeWidget(self, astId):
        # Disconnect the context menu slot
        try:
            self.branchID_2_widget[astId].customContextMenuRequested.disconnect()
            # Disable the slots on the widget
            for key in self.branchID_2_terminals[astId]:
                self.branchID_2_terminals[astId][key].disable()
        except RuntimeError:
            pass

        # Remove the widget from the view
        self.branchID_2_widget[astId].setParent(None)

        # Remove the widget from the widget dictionary
        del self.branchID_2_widget[astId]

    def insertWidget(self, astIndex, widget):
        # With intro, index of layout may not match index of ast
        if self.last_intro_node == 0:
            self.layout.insertWidget(astIndex ,widget)
        else:
            self.layout.insertWidget(astIndex - self.last_intro_node + 1,widget)

    def getWidget(self,node,astTools,simple=False):
        # Get the widget that will hold the AST gui elements

        # If simple is called for, use a line edit
        # TODO: This call doesn't look for compatibility, should separate compatibility check from priority check
        if simple:
            widget = fallbackMulti(node, astTools)
        else:
            widget = self.getByPriority(node, self.widgetList, astTools)

        # Set up the context menu for the widget
        widget.setContextMenuPolicy(Qt.CustomContextMenu)
        widget.customContextMenuRequested.connect( lambda pos , astID = id(node) : self.lineNumCMenu( astID , pos ) )

        # Save the widget and the widgets terminals in two dictionaries
        self.branchID_2_widget[id(node)] = widget
        self.branchID_2_terminals[id(node)] = widget.terminals

        return widget , widget.terminals

    def getByPriority(self, node, widgetSet, astTools):

        # Test each available widget
        # Return a widget representing the best widget available
        # Highest priority means is the largest number
        # Incompatability is a 0

        # Make a list of the priorities
        priorityMap = [w.nH_getPriority(node, astTools) for w in widgetSet]

        # Make a dictionary where the id of the widgets are the keys and the priorities are stored
        d = { id(w):p for p , w in zip(priorityMap,widgetSet)}

        # Use that dictionary to sort the widgets
        sortedWidgets = sorted(widgetSet, key=lambda w: d[id(w)] , reverse=True)
        # Return the widget with the highest priority

        return sortedWidgets[0](node, astTools)

    def lineNumCMenu(self , astID , pos ):
        # Create the menu
        CMenu = QMenu()
        CMenu.addAction(menuHelpers.newAction(self, 'New'        , lambda ignore , astID = astID : self.new(astID) ) )
        CMenu.addAction(menuHelpers.newAction(self, 'Duplicate'  , lambda ignore , astID = astID : self.duplicate(astID) ) )
        CMenu.addAction(menuHelpers.newAction(self, 'Move Up'    , lambda ignore , astID = astID : self.move(astID, -1) ) )
        CMenu.addAction(menuHelpers.newAction(self, 'Move Down'  , lambda ignore , astID = astID : self.move(astID, 1) ) )
        CMenu.addAction(menuHelpers.newAction(self, 'Remove'     , lambda ignore , astID = astID : self.remove(astID) ) )
        CMenu.addAction(menuHelpers.newAction(self, 'Regenerate' , lambda ignore , astID = astID : self.regenerate(astID) ) )
        CMenu.addAction(menuHelpers.newAction(self, 'Raw'        , lambda ignore , astID = astID : self.regenerate(astID, simple=True) ) )

        # Get the global position
        globalPos = self.branchID_2_widget[astID].mapToGlobal(pos)

        # Send out the menu
        CMenu.exec_(globalPos)

# Functions to be used only if there is an introductory widget =========================================================
    def introLineNumCMenu(self , astID , pos ):
        # Create the menu
        CMenu = QMenu()
        CMenu.addAction( menuHelpers.newAction(self, 'Split'        , lambda ignore : self.introSplit() ) )

        # Get the global position
        globalPos = self.branchID_2_widget[astID].mapToGlobal(pos)

        # Send out the menu
        CMenu.exec_(globalPos)

    def introSplit(self):
        # Remove everything from the gui
        def deleteItems(layout):
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    else:
                        deleteItems(item.layout())

        deleteItems(self.layout)

        # Rebuild the dictionaries
        self.branchID_2_widget = {}
        self.branchID_2_terminals = {}

        # Add everything back, ignoring the introduction special treatment
        self.populate(intro=False)

        pass
# ======================================================================================================================

    def new(self,astID):
        # Find what widget was chosen
        index = self.branchID_2_branch().index(astID)

        # Insert a new line in the AST, a comment
        newLine = '# New Line'
        self.AST.insert(index,newLine)

        # Add the widget to the GUI
        widget , terminals = self.getWidget(self.AST[index], self.astTools)
        self.insertWidget(index,widget)

        # Update Line Numbers
        self.updateLineNo()

    def duplicate(self,astID):
        # Find what widget was chosen
        index = self.branchID_2_branch().index(astID)

        # Add the new line to the ast
        duplicateSyntax = self.AST[index].dumps()
        self.AST.insert(index,duplicateSyntax)

        # Insert new widget in the gui
        widget , terminals = self.getWidget(self.AST[index], self.astTools)
        self.insertWidget(index,widget)

        # Update Line Numbers
        self.updateLineNo()

    def regenerate(self,astID,simple=False):
        # Find what widget was chosen
        index = self.branchID_2_branch().index(astID)

        # Remove the old widget
        self.removeWidget(astID)

        # Insert the new widget
        widget , terminals = self.getWidget(self.AST[index], self.astTools, simple=simple)

        # With intro, index of layout may not match index of ast
        self.insertWidget(index,widget)

        # Update Line Numbers for this widget
        self.updateLineNo()

    def move(self, astID, step):
        # Find what widget was chosen
        index = self.branchID_2_branch().index(astID)

        # Check if it is the first or the last entry
        if self.last_intro_node == 0:
            introFudge = 0
        else:
            introFudge = self.last_intro_node

        if (index + step >= 0 + introFudge) and (index + step < len(self.AST)):
            # Remove the old widget
            # With intro, index of layout may not match index of ast
            self.removeWidget(astID)

            # Duplicate the branch
            duplicateSyntax = self.AST[index].dumps()

            # Remove the old branch in the tree
            del self.AST[index]

            # Add it back
            self.AST.insert(index+step,duplicateSyntax)

            # Make a new widget
            widget , terminals = self.getWidget(self.AST[index+step], self.astTools)

            # Add the widget to the layout where it is supposed to be
            # With intro, index of layout may not match index of ast
            # self.layout.insertWidget(index+step,widget)
            self.insertWidget(index+step,widget)

        # Update Line Numbers
        self.updateLineNo()

    def remove(self, astID):

        # Remove the branch from the root node
        index = self.branchID_2_branch().index(astID)
        del self.AST[index]

        # Remove the old widget
        # With intro, index of layout may not match index of ast
        self.removeWidget(astID)

        # Update Line Numbers
        self.updateLineNo()

    def updateLineNo(self):
        # Loop through each widget in the gui
        """
        # for key in self.branchID_2_widget.keys():
        #     w = self.branchID_2_widget[key]
            # Put in the line number
            # print(dir(w))
            if 'lineNumbers' in dir(w):
                w.line_number.setText(w.lineNumbers(w.node))
            else:
                w.line_number.setText(astHelpers.lineNumbers(w.node))
            # Put in the ast branch index
            # index = self.branchID_2_branch().index(key)
            # w.line_number.setText(str(index))
        """
        self.get_thread = getNumberingThread(self.branchID_2_widget, self.updateLineNumber)
        self.get_thread.start()

    def updateLineNumber(self, line_numbers , nodeID):
        # print(line_numbers)
        # print(nodeID)
        for i in range(len(line_numbers)):
            w = self.branchID_2_widget[int(nodeID[i])]
            w.line_number.setText(line_numbers[i])

class getNumberingThread(QThread):

    signal = pyqtSignal(list, list)

    def __init__(self, branchID_2_widget, slot):
        """
        Make a new thread instance with the specified
        subreddits as the first argument. The subreddits argument
        will be stored in an instance variable called subreddits
        which then can be accessed by all other class instance functions

        :param subreddits: A list of subreddit names
        :type subreddits: list
        """
        QThread.__init__(self)
        self.branchID_2_widget = branchID_2_widget

        self.signal.connect(slot)

    # def __del__(self):
    #     self.wait()

    def run(self):
        """
        Go over every item in the self.subreddits list
        (which was supplied during __init__)
        and for every item assume it's a string with valid subreddit
        name and fetch the top post using the _get_top_post method
        from reddit. Store the result in a local variable named
        top_post and then emit a SIGNAL add_post(QString) where
        QString is equal to the top_post variable that was set by the
        _get_top_post function.

        """
        # for subreddit in self.branchID_2_widget:
        #     top_post = self._get_top_post(subreddit)
        #     self.emit(SIGNAL('add_post(QString)'), top_post)
        #     self.sleep(2)
        linenumber_strings = []
        id_strings = []
        self.sleep(1)
        for key in self.branchID_2_widget.keys():
            w = self.branchID_2_widget[key]
            # Put in the line number
            # print(dir(w))
            if 'lineNumbers' in dir(w):
                # w.line_number.setText(w.lineNumbers(w.node))
                line_numbers = w.lineNumbers(w.node)
            else:
                # w.line_number.setText(astHelpers.lineNumbers(w.node))
                line_numbers = astHelpers.lineNumbers(w.node)

            # print(line_numbers)
            # print(id(w.node))
            linenumber_strings.append(line_numbers)
            id_strings.append(str(key))

        self.signal.emit(linenumber_strings, id_strings)
            # Put in the ast branch index
            # index = self.branchID_2_branch().index(key)
            # w.line_number.setText(str(index))
