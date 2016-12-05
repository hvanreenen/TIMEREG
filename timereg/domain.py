import datetime
__author__ = 'hvreenen'

class List(list):
    def __init__(self, *args):
        if args and isinstance(args[0], list):
            args = args[0]
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

class TimeEntry:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.project = None #Project('')
        self.task = None #Task('')
        self.productivity_perc = None
        self.rating = None
        self.location = None

    @property
    def duration(self) -> float:
        if self.start_time and self.end_time:
            elapsed_time = self.end_time - self.start_time
            sec = elapsed_time.total_seconds()
            hours = sec / 3600
            return round(hours, 2)
        else:
            return 0
    @property
    def date(self):
        if self.start_time:
            return self.start_time.date()

    @property
    def week(self):
        if self.start_time:
            return '{}-{}'.format(self.start_time.isocalendar()[0], self.start_time.isocalendar()[1])
        else:
            return ''

    @property
    def month(self):
        if self.start_time:
            return self.start_time.strftime("%Y-%m")
        else:
            return ''

    @staticmethod
    def from_csv(field_list, time_reg):
        entry = TimeEntry()
        entry.start_time = datetime.datetime.strptime(field_list[3], '%Y-%m-%d %H:%M')

        if field_list[4]:
            entry.end_time = datetime.datetime.strptime(field_list[4], '%Y-%m-%d %H:%M')

        entry.project = time_reg.projects.find(field_list[6])
        if not entry.project:
            entry.project = Project(field_list[6])
        entry.task = entry.project.tasks.find(field_list[7])
        if not entry.task:
            entry.task = Task(field_list[7])
        entry.productivity_perc = field_list[8]
        entry.rating = field_list[9]
        entry.location = field_list[10]
        return entry
