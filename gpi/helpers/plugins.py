import importlib
import pkgutil

def parse_plugin_widgets():
    """
    Look through the dictionary of plugins.
    Make a list of plugins for regular use.
    Make a list of introductory plugins.
    :param plugins:
    :return widgets , intros:
    """
    # Get the plugins for this package
    plugins = {}
    for finder, name, ispkg in pkgutil.iter_modules():
        if name.startswith('gpi_'):
            # Check for errors in the importing process
            try:
                plugin = importlib.import_module(name)
                plugins[name] =  plugin
            except Exception as err:
                dialogs.genDialog('Plugin Import Error', 'Trace:\n{}'.format(err))
                traceback.print_exc()
                return

    # Make empty lists for the kinds of widgets we expect to see
    widgets = []
    intros = []

    # Get the widgets and intros from each plugin
    for module in plugins:
        widgets.extend(plugins[module].getWidgets())
        intros.extend(plugins[module].getIntros())

    return widgets, intros
