import struct
from Util import *

import sys
import time
import serial.tools.list_ports
import serial
import threading
from datetime import datetime

from ArduinoGUI import ArduinoGUI


class Arduino:
    _stop = False  # Used to exit threads within THIS class.

    def __init__(self, port, model):
        self._port = port
        self._ser = serial.Serial(port=self._port)  # Defaults to 9600 baudrate
        self._listener = threading.Thread(target=self._listen, args=(.2,))  # Prepare listener for .2 second interval
        self._model = model

    def start(self):
        self._stop = False  # Make sure it's not going to stop immediately.
        self._listener.start()
        self._model.views[self._port] = ArduinoGUI(self._model.mainframe, self)

    def stop(self):
        self._stop = True
        if DEBUG:
            print('{0} Arduino connection on port: {1}'
                  .format(color('STOPPING', COLORS.RED),
                          color(self._port, COLORS.CYAN)))

        try:
            self._model.views[self._port].remove()
        except:
            print("Couldn't delete view?")

    def get_port(self):
        return self._port

    def send(self, command, args):
        send_thread = threading.Thread(target=self._send, args=(command, args))
        send_thread.start()

    def _send(self, command, args):
        self._ser.write(bytes([command]))

        for param in args:
            self._ser.write(bytes([param]))  # Send all parameters

        self._ser.write(bytes([128]))  # Endbyte

    def _listen(self, delay):
        while not self._stop:
            try:

                while self._ser.inWaiting() > 0:
                    byte = self._ser.read()
                    byte = int.from_bytes(byte, byteorder='big')

                    if byte == COMMANDS.SEND_TEMP:
                        reading = self._ser.readline()
                        analog_value = int(reading)
                        voltage = analog_value * 5.0 / 1024
                        temperature = (voltage - 0.5) * 100
                        if DEBUG:
                            print('[{0}]: Received {1} sensor reading - {2} - {3}v - {4} degrees C.'
                                  .format(self._port, 'temperature', analog_value, voltage, temperature))

                            # Plot chart
                            self._model.views[self._port].tempvalue.append(temperature)
                            self._model.views[self._port].temptime.append(datetime.now().strftime("%H:%M:%S"))

                            if len(self._model.views[self._port].tempvalue) > 7:
                                self._model.views[self._port].tempvalue.pop(0)
                                self._model.views[self._port].temptime.pop(0)

                            self._model.views[self._port].redraw()
                    elif byte == COMMANDS.SEND_LIGHT:
                        reading = self._ser.readline()
                        analog_value = int(reading)
                        if DEBUG:
                            print('[{0}]: Received {1} sensor reading - {2}'.format(self._port, 'light', analog_value))

                            # Plot chart
                            self._model.views[self._port].lightvalue.append(analog_value)
                            self._model.views[self._port].lighttime.append(datetime.now().strftime("%H:%M:%S"))

                            if len(self._model.views[self._port].lightvalue) > 7:
                                self._model.views[self._port].lightvalue.pop(0)
                                self._model.views[self._port].lighttime.pop(0)

                            self._model.views[self._port].redraw()
                    elif byte == COMMANDS.SEND_MODE:
                        reading = self._ser.readline()
                        val = int(reading)
                        if val == MODES.AUTO:
                            mode = 'Automatic'
                        else:
                            mode = 'Manual'

                        self._model.views[self._port].mode.config(text="Current mode: {0}".format(mode))

                        if DEBUG:
                            print('[{0}]: Received new {1} - {2}'.format(self._port, 'mode', mode))

                    elif byte == COMMANDS.SEND_STATE:
                        reading = self._ser.readline()
                        val = int(reading)
                        state = '123'
                        if val == STATES.ROLLED_IN:
                            state = 'Rolled in'
                        elif val == STATES.ROLLED_OUT:
                            state = 'Rolled out'
                        else:
                            state = 'Rolling'

                        self._model.views[self._port].status.config(text="Current status: {0}".format(state))

                        if DEBUG:
                            print('[{0}]: Received new {1} - {2}'.format(self._port, 'state', state))

                    elif byte == COMMANDS.INC_TEMP:
                        self._model.views[self._port].cur_temp = self._model.views[self._port].cur_temp + 2
                        self._model.views[self._port].update_labels()

                        if DEBUG:
                            print('[{0}]: {1} {2}'.format(self._port, 'INCREASE', 'TEMP'))

                    elif byte == COMMANDS.DEC_TEMP:
                        self._model.views[self._port].cur_temp = self._model.views[self._port].cur_temp - 2
                        self._model.views[self._port].update_labels()

                        if DEBUG:
                            print('[{0}]: {1} {2}'.format(self._port, 'DECREASE', 'TEMP'))

                    elif byte == COMMANDS.INC_LIGHT:
                        self._model.views[self._port].cur_light = self._model.views[self._port].cur_light + 25
                        self._model.views[self._port].update_labels()

                        if DEBUG:
                            print('[{0}]: {1} {2}'.format(self._port, 'INCREASE', 'LIGHT'))

                    elif byte == COMMANDS.DEC_LIGHT:
                        self._model.views[self._port].cur_light = self._model.views[self._port].cur_light - 25
                        self._model.views[self._port].update_labels()

                        if DEBUG:
                            print('[{0}]: {1} {2}'.format(self._port, 'DECREASE', 'LIGHT'))

                    else:
                        print('[{0}]: {1}'.format(self._port, byte))

            except:


                time.sleep(5)  # Wait at least 5 seconds before continuing

            time.sleep(delay)  # Wait before polling again.
