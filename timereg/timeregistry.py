import datetime
import csv
from collections import OrderedDict

from timereg import config
from timereg.languages import translate
from timereg.project_data import projects
from timereg.projects import Project, Task

__author__ = 'hvreenen'


class TimeReg:
    def __init__(self):
        """
        Tijd registratie tool. Deze class is de hoofd ingang . Het bevat alle time entries

        """
        self.entries = []
        self.weeks = OrderedDict()
        self.months = OrderedDict()
        self.days = OrderedDict()
        self.last_entry = None
        self.config = config.config
        self.hours_today = 0
        self.hours_this_week = 0
        self.project_data = projects

    @property
    def current_week(self):
        return '{}-{}'.format(datetime.date.today().isocalendar()[0], datetime.date.today().isocalendar()[1])

    def load(self):
        """
        laden van de uren. De uren staan in een csv bestand.
        begintijd;eindtijd;uren;project;taak;
        Het pas staat in de config
        """
        filename = self.config['filename']
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar="'", quoting=csv.QUOTE_MINIMAL)
            # day = datetime.date(2000, 1, 1)
            # week = '2000-01'
            # total_day_hours = 0
            # total_week_hours = 0
            for row in reader:
                entry = TimeEntry.from_csv(row, self)
                if entry.week not in self.weeks:
                    self.weeks[entry.week] = entry.duration
                else:
                    self.weeks[entry.week] += entry.duration
                if entry.date not in self.days:
                    self.days[entry.date] = entry.duration
                else:
                    self.days[entry.date] += entry.duration
                # if day != entry.date:
                #     total_day_hours = 0
                #     day = entry.date
                # if week != entry.week:
                #     total_week_hours = 0
                #     week = entry.week
                self.entries.append(entry)
                self.last_entry = entry
                # total_day_hours += entry.duration
                # total_week_hours += entry.duration
                # if entry.date == datetime.date.today():
                #     self.hours_today = total_day_hours
                # if entry.week == '{}-{}'.format(datetime.date.today().isocalendar()[0],
                #                                 datetime.date.today().isocalendar()[1]):
                #     self.hours_this_week = total_week_hours

    def save(self):
        filename = self.config['filename']
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quotechar="'", quoting=csv.QUOTE_MINIMAL)
            for entry in self.entries:
                row = []
                # writer.writerow([entry.start_time.strftime("%Y-%m-%d %H:%M") if entry.start_time else '', entry.end_time.strftime("%Y-%m-%d %H:%M") if entry.end_time else ''
                #                     , entry.duration, entry.project.name, entry.task.name,
                #                  entry.productivity_perc, entry.rating, entry.location])
                writer.writerow([entry.month, entry.week, entry.date_str, entry.start_time_str, entry.end_time_str, entry.duration, entry.project.name, entry.task.name,
                                 entry.productivity_perc, entry.rating, entry.location])

        proj_filename = 'C:/!Ontwikkel/CLINICS-DWH2.0/timereg/project_data.py'
        with open(proj_filename, 'w', newline='\r\n', encoding='utf-8') as proj_data_file:
            proj_data_file.write("""from timereg.projects import Project, Task, List\n\n""")
            proj_data_file.write("""projects = []\n\n""")
            for proj in self.project_data:
                proj_data_file.write("""project = Project('{}')\n""".format(proj.name))
                for task in proj.tasks:
                    proj_data_file.write("""project.tasks.append(Task('{}'))\n""".format(task.name))
                proj_data_file.write("""projects.append(project)\n\n""".format(proj.name))



    def run(self):
        self.load()
        if self.last_entry and not self.last_entry.end_time:
            self.last_entry.end()
        else:
            new_entry = TimeEntry(self)
            self.entries.append(new_entry)
            self.last_entry = new_entry
            new_entry.start()
        self.save()

    def duration_to_time_format(self, duration: float) -> str:
        hours = int(duration)
        rest = duration - int(duration)
        minutes = int(60 * rest)
        return '{0:02d}:{1:02d}'.format(hours, minutes)

    def report(self):
        if not self.entries:
            self.load()
        print('{0:<12}:: {1}'.format('week', 'hours:minutes'))
        # print('{0:<12}:: {1}'.format('____', '____________'))
        total = 0
        for week, duration in self.weeks.items():
            print('{0:<12}:: {1}'.format(week, self.duration_to_time_format(duration)))
            total += duration
        print('================================')
        print('TOTAL       :: {0}'.format(self.duration_to_time_format(total)))
        te_werken = len(self.weeks) * 24
        print('TE WERKEN   :: {0}'.format(self.duration_to_time_format(te_werken)))
        print('OVER        :: {0}'.format(self.duration_to_time_format(total - te_werken)))
        print('================================')

        print('{0:<12}:: {1}'.format('day', 'hours:minutes'))
        # print('{0:<12}:: {1}'.format('____', '____________'))
        # total = 0
        # for day, duration in self.days.items():
        #     print('{0:<12}:: {1}'.format(str(day), self.duration_to_time_format(duration)))
        #     total += duration
        # print('TOTAAL      :: {0}'.format(self.duration_to_time_format(total)))

        projects = {}
        for entry in self.entries:
            name = entry.project.name
            if name == 'algemeenxx':
                name += ' - ' + entry.task.name
            if name not in projects:
                projects[name] = entry.duration
            else:
                projects[name] += entry.duration
        print('================================')
        print('{0:<12}:: {1}'.format('project', 'hours:minutes'))
        # print('{0:<12}:: {1}'.format('____', '____________'))
        for project, duration in projects.items():
            print('{0:<12}:: {1}'.format(project, self.duration_to_time_format(duration)))

class TimeEntry:
    def __init__(self, time_reg):
        self.time_reg = time_reg
        self.start_time = None
        self.end_time = None
        self.project = Project('')
        self.task = Task('')
        self.productivity_perc = None
        self.rating = None
        self.location = None
        self.config = config.config


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
    def duration_str(self):
        return self.time_reg.duration_to_time_format(self.duration)

    @property
    def start_time_str(self):
        if self.start_time:
            return self.start_time.strftime("%Y-%m-%d %H:%M")
        else:
            return ''

    @property
    def end_time_str(self):
        if self.end_time:
            return self.end_time.strftime("%Y-%m-%d %H:%M")
        else:
            return ''

    @property
    def date(self):
        if self.start_time:
            return self.start_time.date()

    @property
    def date_str(self):
        if self.start_time:
            return self.start_time.strftime("%Y-%m-%d")
        else:
            return ''

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
        # field_list.insert(0, 0)
        # field_list.insert(0, 0)
        # field_list.insert(0, 0)

        entry = TimeEntry(time_reg)
        #entry.start_time = datetime.datetime.strptime(field_list[0], '%Y-%m-%d %H:%M:%S.%f')
        # entry.date = datetime.datetime.strptime(field_list[3], '%Y-%m-%d %H:%M')
        entry.start_time = datetime.datetime.strptime(field_list[3], '%Y-%m-%d %H:%M')

        if field_list[4]:
            entry.end_time = datetime.datetime.strptime(field_list[4], '%Y-%m-%d %H:%M')

        entry.project = projects.find(field_list[6])
        if not entry.project:
            entry.project = Project(field_list[6])
        entry.task = entry.project.tasks.find(field_list[7])
        if not entry.task:
            entry.task = Task(field_list[7])
        entry.productivity_perc = field_list[8]
        entry.rating = field_list[9]
        entry.location = field_list[10]
        return entry

    def start(self, start_time=datetime.datetime.now()):
        self.start_time = start_time
        self.project = self.config['default_project']

        print(translate('START time registry on {0:%Y-%m-%d} at {0:%H.%M}').format(self.start_time))
        self.start_time = self.ask_for_start_time(self.start_time)
        print('Worked today: {}, this week: {}'.format(self.time_reg.hours_today, self.time_reg.hours_this_week))
        self.project = self.ask_for_project(self.project)
        self.task = self.ask_for_task(self.project, self.project.default_task)

    def end(self):
        self.end_time = datetime.datetime.now()
        if self.date < datetime.datetime.now().date():
            print('You forgot to registry the end time the other day.')
            self.end_time = self.end_time.replace(year=self.date.year, month=self.date.month, day=self.date.day)
        print('END time registry, started on {0:%Y-%m-%d} at {0:%H:%M}'.format(self.start_time))

        self.end_time = self.ask_for_end_time(self.end_time)
        print('Registered time: {}'.format(self.duration_str))
        self.time_reg.days[self.date] += self.duration
        self.time_reg.weeks[self.week] += self.duration
        # self.time_reg.months[self.month] += self.duration
        hours_today = 0
        hours_this_week = 0
        if datetime.date.today() in self.time_reg.days:
            hours_today = self.time_reg.days[datetime.date.today()]
        if self.time_reg.current_week in self.time_reg.weeks:
            hours_this_week = self.time_reg.weeks[self.time_reg.current_week]
        print('Today: {}, this week: {}'.format(self.time_reg.duration_to_time_format(hours_today), self.time_reg.duration_to_time_format(hours_this_week)))
        self.project = self.ask_for_project(self.project)
        self.task = self.ask_for_task(self.project, self.task)
        self.productivity_perc = self.ask_for_productivity(self.productivity_perc)
        self.rating = self.ask_for_rating(self.rating)
        self.location = self.ask_for_location(self.location)
        self.time_reg.save()

        response = input('Start another time registry? [Y/N]')
        if response == 'r':
            return  self.time_reg.report()
        if response and response.lower() == 'n':
            return
        elif response and (response.lower() == 'y' or response.lower() == 'Y'):
            new_entry = TimeEntry(self)
            new_entry.time_reg = self.time_reg
            self.time_reg.entries.append(new_entry)
            self.time_reg.last_entry = new_entry
            new_entry.start(self.end_time)


    def ask_for_start_time(self, start_time):
        msg = 'Confirm/change start time {0:%H:%M} :'.format(start_time)
        response = input(msg)
        if response == 'r':
            return  self.time_reg.report()
        if not response:
            return start_time
        if ':' in response:
            hour = int(response.split(':')[0])
            minute = int(response.split(':')[1])
            start_time = start_time.replace(hour=hour, minute=minute)
        return start_time

    def ask_for_project(self, project):
        msg = 'Choose project:\r\n' + self.get_projects()
        if project:
            proj_index = projects.index(project.name)
            if proj_index != None:
                msg += 'Current selection: [{} {}]: '.format(proj_index + 1, project.name)
            else:
                msg += 'Current project:  {}: '.format(project.name)
        response = input(msg)
        if not response:
            return project
        if response.isdigit():
            proj_index = int(response) - 1
            while proj_index >= len(projects):
                response = input('Invalid number. Please submit new entry')
                if response.isdigit():
                    proj_index = int(response) - 1
                else:
                    proj_index = -1
            project = projects[proj_index]
        elif isinstance(response, str):
            proj_name = response
            project = Project(proj_name)
            self.time_reg.project_data.append(project)
        return project

    def ask_for_task(self, project, task):
        msg = 'Choose TASK:\r\n' + self.get_tasks(project)
        if task:
            task_index = project.tasks.index(task.name)
            if task_index != None:
                msg += 'Current selection: [{} {}]: '.format(task_index + 1, task.name)
            else:
                msg += 'Current task:  {}: '.format(task.name)
        response = input(msg)
        if not response:
            return task
        if response.isdigit():
            task_index = int(response) - 1
            while task_index >= len(project.tasks):
                response = input('Invalid number. Please submit new entry')
                if response.isdigit():
                    task_index = int(response) - 1
                else:
                    task_index = -1
            task = project.tasks[task_index]
        elif isinstance(response, str):
            task_name = response
            task = Task(task_name)
            project.tasks.append(task)
        return task

    def get_projects(self):
        msg = ''
        index = 1
        for proj in self.time_reg.project_data:
            msg += '{0}: {1}\r\n'.format(index, proj.name)
            index += 1
        return msg

    def get_tasks(self, proj):
        msg = ''
        index = 1
        for task in proj.tasks:
            msg += '{0}: {1}\r\n'.format(index, task.name)
            index += 1
        return msg

    def ask_for_end_time(self, end_time):
        msg = 'Confirm/change end time {0:%H:%M}:'.format(end_time)
        response = input(msg)
        if not response:
            return end_time
        if ':' in response:
            hour = int(response.split(':')[0])
            minute = int(response.split(':')[1])
            end_time = end_time.replace(hour=hour, minute=minute)
        else:
            # uren opgegeven
            sec = float(response) * 3600
            end_time = self.start_time + datetime.timedelta(seconds=sec)
        return end_time

    def ask_for_productivity(self, productivity_perc):
        return productivity_perc

    def ask_for_rating(self, rating):
        return rating

    def ask_for_location(self, location):
        return location


projects = config.config['projects']
#
# p = Project('new')
# i = projects.index(p)
# if p in config.config['projects']:
#     i = config.config['projects'].index(p)
r = TimeReg()
r.run()
# r.report()
