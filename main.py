from os import sched_get_priority_min
from app.Tasklist import TaskList

def print_linebreaks():
    print("\n############################\n")


def list_options():

    options = {
            "1": "List all tasks.", 
            "2": "Create a task.", 
            "3": "Select a task.", 
            "4": "Update selected task.", 
            "5": "Delete selected task", 
            "6": "Mark selected task complete.", 
            "7": "Mark selected task incomplete.",
            "8": "Delete all tasks.",
            "9": "List all options", 
            "10": "Quit"
            }
    print_linebreaks()
    print("Welcome to the Task List CLI")
    print("These are the actions you can perform")
    print_linebreaks()
    
    for choice_num in options:
        print(f"Option {choice_num}. {options[choice_num]}")

    print_linebreaks()

    return options

def make_choice(options, task_list):
    valid_choices = options.keys()
    choice = None

    while choice not in valid_choices:
        print("what would you like to do? Select 9 to see all options again.")
        choice = input("Make your selection using the option number: ")
    
    if choice in ['4', '5', '6', '7'] and task_list.selected_task == None:
        print("You must select a task before you can continue with that option.")
        print("Please select a task!")
        choice = "3"
    return choice


def run_cli(play=True):
    task_list = TaskList(url="http://localhost:5000")

    options = list_options()

    while play==True:
        choice = make_choice(options, task_list)

        task_list.print_selected()

        if choice == "1":
            for task in task_list.list_tasks():
                print(task)

        elif choice == "2":
            print("Let's create a new task. ")
            title = input("What is the title of your task?")
            description = input("How would you describe your task? ")
            response = task_list.create_task(title=title, description=description)

            print_linebreaks()
            print("New Task:", response["task"])
        
        elif choice == "3":
            select_by = input("How would you like to search? Enter 'title' or 'ID': ")
            if select_by == "title": 
                title = input("Which task title would you like to select? ")
                task_list.get_task(title=title)
            elif select_by.upper() == "ID": 
                id = input("Which task ID would you like to select? ")
                if id.isnumeric():
                        id = int(id)
                        task_list.get_task(id=id)
            else: 
                print("Could not select. Please enter id or title.")
            
            if task_list.selected_task:
                print_linebreaks()
                print("Selected task: ", task_list.selected_task)
        
        elif choice == "4":
            print(f"Great! Let's update the task:  {task_list.selected_task}")
            title = input("What is the new title of your task? ")
            description = input("How would you describe the task? ")
            response = task_list.update_task(title=title, description=description)

            print_linebreaks()
            print("Updated task:", response["task"])

        elif choice == "5": 
            task_list.delete_task()
            print_linebreaks()
            print("This task has been deleted. ")

        elif choice == "6": 
            response = task_list.mark_complete()

            print_linebreaks()
            print("Completed task: ", response["task"])

        elif choice == "7":
            response = task_list.mark_incomplete()

            print_linebreaks()
            print("Incomplete task:", response["task"])

        elif choice == "8":
            for task in task_list.list_tasks():
                task_list.get_task(id=task["id"])
                task_list.delete_task()

            print_linebreaks()
            print("All tasks have been deleted.")
        
        elif choice == "9":
            list_options()
        
        elif choice == "10":
            play=False 
            print("\nThanks for using the Task List CLI! ")
        
        print_linebreaks()

run_cli()


        

