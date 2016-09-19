__author__ = 'hvreenen'

class List(list):
    def __init__(self, *args):
        for arg in args:
            self.append(arg)

    def find(self, name):
        for item in self:
            if item.name == name:
                return item

    def index(self, name):
        index = 0
        for item in self:
            if item.name == name:
                return index
            index += 1

class Project:
    def __init__(self, name):
        self.name = name
        self.tasks = List()
        self.default_task = None

class Task:
    def __init__(self, name):
        self.name = name