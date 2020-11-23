# ------------------------------------------------------------------------------
# Lock Class for the scheduler group project for CS 5570
#
# Group 4: Ergin Bostanci, Rod Skoglund, Jonathan Wolfe, Pavan Yannamaneni 
# ------------------------------------------------------------------------------
import OperatorModule

class Lock:
    '''
    Class describing the attributes of a lock
    '''
    def __init__(self, operation):
        '''
        Initializes the Lock requiring only the data item to be specified,
        lock type and holding and waiting transactions can be changed via
        methods

        Parameter:
            operation (Operator class) - Operator holding the lock
        '''
        self.item = operation.get_data_item()
        # Data item associated with the lock, valid entries are
        # a-z for the data item
        self.type = False
        # Lock type, read by default, False indicated read and
        # True indicates write
        self.holding_operations = [operation]
        # Operations holding the lock, valid entries are operations with the
        # type, transaction ID and data item in a string e.g. "w1(b)". These
        # are operations that the lock is for
        self.waiting_operations = []
        # Operations waiting on the lock, valid entries are operations with the
        # type, transaction ID and data item. These are operations that cannot
        # be processed because a conflicting lock is already enacted

        # Initialize for a write lock if the operation is a write
        if operation.is_write():
            self.set_writelock()

    def set_readlock(self):
        '''
        Sets the lock type to read
        '''
        self.type = False

    def set_writelock(self):
        '''
        Sets the lock type to write
        '''
        self.type = True

    def is_readlock(self):
        '''
        Returns True if the lock is a Read lock otherwise False
        '''
        return self.type == False

    def is_writelock(self):
        '''
        Returns True if the lock is a Wrtie lock otherwise False
        '''
        return self.type == True

    def get_lock_type(self):
        '''
        Returns the lock type(string), "write" or "read"
        '''
        return 'write' if self.type else 'read'

    def get_data_item(self):
        '''
        Returns the data item(string) for the lock
        '''
        return self.item

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
