import mysql.connector as sql
import pandas as pd
import os
db = sql.connect(
    host="localhost",
    user="root",
    password="",
    database="python_test"
)

cursor = db.cursor()

false = False
true = True

class Task:
    def __init__(self,id,task, desc, due, assignee ):
        self.task_id = id
        self.task, self.desc, self.due, self.assignee = task, desc, due, assignee
        self.status = -1
        return

    def to_string_tuple(self):
        sts = ""
        if(self.status<0):
            sts="Pending"
        elif (self.status>0):
            sts = "Completed"
        else:
            sts="Working on"
        return (self.task_id,self.task, self.desc, self.due, self.assignee ,sts)
        
    def change_status(self, status):
        if status==1:
            self.status = -1
        elif status==2:
            self.status=0
        else:
            self.status=1
        cursor.execute('update tasks set status = %d'%self.status+" where task_id="+str(self.task_id))
        db.commit()
        print(cursor.rowcount)
        return
            
    def update_name(self,task_name):
        self.task = task_name
        cursor.execute('update tasks set task = "%s"'%self.task+" where task_id="+str(self.task_id))
        db.commit()
        return
    
    def update_desc(self, desc):
        self.desc = desc
        cursor.execute('update tasks set task_desc = "%s"'%self.desc+" where task_id="+str(self.task_id))
        db.commit()
        return
    
    def update_assignee(self,assignee):
        self.assignee = assignee
        cursor.execute('update tasks set assignee = "%s"'%self.assignee+" where task_id="+str(self.task_id))
        db.commit()
        return

    def update_due(self,due):
        self.due = due
        cursor.execute('update tasks set due = "%s"'%self.due+" where task_id="+str(self.task_id))
        db.commit()
        return
    
    def to_tuple(self):
        return (self.task_id, self.task, self.desc, self.due, self.assignee, self.status)
    
class TaskTracker:
    id = 0 
    def __init__(self):
        self.tasks = []
        cursor.execute("select * from tasks")
        for x in cursor:
            t = list(x)
            self.tasks.append(Task(t[0],t[1],t[2],t[3],t[4]))
            TaskTracker.id = t[0]
        return
    
    def find(self,task_id):
        for x in self.tasks:
            if task_id==x.task_id:
                return x
        return -1
    
    def show_all_tasks(self):
        if len(self.tasks)<=0:
            print("No tasks to show")
        else:
            data = []
            for x in self.tasks:
                data.append(x.to_string_tuple())
            df = pd.DataFrame(data,columns=["Task_Id","Task_Name","Description","Due_Date","Assignee","Status"])
            print(df.to_string(index=false))

    def addTask(self,task, desc, due, assignee):
        task_ = Task(TaskTracker.id+1, task, desc, due, assignee)
        self.tasks.append(task_)
        TaskTracker.id += 1
        cursor.execute('insert into tasks values (%s,%s,%s,%s,%s,%s)',task_.to_tuple())
        db.commit()
        print("Task created successfully")

    def update_status(self,task_id,status):
        task = self.find(task_id)
        if task==-1:
            print("No Task found")
        else:
            task.change_status(status)
            print("Updated successfully")
        
    def delete_task(self,task_id):
        cursor.execute("delete from tasks where task_id="+str(task_id))
        db.commit()
        print(cursor.rowcount)
        task = self.find(task_id)
        if task==-1:
            print("No task found")
            return
        self.tasks.remove(task)
        print("Deleted successfully")
        
    def update_task_name(self,task_id,task_name):
        task = self.find(task_id)
        if task==-1:
            print("No task found")
            return
        task.update_name(task_name)
        print("updated")

    def update_task_desc(self, task_id, desc):
        task = self.find(task_id)
        if task==-1:
            print("No task found")
            return
        task.update_desc(desc)
        print("Updated")

    def update_task_due(self,task_id,due):
        task = self.find(task_id)
        if task==-1:
            print("No task found")
            return
        task.update_due(due)
        print("updated")
    
    def update_task_assignee(self,task_id,assignee):
        task = self.find(task_id)
        if task==-1:
            print("No task found")
            return
        task.update_assignee(assignee)
        print("Updated")

def menu():
    list  = TaskTracker()
    while(true):
        print("-------------Main menu-------------")
        print("1. Create Task\n2. Show Tasks\n3. Status Update\n4. Delete Task\n5. Edit\n6. Exit")
        choice = int(input("Enter choice: "))
        match choice:
            case 1:
                os.system("cls")
                print("-------------create task--------------")
                task = input("Enter task: ")
                desc = input("Enter description: ")
                due = input("Enter due date: ")
                assignee = input("Enter assignee name: ")
                list.addTask(task,desc,due,assignee)
                print("task saved.")
                
            case 2: 
                os.system('cls')
                print("-----------all tasks-------------")
                list.show_all_tasks()
                
            case 3:
                os.system('cls')
                print("---------Change status----------")
                task_id = int(input("Enter task id to update status: "))
                print("1. Pending\n2. Working on\n3. Completed")
                status = int(input("Enter status choice from above: "))
                list.update_status(task_id,status)
                
            case 4:
                os.system('cls')
                print("-------------delete task---------------")
                task_id = int(input("Enter task id to delete: "))
                list.delete_task(task_id)
            
            case 5:
                os.system('cls')
                print("-----------edit menu----------")
                print("1. edit task name\n2. edit description\n3. edit due date\n4. edit assignee")
                choice = int(input("Enter choice from above: "))
                while(choice):
                    task_id = int(input("Enter task id: "))
                    match choice:
                        case 1:
                            name = input("Enter new name: ")
                            list.update_task_name(task_id,name) 
                            break
                        case 2:
                            desc = input("Enter new description: ")
                            list.update_task_desc(task_id,desc)
                            break
                        case 3:
                            due = input("Enter new date: ")
                            list.update_task_due(task_id,due)
                            break
                        case 4:
                            assignee = input("Enter new assignee: ")
                            list.update_task_assignee(task_id, assignee)
                            break
                
            case 6:
                print("Exiting..........")
                exit()
                
            case default:
                choice = input("Enter a valid choice: ")
                
        choice = input("wish to continue? y/n ")
        if(choice.lower()=='y'):
            os.system('cls')
            continue
        else:
            print("Exiting..........")
            exit(0)
            
menu()