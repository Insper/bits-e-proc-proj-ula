#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from myhdl import *

from components import *


@block
def toplevel(LEDR, SW, KEY, HEX0, HEX1, HEX2, HEX3, HEX4, HEX5, CLOCK_50, RESET_N):
    sw_s = [SW(i) for i in range(10)]
    key_s = [KEY(i) for i in range(10)]
    ledr_s = [Signal(bool(0)) for i in range(10)]

    bc0 = Signal(intbv(0)[4:])
    bc1 = Signal(intbv(0)[4:])
    hex0 = Signal(intbv(0)[7:])
    hex1 = Signal(intbv(0)[7:])

    ic1 = bin2bcd(SW, bc1, bc0)
    ihex1 = bin2hex(hex1, bc1)
    ihex0 = bin2hex(hex0, bc0)

    # ---------------------------------------- #
    @always_comb
    def comb():
        for i in range(len(ledr_s)):
            LEDR[i].next = ledr_s[i]

    return instances()


LEDR = Signal(intbv(0)[10:])
SW = Signal(intbv(0)[10:])
KEY = Signal(intbv(0)[4:])
HEX0 = Signal(intbv(1)[7:])
HEX1 = Signal(intbv(1)[7:])
HEX2 = Signal(intbv(1)[7:])
HEX3 = Signal(intbv(1)[7:])
HEX4 = Signal(intbv(1)[7:])
HEX5 = Signal(intbv(1)[7:])
CLOCK_50 = Signal(bool())
RESET_N = ResetSignal(0, active=0, isasync=True)

top = toplevel(LEDR, SW, KEY, HEX0, HEX1, HEX2, HEX3, HEX4, HEX5, CLOCK_50, RESET_N)
top.convert(hdl="verilog")
