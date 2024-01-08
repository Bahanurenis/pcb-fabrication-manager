# PCB-Fabrication-Manager (PFM)

PFM is multifunctional tool to help you update your csv files according to your configuration to send your PCB assembler. PFM aims to save you boring csv and manual changing operations. 

PFM needs 3 things: 
- Path of the cofiguration YAML file
- Path of the input CSV file 
- Path of the output CSV (wherever you want to save with  [name].csv) - this is only necessary for pfm command line tool.



##  Configuration File Rules: 
 - Extension should be .yaml or .yml 
 - Should start with headers: 
 - for the column: 


## Usage: 
You can use PFM with two way: 
### PFM command line tool: 
You can use the PFM with your terminal, follow the below steps!
 - Clone the repo and run the below command to create pip package
 - Install the all dependencies with 
	``` pip install .```

** ! Installing the dev dependencies and creating a virtual environment is strongly recommended **

- Install the pfm app with: 
		``` pip install -e .```

```
Usage: pfm [OPTIONS] INPUTFILE OUTPUTFILE

Options:
  --config FILE
  --help         Show this message and exit.
```

pfm needs 3 arguments with below order: 
- config.yaml (name can be different, but the extension should be yaml)
example usage: 
pfm [--config (PATH_OF_YOUR_CONFIG_YAML)] (PATH_OF_YOUR_INPUT_CSV) (PATH_OF_YOUR_OUTPUT_CSV) 

 ```
 pfm -- config /home/ubuntu/projects/pcb-fabrication-manager/input.csv  /home/ubuntu/projects/pcb-fabrication-manager/input.csv /home/ubuntu/projects/config/output1.csv 
```

**NOTE THAT:** -- config is a option but if you don't give any config.yaml file, pfm will try to use the config.yaml from the repo. This feature will be implement later. For now, please give your config.yaml path.

### PFM with GitHub Actions:
You can use pfm while creating a new issue on [[pcb-fabrication-manager](https://github.com/Bahanurenis/pcb-fabrication-manager) ]without downloading the repo.

How: 
* Go to the [issue](https://github.com/Bahanurenis/pcb-fabrication-manager/issues/new/choose) 
* Choose the PFM CSV Update Template and get started: 
*  Template:
```

	    ** Please add your config file as a txt file after this line, you will see e.g."[config.txt] (url)" 

	** Please add your input.csv file after this line, you will see e.g. "[input.csv] (url)" 
```
* Attach your config file with .txt extension (GitHub accepts only specific files e.g. .jpeg, txt, csv).  
* Attach your input csv file 
* Submit new issue. 
 Or created a new issue with a pfm label and your config and input file. 
 
 When you submit  the issue  "Pfm Github" workflow will be triggered. 
 - If your issue has a pfm label, Pfm Github will delete the issue immediately to protect your data. 
 - When Pfm Github is finished, you will receive a notification according to your System Actions settings . To change your settings you can go to [Notifications](https://github.com/settings/notifications) . 
	 - If the workflow is failed, please check the logs. 
	 - If the workflow is finished successfully, you will see your output.csv in the artifact as [your-login-name]-output.

    
**!!!PLEASE NOTE THAT: PFM will keep the logs and artifact only ONE day to protect your data. After one day the logs and the artifact will be expired.**

## Configuration:
```
 # config yaml file should dave headers title 
headers:
# name: name of the column you want to change
# required: False as default, if this column is required,
#set this field to True. Pfm will search and if it can't find the column name you will be notified.
# mapping-name: the new name for the column.
#If mapping-name is empty or "" or doesn't exist in the list, pfm will use the name. So if you will use the same name don't worry at all.  
  -
    name:
    required:
    mapping-name:
# config yaml file should have the rows title. 
rows:
# Key: name of the value that you want to change.
# If you want to change a value with a new value you can give a simply your row value: "new value" e.g.(Top Layer = "T").
# Pfm will search this value in the csv and will replace all findings with the new value.
# if you dont't have any you don't need to give any things under the rows: 
 - Key: "Value"
```
