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
    transaction_count = ''
    type_count = ''

    # Either a history provided by the user or a generated one
    history = ""
    generate_history = True

    # Get whether user wants to manually enter a history or generate it
    while(True):
        user_choice = input("Do you want to manually enter a history? (y/n) ")
        user_choice = user_choice.lower()

        if user_choice == 'y' or user_choice == 'n':
            if user_choice == 'y':
                generate_history = False
            break
        else:
            print("Please enter either y or n")

    if generate_history:
        # Get number of transactions from user
        while(True):
            transaction_count = input("Enter the number of transactions as " \
                                      "a positive number: " )
            try:
                transaction_count = int(transaction_count)
                if transaction_count > 0:
                    break
                else:
                    raise Exception("Transaction count less than 1")
            except ValueError:
                print("Please enter a numeric value")
            except:
                print("Please enter a number greater than zero")
        
        # Get number of data items from user
        while(True):
            type_count = input("Enter the number of data types as an positive " \
                               "integer less than 27: " )
            try:
                type_count = int(type_count)
                if type_count > 0 and type_count < 27:
                    break
                else:
                    raise Exception("Data item count less than 1 or " \
                                    "greater than 27")
            except ValueError:
                print("Please enter a numeric value")
            except:
                print("Please enter a number greater than zero and less than 27")

        # Use input to randomly generate a history to be used in a scheduler
        tranaction_manager.generate_transactions(transaction_count, type_count)
        history = tranaction_manager.generate_history()

    else:
        history = input("Enter a transaction history to send to the " \
                        "scheduler, expected input format is " \
                        "'r2(a); r1(a); w1(a); w2(b); c2; a1;': ")

    # Using Strict 2PL and Wait Wound deadlock prevention create a
    # serializable history that could be sent to a data manager
    scheduler.extract_history(history)

    # Print a report of the history created by the scheduler and any
    # active or blocked transactions still in the scheduler
    scheduler.report_schedule()

if __name__ == "__main__":
    main()
