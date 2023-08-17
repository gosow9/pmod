import sys
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import datetime
from ..config import ConfigHandler
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
        self.handler_fm = ConfigHandler("flag_manager_config.yml")
        self.handler_device = ConfigHandler("config.yml")
        self.cali = self.handler_device.get("cali")
        self.level = self.handler_device.get("level")
        QMainWindow.__init__(self, parent)
        self.set_start_day()
        
                
        
        
        
        #self.start_date = pd.Timestamp(self.handler_fm.get("start_date")["year"],
         #                              self.handler_fm.get("start_date")["month"],
         #                              self.handler_fm.get("start_date")["day"])
        self.data = load_day(self.start_date.year,
                             self.start_date.month,
                             self.start_date.day,
                            "CalL01", 
                            "Level1")

        self.show_dobson_flag = self.handler_fm.get("flags.default_dobson_flag")
        self.show_brewer_flag = self.handler_fm.get("flags.default_brewer_flag")
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

    def set_start_day(self):
        config_value = self.handler_fm.get("start_date")
        if config_value.lower() in ['today', 'current', 'now']:
            # Set the start_date to the current date if the config value is some variant of "today"
            self.start_date = pd.Timestamp(pd.Timestamp.now().date())
        else:
            try:
                # Attempt to retrieve the year, month, and day from the config file
                year = config_value["year"]
                month = config_value["month"]
                day = config_value["day"]
                
                self.start_date = pd.Timestamp(year, month, day)
            except (KeyError, TypeError, ValueError):
                # This block will be executed if there's a KeyError (e.g., "year" not in config_value), 
                # a TypeError (e.g., config_value is not subscriptable), or a ValueError (e.g., invalid date value)
                raise ValueError("Invalid start_date configuration. Please provide a valid year, month, and day or set it to 'today'.")
        
    
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
                            self.cali, 
                            self.level)

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