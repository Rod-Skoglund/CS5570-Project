# ------------------------------------------------------------------------------
# Scheduler for the scheduler group project for CS 5570
#
# Group 4: Ergin Bostanci, Rod Skoglund, Jonathan Wolfe, Pavan Yannamaneni 
# ------------------------------------------------------------------------------

class Transaction:
    '''
    Class describing the attributes of a transaction
    '''
    def __init__(self, ID):
        '''
        Initializes the transaction, only ID is required to initialize, status
        defaults to active, status and operations can be altered via methods

        Parameters:
            ID (int) - number indicating the ID of the transaction
        '''
        self.ID = ID
        # Numerical identifier associated with the transaction
        self.status = "active"
        # Status of the transaction, valid entries are "active",
        # "blocked", "committed" "aborted"
        self.operations = []
        # List of operations associated with the transaction in the form
        # of strings of the operation for example, "r(a)" or "w(a)"

    '''
    TODO:
      - Add methods to set status and add or remove operations
    '''

class Lock:
    '''
    Class describing the attributes of a lock
    '''
    def __init__(self, item):
        '''
        Initializes the Lock requiring only the data item to be specified,
        lock type and holding and waiting transactions can be changed via
        methods

        Parameter:
            item (char) - character indicating the data item, a-z,
                          with the lock
        '''
        self.item = item
        # Data item associated with the lock, valid entries are
        # a-z for the data item
        self.type = "read"
        # Lock type, read by default, can be "read" or "write"
        self.holding_transactions = []
        # Transactions holding the lock, valid entries are transaction IDs
        self.waiting_transactions = []
        # Transactions waiting on the lock, valid entries are transaction IDs

    '''
    TODO:
      - Add methods to set type and add or remove transactions from holding
        or waiting transactions
    '''

class Scheduler:
    '''
    Implementation of the scheduler
    '''
    def __init__(self):
        self.transaction_table = {}
        # Hash table for transactions with transaction ID as a key and
        # Transaction class as the value
        self.lock_table = {}
        # Hash table for locks with data item as the key and Lock class as
        # the value
        self.schedule = ""
        # Final serialiable history produced by scheduler
        self.timestamp = 1
        # Timestamp for tracking ages of operations

    def create_schedule(self, history):
        '''
        Creates a serializable history from a provided history of operations
        of transactions using Strict 2 phase locking with wait-wound deadlock
        prevention

        Parameters:
            history (string) - history of operations of transactions in the form
                of "w3(a); w2(c); w2(a); r1(d); c3; a2; etc"
        '''
        print("TODO: implement main scheduling method")
        '''
        TODO:
          - Add handling to loop through each operation in the history
          - Add ability to extract operation information
          - Track index in the history to follow which operation to process
        '''
        
    '''
    TODO:
      - Scheduler needs more designing to implement 2PL and wait-wound
        prevention, many more TODOs to come
    '''

    def print_schedule(self):
        '''
        Print a report of the history created by the scheduler and
        any active or blocked transactions still in the scheduler
        '''
        print("TODO: implement schedule printer")
        '''
        TODO:
          - Print a report of the self.schedule
          - Print any active or blocked transactions in self.transaction_table
        '''

    def get_timestamp(self):
        '''
        Returns the current timestamp then increases it by 1
        '''
        time = self.timestamp
        self.timestamp += 1
        return time

    def current_timestamp(self):
        '''
        Returns the current timestamp
        '''
        return self.timestamp

if __name__ == "__main__":
    print("This module should not be run directly, use the main module")
