# CS5570-Project
UMKC CS 5570 Project

## Project Scope
- Use whatever programming language you like to implement a scheduler for a database
- The transactions will be of the form T1: r(x); w(x); r(y) etc.
- Generate random transactions set by the user eg I want 4 transactions
- Generate operations for those transactions on x number of data items. eg. user selects 3 data items. The order generated will be a total ordering
- The operations will be randomly sent to the scheduler. (each transactions operation order will be obeyed). 
- The application can also be given a proposed order of operations sent to a scheduler for testing.
    - r1(x); w2(y); w1(x); r3(z), etc...
- The scheduler will apply some variation of 2PL
- Some form of deadlock prevention
- Isolation levels enforced.  At the top level fully serializable.  Try to work in the other isolation levels as appropriate.

## Features
  - User will be prompted to randomly generate transactions or manually enter a history of transactions
  - If the user chooses random generation, then the user will be asked to enter the amount of transactions to generate followed by the amount of data items to disperse over the transactions
  - The number of transactions specified by the user must be at least 1
  - The number of data items specified by the user must be at least 1 and no more than 26
  - If the user enters an entry that does not follow the restrictions above, the user will be warned of incorrect input and prompted again
  - The user input will then be either passed to the transaction manager or the manually entered history of transactions will be passed directly to the scheduler
  - Transactions will be in the form of strings with "T1: r1(x); w1(x); r1(y); c1;"
  - The History of transactions will be a string in the form "r1(x); r2(x); w1(x); r1(y); w2(y); c1; c2;"
  - A manually entered transaction must follow the proper format as designated above otherwise the user will be prompted to re-enter the history
  - The transaction manager will be responsible for randomly generating transactions then randomly combining them into a history with each transactions' operation order being obeyed
  - The transaction manager will then pass the randomly generated history of transactions to the scheduler in the form of a string
  - The scheduler will determine the order of operations to form a serializable history to send to a data manager using rigorous 2 phase locking and wound-wait deadlock prevention
  - This project does not implement a data manager and only simulates it by logging operations that would be sent to the data manager
  - This project does not simulate time passing and thus only the order of operations are relevant
  - Once the scheduler has processed all operations sent to it, it will generate a report of the history for sending operations to a data manager
  - The scheduler will generate a log of processes performed to reach the resulting history
  - The scheduler will report the final states of the transaction table and locking table
  
### Transaction Manager
  - The transaction manager will be provided with the user designated number of transactions and data items to randomly generate
  - Each transaction will contain a random number of 2 to 10 operations and ending with either a commit or an abort
  - The ratio of commits to aborts is 5 to 1
  - Operations will be either read or write and the associated data item for each operation will be randomly choosen from a range of data items the size of the specified amount     by the user
  - Data items are lowercase characters between a to z and begins at a and ending at the amount indicated by the user, e.g. 3 data items means a choice between a, b or c
  - Once the transactions are generated, the operations of each transaction will be randomly combined into a history with each transactions' operation order being obeyed
  - The transaction manager will then make available the randomized history of transactions to the scheduler 

### Scheduler
  - The scheduler receives histories as strings then processes the history into a receiving queue with each operation separated by spaces
  - The scheduler processes the receiving queue by popping off the first operation in the queue and processing it then proceeding to pop off the following one until there are no more operations in the queue to processed
  - Once the receiving queue is empty, a string of operations representing what was send to a data manager should be written to a file as well as a log scheduler processes and the final states of the transaction table and lock table
  - Every operation by a transaction not previously seen creates a transaction log
  - Every transaction log contains the transaction ID, starting timestamp, status as either active, blocked, aborted or committed, a list of operations that have been enacted and a list of operations that are blocked
  - When a transaction is first recieved by the scheduler, the transaction log should be created with its ID, active status and the current timestamp
  - When the scheduler decides to restart a transaction, all of the operations of the transaction will be collected and not processed until a commit or abort is recieved at which point the transaction will be sent back to the transaction manager which is simulated by appending the collected operations to the end of the scheduler's queue
  - Once a transaction is committed or aborted, any new operations recieved should raise an error and not be processed
  - Received operations owned by a blocked transaction are added to a queue for the transaction to be processed when the transaction is unblocked
  - Once an operation is processed, the action taken by the scheduler is logged in a logger
  - All locking operations, read and write operations, commits and unlocking operations are recorded in a history of operations communicating with a data manager
  - Locks are added to the data manager history when they are enabled and the operations, unlocks and commits are added after a commit for the transaction is received

**Rigorous 2PL**
  - Whenever an operation acts on a data item, a lock log is created on the data item
  - Lock logs must track the data item that is locked, lock type as read or write, a list of operators holding the lock and a list of operators waiting on the lock
  - New locks on data items may be acquired but none can be released during the growing phase
  - Existing locks may be released but no new locks can be acquired during the shrinking phase
  - Locks can only be unlocked after the transaction is committed or aborted
  - Locks cannot be converted from read to write or write to read and instead is treated as a conflicting operation, this avoids deadlocks with lock conversions 
 
**Wound-Wait Deadlock Prevention**
  - In the event a requesting operation conflicts with a holding operation
  - If the requesting transaction timestamp is less than the holding timestamp then holding transaction should be aborted and restarted
  - Otherwise the requesting transaction is blocked and the operation is added to the lock's waiting list
