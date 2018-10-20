This is an implementation of the maxConnect4 game between 2 players using the Minimax algorithmc with alpha-beta pruning and depth limited search using a heuristic.
Code Structure:
    The code is divided into 3 files:
     a. maxconnect4.py: Handles initialization of MaxConnect4Game.py; reads files and commandline args and controls the mode of the game (interative / one-move)
     b. MaxConnect4Game.py: Contains all the logic for the game including playing the states (for computer i.e. AI), implementing the depth limited alpha-beta minimax version and also calculating all the scores for the players.
     c. constant.py: Contains the constants used in the program.
How to run the program:
    In bash, cd to the directory where the files are located. The file maxconnect4.py should be executed in the terminal to invoke the application.
a. For Interactive mode:
        
    >python maxconnect4.py interactive input1.txt <computer-next/human-next> <depth>
        
In this mode, computer.txt and human.txt are generated which store the output of the move made by respective players and number of player that plays next is saved at the end of the file.
    
b. For one-move mode:
    
    >python maxconnect4.py one-move input1.txt output1.txt <depth>
        
In this mode, output1.txt store the output of the move made by previous player and number of player that plays next is saved at the end of the file.
