#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name:        logical_expression
# Purpose:     Contains logical_expression class, inference engine,
#              and assorted functions
#
# Created:     09/25/2011
# Last Edited: 07/22/2013  
# Notes:       *This contains code ported by Christopher Conly from C++ code
#               provided by Dr. Vassilis Athitsos
#              *Several integer and string variables are put into lists. This is
#               to make them mutable so each recursive call to a function can
#               alter the same variable instead of a copy. Python won't let us
#               pass the address of the variables, so put it in a list which is
#               passed by reference. We can also now pass just one variable in
#               the class and the function will modify the class instead of a
#               copy of that variable. So, be sure to pass the entire list to a
#               function (i.e. if we have an instance of logical_expression
#               called le, we'd call foo(le.symbol,...). If foo needs to modify
#               le.symbol, it will need to index it (i.e. le.symbol[0]) so that
#               the change will persist.
#              *Written to be Python 2.4 compliant for omega.uta.edu
#-------------------------------------------------------------------------------

import sys
#from copy import copy
import copy

#-------------------------------------------------------------------------------
# Begin code that is ported from code provided by Dr. Athitsos
class logical_expression:
    """A logical statement/sentence/expression class"""
    # All types need to be mutable, so we don't have to pass in the whole class.
    # We can just pass, for example, the symbol variable to a function, and the
    # function's changes will actually alter the class variable. Thus, lists.
    def __init__(self):
        self.symbol = ['']
        self.connective = ['']
        self.subexpressions = []


def print_expression(expression, separator):
    """Prints the given expression using the given separator"""
    if expression == 0 or expression == None or expression == '':
        print '\nINVALID\n'

    elif expression.symbol[0]: # If it is a base case (symbol)
        sys.stdout.write('%s' % expression.symbol[0])

    else: # Otherwise it is a subexpression
        sys.stdout.write('(%s' % expression.connective[0])
        for subexpression in expression.subexpressions:
            sys.stdout.write(' ')
            print_expression(subexpression, '')
            sys.stdout.write('%s' % separator)
        sys.stdout.write(')')


def read_expression(input_string, counter=[0]):
    """Reads the next logical expression in input_string"""
    # Note: counter is a list because it needs to be a mutable object so the
    # recursive calls can change it, since we can't pass the address in Python.
    result = logical_expression()
    length = len(input_string)
    while True:
        if counter[0] >= length:
            break

        if input_string[counter[0]] == ' ':    # Skip whitespace
            counter[0] += 1
            continue

        elif input_string[counter[0]] == '(':  # It's the beginning of a connective
            counter[0] += 1
            read_word(input_string, counter, result.connective)
            read_subexpressions(input_string, counter, result.subexpressions)
            break

        else:  # It is a word
            read_word(input_string, counter, result.symbol)
            break
    return result


def read_subexpressions(input_string, counter, subexpressions):
    """Reads a subexpression from input_string"""
    length = len(input_string)
    while True:
        if counter[0] >= length:
            print '\nUnexpected end of input.\n'
            return 0

        if input_string[counter[0]] == ' ':     # Skip whitespace
            counter[0] += 1
            continue

        if input_string[counter[0]] == ')':     # We are done
            counter[0] += 1
            return 1

        else:
            expression = read_expression(input_string, counter)
            subexpressions.append(expression)


def read_word(input_string, counter, target):
    """Reads the next word of an input string and stores it in target"""
    word = ''
    while True:
        if counter[0] >= len(input_string):
            break

        if input_string[counter[0]].isalnum() or input_string[counter[0]] == '_':
            target[0] += input_string[counter[0]]
            counter[0] += 1

        elif input_string[counter[0]] == ')' or input_string[counter[0]] == ' ':
            break

        else:
            print('Unexpected character %s.' % input_string[counter[0]])
            sys.exit(1)


def valid_expression(expression):
    """Determines if the given expression is valid according to our rules"""
    if expression.symbol[0]:
        return valid_symbol(expression.symbol[0])

    if expression.connective[0].lower() == 'if' or expression.connective[0].lower() == 'iff':
        if len(expression.subexpressions) != 2:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() == 'not':
        if len(expression.subexpressions) != 1:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() != 'and' and \
         expression.connective[0].lower() != 'or' and \
         expression.connective[0].lower() != 'xor':
        print('Error: unknown connective %s.' % expression.connective[0])
        return 0

    for subexpression in expression.subexpressions:
        if not valid_expression(subexpression):
            return 0
    return 1


def valid_symbol(symbol):
    """Returns whether the given symbol is valid according to our rules."""
    if not symbol:
        return 0

    for s in symbol:
        if not s.isalnum() and s != '_':
            return 0
    return 1

# End of ported code
#-------------------------------------------------------------------------------


# Add all your functions here


def check_true_false(kb, alpha, additional_knowledge):
    #print '\n\n', kb_dict
    
    additional_knowledge_symbols = list(extract_symbols(additional_knowledge))  # symbols from additional knowledge
    #print '\nsymbols in additional knwledge:\n', additional_knowledge_symbols
    
    # Assign truth values to additional knowledge symbols
    model = {}
    for subex in additional_knowledge.subexpressions:
        symbol = subex.symbol[0]
        if symbol != '':
            model[symbol] = True
        elif subex.connective[0] == 'not':
            symbol = subex.subexpressions[0].symbol[0]
            model[symbol] = False
            
    #print '\ndict in additional knwledge:\n', model
    
    kb_symbols = extract_symbols(kb)    # extract symbols from kb
    #kb_symbols = list(extract_symbols(kb))
    #print '\nsymbols in kb:\n', kb_symbols
    
    alpha_symbols = extract_symbols(alpha)  # extract symbols from alpha
    #alpha_symbols = list(extract_symbols(alpha))
    #print '\nsymbols in alpha:\n', alpha_symbols
    
    kb_symbols.update(alpha_symbols)    # combine symbols from kb and alpha
    kb.subexpressions.extend(additional_knowledge.subexpressions)   # combine knowledge to kb
    
    # Verify it is a valid logical expression
    if not valid_expression(kb):
        sys.exit('knowledge base extended with invalid additional knowledge')
    
    list_kb_symbols = list(kb_symbols)
    isEntailsAlpha = TT_ENTAILS(kb, alpha, list_kb_symbols, model)
    #print isEntailsAlpha, 'Entailment Alpha'
    
    neg_alpha = get_negation(alpha)
    if not valid_expression(neg_alpha):
        sys.exit('invalid negation of alpha')
    
    print '\n Negation of Alpha is:\n'
    print_expression(neg_alpha, '')
    
    isEntailsNegAlpha = TT_ENTAILS(kb, neg_alpha, list_kb_symbols, model)
    #print isEntailsNegAlpha, 'Entailment Neg Alph'
    
    if isEntailsAlpha and not isEntailsNegAlpha:
        result = 'definitely true'
    if not isEntailsAlpha and isEntailsNegAlpha:
        result = 'definitely false'
    if not isEntailsAlpha and not isEntailsNegAlpha:
        result = 'possibly true, possibly false'
    if isEntailsAlpha and isEntailsNegAlpha:
        result = 'both true and false'
    write_result(result)
    print result
    
def write_result(result):
    f = open('result.txt', 'w')
    f.write(result)
    f.close()
    
def get_negation(statement):
    """Returns the negation of a statement in the form of a logical_expression object"""
    neg_statement = logical_expression()
    neg_statement.connective[0] = 'not'
    neg_statement.subexpressions.append(statement)
    return neg_statement
    
"""
TT_Entails (modified version) to check for entailment 
@param kb       The knowledge base
@param alpha    The statement to check entailment for
@param symbols  All symbols in the knowledge base and alpha included
@param model    Dict containing truth values of symbols
@return Boolean value denoting whether the KB entails alpha or not 
"""
def TT_ENTAILS(kb, alpha, symbols, model):
    return TT_CHECK_ALL(kb, alpha, symbols, model)

def TT_CHECK_ALL(kb, alpha, symbols, model):
    if not symbols:
        if PL_TRUE(kb, model):
            return PL_TRUE(alpha, model)
        return True # if KB is false, return true
    else:
        p = symbols[0:1][0]
        rest = symbols[1:]
        
        if p not in model:      # if symbol p not present in model, process model by adding both True/False values for symbol
            model1 = copy.deepcopy(model)
            model2 = copy.deepcopy(model)
                    
            model1[p] = True
            model2[p] = False

            result1 = TT_CHECK_ALL(kb, alpha, rest, model1)
            result2 = TT_CHECK_ALL(kb, alpha, rest, model2)
            return result1 and result2
        else:       # symbol already present in model
            return TT_CHECK_ALL(kb, alpha, rest, model)

def PL_TRUE(pl, model):
    symbol = pl.symbol[0]
    
    if symbol != '':
        return model[pl.symbol[0]]
    elif pl.connective[0] != '':
        conn = pl.connective[0].lower()
        
        if conn == 'and':
            if len(pl.subexpressions) > 0:
                for subexp in pl.subexpressions:
                    if not PL_TRUE(subexp, model):
                        return False
            return True
        elif conn == 'or':
            if len(pl.subexpressions) > 0:
                for subexp in pl.subexpressions:
                    if PL_TRUE(subexp, model):
                        return True
            return False
        elif conn == 'xor':
            if len(pl.subexpressions) > 0:                
                count = 0
                for subexp in pl.subexpressions:
                    if PL_TRUE(subexp, model):
                        count += 1
                if count == 1:
                    return True
            return False
        elif conn == 'not':
            return not PL_TRUE(pl.subexpressions[0], model)
        elif conn == 'if':
            if PL_TRUE(pl.subexpressions[0], model):
                return PL_TRUE(pl.subexpressions[1], model)
            return True        
        elif conn == 'iff':
            if PL_TRUE(pl.subexpressions[0], model) == PL_TRUE(pl.subexpressions[1], model):
                return True
            return False

def extract_symbols(expression):    
    symbols = set()
    if expression == 0 or expression == None or expression == '':
        return

    elif expression.symbol[0]: # If it is a base case (symbol)
        return set(expression.symbol)

    else: # Otherwise it is a subexpression
        for subexpression in expression.subexpressions:
            update_symbols = extract_symbols(subexpression)
            if update_symbols:
                symbols.update(update_symbols)
                
    #print truth_values_dict
    return symbols