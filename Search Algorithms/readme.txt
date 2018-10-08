Name: Aditya Shantilal Sagam
UTA ID: 1001660179
Programming Language Used: Python (2.4.3)

Code Structure:
1. The code is divided into 3 files:
	a. find_route.py (main module)
	b. Edge.py (class)
	c. State.py (class)
2. Code has been modularized into different methods used for reading files, searching for the destination and writing the output.
3. Two methods for search have been implemented:
	1. Uninformed Search - Uniform Cost Search
	2. Informed Search - A* Search

Instructions to run the code:
1. Open the linux terminal and cd to the parent folder.
2. Once inside the directory, execute the python code with arguments as follows:
	a. Uninformed search
		> python find_route.py find_route uninf <filename>.txt <Source> <Destination>
		eg: > python find_route.py uninf input1.txt Bremen Saarbruecken
	b. Informed Search
		> python find_route.py find_route inf <filename>.txt <Source> <Destination> <heuristics filename>.txt
		eg: > python find_route.py inf input.txt Bremen London h_kassel.txt
	For each of the files included in command line args, if the files reside in some other directory as from where the terminal points, then the path of the file must be included with the file name.
		eg. for input1.txt stored in a different folder use its full address as follows:
		> python find_route.py find_route uninf /home/a/as/ass0179/Fall_2018/input1.txt Munich Kassel
