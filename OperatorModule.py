class Operator:
    def __init__(self, operator):
        '''
        Class for working with operators. Accepts a string representation
        and extracts relevant data. Throws exceptions if the string
        representation is not in the proper format

        Parameters:
            operator (string): String representation of the operation
        '''
        if type(operator) != str:
            raise Exception("Invalid operator type: " + operator)
        operator = operator.strip()
        if len(operator) < 2:
            raise Exception("Invalid operator length: " + operator)
        i = 1
        while operator[i] != '(' and operator[i] != ';':
            i += 1
            if i > 10:
                raise Exception("Invalid operator: " + operator)
        if not operator[1:i].isnumeric():
            raise Exception("Invalid operator format: " + operator)
        self.ID = int(operator[1:i])
        self.type = operator[0]
        self.data_item = None
        if self.type == 'r' or self.type == 'w':
            self.data_item = operator[2 + len(str(self.ID))]

    def get_ID(self):
        # Returns the transaction ID
        return self.ID

    def get_data_item(self):
        # Returns the data item
        return self.data_item

    def is_read(self):
        # Returns if the data type is a read
        return self.type == 'r'

    def is_write(self):
        # Returns if the data type is a write
        return self.type == 'w'

    def is_commit(self):
        # Returns if the data type is a commit
        return self.type == 'c'

    def is_abort(self):
        # Returns if the data type is an abort
        return self.type == 'a'

    def __str__(self):
        # Returns a string representation of the operator
        if self.type == 'r' or self.type == 'w':
            return '{}{}({});'.format(self.type, str(self.ID), self.data_item)
        else:
            return '{}{};'.format(self.type, str(self.ID))

    def __repr__(self):
        # Returns a representation of the operator
        return str(self)
