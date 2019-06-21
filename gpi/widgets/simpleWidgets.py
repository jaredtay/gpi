from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel

def simpleWidget(vertical = False):
    widget = QWidget()
    if vertical:
        layout = QVBoxLayout()
    else:
        layout = QHBoxLayout()
    layout.setContentsMargins(0,0,0,0)
    widget.setLayout(layout)
    widget.slot = dummySlot

    return widget, layout

def simpleLabel(content):
    label = QLabel()
    label.setText(content)
    return label

def dummySlot():
    pass
