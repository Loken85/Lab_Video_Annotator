# Tkinter GUI for Video Image Annotation

from Tkinter import *
import tkSimpleDialog
from HelpDialog import HelpDialog
from AboutDialog import AboutDialog
from ModifySessDlg import ModifySessDlg
from SettingsDlg import SettingsDlg
import tkFileDialog
import json
import yaml
import ConfigParser
from PIL import Image, ImageTk
from ttk import *
#import tktable

# TODO: move helper and graphics functions in to their own sections or util files


class App:

	def __init__(self, master):
		#frame = Frame(master)
		#frame.pack()
		
		#self.button = Button(frame, text="QUIT",fg="red",command=frame.quit)
		#self.button.pack(side=LEFT)
		
		#self.hi_there = Button(frame,text="Hello",command=self.say_hi)
		#self.hi_there.pack(side=LEFT)
		
				
		# Settings Vars		
		self.osVar = IntVar()
		self.ssVar = StringVar()
		# TODO: have the noC var determine img load or blank img for second camera
		self.noCVar = IntVar()
		self.inFPSVar = IntVar()
		# TODO: have annVar change from 2x2d coords to 3d coords
		self.annVar = IntVar()
		self.settings={}
		self.read_settings()
		
		# Default values
		
		master.geometry(self.ssVar.get())
		
		w = self.ss_to_int(self.ssVar.get())
		
		# NOTE: May have to adjust the ratio for smaller screen sizes
		imgH = w/3
		imgW = w/2
		#totH = 990
		totW = w
		
		
		
		
		# block phased out, setting are now defined by a read of config
		# default settings, replaced when loading existing settings, modified by settigns button
		# TODO: use configparser, set defaults based on autodetect for ss and OS
		#self.settings = {'os': 0, 'ss': "1920x1080", 'noC': 2, 'inFPS': 15, 'ann':0}
		
		
		
		# Default Session, replaced when loading existing session, modified by modify session button
		self.sessionInfo = {'sName': "Default",'sDate': "Default",'sAnimal': "Default",'sExp': "Default",'sTotalF': "000000",'sCurrF': "0",'cam1FP': "filepath",'cam2FP': "filepath",'fps': "0"}
		# string vars to hold session info
		self.sNameV = StringVar()
		self.sDateV = StringVar()
		self.sAnimalV = StringVar()
		self.sExpV = StringVar()
		self.sNameV.set(self.sessionInfo['sName'])
		self.sDateV.set(self.sessionInfo['sDate'])
		self.sAnimalV.set(self.sessionInfo['sAnimal'])
		self.sExpV.set(self.sessionInfo['sExp'])
		self.sFPSV = StringVar()
		self.sTotalFV = StringVar()
		self.sCurrFV = StringVar()
		self.sFPSV.set(self.sessionInfo['fps'])
		self.sTotalFV.set(self.sessionInfo['sTotalF'])
		self.sCurrFV.set(self.sessionInfo['sCurrF'])
		self.sCam1FPV = StringVar()
		self.sCam2FPV = StringVar()
		self.sCam1FPV.set(self.sessionInfo['cam1FP'])
		self.sCam2FPV.set(self.sessionInfo['cam2FP'])
		
		self.currImg1Path = StringVar()
		self.currImg2Path = StringVar()
		
		self.prevF = '0'
		
		
		
		self.treeData = {}
		# Default data for testing purposes
		defData = {'Default': {'IMG#': '0', 'C1HN': [205,205], 'C1LP': [255,185], 'C1RP': [155,185], 'C1SG': [205,165], 'C1PV': [205,125], 'C1RL': [255,105], 'C1RR': [155,105], 'C1TB': [215,85], 'C1TM': [275,75], 'C2HN': [205,205], 'C2LP': [255,185], 'C2RP': [155,185], 'C2SG': [205,165], 'C2PV': [205,125], 'C2RL': [255,105] , 'C2RR': [155,105], 'C2TB': [215,85], 'C2TM': [275,75]}}
		self.treeData = defData
		
		# Default image to hold canvas for images on load
		# Change path for different startup images
		#self.imgPath = r"C:\\Python27\CNstuff\sampleA.jpg"
		#self.imgPath2 = r"C:\\Python27\CNstuff\sampleB.jpg"
		self.imgPath = "sampleA.jpg"
		self.imgPath2 = "sampleB.jpg"
		
		if self.sCurrFV.get() == "0":
			self.currImg1Path.set(self.imgPath)
			self.currImg2Path.set(self.imgPath2)		
		
		
		# Padding for top
		topPad = Frame(master, height=10)
		topPad.grid(row=0,column=0,sticky=EW)
		
		# Top Pane, left side is session, right is menu buttons
		mainTP = Frame(master)
		mainTP.grid(row=1,column=0, sticky=EW)
		
		# Content for session info
		
		sessinfoFrame = Frame(mainTP,width=imgW,height=60,relief=GROOVE)		
		sessinfoFrame.grid(row=0,column=0,padx=5)
		sessinfoFrame.grid_propagate('false')
		
		
		#mainTP.paneconfigure(sessinfoFrame,**mainTPoptions)
		
		# First Row Labels
		ssnidLB = Label(sessinfoFrame, text="SsnID:")
		dateLB = Label(sessinfoFrame, text="Date:")
		anmLB = Label(sessinfoFrame, text="Animal:")
		expLB = Label(sessinfoFrame, text="Exp:")
		# First row display
				
		ssnidE = Label(sessinfoFrame, textvariable=self.sNameV)
		dateE = Label(sessinfoFrame, textvariable=self.sDateV)
		anmE = Label(sessinfoFrame, textvariable=self.sAnimalV)
		expE = Label(sessinfoFrame, textvariable=self.sExpV)
		
		# Second row labels
		fpsLB = Label(sessinfoFrame, text="Framerate:")
		totfrLB = Label(sessinfoFrame, text="Total Frames:")
		currfrLB = Label(sessinfoFrame, text="Current Frame:")
		# Second row display		
		fpsD = Label(sessinfoFrame, textvariable=self.sFPSV)
		totfrD = Label(sessinfoFrame, textvariable=self.sTotalFV)
		currfrD = Label(sessinfoFrame, textvariable=self.sCurrFV)		
		
		# Modify button
		modB = Button(sessinfoFrame, text="Modify Session Info", command=self.mod_sess)		
		
		# Session info layout
		ssnidLB.grid(row=0,column=0)
		ssnidE.grid(row=0,column=1)
		dateLB.grid(row=0,column=2)
		dateE.grid(row=0,column=3)
		anmLB.grid(row=0,column=4)
		anmE.grid(row=0,column=5)
		expLB.grid(row=0,column=6)
		expE.grid(row=0,column=7)
		
		fpsLB.grid(row=1,column=0)
		fpsD.grid(row=1,column=1)
		totfrLB.grid(row=1,column=2)
		totfrD.grid(row=1,column=3)
		currfrLB.grid(row=1,column=4)
		currfrD.grid(row=1,column=5)
		
		modB.grid(row=1,column=6)
		
		# Create menu bar at top
		menuFrame = Frame(mainTP,width=imgW,height=60,relief=GROOVE)
		menuFrame.grid(row=0,column=1,padx=5)
		menuFrame.grid_propagate('false')
		
		
		
		# Menu Buttons
		
		newB = Button(menuFrame,text="New",command=self.mod_sess)
		openB = Button(menuFrame,text="Open",command=self.load_data)
		saveB = Button(menuFrame,text="Save",command=self.save_data)
		settingsB = Button(menuFrame,text="Settings",command=self.mod_settings)		
		aboutB = Button(menuFrame,text="About",command=self.about_dlg)
		helpB = Button(menuFrame,text="Help",command=self.help_dlg)
		
		newB.grid(row=0,column=0,padx=20,sticky=W)
		openB.grid(row=0,column=1,padx=20)
		saveB.grid(row=0,column=2,padx=20)
		settingsB.grid(row=0,column=3,padx=20,sticky=W)
		helpB.grid(row=0,column=4,padx=20)
		aboutB.grid(row=0,column=5)
		
		midPad = Frame(master, height=10)
		midPad.grid(row=2,column=0, sticky=EW)
		
		# Create left/right pane
		mainLR = PanedWindow(master, orient=HORIZONTAL)
		mainLR.grid(row=3,column=0)
		
		# old version
		#leftCFrame = Frame(mainLR,width=720,height=totH)
		#mainLR.add(leftCFrame)
		
		
		# 
		topIMG = LabelFrame(mainLR,text="Camera 1",width=imgW,height=imgH)
		mainLR.add(topIMG)
		
		# LEFT / Top Image
		self.topCV = Canvas(topIMG,width=imgW,height=imgH,cursor='cross')
		self.topImg = self.get_img(self.imgPath)
		self.topImgRef = self.topCV.create_image(int(imgW/2),int(imgH/2),image=self.topImg,anchor=CENTER,tags='topImage')		
		self.topCV.pack()
		
		# 
		bottomIMG = LabelFrame(mainLR,text="Camera 2",width=imgW,height=imgH)
		mainLR.add(bottomIMG)
		
		# RIGHT / Bottom Image
		self.bottCV = Canvas(bottomIMG,width=imgW,height=imgH,cursor='cross')
		self.bottImg = self.get_img(self.imgPath2)
		# Offset in image location corrects for bias towards bottom of frame in camera 2 images
		self.bottImgRef = self.bottCV.create_image(int(imgW/2),int(imgH/2 - 50),image=self.bottImg,anchor=CENTER,tags='bottImage')
		# So...tkinter garbage collects your image reference even if it's still in use unless you make an extra copy of it. Go figure.		
		self.bottCV.pack()

		botPad = Frame(master,height=10)
		botPad.grid(row=4,column=0,sticky=EW)
		
		mainBT = Frame(master,width=totW)
		mainBT.grid(row=5,column=0,sticky=EW)
		
		
		controlHolder = Frame(mainBT, width=totW, height=40)
		controlHolder.grid(row=0,column=0)
		
		midControls = Frame(controlHolder,width=imgW,height=30,relief=GROOVE)
		midControls.grid(row=0,column=0, sticky=EW)
		
		# Mid Control Buttons
		forB = Button(midControls,text="Fwd >",command=self.fwd_frame)
		backB = Button(midControls,text="< Back",command=self.bck_frame)
		firstB = Button(midControls,text="<< First",command=self.fst_frame)
		lastB = Button(midControls,text="Last >>",command=self.lst_frame)
		drawB = Button(midControls,text="Draw",command=self.draw_btn)
		showB = Button(midControls,text="Show / Hide")
		
		forB.grid(row=0,column=3)
		backB.grid(row=0,column=1)
		firstB.grid(row=0,column=0)
		lastB.grid(row=0,column=4)
		drawB.grid(row=0,column=2)
		showB.grid(row=0,column=5)	
		
		
		dataPad = Frame(mainBT, height=10)
		dataPad.grid(row=1,column=0, sticky=EW)
		
		# Frame for data table at bottom
		dataHolder = Frame(mainBT, width=totW)
		dataHolder.grid(row=2,column=0, sticky=EW)		
		dataFrame = Frame(dataHolder,width=(totW-20))
		dataFrame.grid(row=0,column=0, padx=265, sticky=EW)
		
		# Info frame at bottom. Currently empty
		suppInfoFrame = Frame(mainBT, width=totW)
		suppInfoFrame.grid(row=3,column=0)
		suppInfoCV = Canvas(suppInfoFrame,width=totW,height=20)
		suppInfoCV.pack()
		
		# Data table
		#dataTable = tkTable.Table(dataFrame)
		dataTable = self.dataTable = Treeview(dataFrame,height=5,padding=3)
		
		# Table constants
		
		colWidth = 55
		minWth = 55
		# Table setup
		dataTable.configure(columns=('IMG#', 'C1HN', 'C1LP', 'C1RP', 'C1SG', 'C1PV', 'C1RL' , 'C1RR', 'C1TB' , 'C1TM',
									'C2HN', 'C2LP', 'C2RP', 'C2SG', 'C2PV', 'C2RL' , 'C2RR', 'C2TB' , 'C2TM'))
		dataTable.column('#0',width=(colWidth*4),minwidth=(minWth*4))
		dataTable.heading('#0',text="File")
		dataTable.column('IMG#',width=colWidth,minwidth=minWth)
		dataTable.heading('IMG#',text='IMG#', command= lambda: self.sort_column('IMG#',False))
		dataTable.column('C1HN',width=colWidth,minwidth=minWth)
		dataTable.heading('C1HN',text='C1HN')
		dataTable.column('C1LP',width=colWidth,minwidth=minWth)
		dataTable.heading('C1LP',text='C1LP')
		dataTable.column('C1RP',width=colWidth,minwidth=minWth)
		dataTable.heading('C1RP',text='C1RP')
		dataTable.column('C1SG',width=colWidth,minwidth=minWth)
		dataTable.heading('C1SG',text='C1SG')		
		dataTable.column('C1PV',width=colWidth,minwidth=minWth)
		dataTable.heading('C1PV',text='C1PV')
		dataTable.column('C1RL',width=colWidth,minwidth=minWth)
		dataTable.heading('C1RL',text='C1RL')
		dataTable.column('C1RR',width=colWidth,minwidth=minWth)
		dataTable.heading('C1RR',text='C1RR')
		dataTable.column('C1TB',width=colWidth,minwidth=minWth)
		dataTable.heading('C1TB',text='C1TB')
		dataTable.column('C1TM',width=colWidth,minwidth=minWth)
		dataTable.heading('C1TM',text='C1TM')
		dataTable.column('C2HN',width=colWidth,minwidth=minWth)
		dataTable.heading('C2HN',text='C2HN')
		dataTable.column('C2LP',width=colWidth,minwidth=minWth)
		dataTable.heading('C2LP',text='C2LP')
		dataTable.column('C2RP',width=colWidth,minwidth=minWth)
		dataTable.heading('C2RP',text='C2RP')
		dataTable.column('C2SG',width=colWidth,minwidth=minWth)
		dataTable.heading('C2SG',text='C2SG')		
		dataTable.column('C2PV',width=colWidth,minwidth=minWth)
		dataTable.heading('C2PV',text='C2PV')
		dataTable.column('C2RL',width=colWidth,minwidth=minWth)
		dataTable.heading('C2RL',text='C2RL')
		dataTable.column('C2RR',width=colWidth,minwidth=minWth)
		dataTable.heading('C2RR',text='C2RR')
		dataTable.column('C2TB',width=colWidth,minwidth=minWth)
		dataTable.heading('C2TB',text='C2TB')
		dataTable.column('C2TM',width=colWidth,minwidth=minWth)
		dataTable.heading('C2TM',text='C2TM')
		
		
		# Data Table layout
		dtSBH = Scrollbar(dataFrame,orient=HORIZONTAL,command=dataTable.xview)
		dtSBV = Scrollbar(dataFrame,orient=VERTICAL,command=dataTable.yview)
		dataTable.configure(xscrollcommand=dtSBH.set, yscrollcommand=dtSBV.set)
		dataTable.grid(row=0,column=0)
		dtSBH.grid(row=1,column=0,sticky=EW)
		dtSBV.grid(row=0,column=1,sticky=NS)
		
		# Test data
		dataTable.insert('','end', 'test', text='Test', values=('1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'))
		self.add_row(dataTable,'test1',('2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'))
		

		# Attributes to hold points and lines for annotation skeleton
		self.diameter = 5
		# Camera 1
		self.C1HNP = defData['Default']['C1HN']
		self.C1LPP = defData['Default']['C1LP']
		self.C1RPP = defData['Default']['C1RP']
		self.C1SGP = defData['Default']['C1SG']
		self.C1PVP = defData['Default']['C1PV']
		self.C1RLP = defData['Default']['C1RL']
		self.C1RRP = defData['Default']['C1RR']
		self.C1TBP = defData['Default']['C1TB']
		self.C1TMP = defData['Default']['C1TM']
		
		# Camera 2
		self.C2HNP = defData['Default']['C2HN']
		self.C2LPP = defData['Default']['C2LP']
		self.C2RPP = defData['Default']['C2RP']
		self.C2SGP = defData['Default']['C2SG']
		self.C2PVP = defData['Default']['C2PV']
		self.C2RLP = defData['Default']['C2RL']
		self.C2RRP = defData['Default']['C2RR']
		self.C2TBP = defData['Default']['C2TB']
		self.C2TMP = defData['Default']['C2TM']
		
		# Attributes for draw, show/hide management
		self.drawn = 0
		self.show = 1
		
		
		# Key bindings/shortcuts for the main window
		# TODO: add to settings, ability to set hotkeys
		master.bind('d', self.fwd_frame)
		master.bind('<Right>', self.fwd_frame)
		master.bind('s', self.draw_btn)
		# master.bind('<space>', self.draw_btn)
		master.bind('a', self.bck_frame)
		master.bind('<Left>', self.bck_frame)
		master.bind('<Home>', self.fst_frame)
		master.bind('<End>', self.lst_frame )
		
		
			
		
		
		

		
		
		
		
		
		
	def say_hi(self):
		print "Hello there!"
		
	def get_img(self,path):
		gImg = Image.open(path)
		gPho = ImageTk.PhotoImage(gImg)		
		return gPho
		
	def add_row(self,tree,name,data):
		#add row to table, if it alredy exists, modify existing row
		if not tree.exists(name):
			tree.insert('','end',name,text=name,values=data)
		else:
			for index, val in enumerate(data):
				# Hopefully indices as opposed to column identifiers work here. May require an offset of 1 (set in enumerate declaration)
				tree.set(name,index,val)
		
	
	def assemble_sess(self,sessInfo,dataTree):
		#put together session object, make serializable for JSON
		saveData = [sessInfo,dataTree]		
		return json.dumps(saveData)
		
	def parse_sess(self,session):
		#disassemble session object from JSON format, return info and data
		parsed = yaml.safe_load(session)
		nSessInfo = parsed[0]
		nDataTree = parsed[1]
		return nSessInfo,nDataTree
		
	def mod_sess(self):
		#creates a new modify session window (modal), takes focus, waits on submit, calls label update with returned info		
		modSessDlg = ModifySessDlg(root,self.sessionInfo)
		root.wait_window(modSessDlg.top)
		# copy over new session info 
		if modSessDlg.sessInfo:
			self.sessionInfo = modSessDlg.sessInfo
			self.update_sess_lbls(self.sessionInfo)			
			self.update_frame()
	
	def update_sess_lbls(self,cSessInfo):
		# updates session info text variables to update display
		self.sNameV.set(cSessInfo['sName'])
		self.sDateV.set(cSessInfo['sDate'])
		self.sAnimalV.set(cSessInfo['sAnimal'])
		self.sExpV.set(cSessInfo['sExp'])
		self.sCam1FPV.set(cSessInfo['cam1FP'])
		self.sCam2FPV.set(cSessInfo['cam2FP'])
		self.sFPSV.set(cSessInfo['fps'])
		self.sTotalFV.set(cSessInfo['sTotalF'])
		self.sCurrFV.set(cSessInfo['sCurrF'])
		
	def save_data(self):
		# Writes session and data information to a file.
		# Calls assemble_sess to combine session and data into single json string, calls filedialogue to get file for writing, tries to write file, closes file
	
		sessJson = self.assemble_sess(self.sessionInfo, self.treeData)
	
		options = {}
		options['defaultextension'] = '.txt'
		options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
		#options['initialdir'] = 'C:\\'
		options['initialfile'] = self.sessionInfo['sName']
		options['parent'] = root
		options['title'] = 'Save Session Data'
	
		saveF = tkFileDialog.asksaveasfile(mode='w', **options)
	
		try:
			saveF.write(sessJson)
		except IOError:
			print "IO error: Cannot write to file"
		else:
			print "Successful write"
	
		saveF.close()
		
	def add_treeData(self,nItemName,nItem):
		# adds to the treeData variable
		# then adds to treeview
		self.treeData[nItemName] = nItem			
		self.add_row(self.dataTable,nItemName,self.parse_data_for_tree(nItem))
	
	def replace_treeView(self):
		# replaces treeView with data from treeData variable, called when loading file
		# get self.treeData, for each entry, take entry key as top-level item in treeview, take entry content as dict with keys for each column in the view, loop call insert
		self.clear_tree()
		
		for key in self.treeData:
			rName = key
			rVal = self.treeData[key]			
			self.add_row(self.dataTable,rName,self.parse_data_for_tree(rVal))
			
	def sort_column(self, col, reverse):
		# sort tree based on column
		entries = [(self.dataTable.set(k,col),k) for k in self.dataTable.get_children('')]
		entries.sort(key= lambda t: int(t[0]), reverse=reverse)
		for index, (val,k) in enumerate(entries):
			self.dataTable.move(k,'',index)
		self.dataTable.heading(col, command= lambda: self.sort_column(col, not reverse))
		
		
	def clear_tree(self):
		# clears existing treeview values. Called when loading file to clear old data
		entries = self.dataTable.get_children()
		for entry in entries:
			self.dataTable.delete(entry)
	
	def load_data(self):
		# load session information from a file
		# calls open file dialog, tries to read file, calls parse_sess to dissassemble json, replaces session object and treeData, calls replace_treeView and update_sess_lbls
		
		options = {}
		options['defaultextension'] = '.txt'
		options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
		options['parent'] = root
		options['title'] = 'Load Session Data'
		
		loadF = tkFileDialog.askopenfile(mode='r', **options)
		
		try:
			loadJson = loadF.read()
		except IOError, Argument:
			print "Cannot read file.\n", Argument
		else:
			print "Successfully read file"
			nSessInfo, nTreeData = self.parse_sess(loadJson)
			self.sessionInfo = nSessInfo			
			self.update_sess_lbls(nSessInfo)
			self.treeData = nTreeData			
			self.replace_treeView()
			self.update_frame()
		
		loadF.close()
		
	def about_dlg(self):
		# TODO: add version info/changelist to about dialog
		aboutdlg = AboutDialog(root, title="About")
		
	
	def help_dlg(self):
		# TODO: add searchable FAQ to help dialog
		helpdlg = HelpDialog(root, title="Help")
		
		
	def mod_settings(self):
		# allow user to change settings values, update setting attributes
		settingsdlg = SettingsDlg(root,self.settings)
		
		if settingsdlg.result:
			self.settings = settingsdlg.result
			self.write_settings()
		
			
	def get_curr_img_paths(self):
		# calculates path for current image
		if self.sCurrFV.get() == "0":
			self.currImg1Path.set(self.imgPath)
			self.currImg2Path.set(self.imgPath2)
			return
		
		# slash direction needs to change based on OS kernel
		if self.osVar.get() == 0:
			# Warning: \0 in a string is treated as an escape char. Hopefully the \\ solves this, otherwise the string needs r prepended to make it raw
			nImgP1 = self.sCam1FPV.get() + '\%05d.jpg' % ((int(self.sCurrFV.get())-1)*((self.inFPSVar.get())/int(self.sFPSV.get()))+1)
			nImgP2 = self.sCam2FPV.get() + '\%05d.jpg' % ((int(self.sCurrFV.get())-1)*((self.inFPSVar.get())/int(self.sFPSV.get()))+1)
		else:
			nImgP1 = self.sCam1FPV.get() + '/%05d.jpg' % ((int(self.sCurrFV.get())-1)*((self.inFPSVar.get())/int(self.sFPSV.get()))+1)
			nImgP2 = self.sCam2FPV.get() + '/%05d.jpg' % ((int(self.sCurrFV.get())-1)*((self.inFPSVar.get())/int(self.sFPSV.get()))+1)
			
		self.currImg1Path.set(nImgP1)
		self.currImg2Path.set(nImgP2)
		
		
	def fwd_frame(self,event=None):
		# advance one frame. Updates current frame number, gets new img paths, loads new imgs, updates canvases with new imgs
		self.prevF = self.sCurrFV.get()
		# check for reaching total frame number
		if int(self.sCurrFV.get()) < int(self.sTotalFV.get()):
			self.sCurrFV.set(str(int(self.sCurrFV.get())+1))		
		self.update_frame()
		
		
			
	def bck_frame(self,event=None):
		# go back one frame. Updates current frame number, gets new img paths, loads new imgs, updates canvases with new imgs
		self.prevF = self.sCurrFV.get()
		if self.sCurrFV.get() == "0":
			return
			
		self.sCurrFV.set(str(int(self.sCurrFV.get())-1))
		self.update_frame()
		
	def fst_frame(self,event=None):
		# go to first frame
		self.prevF = self.sCurrFV.get()
		self.sCurrFV.set('1')
		self.update_frame()
		
	def lst_frame(self,event=None):
		# go to last frame
		self.prevF = self.sCurrFV.get()
		self.sCurrFV.set(self.sTotalFV.get())
		self.update_frame()
		
	def update_frame(self):
		# Handles fetching new img paths, loading new imgs, and updating canvases
		# check and draw for skeleton if one exists for current frame, update tree data
		# oldPath = self.currImg1Path.get()
		if self.drawn and not self.currImg1Path.get() == self.imgPath:
			# if annotation does not already exist, write in annotation for old frame
			self.rec_annotation()
		
		self.get_curr_img_paths()
		
		try:
			self.topImg = self.get_img(self.currImg1Path.get())
			self.bottImg = self.get_img(self.currImg2Path.get())
		except:
			print 'Invalid Image'
		else:
			self.topCV.itemconfig(self.topImgRef, image = self.topImg)
			self.bottCV.itemconfig(self.bottImgRef, image = self.bottImg)
			
			self.remove_skeleton()
			if self.check_annotation(self.currImg1Path.get()):
				self.update_points(self.treeData[self.currImg1Path.get()])
				self.draw_skeleton()
				self.drawn = 1
			else:
				self.drawn = 0
			
	def draw_skeleton(self):
		# Draws points and lines for annotation skeleton. Sets mouse bindings so points can be dragged by mouse (calls move_point)
		# Points will be drawn at wherever the last point locations were set
		# Colour reference: HN: white, LP: blue, RP: red, RL: dark blue, RR: dark red, SG: yellow, PV: orange, TB: violet, TM: dark violet
		self.topCV.bind("<B1-Motion>", self.move_point1)
		self.topCV.create_oval((self.C1HNP[0]-self.diameter),(self.C1HNP[1]-self.diameter),(self.C1HNP[0]+self.diameter),(self.C1HNP[1]+self.diameter),fill='white',activefill='green',tags='C1HNP')
		self.topCV.create_oval((self.C1LPP[0]-self.diameter),(self.C1LPP[1]-self.diameter),(self.C1LPP[0]+self.diameter),(self.C1LPP[1]+self.diameter),fill='blue',activefill='green',tags='C1LPP')
		self.topCV.create_oval((self.C1RPP[0]-self.diameter),(self.C1RPP[1]-self.diameter),(self.C1RPP[0]+self.diameter),(self.C1RPP[1]+self.diameter),fill='red',activefill='green',tags='C1RPP')
		self.topCV.create_oval((self.C1SGP[0]-self.diameter),(self.C1SGP[1]-self.diameter),(self.C1SGP[0]+self.diameter),(self.C1SGP[1]+self.diameter),fill='yellow',activefill='green',tags='C1SGP')
		self.topCV.create_oval((self.C1PVP[0]-self.diameter),(self.C1PVP[1]-self.diameter),(self.C1PVP[0]+self.diameter),(self.C1PVP[1]+self.diameter),fill='orange',activefill='green',tags='C1PVP')
		self.topCV.create_oval((self.C1RLP[0]-self.diameter),(self.C1RLP[1]-self.diameter),(self.C1RLP[0]+self.diameter),(self.C1RLP[1]+self.diameter),fill='dark blue',activefill='green',tags='C1RLP')
		self.topCV.create_oval((self.C1RRP[0]-self.diameter),(self.C1RRP[1]-self.diameter),(self.C1RRP[0]+self.diameter),(self.C1RRP[1]+self.diameter),fill='dark red',activefill='green',tags='C1RRP')
		self.topCV.create_oval((self.C1TBP[0]-self.diameter),(self.C1TBP[1]-self.diameter),(self.C1TBP[0]+self.diameter),(self.C1TBP[1]+self.diameter),fill='violet',activefill='green',tags='C1TBP')
		self.topCV.create_oval((self.C1TMP[0]-self.diameter),(self.C1TMP[1]-self.diameter),(self.C1TMP[0]+self.diameter),(self.C1TMP[1]+self.diameter),fill='dark violet',activefill='green',tags='C1TMP')
		
		self.bottCV.bind("<B1-Motion>", self.move_point2)
		self.bottCV.create_oval((self.C2HNP[0]-self.diameter),(self.C2HNP[1]-self.diameter),(self.C2HNP[0]+self.diameter),(self.C2HNP[1]+self.diameter),fill='white',activefill='green',tags='C2HNP')
		self.bottCV.create_oval((self.C2LPP[0]-self.diameter),(self.C2LPP[1]-self.diameter),(self.C2LPP[0]+self.diameter),(self.C2LPP[1]+self.diameter),fill='blue',activefill='green',tags='C2LPP')
		self.bottCV.create_oval((self.C2RPP[0]-self.diameter),(self.C2RPP[1]-self.diameter),(self.C2RPP[0]+self.diameter),(self.C2RPP[1]+self.diameter),fill='red',activefill='green',tags='C2RPP')
		self.bottCV.create_oval((self.C2SGP[0]-self.diameter),(self.C2SGP[1]-self.diameter),(self.C2SGP[0]+self.diameter),(self.C2SGP[1]+self.diameter),fill='yellow',activefill='green',tags='C2SGP')
		self.bottCV.create_oval((self.C2PVP[0]-self.diameter),(self.C2PVP[1]-self.diameter),(self.C2PVP[0]+self.diameter),(self.C2PVP[1]+self.diameter),fill='orange',activefill='green',tags='C2PVP')
		self.bottCV.create_oval((self.C2RLP[0]-self.diameter),(self.C2RLP[1]-self.diameter),(self.C2RLP[0]+self.diameter),(self.C2RLP[1]+self.diameter),fill='dark blue',activefill='green',tags='C2RLP')
		self.bottCV.create_oval((self.C2RRP[0]-self.diameter),(self.C2RRP[1]-self.diameter),(self.C2RRP[0]+self.diameter),(self.C2RRP[1]+self.diameter),fill='dark red',activefill='green',tags='C2RRP')
		self.bottCV.create_oval((self.C2TBP[0]-self.diameter),(self.C2TBP[1]-self.diameter),(self.C2TBP[0]+self.diameter),(self.C2TBP[1]+self.diameter),fill='violet',activefill='green',tags='C2TBP')
		self.bottCV.create_oval((self.C2TMP[0]-self.diameter),(self.C2TMP[1]-self.diameter),(self.C2TMP[0]+self.diameter),(self.C2TMP[1]+self.diameter),fill='dark violet',activefill='green',tags='C2TMP')
		
	def remove_skeleton(self):
		# deletes skeleton, called when changing frames
		self.topCV.delete('C1HNP')
		self.topCV.delete('C1LPP')
		self.topCV.delete('C1RPP')
		self.topCV.delete('C1SGP')
		self.topCV.delete('C1PVP')
		self.topCV.delete('C1RLP')
		self.topCV.delete('C1RRP')
		self.topCV.delete('C1TBP')
		self.topCV.delete('C1TMP')
		
		self.bottCV.delete('C2HNP')
		self.bottCV.delete('C2LPP')
		self.bottCV.delete('C2RPP')
		self.bottCV.delete('C2SGP')
		self.bottCV.delete('C2PVP')
		self.bottCV.delete('C2RLP')
		self.bottCV.delete('C2RRP')
		self.bottCV.delete('C2TBP')
		self.bottCV.delete('C2TMP')		
		
	
	
	
	def move_point1(self,event):
		# Moves a single point for camera 1
		img = self.topCV.find_withtag('topImage')
		point = self.topCV.find_withtag(CURRENT)
		if point == img:
			return
		self.topCV.coords(point,(event.x-5),(event.y-5),(event.x+5),(event.y+5))
		
	def move_point2(self,event):
		# Moves a single point for camera 2
		img = self.bottCV.find_withtag('bottImage')
		point = self.bottCV.find_withtag(CURRENT)
		if point == img:
			return
		self.bottCV.coords(point,(event.x-5),(event.y-5),(event.x+5),(event.y+5))
		
	def parse_data_for_tree(self, data):
		# takes a dict of data values and keys for a frame and assembles a list of the data values in the correct order for insertion into the treeview
		# these values are lists as base, converts them to strings for display. This method is necessary because the load/save stores the data in arbitrary order
		vals = []
		vals.append(str(data['IMG#']))
		vals.append(str(data['C1HN']))
		vals.append(str(data['C1LP']))
		vals.append(str(data['C1RP']))
		vals.append(str(data['C1SG']))
		vals.append(str(data['C1PV']))
		vals.append(str(data['C1RL']))
		vals.append(str(data['C1RR']))
		vals.append(str(data['C1TB']))
		vals.append(str(data['C1TM']))
		vals.append(str(data['C2HN']))
		vals.append(str(data['C2LP']))
		vals.append(str(data['C2RP']))
		vals.append(str(data['C2SG']))
		vals.append(str(data['C2PV']))
		vals.append(str(data['C2RL']))
		vals.append(str(data['C2RR']))
		vals.append(str(data['C2TB']))
		vals.append(str(data['C2TM']))
		return vals
		
	def draw_btn(self,event=None):
		# Draws the annotation skeleton. If there is a treedata entry for the current frame it draws that annotation. else, it draws the last annotation
		# Check if annotation is already drawn (in case it is hidden)
		if self.topCV.find_withtag('C1HNP'):
			return
		
		self.draw_skeleton()
		self.drawn = 1
		
	def rec_annotation(self):
		# compile current annotation to add to treedata and tree view
		self.get_points()
		newData = {'IMG#': self.prevF, 'C1HN': self.C1HNP, 'C1LP': self.C1LPP, 'C1RP': self.C1RPP, 'C1SG': self.C1SGP, 'C1PV': self.C1PVP, 'C1RL': self.C1RLP, 'C1RR': self.C1RRP, 'C1TB': self.C1TBP, 'C1TM': self.C1TMP, 'C2HN': self.C2HNP, 'C2LP': self.C2LPP, 'C2RP': self.C2RPP, 'C2SG': self.C2SGP, 'C2PV': self.C2PVP, 'C2RL': self.C2RLP, 'C2RR': self.C2RRP, 'C2TB': self.C2TBP, 'C2TM': self.C2TMP}
		self.add_treeData(self.currImg1Path.get(), newData)
		return 0
		
	def check_annotation(self, file):
		# checks if annotation exists for file
		return self.treeData.has_key(file)
			
	def update_points(self,data):
		# updates annotation point attributes from treeData entry
		self.C1HNP = data['C1HN']
		self.C1LPP = data['C1LP']
		self.C1RPP = data['C1RP']
		self.C1SGP = data['C1SG']
		self.C1PVP = data['C1PV']
		self.C1RLP = data['C1RL']
		self.C1RRP = data['C1RR']
		self.C1TBP = data['C1TB']
		self.C1TMP = data['C1TM']
		
		self.C2HNP = data['C2HN']
		self.C2LPP = data['C2LP']
		self.C2RPP = data['C2RP']
		self.C2SGP = data['C2SG']
		self.C2PVP = data['C2PV']
		self.C2RLP = data['C2RL']
		self.C2RRP = data['C2RR']
		self.C2TBP = data['C2TB']
		self.C2TMP = data['C2TM']
		
		
	def get_points(self):
		# gets coords of annotation points and writes the values into point attributes
		# Note: int() truncates float values, does not round. This can result in stationary points being off by 1 
		self.C1HNP = [int(self.topCV.coords('C1HNP')[0]+self.diameter),int(self.topCV.coords('C1HNP')[1]+self.diameter)]
		self.C1LPP = [int(self.topCV.coords('C1LPP')[0]+self.diameter),int(self.topCV.coords('C1LPP')[1]+self.diameter)]
		self.C1RPP = [int(self.topCV.coords('C1RPP')[0]+self.diameter),int(self.topCV.coords('C1RPP')[1]+self.diameter)]
		self.C1SGP = [int(self.topCV.coords('C1SGP')[0]+self.diameter),int(self.topCV.coords('C1SGP')[1]+self.diameter)]
		self.C1PVP = [int(self.topCV.coords('C1PVP')[0]+self.diameter),int(self.topCV.coords('C1PVP')[1]+self.diameter)]
		self.C1RLP = [int(self.topCV.coords('C1RLP')[0]+self.diameter),int(self.topCV.coords('C1RLP')[1]+self.diameter)]
		self.C1RRP = [int(self.topCV.coords('C1RRP')[0]+self.diameter),int(self.topCV.coords('C1RRP')[1]+self.diameter)]
		self.C1TBP = [int(self.topCV.coords('C1TBP')[0]+self.diameter),int(self.topCV.coords('C1TBP')[1]+self.diameter)]
		self.C1TMP = [int(self.topCV.coords('C1TMP')[0]+self.diameter),int(self.topCV.coords('C1TMP')[1]+self.diameter)]
		
		self.C2HNP = [int(self.bottCV.coords('C2HNP')[0]+self.diameter),int(self.bottCV.coords('C2HNP')[1]+self.diameter)]
		self.C2LPP = [int(self.bottCV.coords('C2LPP')[0]+self.diameter),int(self.bottCV.coords('C2LPP')[1]+self.diameter)]
		self.C2RPP = [int(self.bottCV.coords('C2RPP')[0]+self.diameter),int(self.bottCV.coords('C2RPP')[1]+self.diameter)]
		self.C2SGP = [int(self.bottCV.coords('C2SGP')[0]+self.diameter),int(self.bottCV.coords('C2SGP')[1]+self.diameter)]
		self.C2PVP = [int(self.bottCV.coords('C2PVP')[0]+self.diameter),int(self.bottCV.coords('C2PVP')[1]+self.diameter)]
		self.C2RLP = [int(self.bottCV.coords('C2RLP')[0]+self.diameter),int(self.bottCV.coords('C2RLP')[1]+self.diameter)]
		self.C2RRP = [int(self.bottCV.coords('C2RRP')[0]+self.diameter),int(self.bottCV.coords('C2RRP')[1]+self.diameter)]
		self.C2TBP = [int(self.bottCV.coords('C2TBP')[0]+self.diameter),int(self.bottCV.coords('C2TBP')[1]+self.diameter)]
		self.C2TMP = [int(self.bottCV.coords('C2TMP')[0]+self.diameter),int(self.bottCV.coords('C2TMP')[1]+self.diameter)]
		
		
	def apply_settings(self):
		# apply settings for GUI	
		
		
		# set values 
		self.osVar.set(self.settings['os'])
		self.ssVar.set(self.settings['ss'])					
		self.noCVar.set(self.settings['noC'])
		self.inFPSVar.set(self.settings['inFPS'])
		self.annVar.set(self.settings['ann'])
		
		return
		
	def read_settings(self):
		# read settings file, update settings object		
		
		config = ConfigParser.ConfigParser()
		
		#TODO: try block this read
		config.read('ann_GUI_config.cfg')
		
		self.settings['os'] = config.getint('Settings','os')
		self.settings['ss'] = config.get('Settings','ss')
		self.settings['noC'] = config.getint('Settings','noC')
		self.settings['inFPS'] = config.getint('Settings','inFPS')
		self.settings['ann'] = config.getint('Settings','ann')
		
		self.apply_settings()
		
		
		
	def write_settings(self):
		# write a settings config file with values from self.settings
		
		config = ConfigParser.ConfigParser()
		
		config.add_section('Settings')
		
		for key in self.settings:
			config.set('Settings',key,self.settings[key])
			
		with open('ann_GUI_config.cfg', 'wb') as configfile:
			config.write(configfile)
		
	
	def ss_to_int(self, ss):
		# translates ss string to int for calculating size parameters
		# TOOD: maintain separat "res list" parameter for both settings and size functions
		sizes = { "1920x1080": 1800, "1600x900": 1500, "1280x720": 1200, "800x600": 720 }
		return sizes.get(ss, 1800)
		
		
		
		
		
			
		
		
	
				
	
	
		
		
		
		
	

root = Tk()

app = App(root)
root.title("Lab Video Annotator v0.18")

root.mainloop()
root.destroy()