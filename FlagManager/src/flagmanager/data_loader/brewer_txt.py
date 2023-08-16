import os
import re
import pprint
import pandas as pd
import numpy as np
import matplotlib.dates as mdates
from ..config import ConfigHandler
from typing import Any, Dict
from datetime import datetime
from collections import deque
from pathlib import PurePosixPath

handler = ConfigHandler()
default_header = handler.get("brewer.header")




class Brewer:
    def __init__(self,  filepath: str, names: list = default_header):
        self.names = names
        self.filepath = filepath
        self.file_name = os.path.basename(filepath)
        self._load()

    
    def _load(self):
        self.file_lines = self._get_file()
        self.header_lines, self.header_len = self._get_header_lines()
        self.full_header = self._get_full_header_str(self.header_len)
        self.header_str = self._get_header_str()
        self.data, self.data_len = self._get_data_lines()
        self.footer_lines, self.footer_len = self._get_footer_lines()
        self.footer_str = self._get_footer_str()
        self.header_dict = self._extract_header_dict()
        self.df = self._get_data_frame()
        del(self.file_lines)

    
    def _get_file(self):
        with open(self.filepath, 'r') as file:
            lines = file.read().split('\n')
            return lines
        
        
    def _get_header_lines(self):
        nr = 0
        for line in self.file_lines:
            if re.search("Type", line):
                #print(f"Stop condition met: {line}")
                break
            nr += 1
        #print("Number of header lines:",nr)
        return self.file_lines[:nr-1], nr
    
    
    def _get_header_str(self):
        header = "".join(self.header_lines)
        return header
    
    def _get_full_header_str(self, nr):
        return self.file_lines[:nr+2]
    
    
    def _get_footer_lines(self):
        footer_start = self.header_len + 2 + self.data_len
        footer = self.file_lines[footer_start:]
        return footer, len(footer)
    
    
    def _get_footer_str(self):
        header = "".join(self.footer_lines)
        return header
    
    
    def _get_data_lines(self):
        nr = 0
        data = []
        for line in self.file_lines[self.header_len+2:]:
            if line.strip() == '': 
                break
            data.append(line)
            nr += 1
        #print("Number of data lines:",nr)
        return data, nr

    def _get_data_frame(self):
        df = pd.DataFrame([re.split(r'\s{2,}', row) for row in self.data],columns=self.names)
        date = self.header_dict["Measurements date"]
        df = df.replace('/', np.NaN)
        df['timestamp'] = pd.to_datetime(df['Time(UTC)'], format='%H:%M:%S').apply(lambda dt: dt.replace(year=date.year, month=date.month, day=date.day))
        df["date_num"] = mdates.date2num(df['timestamp'])
        df["ozone"] = df['Ozone'].astype(float)
        df["Ozone"] = df['Ozone'].astype(float)
        df["flag"] = df['Flag'].astype(int)
        df["Temp"] = df['Temp'].astype(int)
        df["Airmass"] = df['Airmass'].astype(float)
        df["Ozone_error"] = df["Ozone_error"].astype(float)
        df["SO2"] = df["SO2"].astype(float)
        df["SO2_error"] = df["SO2_error"].astype(float)
        

        return df
    
    def save(self, df, dir_path):
        file_path = os.path.join(dir_path,self.file_name)
        with open(file_path, 'w') as f:
            for l in self.full_header:
                f.write(l+"\n")
            for ind, row in df.iterrows():
                line = (
                f"{row['Type']}  {row['Time(UTC)']}   {row['Temp']:>2}   {row['Airmass']:>6.3f}  {row['Ozone']:>8.1f}  "
                f"{row['Ozone_error']:>6.1f}  {row['SO2']:>6.1f}  {row['SO2_error']:>6.1f}     {row['flag']:^1}"
                )

                f.write(line + "\n")
            for l in self.footer_lines:
                f.write(l+"\n")



    def _extract_header_dict(self)-> dict:
        try:
            date = re.search(r'for ([A-Z]+\s\d+\/\d+)', self.header_str).group(1)
        except AttributeError:
            print("Error: No match found for 'Date' in header lines")   
            date = None
        
        try:
            location = re.search(r'at ([\w_]+)', self.header_str).group(1)
        except AttributeError:
            print("Error: No match found for 'location' in header lines")   
            location = None
        
        try:
            instrument = re.search(r'instrument # ([\d\s]+)', self.header_str).group(1).strip()
        except AttributeError:
            print("Error: No match found for 'instrument' in header lines")   
            instrument = None
        
        try:  
            latitude = float(re.search(r'Latitude\s*=\s*([\d\.]+)', self.header_str).group(1))
        except AttributeError:
            print("Error: No match found for 'latitude' in header lines")
            latitude = None
        
        try:  
            longitude = float(re.search(r'Longitude\s*=\s*([\d\.]+)', self.header_str).group(1))
        except AttributeError:
            print("Error: No match found for 'Longitude' in header lines")
            longitude = None
        
        try:  
            version = re.search(r'Version: ([\d\.\s:]+)', self.header_str).group(1).strip()
        except AttributeError:
            print("Error: No match found for 'version' in header lines")
            version = None
            
        try:  
            etc = [float(val) for val in re.search(r'ETC Values\s*\(O3/SO2\)\s*=\s*([\d\s\/]+)', self.header_str).group(1).split('/')]
        except AttributeError:
            print("Error: No match found for 'ETC values' in header lines")
            etc = None
            
        try:  
            absorption = [float(val) for val in re.search(r'O3 Absorption \(O3/SO2\) =  ([\d\.\s\/]+)', self.header_str).group(1).split('/')]
        except AttributeError:
            print("Error: No match found for 'absorption' in header lines")
            absorption = None

        dict_values = {
            'Measurements date': datetime.strptime(date, '%b %d/%y'),
            'Location': location,
            'Instrument': instrument,
            'Latitude': latitude,
            'Longitude': longitude,
            'Version': version,
            'ETC Values (O3/S02)': etc,
            'O3 Absorption (O3/S02)': absorption
        }
        return dict_values
    
    
    def print_header(self):
        print(self.header_str)
        
    def get_header(self):
        return self.header_lines
    
    def get_footer(self):
        return self.footer_lines
    
    
    def print_meta_data(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.header_dict)
        
    def get_df(self):
        return self.df
        
        
            
        
if __name__ == "__main__":
    test1 = r"\\ad.pmodwrc.ch\Institute\Departments\WRC\OZONE\B_Brewer\DataPostProcessing\ProcessedData\Level1\040\CalL01\2023\DS18323.040"
    test2 = r"\\ad.pmodwrc.ch\Institute\Departments\WRC\OZONE\B_Brewer\DataPostProcessing\ProcessedData\Level1\072\CalL01\2023\DS00123.072"
    out = r"C:\Users\cedric.renda\Documents\FlagManager\flagmanager\tests\data_loader\myfile.txt"
    
    
    df1 = Brewer(test1)
    df2 = Brewer(test2)
    print(df1.get_footer())
    print(df1.get_header())
    df1.print_meta_data()
    print(df2.get_footer())
    print(df2.get_header())
    df2.print_meta_data()

    
    
