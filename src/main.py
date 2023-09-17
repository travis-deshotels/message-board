#!/usr/bin/python
import dao.sqlitedao as dao
from util.posterconfig import PosterConfig
from util.messageprinter import MessagePrinter

message_printer = MessagePrinter(dao)

def quit_was_selected(command):
    return command == "quit" or command == "exit"


def process_command(command, poster, number_of_messages):
    if command[0] == "read":
        message_printer.print_message(command[1])
    elif command[0] == "listall":
        message_printer.print_messages(number_of_messages, print_all=True)
    elif command[0] == "post":
        dao.post_message(command[1], poster)
    elif command[0] == "help":
        print("Commands are:\n listall\n read <message id>\n post <message>\n exit")
    elif command[0] == "delete":
        dao.post_message(f"Hey {poster}, you can't delete messages.", "the admin")
    else:
        print('Invalid command. Type "help" for available commands.')


def main():
    poster, number_of_messages = PosterConfig().get_config_values()
    message_printer.print_messages(number_of_messages)
    while True:
        command_parts = input(">").split(" ", 1)
        if quit_was_selected(command_parts[0]):
            break
        else:
            process_command(command_parts, poster, number_of_messages)


if __name__ == "__main__":
    main()
