#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
from threading import Thread
import time

class QuestionAdder(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        
        self.initialize()
        
    def initialize(self):
        self.c = ttk.Frame(self, padding="5")
        self.c.grid(column=0, row=0)
        
        # String variables
        self.q = StringVar()
        self.o1 = StringVar()
        self.o2 = StringVar()
        self.o3 = StringVar()
        self.o4 = StringVar()
        self.warn = StringVar()
        
        # validate command
        vcmd = (self.register(self.validateOptn),"%P")
    
        # Create labels/entries for instructions/input
        ttk.Label(self.c, text="Question: ").grid(column=0, row=0)
        self.question = ttk.Entry(self.c, width=60, textvariable=self.q)
        self.question.grid(column=1, row=0, columnspan=2)
        
        ttk.Label(self.c, text="Correct option: ").grid(column=0, row=1)
        self.opt1 = ttk.Entry(self.c, width=25, textvariable=self.o1,
                validate="key", validatecommand=vcmd)
        self.opt1.grid(column=1, row=1, sticky="WE")
        self.opt1.bind("<FocusIn>", self.clearWarning)
        
        ttk.Label(self.c, text="Wrong option 1: ").grid(column=0, row=2)
        self.opt2 = ttk.Entry(self.c, width=25, textvariable=self.o2,
                validate="key", validatecommand=vcmd)
        self.opt2.grid(column=1, row=2, sticky="WE")
        self.opt2.bind("<FocusIn>", self.clearWarning)
        
        ttk.Label(self.c, text="Wrong option 2: ").grid(column=0, row=3)
        self.opt3 = ttk.Entry(self.c, width=25, textvariable=self.o3,
                validate="key", validatecommand=vcmd)
        self.opt3.grid(column=1, row=3, sticky="WE")
        self.opt3.bind("<FocusIn>", self.clearWarning)
        
        ttk.Label(self.c, text="Wrong option 3: ").grid(column=0, row=4)
        self.opt4 = ttk.Entry(self.c, width=25, textvariable=self.o4,
                validate="key", validatecommand=vcmd)
        self.opt4.grid(column=1, row=4, sticky="WE")
        self.opt4.bind("<FocusIn>", self.clearWarning)
        
        # button to submit
        self.submit = ttk.Button(self.c, width=10, text="Submit", command=self.submitQ)
        self.submit.grid(column=2, row=1, rowspan=4, sticky="NWES")
        
        # warning label
        self.warning = ttk.Label(self, textvariable=self.warn, padding="2",
            relief="sunken", anchor="center", wraplength=500, justify="center")
        self.warning.grid(column=0, row=5, sticky="WE")
        
        # add padding
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)
            
        self.resizable(False, False)
        self.bind("<Return>", self.submitQ)
        self.question.focus_set()
            
    def submitQ(self, *args):
        # prevent double submissions
        if self.warn.get() == "Question added!":
            return
        # Ensure that all options are set, we have a question
        #and all options differ from one another
        q = self.q.get().strip()
        t = (self.o1.get().strip(), self.o2.get().strip(),
            self.o3.get().strip(), self.o4.get().strip())
        # dict to get correct msg by index
        opt_i = {0: "correct option",
                    1: "wrong option 1",
                    2: "wrong option 2",
                    3: "wrong option 3"}
        
        # check for empty entries
        if not q:
            self.setWarning("Invalid Question!!", "red")
            return
        for i, option in enumerate(t):
            if not option:
                self.setWarning("Invalid option for '"+opt_i[i]+"'", "red")
                return
                
        # check for equal answers
        for i in range(len(t)):
            sub_t = t[i+1:]
            for i2 in range(len(sub_t)):
                if t[i] == sub_t[i2]:
                    self.setWarning("The '{}' is the same as '{}'!".format(
                        opt_i[i], opt_i[i+1+i2]), "red")
                    return
                    
        # create the string to write to the file
        s = ''+q+', '+t[0]+', '+t[1]+', '+t[2]+', '+t[3]
        
        with open("quiz.db", "a") as f:
            f.write("\n"+s)
        
        self.question.focus_set()
        self.q.set("")
        self.o1.set("")
        self.o2.set("")
        self.o3.set("")
        self.o4.set("")
        self.setWarning("Question added!", "blue")
        
    def validateOptn(self, P):
        return (len(P) <= 36)
        
    def setWarning(self, msg, clr):
        self.warning["foreground"] = clr
        self.warn.set(msg)
        
    def clearWarning(self, event):
        self.warning["foreground"] = "black"
        self.warn.set("")
        
if __name__ == "__main__":
    myapp = QuestionAdder(None)
    myapp.title = "Quiz Question Adder"
    Thread(target=myapp.mainloop).run()