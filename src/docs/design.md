## Problem Description:

User is designing PCB, at the end he/she will export a csv file. User will send this csv file to PCB assembly company and the company wants specific csv format. User is updating BOM and CPL csv files manually, and the request is to make this automated.

User Scenario about CPL csv file:

```
Altium Designer Pick and Place Locations

========================================================================================================================
File Design Information:

Date:       05/12/23
Time:       00:08
Revision:  xyz
Variant:    No variations
Units used: mm

"Designator","Layer","Center-X(mm)","Center-Y(mm)","Rotation"
```
csv 1.1: Altium CPL csv file with columns name


```
"Designator","Layer","Mid X","Mid Y","Rotation"
```
csv 1.2: Assembly company format

The first description part should be ignored/deleted and the column's name should be change
```
"Designator" -> "Designator"
"Layer" -> "Layer"
"Center-X(mm)" -> "Mid X"
"Center-Y(mm)" -> "Mid Y"
"Rotatin" -> "Rotation"
```

User scenario about BOM(Bill of Metarials) csv file:
- This scenario will be about validation
```
Altium example of BOM:
Line #,Comment,Description,Designator,Quantity,JLCPCB Part #,Footprint
```
[The company wants to have the below fields](https://jlcpcb.com/help/article/45-bill-of-materials-for-pcb-assembly):
```
(Comment),(Designator),[JLCPCB PartOptional] #,(Footprint)
```
pcb-fabrication-manager should validate the exported csv should have () parts, if one of them is missing the should let the user know.

## Design Ideas:
pcb-fabrication-manager: pfm
- 5.12.2023:
	- According to the problem description, pfm will have two functionality
		1. CSV update
		2. CSV validation

	* Design should be generic. The assembly company can be changed, or can change the required field's name. pfm should be able to handle this situation.
	 So pfm will now the column's name, because it will be specific for the Altium. But it will take  the new values as an argument from the user.
		 - Problem1: This can be a hassle for the user. pfm should make the process automated and easy for the user.
			 * Option1: User will provide a <config.yaml>, <input.csv>, and <output_file_name>, pfm will define the rules for yaml file of course. And it will parse the yaml file and map with the input.csv at the end it will give <output_file_name>.csv
				 * In this scenario, pfm will be created as an command line tool.
				 * User will use pfm with option and argument(bom/cpl) and parameters

	* Future ideas:
		[] milestone1: pfm will be implemented as command line tool, also the repo can provide the usage with GitHub workflow. When workflow is finished the repo will send the csv file or notification via email. And the issue will be closed after.
