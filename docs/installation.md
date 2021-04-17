# Installation Instructions

Download and install [Python 3.9.4](https://www.python.org/downloads/release/python-394/)

Download additional packages by running this command in the directory where you just installed Python:

    python -m pip install matplotlib==3.3.3 numpy==1.19.3 scipy==1.6.0
    
<< screenshot goes here >>

https://github.com/dmh23/deep_racer_guru/releases
( download and unzip )

create a two line batch script (e.g. .".bat" if using windows):
    cd C:\Users\david\PycharmProjects\deep_racer_guru
    "C:\Program Files (x86)\Python\3.9.1\python.exe" -m src.main.guru
( the directory should be the one containing the "src" folder etc. )


## Installation Notes   ***OLD

DRG is written entirely in Python 3. It "should" work with any recent 3.x.x version of Python (I currently use version 3.8.3)

You will also need to install the following standard libraries using "pip":
* tkinter
* math
* pickle
* json
* os
* numpy
* matplotlib
* scipy

### Upgrade Instructions From Old Versions

If upgrading from **1.2.0** or **1.2.1**
* Edit src/configuration/personal_configuration.py which will be overwritten when you download the new version (see "Configure DRG", below)

If upgrading from **1.1.0**
* The list of required libraries has changed, see "Installation Notes" above
* Edit src/configuration/personal_configuration.py which will be overwritten when you download the new version (see "Configure DRG", below)

If upgrading from **1.0.0**
* The list of required libraries has changed, see "Installation Notes" above
* Edit src/configuration/personal_configuration.py which will be overwritten when you download the new version (see "Configure DRG", below)
* Run DRG, and go to the Admin menu and choose "Re-calculate Log Meta"
