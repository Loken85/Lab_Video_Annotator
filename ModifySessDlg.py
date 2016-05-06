from Tkinter import *

# TODO: replace filepath entries with tkfiledialog.askdirectory to return directory? or does first img work better? 
# change to transient and grab_set focus
# Window for modifying session info. Contains entry fields for all session info, submits to modify session info method and changes session info object
class ModifySessDlg(object):

	def __init__(self,parent,data):
		top = self.top = Toplevel(parent)
		top.title("Session Information")
		
		self.sessInfo = 0
		
		# create string vars
		self.sNameV = StringVar()		
		self.sDateV = StringVar()		
		self.sAnimalV = StringVar()		
		self.sExpV = StringVar()		
		self.sCam1FPV = StringVar()		
		self.sCam2FPV = StringVar()
		self.sFPSV = StringVar()
		self.sTotalFV = StringVar()		
		self.sCurrFV = StringVar()		
		
		
		# size vars
		labelW = 80		
		entryW = 200
		entryH = 150
		
		# Setup of frame and label/entry layout
		
		titleFrame = Frame(top)
		titleFrame.grid(row=0,column=0,sticky=EW)
		
		titleLbl = Label(titleFrame, text= "Enter New Session Information")
		titleLbl.grid(row=0,column=0,sticky=W)
		
		entryPane = PanedWindow(top,orient=HORIZONTAL)
		entryPane.grid(row=1,column=0,sticky=NSEW)
		
		#labels
		labelFrame = Frame(entryPane,width=labelW,height=entryH)
		entryPane.add(labelFrame)		
		
		sNameL = Label(labelFrame, text="Session Name:")
		sDateL = Label(labelFrame, text="Session Date:")
		sAnimalL = Label(labelFrame, text="Animal:")
		sExpL = Label(labelFrame, text="Experiment:")
		sCam1FPL = Label(labelFrame, text="Camera 1 FilePath:")
		sCam2FPL = Label(labelFrame, text="Camera 2 FilePath:")
		sFPSL = Label(labelFrame, text="Framerate:")
		sTotalFL = Label(labelFrame, text="Total Frame Count:")
		sCurrFL = Label(labelFrame, text="Current Frame:")
		
		#label layout
		sNameL.grid(row=0,column=0,sticky=E)
		sDateL.grid(row=1,column=0,sticky=E)
		sAnimalL.grid(row=2,column=0,sticky=E)
		sExpL.grid(row=3,column=0,sticky=E)
		sCam1FPL.grid(row=4,column=0,sticky=E)
		sCam2FPL.grid(row=5,column=0,sticky=E)
		sFPSL.grid(row=6,column=0,sticky=E)
		sTotalFL.grid(row=7,column=0,sticky=E)
		sCurrFL.grid(row=8,column=0,sticky=E)
		
		# entries
		entryFrame = Frame(entryPane,width=entryW,height=entryH)
		entryPane.add(entryFrame)		
		
		sNameE = Entry(entryFrame, textvariable=self.sNameV)
		sDateE = Entry(entryFrame,textvariable=self.sDateV)
		sAnimalE = Entry(entryFrame,textvariable=self.sAnimalV)
		sExpE = Entry(entryFrame,textvariable=self.sExpV)
		sCam1FPE = Entry(entryFrame,textvariable=self.sCam1FPV)
		sCam2FPE = Entry(entryFrame,textvariable=self.sCam2FPV)
		sFPSE = Entry(entryFrame,textvariable=self.sFPSV)
		sTotalFE = Entry(entryFrame,textvariable=self.sTotalFV)
		sCurrFE = Entry(entryFrame,textvariable=self.sCurrFV)
		# set text variable contents from parse of session data
		self.sNameV.set(data['sName'])
		self.sDateV.set(data['sDate'])
		self.sAnimalV.set(data['sAnimal'])
		self.sExpV.set(data['sExp'])
		self.sCam1FPV.set(data['cam1FP'])
		self.sCam2FPV.set(data['cam2FP'])
		self.sFPSV.set(data['fps'])
		self.sTotalFV.set(data['sTotalF'])
		self.sCurrFV.set(data['sCurrF'])
		
		# entry layout
		sNameE.grid(row=0,column=0,sticky=W)
		sDateE.grid(row=1,column=0,sticky=W)
		sAnimalE.grid(row=2,column=0,sticky=W)
		sExpE.grid(row=3,column=0,sticky=W)
		sCam1FPE.grid(row=4,column=0,sticky=W)
		sCam2FPE.grid(row=5,column=0,sticky=W)
		sFPSE.grid(row=6,column=0,sticky=W)
		sTotalFE.grid(row=7,column=0,sticky=W)
		sCurrFE.grid(row=8,column=0,sticky=W)
		
		# submit
		submitFrame = Frame(top)
		submitFrame.grid(row=2,column=0,sticky=EW)
		
		subB = Button(submitFrame,text="Submit",command=self.submit)
		cancB = Button(submitFrame,text="Cancel",command=self.cancel)
		subB.grid(row=0,column=0)
		cancB.grid(row=0,column=1)
		
		
		
	def submit(self):
		# copy entry fields into session data structure
		# TODO: add verification for all fields <- LACKING THIS IS REAL BAD!
		
		sessInfo = {}
		sessInfo['sName'] = self.sNameV.get()
		sessInfo['sDate'] = self.sDateV.get()
		sessInfo['sAnimal'] = self.sAnimalV.get()
		sessInfo['sExp'] = self.sExpV.get()
		sessInfo['cam1FP'] = self.sCam1FPV.get()
		sessInfo['cam2FP'] = self.sCam2FPV.get()
		sessInfo['fps'] = self.sFPSV.get()
		sessInfo['sTotalF'] = self.sTotalFV.get()
		sessInfo['sCurrF'] = self.sCurrFV.get()
		
		self.sessInfo = sessInfo
		
		self.top.destroy()
		
	def cancel(self):
		self.top.destroy()
		