from spy_details import spy, Spy, ChatMessage, friends
#getting Spy Details from spy_details.py file
from steganography.steganography import Steganography
#importing Steganography
from termcolor import colored, cprint
#import termcolor for terminal color

STATUS_MESSAGES = ['My name is Bond, James Bond', 'Hey there, I am using Spy Chat', 'Available']

print 'Hello! Let\'s get started'

question = 'Do you want to continue as ' + spy.salutation + ' ' + spy.name + ' (Y/N)? '
existing = raw_input(question)

def add_status():

    updated_status_message = None

    if spy.current_status_message != None:

        print 'Your current status message is %s \n' % (spy.current_status_message)
        default = raw_input('Do you want to select from the older status (y/n)? ')

        if default.upper() == 'N':
            new_status_message = raw_input('What status message do you want to set? ')

            if len(new_status_message) > 0:
                STATUS_MESSAGES.append(new_status_message)
                updated_status_message = new_status_message

        elif default.upper() == 'Y':

            item_position = 1

            for message in STATUS_MESSAGES:
                print '%d- %s' % (item_position, message)
                item_position = item_position + 1

            message_selection = int(raw_input('\nChoose from the above messages '))

            if len(STATUS_MESSAGES) >= message_selection:
                updated_status_message = STATUS_MESSAGES[message_selection - 1]
        else:
            print 'The option you chose is not valid! Press either y or n.'
    else:
        print 'You don\'t have any status message currently \n'

        new_status_message = raw_input('What status message do you want to set? ')


        if len(new_status_message) > 0:
            STATUS_MESSAGES.append(new_status_message)
            updated_status_message = new_status_message


        if updated_status_message:
            print 'Your updated status message is:- %s' % (updated_status_message)
        else:
            print 'You current don\'t have a status update'

        return updated_status_message


def add_friend():

    new_friend = Spy('','',0,0.0)

    try:
        friend_name = raw_input('Please add your friend\'s name: ')
        try:
            if len(friend_name > 0):
                new_friend.name = friend_name
                friend_salutation = raw_input('Are they Mr. or Ms.?: ')
                try:
                    if friend_salutation is 'Mr.' or 'Ms.' or 'Dr.' or 'Kr. ' or 'Er. ':
                        new_friend.salutation = friend_salutation
                        new_friend.name = new_friend.salutation + ' ' + new_friend.name
                        friend_age = int(raw_input('Age?'))
                        try:
                            if type(friend_age) is int and 12 < friend_age < 100:
                                new_friend.age = friend_age
                                friend_rating = float(raw_input('Spy rating?'))
                                try:
                                    if type(friend_rating) is float and 0 < friend_rating <= 5:
                                        new_friend.rating = friend_rating
                                except Exception:
                                    print 'Error: Enter correct rating of friend'
                        except Exception:
                            print 'Error: Enter correct age of friend'
                except Exception:
                    print 'Error: Enter correct salutation of friend'
        except Exception:
            print 'Error: Enter correct name of friend'
    except Exception:
        print 'Error valid details of friend'

    if len(new_friend.name) > 0 and new_friend.age > 12 and new_friend.rating >= spy.rating:
        friends.append(new_friend)
        print 'Friend Added!'
    else:
        print 'Sorry! Invalid entry. We can\'t add spy with the details you provided'

    return len(friends)


def select_a_friend():
    item_number = 0

    for friend in friends:
        print '%d. %s %s aged %d with rating %.2f is online' % (item_number +1, friend.salutation, friend.name,
                                                   friend.age,
                                                   friend.rating)
        item_number = item_number + 1

    friend_choice = raw_input('Choose from your friends')

    friend_choice_position = int(friend_choice) - 1

    return friend_choice_position


def send_message():

    friend_choice = select_a_friend()

    original_image = raw_input('What is the name of the image?')
    output_path = 'output.jpg'
    text = raw_input('What do you want to say? ')
    Steganography.encode(original_image, output_path, text)
    new_chat = ChatMessage(text,True)
    friends[friend_choice].chats.append(new_chat)

    #node =1
    #show = ''
    #while node <= len(friends[friend_choice].chats):
        #show =  friends[friend_choice].chats
        #node = node+1
    #print show
    #print len(friends[friend_choice].chats)

    print 'Your secret message image is ready!'


def read_message():

    sender = select_a_friend()

    output_path = raw_input('What is the name of the file?')

    secret_text = Steganography.decode(output_path)

    if len(secret_text) > 0:
        if secret_text == 'SOS' or secret_text == 'Emergency' or secret_text == 'Save Me'\
                or secret_text == 'In Trouble':
            print colored('Help Required', 'red')

        new_chat = ChatMessage(secret_text,False)

        friends[sender].chats.append(new_chat)

        print 'Your secret message has been saved!'


def read_chat_history():

    read_for = select_a_friend()

    print '\n6'

    for chat in friends[read_for].chats:
        if chat.sent_by_me:
            print ('[%s] %s: %s' % (colored(chat.time.strftime('%d %B %Y'), 'blue'),
                                                colored('Me:', 'red'), chat.message))
        else:
            print '[%s] %s said: %s' % (colored(chat.time.strftime('%d %B %Y'), 'red'),
                                        colored(friends[read_for].name, 'blue'), chat.message)


def start_chat(spy):

    spy.name = spy.salutation + ' ' + spy.name


    if 12 < spy.age < 50:


        print 'Authentication complete. Welcome ' + spy.name + ' age: ' \
              + str(spy.age) + ' and rating of: ' + str(spy.rating) + ' Proud to have you onboard'

        show_menu = True

        while show_menu:
            menu_choices = 'What do you want to do? \n 1. Add a status update \n 2. Add a friend \n'\
                                ' 3. Send a secret message \n 4. Read a secret message \n' \
                                ' 5. Read Chats from a user \n 6. Close Application \n'
            menu_choice = raw_input(menu_choices)

            if len(menu_choice) > 0:
                menu_choice = int(menu_choice)

                if menu_choice == 1:
                    spy.current_status_message = add_status()
                elif menu_choice == 2:
                    number_of_friends = add_friend()
                    print 'You have %d friends' % (number_of_friends)
                elif menu_choice == 3:
                    send_message()
                elif menu_choice == 4:
                    read_message()
                elif menu_choice == 5:
                    read_chat_history()
                else:
                    show_menu = False
            else:
                print 'Sorry you are not of the correct age to be a spy'

if existing.upper() == 'Y':
    start_chat(spy)
else:

    spy = Spy('','',0,0.0)

    try:

        name = raw_input('Welcome to spy chat, you must tell me your spy name first: ')
        try:
            if len(name) > 0:
                spy.name = name
                salutation = str(raw_input('Should I call you Mr. or Ms.?: '))
                try:
                    if salutation is 'Mr.' or 'Ms.' or 'Er.' or 'Dr.' or 'Kr.':
                        spy.salutation = salutation
                        age = int(raw_input('What is your age?'))
                        try:
                            if 12 <= age < 100 and type(age) is int:
                                spy.age = age
                                rating = float(raw_input('What is your spy rating?'))
                                try:
                                    if 0 < rating <= 5 and type(rating) is float:
                                        spy.rating = rating
                                except Exception:
                                    print 'Error: Enter correct rating of spy'
                        except Exception:
                            print 'Error: Enter correct age of spy'
                except Exception:
                    print 'Error: Enter correct salutation of spy'
        except Exception:
            print 'Error: Enter correct name of spy'

    except Exception:
        print 'Error: Enter valid details of spy'

    start_chat(spy)