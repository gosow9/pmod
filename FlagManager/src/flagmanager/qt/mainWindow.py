from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from ..mpl.mpl_Widget import  mplDataFramePlot
from PySide6.QtCore import Qt, Slot, QDate
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, 
                               QHeaderView, QLabel, QMainWindow, QSlider,
                               QTableWidget, QTableWidgetItem, QVBoxLayout,
                               QWidget, QCalendarWidget, QCheckBox,QPushButton)



def init(self):
    menubar(self)
    calendar(self)
    table(self)
    saveButton(self)
    checkbox(self)
    figure(self)
    layout(self)


def menubar(self):
    # Main menu bar
    self.menu = self.menuBar()
    self.menu_file = self.menu.addMenu("File")
    exit = QAction("Exit", self, triggered=qApp.quit)
    self.menu_file.addAction(exit)    
    
    
def calendar(self):
    self.calendar = QCalendarWidget()
    self.calendar.setMinimumDate(QDate(2018, 1, 1))
    self.calendar.setMaximumDate(QDate(2023, 1, 1))
    self.calendar.setGridVisible(True)
    self.calendar.setSelectedDate(QDate(self.start_date.year,
                             self.start_date.month,
                             self.start_date.day))
    
    
def figure(self):
    self.fig = Figure(figsize=(5, 3))
    self.canvas = mplDataFramePlot(self.data, parent=None, width=5, height=4, dpi=100)
    self.canvas.get_table_obj(self.table, 
                              self.combo, 
                              self.column_names, 
                              self.save_button,
                              self.save_path)
    self.toolbar = NavigationToolbar(self.canvas, self)
    
def saveButton(self):
    self.save_button = QPushButton("Save")



               
    
def checkbox(self):
    self.show_pre_flagged = QCheckBox('Show preflagged data', self)
    self.show_pre_flagged.setChecked(True)
    self.show_brewer_checkbox = QCheckBox('Show Brewer devices', self)
    self.show_brewer_checkbox.setChecked(True)
    self.show_dobson_checkbox = QCheckBox('Show Dobson devices', self)
    self.show_dobson_checkbox.setChecked(True)
    


def table(self):
        self.table = QTableWidget()
        self.column_names = ["Timestamp hour:min:sec", "Measured Ozone", "Flag"]
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.combo = QComboBox()
        keys = self.data.keys()
        first = next(iter(self.data))
        self.combo.addItems(keys)
        set_table_config(self, self.data[first]["df"])
      
        
def update_table(self):
    keys = self.data.keys()
    first = next(iter(self.data))
    self.combo.clear()
    self.combo.addItems(keys)
    set_table_config(self, self.data[first]["df"])
    
    
def update_datapoint_table(self, key, point=None):
    keys = self.data.keys()
    self.combo.clear()
    self.combo.addItems(keys)
    set_table_config(self, self.data[key]["df"])
    
 
def set_table_config(self, df):
    row_count = len(df)
    self.table.setRowCount(row_count)
    self.table.setColumnCount(3)
    self.table.setHorizontalHeaderLabels(self.column_names)
    set_table_data(self, df)
    

def set_table_data(self, df):
    for ind, row in df.iterrows():
            self.table.setItem(ind, 0, 
            QTableWidgetItem(f"{row['timestamp'].strftime('%H:%M:%S')}"))
            self.table.setItem(ind, 1, 
            QTableWidgetItem(f"{row['ozone']:.2f}"))
            self.table.setItem(ind, 2,
            QTableWidgetItem(f"{row['flag']:.2f}"))       


def layout(self):
     # Right layout
    rlayout = QVBoxLayout()
    rlayout.setContentsMargins(1, 1, 1, 1)
    rlayout.addWidget(self.calendar)
    rlayout.addWidget(QLabel("Device:"))
    rlayout.addWidget(self.combo)
    rlayout.addWidget(self.table)
    rlayout.addWidget(self.save_button)

    # Left layout
    llayout = QVBoxLayout()
    sub = QHBoxLayout()
    sub.addWidget(self.show_brewer_checkbox)
    sub.addWidget(self.show_dobson_checkbox)
    sub.addWidget(self.show_pre_flagged)
    llayout.addLayout(sub)
    rlayout.setContentsMargins(1, 1, 1, 1)
    llayout.addWidget(self.toolbar)
    llayout.addWidget(self.canvas, 88)
    
    
    # Main layout
    layout = QHBoxLayout(self._main)
    layout.addLayout(llayout, 60)
    layout.addLayout(rlayout, 40)