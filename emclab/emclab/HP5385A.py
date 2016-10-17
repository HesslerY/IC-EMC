# -*- coding: utf-8 -*-
import time
import visa
from pprint import pprint

from .GPIB import GPIB

#===============================================================
class HP5385A(GPIB):
    """Frequency counter HP5385A.

    """
    #===============================================================
    def __init__(self, addr, chan = None, fname = None):
        """Initialization.

        """
        rm = visa.ResourceManager()
        self._dev = rm.open_resource('GPIB0::' + str(addr) + '::INSTR')

        # get instrument address

        self.addr = addr

        # get instrument name
        self.name = self._name()

        self._timestamp()

        self.fname = fname

        self._sel_chan(chan = chan)

    #===============================================================
    def meas_freq(self, chan = None):
        """Measure frequency.

        Returns frequency.

        Input parameters:
        chan - select channel:
        1, '1', 'A' or 2, '2', 'B'
        """
        self._dev.write('"FU{}"'.format(self.chan))
        freq = self._dev.query('ENTER')

        sent = "The measured frequency is: {} Hz.\n".format(freq)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return freq

    #===============================================================
    def set_attn(self, attn = None):
        """Sets attenuation to 1 or 20.

        Returns attenuation.

        Input parameters:
        attn - atenuation level:
        1, '1' or 2, '2', 20, '20'
        """
        if attn == None:
            attn = int(input("Enter an attenuation level:\n1 - 1\n2 - 20\n"))

        if attn in [1,'1']:
            attn = 1
            attnl = 0
        elif attn in [2, '2', 20, '20']:
            attn = 20
            attnl = 1
        else:
            raise ValueError("Please enter a valid input\n")

        self._dev.write('"AT{}"'.format(attnl))
        sent = "Attenuation has been set to: {}\n".format(attn)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return attn

    #===============================================================
    def set_filter(self, filt = None):
        """Enables or disables A-Input 100 kHz LPF.

        Returns filter status.

        Input parameters:
        filt - filter turned on or off
        1, '1', 'off', 'Off', 'OFF' or 2, '2', 'on', 'On', 'ON'
        """

        if filt == None:
            input("Turn A-Input 100kHz LPF:\n1 - OFF\n2 - ON\n")

        if filt in [1, '1', 'off', 'Off', 'OFF']:
            filt = 'OFF'
            filts = 0
        elif filt in [2, '2', 'on', 'On', 'ON']:
            filt = 'ON'
            filts = 1
        else:
            raise ValueError("Please enter a valid input\n")

        self._dev.write('"FI{}"'.format(filts))
        sent = "A-Input 100 kHz LPF is set to: {}.\n".format(filt)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return filt

    #===============================================================
    def initial(self):
        """Resets abd gi ti Default state.

        """

        self._dev.write('"IN"')
        sent = "Device has been reset.\n"
        sentence = self._sent + sent
        print(sentence)
        self._write_sent(sentence)

    #===============================================================
    # PRIVATE METHODS
    #===============================================================
    def _sel_chan(self, chan = None):
        """Select channel.

        Returns channel number.

        Input parameters:
        chan - select channel:
        1, '1', 'A' or 2, '2', 'B'

        """
        if chan == None:
            chan = input("Select a channel:\n1 - A\n2 - B\n")

        if chan in [1,'1','A']:
            chan = 1
        elif chan in [2, '2', 3, '3', 'B']:
            chan = 3
        else:
            raise ValueError("Please enter a valid input\n")

        self.chan = chan

        self._sent = "Time: " + str(self.time) + "\nAddress: " + str(self.addr) + "\nChannel: " + str(self.chan) + "\n"

        sent = "The selected channel is: {}\n".format(chan)
        sentence = self._sent + sent
        print(sentence)
        if self.fname != None:
            self._write_sent(sentence)

        return chan
