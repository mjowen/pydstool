""" EXAMPLE: 3-Box Brusselator

    Drew LaMar, December 2005

    NOTE: Problems following new branch from BP1 (repeats curve).
"""

from PyDSTool import *

pars = {'D1': 1.0 , 'D2': 10.0, 'A': 2.1, 'B': 3.5, 'lambda': 5}

tdomain = [0,50]

icdict = {'X1': 1.087734, 'X2': 1.087734, 'X3': 4.124552, \
		  'yy1': 1.8488063, 'yy2': 1.8488063, 'yy3': 1.0389936}

# Set up model
X1str = 'D1*(X2 - 2*X1 + X3) + lambda*(A - (B+1)*X1 + pow(X1,2)*yy1)'
X2str = 'D1*(X3 - 2*X2 + X1) + lambda*(A - (B+1)*X2 + pow(X2,2)*yy2)'
X3str = 'D1*(X1 - 2*X3 + X2) + lambda*(A - (B+1)*X3 + pow(X3,2)*yy3)'
yy1str = 'D2*(yy2 - 2*yy1 + yy3) + lambda*(B*X1 - pow(X1,2)*yy1)'
yy2str = 'D2*(yy3 - 2*yy2 + yy1) + lambda*(B*X2 - pow(X2,2)*yy2)'
yy3str = 'D2*(yy1 - 2*yy3 + yy2) + lambda*(B*X3 - pow(X3,2)*yy3)'

DSargs = args(name='Brusselator')
DSargs.tdomain = tdomain
DSargs.pars = pars
DSargs.varspecs = {'X1': X1str, 'X2': X2str, 'X3': X3str, 'yy1': yy1str, 'yy2': yy2str, 'yy3': yy3str}
DSargs.xdomain = {'X1': [0, 50], 'X2': [0, 50], 'X3': [0, 50], 'yy1': [0, 50], 'yy2': [0, 50], 'yy3': [0, 50]}
DSargs.ics = icdict

testDS = Generator.Vode_ODEsystem(DSargs)

# Set up continuation class
PyCont = ContClass(testDS)

PCargs = args(name='EQ1', type='EP-C')
PCargs.freepars = ['lambda']
PCargs.StepSize = 5e-3
PCargs.LocBifPoints = ['BP','LP']
PCargs.verbosity = 2
PCargs.SaveEigen = True
PyCont.newCurve(PCargs)

print('Computing curve...')
start = perf_counter()
PyCont['EQ1'].forward()
print('done in %.3f seconds!' % (perf_counter()-start))

# Plot
PyCont['EQ1'].display(('lambda','X1'), stability=True)
PyCont.plot.toggleAll('off', byname='P1')
show()
