# deep_racer_guru

## Introduction

Deep Racer Guru (DRG) is a graphical analysis tool for AWS Deep Racer logs.

Its main purpose is to provide "out-of-the-box" analysis that can run locally on your own computer.

You don't have to write Python code. Simply download logs from the AWS Deep Racer console, and then use a GUI to see how your models are performing.

![](./sample_pictures/Collage.png)

## Installation Notes

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

## Getting Started

### Download Logs
You'll first need to download some log files as follows:
* Go to the DeepRacer console and view the training info for a model
* Click the "**Download logs**" button below the training graph 
* Open the zip archive and locate the **robomaker** log file in the **logs/training** folder
![](./sample_pictures/find_correct_log_file.png)
* Extract/save it locally
* If you wish, repeat this process to download log file(s) for other model(s) too

### Configure DRG
Tell DRG where you have saved your log files by editing:
* src/configuration/personal_configuration.py
![](./sample_pictures/personal_config_file.png)

### Run DRG
Run the main guru application class from here:
* src/main/guru.py
![](./sample_pictures/how_to_run.png)

### Import Log Files
You must "Import" new log files before you can open them for analysis:
* In the Deep Racer Guru application, go to the **File -> New** menu option
* It will display a list of the new files, if it is correct then click OK to import them into DRG

### Open Log Files
* Use the Track menu to select the correct track
* Now go to the **File -> Open** menu to choose from log files you have downloaded for that selected track


## Archive - Upgrade Instructions for Older Versions

### Upgrading to Previous Version 1.2.0 / 1.2.1

If you are completely new, then skip this section. Go to "Before You Start"

If you are already using version 1.0.0 or 1.1.0 then **you must upgrade if you want to import log files via the newly-improved AWS DeepRacer console**

* Download additional Python library: *scipy*
* If you did not previously upgrade to version 1.1.0 then follow those instructions too (see below ...)
* Read the "Getting Started" section below for revised instructions how to import log files via the newly-improved AWS DeepRacer console

Note: log files *already downloaded* are compatible with version 1.2.0 i.e. there is no need to download them again


### Upgrading to Previous Version 1.1.0

If you are still using version 1.0.0 and wish to upgrade to the improved 1.1.0 or other new releases, then please note the following upgrade instructions:
* Download additional Python libraries: *numpy* and *matplotlib*
* Run the guru tool, and go to the Admin menu and choose "Re-calculate Log Meta"
* It should now work fine, with many new analysis options for you to explore







