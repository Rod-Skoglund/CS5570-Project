# ------------------------------------------------------------------------------
# Transaction Class for the scheduler group project for CS 5570
#
# Group 4: Ergin Bostanci, Rod Skoglund, Jonathan Wolfe, Pavan Yannamaneni 
# ------------------------------------------------------------------------------

class Transaction:
    '''
    Class describing the attributes of a transaction
    '''
    def __init__(self, ID, Timestamp):
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
        self.timestamp = Timestamp
        # Timestamp of when the transaction was first receieved
        self.active_operations = []
        # List of active operations associated with the transaction in the form
        # of strings of the operation for example, "r1(a)" or "w1(a)"
        self.blocked_operations = []
        # List of blocked operations associated with the transaction in the form
        # of strings of the operation that have been receieved after the
        # transaction was blocked and are waiting for the transaction to be
        # unblocked to be processed. This ensures that the order of the
        # transaction is respected.

    def set_active(self):
        '''
        Sets the status of the transaction to active
        '''
        self.status = "active"

    def set_blocked(self):
        '''
        Sets the status of the transaction to blocked
        '''
        self.status = "blocked"

    def set_committed(self):
        '''
        Sets the status of the transaction to committed
        '''
        self.status = "committed"

    def set_aborted(self):
        '''
        Sets the status of the transaction to aborted
        '''
        self.status = "aborted"

    def add_active_operation(self, operation):
        '''
        Adds operation to the list of active operations for the transaction
        '''
        self.active_operations.append(operation)

    def remove_active_operation(self, operation):
        '''
        Removes first matching operation from the list of active operations
        for the transaction
        '''
        self.active_operations.remove(operation)

    def add_blocked_operation(self, operation):
        '''
        Adds operation to the list of blocked operations for the transaction
        '''
        self.blocked_operations.append(operation)

    def remove_blocked_operation(self, operation):
        '''
        Removes first matching operation from the list of blocked operations
        for the transaction
        '''
        self.blocked_operations.remove(operation)
