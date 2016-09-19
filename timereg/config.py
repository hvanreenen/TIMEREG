from timereg.projects import Project, Task, List

__author__ = 'hvreenen'


project1 = Project('pyelt')
project1.tasks.append(Task('framework'))
project1.tasks.append(Task('unittests'))
project1.tasks.append(Task('domain'))
project1.tasks.append(Task('etl timeff'))
project1.tasks.append(Task('etl anders'))
project1.tasks.append(Task('debuggen'))
project1.default_task = project1.tasks[0]

project2 = Project('_test_proms')
project2.tasks.append(Task('aanpassen/debuggen productie'))
project2.tasks.append(Task('aanpassingen voor pto/prem'))
project2.tasks.append(Task('zonnestraal'))
project2.tasks.append(Task('datamart maken van promsscores'))
project2.tasks.append(Task('soap op python'))
project2.default_task = project2.tasks[0]

project3 = Project('algemeen')
project3.tasks.append(Task('overleg'))
project3.tasks.append(Task('email'))
project3.tasks.append(Task('admin'))
project3.tasks.append(Task('inwerken Rob'))
project3.tasks.append(Task('linux inwerken'))
project3.default_task = project3.tasks[0]



config = {
    'filename': 'C:/Users/hjvreenen/Documents/!uren/Uren.csv',
    'lang': 'en',
    'projects': List(project1, project2, project3),
    'default_project': project1,
    'sort_type': ''
}
