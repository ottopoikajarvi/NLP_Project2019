import tkinter as tk
import subprocess

def start_analysis():
    print("Starting the process")
    argument2 = entry.get()
    subprocess.Popen("python3 pickleopener.py " + argument2, shell=True)
    

master = tk.Tk()
tk.Label(master, text="""Yle news "brexit" sentence analyser""").grid(row=0)
tk.Label(master, text="Brexit").grid(row=0, column=1)
tk.Label(master, text="Enter a second\nsearch term (optional)").grid(row=1)
tk.Label(master, text="Program will output status updates to terminal\nSome plots will be pop up\nThe analysing process continues after they are closed").grid(row=2, columnspan=2)

entry = tk.Entry(master)


entry.grid(row=1, column=1)


tk.Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=tk.W, pady=4, padx=70)
tk.Button(master, text='Start Analysing', command=start_analysis).grid(row=3, column=1, sticky=tk.W, pady=4)
tk.mainloop()