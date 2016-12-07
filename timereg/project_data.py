from timereg.domain import Project, Task, List
projects = []
project = Project('pyelt')
project.tasks.append(Task('framework aanpassen'))
project.tasks.append(Task('fhir domain'))
project.tasks.append(Task('datamart'))
project.tasks.append(Task('vektis agb'))
project.tasks.append(Task('ref data'))
projects.append(project)

project = Project('timereg')
project.tasks.append(Task('refactor'))
projects.append(project)

project = Project('proms')
project.tasks.append(Task('soap koppeling research'))
project.tasks.append(Task('code review'))
project.tasks.append(Task('testen'))
project.tasks.append(Task('conversie naar timeff van orthopedium'))
projects.append(project)

project = Project('algemeen')
project.tasks.append(Task('emails afhandelen'))
project.tasks.append(Task('holocrazy training'))
project.tasks.append(Task('inwerken/overdracht'))
project.tasks.append(Task('overleg'))
project.tasks.append(Task('code review voorbereiden'))
projects.append(project)

