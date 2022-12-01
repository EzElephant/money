import sys
import matplotlib.pyplot as plt

class Record:
    """Represent a record."""
    # constructor
    def __init__(self, cate, desc, cost):
        self._cate = cate
        self._desc = desc
        self._amount = cost
    # getter methods
    @property
    def cate(self):
        return self._cate
    @property
    def desc(self):
        return self._desc
    @property
    def amount(self):
        return self._amount

class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self):
        self._records = []
        try:
            # Use with open. In the end, the file will close automatically.
            with open('records.txt', 'r') as f:
                buffer = f.readline()
                # if empty string means that it is the first time to open program
                if (buffer == ''):
                    raise FileNotFoundError
                self._money = int(buffer)
                for tmp in f.readlines():
                    desc, amt = tmp.split(' ')
                    self._records.append(tuple([desc, int(amt)]))
                print('Welcome back!')
        # if the file has wrong format tell the user
        except ValueError:
            sys.stderr.write('Invalid format in records.txt.\n')
            self._money = self.ask_money()
        except FileNotFoundError:
            self._money = self.ask_money()

    @staticmethod
    def ask_money():
        while True:
            try:
                money = int(input('How much money do you have? '))
            # deal exception
            except ValueError:
                print('Invalid value for money, please enter an interger.')
                continue
            break
        return money

    def add(self):
        1
    # 1. Define the formal parameter so that a string input by the user
    # representing a record can be passed in.
    # 2. Convert the string into a Record instance.
    # 3. Check if the category is valid. For this step, the predefined
    # categories have to be passed in through the parameter.
    # 4. Add the Record into self._records if the category is valid.
    def view(self):
        1
    # 1. Print all the records and report the balance.
    def delete(self):
        1
    # 1. Define the formal parameter.
    # 2. Delete the specified record from self._records.
    def find(self):
        1
    # 1. Define the formal parameter to accept a non-nested list
    # (returned from find_subcategories)
    # 2. Print the records whose category is in the list passed in
    # and report the total amount of money of the listed records.
    def save(self):
        1
    # 1. Write the initial money and all the records to 'records.txt'.

class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self, L):
        self._categories = L

    def view(self, step = 0, L = []):
        if L == []:
            L = self._categories
        for cate in L:
            if type(cate) == list:
                self.view(step + 1, cate)
            else:
                print('  ' * step + '- ' + cate)
                

    def is_category_valid(self, tar, L = []):
        if L == []:
            L = self._categories
        for cate in L:
            if type(cate) == list:
                if self.is_category_valid(tar, cate):
                    return True
            else:
                if cate == tar:
                    return True
        return False

    def find_subcategories(self, tar, L = []):
        def _flatten(L):
            if type(L) == list:
                result = []
                for child in L:
                    result.extend(_flatten(child))
                return result
            else:
                return [L]

        if L == []:
            L = self._categories
        if type(L) == list:
            for v in L:
                p = self.find_subcategories(tar, v)
                if p == True:
                    # if found, return the flatten list including itself
                    # and its subcategories
                    index = L.index(v)
                    return _flatten(L[index:index + 2])
                if p != False:
                # p is a list returned from flatten
                    return p
        return L == tar

# add function
def add(money, records):
    try:
        desc, amt = input('Add an expense or income record with description and amount:\n').split(' ')
        # judge whether it is valid input
        amt = int(amt)
    except ValueError:
        sys.stderr.write('Invalid input.\nFail to add a record.\n')
        return money, records
    # create tuple and append it to the end of records
    records.append(tuple([desc, int(amt)]))
    # money update
    money += amt
    return money, records

# view function
def view(money, records):
    pos_size = []
    pos_label = []
    neg_size = []
    neg_label = []
    print('Here\'s your expense and income records:')
    print('Description          Amount')
    print('---------------------------')
    for record in records:
        desc, amt = record
        if amt > 0:
            pos_size.append(amt)
            pos_label.append(desc)
        elif amt < 0:
            neg_size.append(-amt)
            neg_label.append(desc)
        print('%-20s %-6d' % (desc, amt))
    print('---------------------------')
    print('Now you have', money, 'dollars.')

    # draw pie chart
    if (len(pos_size) > 0):
        plt.title("Income records")
        plt.pie(pos_size, labels = pos_label ,autopct='%1.1f%%')
        plt.axis('equal')
        plt.show()

    if (len(neg_size) > 0):
        plt.title("Expenditure records")
        plt.pie(neg_size, labels = neg_label ,autopct='%1.1f%%')
        plt.axis('equal')
        plt.show()

# delete function
def delete(money, records):
    description = input('Can you descripe which record you want to delete?\n')
    for record in records:
        desc, amt = record
        if description in desc:
            print('Do you want to delete the following record?(y/n)')
            print('Description:', desc)
            print('Amount:', amt)
            answer = input()
            if answer == 'y' or answer == 'Y':
                # delete the record
                records.remove(record)
                # money update
                money -= int(amt)
                print('Delete successfully.')
                return money, records
    # if didn't match, tell the user.
    print('Can\'t find more related record.')
    return money, records

# write records to file
def write_file(money, records):
    with open('records.txt', 'w+') as f:
        f.write(str(money) + '\n')
        buffer = []
        for record in records:
            buffer.append(str(record[0]) + ' ' + str(record[1]))
        f.writelines('\n'.join(buffer))
    sys.stderr.write('Exit successfully.')

# main function
if __name__ == '__main__':
    categories = Categories()
    records = Records()
    while True:
        command = input('\nWhat do you want to do (add / ...)? ')
        if command == 'add':
            record = input('Add an expense or income record with ...:\n')
            records.add(record, categories)
        elif command == 'view':
            records.view()
        elif command == 'delete':
            delete_record = input("Which record do you want to delete? ")
            records.delete(delete_record)
        elif command == 'view categories':
            categories.view()
        elif command == 'find':
            category = input('Which category do you want to find? ')
            target_categories = categories.find_subcategories(category)
            records.find(target_categories)
        elif command == 'exit':
            records.save()
            break
        else:
            sys.stderr.write('Invalid command. Try again.\n')
