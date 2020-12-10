# ------------------------------------------------------------------------------
# Logger for the scheduler group project for CS 5570
#
# Group 4: Ergin Bostanci, Rod Skoglund, Jonathan Wolfe, Pavan Yannamaneni 
# ------------------------------------------------------------------------------
import LockModule
import OperatorModule

import copy

class Logger:
    '''
    Maintains a log of actions performed by the scheduler and a log of
    operations sent to the data manager
    '''
    def __init__(self):
        self.processes_log = ""
        # String of processes performed by the scheduler with each line
        # starting with a number indicating the order of the process and
        # the remaining line detailing the performed action
        self.processes_timestamp = 1
        # Number tracking the progress of the processes and is incremented
        # with each new process added to the log
        self.data_manager_log = ""
        # String of operations sent to the data manager in the order that
        # they were sent
        self.history = []

    def apply_lock(self, operation):
        '''
        Logs applies lock on a operation to the processes log
        
        Parameters:
            operation (Operator class) - operator applying the lock
        '''
        self.processes_log += "{} Apply lock on {}\n".format( \
            self.processes_timestamp, operation)
        self.processes_timestamp += 1

        self.history.append(('l', operation))

    def process_operation(self, operation):
        '''
        Logs processing of an operation to the data manager
        to the processes log
        
        Parameters:
            operation (Operator class) - operator being processed
        '''
        self.processes_log += "{} Process {}\n".format( \
            self.processes_timestamp, operation)
        self.processes_timestamp += 1

        self.history.append(('p', operation))

    def release_lock(self, operation):
        '''
        Logs releasing a lock on an operation to the processes log
        
        Parameters:
            operation (Operator class) - operator with released lock
        '''
        self.processes_log += "{} Release lock on {}\n".format( \
            self.processes_timestamp, operation)
        self.processes_timestamp += 1

        self.history.append(('u', operation))

    def process_commit(self, transaction_ID):
        '''
        Logs committing a transaction to the processes log
        
        Parameters:
            transaction_ID (int) - Transaction ID number of the committed
                                    transaction
        '''
        self.processes_log += "{} Committed transaction {}\n".format( \
            self.processes_timestamp, transaction_ID)
        self.processes_timestamp += 1

        self.history.append(('c', transaction_ID))
        self.data_manager_log += " c{};".format(transaction_ID)

    def process_abort(self, transaction_ID):
        '''
        Logs aborting a transaction to the processes log
        
        Parameters:
            transaction_ID (int) - Transaction ID number of the aborted
                                    transaction
        '''
        self.processes_log += "{} Aborted transaction {}\n".format( \
            self.processes_timestamp, transaction_ID)
        self.processes_timestamp += 1

        self.history.append(('a', transaction_ID))

    def process_restart(self, transaction_ID):
        '''
        Logs restarting a transaction to the processes log
        
        Parameters:
            transaction_ID (int) - Transaction ID number of the restarted
                                    transaction
        '''
        self.processes_log += "{} Restart transaction {}\n".format( \
            self.processes_timestamp, transaction_ID)
        self.processes_timestamp += 1

        for op in copy.deepcopy(self.history):
            if op[0] == 'c' or op[0] == 'a':
                if op[1] == transaction_ID and op in self.history:
                    self.history.remove(op)
            elif op[1].ID == transaction_ID:
                if op in self.history:
                    self.history.remove(op)

    def block_transaction(self, operation):
        '''
        Logs blocking a transaction to the processes log
        
        Parameters:
            operation (Operator class) - operator causing the block
        '''
        self.processes_log += "{} Apply block for {}\n".format( \
            self.processes_timestamp, operation)
        self.processes_timestamp += 1

    def unblock_transaction(self, transaction_ID):
        '''
        Logs unblocking of a transaction to the processes log
        
        Parameters:
            transaction_ID (int) - Transaction ID number of the unblocked
                                    transaction
        '''
        self.processes_log += "{} Unblock transaction {}\n".format( \
            self.processes_timestamp, transaction_ID)
        self.processes_timestamp += 1

    def handle_conflict(self, operation, lock):
        '''
        Logs conflict to the processes log
        
        Parameters:
            operation (Operator class) - Operation involved in the conflict
            lock (Lock class) - Lock involved in the conflict
        '''
        self.processes_log += "{} Resolve conflict between {} and {} lock on" \
                              " {}\n".format( \
            self.processes_timestamp, \
            operation, \
            lock.get_lock_type(), \
            lock.get_data_item())
        self.processes_timestamp += 1

    def custom_log(self, message):
        '''
        Logs a custom message to the processes log

        Parameters:
            message (String) - Message to log in the processes log
        '''
        self.processes_log += "{} {}\n".format(self.processes_timestamp, \
                                               message)
        self.processes_timestamp += 1
    
    def add_data_manager_operation(self, operation):
        '''
        Appends operation to the end of the data manager log

        Parameters:
            operation (Operator class) -
                Operation to be sent to the data manager
        '''
        self.data_manager_log += " {}".format(operation)
        self.process_operation(operation)
