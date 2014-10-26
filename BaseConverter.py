#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
import sys

sys.path.insert(0,"/home/rojergs/Documents/pyStuff/myLibs")

from abstractDataTypes import Stack

class BaseConverter(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        
        self.initialize() # call the GUI initializer
        
    def initialize(self):
        # create the GUI container to hold everything
        self.container = ttk.Frame(self,
                                    padding="3 3 12 12")
        self.container.grid(column=0, row=0, sticky=
                                            (N, W, E, S))
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)
        
        # top label, just text
        ttk.Label(self, text="Convert number").grid(
                            columnspan=3, column=1, row=1)
        
        # the validate command for the entry
        vcmd = (self.register(self.validateEntryEdit),'%P')
        # the entry with the number we want to convert
        self.numberEntry = ttk.Entry(self, width=13,
            validate="key", validatecommand=vcmd)
        self.numberEntry.grid(column=1, row=2)
        # bind the return key with converting stuff!
        self.numberEntry.bind("<Return>", self.ConvertOnReturn)
        
        # simple label to choose the base
        ttk.Label(self, text="from base:").grid(column=2, row=2)
        
        self.fromBase = StringVar()
        # combobox with the 36 "from" bases allowed
        self.chooseFromBase = ttk.Combobox(self, width=3,
            textvariable = self.fromBase)
        self.chooseFromBase.grid(column=3, row=2,
            sticky=(E, W))
        self.chooseFromBase.state(["readonly"])
        self.chooseFromBase["values"] = list(range(2,37))
        self.chooseFromBase.set("10")
        
        # middle label to identify the arrival point:
        ttk.Label(self, text="to base:", anchor="w").grid(
                            column=2, row=3)
        
        self.toBase = StringVar()
        # combobox with the 36 "to" bases allowed
        self.chooseToBase = ttk.Combobox(self, width=3,
            textvariable = self.toBase)
        self.chooseToBase.grid(column=3, row=3,
            sticky=(E, W))
        self.chooseToBase.state(["readonly"])
        self.chooseToBase["values"] = list(range(2,37))
        self.chooseToBase.set("2")
        
        # convert button
        ttk.Button(self, text="Convert!", padding="0 10 0 10",
                    command=self.ConvertOnClick).grid(
                    rowspan=2, column=4, row=2, padx=50)
        
        self.display = StringVar()            
        # result label
        self.displayLabel = ttk.Label(self, textvariable=self.display,
        padding="2", width=40, relief="sunken", anchor="center",
        wraplength=300, justify="center")
        self.displayLabel.grid(columnspan=4, column=1, row=4)
        self.display.set("Type in a number, choose its base, "\
            "select the desired conversion base.")
        
        # fix the size
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)
        self.resizable(False, False)
        self.update()
        self.geometry(self.geometry())
        
        self.EntryFocus() # set focus
        
    def ConvertOnClick(self):
        self.display.set("")
        self.displayLabel["foreground"] = "black" # ensure a black font
    
        chars = "0123456789abcdefghijklmnopqrstuvwxyz"
        
        # do some error testing:
        convert = self.numberEntry.get()
        allowed_chars = chars[:int(self.fromBase.get())]
        for char in convert:
            if char not in allowed_chars:
                self.DisplayError("Invalid characters for chosen base\n")
                return
        
        fromBase = self.fromBase.get()
        toBase = self.toBase.get()
        decimal = self.NToDecimal(convert, fromBase)
        for char in decimal:
            if char not in "0123456789":
                self.DisplayError("An internal error occurred :/\n")
        destination_base = self.DecimalToN(decimal, toBase)
        self.display.set(destination_base)
        
        self.EntryFocus()
        
    def ConvertOnReturn(self, event):
        self.ConvertOnClick()
        
    def DisplayError(self, msg):
        self.displayLabel["foreground"] = "red"
        self.display.set(msg)
        
    def NToDecimal(self, num, fromBase):
        fromBase = int(fromBase)
        if fromBase < 2 or fromBase > 36:
            self.DisplayError("Invalid number base to"\
            " convert from.")
            return
            
        chars = "0123456789abcdefghijklmnopqrstuvwxyz"
        num = str(num)
        result = 0
        
        while num:
            char = chars.index(num[:1])
            num = num[1:]
            result += char * pow(fromBase, len(num))
        
        return str(result)
        
    def DecimalToN(self, num, toBase):
        toBase = int(toBase)
        num = int(num)
        if toBase < 2 or toBase > 36:
            self.DisplayError("Invalid number base to"\
            " convert to.")
            return
            
        s = Stack()
        chars = "0123456789abcdefghijklmnopqrstuvwxyz"
        n = num
        
        while num != 0:
            s.push(chars[num%toBase])
            num //= toBase
        result = s.to_reverse_string() if n != 0 else "0"
        
        return result
        
    def validateEntryEdit(self, P):
        return (len(P) <= 13)
        
    def EntryFocus(self):
        self.numberEntry.focus_set()
        self.numberEntry.selection_range(0, END)
        
    def start(self):
        self.mainloop()
        
if __name__ == "__main__":
    app = BaseConverter(None)
    app.title = "Base Converter"
    app.start()