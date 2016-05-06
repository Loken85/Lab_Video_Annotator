from Tkinter import *
import tkMessageBox
import os

# Settings Dialogue to change GUI General (non-sessional) settings. Should read in current settings from file, and write new settings to that file
class SettingsDlg(Toplevel):

	def __init__(self,parent,settings):
	
		Toplevel.__init__(self,parent)
		self.transient(parent)
		
		self.title("Settings")
		
		self.parent = parent		
		
		self.result = None 
		
		#vars for settings fields, button values, etc.		
		self.osVar = IntVar()
		self.ssVar = StringVar()
		self.resList = ["1920x1080", "1600x900", "1280x720", "800x600"]				
		self.noCVar = IntVar()
		self.inFPSVar = IntVar()
		self.annVar = IntVar()
		
		self.read_set(settings)
		
		
		body = Frame(self)
		self.initial_focus = self.body(body)
		body.pack(padx=5,pady=5)
		
		self.controls(self)
		
		self.grab_set()
		
		if not self.initial_focus:
			self.initial_focus = self
			
		self.protocol("WM_DELETE_WINDOW", self.cancel)
		
		self.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
		
		self.initial_focus.focus_set()
		
		self.wait_window(self)
		
		
	def body(self,master):
	
		Label(master, text="Global Settings").grid(row=0)
		
		Label(master, text="Operating System:").grid(row=1,column=0)		
		Radiobutton(master, text="Windows", variable=self.osVar, value=0).grid(row=1,column=1)
		Radiobutton(master, text="OSX/Linux", variable=self.osVar, value=1).grid(row=1,column=2)
		
		Label(master, text="Screen Size:").grid(row=2,column=0)
		# option menu: 1920x1080, 1600x900, 1280x720, 800x600 
		resOpt = apply(OptionMenu, (master, self.ssVar) + tuple(self.resList))			
		resOpt.grid(row=2,column=1)
		
		Label(master, text="No. Cameras:").grid(row=3,column=0)
		Radiobutton(master, text="1", variable=self.noCVar, value=1).grid(row=3,column=1)
		Radiobutton(master, text="2", variable=self.noCVar, value=2).grid(row=3,column=2)
		
		
		Label(master, text="Input FPS:").grid(row=4,column=0)
		Spinbox(master, from_=1, to=60, textvariable = self.inFPSVar).grid(row=4,column=1)
				
		Label(master, text="Annotation Type:").grid(row=5,column=0)
		Radiobutton(master, text="2D", variable=self.annVar, value=0).grid(row=5,column=1)
		Radiobutton(master, text="3D", variable=self.annVar, value=1).grid(row=5,column=2)
		
		# TODO: return widget that should have focus
		return None
		
	def controls(self, master):
	
		controlFrame = Frame(master)
		
		subButton = Button(controlFrame, text="Submit",command=self.submit).grid(row=0,column=0)
		cancelButton = Button(controlFrame, text="Cancel",command=self.cancel).grid(row=0,column=1)	
		controlFrame.pack(padx=5,pady=5)
		return
		
	def submit(self, event=None):
	
		if not self.validate():
			self.initial_focus.focus_set()
			return
		
		
		tkMessageBox.showwarning("Submit Settings", "Settings will not be applied until the program is restarted.")
		
		self.write_set()
		self.withdraw()
		
		self.update_idletasks()		
		
		self.cancel()

	
		
	def cancel(self,event=None):
		
		self.parent.focus_set()
		self.destroy()
		
	def validate(self):
	
		return 1
		
	def write_set(self):
		# copy values into settings/result
		
		settings = {}
		settings['os'] = self.osVar.get()
		settings['ss'] = self.ssVar.get()
		settings['noC'] = self.noCVar.get()
		settings['inFPS'] = self.inFPSVar.get()
		settings['ann'] = self.annVar.get()
		
		self.result = settings
		
	
		
		
	def read_set(self, settings):
		# call set on vars using values from settings object
		self.osVar.set(settings['os'])
		self.ssVar.set(settings['ss'])					
		self.noCVar.set(settings['noC'])
		self.inFPSVar.set(settings['inFPS'])
		self.annVar.set(settings['ann'])
		return
		