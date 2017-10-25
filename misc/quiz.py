#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
from random import shuffle
import threading
import time

class Quiz(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        
        self.parent = parent
        
        self.loadDB()
        
        self.initialize()
        
    def initialize(self):
        # add the main container
        self.c = ttk.Frame(self, padding="5")
        self.c.grid(column=0, row=0, sticky="NWES")
        self.c.columnconfigure(0, weight=1)
        self.c.rowconfigure(0, weight=1)
        
        # string variables
        self.sQuestion = StringVar()
        self.selected = IntVar()
        self.sOpt1 = StringVar()
        self.sOpt2 = StringVar()
        self.sOpt3 = StringVar()
        self.sOpt4 = StringVar()
        self.warn = StringVar()
        
        # question label
        self.question = ttk.Label(self.c, textvariable=self.sQuestion,
        justify="left", padding="5", width=50, wraplength=397, relief="raised")
        self.question.grid(column=0, row=0, sticky=(W,E), columnspan=2)
        
        # option radiobuttons
        self.rOpt1 = ttk.Radiobutton(self.c, textvariable=self.sOpt1, 
                        variable=self.selected, value=1)
        self.rOpt1.grid(column=0, row=1, sticky=(W), columnspan=2)
        self.rOpt2 = ttk.Radiobutton(self.c, textvariable=self.sOpt2, 
                        variable=self.selected, value=2)
        self.rOpt2.grid(column=0, row=2, sticky=(W), columnspan=2)
        self.rOpt3 = ttk.Radiobutton(self.c, textvariable=self.sOpt3,
                        variable=self.selected, value=3)
        self.rOpt3.grid(column=0, row=3, sticky=(W), columnspan=2)
        self.rOpt4 = ttk.Radiobutton(self.c, textvariable=self.sOpt4,
                        variable=self.selected, value=4)
        self.rOpt4.grid(column=0, row=4, sticky=(W), columnspan=2)

        # submit button
        self.submit = ttk.Button(self.c, text="Submit", width=8,
            command=self.submitAnswer)
        self.submit.grid(column=0, row=5, sticky=(W))
        # status lbl
        self.status = ttk.Label(self.c, textvariable=self.warn, padding="5",
                        relief="sunken", width=40)
        self.status.grid(column=1, row=5, sticky=(W,E))
        
        # counter frame and its divs
        self.counterFrame = ttk.Frame(self.c, padding="5", relief="sunken")
        self.counterFrame.grid(column=0, row=6, columnspan=2, sticky=(N,W,E,S))
        self.rightFrame = ttk.Frame(self.counterFrame, width=25)
        self.rightFrame.pack(side=LEFT, fill="y")
        self.wrongFrame = ttk.Frame(self.counterFrame, width=25)
        self.wrongFrame.pack(side=RIGHT, fill="y")
        
        self.right = StringVar()
        self.wrong = StringVar()
        
        ttk.Label(self.rightFrame, text="Correct: ").pack(side=LEFT, fill="y")
        self.correct = ttk.Label(self.rightFrame, textvariable=self.right)
        self.correct.pack(side=LEFT, fill="y")
        
        ttk.Label(self.wrongFrame, text="Incorrect: ").pack(side=LEFT, fill="y")
        self.incorrect = ttk.Label(self.wrongFrame, textvariable=self.wrong)
        self.incorrect.pack(side=LEFT, fill="y")
        
        self.right.set("0")
        self.wrong.set("0")
        
        for child in self.c.winfo_children():
            child.grid_configure(padx=5, pady=3)
            
        self.bind("<Return>", self.submitAnswer)
        self.bind("1", self.changeSelection)
        self.bind("2", self.changeSelection)
        self.bind("3", self.changeSelection)
        self.bind("4", self.changeSelection)
        
        self.nextQuestion()
        self.selected.set("1")
        
    def nextQuestion(self):
        if not self.questions:
            self.loadDB()
            self.setWarn("You answered every question!", "#0033CC")
        self.current_question = (self.questions[0]).split(", ")
        self.questions = self.questions[1:]
        
        self.sQuestion.set(self.current_question[0])
        answers = self.current_question[1:]
        shuffle(answers)
        self.sOpt1.set(answers[0])
        self.sOpt2.set(answers[1])
        self.sOpt3.set(answers[2])
        self.sOpt4.set(answers[3])
        
    def changeSelection(self, event):
        self.selected.set(event.char)
        
    def submitAnswer(self, *args):
    
        # get the chosen text
        opts = [None, self.sOpt1, self.sOpt2, self.sOpt3, self.sOpt4]
        chosen = opts[self.selected.get()].get()
        if chosen == self.current_question[1]:
            n = self.right.get()
            self.right.set(str(int(n)+1))
            self.setWarn("Correct", "#006600") # dark green
        else:
            n = self.wrong.get()
            self.wrong.set(str(int(n)+1))
            self.setWarn("Incorrect", "#CC0000") # a darker red
    
        self.nextQuestion()

    def setWarn(self, msg, clr):
        self.status["foreground"] = clr
        self.warn.set(msg)
        
    def loadDB(self):
        with open("quiz.db", "r") as f:
            self.questions = f.read().split('\n')
        shuffle(self.questions)
        
    def mainloop(self):
        raise RuntimeError("Quiz instances should call .start()")
        
    def start(self):
        Tk.mainloop(self)

        
if __name__ == "__main__":
    q = Quiz(None)
    q.start()
