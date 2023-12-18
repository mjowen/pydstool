# Self exciting hodgkin huxley model for limit cycle continuation

from PyDSTool import *
import matplotlib.pyplot as plt

icdict = {'V': -75, 'm': 0.05, 'h': 0.6, 'n': 0.325, 's': 0.3}

pars = {'am1':0.1, 'am2':50, 'am3':10, 'bm1':4, 'bm2':75, 'bm3':18, 'ah1':0.07, 'ah2':75, 'ah3':20,
'bh1':45, 'bh2':10, 'gna':120, 'Ena':40, 'an1':0.01, 'an2':65, 'an3':10, 'bn1':0.125, 'bn2':75,
'bn3':80, 'gk' :25, 'Ek' :-87, 'as1':0.01, 'as2':65, 'as3':10, 'bs1':0.125, 'bs2':75, 'bs3':80,
'gs' :10, 'Es' :-87, 'gl' :0.3, 'El' :-64.387, 'Cm' :1}

mstr = '-am1*(V+am2)/(exp(-(V+am2)/am3)-1)*(1-m)-bm1*exp(-(V+bm2)/bm3)*m'
hstr = 'ah1*exp(-(V+ah2)/ah3)*(1-h)-1/(exp(-(V+bh1)/bh2)+1)*h'
nstr = '-an1*(V+an2)/(exp(-(V+an2)/an3)-1)*(1-n)-bn1*exp((V+bn2)/bn3)*n'
sstr = '-as1*(V+as2)/(exp(-(V+as2)/as3)-1)*(1-s)-bs1*exp(-(V+bs2)/bs3)*s'
Vstr = '-(gna*pow(m,3)*h*(V-Ena)+gk*pow(n,4)*(V-Ek)+gs*pow(s,4)*(V-Es)+gl*(V-El))/Cm'

DSargs = args(name='hh')
DSargs.pars = pars
DSargs.varspecs = {'V': Vstr, 'm': mstr, 'h': hstr, 'n': nstr, 's': sstr}
DSargs.ics = icdict
DSargs.pdomain = {'gna': [100,140]}
DSargs.tdata = [0,100]

DS = Generator.Radau_ODEsystem(DSargs)
traj = DS.compute('demo')
pts = traj.sample()

plt.figure()
plt.plot(pts['t'], pts['V'])
plt.title('gk=25 - no oscillations')
plt.savefig('trajectory1.png')

plt.figure()
plt.plot(pts['t'], pts['s'], label='s')
plt.plot(pts['t'], pts['m'], label='m')
plt.plot(pts['t'], pts['h'], label='h')
plt.plot(pts['t'], pts['n'], label='n')
plt.title('gk=25 - no oscillations')
plt.savefig('probabilities1.png')

DS.set(pars={'gk': 13})
traj = DS.compute('demo-lc')
pts = traj.sample()

plt.figure()
plt.plot(pts['t'], pts['V'])
plt.title('gk=13 - oscillations')
plt.savefig('trajectory2.png')

plt.figure()
plt.plot(pts['t'], pts['s'], label='s')
plt.plot(pts['t'], pts['m'], label='m')
plt.plot(pts['t'], pts['h'], label='h')
plt.plot(pts['t'], pts['n'], label='n')
plt.title('gk=13 - oscillations but fast convergence')
plt.savefig('probabilities2.png')

DS.set(pars={'as1': 1e-6, 'bs1': 1e-4}, tdata=[0,26000])
# traj = DS.compute('demo-lc-slow')
# pts = traj.sample()

# plt.figure()
# plt.plot(pts['t'], pts['V'])
# plt.title('gk=13 - slow convergence')
# plt.savefig('trajectory3.png')

# plt.figure()
# plt.plot(pts['t'], pts['s'], label='s')
# plt.plot(pts['t'], pts['m'], label='m')
# plt.plot(pts['t'], pts['h'], label='h')
# plt.plot(pts['t'], pts['n'], label='n')
# plt.title('gk=13 - oscillations with slow convergence')
# plt.savefig('probabilities3.png')

# plt.figure()
# plt.plot(pts['V'], pts['s'])
# plt.title('oscillations in s')
# plt.savefig('slows.png')

DS.set(tdata = [0,20], ics = {'V': -18.927341, 'm': 0.96708202, 'h': 0.023748446, 'n': 0.65769453, 's': 0.12350425})
traj = DS.compute('demo-lc')
pts = traj.sample()

plt.figure()
plt.plot(pts['t'], pts['V'])
plt.title('one pulse')
plt.savefig('trajectory4.png')

#get pointset from cycle
cycle = pts

P = ContClass(DS)

PCargs = args(name='lc', type='LC-C')
PCargs.freepars = ['gna']
PCargs.StepSize = 0.01
PCargs.MaxNumPoints = 1000
PCargs.MaxStepSize = 1
PCargs.VarTol = 1e-3
PCargs.FuncTol = 1e-3
PCargs.initcycle = cycle
PCargs.LocBifPoints = 'all' #Helps with stability (lots of nearby LP and PD) - avoids MX termination points immediatly appearing and stopping continuation
PCargs.StopAtPoints = 'B'
PCargs.verbosity = 0
P.newCurve(PCargs)

P['lc'].forward()
P['lc'].backward()
sol = P['lc'].sol

plt.clf()
P.display(coords=('gna','_T'))
plt.savefig('cont.png')
plt.clf()
#info(P['lc'])
