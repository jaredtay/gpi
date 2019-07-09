.. gpi documentation master file, created by
   sphinx-quickstart on Tue Jun 25 13:55:06 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

GPI
===============================

.. toctree::
   :maxdepth: 2

   index
   gpi

Introduction
============

GPI, short for graphical programming interface, is a tool for rapidly generating a GUI based on a python script. GPI uses the abstract syntax tree processor called `redbaron <https://github.com/PyCQA/redbaron>`_ to analyze each line of code and create a graphical interface for editing the code. The package is plugin extensible, making custom widgets available for more specialized treatment of code.

Requirements
============

GPI is designed to work on Windows, Linux, and Macintosh given
the required dependencies.

* redbaron
* PyQt

Installation
============

The following will install both redbaron and gpi.

    python setup.py install

Conda provides some convenient python package managing tools. I recommend using it for install pyqt.

    conda install pyqt

Running GPI
===========

The program can be run simply using the `gpi` command. There is an example in the examples folder that illustrates some default behaviors for common code elements.

Plugins
=======

GPI is easily extended thanks to a plugin architecture. Any modules installed with the `gpi_` prefix will be loaded in, and any widgets definedin the plugins will be injected using the `getWidgets()` and `getIntros()` methods.

An example project that uses and extends GPI is `De-la-mo-v2 <https://git.linux.iastate.edu/NASA-AK/de-la-mo-v2>`_.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`