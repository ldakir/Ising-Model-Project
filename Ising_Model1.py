#Lamiaa Dakir
from __future__ import division, print_function
from random import random, randrange
from numpy import ones, roll, exp
from pylab import plot, ylabel, show
from matplotlib import colors
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

"""
Simulation of the ising model using the Monte Carlo method

"""
N=15 # NxN size of the lattice
steps= 100000 #number of steps 
J= 1 #Exchange energy

#Setting the initial spins randomly 
s=ones([N,N], int)
for i in range(N):
	for j in range(N):	
 		if random()< 0.5:
  			s[i,j]=1	
  		else: 
   			s[i,j]=-1
   			
#Figure of the initial state of spins	
# fig = plt.figure()
# X, Y = np.meshgrid(range(N), range(N)) #creating a grid NxN
# mesh = plt.pcolormesh(X, Y, s, cmap='Spectral')
# plt.colorbar()
# plt.savefig('initial_spins.png')
# plt.show()

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
	
#Calculating the final energy Ef to make the code run faster
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
 	
 	
	
eplot=[] #Array to store the energy
mplot=[] #Array to store the magnetization

#eplot3=[] #Array to store the energy
#mplot3=[] #Array to store the magnetization

#eplot5=[] #Array to store the energy
#mplot5=[] #Array to store the magnetization
#Repeating the Monte Carlo algorithm "steps" times
for k in range(steps):
	eplot.append(data(1)[0]) 
	mplot.append(data(1)[1])

# Plotting the energy as a function of iterations 	
plt.plot(eplot, 'r')
plt.xlabel("Iterations")
plt.ylabel("Energy")
plt.title("Evolution of the energy of the system for T=4")
plt.savefig('E.png')
plt.show()

# Plotting the magnetization as function of iterations
plt.plot(mplot, 'b')
plt.xlabel("Iterations")
plt.ylabel("Magnetization")
plt.title("Evolution of the magnetization of the system for T=4")
plt.savefig('M.png')
plt.show()



#Making an animation of the Monte Carlo algorithm

def data_animation(T):
	#Choosing a random spin to flip 
	i= randrange(N) 
	j= randrange(N)
	
	Ei=E(s)		#Initial energy 
	s[i,j] *=-1
	Ef= E(s)    #Final energy
	deltaE= Ef-Ei #energy change
	
	#Deciding whether to accept or reject the flip
	if random()< exp(-deltaE/T):
		s[i,j] *=1
	else:
 		s[i,j] *=-1
 		
 	mesh.set_array(s.ravel())
	return (mesh),


#Figure of the final state of spins	
# fig = plt.figure()
# X, Y = np.meshgrid(range(N), range(N)) #creating a grid NxN
# mesh = plt.pcolormesh(X, Y, s, cmap='Spectral')
# plt.colorbar()
# plt.savefig('final_spins4.png')
# plt.show()


#Animation of the spins as the Monte Carlo algorithm is repeated
a = animation.FuncAnimation(fig, data_animation, frames = steps ,interval=1,blit=True)
#a.save('animation.htm') #Saving animation
plt.show()