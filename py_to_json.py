import json
from encryption_functions import Clyde_encrypt

class JSON_handler:
    def __init__(self, file):
        self.file_name = file
        self.file = json.load(file)

    def check(self, name, password):
        if name in self.file.keys():
            return self.file[name] == Clyde_encrypt(password)
        else:
            self.update(name, password)
            return True

    def update(self, name, password):
        self.file[name] = Clyde_encrypt(password)

