import textwrap


def pad_right(text, number_of_spaces):
    return text + " " * (number_of_spaces - len(text))


class MessagePrinter:
    def __init__(self, dao):
        self.dao = dao

    def print_messages(self, number_of_messages, print_all=False):
        messages = self.dao.get_messages(number_of_messages, print_all)
        for message in messages:
            print(f"{message.message_id} "
                  f"{pad_right(message.message_text, 39)} "
                  f"{pad_right(message.message_poster, 12)} "
                  f"{message.message_posted_at}")

    def print_message(self, message_id):
        msg = self.dao.get_message(message_id)
        if msg is None:
            print("No message matched the message id")
        else:
            print(textwrap.fill(msg.message_text, 80))
            print(f"{msg.message_poster} {msg.message_posted_at}")
