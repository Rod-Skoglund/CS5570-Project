# ------------------------------------------------------------------------------
# Entry point for the scheduler group project for CS 5570
#
# Group 4: Ergin Bostanci, Rod Skoglund, Jonathan Wolfe, Pavan Yannamaneni 
# ------------------------------------------------------------------------------

import TransactionManagerModule
import SchedulerModule

def main():
    '''
    Entry point function for the scheduler project
    '''
    
    tranaction_manager = TransactionManagerModule.TransactionManager()
    scheduler = SchedulerModule.Scheduler()

    # Get user input for the amount of transactions and data items
    '''
    TODO:
      - Get user input for the amount of transactions and data_types and
        replace the hard-coded numbers below with this functionality
      - Need to wrap user input requestw in while loops to keep asking
        till the user enters valid input
      - Validate input is a number > 0, prompt again otherwise
      - type_count should be < 27, prompt again otherwise
    '''
    transaction_count = 0
    type_count = 0

    while(True):
      transaction_count = input("Enter the number of transactions as an positive integer: " )
      if transaction_count.isnumeric():
          transaction_count=int(transaction_count)
          if transaction_count>0:
              break        
      print("Please enter a numeric value greater than zero")

    while(True):
      type_count = input("Enter the number of data types as an positive integer less than 27: " )
      if type_count.isnumeric():
          type_count=int(type_count)
          if type_count>0 and type_count<27:
              break        
      print("Please enter a numeric value greater than zero and less than 27")

    # Use input to randomly generate a history to be used in a scheduler
    tranaction_manager.generate_transactions(transaction_count, type_count)
    history = tranaction_manager.generate_history()    

    # Using Strict 2PL and Wait Wound deadlock prevention create a
    # serializable history that could be sent to a data manager
    scheduler.create_schedule(history)

    # Print a report of the history created by the scheduler and any
    # active or blocked transactions still in the scheduler
    scheduler.print_schedule()

if __name__ == "__main__":
    main()
