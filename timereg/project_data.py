from timereg.projects import Project, Task, List

projects = []

project = Project('pyelt')
project.tasks.append(Task('framework'))
project.tasks.append(Task('unittests'))
project.tasks.append(Task('domain'))
project.tasks.append(Task('etl timeff'))
project.tasks.append(Task('etl anders'))
project.tasks.append(Task('debuggen'))
projects.append(project)

project = Project('_test_proms')
project.tasks.append(Task('aanpassen/debuggen productie'))
project.tasks.append(Task('aanpassingen voor pto/prem'))
project.tasks.append(Task('zonnestraal'))
project.tasks.append(Task('datamart maken van promsscores'))
project.tasks.append(Task('soap op python'))
projects.append(project)

project = Project('algemeen')
project.tasks.append(Task('overleg'))
project.tasks.append(Task('email'))
project.tasks.append(Task('admin'))
project.tasks.append(Task('inwerken Rob'))
project.tasks.append(Task('linux inwerken'))
projects.append(project)

