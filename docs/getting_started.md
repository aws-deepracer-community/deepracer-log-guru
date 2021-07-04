# Getting Started

## Download Logs

DRG works with logs from either the AWS DeepRacer console, or your own independent training if you have moved away from the official console.

You just need to make sure you extract the correct **robomaker** log file and then you can store it wherever you want to organize your log files.

You will probably want to store related log files in the same directory/folder so you can manage and compare them most easily using DRG.

### Download Logs from AWS Console

Download a log file as follows:
* Go to the AWS DeepRacer console and view the training details for a model
* Click the "**Download logs**" button at the top of the training section (note - this button is only enabled once training has completed)

![](pictures/getting_started/download_logs.png)

* After it has downloaded, open the zip archive and locate the single **robomaker** log file in the **logs/training** folder

![](pictures/getting_started/find_correct_log_file.png)

* Extract/save it locally
* Note - DRG does NOT require any other files in the zip archive
* If you wish, repeat this process to download log file(s) for other model(s) too

### Download Logs from DRFC (DeepRacer-For-Cloud)

You may find the following script useful:

    !/bin/bash

    cd $DR_DIR/data/logs
    rm *.log *.zip

    for name in `docker ps --format "{{.Names}}"`; do
            docker logs ${name} >& ${name}.log
    done

    zip robomaker_log deepracer-0_robomaker.1.*.log
    aws s3 cp robomaker_log.zip  s3://$DR_LOGS_COPY_S3_BUCKET/
    
To use this, you will need to set the value of $DR_LOGS_COPY_S3_BUCKET in the system.env configuration file, for example:

    DR_LOGS_COPY_S3_BUCKET=dmh-2021-transfers/logs
    
This script will compress and store the correct log file in an S3 bucket for a **currently-running-training session**

You can then easily download or transfer the log file to wherever you need to perform log analysis.

### Download Logs from Other Sources

Simply transfer or copy **robomaker** log files into a directory/folder that DRG can access.

Make sure you have obtained the correct type of log file which should mostly contain entries like this:

    SIM_TRACE_LOG:0,1,-2.2896,-4.6243,2.7800,0.00,3.80,7,0.0000,False,True,0.1577,0,89.24,35.413,prepare,0.00
    SIM_TRACE_LOG:0,2,-2.2896,-4.6243,2.7823,-2.50,2.50,6,0.1577,False,True,0.1577,0,89.24,35.462,in_progress,0.00
    SIM_TRACE_LOG:0,3,-2.2885,-4.6243,2.7954,-2.50,2.50,6,0.0012,False,True,0.1588,0,89.24,35.526,in_progress,0.00
    SIM_TRACE_LOG:0,4,-2.2817,-4.6236,2.9279,-25.00,0.80,1,0.0077,False,True,0.1665,0,89.24,35.583,in_progress,0.00
    SIM_TRACE_LOG:0,5,-2.2586,-4.6262,1.9827,-10.00,1.80,4,0.0258,False,True,0.1922,1,89.24,35.63,in_progress,0.00
    SIM_TRACE_LOG:0,6,-2.2342,-4.6286,1.1980,-2.50,2.50,6,0.0271,False,True,0.2194,1,89.24,35.703,in_progress,0.00

Also make sure you do NOT delete the information at the start of the log, since this contains the hyperparameters, track name, action space and so on - which are essential for DRG.

## Launch DRG
Run the main DRG application, as per the [Installation Instructions](installation.md#launch-deep-racer-guru)

## Configure DRG
Tell DRG where you have saved your log files using "Switch Directory":

![](pictures/getting_started/file_menu_switch_directory.png)

## Import Log Files
You must then "Import" new log files before you can open them for analysis, using "New File(s)":

![](pictures/getting_started/file_menu_new_files.png)

It will display a list of the new files, if it is correct then click OK to import them into DRG:

![](pictures/getting_started/import_new_log_files.png)


### Open Log Files
Use the "Track" menu to select the correct track - note that tracks with log files are at the top of the list, above the divider
  
![](pictures/getting_started/choose_track.png)

View all imported log files for your selected track using "Open File":

![](pictures/getting_started/file_menu_open_files.png)

Click on the model name to open its log file:

![](pictures/getting_started/choose_file_to_open.png)


