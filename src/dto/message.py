from datetime import datetime


def formatted_time_from_unix_time(unix_time, robust=False):
    date_format = "%B %d, %Y %H:%M:%S" if robust else "%y %b %d %H:%M:%S"
    return datetime.utcfromtimestamp(int(unix_time)).strftime(date_format)


class Message:
    message_id = ''
    message_text = ''
    message_poster = ''
    message_posted_at = ''

    def get_messages(self, data):
        pass

    def get_message(self, data):
        pass


class DynamoMessage(Message):
    def get_messages(self, data):
        messages = []
        for datum in data:
            message = Message()
            message.message_id = datum['messageUID']
            message.message_text = datum['message']
            message.message_poster = datum['poster']
            message.message_posted_at = f"{datum['messageDate']} {datum['messageTime'].split('.')[0]}"
            messages.append(message)

        return messages

    def get_message(self, data):
        message = Message()
        message.message_id = ''
        message.message_text = data['message']
        message.message_poster = data['poster']
        message.message_posted_at = f"{data['messageDate']} {data['messageTime'].split('.')[0]}"

        return message


class SqliteMessage(Message):
    def get_messages(self, data):
        response = []
        for item in data:
            message = Message()
            message.message_id = item[0]
            message.message_text = item[1]
            message.message_poster = item[2]
            message.message_posted_at = formatted_time_from_unix_time(item[3])
            response.append(message)

        return response

    def get_message(self, data):
        message = Message()
        message.message_text = data[0]
        message.message_poster = data[1]
        message.message_posted_at = formatted_time_from_unix_time(data[2], robust=True)

        return message
