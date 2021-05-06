# App name: Task Manager
# Description: Task manager application, capturing task name, task date,
# task description and storing all task in a text file.
# Actions: add task, update task, delete task
# Author: Jean-Marie Abel

from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from datetime import date
import os


class CreateApp:
    root = Tk()
    date_entry_val = StringVar()
    cal = 0

    # Show calendar datepicker
    def showCalendar(self):
        today = date.today()
        y, m, d = str(today).split("-")
        root = Tk()
        root.title("Datepicker")

        self.cal = Calendar(root, font="Arial 14", selectmode='day', locale='en_US',
                       cursor="hand1", year=int(y), month=int(m), day=int(d), background='darkblue', foreground='#000', borderwidth=2)

        self.cal.pack(fill="both", expand=True)

        ttk.Button(root, text="ok", command=self.set_date_value).pack()

        root.mainloop()

    # Set selected date value
    def set_date_value(self):
        my_date = self.cal.selection_get()
        self.date_entry_val.set(my_date)


    def read_file(self):
        count = 0
        print("\nUsing for loop")

        with open("task_list.txt") as fp:
            for line in fp:
                count += 1
                print("Line{}: {}".format(count, line.strip()))

    # Add new task
    def add_new_task(self):
        taskTitle = self.title_entry_var.get()
        taskDate = self.date_entry_val.get()
        taskDescription = self.task_view_txt.get("1.0",END)

        line = taskTitle + "|" + taskDate + "|" + taskDescription + "\n"
        with open('task_list.txt', 'a') as f:
            f.write(line)

        self.title_entry_var.set("")
        self.date_entry_val.set("")
        self.task_view_txt.delete('1.0', END)

    def update_task(self):
        pass

    def delete_task(self):
        pass

    def __init__(self):
        style = ttk.Style()
        style.theme_use('classic')  # Any style other than aqua.
        style.configure('TFrame', background='white')
        style.configure(".", font=("Arial", 15))
        self.root.title("Task Manager")
        self.root.geometry("480x650")

        style.configure('Date.TButton', foreground='black', background='white', borderwidth='0')

        frame = ttk.Frame(self.root, padding="10 10 10 10")
        frame.grid(column=0, row=0, sticky=(N, S, E, W))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        # 1st row
        ttk.Label(frame, text="Task Name: ", background="white").grid(column=0, row=0, sticky=(W, E))

        self.title_entry_var = StringVar()
        title_entry = ttk.Entry(frame, width=25, textvariable=self.title_entry_var)
        title_entry.grid(column=1, row=0, sticky=(W, E))

        # date picker
        self.date_entry_val.set('YYYY-MM-DD')
        ttk.Label(frame, text="Choose date: ", background="white").grid(column=0, row=1, sticky=(W, E))
        date_entry = ttk.Entry(frame, width=7, text=self.date_entry_val, textvariable=self.date_entry_val)
        date_entry.grid(column=1, row=1, sticky=(W, E))
        ttk.Button(frame, text='Calendar', style='Date.TButton', command=self.showCalendar).grid(column=2, row=1, sticky=(W, E))

        # Text field
        #self.task_txt_var = StringVar()
        ttk.Label(frame, text="Enter task: ", background="white").grid(column=0, row=3, sticky=(W, E))
        self.task_view_txt = Text(frame, height=10, width=30, insertborderwidth=2, relief=RIDGE, highlightbackground='#ccc')
        self.task_view_txt.grid(column=0, row=4, columnspan=3, sticky=(W, E))

        # Action buttons
        ttk.Button(frame, text="Add Task", command=self.add_new_task).grid(column=0, row=5, sticky=(W, E))
        ttk.Button(frame, text="Update Task", command=self.update_task).grid(column=1, row=5, sticky=(W, E))
        ttk.Button(frame, text="Delete Task", command=self.delete_task).grid(column=2, row=5, sticky=(W, E))


        # Task list
        ttk.Label(frame, text="Task List", background="white").grid(column=0, row=6, sticky=(W, E))
        task_list = ttk.Treeview(frame)
        task_list["columns"] = ("one", "two", "three")
        task_list.column("#0", width=3, minwidth=3, stretch=YES)
        task_list.column("one", width=5, minwidth=5, stretch=YES)
        task_list.column("two", width=15, minwidth=15)
        task_list.column("three", width=20, minwidth=20, stretch=YES)

        task_list.heading("#0", text="#", anchor=W)
        task_list.heading("one", text="Date", anchor=W)
        task_list.heading("two", text="Name", anchor=W)
        task_list.heading("three", text="Task", anchor=W)

        task_list.grid(column=0, row=7, columnspan=3, sticky=(W, E))

        # Insert data in list view
        task_list.insert("", "end", text="1", values=("23-Jun-17 11:05", "Name Gathering", "Text"))
        task_list.insert("", "end", text="2", values=("24-Jun-17 11:25", "ATM E-dm", "1 KB"))









        self.root.mainloop()


create_app = CreateApp()
