#!/usr/bin/env python3

from .components import *
import random
import pytest 
import os

try:
    from telemetry import telemetryMark
    pytestmark = telemetryMark()
except ImportError as err:
    print("Telemetry não importado")

random.seed(5)
randrange = random.randrange

def source(name):
	dir = os.path.dirname(__file__)
	src_dir = os.path.join(dir, '.' )
	return os.path.join(src_dir, name)

# -------------------------------------
# -- TESTS
# -------------------------------------

@pytest.mark.telemetry_files(source('components.py'))
def test_and16():
    q, a, b = [Signal(intbv(0)) for i in range(3)]
    and16_1 = and16(a, b, q)

    @instance
    def stimulus():
        for i in range(0, 4):
            a.next = randrange(2**16 - 1)
            b.next = randrange(2**16 - 1)
            yield delay(1)
            assert q.val == (a and b)

    sim = Simulation(and16_1, stimulus)
    sim.run()

@pytest.mark.telemetry_files(source('components.py'))
def test_or8way():
    q = Signal(bool(0))
    sig = Signal(intbv(0, max=2**8 - 1))
    dut = or8way(sig(0), sig(1), sig(2), sig(3), sig(4), sig(5), sig(6), sig(7), q)

    @instance
    def stimulus():
        for i in range(0, 32):
            sig.next = randrange(2**8 - 2) + 1
            yield delay(1)
            assert q.val
        sig.next = 0
        yield delay(1)
        assert q.val == 0

    sim = Simulation(dut, stimulus)
    sim.run()

@pytest.mark.telemetry_files(source('components.py'))
def test_orNway():
    q = Signal(bool(0))
    i = Signal(intbv(0, max=2**16 - 1))
    orNway_1 = orNway(i, q)

    @instance
    def stimulus():
        i.next = randrange(2**16 - 2) + 1
        yield delay(1)
        assert q.val
        i.next = 0
        yield delay(1)
        assert q.val == 0

    sim = Simulation(orNway_1, stimulus)
    sim.run()

@pytest.mark.telemetry_files(source('components.py'))
def test_barrelShifter():
    q = Signal(intbv(0))
    a = Signal(intbv(8))
    size = Signal(intbv(0))
    dir = Signal(bool(0))
    barrelShifter_1 = barrelShifter(a, dir, size, q)

    @instance
    def stimulus():
        for i in range(0, 32):
            a.next = randrange(2**16 - 1)
            dir.next = randrange(2)
            yield delay(1)
            if dir.val:
                assert q.val == a << size
            else:
                assert q.val == a >> size

    sim = Simulation(barrelShifter_1, stimulus)
    sim.run()

@pytest.mark.telemetry_files(source('components.py'))
def test_mux2way():
    q, a, b = [Signal(intbv(0)) for i in range(3)]
    muxIn = [a, b]
    sel = Signal(bool(0))
    mux2way_1 = mux2way(q, a, b, sel)

    @instance
    def stimulus():

        for i in range(32):
            a.next, b.next = [randrange(8) for i in range(2)]
            sel.next = randrange(2)
            yield delay(1)
            assert q.val == muxIn[sel.val]

    sim = Simulation(mux2way_1, stimulus)
    sim.run()

@pytest.mark.telemetry_files(source('components.py'))
def test_mux4way():
    q, a, b, c, d = [Signal(intbv(0)) for i in range(5)]
    muxIn = [a, b, c, d]
    sel = Signal(intbv(0))
    mux4way_1 = mux4way(q, a, b, c, d, sel)

    @instance
    def stimulus():
        for i in range(32):
            a.next, b.next, c.next, d.next = [randrange(8) for i in range(4)]
            sel.next = randrange(len(muxIn))
            yield delay(1)
            assert q.val == muxIn[sel.val]

    sim = Simulation(mux4way_1, stimulus)
    sim.run()

@pytest.mark.telemetry_files(source('components.py'))
def test_mux8way():
    q, a, b, c, d, e, f, g, h = [Signal(intbv(0)) for i in range(9)]
    muxIn = [a, b, c, d, e, f, g, h]
    sel = Signal(intbv(0))
    mux8way_1 = mux8way(q, a, b, c, d, e, f, g, h, sel)

    @instance
    def stimulus():
        for i in range(32):
            a.next, b.next, c.next, d.next = [randrange(8) for i in range(4)]
            e.next, f.next, g.next, h.next = [randrange(8) for i in range(4)]
            sel.next = randrange(len(muxIn))
            yield delay(1)
            assert q.val == muxIn[sel.val]

    sim = Simulation(mux8way_1, stimulus)
    sim.run()

@pytest.mark.telemetry_files(source('components.py'))
def test_deMux2way():
    a, q0, q1, sel = [Signal(intbv(0)) for i in range(4)]
    deMuxOuts = [q0, q1]
    deMux2way_1 = deMux2way(a, q0, q1, sel)

    @instance
    def stimulus():
        for i in range(32):
            a.next = randrange(32)
            sel.next = randrange(2)
            yield delay(1)
            assert deMuxOuts[sel.val] == a.val
            assert deMuxOuts[1 - sel.val] == 0

    sim = Simulation(deMux2way_1, stimulus)
    sim.run()

@pytest.mark.telemetry_files(source('components.py'))
def test_deMux4way():
    a, q0, q1, q2, q3, sel = [Signal(intbv(0)) for i in range(6)]
    deMuxOuts = [q0, q1, q2, q3]
    deMux4way_1 = deMux4way(a, q0, q1, q2, q3, sel)

    @instance
    def stimulus():
        for i in range(32):
            a.next = randrange(32)
            sel.next = randrange(2)
            yield delay(1)
            for i in range(len(deMuxOuts)):
                if i == sel.val:
                    assert deMuxOuts[i] == a.val
                else:
                    assert deMuxOuts[i] == 0

    sim = Simulation(deMux4way_1, stimulus)
    sim.run()

@pytest.mark.telemetry_files(source('components.py'))
def test_deMux8way():
    a, q0, q1, q2, q3, q4, q5, q6, q7, sel = [Signal(intbv(0)) for i in range(10)]
    deMuxOuts = [q0, q1, q2, q3, q4, q5, q6, q7]
    deMux8way_1 = deMux8way(a, q0, q1, q2, q3, q4, q5, q6, q7, sel)

    @instance
    def stimulus():
        for i in range(32):
            a.next = randrange(32)
            sel.next = randrange(2)
            yield delay(1)
            for i in range(len(deMuxOuts)):
                if i == sel.val:
                    assert deMuxOuts[i] == a.val
                else:
                    assert deMuxOuts[i] == 0

    sim = Simulation(deMux8way_1, stimulus)
    sim.run()

@pytest.mark.telemetry_files(source('components.py'))
def test_bin2bcd():
    bc0 = Signal(intbv(0)[4:])
    bc1 = Signal(intbv(0)[4:])
    b = Signal(intbv(0)[9:])

    ic1 = bin2bcd(b, bc1, bc0)

    @instance
    def stimulus():
        yield delay(1)

    sim = Simulation(ic1, stimulus)
    sim.run()
