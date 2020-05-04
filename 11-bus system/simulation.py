#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Run from a Python command prompt as

        python simulation.py <case>

    where <case> can be

        A, for generators with no PSS, constant excitation and constant torque,
        B, for                 no PSS, AVR                 and constant torque,
        C, for  PSS based on residues, AVR                 and constant torque,
        D, for           Kundur's PSS, AVR                 and constant torque.

    Some notes on this simulation:

        - PSS parameters for case D were taken from

            Klein, M., Rogers, G. J., Moorty, S., & Kundur, P. (1992).
            Analytical investigation of factors influencing power system
            stabilizers performance. IEEE Transactions on Energy Conversion,
            7(3), 382-390.

        - The observed quantity is the speed of generator G3.

'''

import pyramses
import os, glob
import sys

# Process input arguments
sim_case = sys.argv[1]

# Delete output files from previous simulations
files = glob.glob('output/*')
for f in files:
    os.remove(f)

# Initialize case description
case = pyramses.cfg()

# Define input files
if sim_case == 'A':
    case.addData('input\\sync_A.dat')
elif sim_case == 'B':
    case.addData('input\\sync_B.dat')
elif sim_case == 'C':
    case.addData('input\\sync_C.dat')
elif sim_case == 'D':
    case.addData('input\\sync_D.dat')
else:
    print('The first script argument should be either A, B, or C. See file ' \
          + 'header for details.')

case.addData('input\\syst.dat')
case.addData('input\\volt_load.dat')
case.addData('input\\settings.dat')
case.addObs('input\\obs.dat')
case.addDst('input\\load_increase.dst')

# Define output files
case.addTrj('output\\obs.trj')
case.addInit('output\\init.trace')
case.addOut('output\\output.trace')

# Create simulator instance
ram = pyramses.sim()

# Run simulation
ram.execSim(case)

# Plot machine speed
ext = pyramses.extractor(case.getTrj())
ext.getSync('G3').S.plot()

# Remove files from run-time observables and other temporary files
temp_files = [f for f in glob.glob('./*') if 'temp' in f or 'pyramses' in f]
for f in temp_files:
    os.remove(f)

# Delete output files (except init.trace and output.trace)
files = glob.glob('output/*')
for f in files:
    if f != case.getInit() and f != case.getOut():
        os.remove(f)
