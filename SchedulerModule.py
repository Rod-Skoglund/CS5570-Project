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
            if(history[pos] == ' ' and begin != pos):
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
        
        while len(operation_list) > 0:
            # Respect FIFO order
            operation = operation_list.pop(0)

            # Route to appropriate function based on operator type
            if operation.is_read() or operation.is_write():
                self.process_read_write(operation)
            elif operation.is_commit():
                self.process_commits(operation.ID)
            elif operation.is_abort():
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
            self.logger.custom_log("{} blocked".format(str(operator)))
            return

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
        
        transaction = self.transaction_table[transaction_ID]
        
        if transaction.is_restarted():
            self.logger.custom_log("Send transaction {} to be requeued." \
                                   .format(transaction_ID))
            restarting_ops = copy.deepcopy(transaction.blocked_operations)
            self.transaction_table.pop(transaction_ID)
            if not restarting_ops[-1].is_commit():
                restarting_ops.append(OperatorModule \
                        .Operator("c{};".format(transaction_ID)))
            self.process_operations(restarting_ops)
        elif transaction.is_blocked():
            transaction.add_blocked_operation(OperatorModule. \
                    Operator("c{};".format(transaction_ID)))
            self.logger.custom_log("Commit {} is blocked" \
                                   .format(transaction_ID))
        else:
            self.logger.custom_log("Starting commit of T{}" \
                                   .format(transaction_ID))
            transaction.set_committed()
            for idx in range(0, len(transaction.active_operations)):
                self.logger.add_data_manager_operation( \
                    transaction.active_operations[idx])
                if idx == len(transaction.active_operations) - 1:
                    self.logger.process_commit(transaction_ID)
                self.release_lock(transaction.active_operations[idx])

    def process_aborts(self, transaction_ID):
        '''
        Processes transaction aborts by marking the transaction as aborted
        and removing all existing locks held by the transaction's operations

        Parameters:
            transaction_ID (int) - Number of the transaction ID to abort
        '''
        self.logger.custom_log("Aborting transaction {}".format(transaction_ID))
        transaction = self.transaction_table[transaction_ID]
        
        if not transaction.is_restarted():
            for op in transaction.active_operations:
                self.release_lock(op)
                
        self.clear_waiting_lock_ops(transaction.blocked_operations)
                
        transaction.active_operations.extend(transaction.blocked_operations)
        transaction.blocked_operations.clear()
        transaction.set_aborted()
        self.logger.process_abort(transaction_ID)                

    def restart_transaction(self, transaction_ID):
        '''
        Restart the transaction by unlocking any active operations, setting
        the transaction status to restart and moving the active operations
        list to the front of the blocked operations list

        Parameters:
            transaction_ID (int) - Transaction ID of transaction to restart
        '''

        if (transaction_ID in self.transaction_table) and \
           not self.transaction_table[transaction_ID].is_restarted():
            self.logger.custom_log("Restarting {}".format(transaction_ID))
            transaction = self.transaction_table[transaction_ID]
            transaction.set_restarted()
            self.clear_waiting_lock_ops(transaction.blocked_operations)                
            transaction.blocked_operations = \
                transaction.active_operations + transaction.blocked_operations
            for op in transaction.active_operations:
                self.release_lock(op)
            transaction.active_operations.clear()
            self.logger.process_restart(transaction_ID)

            if transaction.blocked_operations[-1].is_commit():
                self.process_commits(transaction_ID)
            elif transaction.blocked_operations[-1].is_abort():
                self.process_aborts(transaction_ID)

    def unblock_transaction(self, transaction_ID):
        '''
        Removes a block held on a transaction and begins processing blocked
        operations

        Parameters:
            transaction_ID (int) - Transaction ID of transaction to unblock
        '''
        transaction = self.transaction_table[transaction_ID]
        self.logger.unblock_transaction(transaction_ID)
        if len(transaction.blocked_operations) == 0:
            return
        blocked_ops = copy.deepcopy(transaction.blocked_operations)
        transaction.blocked_operations.clear()
        transaction.set_active()
        for op_index in range(0, len(blocked_ops)):
            if(transaction.is_blocked()):
                transaction.blocked_operations += blocked_ops[op_index:]
                break
            else:
                if blocked_ops[op_index].is_read() or \
                   blocked_ops[op_index].is_write():
                    self.process_read_write(blocked_ops[op_index])
                elif blocked_ops[op_index].is_commit():
                    self.process_commits(blocked_ops[op_index].ID)

    def release_lock(self, operation):
        '''
        Removes the lock held by the operation and initiates processing of
        waiting operations

        Parameters:
            operation (Operator class) - Operation of the lock to be released
        '''

        self.logger.release_lock(operation)
        with open("processes_log.txt", "w") as processes_file:
            processes_file.write(self.logger.processes_log)
        lock = self.lock_table[operation.get_data_item()]
        lock.remove_holding_operation(operation)
        
        lock.set_readlock()
        for op in lock.holding_operations:
            if op.is_write():
                lock.set_writelock()
                break
            
        if not lock.holding_operations and not lock.waiting_operations:
            self.lock_table.pop(lock.get_data_item())
        else:
            waiting_ops = copy.deepcopy(lock.waiting_operations)
            lock.waiting_operations.clear()
            for op in waiting_ops:
                self.unblock_transaction(op.get_ID())

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

        for hold_op in lock.holding_operations:
            hold_timestamp = self.transaction_table[hold_op.get_ID()].timestamp
            if transaction.timestamp > hold_timestamp:
                must_wait = True
                break

        if must_wait:
            lock.add_waiting_operation(operator)
            transaction.add_blocked_operation(operator)
            transaction.set_blocked()
            self.logger.block_transaction(operator)
        else:            
            restart_list = []
            for hold_op in copy.deepcopy(lock.holding_operations):
                hold_timestamp = \
                    self.transaction_table[hold_op.get_ID()].timestamp
                if transaction.timestamp < hold_timestamp:
                    restart_list.append(hold_op.get_ID())
                    lock.remove_holding_operation(hold_op)

            if operator.is_write():
                lock.set_writelock()
            if len(lock.holding_operations) == 0 and operator.is_read():
                lock.set_readlock()
                
            lock.add_holding_operation(operator)
            transaction.add_active_operation(operator)
            self.logger.apply_lock(operator)

            # Delay restarting transactions to prevent advancing the waiting
            # list before the requesting operation can be added as holding
            for transaction_ID in restart_list:
                self.restart_transaction(transaction_ID)

    def report_schedule(self):
        '''
        Print a report of the history created by the scheduler and
        any active or blocked transactions still in the scheduler
        '''
        with open("data_manager_log.txt", "w") as data_manager_file:
            data_manager_file.write("H:" + self.logger.data_manager_log)

        with open("processes_log.txt", "w") as processes_file:
            processes_file.write(self.logger.processes_log)

        with open("transactions_log.txt" , "w") as transactions_file:
            transactions = list(self.transaction_table.values())
            for transaction in transactions:
                transactions_file.write(str(transaction) + "\n")

        with open("locks_log.txt", "w") as locks_file:
            locks = list(self.lock_table.values())
            for lock in locks:
                locks_file.write(str(lock) + "\n")

        with open("produced_history.txt", "w") as history_file:
            for op in self.logger.history:
                if op[0] == 'p':
                    history_file.write(str(op[1]))
                elif op[0] == 'a' or op[0] == 'c':
                    history_file.write(op[0] + str(op[1]) + ";")
                else:
                    history_file.write(op[0] + str(op[1]))

        print("Scheduler completed all tasks")

    def clear_waiting_lock_ops(self, waiting_ops):
        '''
        Removes operations from all locks with the operation in locks'
        the waiting list

        Parameters:
            waiting_ops (List) - List of blocked operations
        '''

        for op in waiting_ops:
            if op.get_data_item() in self.lock_table:
                lock = self.lock_table[op.get_data_item()]
                lock.remove_waiting_operation(op)
                self.logger.custom_log("Removing blocked operation {} from " \
                                       "lock's waiting list".format(str(op)))
                if not lock.holding_operations and \
                   not lock.remove_waiting_operation:
                    self.lock_table.pop(lock.get_data_item())

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
