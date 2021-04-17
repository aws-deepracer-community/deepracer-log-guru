


Trial Link to other documentation:
[Terminology](docs/terminology.md)



# deep_racer_guru

## Introduction

Deep Racer Guru (DRG) is an interactive detailed analysis tool for AWS Deep Racer logs.

Its main purpose is to provide "out-of-the-box" analysis that can run locally on your own computer.

You don't have to write Python code. Simply download logs from the AWS Deep Racer console, and then use a GUI to see how your models are performing.

![Analyze DeepRacer logs easily with DRG](./sample_pictures/Collage.png)



## Getting Started

### Download Logs
You'll first need to download some log files as follows:
* Go to the DeepRacer console and view the training info for a model
* Click the "**Download logs**" button at the top of the training section 
* Open the zip archive and locate the **robomaker** log file in the **logs/training** folder

![](./sample_pictures/find_correct_log_file.png)

* Extract/save it locally
* If you wish, repeat this process to download log file(s) for other model(s) too

### Configure DRG
Tell DRG where you have saved your log files by editing:
* src/configuration/personal_configuration.py

![](./sample_pictures/personal_config_file.png)

### Run DRG
Run the main DRG application class from here:
* src/main/guru.py

![](./sample_pictures/how_to_run.png)

### Import Log Files
You must "Import" new log files before you can open them for analysis:
* In the Deep Racer Guru application, go to the **File -> New** menu option
* It will display a list of the new files, if it is correct then click OK to import them into DRG

### Open Log Files
* Use the Track menu to select the correct track
* Now go to the **File -> Open** menu to choose from log files you have downloaded for that selected track







