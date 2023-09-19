#!/usr/bin/env python3
import random
import os
import pytest
from myhdl import block, instance, Signal, intbv, delay, bin
from .ula import *

try:
    from telemetry import telemetryMark

    pytestmark = telemetryMark()
except ImportError as err:
    print("Telemetry não importado")


def source(name):
    dir = os.path.dirname(__file__)
    src_dir = os.path.join(dir, ".")
    return os.path.join(src_dir, name)


random.seed(5)
randrange = random.randrange


@pytest.mark.telemetry_files(source("ula.py"))
def test_ula():
    x = Signal(modbv(1)[16:])
    y = Signal(modbv(2)[16:])
    saida = Signal(modbv(0)[16:])
    control = Signal(modbv(0))
    zr = Signal(bool(0))
    ng = Signal(bool(0))
    ula_1 = ula(x, y, control, zr, ng, saida)

    @instance
    def stimulus():
        control.next = 0b000010
        yield delay(10)
        assert saida == x + y

        control.next = 0b000000
        yield delay(10)
        assert saida == (x & y)

        control.next = 0b100010
        yield delay(10)
        assert saida == y

        control.next = 0b001010
        yield delay(10)
        assert saida == x

        control.next = 0b100110
        yield delay(10)
        assert saida == ~y

        control.next = 0b011010
        yield delay(10)
        assert saida == ~x

        control.next = 0b101010
        yield delay(10)
        assert saida == 0

        control.next = 0b101000
        yield delay(10)
        assert saida == 0

        control.next = 0b101001
        yield delay(10)
        assert saida == intbv(-1)[16:]

        # ------ zr ng --------#
        assert zr == 0 and ng == 1

        control.next = 0b101000
        yield delay(10)
        assert zr == 1 and ng == 0

        control.next = 0b000010
        yield delay(10)
        assert zr == 0 and ng == 0

    sim = Simulation(ula_1, stimulus)
    traceSignals(ula_1)
    sim.run()


@pytest.mark.telemetry_files(source("ula.py"))
def test_zerador():
    z = Signal(bool(0))
    a = Signal(modbv(0))
    y = Signal(modbv(0))
    zerador_1 = zerador(z, a, y)

    @instance
    def stimulus():
        a.next = randrange(2**16 - 1)
        z.next = 0
        yield delay(10)
        assert y == a
        z.next = 1
        yield delay(10)
        assert y == 0

    sim = Simulation(zerador_1, stimulus)
    sim.run()


@pytest.mark.telemetry_files(source("ula.py"))
def test_comparador():
    a = Signal(modbv(0))
    ng = Signal(bool(0))
    zr = Signal(bool(0))
    comparador_1 = comparador(a, zr, ng, 16)

    @instance
    def stimulus():
        a.next = 0
        yield delay(10)
        assert ng == 0 and zr == 1
        a.next = 0xFFFF
        yield delay(10)
        assert ng == 1 and zr == 0
        a.next = 32
        yield delay(10)
        assert ng == 0 and zr == 0

    sim = Simulation(comparador_1, stimulus)
    sim.run()


@pytest.mark.telemetry_files(source("ula.py"))
def test_inversor():
    z = Signal(bool(0))
    a = Signal(modbv(0))
    y = Signal(modbv(0))

    inversor_1 = inversor(z, a, y)

    @instance
    def stimulus():
        for i in range(256):
            a.next = randrange(2**16 - 1)
            z.next = randrange(2)
            yield delay(1)
            if z == 0:
                assert a == y
            else:
                assert a == ~y

    sim = Simulation(inversor_1, stimulus)
    sim.run()


@pytest.mark.telemetry_files(source("ula.py"))
def test_inc():
    a = Signal(modbv(0))
    q = Signal(modbv(0))

    inc16_1 = inc(a, q)

    @instance
    def stimulus():
        for i in range(256):
            a.next = randrange(2**16 - 2)
            yield delay(1)
            assert q == a + 1

    sim = Simulation(inc16_1, stimulus)
    sim.run()


@pytest.mark.telemetry_files(source("ula.py"))
def test_add():
    a = Signal(modbv(0))
    b = Signal(modbv(0))
    q = Signal(modbv(0))

    add16_1 = add(a, b, q)

    @instance
    def stimulus():
        for i in range(256):
            a.next, b.next = [randrange(2**15 - 1) for i in range(2)]
            yield delay(1)
            assert q == a + b

    sim = Simulation(add16_1, stimulus)
    sim.run()
