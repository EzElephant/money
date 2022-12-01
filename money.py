import sys
import matplotlib.pyplot as plt

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

def init():
    records = []
    try:
        # Use with open. In the end, the file will close automatically.
        with open('records.txt', 'r') as f:
            buffer = f.readline()
            # if empty string means that it is the first time to open program
            if (buffer == ''):
                raise FileNotFoundError
            money = int(buffer)
            for tmp in f.readlines():
                desc, amt = tmp.split(' ')
                records.append(tuple([desc, int(amt)]))
            print('Welcome back!')
    # if the file has wrong format tell the user
    except ValueError:
        sys.stderr.write('Invalid format in records.txt.\n')
        money = ask_money()
    except FileNotFoundError:
        money = ask_money()
    return money, records


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
    # enter initial money
    money, records = init()

    # command
    while True:
        op = input('What do you want to do (add / view / delete / exit)? ')
        if (op == 'add'):
            money, records = add(money, records)
        elif (op == 'view'):
            view(money, records)
        elif (op == 'delete'):
            money, records = delete(money, records)
        elif (op == 'exit'):
            write_file(money, records);
            break
        else:
            print('Please enter valid command.')
