# Installation Instructions

## Install Python
Download and install [Python 3.9.4](https://www.python.org/downloads/release/python-394/)

If you change the install options, be sure you still install pip and tkinter:
[](pictures/Python Install Correct Options.png)

Download additional packages by running this command in the directory where you just installed Python:

    python -m pip install matplotlib==3.3.3 numpy==1.19.3 scipy==1.6.0
    
<< screenshot goes here >>

https://github.com/dmh23/deep_racer_guru/releases
( download and unzip )

create a two line batch script (e.g. .".bat" if using windows):
    cd C:\Users\david\PycharmProjects\deep_racer_guru
    "C:\Program Files (x86)\Python\3.9.1\python.exe" -m src.main.guru
( the directory should be the one containing the "src" folder etc. )



### Upgrade Instructions From Old Versions

* Run DRG, and go to the Admin menu and choose "Re-calculate Log Meta"
