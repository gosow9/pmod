from .brewer_txt import Brewer
from .dobson_txt import Dobson
import pandas as pd
import os
import glob
import pandas as pd
import matplotlib.dates as mdates

BREWER_PATH = r"\\ad.pmodwrc.ch\\Institute\\Departments\\WRC\\OZONE\\B_Brewer\\DataPostProcessing\\ProcessedData"
DOBSON_PATH = r"\\ad.pmodwrc.ch\\Institute\\Departments\\WRC\\OZONE\\A_Dobsons\\DataPostProcessing\\ProcessedData"

devices = {"Dobson":["051","062","101"], "Brewer":["040","072","156","163"]}


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
    path = BREWER_PATH + n + level + n + device + n + cal + n + str(year) + n + filename
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
            if key == "Dobson":
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
                    
                    
            if key == "Brewer": 
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

            
        
