import sys
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import datetime

from .mainWindow import init, set_table_config, update_table
#from .plot import (set_canvas, plot_dataframes, set_table_config, 
#                        set_table_data)

from ..data_loader.brewer_txt import Brewer
from ..data_loader.dobson_txt import Dobson
from ..data_loader.load import load_day


from PySide6.QtCore import Qt, Slot, QDate
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget)



class ApplicationWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.start_date = pd.Timestamp(2020,10,3)
        self.data = load_day(self.start_date.year,
                             self.start_date.month,
                             self.start_date.day,
                            "CalL01", 
                            "Level1")
        self.save_path = "C:\\Users\\cedric.renda\\Documents"
        self.show_dobson_flag = True
        self.show_brewer_flag = True
        self.setWindowTitle('Flag Manager')
        

        # Central widget
        self._main = QWidget()
        self.setCentralWidget(self._main)
        
        init(self)
        
        
        # Signal and Slots connections
        self.combo.currentTextChanged.connect(self.combo_option)
        self.calendar.clicked.connect(self.calender_changed)
        self.show_pre_flagged.stateChanged.connect(self.show_preflagged_data)
        self.show_brewer_checkbox.stateChanged.connect(self.show_brewer)
        self.show_dobson_checkbox.stateChanged.connect(self.show_dobson)


        
    
    @Slot()
    def combo_option(self, text):
        if text in self.data:
            set_table_config(self, self.data[text]["df"])

    
    @Slot()
    def calender_changed(self, text):
        date = self.calendar.selectedDate().toPython()
        #date = datetime.datetime.strptime(date, "%Y-%m-%d")

        year, month, day = date.year, date.month, date.day
        self.data = load_day(year,
                            month, 
                            day, 
                            "CalL01", 
                            "Level1")
        if self.show_brewer_flag == False:
            new_dict = {k: v for k, v in self.data.items() if not k.startswith('Brewer')}
            self.data = new_dict
        if self.show_dobson_flag == False:
            new_dict = {k: v for k, v in self.data.items() if not k.startswith('Dobson')}
            self.data = new_dict
        self.canvas.update_figure(self.data)
        update_table(self)
        
        
    @Slot()
    def show_preflagged_data(self, state):
        if state == 2:
            self.canvas.toggle_figure_preflags(True)
        else:
            self.canvas.toggle_figure_preflags(False) 

        
    @Slot()
    def show_dobson(self, state):
        if state == 2:
            self.show_dobson_flag = True
            self.update_day()
        else:
            self.show_dobson_flag = False
            self.update_day()
            
    
    @Slot()
    def show_brewer(self, state):
        if state == 2:
            self.show_brewer_flag = True
            self.update_day()
        else:
            self.show_brewer_flag = False
            self.update_day()
        
        
    def update_day(self):
        date = self.calendar.selectedDate().toPython()
        #date = datetime.datetime.strptime(date, "%Y-%m-%d")
        year, month, day = date.year, date.month, date.day
        self.data = load_day(year,
                            month, 
                            day, 
                            "CalL01", 
                            "Level1")
        if self.show_brewer_flag == False:
            new_dict = {k: v for k, v in self.data.items() if not k.startswith('Brewer')}
            self.data = new_dict
        if self.show_dobson_flag == False:
            new_dict = {k: v for k, v in self.data.items() if not k.startswith('Dobson')}
            self.data = new_dict
        self.canvas.update_figure(self.data)
        update_table(self)
        
        





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ApplicationWindow()
    #w.setFixedSize(1280, 720)
    w.resize(1280, 720)
    w.show()
    app.exec()