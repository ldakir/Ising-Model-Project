#Lamiaa Dakir
from __future__ import division, print_function
from random import random, randrange
from numpy import ones, roll,arange
from pylab import plot, ylabel, show
from math import exp
import matplotlib.pyplot as plt
import numpy as np

"""
Varying the temperature of the system

"""

N=15 # NxN size of the lattice
steps= 10000 #number of steps 
J= 1 #Exchange energy

#Setting the initial state of spins  
s=ones([N,N], int)
for i in range(N):
	for j in range(N):	
 		if random()< 0.5:
  			s[i,j]=1	
  		else: 
   			s[i,j]=-1
   			

#Function that calculates the total energy
def E(s):
	E1= 0
	E2= 0
	for ix in range(N-1):
		for jx in range(N):
			E1 += s[ix,jx]*s[ix+1,jx]
	for iy in range(N):
		for jy in range(N-1):
			E2 += s[iy,jy]*s[iy,jy+1]
	return (-J*(E1+E2))	
	
#Function that calculates the total magnetization
def M(s):	
	sum=0
	for i in range(N):
		for j in range(N):
			sum += s[i,j]
	return sum

#Calculating the final energy to make the code run faster
def Ef(s,Ei,i,j):
	if i==0 and j==0:
		Ef= Ei-2*s[i,j]*(s[i+1,j]+s[i,j+1])
	elif i== N-1 and j==0:
		Ef= Ei-2*s[i,j]*(s[i-1,j]+s[i,j+1])
	elif i==0 and j==N-1:
		Ef= Ei-2*s[i,j]*(s[i+1,j]+s[i,j-1])
	elif i==N-1 and j==N-1:
		Ef=Ei-2*s[i,j]*(s[i-1,j]+s[i,j-1])
	elif j==0:
		Ef=Ei-2*s[i,j]*(s[i-1,j]+s[i+1,j]+s[i,j+1])
	elif i==0:
		Ef=Ei-2*s[i,j]*(s[i+1,j]+s[i,j-1]+s[i,j+1])
	elif j== N-1:
		Ef=Ei-2*s[i,j]*(s[i-1,j]+s[i+1,j]+s[i,j-1])
	elif i== N-1:
		Ef= Ei-2*s[i,j]*(s[i-1,j]+s[i,j-1]+s[i,j+1])
	else:
		Ef=Ei-2*s[i,j]*(s[i-1,j]+s[i+1,j]+s[i,j-1]+s[i,j+1])
	return Ef
	
#Monte Carlo Algorithm
def data(T): 
	#Choosing a random spin to flip 
	i= randrange(N) 
	j= randrange(N)
	Ei=E(s)		#Initial energy 
	s[i,j] *=-1
	E_final= Ef(s,Ei,i,j)    #Final energy
	deltaE= E_final-Ei #energy change
	
	#Deciding whether to accept or reject the flip
	if random()< exp(-deltaE/T):
		s[i,j] *=1
	else:
 		s[i,j] *=-1
 	return (E(s), M(s),s) #return energy, magnetization and spins



#Defining a function that calculates the average of the data
def average(data):
	sum=0
	start=200
	for i in range(start,steps):
		sum += data[i]
	return sum/(steps-start)


#Calculating the average energy and magnetization for different temperatures

eplot=[] #Array that stores the average energy
mplot=[] #Array that stores the average magnetization

Temps=[] #Temperatures

E_error=[] 	#Error ranges for energy
M_error=[]	#Error ranges for magnetization

for T in arange(1,5,0.1):
	Temps.append(T)
	E_data=[]
	M_data=[]
	#Repeating the Monte Carlo algorithm "steps" times	
	for k in range (steps):	
		E_data.append(data(T)[0])
		M_data.append(data(T)[1])
		
	eplot.append(average(E_data))
	mplot.append(average(M_data))
	
	E_error.append(max(E_data)-min(E_data))
	M_error.append(max(M_data)-min(M_data))


# Plotting the average energy as a function of temperature 
plt.errorbar(Temps, eplot, yerr=E_error, fmt='ro')
plt.xlabel("Temperature")
plt.ylabel("Average energy")
plt.title("Energy as a function of temperature")
plt.savefig('E_Temperature.png')
plt.show()

#Plotting the average magnetization as a function of temperature 
plt.errorbar(Temps, mplot, yerr=M_error, fmt='bo')
plt.xlabel("Temperature")
plt.ylabel("Average magnetization")
plt.title("Magnetization as a function of temperature")
plt.savefig('M_Temperature.png')
plt.show()