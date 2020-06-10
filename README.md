# deep_racer_guru
Analysis tool for AWS Deep Racer logs


### Before You Start
Make sure you have the following Python libraries:
* tkinter
* boto3
* math
* pickle
* json
* os
* traceback

Setup an AWS *shared credentials file*, as per:
* https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#shared-credentials-file

Personalize settings in this file:
* src/configuration/personal_configuration.py

### Getting Started

Run the main guru application class from here:
* src/main/guru.py

You'll first need to download some log files as follows:
* Go to the DeepRacer console and view the training info for a model
* Click on the "view logs" link for the **simulation job** (beware - NOT the "training job")
* Open the log file in CloudWatch so you can copy the full name of the log stream, something like this:
`sim-gqnx0h0j34zh/2020-06-10T10-55-49.817Z_766c44e1-c008-4255-8cc3-f8a1ed4adbba/SimulationApplicationLogs`
* In the Deep Racer Guru application, go to the File -> Fetch menu option
* Paste the full log file name into the first text entry box (the cursor will be ready and waiting for you)
* Click OK / press RETURN
* Wait a short while (large logs might take a couple of minutes)

If that worked, you can open a log file as follows:
* Use the Track menu to select the correct track
* Now go to the File -> Open menu to choose from log files you have downloaded for that selected track


