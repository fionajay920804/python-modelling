Requirement:
•	Platform: MacOS, Linux, Windows
•	Packages requirement: tkinter, numpy, network, pandas, matplotlib, pygraphviz
•	Environment: python3
I strongly recommend running this program on MacOS. 
This is because in a Windows environment, 
it is difficult to install all of the above packages,
which also require many dependencies. 
In addition, I wrote this program in the MacOS environment. 
I recommend running this program by using the command line in terminal since many IDEs do not work well with packages.
•	Step1: cd to the folder where the program is stored

•	Step2: run the gen_network_demo.py

•	Step3: select the configuration file(config.txt)

•	Step4: set the names of file, which are the graphs of this program

•	Step5: check all the output files in the folder


For Monte Carlo simulation:
First: you can use the file which the stage1 generate or can generate the new file by running prepare_data file.

•	Step1: cd to the folder where the program is stored

•	Step2: run the mcmc.py

•	Step3: select the configuration file(config.txt)

•	Step4: select the observed outbreak file(.CSV)

•	Step5: input the parameter you want to infer. choose from q, g and symp_prob_threshold. You can input one or more parameters which separated by spaces

•	Step6: input the simulation times

•	Step7: save the picture of distribution of parameter