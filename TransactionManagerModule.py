# ------------------------------------------------------------------------------
# Transaction Manager for the scheduler group project for CS 5570
#
# Group 4: Ergin Bostanci, Rod Skoglund, Jonathan Wolfe, Pavan Yannamaneni 
# ------------------------------------------------------------------------------
import random as rnd

class TransactionManager:
    '''
    Class to handle the random generation of a history containing
    a given number of transactions on a given number of data items
    '''
    def __init__(self):
        self.transactions = []  # list of randomly generated transactions
        self.history = ""       # string of operations from transactions

    def generate_transactions(self, transaction_count, item_count):
        '''
        The function to randomly generate a given number of transactions
        with a random number of operations distributed on a given number
        of data items

        Parameters:
            transaction_count (int): Number of transactions to generate
            item_count (int): Number of data items to spread over operations
        '''
        print("TODO: implement transaction generator")
        '''
        TODO:
          - Create transaction_count number of transactions
          - Each transaction should be a string in the format of
            "T1: r(x); w(x); r(y) etc"
          - Each transaction should be added to self.transactions
          - Each transaction should have a random amount of read
            and write operations with a minimum and maximum amount
            of operations
          - Each transaction should be ended in either a commit or abort
          - Each operation should randomly choose a data item within the
            range of data items specified by item_count
          - Data items should be a lowercase a-z character
          - If the user specifies 5 data items, then the operators should
            only use the first 5 a-z characters
        '''

    def generate_history(self):
        '''
        The function to randomly process operations of generated transactions
        into a string to be passed into a scheduler

        Returns:
            String: History of transaction operations
        '''
        print("TODO: implement history generator")
        '''
        TODO:
          - Create a string of a history of operations from self.transactions
          - The string should be set to self.history
          - The resulting string should be in the format of "w3(c); r3(c); c3;
            a2; r1(c); r1(c); w1(b); a1;"
          - Transactions should be removed from self.transactions once they
            have been added to self.history
        '''
        return self.history

if __name__ == "__main__":
    print("This module should not be run directly, use the main module")
