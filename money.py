import sys
import matplotlib.pyplot as plt

class Date:
    """Represent a date."""
    def __init__(self, month, day):
        """Constructor for Date."""
        if month < 1 or month > 12:
            raise ValueError
        self._month = month
        if day < 0:
            raise ValueError
        if day > 29 and month in [2]:
            raise ValueError
        if day > 30 and month in [4, 6, 9, 11]:
            raise ValueError
        if day > 31:
            raise ValueError
        self._day = day

    def __repr__(self):
        return f'{self._month:02d}/{self._day:02d}'

    def __int__(self):
        """Convert Date to int."""
        # Use for sort.
        return self._month * 31 + self._day

    #getter method
    @property
    def month(self):
        """property for _month"""
        return self._month
    @property
    def day(self):
        """property for _day"""
        return self._day

class Record:
    """Represent a record."""
    # constructor
    def __init__(self, L):
        """Constructor for Record. """
        if len(L) != 5:
            self.exist = False
            sys.stderr.write('Invalid format for record.\n')
            return
        try:
            self.exist = True
            self._cate = L[2]
            self._desc = L[3]
            self._date = Date(int(L[0]), int(L[1]))
            self._amount = int(L[4])
        except ValueError:
            print('Invalid input.')
            self.exist = False

    def __repr__(self):
        """repr for Record."""
        return f'{self._date}  {self._cate:15s} {self._desc:20s} {self._amount}'

    # getter methods
    @property
    def cate(self):
        """property for _cate"""
        return self._cate
    @property
    def desc(self):
        """property for _desc"""
        return self._desc
    @property
    def amount(self):
        """property for _amount"""
        return self._amount
    @property
    def date(self):
        """property for _date"""
        return self._date

class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self):
        """Constructor for Records."""
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
                    new_record = Record(tmp.split(' '))
                    if new_record.exist:
                        self._records.append(new_record)
                    else:
                        raise ValueError
                print('Welcome back!')
        # if the file has wrong format tell the user
        except ValueError:
            sys.stderr.write('Invalid format in records.txt.\n')
            self._money = self.ask_money()
        except FileNotFoundError:
            self._money = self.ask_money()
        self._records.sort(key = lambda x: int(x.date))

    @staticmethod
    def ask_money():
        """Ask how much money does the user have. Return an interger."""
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
        """Add a Record to Records."""
        if categories.is_category_valid(record.cate):
            self._records.append(record)
            self._money += int(record.amount)
        else:
            sys.stderr.write('Invalid input.\nFail to add a record.\n')
        self._records.sort(key = lambda x: int(x.date))

    def view(self):
        """View the Records."""
        pos_size = []
        pos_label = []
        neg_size = []
        neg_label = []
        list_x = []
        list_y = []
        x_label = []
        money_change = 0
        print('Here\'s your expense and income records:')
        print('Date   Category        Description          Amount')
        print('--------------------------------------------------')
        for record in self._records:
            print(record)
            money_change += int(record.amount)
            if len(list_x) > 0 and int(record.date) == list_x[-1]:
                list_y[-1] = money_change
            else:
                list_x.append(int(record.date))
                list_y.append(money_change)
                x_label.append(record.date)
            if record.amount > 0:
                pos_size.append(record.amount)
                pos_label.append(record.desc)
            elif record.amount < 0:
                neg_size.append(-record.amount)
                neg_label.append(record.desc)
        print('--------------------------------------------------')
        print('Now you have', self._money, 'dollars.')

        # draw pie chart
        see_pie = input('Do you want to see pie chart? (y/n) ')
        if see_pie in ['y', 'Y']:
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
        
        see_plot = input('Do you want to see plot? (y/n) ')
        if see_plot in ['y', 'Y']:
            plt.title("Chart for money change")
            plt.ylabel('Money change')
            plt.xlabel('Date')
            plt.plot(range(len(list_x)), list_y, color='red', markersize="16", marker=".")
            plt.xticks(range(len(list_x)), x_label)
            plt.show()

    def delete(self, description):
        """Delete record in Records."""
        for record in self._records:
            if description in record.desc:
                print('Do you want to delete the following record?(y/n)')
                print('Date   Category        Description          Amount')
                print('--------------------------------------------------')
                print(record)
                answer = input()
                if answer == 'y' or answer == 'Y':
                    # delete the record
                    self._records.remove(record)
                    self._money -= int(record.amount)
                    print('Delete successfully.')
        # if didn't match, tell the user.
        print('Can\'t find more related record.')

    def find(self, target_categories):
        """Find particular record according to the category."""
        print('Here\'s your expense and income records:')
        print('Date   Category        Description          Amount')
        print('--------------------------------------------------')
        money = 0
        for record in self._records:
            if record.cate in target_categories:
                print(record)
                money += record.amount
        print('--------------------------------------------------')
        print('Now you have', money, 'dollars.')

    def save(self):
        """Save Records in records.txt."""
        with open('records.txt', 'w+') as f:
            f.write(str(self._money) + '\n')
            buffer = []
            for record in self._records:
                buffer.append(str(record.date.month) + ' ' + str(record.date.day) + ' ' + record.cate + ' ' + record.desc + ' ' + str(record.amount))
            f.writelines('\n'.join(buffer))
        sys.stderr.write('Exit successfully.')

class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self, L):
        """Constructor for Categories"""
        self._categories = L

    def view(self, step = 0, L = []):
        """View the Categories"""
        if L == []:
            L = self._categories
        for cate in L:
            if type(cate) == list:
                self.view(step + 1, cate)
            else:
                print('  ' * step + '- ' + cate)
                

    def is_category_valid(self, tar, L = []):
        """Judge whether category is valid."""
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

    def find_subcategories(self, tar):
        """Return the subcategories for tar."""
        def find_subcategories_gen(tar, categories, Found = False):
            """Generator to find subcategories."""
            if type(categories) == list:
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(tar, child, Found)
                    if child == tar and index + 1 < len(categories) and type(categories[index + 1]) == list:
                        yield from find_subcategories_gen(tar, categories[index + 1], True)
            else:
                if categories == category or Found:
                    yield categories
        return [i for i in find_subcategories_gen(tar, self._categories)]

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
            if len(target_categories) == 0:
                print('Can\'t find such category.')
            else:
                records.find(target_categories)
        elif command == 'exit':
            records.save()
            break
        else:
            sys.stderr.write('Invalid command. Try again.\n')
