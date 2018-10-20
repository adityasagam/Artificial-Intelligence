#!/usr/bin/env 

import sys
from MaxConnect4Game import *

def oneMoveGame(currentGame):
    if currentGame.pieceCount == 42:    # Is the board full already?
        print 'BOARD FULL\n\nGame Over!\n'
        sys.exit(0)

    currentGame.aiPlay()

    print 'Game state after move:'
    currentGame.printGameBoard()

    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    currentGame.printGameBoardToFile(currentGame.switchPlayer(currentGame.currentTurn))
    currentGame.gameFile.close()


def interactiveGame(currentGame, isCompNext):
    '''
    if currentGame.pieceCount == 42:    # Is the board full already?
        print 'BOARD FULL\n\nGame Over!\n'
        sys.exit(0)
    '''
    humanPlayer = currentGame.switchPlayer(currentGame.currentTurn)
    while currentGame.pieceCount < 42:
        # Computers move
        if isCompNext:
            currentGame.aiPlay();
            print 'Game state after computers move:'
            currentGame.printGameBoard()
            
            currentGame.gameFile = open("computer.txt","w+")
            
            currentGame.printGameBoardToFile(humanPlayer)
            currentGame.gameFile.close()
            
            currentGame.countScore()
            print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
            
            if currentGame.pieceCount == 42:
                break;
            
        # Humans move
        isValid = None
        while not isValid:
            humanChoice = input('Make a move human...\nHint: Enter a column number starting from 0\n')
            isValid = currentGame.playPiece(humanChoice, humanPlayer)
            if not isValid:
                print '\nInvalid move ...'
        
        print 'Game state after humans move:'
        currentGame.printGameBoard()
        
        currentGame.gameFile = open("human.txt","w+")
        currentGame.printGameBoardToFile(currentGame.currentTurn)
        currentGame.gameFile.close()
        
        currentGame.countScore()
        print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
        isCompNext = True
        
        
    print 'BOARD FULL\n\nGame Over!\n'
    sys.exit(0)

def main(argv):
    # Make sure we have enough command-line arguments
    if len(argv) != 5:
        print 'Four command-line arguments are needed:'
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)

    game_mode, inFile = argv[1:3]
    

    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)

    currentGame = maxConnect4Game() # Create a game

    # Try to open the input file
    try:
        currentGame.gameFile = open(inFile, 'r')
    except IOError:
        print("\nError opening input file with given name.")
        print("Creating file with empty board state (same file name)...")
        currentGame.gameFile = open(inFile, 'w+')
        emptyBoard = [[0 for row in range(0,7)] for col in range(0,6)]
        for row in emptyBoard:
            currentGame.gameFile.write(''.join(str(col) for col in row) + '\r\n')
        currentGame.gameFile.write('1\r\n')
        currentGame.gameFile.close()
        currentGame.gameFile = open(inFile, 'r')
        
    # Read the initial game state from the file and save in a 2D list
    file_lines = currentGame.gameFile.readlines()
    
    # read game board ie form beginning to second last line (last line is the player)
    currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]   
    currentGame.currentTurn = int(file_lines[-1][0])
    currentGame.gameFile.close()
    currentGame.depthLimit = int(argv[4])
    
    #print '\nDepth is :' +  str(currentGame.depthLimit)
    print '\nMaxConnect-4 game\n'
    print 'Game state before move:'
    currentGame.printGameBoard()

    # Update a few game variables based on initial state and print the score
    currentGame.checkPieceCount()
    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))
    '''
    res = currentGame.calScore(currentGame.gameBoard)
    print('Score new: Player 1 = %d, Player 2 = %d\n' % (res[0], res[1]))
    '''
    if game_mode == 'interactive':
        nextPlayer = str.lower(argv[3])
        if not nextPlayer == 'computer-next' and not nextPlayer == 'human-next':
            sys.exit('\nPlease select computer-next or human-next for the next player parameter as mentioned!')
        
        if nextPlayer == 'computer-next':
            isCompNext = True
        else:
            isCompNext = False
            
        if not isCompNext:
            currentGame.currentTurn = currentGame.switchPlayer(currentGame.currentTurn)
        interactiveGame(currentGame, isCompNext) # Be sure to pass whatever else you need from the command line
    else: # game_mode == 'one-move'
        # Set up the output file
        outFile = argv[3]
        try:
            currentGame.gameFile = open(outFile, 'w')
        except:
            sys.exit('Error opening output file.')
        oneMoveGame(currentGame) # Be sure to pass any other arguments from the command line you might need.


if __name__ == '__main__':
    main(sys.argv)


