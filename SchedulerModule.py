# ------------------------------------------------------------------------------
# Scheduler for the scheduler group project for CS 5570
#
# Group 4: Ergin Bostanci, Rod Skoglund, Jonathan Wolfe, Pavan Yannamaneni 
# ------------------------------------------------------------------------------
import TransactionModule
import LockModule
import LoggerModule
import OperatorModule

import copy

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
        begin = 0
        for pos in range(0, len(history)):
            if(history[pos] == ' '):
                op = OperatorModule.Operator(history[begin:pos])
                self.received_operations.append(op)
                if pos + 1 < len(history):
                    begin = pos + 1
                else:
                    begin = len(history)
        
        if(begin != len(history)):
            op = OperatorModule.Operator(history[begin:len(history)])
            self.received_operations.append(op)

        self.process_operations(self.received_operations)

    def process_operations(self, operation_list):
        '''
        Loops through each operation in operation_list routing each operation
        to the appropriate function. Once the queue is empty, it then calls
        on the generation of a report of the schedule

        Parameters:
            operation_list (list) - Queue of operations to process in FIFO order
        '''
        
        while len(self.received_operations) > 0:
            # Respect FIFO order
            operation = self.received_operations.pop(0)
            
            # Route to appropriate function based on operator type
            if operation.is_read() or operation.is_write():
                self.process_read_write(operation)
            elif operation.is_commit():
                self.process_commits(operation.ID)
            else operation.is_abort():
                self.process_aborts(operation.ID)
        
    def process_read_write(self, operator):
        '''
        Processes read and write operators using 2 phase locking
        
        Parameters:
            operator (Operator class) - operator requesting to be processed
        '''

        transaction = self.transaction_table.get(operator.get_ID())

        # Create a new transaction instance if it does not exist
        if transaction == None:
            transaction = TransactionModule.Transaction(operator.get_ID(), \
                                            self.get_timestamp())
            self.transaction_table[operator.get_ID()] = transaction

        # Processing an operator when it is blocked can cause the
        # transaction to no longer respect transaction ordering
        if transaction.is_blocked() or transaction.is_restarted():
            transaction.add_blocked_operation(operator)

        lock = self.lock_table.get(operator.get_data_item())

        # When a data item is not locked, there is no risk of conflicts
        if lock == None:
            self.lock_table[operator.get_data_item()] = \
                LockModule.Lock(operator)
            transaction.add_active_operation(operator)
            self.logger.apply_lock(operator)
        else:
            # A conflict can only occur when an operation is a write or
            # the lock on the data item is a write
            if lock.is_writelock() or operator.is_write():
                self.handle_conflict(operator, lock)
            else:
                lock.add_holding_operation(operator)
                self.logger.apply_lock(operator)
                transaction.add_active_operation(operator)

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
          - If the transaction is marked to restart, append the blocked
          operations list to the end of the receieved operations queue and
          remove the transaction from the transaction table
          - Mark transaction as committed using the appropriate method in
          the transaction class
          - Add each operation in the transaction's active operation list to
          the data manager log with the self.logger
          - Call the appropriate method for each operation in the transaction's
          active operation list to unlock the lock held by each operation
          - Log processing of commits
        '''

    def process_aborts(self, transaction_ID):
        '''
        Processes transaction aborts by marking the transaction as aborted
        and removing all existing locks held by the transaction's operations

        Parameters:
            transaction_ID (int) - Number of the transaction ID to abort
        '''
        print("TODO: implement process_aborts method")
        '''
        TODO:
          - If the transaction is marked to restart, move all operations
          from the blocked transactions to active and mark transaction as
          aborted
          - Mark transaction status as aborted using the appropriate method
          - Remove all locks on active operations
          - Log aborting transaction
        '''

    def restart_transaction(self, transaction_ID):
        '''
        Restart the transaction by unlocking any active operations, setting
        the transaction status to restart and moving the active operations
        list to the front of the blocked operations list

        Parameters:
            transaction_ID (int) - Transaction ID of transaction to restart
        '''
        print("TODO: implement process_restart method")
        '''
        TODO:
          - If transaction is already marked as restart then skip restarting
          - Mark status of the transaction to restarted by using the appropriate
          method
          - Unlock all operations in the active operations list for the
          transaction
          - Move the active operations list to the front of the blocked
          operations list
          - Log restarting of the transaction
        '''

    def unblock_transaction(self, transaction_ID):
        '''
        Removes a block held on a transaction and begins processing blocked
        operations

        Parameters:
            transaction_ID (int) - Transaction ID of transaction to unblock
        '''
        print("TODO: implement unblock_transaction method")
        '''
        TODO:
        - Set transaction status to active with the appropriate method
        - Make a temporary deep copy of the waiting list and empty the
        waiting list for the transaction
        - Use the appropriate method to process the copy of the waiting list
        - Log unblocking transactions
        '''

    def release_lock(self, operation):
        '''
        Removes the lock held by the operation and initiates processing of
        waiting operations

        Parameters:
            operation (Operator class) - Operation of the lock to be released
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
          - Log releasing locks
        '''

    def handle_conflict(self, operator, lock):
        '''
        Handles conflicts between operations and locks using wait-wound
        deadlock prevention

        Parameters:
            operator (Operator class) - requesting operator
            lock (Lock class) - conflicting lock
        '''
        must_wait = False
        transaction = self.transaction_table[operator.get_ID()]

        self.logger.handle_conflict(operator, lock)

        for hold_op in copy.deepcopy(lock.holding_operations):
            hold_timestamp = self.transaction_table[hold_op.get_ID()].timestamp
            if transaction.timestamp < hold_timestamp:
                self.restart_transaction[hold_op.get_ID()]
            elif transaction.timestamp > hold_timestamp:
                must_wait = True
                    
        if len(lock.holding_operations) == 0:
            lock.add_holding_operation(operator)
            lock.set_writelock() if operator.is_write() else lock.set_readlock()
            transaction.add_active_operation(operator)
            self.logger.apply_lock(operator)
        elif must_wait:
            lock.add_waiting_operation(operator)
            transaction.set_blocked()
            self.logger.block_transaction(operator)
        else:
            lock.add_holding_operation(operator)
            transaction.add_active_operation(operator)
            if operator.is_write():
                lock.set_writelock()
            self.logger.apply_lock(operator)

    def report_schedule(self):
        '''
        Print a report of the history created by the scheduler and
        any active or blocked transactions still in the scheduler
        '''
        print("TODO: implement report_schedule method")
        '''
        TODO:
          - Save a report of the scheduler processes from self.logger
          - Save a report on any active or blocked transactions in
          self.transaction_table
          - Save a report of the operations sent to the data manager from
          the self.logger
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
