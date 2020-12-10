# ------------------------------------------------------------------------------
# Transaction Manager for the scheduler group project for CS 5570
#
# Group 4: Ergin Bostanci, Rod Skoglund, Jonathan Wolfe, Pavan Yannamaneni 
# ------------------------------------------------------------------------------
import random as rnd

class TransactionManager:
    '''
    Class to handle the random generation of a history containing
    a given number of transactions on a given number of data items
    '''
    def __init__(self):
        self.transactions = []  # list of randomly generated transactions
        self.history = ""       # string of operations from transactions

    def generate_transactions(self, transaction_count, item_count):
        '''
        The function to randomly generate a given number of transactions
        with a random number of operations distributed on a given number
        of data items

        Parameters:
            transaction_count (int): Number of transactions to generate
            item_count (int): Number of data items to spread over operations
        '''
        print("Attempting to generate {} transactions on {} data items" \
              .format(transaction_count, item_count))
        
        for transaction_id in range (1,transaction_count+1):
            Mytransation = "T{}:".format(transaction_id)
            for operation in range (0,rnd.randint(1,8)) :
                Mytransation += " {}{}({});" \
                                .format(rnd.choice(['w','r']), \
                                        transaction_id, \
                                        chr(rnd.randint(97, 96 + item_count)))
            Mytransation += " {}{};".format( \
                rnd.choices(['a','c'], weights = [1, 10,], k = 1)[0], \
                transaction_id)
            self.transactions.append(Mytransation)


    def generate_history(self):
        '''
        The function to randomly process operations of generated transactions
        into a string to be passed into a scheduler. Assumes proper formatting
        e.g. "T1: r1(x); w1(x); r1(y); c1;"

        Returns:
            String: History of transaction operations
        '''
        # Remove 'T#:' heading from every transaction
        for idx in range(0 , len(self.transactions)):
            transaction_ID_len = len(str(idx + 1))
            self.transactions[idx] = "{}".format(transaction_ID_len) + \
                            self.transactions[idx][2 + transaction_ID_len:]
            
        while len(self.transactions) > 0:
            transaction_idx = rnd.randint(0, len(self.transactions) - 1)
            transaction_ID_len = int(self.transactions[transaction_idx][0])

            # If all that remains is the abort or commit, remove
            # transaction after getting the operation
            if self.transactions[transaction_idx][2] == 'c' or \
               self.transactions[transaction_idx][2] == 'a':
                self.history += self.transactions[transaction_idx][1:]
                self.transactions.pop(transaction_idx)
            # Get the first operator then remove it from the transaction
            else:
                self.history += self.transactions[transaction_idx] \
                                [1:7 + transaction_ID_len]
                self.transactions[transaction_idx] = \
                self.transactions[transaction_idx][0] + \
                self.transactions[transaction_idx][(7 + transaction_ID_len):]

        with open("history_log.txt", "w") as history_file:
            history_file.write("Initial history:" + self.history)

        return self.history

if __name__ == "__main__":
    print("This module should not be run directly, use the main module")
