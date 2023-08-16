from .brewer_txt import Brewer
from .dobson_txt import Dobson
from ..config import ConfigHandler
import pandas as pd
import os
import glob
import pandas as pd
import matplotlib.dates as mdates

handler = ConfigHandler()
BREWER_PATH = handler.get("brewer.path")
BREWER_KEY = handler.get("brewer.key")
if not os.path.exists(BREWER_PATH):
            raise FileNotFoundError(f"Path not found: {BREWER_PATH}")
        
DOBSON_PATH = handler.get("dobson.path")
if not os.path.exists(DOBSON_PATH):
            raise FileNotFoundError(f"Path not found: {DOBSON_PATH}")
DOBSON_KEY = handler.get("dobson.key")


devices = {DOBSON_KEY : handler.get("dobson.devices"),
           BREWER_KEY : handler.get("brewer.devices")}


def get_files_of_type(start_folder, file_extension):
    """
    Get all files of a specific type in a folder and all its subfolders.

    :param start_folder: The folder in which to start the search.
    :param file_extension: The desired file extension.
    :return: A list of file paths.
    """
    files = []
    for dirpath, dirnames, filenames in os.walk(start_folder):
        for filename in filenames:
            if filename.endswith(file_extension):
                file = os.path.join(dirpath, filename)
                files.append(file)

    return files

def create_brewer_path(year, month, day, device, level, cal):
    n = r"\\"
    filename = "DS" + str(pd.Timestamp(year=year,month=month,day=day).dayofyear)+str(year%100)+"."+ device
    path = os.path.join(BREWER_PATH, level, device, cal, str(year), filename)
    if os.path.exists(path):
        return path 
    else:
        return False
    
    
def create_dobson_path(year, month, day, device, level, cal):
    n = r"\\"
    filename = "AE" + str(year)+str(month).zfill(2)+str(day).zfill(2)+"."+ device
    path = DOBSON_PATH + n + level + n + device + n + cal + n + str(year) + n + filename
    if os.path.exists(path):
        return path 
    else:
        return False


def load_day(year, month, day, cal, level, devices=devices):
    dataframes = {}
    for key, val in devices.items():
        for device in val:
            if key == DOBSON_KEY:
                path = create_dobson_path(year,month,day,device,level,cal)
                if path:
                    dfs = Dobson(path)
                    dataframes[key+"_"+device]= {"df":dfs.df, 
                                                 "header": dfs.header_str,
                                                 "path":path, 
                                                 "day":day, 
                                                 "month":month, 
                                                 "year":year,
                                                 "obj": dfs}
                    
                    
            if key == BREWER_KEY: 
                path = create_brewer_path(year,month,day,device,level,cal)
                if path:
                    dfs = Brewer(path)
                    dataframes[key+"_"+device]= {"df":dfs.df, 
                                                 "header":dfs.header_dict,
                                                 "path":path, 
                                                 "day":day, 
                                                 "month":month, 
                                                 "year":year,
                                                 "obj":dfs}
                    
    return dataframes

            
        
