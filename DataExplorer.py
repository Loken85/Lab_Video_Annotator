from Tkinter import *
import tkFileDialog
import json
import yaml
import numpy as np
import scipy.io as sio
import sys
import os
from ttk import *




class DataExplorer:

	def __init__(self, master):
		#top = self.top = Toplevel(parent)
		#top.title("Data Parser")
		
		
		self.dataName = StringVar()
		
		self.dataName.set("Default")
		
		
		# Setup of frame and button layout
		
		titleFrame = Frame(master)
		titleFrame.grid(row=0,column=0,sticky=EW)
		
		titleLbl = Label(titleFrame, text= "Import Annotations to Explore")
		titleLbl.grid(row=0,column=0,sticky=W)
		
		currDataLbl = Label(titleFrame, text="Current Data:")
		currDataE = Label(titleFrame, textvariable = self.dataName)
		
		currDataLbl.grid(row=1,column=0)
		currDataE.grid(row=1,column=1,sticky=W)
		
		
		importFrame = Frame(master)
		importFrame.grid(row=1,column=0, sticky=EW)
		importLbl = Label(importFrame, text="Import Annotation")
		importLbl.grid(row=0,column=0,sticky=EW)
		importBtn = Button(importFrame,text="Import",command = self.impData)
		importBtn.grid(row=1,column=0,sticky=W)
		
		exportFrame = Frame(master)
		exportFrame.grid(row=2,column=0, sticky=EW)
		exportLbl = Label(exportFrame, text="Export Data")
		exportLbl.grid(row=0,column=0,sticky=EW)
		exportBtn = Button(exportFrame, text="Export", command=self.expData)
		exportBtn.grid(row=1,column=0,sticky=W)
		
		
		# Setup of data
		# Parsed JSON dict
		self.parsed = 0
		# Session Info
		self.sessInfo = 0
		# Session data
		self.sessData = 0
		# Data as array
		self.dataArr = 0
		# Three D data
		self.threeDarr = 0
		# Centre of Mass data
		self.cOM = 0
		# Dists from Centre of Mass data
		self.dists = 0
		
		
		
		
		
	def impData(self):
		#import session data from a file
		options = {}
		options['defaultextension'] = '.txt'
		options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
		options['parent'] = root
		options['title'] = 'Import Session Data'
		
		f = tkFileDialog.askopenfilename(**options)
		
		loadF = open(f,'r')
		
		try:
			loadJson = loadF.read()
		except IOError, Argument:
			print "Cannot read file.\n", Argument
		else:
			print "Successfully read file"
			# Set session name
			self.dataName.set(os.path.splitext(os.path.basename(f))[0])
			# parse imported json to dict
			self.parsed = yaml.safe_load(loadJson)
			self.sessInfo = self.parsed[0]
			self.sessData = self.parsed[1]
			# Call process on imported data
			self.processData()
	
		
		
	def expData(self):
		# Export data as a .mat
		# Change here to change what arrays are being exported and written to the file
		
		fname = self.dataName.get() + '.mat'
		print fname
		
		sio.savemat(fname, {'rawData':self.dataArr, 'threeDData':self.threeDarr, 'COM':self.cOM, 'dists':self.dists})
		
		
		
	def processData(self):
		# process parsed data into numpy arrays
		# change in here to change the structure/content of what is displable/exportable
		
		data = {}
		for key in self.sessData:
			rName = key
			rVal = self.sessData[key]
			data[rVal['IMG#']] = rVal
			
		# convert dict of tuples to numpy array
		self.dataArr = np.zeros((len(data),20,2),)
		
		i=0
		for key in sorted(data,key=self.asint):	
			self.dataArr[i,0] = key
			self.dataArr[i,1] = data[key]['C1HN']
			self.dataArr[i,2] = data[key]['C1SG']
			self.dataArr[i,3] = data[key]['C1LP']
			self.dataArr[i,4] = data[key]['C1RP']
			self.dataArr[i,5] = data[key]['C1PV']
			self.dataArr[i,6] = data[key]['C1RL']
			self.dataArr[i,7] = data[key]['C1RR']
			self.dataArr[i,8] = data[key]['C1TB']
			self.dataArr[i,9] = data[key]['C1TM']
			self.dataArr[i,10] = data[key]['C2HN']
			self.dataArr[i,11] = data[key]['C2SG']
			self.dataArr[i,12] = data[key]['C2LP']
			self.dataArr[i,13] = data[key]['C2RP']
			self.dataArr[i,14] = data[key]['C2PV']
			self.dataArr[i,15] = data[key]['C2RL']
			self.dataArr[i,16] = data[key]['C2RR']
			self.dataArr[i,17] = data[key]['C2TB']
			self.dataArr[i,18] = data[key]['C2TM']
			self.dataArr[i,19] = data[key]['IMG#']
			i = i+1
			
		# make into a 3D array using x,y of cam2 and y of cam1
		self.threeDarr = np.zeros((len(data),10,3))

		self.threeDarr[:,0,0] = self.dataArr[:,0,0]

		self.threeDarr[:,1,0] = self.dataArr[:,10,0]
		self.threeDarr[:,1,1] = self.dataArr[:,10,1]
		self.threeDarr[:,1,2] = self.dataArr[:,1,1]

		self.threeDarr[:,2,0] = self.dataArr[:,11,0]
		self.threeDarr[:,2,1] = self.dataArr[:,11,1]
		self.threeDarr[:,2,2] = self.dataArr[:,2,1]

		self.threeDarr[:,3,0] = self.dataArr[:,12,0]
		self.threeDarr[:,3,1] = self.dataArr[:,12,1]
		self.threeDarr[:,3,2] = self.dataArr[:,3,1]

		self.threeDarr[:,4,0] = self.dataArr[:,13,0]
		self.threeDarr[:,4,1] = self.dataArr[:,13,1]
		self.threeDarr[:,4,2] = self.dataArr[:,4,1]

		self.threeDarr[:,5,0] = self.dataArr[:,14,0]
		self.threeDarr[:,5,1] = self.dataArr[:,14,1]
		self.threeDarr[:,5,2] = self.dataArr[:,5,1]

		self.threeDarr[:,6,0] = self.dataArr[:,15,0]
		self.threeDarr[:,6,1] = self.dataArr[:,15,1]
		self.threeDarr[:,6,2] = self.dataArr[:,6,1]

		self.threeDarr[:,7,0] = self.dataArr[:,16,0]
		self.threeDarr[:,7,1] = self.dataArr[:,16,1]
		self.threeDarr[:,7,2] = self.dataArr[:,7,1]

		self.threeDarr[:,8,0] = self.dataArr[:,17,0]
		self.threeDarr[:,8,1] = self.dataArr[:,17,1]
		self.threeDarr[:,8,2] = self.dataArr[:,8,1]

		self.threeDarr[:,9,0] = self.dataArr[:,18,0]
		self.threeDarr[:,9,1] = self.dataArr[:,18,1]
		self.threeDarr[:,9,2] = self.dataArr[:,9,1]
		
		# Create centre of mass column from 3d data

		self.cOM = np.zeros((len(data),1,3))

		i=0
		for row in self.cOM:
			self.cOM[i,0,0] = np.floor((self.threeDarr[i,2,0] + self.threeDarr[i,5,0])/2)
			self.cOM[i,0,1] = np.floor((self.threeDarr[i,2,1] + self.threeDarr[i,5,1])/2)
			self.cOM[i,0,2] = np.floor((self.threeDarr[i,2,2] + self.threeDarr[i,5,2])/2)
			i = i+1
		
		# create dist array. This is distance from centre of mass for each point in each frame	
		self.dists = np.zeros((len(data),10))

		i=0
		for row in self.cOM:
			self.dists[i,0] = self.threeDarr[i,0,0]
			self.dists[i,1] = np.floor(np.linalg.norm(self.cOM[i,0,:]-self.threeDarr[i,1,:]))
			self.dists[i,2] = np.floor(np.linalg.norm(self.cOM[i,0,:]-self.threeDarr[i,2,:]))
			self.dists[i,3] = np.floor(np.linalg.norm(self.cOM[i,0,:]-self.threeDarr[i,3,:]))
			self.dists[i,4] = np.floor(np.linalg.norm(self.cOM[i,0,:]-self.threeDarr[i,4,:]))
			self.dists[i,5] = np.floor(np.linalg.norm(self.cOM[i,0,:]-self.threeDarr[i,5,:]))
			self.dists[i,6] = np.floor(np.linalg.norm(self.cOM[i,0,:]-self.threeDarr[i,6,:]))
			self.dists[i,7] = np.floor(np.linalg.norm(self.cOM[i,0,:]-self.threeDarr[i,7,:]))
			self.dists[i,8] = np.floor(np.linalg.norm(self.cOM[i,0,:]-self.threeDarr[i,8,:]))
			self.dists[i,9] = np.floor(np.linalg.norm(self.cOM[i,0,:]-self.threeDarr[i,9,:]))
			i=i+1
			
		
		
	def asint(self,s):
		# Helper function for converting number strings to ints
		try: return int(s), ''
		except ValueError: return sys.maxint, s
		
# Self-standing for testing purposes
root = Tk()

app = DataExplorer(root)
root.title("Data Explorer")
root.mainloop()
		
		
		

