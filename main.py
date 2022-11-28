#!/usr/bin/python
import textwrap
import dao.messagedao as dao

POSTER = ""


def pad_right(text, number_of_spaces):
    return text + " " * (number_of_spaces - len(text))


def get_formatted_time(unformatted_time):
    return unformatted_time.strftime("%y %b %d %H:%M:%S")


def print_messages(print_all=False):
    messages = dao.get_messages(print_all)
    for message in messages:
        print(f"{message[0]} {pad_right(message[1], 39)} {pad_right(message[2], 12)} {get_formatted_time(message[3])}")


def print_message(message_id):
    msg = dao.get_message(message_id)
    print(textwrap.fill(msg[0][0], 80))
    print(f"{msg[0][1]} {get_formatted_time(msg[0][2])}")


def main():
    print_messages()
    while True:
        full_command = input(">")
        command = full_command.split(" ", 1)
        if command[0] == "read":
            print_message(command[1])
        elif command[0] == "listall":
            print_messages(print_all=True)
        elif command[0] == "post":
            dao.post_message(command[1], POSTER)
        elif command[0] == "quit":
            break


if __name__ == "__main__":
    main()
