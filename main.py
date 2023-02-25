#!/usr/bin/python
from datetime import datetime

import dao.sqlitedao as dao
import os.path
import textwrap


def pad_right(text, number_of_spaces):
    return text + " " * (number_of_spaces - len(text))


def formatted_time_from_unix_time(unix_time, robust=False):
    date_format = "%B %d, %Y %H:%M:%S" if robust else "%y %b %d %H:%M:%S"
    return datetime.utcfromtimestamp(unix_time).strftime(date_format)


def print_messages(number_of_messages, print_all=False):
    messages = dao.get_messages(number_of_messages, print_all)
    for message in messages:
        print(f"{message['messageuid']} "
              f"{pad_right(message['message'], 39)} "
              f"{pad_right(message['poster'], 12)} "
              f"{formatted_time_from_unix_time(message['postedat'])}")


def print_message(message_id):
    msg = dao.get_message(message_id)
    if len(msg) == 0:
        print("No message matched the message id")
    else:
        print(textwrap.fill(msg['message'], 80))
        print(f"{msg['poster']} {formatted_time_from_unix_time(msg['postedat'], robust=True)}")


def is_poster_configured():
    return os.path.isfile(".msgconfig")


def load_poster_from_config():
    with open(".msgconfig", "r") as config:
        return config.read().split(",")


def create_config_file():
    with open(".msgconfig", "w") as config:
        poster = input("Enter your username: ")
        number_of_messages = input("Enter the number of messages to display: ")
        config.write(f"{poster},{number_of_messages}")
        return poster, number_of_messages


def get_config_values():
    if is_poster_configured():
        return load_poster_from_config()
    else:
        return create_config_file()


def quit_was_selected(command):
    return command == "quit" or command == "exit"


def process_command(command, poster, number_of_messages):
    if command[0] == "read":
        print_message(command[1])
    elif command[0] == "listall":
        print_messages(number_of_messages, print_all=True)
    elif command[0] == "post":
        dao.post_message(command[1], poster)
    elif command[0] == "help":
        print("Commands are:\n listall\n read <message id>\n post <message>\n exit")
    elif command[0] == "delete":
        dao.post_message(f"Hey {poster}, you can't delete messages.", "the admin")
    else:
        print('Invalid command. Type "help" for available commands.')


def main():
    poster, number_of_messages = get_config_values()
    print_messages(number_of_messages)
    while True:
        command_parts = input(">").split(" ", 1)
        if quit_was_selected(command_parts[0]):
            break
        else:
            process_command(command_parts, poster, number_of_messages)


if __name__ == "__main__":
    main()
