from bs4 import BeautifulSoup
from copy import copy
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))



class Html_handler:
    def __init__(self, file):
        self.file = BeautifulSoup(file, "html.parser")
        self.positions = list(
            map(lambda x: int(x.string[:-2]), self.file.find_all(class_="position"))
        )
        self.usernames = list(
            map(lambda x: x.string, self.file.find_all(class_="username"))
        )
        self.points = list(map(lambda x: x.string, self.file.find_all(class_="points")))
        self.new_user = copy(self.file.body.table.find("tr", class_="data"))

    def update(self, score, name):
        if name in self.usernames:
            og_score = self.file.find(
                class_="username", string=name
            ).find_next_sibling().string
            if int(og_score) < score:
                og_score.replace_with(str(score))
        else:
            self.create_user(score, name)
        self.update_pos(name)

    def create_user(self, score, name):
        self.new_user.find(class_="position").string.replace_with(
            f"{len(self.usernames)+1}th"
        )
        self.new_user.find(class_="username").string.replace_with(name)
        self.new_user.find(class_="points").string.replace_with(str(score))
        self.file.body.table.append(self.new_user)

    def update_pos(self, name):

        # defining relative elements
        previous_row = (
            self.file.body.table.find("td", class_="username", string=name)
            .find_parent()
            .find_previous_sibling()
        )
        current_row = self.file.body.table.find(
            "td", class_="username", string=name
        ).find_parent()
        next_row = (
            self.file.body.table.find("td", class_="username", string=name)
            .find_parent()
            .find_next_sibling()
        )

        # checking for score with neighbouring elements
        if previous_row.find(class_="points") and int(
            current_row.find(class_="points").string
        ) > int(previous_row.find(class_="points").string):
            prev_pos = int(previous_row.find(class_="position").string[:-2]) + 1
            curr_pos = int(current_row.find(class_="position").string[:-2]) - 1
            previous_row.find(class_="position").string.replace_with(
                str(prev_pos) + self.match_th(prev_pos)
            )
            current_row.find(class_="position").string.replace_with(
                str(curr_pos) + self.match_th(curr_pos)
            )
            previous_row.insert_before(current_row)
            return self.update_pos(name)
        elif next_row and next_row.find(class_="points") and int(
            current_row.find(class_="points").string
        ) < int(next_row.find(class_="points").string):
            next_pos = int(next_row.find(class_="position").string[:-2]) - 1
            curr_pos = int(current_row.find(class_="position").string[:-2]) + 1
            next_row.find(class_="position").string.replace_with(
                str(next_pos) + self.match_th(next_pos)
            )
            current_row.find(class_="position").string.replace_with(
                str(curr_pos) + self.match_th(curr_pos)
            )
            next_row.insert_after(current_row)
            return self.update_pos(name)

    def match_th(self, number):
        match number:
            case 1:
                return "st"
            case 2:
                return "nd"
            case 3:
                return "rd"
            case _:
                return "th"
    
    def information(self):
        self.usernames = list(
            map(lambda x: x.string, self.file.find_all(class_="username"))
        )