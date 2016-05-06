from Tkinter import *
import tkSimpleDialog

class HelpDialog(tkSimpleDialog.Dialog):
	
	def body(self, master):
		
		Label(master, text="Annotation GUI Help").grid(row=0)
		Label(master, text="Help functionality is not yet implemented").grid(row=1)
		Label(master, text="Contact the Program Creator for more information").grid(row=2)
		
		return None
	
	
	
	def apply(self):
		return None 
		
	def buttonbox(self):
		return None 