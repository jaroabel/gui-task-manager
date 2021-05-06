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

    # Clear title, date, comment fields
    def clear_field(self):
        self.title_entry_var.set("")
        self.date_entry_val.set("")
        self.task_view_txt.delete('1.0', END)

    # read text file
    def read_file(self):
        self.dic_list.clear()
        count = 0
        print("\nUsing for loop")

        with open("task_list.txt") as fp:
            for line in fp:
                count += 1
                self.dic_list[count] = line.strip().split("|")
                print("Line{}: {}".format(count, line.strip()))
        print("Line", self.dic_list)

    # Add new task
    def add_new_task(self):
        taskTitle = self.title_entry_var.get()
        taskDate = self.date_entry_val.get()
        taskDescription = self.task_view_txt.get("1.0",END)

        line = taskTitle + "|" + taskDate + "|" + taskDescription
        with open('task_list.txt', 'a') as f:
            f.write(line)

        self.clear_field()
        self.read_file()
        self.display_task_in_treeview()

    # Update text file after update action was taking on the GUI app
    def update_text_file(self):
        list_items = []
        for key, value in self.dic_list.items():
            line = f"{value[0].strip()}|{value[1].strip()}|{value[2].strip()}\n"
            list_items.append(line)

        with open('task_list.txt', 'w') as f:
            for i in list_items:
                f.write(i)

        self.clear_field()

    # Display selected value from tree view in upper fields
    def get_listview_value(self, event):
        self.clear_field()
        curItem = self.task_list.focus()
        listVal = self.task_list.item(curItem)

        self.list_id = listVal['text']
        self.title_entry_var.set(listVal['values'][1])
        self.date_entry_val.set(listVal['values'][0])
        self.task_view_txt.insert('1.0', listVal['values'][2])

    # Update task
    def update_task(self):
        taskTitle = self.title_entry_var.get()
        taskDate = self.date_entry_val.get()
        taskDescription = self.task_view_txt.get("1.0",END)

        self.dic_list[self.list_id][0] = taskTitle
        self.dic_list[self.list_id][1] = taskDate
        self.dic_list[self.list_id][2] = taskDescription

        self.update_text_file()
        self.display_task_in_treeview()

    # Delete task
    def delete_task(self):
        self.dic_list.pop(self.list_id, None)
        self.update_text_file()
        self.read_file()
        self.display_task_in_treeview()

    def __init__(self):
        self.list_id = 0
        self.dic_list = {}
        self.read_file()
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
        self.task_list = ttk.Treeview(frame)
        self.task_list["columns"] = ("one", "two", "three")
        self.task_list.column("#0", width=3, minwidth=3, stretch=YES)
        self.task_list.column("one", width=5, minwidth=5, stretch=YES)
        self.task_list.column("two", width=15, minwidth=15)
        self.task_list.column("three", width=20, minwidth=20, stretch=YES)

        self.task_list.heading("#0", text="#", anchor=W)
        self.task_list.heading("one", text="Date", anchor=W)
        self.task_list.heading("two", text="Name", anchor=W)
        self.task_list.heading("three", text="Task", anchor=W)

        self.task_list.grid(column=0, row=7, columnspan=3, sticky=(W, E))

        # Insert data in list view
        self.display_task_in_treeview()

    # Display all task in Tree View
    def display_task_in_treeview(self):
        self.task_list.delete(*self.task_list.get_children())
        for key, value in self.dic_list.items():
            self.task_list.insert("", "end", text=key, values=(value[1], value[0], value[2]))
        self.task_list.bind("<<TreeviewSelect>>", self.get_listview_value)






        self.root.mainloop()


create_app = CreateApp()
