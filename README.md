# Ozone Measurement Data Analysis
This project focuses on processing and analyzing ozone measurement data taken in Davos using various Dobson and Brewer devices. Our aim is to transform raw data from text files into a structured MariaDB, filter out noise, and identify outliers both automatically and manually.

## Overview
1. **Data Collection:** Measurements are recorded in text files from multiple devices.
2. **Database Creation:** Raw data from text files are ingested into a MariaDB.
3. **Data Cleaning:** Noise and irrelevant data points are filtered out.
4. **Auto-flagging Outliers:** A script is used to automatically identify and flag potential outliers in the data.
5. **Manual Outlier Flagging:** A Python QT GUI allows users to visually inspect the data and manually flag or correct outliers.

## Features
- **Database Structure:** Designed for easy querying and data analysis.
- **Auto-flagging Script:** Automated preliminary outlier detection.
- **GUI Tool:** Visually inspect, correct, or flag data points using an intuitive interface.

## Setup and Installation
### Prerequisites:

- MariaDB
- Python 3.x
- Required Python libraries: `pandas`, `qt`, etc. 

1. **Database Setup:**

    - Start MariaDB server.
    - Create the necessary tables and schemas as per the DB structure.

2. **Python Environment Setup:**

    - Clone the repository: git clone [repo_link](https://github.com/gosow9/pmod.git).
    - Navigate to the project directory.
    - Install the required packages: pip install -r requirements.txt.

3. **Starting the GUI Tool:**

    - Run the command: python gui_tool.py.
  
## Usage
1. **Data Ingestion:**
   - Run the data ingestion script to populate the MariaDB with raw data from the text files.

2. **Auto-flagging:**

   - Run the autoflag script: python autoflag_script.py.
3. **Manual Flagging:**

    - Start the GUI tool.
    - Load the dataset you want to inspect.
    - Manually flag or correct outliers using the provided tools.
    - Save flagged data points.

## Contributing
We welcome contributions! If you find any bugs or have suggestions, please open an issue. If you'd like to contribute directly, please fork the repository, make your changes, and open a pull request.

## License
[Specify License Here, e.g., MIT, GPL, etc.]