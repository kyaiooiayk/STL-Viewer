#====================================================================
#====================================================================
'''
THIS SCRIPT CONTAINS ALL THE UTILITIES NEEDED TO PARAMETRISE A 
PROFILE USING THE FFD - FREE FORM DEFORMATION
'''
#====================================================================
#====================================================================



#=================
#IMPORTING MODULES
#=================
import numpy
import numpy as np
import scipy,os
from scipy.misc import factorial as f
from scipy import optimize 
from scipy.misc import comb
from scipy import *



#=========================================
#CLASS DEFINITION AND FUNCTION DEFINITIONS
#=========================================
class PARA():
    
 
       
    #======================================================
    #DEFINITION OF THE TRIVARIATE BERNESTEIN TENSOR PRODUCT
    #======================================================
	def FFD(self,CP,xSelected,ySelected,zSelected, xLatticeMin, xLatticeMax, yLatticeMin, yLatticeMax, zLatticeMin, zLatticeMax):
	
		s, t, u = self.compute_local_coords(CP,xSelected,ySelected,zSelected, xLatticeMin, xLatticeMax, yLatticeMin, yLatticeMax, zLatticeMin, zLatticeMax)

		l = len(CP[:, 0, 0, 0]) - 1 
		m = len(CP[0, :, 0, 1]) - 1 
		n = len(CP[0, 0, :, 2]) - 1
		print("\ndegree of BPs in x,y,z"), l,m,n
		
		
		a7=0
		a8=0
		a9=0
		for ii in range(l+1):
			a4=0
			a5=0
			a6=0   
			for jj in range(m+1):
				a1=0
				a2=0
				a3=0 
				for kk in range(n+1):
					a1+=self.BPB(n, kk, u) * CP[ii, jj, kk, 0]
					a2+=self.BPB(n, kk, u) * CP[ii, jj, kk, 1]
					a3+=self.BPB(n, kk, u) * CP[ii, jj, kk, 2]
				a4+=self.BPB(m, jj, t)*a1
				a5+=self.BPB(m, jj, t)*a2
				a6+=self.BPB(m, jj, t)*a3
			a7+=self.BPB(l, ii, s)*a4
			a8+=self.BPB(l, ii, s)*a5
			a9+=self.BPB(l, ii, s)*a6

		return a7, a8, a9

    #==========================================================
    #DEFINITION OF THE BIVARIATE BERNESTEIN TENSOR PRODUCT (2D)
    #==========================================================
	def FFD_2D(self,CP,l,m,s,t):		
		a7=0
		a8=0  
		for ii in range(l+1):
			a4=0
			a5=0
			for jj in range(m+1):
				a4+=self.BPB(m, jj, t)*CP[ii, jj, 0]
				a5+=self.BPB(m, jj, t)*CP[ii, jj, 1] 
			a7+=self.BPB(l, ii, s)*a4
			a8+=self.BPB(l, ii, s)*a5

		return a7, a8
		
	def createNormalisedCoords(self, CPx, CPy, CPz, xLatticeMin, xLatticeMax, yLatticeMin, yLatticeMax, zLatticeMin, zLatticeMax):
		ax_wt = np.linspace(xLatticeMin, xLatticeMax, CPx)
		by_wt = np.linspace(yLatticeMin, yLatticeMax, CPy)
		cz_wt = np.linspace(zLatticeMin, zLatticeMax, CPz)
		
		return ax_wt, by_wt, cz_wt
				

	def createLattice(self, CPx, CPy, CPz, xLatticeMin, xLatticeMax, yLatticeMin, yLatticeMax, zLatticeMin, zLatticeMax):
	
		ax_wt, by_wt, cz_wt  = self.createNormalisedCoords(CPx, CPy, CPz, xLatticeMin, xLatticeMax, yLatticeMin, yLatticeMax, zLatticeMin, zLatticeMax)
	
		CPLattice = np.zeros((CPx, CPy, CPz, 3))
		for ii in range(CPx):
			for jj in range(CPy):
				for kk in range(CPz):
					CPLattice[ii, jj, kk ,0] = ax_wt[ii]
					CPLattice[ii, jj, kk ,1] = by_wt[jj]
					CPLattice[ii, jj, kk ,2] = cz_wt[kk]
		return CPLattice	


	def FFD_fd(self,CP,l,m,n,s,t,u):
	
		"""Compute FFD first derivative wrt CPs.
		
		dS/dDVs	
		"""
		
		a7=0
		a8=0
		a9=0
		for ii in range(l+1):
			a4=0
			a5=0
			a6=0   
			for jj in range(m+1):
				a1=0
				a2=0
				a3=0 
				for kk in range(n+1):
					a1+=self.BPB(n, kk, u) #* CP[ii, jj, kk, 0]
					a2+=self.BPB(n, kk, u) #* CP[ii, jj, kk, 1]
					a3+=self.BPB(n, kk, u) #* CP[ii, jj, kk, 2]
				a4+=self.BPB(m, jj, t)*a1
				a5+=self.BPB(m, jj, t)*a2
				a6+=self.BPB(m, jj, t)*a3
			a7+=self.BPB(l, ii, s)*a4
			a8+=self.BPB(l, ii, s)*a5
			a9+=self.BPB(l, ii, s)*a6

		return a7, a8, a9
    


                                  
    #=======================================
    #DEFINITION OF THE BERNESTEIN POLYNOMIAL
    #=======================================
	def BPB(self, n, i, coord):
		r =comb(n, i)*(1.-coord)**(n-i)*coord**i        			
		return r


    
    #=============================
    #COMPUTE THE LOCAL COORDINATES
    #=============================
	def compute_local_coords_2d(self, CP,x,y):

		XX0=np.array([min(CP[:,:,0].flatten()),min(CP[:,:,1].flatten())])

		S = np.array([max(CP[:,:,0].flatten())-min(CP[:,:,0].flatten()),0.])
		T = np.array([0.,max(CP[:,:,1].flatten())-min(CP[:,:,1].flatten())])

		s=[]
		t=[]

		XX = np.array([x[:]-XX0[0], y[:]-XX0[1]])
		#XX = np.array([x[:]-0, y[:]-0, z[:]-0])        
		s=(np.dot(np.cross(T, U), XX) / np.dot(np.cross(T, U), S))
		t=(np.dot(np.cross(S, U), XX) / np.dot(np.cross(S, U), T))
						
		return np.array(s),np.array(t)



	def compute_local_coords(self, CP,x,y,z, xLatticeMin, xLatticeMax, yLatticeMin, yLatticeMax, zLatticeMin, zLatticeMax):

		"""Compute the transformed FFD local coordinates.
		"""
		
		CPx = len(CP[:, 0, 0, 0])
		CPy = len(CP[0, :, 0, 1])
		CPz = len(CP[0, 0, :, 2])
		
		ax_wt, by_wt, cz_wt  = self.createNormalisedCoords(CPx, CPy, CPz, xLatticeMin, xLatticeMax, yLatticeMin, yLatticeMax, zLatticeMin, zLatticeMax)
				
		
		SS=np.array([abs(max(ax_wt)-min(ax_wt)),0,0,])
		TT=np.array([0.,abs(max(by_wt)-min(by_wt)),0.0])
		UU=np.array([0,0,abs(max(cz_wt)-min(cz_wt))])

		XX0=np.array([min(CP[:,:,:,0].flatten()),min(CP[:,:,:,1].flatten()),min(CP[:,:,:,2].flatten())])

		S = np.array([SS[0],SS[1],SS[2]])
		T = np.array([TT[0],TT[1],TT[2]])
		U = np.array([UU[0],UU[1],UU[2]])

		s=[]
		t=[]
		u=[]

		XX = np.array([x[:]-XX0[0], y[:]-XX0[1], z[:]-XX0[2]])           
		s = (np.dot(np.cross(T, U), XX) / np.dot(np.cross(T, U), S))
		t = (np.dot(np.cross(S, U), XX) / np.dot(np.cross(S, U), T))
		u = (np.dot(np.cross(S, T), XX) / np.dot(np.cross(S, T), U))

		return np.array(s),np.array(t),np.array(u)



    #=======================================
    #FIND POINTS ENCLOSED IN THE LATTICE BOX
    #=======================================
	def findPointsInLattice(self,CP,X,Y,Z):
	
		"""Find points in the FFD lattice.
		"""
		
		
		XE=[]; YE=[]; ZE=[]

		xub=max(CP[:, 0, 0, 0]) 
		xlb=min(CP[:, 0, 0, 0])

		yub=max(CP[0, :, 0, 1]) 
		ylb=min(CP[0, :, 0, 1])

		zub=max(CP[0, 0, :, 2]) 
		zlb=min(CP[0, 0, :, 2])
		
		ID = []
		counter = -1
		for p in (range(len(X))):
			counter += 1
			if X[p] >= xlb and X[p] <= xub and Y[p] >= ylb and Y[p] <= yub and Z[p] >= zlb and Z[p] <= zub:
				XE.append(X[p])
				YE.append(Y[p])
				ZE.append(Z[p])
				ID.append(counter)

		return np.array(XE), np.array(YE), np.array(ZE), np.array(ID)


#===
#EOF
#===