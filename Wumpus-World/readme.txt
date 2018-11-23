Name: Aditya Shantilal Sagam
UTA ID: 1001660179
Programming Language: Python
Structure:
    Instead of combining the KB and additional knowledge, this code first extracts all the symbols in additional knowledge and assigns appropriate truth values to the symbols. The expressions from both KB and additional KB are then combined. Symbols from KB and alpha are combined.
    TT_ENTAILS runs twice, once for KB's entailment with alpha and negation of alpha
How to run the code:
    >time python check_true_false.py wumpus_rules.txt additional_knowledge.txt statement.txt

NOTE: The implementation supports xor statements and is written so as to parse the input symbols from the provided statements dynamically.
    
