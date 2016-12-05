import csv
import datetime
from collections import OrderedDict

from timereg import config
from timereg.domain import Project, Task, List, TimeEntry
from timereg.helpers import Formatter
from timereg.languages import translate
from timereg.project_data import projects

__author__ = 'hvreenen'


class TimeRegApp:
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
        self.projects = List(projects)
        self.config = config.config

    def run(self):
        self.load_data()
        if self.last_entry and not self.last_entry.end_time:
            #register end time
            self.register_end_time()
            self.save_data()

            response = input('Start another time registry or report? [Y/N|R]')
            if response.lower() == 'r':
                return self.report()
            if response and response.lower() == 'n':
                return
            elif response and (response.lower() == 'y' or response.lower() == 'Y'):
                self.register_start_time()
                self.save_data()
        else:
            self.register_start_time()
            self.save_data()

    def register_start_time(self):
        new_entry = TimeEntry()
        new_entry.start_time = datetime.datetime.now()
        if self.last_entry:
            # zet default project en taak op laatste project en taak
            new_entry.project = self.last_entry.project
            new_entry.task = self.last_entry.task
        self.entries.append(new_entry)

        new_entry.start_time = self.ask_for_start_time(new_entry.start_time)
        new_entry.project = self.ask_for_project(new_entry.project)
        new_entry.task = self.ask_for_task(new_entry.project, new_entry.task)
        self.last_entry = new_entry

    def register_end_time(self):
        time_entry = self.last_entry
        default_end_time = datetime.datetime.now()
        if time_entry.date < datetime.datetime.now().date():
            self.print('You forgot to registry the end time the other day.')
            default_end_time = default_end_time.replace(year=default_end_time.date.year, month=default_end_time.date.month, day=default_end_time.date.day)

        time_entry.end_time = self.ask_for_end_time(time_entry,default_end_time)
        self.print_stats(time_entry)
        time_entry.project = self.ask_for_project(time_entry.project)
        time_entry.task = self.ask_for_task(time_entry.project, time_entry.task)
        time_entry.productivity_perc = self.ask_for_productivity(time_entry.productivity_perc)
        time_entry.rating = self.ask_for_rating(time_entry.rating)
        time_entry.location = self.ask_for_location(time_entry.location)

    def print(self, msg):
        print(msg)
        
    @property
    def current_week(self):
        return '{}-{}'.format(datetime.date.today().isocalendar()[0], datetime.date.today().isocalendar()[1])

    def load_data(self):
        """
        laden van de uren. De uren staan in een csv bestand.
        begintijd;eindtijd;uren;project;taak;
        Het pas staat in de config
        """
        filename = self.config['filename']
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar="'", quoting=csv.QUOTE_MINIMAL)

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
                
                self.entries.append(entry)
                self.last_entry = entry

    def save_data(self):
        filename = self.config['filename']
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quotechar="'", quoting=csv.QUOTE_MINIMAL)
            for entry in self.entries:
                row = []
               
                writer.writerow([entry.month, entry.week, Formatter.format_date(entry.date), Formatter.format_time(entry.start_time), Formatter.format_time(entry.end_time), entry.duration, entry.project.name, entry.task.name,
                                 entry.productivity_perc, entry.rating, entry.location])

        def save_project_data():
            filename = 'project_data.py'
            with open(filename, 'w', newline='', encoding='utf-8') as py_file:
                py_file.write("""from timereg.domain import Project, Task, List
projects = []
""")

                for proj in self.projects:
                    py_file.write("project = Project('{}')\n".format(proj.name))
                    for task in proj.tasks:
                        py_file.write("project.tasks.append(Task('{}'))\n".format(task.name))
                    py_file.write("projects.append(project)\n\n".format(proj.name))

        save_project_data()

    def report(self):
        if not self.entries:
            self.load_data()
        print('{0:<12}:: {1}'.format('week', 'hours:minutes'))
        total = 0
        for week, duration in self.weeks.items():
            print('{0:<12}:: {1}'.format(week, Formatter.duration_to_time_format(duration)))
            total += duration
        print('================================')
        print('TOTAL       :: {0}'.format(Formatter.duration_to_time_format(total)))
        te_werken = len(self.weeks) * 24
        print('TE WERKEN   :: {0}'.format(Formatter.duration_to_time_format(te_werken)))
        print('OVER        :: {0}'.format(Formatter.duration_to_time_format(total - te_werken)))
        print('================================')

        print('{0:<12}:: {1}'.format('day', 'hours:minutes'))

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
        
        for project, duration in projects.items():
            print('{0:<12}:: {1}'.format(project, Formatter.duration_to_time_format(duration)))
            
    def ask_for_start_time(self, default_start_time):
        self.print(translate('START time registry on {0:%Y-%m-%d} at {0:%H.%M}').format(default_start_time))
        msg = 'Confirm/change start time {0:%H:%M} :'.format(default_start_time)
        response = input(msg)
        if response == 'r':
            return  self.time_reg.report()
        if not response:
            return default_start_time
        if ':' in response:
            hour = int(response.split(':')[0])
            minute = int(response.split(':')[1])
            start_time = default_start_time.replace(hour=hour, minute=minute)
        self.print('Worked today: {}, this week: {}'.format(self.hours_today, self.hours_this_week))
        return start_time

    def ask_for_project(self, project):
        msg = 'Choose project:\r\n' + self.get_projects_str()
        if project:
            proj_index = self.projects.index(project.name)
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
            self.projects.append(project)
        return project

    def ask_for_task(self, project, task):
        msg = 'Choose TASK:\r\n' + self.get_tasks_str(project)
        if task:
            task_index = project.tasks.index(task.name)
            if task_index != None:
                msg += 'Current selection: [{} {}]: '.format(task_index + 1, task.name)
            else:
                # msg += 'Current task:  {}: '.format(task.name)
                msg += 'Current task: '.format()
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

    def get_projects_str(self) -> str:
        msg = ''
        index = 1
        for proj in self.projects:
            msg += '{0}: {1}\r\n'.format(index, proj.name)
            index += 1
        return msg

    def get_tasks_str(self, proj):
        msg = ''
        index = 1
        for task in proj.tasks:
            msg += '{0}: {1}\r\n'.format(index, task.name)
            index += 1
        return msg

    def ask_for_end_time(self, time_entry, default_end_time):
        self.print('END time registry, started on {0:%Y-%m-%d} at {0:%H:%M}'.format(time_entry.start_time))
        msg = 'Confirm/change end time {0:%H:%M}:'.format(default_end_time)
        response = input(msg)
        # if not response:
        #     return default_end_time
        if ':' in response:
            hour = int(response.split(':')[0])
            minute = int(response.split(':')[1])
            end_time = default_end_time.replace(hour=hour, minute=minute)
        elif response != '':
            # uren opgegeven
            sec = float(response) * 3600
            end_time = self.start_time + datetime.timedelta(seconds=sec)
        else:
            end_time = default_end_time
        time_entry.end_time = end_time
        self.print('Registered time: {}'.format(Formatter.duration_to_time_format(time_entry.duration)))
        return end_time

    def ask_for_productivity(self, productivity_perc):
        return productivity_perc

    def ask_for_rating(self, rating):
        return rating

    def ask_for_location(self, location):
        return location

    def print_stats(self, time_entry):
        self.days[time_entry.date] += time_entry.duration
        self.weeks[time_entry.week] += time_entry.duration
        hours_today = 0
        hours_this_week = 0
        if datetime.date.today() in self.days:
            hours_today = self.days[datetime.date.today()]
        if self.current_week in self.weeks:
            hours_this_week = self.weeks[self.current_week]
        self.print('Today: {}, this week: {}'.format(Formatter.duration_to_time_format(hours_today),
                                                     Formatter.duration_to_time_format(hours_this_week)))



    


    

# projects = config.config['projects']
#
# p = Project('new')
# i = projects.index(p)
# if p in config.config['projects']:
#     i = config.config['projects'].index(p)
r = TimeRegApp()
r.run()
# r.report()
