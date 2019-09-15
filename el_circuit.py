#!env python

import json
from operator import mul

class R(object):
    def __init__(self, resistor):
        self.resistor = float(resistor)
        self.voltage = None
        self.current = None
        self.rtype = "resistor"

    def set_voltage(self, voltage):
        """
        Set voltage for resistor and calculate current
        """
        self.voltage = float(voltage)
        self.current = self.voltage / self.resistor

    def get_rvc(self):
        """
        Return tuple (resistor, voltage, current)
        """
        return {self.rtype: self.resistor, "voltage": self.voltage, "current": self.current}

    def rprint(self):
        jd = json.dumps(self.get_rvc(), indent=4)
        print jd

class RP(R):
    def __init__(self, *resistors):
        self.voltage = None
        self.current = None
        self.resistors = []
        self.rtype = "parallel"
        for resistor in resistors:
            if type(resistor) not in (R, RP, RS):
                self.resistors.append(R(resistor))
            else:
                self.resistors.append(resistor)
        self.resistor = self.get_p_resistor()

    def get_p_resistor2(self, r1, r2):
        return r1* r2 / (r1 + r2)

    def get_p_resistor(self):
        ress = [res.resistor for res in self.resistors]
        return reduce(self.get_p_resistor2, ress)

    def set_voltage(self, voltage):
        R.set_voltage(self, voltage)
        for res in self.resistors:
            res.set_voltage(voltage)

    def get_rvc(self):
        rvc = [res.get_rvc() for res in self.resistors]
        return [R.get_rvc(self), rvc]

class RS(R):
    def __init__(self, *resistors):
        self.voltage = None
        self.current = None
        self.resistors = []
        self.rtype = "serial"
        for resistor in resistors:
            if type(resistor) not in (R, RP, RS):
                self.resistors.append(R(resistor))
            else:
                self.resistors.append(resistor)
        self.resistor = self.get_s_resistor()

    def get_s_resistor(self):
        ress = [res.resistor for res in self.resistors]
        return sum(ress)

    def set_voltage(self, voltage):
        R.set_voltage(self, voltage)
        for res in self.resistors:
            res.set_voltage(voltage * res.resistor / self.resistor)

    def get_rvc(self):
        rvc = [res.get_rvc() for res in self.resistors]
        return [R.get_rvc(self), rvc]


RR = RS(7, RP(5, RS(RP(4,3),4,RP(4,6))))
RR.set_voltage(25)
RR.rprint()

#RR.set_voltage(20)
#RR.rprint()
