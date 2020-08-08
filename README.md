# deep_racer_guru
Analysis tool for AWS Deep Racer logs

### NEW: Upgrading to Latest Version 1.2.0 / 1.2.1

If you are completely new, then skip this section. Go to "Before You Start"

If you are already using version 1.0.0 or 1.1.0 then **you must upgrade if you want to import log files via the newly-improved AWS DeepRacer console**

* Download additional Python library: *scipy*
* If you did not previously upgrade to version 1.1.0 then follow those instructions too (see below ...)
* Read the "Getting Started" section below for revised instructions how to import log files via the newly-improved AWS DeepRacer console

Note: log files *already downloaded* are compatible with version 1.2.0 i.e. there is no need to download them again


### ARCHIVE: Upgrading to Previous Version 1.1.0

If you are still using version 1.0.0 and wish to upgrade to the improved 1.1.0 or other new releases, then please note the following upgrade instructions:
* Download additional Python libraries: *numpy* and *matplotlib*
* Run the guru tool, and go to the Admin menu and choose "Re-calculate Log Meta"
* It should now work fine, with many new analysis options for you to explore


### Before You Start
Make sure you have the following Python libraries:
* tkinter
* math
* pickle
* json
* os
* numpy
* matplotlib
* scipy

Personalize settings in this file:
* src/configuration/personal_configuration.py

### Getting Started

Run the main guru application class from here:
* src/main/guru.py

You'll first need to download some log files as follows:
* Go to the DeepRacer console and view the training info for a model
* Scroll down to the "Resources" section
* Click the "**Download RoboMaker logs**" button to download the **simulation** log file 
* Save it in your log directory (the one you have configured in your personal_configuration.py file as above)
* If you wish, repeat this process to download log file(s) for other model(s) too 
* In the Deep Racer Guru application, go to the **File -> New** menu option
* It will display a list of the new files, if it is correct then click OK to import them into the Guru

Then, you can open a log file as follows:
* Use the Track menu to select the correct track
* Now go to the **File -> Open** menu to choose from log files you have downloaded for that selected track


