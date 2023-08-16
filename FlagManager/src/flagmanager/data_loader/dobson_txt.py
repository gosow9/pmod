from pathlib import PurePosixPath
from typing import Any, Dict
from ..config import ConfigHandler
import pandas as pd
import numpy as np
import os
import re
import matplotlib.dates as mdates

handler = ConfigHandler()
default_header = handler.get("dobson.header")


class Dobson:
    """``ImageDataSet`` loads / save dobson datafile from a given filepath as 'pandas' dataframe.

    Example:
    ::

        >>> DobsonData(filepath='/img/file/path.101')
    """

    def __init__(self, filepath: str, header: list = default_header):
        """Creates a new instance of Dobson to load / save df data at the given filepath.

        Args:
            filepath: The location of the image file to load / save data.
            header: The overwrite the standart colum names in the dobson file when dataset being saved and loaded.
            version: The version of the dataset being saved and loaded.
        """
        self.colums = header
        self.file_name = os.path.basename(filepath)
        self.filepath = filepath
        self.df = self._load()
        self._get_header()


    def _load(self) -> pd.DataFrame:
        """Loads data from the text file.

        Returns:
            Data from the text file as a pandas df.
        """
        
        df = pd.read_csv(self.filepath, 
                           index_col = False, 
                           header = None,
                           delim_whitespace = True,
                           skiprows = 1,
                           names = self.colums)
        
        df = df.replace('/', np.NaN)   
        df["iii"] = df["iii"].astype(str).str.zfill(3)
        df["timeA"] = df["timeA"].astype(str).str.zfill(6)
        df["timeD"] = df["timeD"].astype(str).str.zfill(6)
        df["timeC"] = df["timeC"].astype(str).str.zfill(6)
        df["yyyymmdd"] = df["yyyymmdd"].astype(str)
        df["timestamp"] = pd.to_datetime(df["yyyymmdd"] + df["timeC"],
                                         format='%Y%m%d%H%M%S')
        df["date_num"] = mdates.date2num(df['timestamp'])
        df["ozone"] = df['OzAD'].astype(float)
        df["flag"] = df['flag1'] + df['flag2'] + df['flag3']
        df["OzA"] = df["OzA"].astype(float)
        df["OzC"] = df["OzC"].astype(float)
        df["OzD"] = df["OzD"].astype(float)
        df["OzAD"] = df["OzAD"].astype(float)
        df["OzCD"] = df["OzCD"].astype(float)
        df["OzAC"] = df["OzAC"].astype(float)
        return df
    
    def get_df(self)-> pd.DataFrame:
        return self.df
    
    def _get_header(self)->str:
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as file:
                self.header_str = file.readline().strip()
                
    def save(self, df, year, name, dir_path, level, cali):
        df.loc[df['flag'] == 0, ['flag1', 'flag2', 'flag3']] = 0
        df.loc[df['flag'] == 9, ['flag1', 'flag2', 'flag3']] = 9
        file_path = os.path.join(dir_path,
                                 level, 
                                 name,
                                 cali, 
                                 year,
                                 self.file_name)
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(file_path, 'w') as f:
            s = re.sub(r'CalL\d+', cali, self.header_str)
            f.write(" "+s+"\n")
            for row in df.itertuples():
                line = (
                f" {row.iii:<3} {row.t:^1}  {row.yyyymmdd:^8}  {row.ss:^2}  {row.tt:^2}  "
                f"{row.timeC:^6} {row.rvalC:>6.2f} {row.sdevC:>7.4f}  {row.timeD:>6} "
                f"{row.rvalD:>6.2f} {row.sdevD:>7.4f}  {row.timeA:>6} {row.rvalA:>6.2f} "
                f"{row.sdevA:>7.4f}  {row.flag1:^1} {row.flag2:^1} {row.flag3:^1} "
                f"{row.muC:>6.3f} {row.muD:>6.3f} {row.muA:>6.3f} {row.OzC:>6.1f} "
                f"{row.OzD:>6.1f} {row.OzA:>6.1f} {row.OzAD:>6.1f} {row.OzCD:>6.1f} "
                f"{row.OzAC:>6.1f}"
                )

                f.write(line + "\n")
        
                
        
            
        
if __name__ == "__main__":
    test1 = r"\\ad.pmodwrc.ch\Institute\Departments\WRC\OZONE\B_Brewer\DataPostProcessing\ProcessedData\Level1\040\CalL01\2023\DS18323.040"
    df = Dobson(test1)
    print(df.df)

    
    
