from timereg.domain import Project, Task, List
projects = []
project = Project('pyelt')
project.tasks.append(Task('framework aanpassen'))
project.tasks.append(Task('debuggen'))
project.tasks.append(Task('refactor'))
project.tasks.append(Task('timeff mappings'))
project.tasks.append(Task('proms mappings'))
project.tasks.append(Task('yellowfin'))
projects.append(project)

project = Project('proms')
project.tasks.append(Task('aanpassingen'))
project.tasks.append(Task('debuggen'))
project.tasks.append(Task('soap koppeling research'))
project.tasks.append(Task('ad hoc vragen'))
projects.append(project)

project = Project('algemeen')
project.tasks.append(Task('emails afhandelen'))
project.tasks.append(Task('holocrazy training'))
project.tasks.append(Task('inwerken/overdracht'))
project.tasks.append(Task('code review'))
project.tasks.append(Task('overleg'))
project.tasks.append(Task('admin dingen'))
projects.append(project)

