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
        self.status = 1
        # Status of the transaction, valid entries are "active",
        # "blocked", "committed" "aborted", "restarted"
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
        self.status = 1

    def is_active(self):
        '''
        Returns True is status is Active otherwise False
        '''
        return self.status == 1

    def set_blocked(self):
        '''
        Sets the status of the transaction to blocked
        '''
        self.status = 2

    def is_blocked(self):
        '''
        Returns True is status is Blocked otherwise False
        '''
        return self.status == 2

    def set_committed(self):
        '''
        Sets the status of the transaction to committed
        '''
        self.status = 3

    def is_committed(self):
        '''
        Returns True is status is Committed otherwise False
        '''
        return self.status == 3

    def set_aborted(self):
        '''
        Sets the status of the transaction to aborted
        '''
        self.status = 0

    def is_aborted(self):
        '''
        Returns True is status is Aborted otherwise False
        '''
        return self.status == 0

    def set_restarted(self):
        '''
        Sets the status of the transaction to restarted
        '''
        self.status = 4

    def is_restarted(self):
        '''
        Returns True is status is Restarted otherwise False
        '''
        return self.status == 4

    def add_active_operation(self, operation):
        '''
        Adds operation to the list of active operations for the transaction

        Parameters:
            operation(Operator class) - Operator to add to list
        '''
        self.active_operations.append(operation)

    def remove_active_operation(self, operation):
        '''
        Removes first matching operation from the list of active operations
        for the transaction

        Parameters:
            operation(Operator class) - Operator to remove from list
        '''
        self.active_operations.remove(operation)

    def add_blocked_operation(self, operation):
        '''
        Adds operation to the list of blocked operations for the transaction

        Parameters:
            operation(Operator class) - Operator to add to list
        '''
        self.blocked_operations.append(operation)

    def remove_blocked_operation(self, operation):
        '''
        Removes first matching operation from the list of blocked operations
        for the transaction

        Parameters:
            operation(Operator class) - Operator to remove from list
        '''
        self.blocked_operations.remove(operation)

    def __str__(self):
        # Returns a string representation of the Transaction
        return "ID: {}, Status: {}, Timestamp: {}, active: {}, blocked: {}" \
            .format(self.ID, self.status, self.timestamp,
                    self.active_operations, self.blocked_operations)

    def __repr__(self):
        # Returns a representation of the Transaction
        return str(self)
