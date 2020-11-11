# ------------------------------------------------------------------------------
# Scheduler for the scheduler group project for CS 5570
#
# Group 4: Ergin Bostanci, Rod Skoglund, Jonathan Wolfe, Pavan Yannamaneni 
# ------------------------------------------------------------------------------
import TransactionModule
import LockModule
import LoggerModule

class Scheduler:
    '''
    Creates a serializable history from a provided history of operations
    of transactions using Strict 2 phase locking with wait-wound deadlock
    prevention then reports on the resulting schedule
    '''
    def __init__(self):
        self.transaction_table = {}
        # Hash table for transactions with transaction ID as a key and
        # Transaction class as the value
        self.lock_table = {}
        # Hash table for locks with data item as the key and Lock class as
        # the value
        self.received_operations = []
        # Queue for holding each operation in the order it was receieved
        self.schedule = ""
        # Final serialiable history produced by scheduler
        self.timestamp = 1
        # Timestamp for tracking ages of operations
        self.logger = LoggerModule.Logger()
        # Logger for maintaining activities performed by the scheduler

    def extract_history(self, history):
        '''
        Extracts the operations from the history by spaces into the
        received_operations queue

        Parameters:
            history (string) - history of operations of transactions in the form
                of "w3(a); w2(c); w2(a); r1(d); c3; a2; etc"
        '''
        print("TODO: implement extract_history method")
        '''
        TODO:
          - Add ability to extract operations from the provided history into
          items in the received_operations queue
          - Order of the operations must be maintained
          - Operations should be separated by spaces
        '''

        self.process_history()

    def process_operations(self, operation_list = self.received_operations):
        '''
        Loops through each operation in operation_list routing each operation
        to the appropriate function. Once the queue is empty, it then calls
        on the generation of a report of the schedule

        Parameters:
            operation_list (list) - Queue of operations to process in FIFO order
        '''
        print("TODO: implement process_history method")
        '''
        TODO:
          - Add handling to loop through each operation in operation_list
          - Pop off each operation from the operation_list as it is processed
          - Route each operation to the appropriate function
        '''
        
    def process_read_write(self, operator):
        '''
        Processes read and write operators using 2 phase locking
        
        Parameters:
            operator (string) - operator requesting to be processed
        '''
        print("TODO: implement process_read_write method")
        '''
        TODO:
        '''

    def process_commits(self, transaction_ID):
        '''
        Processes transaction commits by adding transaction operations
        to the data manager log, initiating the release of locks
        held by the transaction and marking the transaction as committed

        Parameters:
            transaction_ID (int) - Number of the transaction ID to commit
        '''
        print("TODO: implement process_commits method")
        '''
        TODO:
          - Mark transaction as committed using the appropriate method in
          the transaction class
          - Add each operation in the transaction's active operation list to
          the data manager log with the self.logger
          - Call the appropriate method for each operation in the transaction's
          active operation list to unlock the lock held by each operation
        '''

    def process_aborts(self):
        '''
        
        '''
        print("TODO: implement process_aborts method")
        '''
        TODO:
        '''

    def restart_transaction(self):
        '''
        '''
        print("TODO: implement process_restart method")
        '''
        TODO:
        '''

    def unblock_transaction(self, transaction):
        '''
        Removes a block held on a transaction and begins processing blocked
        operations
        '''
        print("TODO: implement unblock_transaction method")
        '''
        TODO:
        - Set transaction status to active with the appropriate method
        - Make a temporary deep copy of the waiting list and empty the
        waiting list for the transaction
        - Use the appropriate method to process the copy of the waiting list
        '''

    def release_lock(self, operation):
        '''
        Removes the lock held by the operation and initiates processing of
        waiting operations

        Parameters:
            operation (string) - Operation of the lock to be released
        '''
        print("TODO: implement unlock_item method")
        '''
        TODO:
          - Find lock
          - Remove operation from holding operations list
          - If the holding and waiting operations lists are empty then after
          removing the operation completely remove the lock from self.lock_table
          - If the holding list is empty after removing the operation but
          the waiting list has operations, then move each waiting operation
          to holding if it is not conflicting
          - For each operation moved to holding, call the appropriate method
          to unblock its transaction
        '''

    def handle_conflict(self, operator, lock):
        '''
        Handles conflicts between operations and locks using wait-wound
        deadlock prevention

        Parameters:
            operator (string) - requesting operator
            lock (Lock class) - 
        '''
        print("TODO: implement handle_conflict method")
        '''
        TODO:
        '''

    def report_schedule(self):
        '''
        Print a report of the history created by the scheduler and
        any active or blocked transactions still in the scheduler
        '''
        print("TODO: implement report_schedule method")
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
