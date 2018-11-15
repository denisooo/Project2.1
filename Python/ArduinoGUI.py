from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from Util import *
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import time

class ArduinoGUI:
    def __init__(self, master, arduino):
        self.master = master
        self.frame = ttk.Frame(self.master)

        # Reference for arduino object
        self._arduino = arduino

        # verdeel het GUI scherm in 2 aparte frames 1 voor data en knoppen, de ander voor de mathplot
        self.frameone = ttk.Frame(self.frame)  # contains all the buttons and labels
        self.frameone.grid(column=0, row=0, sticky='NW')  # sticks frames to the upper left corner of the root window
        self.frametwo = ttk.Frame(self.frame)
        self.frametwo.grid(column=1, row=0, sticky='NW')
        self.framethree = ttk.Frame(self.frame)
        self.framethree.grid(column=1, row=1)

        self.toolbarboolean = FALSE  # control boolean for the toolbar rendering

        # list that will contain the data that is passed by the arduino sensors
        self.temptime = [0]
        self.tempvalue = [0]

        self.lighttime = [0]
        self.lightvalue = [0]

        # Control variables for the input fields
        self.temp = StringVar()
        self.light = StringVar()

        # start GUI
        self.status = Label(self.frameone, text="Current status: Rolled in")  # rolled in, rolled out, or rolling
        self.status.grid(column=0, row=1, sticky=(W))

        self.mode = Label(self.frameone, text="Current mode: Automatic")  # automatic or manual
        self.mode.grid(column=0, row=2, sticky=(W))

        self.changeMode = ttk.Button(self.frameone, text='Change mode', width=25,
                                     command=self.change_mode)  # should change the mode from automatic to manual or the other way around
        self.changeMode.grid(column=0, row=3)

        self.inrollen = ttk.Button(self.frameone, text='Roll in', width=25,
                                   command=self.roll_in)  # should change the mode to manual and call roll in
        self.inrollen.grid(column=0, row=4)

        self.uitrollen = ttk.Button(self.frameone, text='Roll out', width=25,
                                    command=self.roll_out)  # should change the mode to manual and roll out
        self.uitrollen.grid(column=0, row=5)

        # Temperature
        self.cur_temp = 15  # Default is 50
        self.dec_temp = ttk.Button(self.frameone, text="-2", width=5,
                                   command=self.dec_temp)
        self.dec_temp.grid(column=1, row=10)

        self.ceil_temp_label = Label(self.frameone, width=25, text="Temperature: {0}".format(self.cur_temp))
        self.ceil_temp_label.grid(column=0, row=10)

        self.inc_temp = ttk.Button(self.frameone, text="+2", width=5,
                                   command=self.inc_temp)
        self.inc_temp.grid(column=2, row=10)

        # Light
        self.cur_light = 800  # Default is 800
        self.dec_light = ttk.Button(self.frameone, text="-25", width=5,
                                    command=self.dec_light)
        self.dec_light.grid(column=1, row=11)

        self.ceil_light_label = Label(self.frameone, width=25, text="Light intensity: {0}".format(self.cur_light))
        self.ceil_light_label.grid(column=0, row=11)

        self.inc_light = ttk.Button(self.frameone, text="+25", width=5,
                                    command=self.inc_light)
        self.inc_light.grid(column=2, row=11)

        self.f = Figure(figsize=(7, 7), dpi=100)
        self.f.set_facecolor('lightgrey')

        self.a1 = self.f.add_subplot(211)
        self.a1.set_ylim([0, 35])  # temp

        self.a2 = self.f.add_subplot(212)
        self.a2.set_ylim([0, 1023])  # light

        self.a1.plot(self.temptime, self.tempvalue, label='Temperatuur')
        self.a1.set_title('Temperatuur:', loc='left')
        self.a1.set_xlabel('Tijd')

        self.a1.set_ylabel('Waarde')
        self.a1.legend()

        self.a2.plot(self.lighttime, self.lightvalue, label='Lichtintensiteit')
        self.a2.set_title('Licht:', loc='left')

        self.a2.set_xlabel('Tijd')
        self.a2.set_ylabel('Waarde')
        self.a2.legend()

        self.canvas = FigureCanvasTkAgg(self.f, master=self.frametwo)
        self.canvas.get_tk_widget().pack()
        self.canvas._tkcanvas.pack()

        for child in self.frameone.winfo_children():
            child.grid_configure(padx=5, pady=5)
        self.master.add(self.frame,
                        text=self._arduino.get_port())  # notebook tab label: deze moet nog even de text gewijzigd worden naar iets dynamics

    def remove(self):
        self.frame.destroy()

    def redraw(self):
        self.frametwo = ttk.Frame(self.frame)
        self.frametwo.grid(column=1, row=0)

        self.a1.plot(self.temptime, self.tempvalue, label='Temperatuur')
        self.a1.set_title('Temperatuur:', loc='left')
        self.a1.set_xlabel('Tijd')
        self.a1.set_ylabel('Waarde')

        self.a2.plot(self.lighttime, self.lightvalue, label='Lichtintensiteit')
        self.a2.set_title('Lichtintensiteit:', loc='left')
        self.a2.set_xlabel('Tijd')
        self.a2.set_ylabel('Waarde')

        self.canvas = FigureCanvasTkAgg(self.f, master=self.frametwo)
        self.canvas.get_tk_widget().pack()
        self.canvas._tkcanvas.pack()

    def modifydata(self):
        self.tempvalue[0] = self.tempvalue[0] + 5
        print(self.tempvalue)

    def roll_in(self):
        self._arduino.send(COMMANDS.ROLL_IN, [])

    def roll_out(self):
        self._arduino.send(COMMANDS.ROLL_OUT, [])

    def change_mode(self):
        self._arduino.send(COMMANDS.CHANGE_MODE, [])

    def inc_temp(self):
        self._arduino.send(COMMANDS.INC_TEMP, [])

    def dec_temp(self):
        self._arduino.send(COMMANDS.DEC_TEMP, [])

    def inc_light(self):
        self._arduino.send(COMMANDS.INC_LIGHT, [])

    def dec_light(self):
        self._arduino.send(COMMANDS.DEC_LIGHT, [])

    def update_labels(self):
        self.ceil_light_label.config(text="Light: {0}".format(self.cur_light))
        self.ceil_temp_label.config(text="Temp: {0}".format(self.cur_temp))

    def setTemp(self):

        try:
            templimit = int(self.temp.get())
            print(templimit)
        except:
            print('de input is niet te casten naar een int')
            messagebox.showerror('Voer een geldige waarde in.')

    def setLight(self):
        try:
            lightlimit = int(self.light.get())
            print(lightlimit)
        except:
            print('de input is niet te casten naar int')
            messagebox.showerror('Voer een geldige waarde in.')
