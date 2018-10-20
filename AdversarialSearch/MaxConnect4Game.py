#!/usr/bin/env python

# Written by Chris Conly based on C++
# code provided by Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

import copy
import random
import constant
import sys

class maxConnect4Game:
    
    def __init__(self):
        self.gameBoard = [[0 for i in range(7)] for j in range(6)]
        self.currentTurn = 1
        self.player1Score = 0
        self.player2Score = 0
        self.pieceCount = 0
        self.gameFile = None
        self.depthLimit = None
        self.currDepth = 0
        random.seed()

    # Count the number of pieces already played
    def checkPieceCount(self):
        self.pieceCount = self.getPieceCount(self.gameBoard) #sum(1 for row in self.gameBoard for piece in row if piece)
    
    def getPieceCount(self, state):
        return sum(1 for row in state for piece in row if piece)
    
    # Output current game status to console
    def printGameBoard(self):
        print ' -----------------'
        for i in range(6):
            print ' |',
            for j in range(7):
                print('%d' % self.gameBoard[i][j]),
            print '| '
        print ' -----------------'
    
    
    # Output a particular state to console
    def printGameState(self, state):
        print ' -----------------'
        for i in range(6):
            print ' |',
            for j in range(7):
                print('%d' % state[i][j]),
            print '| '
        print ' -----------------'
    
    
    # Output current game status to file
    def printGameBoardToFile(self, nextPlayer):
        for row in self.gameBoard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r\n')
        self.gameFile.write('%s\r\n' % str(nextPlayer))

    # Place the current player's piece in the requested column
    def playPiece(self, column, player):
        if not self.gameBoard[0][column]:       # check if the column is full
            for i in range(5, -1, -1):          # check for an empty location from bottom
                if not self.gameBoard[i][column]:
                    self.gameBoard[i][column] = player
                    self.pieceCount += 1
                    return 1
    
    def alphaBeta_Minimax(self, state, currentTurn):
        best = None
        val = constant.MIN
        alpha = constant.MIN
        beta = constant.MAX
        
        for action, nextState in self.successor(state, currentTurn).items():
            t = self.minVal(nextState, self.switchPlayer(currentTurn), alpha, beta)
            if t > val:
                val = t
                best = action  
        
        return best
    
    def minVal(self, state, currentTurn, alpha, beta):         
        if self.isTerminal(state):
            return self.getUtility(state, False)
        if self.isDepthReached():
            return self.getUtility(state, True)
        else:
            val = constant.MAX
            #print 'max val:' + str(val)
            
            for action, nextState in self.successor(state, currentTurn).items():
                #print '\n for move:' + str(action)
                #self.printGameState(nextState)
                
                valMax = self.maxVal(nextState, self.switchPlayer(currentTurn), alpha, beta)
                val = min( val, valMax)
                if val <= alpha:
                    return val
                beta = min(beta, val)
            return val
        
    def maxVal(self, state, currentTurn, alpha, beta):        
        if self.isTerminal(state):
            return self.getUtility(state, False)
        if self.isDepthReached():
            #print '\nReturn Eval'
            return self.getUtility(state, True)
        else:
            val = constant.MIN
            #print 'min val:' + str(val)
            
            for action, nextState in self.successor(state, currentTurn).items():
                #print '\n for move:' + str(action)
                #self.printGameState(state)
                valMin = self.minVal(nextState, self.switchPlayer(currentTurn), alpha, beta)
                val = max(val, valMin)
                if val >= beta:
                    return val
                alpha = max(alpha, val)
            return val
    
    def isDepthReached(self):
        #print '\nCur Depth: ' + str( self.currDepth ) + '<= Limit: ' + str(self.depthLimit )
        #print ' is ' +  str(self.currDepth <= self.depthLimit)
        
        if self.currDepth <= self.depthLimit:
            return False
        #print '\nDepth reached'
        return True
        
    def getUtility(self, state, isCalcEval):
        result = self.calcScore(state, isCalcEval)
        
        if self.currentTurn == 1:
            return result[0] - result[1]
        return result[1] - result[0]
        
    def isTerminal(self, state):
        if self.getPieceCount(state) == 42:
            #print '\nTerminal State'
            return True
        else:
            #print '\nNon Terminal State'
            return False
            
    def switchPlayer(self, currentPlayer):
        if currentPlayer == 2:
            return 1
        else:
            return 2
        
    # The AI section. Currently plays randomly.
    def aiPlay(self):        
        row, col = self.alphaBeta_Minimax(self.gameBoard, self.currentTurn)
        self.gameBoard[row][col] = self.currentTurn
        self.pieceCount += 1
        #self.currentTurn = self.switchPlayer(self.currentTurn)
        
    # generates array of Action_States (wrapper for action and successor states)
    def successor(self, currentState, currentTurn):
        self.currDepth += 1
        listNextStates = {}
        
        for col in range(0,7):
            newState = None
            actionRow = None
            actionCol = None
            
            for row in range(5,-1,-1):
                if currentState[row][col] == 0:
                    newState = copy.deepcopy(currentState)
                    newState[row][col] = currentTurn
                    actionRow = row
                    actionCol = col
                    break;
                    
            if newState:                
                #print '\naction:'+str((actionRow, actionCol))+'\n'
                #self.printGameState(newState);
                listNextStates[(actionRow, actionCol)] = newState
            
        return listNextStates
    
    '''
        @description - Calculate the number of 4-in-a-row each player has
        @param       - current state
        @return      - array with element 1 as player-1 score, element 2 as player-2 score
    '''
    def calcScore(self, state, isCalcEval):
        player1Score = 0
        player2Score = 0
        
        # Check horizontally
        for row in state:
            
            # calculate eval
            if isCalcEval:
                # check player 1
                player1Score += self.getEvalScore(row[0:4], 1)
                player1Score += self.getEvalScore(row[1:5], 1)
                player1Score += self.getEvalScore(row[2:6], 1)
                player1Score += self.getEvalScore(row[3:7], 1)
                
                # check player 2
                player2Score += self.getEvalScore(row[0:4], 2)
                player2Score += self.getEvalScore(row[1:5], 2)
                player2Score += self.getEvalScore(row[2:6], 2)
                player2Score += self.getEvalScore(row[3:7], 2)
               
            # Calculate Utility
            # Check player 1
            if row[0:4] == [1]*4:
                player1Score += 1
            if row[1:5] == [1]*4:
                player1Score += 1
            if row[2:6] == [1]*4:
                player1Score += 1
            if row[3:7] == [1]*4:
                player1Score += 1
            # Check player 2
            if row[0:4] == [2]*4:
                player2Score += 1
            if row[1:5] == [2]*4:
                player2Score += 1
            if row[2:6] == [2]*4:
                player2Score += 1
            if row[3:7] == [2]*4:
                player2Score += 1

        # Check vertically
        for j in range(7):
        
            # Calculate eval
            if isCalcEval:
                # Check player 1
                # starting row 0
                subArr = [ state[0][j],  state[1][j], state[2][j], state[3][j]]
                player1Score += self.getEvalScore(subArr, 1)
                
                # starting row 1
                subArr = [ state[1][j],  state[2][j], state[3][j], state[4][j]]
                player1Score += self.getEvalScore(subArr, 1)
                # starting row 2
                subArr = [ state[2][j],  state[3][j], state[4][j], state[5][j]]
                player1Score += self.getEvalScore(subArr, 1)
                    
                # Check player 2
                # Starting row 0
                subArr = [ state[0][j],  state[1][j], state[2][j], state[3][j]]
                player2Score += self.getEvalScore(subArr, 2)
                # Starting row 1
                subArr = [ state[1][j],  state[2][j], state[3][j], state[4][j]]
                player2Score += self.getEvalScore(subArr, 2)
                # Starting row 2
                subArr = [ state[2][j],  state[3][j], state[4][j], state[5][j]]
                player2Score += self.getEvalScore(subArr, 2)
            
            # Calculate Utility
            # Check player 1
            if (state[0][j] == 1 and state[1][j] == 1 and
                   state[2][j] == 1 and state[3][j] == 1):
                player1Score += 1
            if (state[1][j] == 1 and state[2][j] == 1 and
                   state[3][j] == 1 and state[4][j] == 1):
                player1Score += 1
            if (state[2][j] == 1 and state[3][j] == 1 and
                   state[4][j] == 1 and state[5][j] == 1):
                player1Score += 1
            # Check player 2
            if (state[0][j] == 2 and state[1][j] == 2 and
                   state[2][j] == 2 and state[3][j] == 2):
                player2Score += 1
            if (state[1][j] == 2 and state[2][j] == 2 and
                   state[3][j] == 2 and state[4][j] == 2):
                player2Score += 1
            if (state[2][j] == 2 and state[3][j] == 2 and
                   state[4][j] == 2 and state[5][j] == 2):
                player2Score += 1

        # Check diagonally
        # Calculate Eval
        if isCalcEval:
            # Check player 1
            subArr = [state[2][0], state[3][1], state[4][2], state[5][3]]
            player1Score += self.getEvalScore(subArr, 1)
            
            subArr = [state[1][0], state[2][1], state[3][2], state[4][3]]
            player1Score += self.getEvalScore(subArr, 1)
            
            subArr = [state[2][1], state[3][2], state[4][3], state[5][4]]
            player1Score += self.getEvalScore(subArr, 1)
            
            subArr = [state[0][0], state[1][1], state[2][2], state[3][3]]
            player1Score += self.getEvalScore(subArr, 1)
            
            subArr = [state[1][1], state[2][2], state[3][3], state[4][4]]
            player1Score += self.getEvalScore(subArr, 1)
            
            subArr = [state[2][2], state[3][3], state[4][4], state[5][5]]
            player1Score += self.getEvalScore(subArr, 1)
            
            subArr = [state[0][1], state[1][2], state[2][3], state[3][4]]
            player1Score += self.getEvalScore(subArr, 1)
            
            subArr = [state[1][2], state[2][3], state[3][4], state[2][5]]
            player1Score += self.getEvalScore(subArr, 1)
            
            subArr = [state[2][3], state[3][4], state[4][5], state[5][6]]
            player1Score += self.getEvalScore(subArr, 1)
            
            subArr = [state[0][2], state[1][3], state[2][4], state[3][5]]
            player1Score += self.getEvalScore(subArr, 1)
            
            subArr = [state[1][3], state[2][4], state[3][5], state[4][6]]
            player1Score += self.getEvalScore(subArr, 1)
            
            subArr = [state[0][3], state[1][4], state[2][5], state[3][6]]
            player1Score += self.getEvalScore(subArr, 1)
            
            subArr = [state[0][3], state[1][2], state[2][1], state[3][0]]
            player1Score += self.getEvalScore(subArr, 1)
            
            subArr = [state[0][4], state[1][3], state[2][2], state[3][1]]
            player1Score += self.getEvalScore(subArr, 1)
            
            subArr = [state[1][3], state[2][2], state[3][1], state[4][0]]
            player1Score += self.getEvalScore(subArr, 1)
            
            subArr = [state[0][5], state[1][4], state[2][3], state[3][2]]
            player1Score += self.getEvalScore(subArr, 1)
            
            subArr = [state[1][3], state[2][3], state[3][2], state[4][1]]
            player1Score += self.getEvalScore(subArr, 1)
            
            subArr = [state[2][3], state[3][2], state[4][1], state[5][0]]
            player1Score += self.getEvalScore(subArr, 1)
            
            subArr = [state[0][6], state[1][5], state[2][4], state[3][3]]
            player1Score += self.getEvalScore(subArr, 1)
            
            subArr = [state[1][5], state[2][4], state[3][3], state[4][2]]
            player1Score += self.getEvalScore(subArr, 1)
            
            subArr = [state[2][4], state[3][3], state[4][2], state[5][1]]
            player1Score += self.getEvalScore(subArr, 1)
            
            subArr = [state[1][6], state[2][5], state[3][4], state[4][3]]
            player1Score += self.getEvalScore(subArr, 1)
            
            subArr = [state[2][5], state[3][4], state[4][3], state[5][2]]
            player1Score += self.getEvalScore(subArr, 1)
            
            subArr = [state[2][6], state[3][5], state[4][4], state[5][3]]
            player1Score += self.getEvalScore(subArr, 1)
            
            #  Check player 2
            subArr = [state[2][0], state[3][1], state[4][2], state[5][3]]
            player2Score += self.getEvalScore(subArr, 2)
            
            subArr = [state[1][0], state[2][1], state[3][2], state[4][3]]
            player2Score += self.getEvalScore(subArr, 2)
            
            subArr = [state[2][1], state[3][2], state[4][3], state[5][4]]
            player2Score += self.getEvalScore(subArr, 2)
            
            subArr = [state[0][0], state[1][1], state[2][2], state[3][3]]
            player2Score += self.getEvalScore(subArr, 2)
            
            subArr = [state[1][1], state[2][2], state[3][3], state[4][4]]
            player2Score += self.getEvalScore(subArr, 2)
            
            subArr = [state[2][2], state[3][3], state[4][4], state[5][5]]
            player2Score += self.getEvalScore(subArr, 2)
            
            subArr = [state[0][1], state[1][2], state[2][3], state[3][4]]
            player2Score += self.getEvalScore(subArr, 2)
            
            subArr = [state[1][2], state[2][3], state[3][4], state[2][5]]
            player2Score += self.getEvalScore(subArr, 2)
            
            subArr = [state[2][3], state[3][4], state[4][5], state[5][6]]
            player2Score += self.getEvalScore(subArr, 2)
            
            subArr = [state[0][2], state[1][3], state[2][4], state[3][5]]
            player2Score += self.getEvalScore(subArr, 2)
            
            subArr = [state[1][3], state[2][4], state[3][5], state[4][6]]
            player2Score += self.getEvalScore(subArr, 2)
            
            subArr = [state[0][3], state[1][4], state[2][5], state[3][6]]
            player2Score += self.getEvalScore(subArr, 2)
            
            subArr = [state[0][3], state[1][2], state[2][1], state[3][0]]
            player2Score += self.getEvalScore(subArr, 2)
            
            subArr = [state[0][4], state[1][3], state[2][2], state[3][1]]
            player2Score += self.getEvalScore(subArr, 2)
            
            subArr = [state[1][3], state[2][2], state[3][1], state[4][0]]
            player2Score += self.getEvalScore(subArr, 2)
            
            subArr = [state[0][5], state[1][4], state[2][3], state[3][2]]
            player2Score += self.getEvalScore(subArr, 2)
            
            subArr = [state[1][3], state[2][3], state[3][2], state[4][1]]
            player2Score += self.getEvalScore(subArr, 2)
            
            subArr = [state[2][3], state[3][2], state[4][1], state[5][0]]
            player2Score += self.getEvalScore(subArr, 2)
            
            subArr = [state[0][6], state[1][5], state[2][4], state[3][3]]
            player2Score += self.getEvalScore(subArr, 2)
            
            subArr = [state[1][5], state[2][4], state[3][3], state[4][2]]
            player2Score += self.getEvalScore(subArr, 2)
            
            subArr = [state[2][4], state[3][3], state[4][2], state[5][1]]
            player2Score += self.getEvalScore(subArr, 2)
            
            subArr = [state[1][6], state[2][5], state[3][4], state[4][3]]
            player2Score += self.getEvalScore(subArr, 2)
            
            subArr = [state[2][5], state[3][4], state[4][3], state[5][2]]
            player2Score += self.getEvalScore(subArr, 2)
            
            subArr = [state[2][6], state[3][5], state[4][4], state[5][3]]
            player2Score += self.getEvalScore(subArr, 2)
                
        # Check player 1
        if (state[2][0] == 1 and state[3][1] == 1 and
               state[4][2] == 1 and state[5][3] == 1):
            player1Score += 1
        if (state[1][0] == 1 and state[2][1] == 1 and
               state[3][2] == 1 and state[4][3] == 1):
            player1Score += 1
        if (state[2][1] == 1 and state[3][2] == 1 and
               state[4][3] == 1 and state[5][4] == 1):
            player1Score += 1
        if (state[0][0] == 1 and state[1][1] == 1 and
               state[2][2] == 1 and state[3][3] == 1):
            player1Score += 1
        if (state[1][1] == 1 and state[2][2] == 1 and
               state[3][3] == 1 and state[4][4] == 1):
            player1Score += 1
        if (state[2][2] == 1 and state[3][3] == 1 and
               state[4][4] == 1 and state[5][5] == 1):
            player1Score += 1
        if (state[0][1] == 1 and state[1][2] == 1 and
               state[2][3] == 1 and state[3][4] == 1):
            player1Score += 1
        if (state[1][2] == 1 and state[2][3] == 1 and
               state[3][4] == 1 and state[4][5] == 1):
            player1Score += 1
        if (state[2][3] == 1 and state[3][4] == 1 and
               state[4][5] == 1 and state[5][6] == 1):
            player1Score += 1
        if (state[0][2] == 1 and state[1][3] == 1 and
               state[2][4] == 1 and state[3][5] == 1):
            player1Score += 1
        if (state[1][3] == 1 and state[2][4] == 1 and
               state[3][5] == 1 and state[4][6] == 1):
            player1Score += 1
        if (state[0][3] == 1 and state[1][4] == 1 and
               state[2][5] == 1 and state[3][6] == 1):
            player1Score += 1

        if (state[0][3] == 1 and state[1][2] == 1 and
               state[2][1] == 1 and state[3][0] == 1):
            player1Score += 1
        if (state[0][4] == 1 and state[1][3] == 1 and
               state[2][2] == 1 and state[3][1] == 1):
            player1Score += 1
        if (state[1][3] == 1 and state[2][2] == 1 and
               state[3][1] == 1 and state[4][0] == 1):
            player1Score += 1
        if (state[0][5] == 1 and state[1][4] == 1 and
               state[2][3] == 1 and state[3][2] == 1):
            player1Score += 1
        if (state[1][4] == 1 and state[2][3] == 1 and
               state[3][2] == 1 and state[4][1] == 1):
            player1Score += 1
        if (state[2][3] == 1 and state[3][2] == 1 and
               state[4][1] == 1 and state[5][0] == 1):
            player1Score += 1
        if (state[0][6] == 1 and state[1][5] == 1 and
               state[2][4] == 1 and state[3][3] == 1):
            player1Score += 1
        if (state[1][5] == 1 and state[2][4] == 1 and
               state[3][3] == 1 and state[4][2] == 1):
            player1Score += 1
        if (state[2][4] == 1 and state[3][3] == 1 and
               state[4][2] == 1 and state[5][1] == 1):
            player1Score += 1
        if (state[1][6] == 1 and state[2][5] == 1 and
               state[3][4] == 1 and state[4][3] == 1):
            player1Score += 1
        if (state[2][5] == 1 and state[3][4] == 1 and
               state[4][3] == 1 and state[5][2] == 1):
            player1Score += 1
        if (state[2][6] == 1 and state[3][5] == 1 and
               state[4][4] == 1 and state[5][3] == 1):
            player1Score += 1

        # Check player 2
        if (state[2][0] == 2 and state[3][1] == 2 and
               state[4][2] == 2 and state[5][3] == 2):
            player2Score += 1
        if (state[1][0] == 2 and state[2][1] == 2 and
               state[3][2] == 2 and state[4][3] == 2):
            player2Score += 1
        if (state[2][1] == 2 and state[3][2] == 2 and
               state[4][3] == 2 and state[5][4] == 2):
            player2Score += 1
        if (state[0][0] == 2 and state[1][1] == 2 and
               state[2][2] == 2 and state[3][3] == 2):
            player2Score += 1
        if (state[1][1] == 2 and state[2][2] == 2 and
               state[3][3] == 2 and state[4][4] == 2):
            player2Score += 1
        if (state[2][2] == 2 and state[3][3] == 2 and
               state[4][4] == 2 and state[5][5] == 2):
            player2Score += 1
        if (state[0][1] == 2 and state[1][2] == 2 and
               state[2][3] == 2 and state[3][4] == 2):
            player2Score += 1
        if (state[1][2] == 2 and state[2][3] == 2 and
               state[3][4] == 2 and state[4][5] == 2):
            player2Score += 1
        if (state[2][3] == 2 and state[3][4] == 2 and
               state[4][5] == 2 and state[5][6] == 2):
            player2Score += 1
        if (state[0][2] == 2 and state[1][3] == 2 and
               state[2][4] == 2 and state[3][5] == 2):
            player2Score += 1
        if (state[1][3] == 2 and state[2][4] == 2 and
               state[3][5] == 2 and state[4][6] == 2):
            player2Score += 1
        if (state[0][3] == 2 and state[1][4] == 2 and
               state[2][5] == 2 and state[3][6] == 2):
            player2Score += 1

        if (state[0][3] == 2 and state[1][2] == 2 and
               state[2][1] == 2 and state[3][0] == 2):
            player2Score += 1
        if (state[0][4] == 2 and state[1][3] == 2 and
               state[2][2] == 2 and state[3][1] == 2):
            player2Score += 1
        if (state[1][3] == 2 and state[2][2] == 2 and
               state[3][1] == 2 and state[4][0] == 2):
            player2Score += 1
        if (state[0][5] == 2 and state[1][4] == 2 and
               state[2][3] == 2 and state[3][2] == 2):
            player2Score += 1
        if (state[1][4] == 2 and state[2][3] == 2 and
               state[3][2] == 2 and state[4][1] == 2):
            player2Score += 1
        if (state[2][3] == 2 and state[3][2] == 2 and
               state[4][1] == 2 and state[5][0] == 2):
            player2Score += 1
        if (state[0][6] == 2 and state[1][5] == 2 and
               state[2][4] == 2 and state[3][3] == 2):
            player2Score += 1
        if (state[1][5] == 2 and state[2][4] == 2 and
               state[3][3] == 2 and state[4][2] == 2):
            player2Score += 1
        if (state[2][4] == 2 and state[3][3] == 2 and
               state[4][2] == 2 and state[5][1] == 2):
            player2Score += 1
        if (state[1][6] == 2 and state[2][5] == 2 and
               state[3][4] == 2 and state[4][3] == 2):
            player2Score += 1
        if (state[2][5] == 2 and state[3][4] == 2 and
               state[4][3] == 2 and state[5][2] == 2):
            player2Score += 1
        if (state[2][6] == 2 and state[3][5] == 2 and
               state[4][4] == 2 and state[5][3] == 2):
            player2Score += 1
        
        return [player1Score, player2Score]
    
    def getEvalScore(self, arr, player):
        evalScore = 0
        if self.isCombinationExist(arr, 0, 3, player, 1):
            evalScore += constant.ONE_PIECE_EVAL
        if self.isCombinationExist(arr, 0, 2, player, 2):
            evalScore += constant.TWO_PIECE_EVAL
        if self.isCombinationExist(arr, 0, 1, player, 3):
            evalScore += constant.THREE_PIECE_EVAL
        return evalScore
        
    def isCombinationExist(self, arr, num1, num1Count, num2, num2Count):
        if (arr.count(num1) == num1Count and arr.count(num2) == num2Count):
            return True
        return False
        
    # Calculate the number of 4-in-a-row each player has
    def countScore(self):
        result = self.calcScore(self.gameBoard, False)
        self.player1Score = result[0];
        self.player2Score = result[1];
