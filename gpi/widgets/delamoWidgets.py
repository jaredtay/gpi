from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt

from gpi.widgets import terminalWidgets, simpleWidgets, templateWidget


def getWidgets():
    return [CreateFromMold]# ,introWidget,DelamoModeler_Initialize,Output_Filenames]

def getIntros():
    return [introWidget]
# ===========================================================================================

class CreateFromMold(templateWidget.nodeHandler):
    """
    Documentation from the API
    Create a layer atop the specified mold. 
     * direction: "OFFSET" or "ORIG"
     * thickness: Thickness of layer (offsetting operation)
     * name: Unique name for layer
     * Section: ABAQUS section fo the layer
     * layup: Ply orientation in degrees
     * coordsys: Reference coordinate system for layup
    """
    value = 5
    def __init__(self, trueNode, astTools):
        super(self.__class__, self).__init__(trueNode, astTools)

    @classmethod
    def nH_getPriority(cls,node, astTools):

        condition1 = False
        condition2 = False

        try:
            condition1 = node.value[0].value == 'Layer'
            condition2 = node.value[1].value == 'CreateFromMold'

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

        

    @staticmethod
    def nH_widgetBuilder(node, astTools):
        # Make the frame
        widget = QFrame()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        terminalsDict = {}

        # Add the title
        titleLabel = simpleWidgets.simpleLabel('Create From Mold')
        titleLabel.setToolTip(node.dumps())
        titleLabel.setAlignment(Qt.AlignHCenter)
        layout.addWidget(titleLabel)

        ## Check for each positional argument
        labels_tooltips_nodes = []

        DM_label = 'DM Object : '
        DM_tooltip = 'Name of the de-la-mo model object'
        DM_node = node.value.value[2].value[0]
        labels_tooltips_nodes.append([DM_label,DM_tooltip,DM_node])

        mold_label = 'Mold : '
        mold_tooltip = 'Mold'
        mold_node = node.value.value[2].value[1]
        labels_tooltips_nodes.append([mold_label,mold_tooltip,mold_node])
        
        direction_label = 'Direction : '
        direction_tooltip = '\'OFFSET\' or \'ORIG\' '
        direction_node = node.value.value[2].value[2]
        labels_tooltips_nodes.append([direction_label,direction_tooltip,direction_node])

        thickness_label= 'Layer thickness : '
        thickness_tooltip = 'Layer thickness'
        thickness_node = node.value.value[2].value[3]
        labels_tooltips_nodes.append([thickness_label,thickness_tooltip,thickness_node])

        name_label = 'Unique layer name : '
        name_tooltip = 'Unique layer name'
        name_node = node.value.value[2].value[4]
        labels_tooltips_nodes.append([name_label,name_tooltip,name_node])

        section_label = 'Section : '
        section_tooltip = 'ABAQUS section of the layer'
        section_node = node.value.value[2].value[5]
        labels_tooltips_nodes.append([section_label,section_tooltip,section_node])

        layup_label= 'Ply orientation : '
        layup_tooltip = 'Ply orientation in degrees'
        layup_node = node.value.value[2].value[6]
        labels_tooltips_nodes.append([layup_label,layup_tooltip,layup_node])
       
        # Add a horizontal widget to put the input and output widgets into
        # Output vertical layout
        input_output_widget = QWidget()
        input_output_layout = QHBoxLayout()
        input_output_widget.setLayout(input_output_layout)

        # input vertical layout
        input_widget = QWidget()
        input_layout = QVBoxLayout()
        input_widget.setLayout(input_layout)
        input_Label = simpleWidgets.simpleLabel('Inputs')
        input_Label.setAlignment(Qt.AlignHCenter)
        input_layout.addWidget(input_Label)

        # Build the GUI
        for label , tooltip , astNode in labels_tooltips_nodes:
            eachWidget , eachLayout = simpleWidgets.simpleWidget()
            eachLabel = simpleWidgets.simpleLabel(label)
            eachLabel.setToolTip(tooltip)
            eachLE    = terminalWidgets.LE_terminal()
            # eachLE    = terminalWidgets.COMBO_terminal()
            eachLE.setup(astNode)
            eachLayout.addWidget(eachLabel)
            eachLayout.addWidget(eachLE,1)
            # eachLayout.addStretch(1)
            input_layout.addWidget(eachWidget,1)
            terminalsDict.update({id(eachLE):eachLE})

        ## Check for keyword arguments
        if node.value.value[2].value[7].target.value == 'coordsys':
            coordsys_tooltip = 'Reference coordinate system for layup'
            coordsys_node = node.value.value[2].value[7].value

            anotherWidget , anotherLayout = simpleWidgets.simpleWidget()
            anotherLabel = simpleWidgets.simpleLabel('coordsys : ')
            anotherLabel.setToolTip(tooltip)
            anotherLE    = terminalWidgets.LE_terminal()
            # eachLE    = terminalWidgets.COMBO_terminal()
            anotherLE.setup(coordsys_node)
            anotherLayout.addWidget(anotherLabel)
            anotherLayout.addWidget(anotherLE,1)
            # eachLayout.addStretch(1)
            input_layout.addWidget(anotherWidget,1)
            terminalsDict.update({id(anotherLE):anotherLE})

        # Outputs
        # Output vertical layout
        output_widget = QWidget()
        output_layout = QVBoxLayout()
        output_widget.setLayout(output_layout)
        output_Label = simpleWidgets.simpleLabel('Outputs')
        output_Label.setAlignment(Qt.AlignHCenter)
        output_layout.addWidget(output_Label)

        label = 'New Layer : '
        tooltip = 'Create a new layer from a mold'
        astNode = node.target
        eachWidget , eachLayout = simpleWidgets.simpleWidget()
        eachLabel = simpleWidgets.simpleLabel(label)
        eachLabel.setToolTip(tooltip)
        eachLE    = terminalWidgets.LE_terminal()
        # eachLE    = terminalWidget.COMBO_terminal()
        eachLE.setup(astNode)
        eachLayout.addWidget(eachLabel)
        eachLayout.addWidget(eachLE,1)
        # eachLayout.addStretch(1)
        output_layout.addWidget(eachWidget,1)
        terminalsDict.update({id(eachLE):eachLE})

        # Add output and input widgets to the main input_output_layout
        input_output_layout.addWidget(output_widget)
        input_output_layout.addWidget(input_widget)

        # Add input_output_widget to the main layout
        layout.addWidget(input_output_widget)

        return widget , terminalsDict

# ===========================================================================================

class introWidget(templateWidget.nodeHandler):
    """
    Standard widget for the initialization of de-la-mo scripts
    """
    def __init__(self, trueNode, astTools):
        super(self.__class__, self).__init__(trueNode, astTools)

    @classmethod
    def nH_getPriority(cls, node, astTools):
        # Check to see if the intro is the right format
        # Make a check in the future
        if node[15].dumps == "# Initialize the DeLaMo model":
            return 1
        else:
            return 0

        # if node.type == 'comment':
        #     return cls.value 
        # else:
        #     return 0

    @classmethod
    def nH_bijectiveTest(cls, trueNode, astTools):
        # TODO: Fix this so it works on a copy of the node
        # Get the appropriate widget for the copy of the node
        # testNode = copy.copy(trueNode)
        widget , terminals = cls.nH_widgetBuilder(trueNode, astTools)
        
        # Execute all slots in the GUI
        # assert len(terminals) > 0
        for key in terminals:
            terminals[key].slot()

        # Check that nothing has changed and raise if it has
        # failed = ( trueNode.dumps() != testNode.dumps() )
        # if failed:
        #     raise ValueError('Bijective Test Failed at \"{}\"'.format(trueNode.dumps())) 
        # pass 
    

    @classmethod
    def nH_widgetBuilder(cls , ast, astTools):
        # Make the frame
        widget = QFrame()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        terminalsDict = {}

        # Save the last_intro_node
        widget.last_intro_node = 66

        # Set up the title
        titleString = 'De-La-Mo Initialization'

        titleLabel = simpleWidgets.simpleLabel(titleString)
        titleLabel.setAlignment(Qt.AlignHCenter)

        intro_dump = ''
        for i in range(widget.last_intro_node):
            intro_dump += ast[i].dumps()
            intro_dump += '\n'

        titleLabel.setToolTip(intro_dump)
        layout.addWidget(titleLabel)
        
        descriptionText = \
        'This block hides a significant amount of the initialization of the script. It holds \n \
        the code that imports de-la-mo modules, loads parameters, and instantiates tools used \n \
        in the rest of the script. It is not important to the end user, but if the user is \n \
        interested they may right click on the block and select \'Split\' from the menu, or \n \
        the user may look at the raw code in a text editor.'
        description = simpleWidgets.simpleLabel(descriptionText)
        description.setAlignment(Qt.AlignHCenter)
        layout.addWidget(description)
        
        # input and output lists
        input_labels_tooltips_nodes  = []
        output_labels_tooltips_nodes = []
        
        # Example
        # DM_label = 'DM Object : '
        # DM_tooltip = 'Name of the de-la-mo model object'
        # DM_node = node.value.value[2].value[0]
        # input_labels_tooltips_nodes.append([DM_label,DM_tooltip,DM_node])

        # Node 16
        DM_label = 'DM Object : '
        DM_tooltip = 'Name of the de-la-mo model object'
        DM_node = ast[16].target
        output_labels_tooltips_nodes.append([DM_label,DM_tooltip,DM_node])

        # Node 34
        ScriptName_label = 'Script Name : '
        ScriptName_tooltip = 'Should match the name of the python script open here, with quotes.'
        ScriptName_node = ast[34].value.value[2][0].value
        input_labels_tooltips_nodes.append([ScriptName_label,ScriptName_tooltip,ScriptName_node])

        # Node 41
        parameter_label = 'Abaqus Parameter File : '
        parameter_tooltip = ''
        parameter_node = ast[41].value[2][0].value
        input_labels_tooltips_nodes.append([parameter_label,parameter_tooltip,parameter_node])


       
        # Add a horizontal widget to put the input and output widgets into
        # Output vertical layout
        input_output_widget = QWidget()
        input_output_layout = QHBoxLayout()
        input_output_widget.setLayout(input_output_layout)

        # input vertical layout
        input_widget = QWidget()
        input_layout = QVBoxLayout()
        input_widget.setLayout(input_layout)
        input_Label = simpleWidgets.simpleLabel('Inputs')
        input_Label.setAlignment(Qt.AlignHCenter)
        input_layout.addWidget(input_Label)

        # Build the GUI
        for label , tooltip , astNode in input_labels_tooltips_nodes:
            eachWidget , eachLayout = simpleWidgets.simpleWidget()
            eachLabel = simpleWidgets.simpleLabel(label)
            eachLabel.setToolTip(tooltip)
            eachLE    = terminalWidgets.LE_terminal()
            # eachLE    = terminalWidgets.COMBO_terminal()
            eachLE.setup(astNode)
            eachLayout.addWidget(eachLabel)
            eachLayout.addWidget(eachLE,1)
            # eachLayout.addStretch(1)
            input_layout.addWidget(eachWidget,1)
            terminalsDict.update({id(eachLE):eachLE})

        # Outputs
        # Output vertical layout
        output_widget = QWidget()
        output_layout = QVBoxLayout()
        output_widget.setLayout(output_layout)
        output_Label = simpleWidgets.simpleLabel('Outputs')
        output_Label.setAlignment(Qt.AlignHCenter)
        output_layout.addWidget(output_Label)

        # Build the GUI
        for label , tooltip , astNode in output_labels_tooltips_nodes:
            eachWidget , eachLayout = simpleWidgets.simpleWidget()
            eachLabel = simpleWidgets.simpleLabel(label)
            eachLabel.setToolTip(tooltip)
            eachLE    = terminalWidgets.LE_terminal()
            # eachLE    = terminalWidgets.COMBO_terminal()
            eachLE.setup(astNode)
            eachLayout.addWidget(eachLabel)
            eachLayout.addWidget(eachLE,1)
            # eachLayout.addStretch(1)
            output_layout.addWidget(eachWidget,1)
            terminalsDict.update({id(eachLE):eachLE})

        # Add output and input widgets to the main input_output_layout
        input_output_layout.addWidget(output_widget)
        input_output_layout.addWidget(input_widget)

        # Add input_output_widget to the main layout
        layout.addWidget(input_output_widget)


        return widget , terminalsDict

    @classmethod
    def lineNumbers(cls, node):
        # # Get the absolute bounding box
        # abs_bb = node[0].absolute_bounding_box
        # start_line = abs_bb.top_left.line
        # abs_bb = node[65].absolute_bounding_box
        # end_line = abs_bb.bottom_right.line

        # lineNumberString = '{} to {}'.format(start_line,end_line)
        lineNumberString = 'Intro'
        return lineNumberString

# ===========================================================================================
class DelamoModeler_Initialize(templateWidget.nodeHandler):
    value = 5
    def __init__(self, trueNode, astTools):
        super(self.__class__, self).__init__(trueNode, astTools)

    @classmethod
    def nH_getPriority(cls, node, astTools):

        condition1 = False
        condition2 = False

        try:
            condition1 = node.value.value[0].value == 'DelamoModeler'
            condition2 = node.value.value[1].value == 'Initialize'
        except AttributeError:
            # The node didn't have the values in the right places
            pass
        if condition1 and condition2:
            return cls.value

        else:
            return 0
        

    @staticmethod
    def nH_widgetBuilder(node, astTools):
        # Make the frame
        widget = QFrame()
        
        # Open the .ui file created in QtDesigner
        scriptdir=os.path.abspath(os.path.split(sys.modules[test.__module__].__file__)[0])
        uifile = open(os.path.join(scriptdir,'assets','ui','DMI.ui'))

        # Load the .ui file
        uic.loadUi(uifile,widget)

        # Close the file
        uifile.close()
        
        # Setup the terminals in the widget
        widget.fptf.setup(node.value.value[2][1].value)
        widget.nt.setup(node.value.value[2][2].value)

        # For now just make an empty dictionary for the log
        terminalsDict = {id(widget.fptf):widget.fptf,
               id(widget.nt):widget.nt,
              }


        return widget , terminalsDict

# =============================================================================

class Output_Filenames(templateWidget.nodeHandler):
    value = 5
    def __init__(self, trueNode, astTools):
        super(self.__class__, self).__init__(trueNode, astTools)

    @classmethod
    def nH_getPriority(cls, node, astTools):

        condition1 = False
        condition2 = False

        try:
            condition1 = node.value.value[0].value == 'process'
            condition2 = node.value.value[1].value == 'output_filenames'
        except AttributeError:
            # The node didn't have the values in the right places
            pass
        if condition1 and condition2:
            return cls.value

        else:
            return 0
        

    @staticmethod
    def nH_widgetBuilder(node, astTools):
        # Make the frame
        widget = QFrame()
        
        # Open the .ui file created in QtDesigner
        scriptdir=os.path.abspath(os.path.split(sys.modules[test.__module__].__file__)[0])
        uifile = open(os.path.join(scriptdir,'assets','ui','output_filenames.ui'))

        # Load the .ui file
        uic.loadUi(uifile,widget)

        # Close the file
        uifile.close()
        
        # Setup the terminals in the widget
        widget.fptf.setup(node.value.value[2][0].value)
        widget.comboBox.setup(node.value.value[2][1].value)
        
        layer_options = astTools.getLayers()
        widget.comboBox.insertItems(1,layer_options)

        # For now just make an empty dictionary for the log
        terminalsDict = {id(widget.fptf):widget.fptf,
               id(widget.comboBox):widget.comboBox,
              }
        terminalsDict = {}
        

        return widget , terminalsDict


