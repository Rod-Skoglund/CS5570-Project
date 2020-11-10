# ------------------------------------------------------------------------------
# Lock Class for the scheduler group project for CS 5570
#
# Group 4: Ergin Bostanci, Rod Skoglund, Jonathan Wolfe, Pavan Yannamaneni 
# ------------------------------------------------------------------------------

class Lock:
    '''
    Class describing the attributes of a lock
    '''
    def __init__(self, item, operation):
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
        self.holding_operations = [operation]
        # Operations holding the lock, valid entries are operations with the
        # type, transaction ID and data item in a string e.g. "w1(b)". These
        # are operations that the lock is for
        self.waiting_operations = []
        # Operations waiting on the lock, valid entries are operations with the
        # type, transaction ID and data item. These are operations that cannot
        # be processed because a conflicting lock is already enacted

        # Initialize for a write lock if the operation is a write
        if operation[0] == 'w':
            self.set_writelock()

    def set_readlock(self):
        '''
        Sets the lock type to read
        '''
        self.type = "read"

    def set_writelock(self):
        '''
        Sets the lock type to write
        '''
        self.type = "write"

    def add_holding_operation(self, operation):
        '''
        Adds the opertaion to the list of operations holding the lock
        '''
        self.holding_operations.append(operation)

    def remove_holding_operation(self, operation):
        '''
        Removes the operation from the list of operations holding the lock
        '''
        self.holding_operations.remove(operation)

    def add_waiting_operation(self, operation):
        '''
        Adds the operation to the list of operation waiting on the lock
        '''
        self.waiting_operations.append(operation)

    def remove_waiting_operation(self, operation):
        '''
        Removes the operation from the list of operations waiting on the lock
        '''
        self.waiting_operations.remove(operation)
