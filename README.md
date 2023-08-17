# Ozone Measurement Data Analysis
This project focuses on processing and analyzing ozone measurement data taken in Davos using various Dobson and Brewer devices. Our aim is to have a tool to visualize the datapoints with their respective flags an change the flag when clicked on. 

## Overview
1. **Data Collection:** Measurements are recorded in text files from multiple devices.
2. **Manual Outlier Flagging:** A Python QT GUI allows users to visually inspect the data and manually flag or correct outliers.
3. **Saving data** into same folder structure as supplied

## Future developement
- **Database Structure:** Designed for easy querying and data analysis.
- **Auto-flagging Script:** Automated preliminary outlier detection.


## Setup and Installation

1. **Python Environment Setup:**

    - Clone the repository: git clone [repo_link](https://github.com/gosow9/pmod.git).
    - Navigate to the project directory.
    - Install the required packages: pip install -r requirements.txt.

Here a way to do it in git bash and anaconda:
```bash
git clone https://github.com/gosow9/pmod.git
```
after cloning the repo we change directory in and setup our python environment. On Windows install and use the anaconda powershell to create a new envionment
```bash
conda create -n <YOUR-ENV-NAME>
conda activate <YOUR-ENV-NAME>
conda install pip 
```
once pip is installed we can install the other packages
```bash
pip install -r requirements.txt
```
2. **Change config file:**
To run the programm we need to change the save defined in the config.yml file. Here we need to change both saving paths to the destiantion we want to use.

3. **Starting the GUI Tool:**

    - change to the Flagmanager/src directory and run 

```bash
python main.py
```

### Prerequisites:
- Python 3.x
- Required Python libraries: requirements.txt file


## Contributing
We welcome contributions! If you find any bugs or have suggestions, please open an issue. If you'd like to contribute directly, please fork the repository, make your changes, and open a pull request.

## License
[MIT](LICENSE)