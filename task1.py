import sys
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (QHBoxLayout, QLineEdit, QPushButton, QApplication,QMessageBox, QVBoxLayout, QWidget, QLabel)
from PySide2.QtCore import Qt
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np
import re
import pytest
matplotlib.use('Qt5Agg')

replacements = {'^': '**'}
allowed_words = ['x']

def string2func(parent,string):
    ''' takes a string function and returns a function of x '''
    ''' can be expanded to support many mathematical functions (sin,cos,ln,exp,...) or multi variable functions'''
    
    # check if all words are allowed:
    for word in re.findall('[a-zA-Z_]+', string):
        if word not in allowed_words:
            eq="\n Function should look like : 5*x^3 + 2*x"
            QMessageBox.warning(parent, "Invalid Function Syntax", '"{}" is forbidden to use in math expression'.format(word) + eq)
            
    # replace ^ with ** 
    for old, new in replacements.items():
        string = string.replace(old, new)
    # handling y = 1 function
    if string =='1':
        string = "x/x"
    def func(x):
        return eval(string)

    return func


class Canvas(FigureCanvasQTAgg):
    # matplotlib figure
    def __init__(self, parent = None, width = 5, height = 5, dpi = 100):
        
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvasQTAgg.__init__(self, fig)
        self.setParent(parent)
 
    # plotting the graph
    def plot(self,x,y):
        
        ax = self.figure.add_subplot(111)
        ax.clear()

        # handling constant function
        if isinstance(y,float) or isinstance(y,int) :
            ax.axhline(y=y)
        else :
            ax.plot(x,y)

class Window(QWidget):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle("Simple Plotter")
        self.setGeometry(350,100,400,500)
        self.Set_Icon()
        

        # Create widgets
        self.label=QLabel("Please enter a function to be plotted",self)
        
        self.input_equation = QLineEdit(self)
        self.input_equation.setAlignment(Qt.AlignCenter)
        
        self.label1=QLabel("Enter plotting interval")
        self.label2=QLabel("From:")
        self.label3=QLabel("To:")
        
        self.input_min = QLineEdit(self)
        self.input_max = QLineEdit(self)

        self.button = QPushButton("Plot",self)
        self.canvas = Canvas(self, width=8, height=4)
       
        # Layout
        self.Set_Layout()
        
        # Add button signal to greetings slot
        self.button.clicked.connect(self.Plot)

    def Set_Icon(self):
        icon =QIcon("mm1.png")
        self.setWindowIcon(icon)

    def Set_Layout(self):

        layout_row=QHBoxLayout()
        layout_row.addWidget(self.label2)
        layout_row.addWidget(self.input_min)
        layout_row.addWidget(self.label3)
        layout_row.addWidget(self.input_max)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_equation)
        layout.addWidget(self.label1)

        layout.addLayout(layout_row)
        
        layout.addWidget(self.button)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    # trigerred function when button is pressed
    def Plot(self):

        if self.input_equation.text() =="":
            QMessageBox.warning(self, "Function Error", "Please enter a function")
            return
        
        try:
            a = float(self.input_min.text())
            b = float(self.input_max.text())
        except:
            QMessageBox.warning(self, "Limits", "Please enter proper limits")
        if a>b :
            QMessageBox.warning(self, "Limits", "Please enter proper limits")
        
        # generating plotted points
        x = np.linspace(a, b)
        func = string2func(self,self.input_equation.text())
        self.canvas.plot(x,func(x))
        self.canvas.draw()

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Window()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())