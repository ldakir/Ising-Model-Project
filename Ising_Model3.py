#Lamiaa Dakir
from __future__ import division, print_function
from random import random, randrange
from numpy import ones, roll,arange
from pylab import plot, ylabel, show
from math import exp
import matplotlib.pyplot as plt
import numpy as np

"""
Adding an external magnetic field to the system 

"""
N=15 # NxN size of the lattice
steps= 10000 #number of steps 
J= 1 #Exchange energy
u=1 #Magnetic moment
h= 0.1 #external magnetic field

#Setting the initial spins randomly 
s=ones([N,N], int)
for i in range(N):
	for j in range(N):	
 		if random()< 0.5:
  			s[i,j]=1	
  		else: 
   			s[i,j]=-1
   			
def M(s):	
	sum=0
	for i in range(N):
		for j in range(N):
			sum += s[i,j]
	return sum
	
#Function that calculates the total energy
def E(s,h): #h is the external magnetic field
	E1= 0
	E2= 0
	for ix in range(N-1):
		for jx in range(N):
			E1 += s[ix,jx]*s[ix+1,jx]
	for iy in range(N):
		for jy in range(N-1):
			E2 += s[iy,jy]*s[iy,jy+1]
	return (-J*(E1+E2)-u*h*M(s))	

	
#Monte Carlo Algorithm
def data(T,h): 
	#Choosing a random spin to flip 
	i= randrange(N) 
	j= randrange(N)
	Ei=E(s,h)		#Initial energy 
	s[i,j] *=-1
	Ef=E(s,h)    #Final energy
	deltaE= Ef-Ei #energy change
	
	#Deciding whether to accept or reject the flip
	if random()< exp(-deltaE/T):
		s[i,j] *=1
	else:
 		s[i,j] *=-1
 	return (E(s,h),M(s)) #return energy and magnetization



#Defining a function that calculates the average of the data
def average(data):
	sum=0
	start=30
	for i in range(start,steps):
		sum += data[i]
	return sum/(steps-start)

"""
Calculating the average energy for a constant external magnetic field h and different temperatures 

"""

eplot_T=[] #Array that stores the average energy
Temps=[] #Temperatures
E_error=[] 	#Error ranges for energy

for T in arange(1,7,0.1):
	Temps.append(T)
	E_data=[]
	#Repeating the Monte Carlo algorithm "steps" times	
	for k in range (steps):	
		E_data.append(data(T,h))
		
	eplot_T.append(average(E_data))
	E_error.append(max(E_data)-min(E_data))

	
#Plotting the average energy for a constant h as a function of temperature 
plt.errorbar(Temps, eplot, yerr=E_error, fmt='o')
plt.xlabel("Temperature")
plt.ylabel("Average energy")
plt.title("Energy as a function of temperature")
plt.savefig('E_Temperature.png')
plt.show()

"""
Calculating the average energy for different external magnetic fields h and a constant temperature

"""
eplot_h=[]
mplot_h_1=[]
mplot_h_2=[]
mplot_h_3=[]
external_m=[]
for h in arange(-5,5,0.5):
	external_m.append(h)
 	E_data=[]
 	M_data1=[]
# 	M_data2=[]
# 	M_data3=[]
	for k in range (steps):
 		E_data.append(data(1,h)[0])
		M_data1.append(data(1,h)[1])
# 		M_data2.append(data(2.2,h)[1])
# 		M_data3.append(data(5,h)[1])
	eplot_h.append(average(E_data))
	mplot_h_1.append(average(M_data1))
# 	mplot_h_2.append(average(M_data2))
# 	mplot_h_3.append(average(M_data3))
	

# Plotting the average energy for a constant T as a function of external magnetic field h
plt.plot(external_m, eplot_h,'g')
plt.xlabel("External magnetic field")
plt.ylabel("Average energy")
plt.title("Energy as a function of external magnetic field")
plt.savefig('E_h.png')
plt.show()	

#Plotting the average energy for T=1, T=2.2 and T= 5 as a function of external magnetic field h
plt.plot(external_m, mplot_h_1, label= 'T=1')
# plt.plot(external_m, mplot_h_2, label= 'T=2.2')
# plt.plot(external_m, mplot_h_3, label= 'T=15')
plt.legend()
plt.xlabel("External magnetic field")
plt.ylabel("Average magnetization")
plt.title("Magnetization as a function of external magnetic field")
plt.savefig('E_h_T.png')
plt.show()	
	
		

