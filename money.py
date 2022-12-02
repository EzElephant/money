import sys
import matplotlib.pyplot as plt

class Record:
    """Represent a record."""
    # constructor
    def __init__(self, L):
        if len(L) != 3:
            self.exist = False
            sys.stderr.write('Invalid format for record')
            return
        self.exist = True
        self._cate = L[0]
        self._desc = L[1]
        try:
            self._amount = int(L[2])
        except ValueError:
            print('Invalid value for cost, please enter an interger.')

    def __repr__(self):
        return '%-15s %-20s %-6d' % (self._cate, self._desc, self._amount)

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

    def add(self, record, categories):
        if categories.is_category_valid(record.cate):
            self._records.append(record)
            self._money += int(record.amount)
        else:
            sys.stderr.write('Invalid input.\nFail to add a record.\n')

    def view(self):
        # pos_size = []
        # pos_label = []
        # neg_size = []
        # neg_label = []
        print('Here\'s your expense and income records:')
        print('Category        Description          Amount')
        print('-------------------------------------------')
        for record in self._records:
            print(record)
        print('-------------------------------------------')
        print('Now you have', self._money, 'dollars.')

        # draw pie chart
        # if (len(pos_size) > 0):
        #     plt.title("Income records")
        #     plt.pie(pos_size, labels = pos_label ,autopct='%1.1f%%')
        #     plt.axis('equal')
        #     plt.show()

        # if (len(neg_size) > 0):
        #     plt.title("Expenditure records")
        #     plt.pie(neg_size, labels = neg_label ,autopct='%1.1f%%')
        #     plt.axis('equal')
        #     plt.show()

    def delete(self, description):
        for record in self._records:
            if description in record.desc:
                print('Do you want to delete the following record?(y/n)')
                print('Category        Description          Amount')
                print('-------------------------------------------')
                print(record)
                answer = input()
                if answer == 'y' or answer == 'Y':
                    # delete the record
                    self.records.remove(record)
                    self._money -= int(record.amount)
                    print('Delete successfully.')
        # if didn't match, tell the user.
        print('Can\'t find more related record.')

    def find(self, target_categories):
        for record in self._records:
            print('Here\'s your expense and income records:')
            print('Category        Description          Amount')
            print('-------------------------------------------')
            money = 0
            if record.cate in target_categories:
                print(record)
                money += record.amount
            print('-------------------------------------------')
            print('Now you have', money, 'dollars.')

    def save(self):
        with open('records.txt', 'w+') as f:
            f.write(str(self._money) + '\n')
            buffer = []
            for record in self._records:
                buffer.append(str(record.cate) + ' ' + str(record.desc) + ' ' + str(record.amount))
            f.writelines('\n'.join(buffer))
        sys.stderr.write('Exit successfully.')

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

# main function
if __name__ == '__main__':
    categories = Categories(['expense', ['food', ['meal', 'snack', 'drink'], 'transportation',['bus', 'railway']], 'income', ['salary', 'bonus']])
    records = Records()
    while True:
        command = input('What do you want to do  (add / view / delete / view categories / find / exit)? ')
        if command == 'add':
            record = Record(input('Add an expense or income record with category, description, and cost (separate by spaces):\n').split(' '))
            if record.exist:
                records.add(record, categories)
        elif command == 'view':
            records.view()
        elif command == 'delete':
            description = input('Can you descripe which record you want to delete?\n')
            records.delete(description)
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
