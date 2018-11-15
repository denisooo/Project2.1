from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import serial.tools.list_ports
from PyCtrl import PyCtrl


class MainView:
    def __init__(self, master):
        """Initialize the main Program View.
        """
        self.ports = list(serial.tools.list_ports.comports())
        self.master = master  # initialize Root window
        self.master.title('Zeng.ltd Dashboard')  # set title for Root window
        self.master.geometry("1000x700")  # set size and location for Root window
        self.master.configure(background="lightgrey")
        self.mainframe = ttk.Notebook(self.master,
                                      padding="0 0 0 0")  # left top right bottem    create mainframe in Root winow
        self.mainframe.grid(column=0, row=0, sticky=(N, W, S, E))  # set mainframe to root windows size
        self.master.protocol("WM_DELETE_WINDOW", lambda: self.quit())

        menubar = Menu(self.master)  # create a menubar

        # display the menu
        self.master.config(menu=menubar)

        # List of all our views
        self.views = {}  # Empty dict

        # The back-end process
        self.pyctrl = PyCtrl(self)
        self.pyctrl.start()



    def quit(self):
        self.pyctrl.stop()  # Will automatically stop all arduinos
        self.master.quit()
        self.master.destroy()


# END OF class: Mainview--------------------------------------------------------------------------
def main():
    root = Tk()
    MainView(root)
    root.mainloop()


main()
