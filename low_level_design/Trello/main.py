'''
classes:
- user
- project
- tasks
- project_manager
'''

class User:
    def __init__(self, id):
        self.id = id

# use factory pattern for bug, task, documentation, ....
# use builder design pattern to create tasks with different argument types
class Task:
    def __init__(self, task_id):
        self.task_id = task_id
        self.assignee = None
        self.description = None
    def __str__(self):
        return str(self.task_id)

class Project:
    def __init__(self, project_id):
        self.project_id = project_id
        self.tasks = set()

    def add_task(self, task):
        self.tasks.add(task)

    def __str__(self):
        all_tasks = ''
        for task in self.tasks:
            all_tasks += str(task)
        return all_tasks

class ProjectManager:
    def __new__(cls):
        if(not hasattr(ProjectManager, '_instance')):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.projects = []

    def add_project(self, project):
        self.projects.append(project)

    def show_projects(self):
        for project in self.projects:
            print(project)

project_1 = Project(1)
task_1 = Task(1)

project_1.add_task(task_1)

projectManager = ProjectManager()
projectManager.add_project(project_1)
projectManager.show_projects()


