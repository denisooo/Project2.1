from Arduino import Arduino
from Util import *

import time
import serial.tools.list_ports
import threading


# Main controller for back-end
class PyCtrl:
    _available_ports = []
    _available_arduinos = []
    _stop = False  # Used to exit threads within THIS class

    def __init__(self, model):
        self._port_scanner = threading.Thread(target=self._update_ports, args=(5,)) # args = tijd tussen com poort scans
        self._model = model

    def start(self):
        self._stop = False  # Make sure we don't auto-stop on future runs.
        self._port_scanner.start()

    def stop(self):
        if DEBUG:
            print(color('Stopping back-end process.', COLORS.YELLOW))
        self._stop = True
        for ard in self._available_arduinos:
            ard.stop()

    def get_arduinos(self):
        return self._available_arduinos

    # Listen to our available ports, and update them
    def _update_ports(self, delay):
        while not self._stop:
            if DEBUG:
                pass

            # Get all ports
            ports = list(serial.tools.list_ports.comports())

            # Check all ports
            for p in ports:
                if not p[0] in self._available_ports:
                    self._available_ports.append(p[0])  # Set port to in-use
                    arduino = Arduino(p[0], self._model)
                    self._available_arduinos.append(arduino)  # Add a new arduino to our list
                    arduino.start()
                    if DEBUG:
                        print('Added new Arduino on port: {0}'
                            .format(color(p[0], COLORS.CYAN, TextStyle.HIGHLIGHT)))

            # Remove inactive ports
            for k in self._available_ports:
                r = 1
                for p in ports:
                    if k == p[0]:
                        r = 0
                        break
                if r:
                    self._available_ports.remove(k)  # Remove this port from our active list
                    if DEBUG:
                        print('Removed inactive port: {0}'
                              .format(color(k, COLORS.YELLOW, TextStyle.HIGHLIGHT)))

            # Update our actual list
            for ard in self._available_arduinos:
                if not ard.get_port() in self._available_ports:
                    ard.stop()
                    self._available_arduinos.remove(ard)  # Remove the reference to this arduino from our active list

            time.sleep(delay)
