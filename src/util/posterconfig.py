import os

class PosterConfig:
    filename = ".msgconfig"

    def is_poster_configured(self):
        return os.path.isfile(self.filename)

    def load_poster_from_config(self):
        with open(self.filename, "r") as config:
            return config.read().split(",")

    def create_config_file(self):
        with open(self.filename, "w") as config:
            poster = input("Enter your username: ")
            number_of_messages = input("Enter the number of messages to display: ")
            config.write(f"{poster},{number_of_messages}")
            return poster, number_of_messages

    def get_config_values(self):
        if self.is_poster_configured():
            return self.load_poster_from_config()
        else:
            return self.create_config_file()
