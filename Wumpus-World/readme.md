Title: This program is used to test entailment for any statement and negation of that statement in the wumpus world with some predefined rules to determine if its partially true, completely true, completely false or both true and false.
Assignment: https://omega.uta.edu/~gopikrishnav/classes/2018/fall/4308_5360/assmts/assmt7.html

Programming Language: Python

Structure:
    The code first extracts all the symbols in additional knowledge and assigns appropriate truth values to the symbols. Expressions from both KB and additional KB are then combined. Symbols from KB and alpha are combined.
    TT_ENTAILS runs twice, once for KB's entailment with alpha and negation of alpha

How to run the code:
>time python check_true_false.py wumpus_rules.txt additional_knowledge.txt statement.txt

NOTE: The implementation supports xor statements and is written so as to parse the input symbols from the provided statements dynamically.
    
