import sys
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QApplication, QTableWidgetItem,QMainWindow, QVBoxLayout, QWidget, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
import colorsys
import numpy as np


class MplCanvas(FigureCanvas):
    def __init__(self, data=None, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.data = data
        self.preflagged = True
        self.df_dict = {}
        #self.pick_event_occurred = pyqtSignal(bool)
        
        super(MplCanvas, self).__init__(self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.compute_initial_figure()

    def compute_initial_figure(self):
        pass

        

class mplDataFramePlot(MplCanvas):
    def __init__(self, data, parent=None, width=5, height=4, dpi=100):
        super(mplDataFramePlot, self).__init__(data, parent, width, height, dpi)
        self.data = data
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        

        
    def load_dataframe(self, key, df):
        color = next(self.axes._get_lines.prop_cycler)['color']
        d_color = self._darker(color)
        if 'flag' not in df.columns:
            df['flag'] = 0
        

        x = df[df["flag"]==0]["date_num"]
        y = df[df["flag"]==0]["ozone"]
        
        x_flag = df[df["flag"]!=0]["date_num"]
        y_flag = df[df["flag"]!=0]["ozone"]
        
        if self.preflagged:
            x_flag_show = df[df["flag"]!=0]["date_num"]
            y_flag_show = df[df["flag"]!=0]["ozone"]
        else:
            x_flag_show = df[df["flag"]==9]["date_num"]
            y_flag_show = df[df["flag"]==9]["ozone"]
        
        line, = self.axes.plot(x, y, 
                      color=color, 
                      alpha=0.7, 
                      label=key)
        unflagged, = self.axes.plot(x, y, 
                      marker="o", 
                      color=color, 
                      alpha=0.7,
                      picker=True, 
                      pickradius=1)
        flagged, = self.axes.plot(x_flag_show, y_flag_show,
                      marker="x",
                      linestyle='', 
                      color=d_color, 
                      picker=True, 
                      pickradius=1)
        lgd = self.axes.legend()
        self.df_dict[key] = {"key":key, 'df': df, 'line': line, 'unflagged':unflagged, 'flagged':flagged}
        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        self.axes.grid(True)
        

    def compute_initial_figure(self):
        for device, dic in self.data.items():
            self.load_dataframe(device, dic["df"])
            self.axes.set_title(str(dic["year"])+"-"+str(dic["month"])+"-"+str(dic["day"]))
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        
        
    def update_figure(self, data):
        self.axes.clear()
        self.data=data
        del self.df_dict
        self.df_dict = {}
        for device, dic in self.data.items():
            self.load_dataframe(device, dic["df"])
            self.axes.set_title(str(dic["year"])+"-"+str(dic["month"])+"-"+str(dic["day"]))
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.draw()
        
        
    def toggle_figure_preflags(self, preflag):
        self.preflagged = preflag
        self.axes.clear()
        del self.df_dict
        self.df_dict = {}
        for device, dic in self.data.items():
            self.load_dataframe(device, dic["df"])
            self.axes.set_title(str(dic["year"])+"-"+str(dic["month"])+"-"+str(dic["day"]))
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.draw()
        
    
    def update_data_line(self, key):
        df = self.data[key]["df"]
        self.df_dict[key]["df"] = df
        x = df[df["flag"]==0]["date_num"].to_numpy()
        y = df[df["flag"]==0]["ozone"].to_numpy()

        x_flag = df[df["flag"]!=0]["date_num"].to_numpy()
        y_flag = df[df["flag"]!=0]["ozone"].to_numpy()
        

        self.df_dict[key]["line"].set_data(x,y)
        self.df_dict[key]["unflagged"].set_data(x,y)
        self.df_dict[key]["flagged"].set_data(x_flag,y_flag)
        self.fig.canvas.draw()
 
 
    def get_table_obj(self, table, combo, col_nm, save, path):
        self.table = table
        self.combo = combo
        self.column_names = col_nm
        self.save_button = save
        self.path = path
        self.save_button.clicked.connect(self.saveFileDialog)
        
        
    def saveFileDialog(self):
        for device, dic in self.data.items():
                dic["obj"].save(dic["df"], self.path) 
    
        
    def update_table(self, key):
        self.combo.clear()
        keys = self.data.keys()
        self.combo.addItems(keys)
        self.combo.setCurrentText(key)
        df = self.data[key]["df"]
        row_count = len(df)
        self.table.setRowCount(row_count)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(self.column_names)
        for ind, row in df.iterrows():
            self.table.setItem(ind, 0, 
            QTableWidgetItem(f"{row['timestamp'].strftime('%H:%M:%S')}"))
            self.table.setItem(ind, 1, 
            QTableWidgetItem(f"{row['ozone']:.2f}"))
            self.table.setItem(ind, 2,
            QTableWidgetItem(f"{row['flag']:.2f}"))
        
        
    def on_pick(self, event):
        thisline = event.artist
        xdata = thisline.get_xdata()
        ydata = thisline.get_ydata()
        ind = event.ind
        points = tuple(zip(xdata[ind], ydata[ind]))
        key = 0
        for k, v in self.df_dict.items():
            if (v["line"] == thisline) | (v["unflagged"] == thisline)| (v["flagged"] == thisline):
                key = k
        if key == 0:
            return
        mask = (self.data[key]["df"]['date_num'] == xdata[ind][0]) & (self.data[key]["df"]['ozone'] == ydata[ind][0])
        self.data[key]["df"].loc[mask, 'flag'] = self.data[key]["df"].loc[mask, 'flag'].apply(lambda x: 9 if x == 0 else 0)
        self.update_data_line(key)
        self.update_table(key)


    def _darker(self, color, factor=0.9):
        r, g, b = mcolors.to_rgb(color)
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        l *= factor  # make it darker by multiplying the lightness by a factor < 1
        return colorsys.hls_to_rgb(h, l, s)



