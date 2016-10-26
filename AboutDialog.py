from Tkinter import *
import tkSimpleDialog

class AboutDialog(tkSimpleDialog.Dialog):

	def body(self, master):
	
		Label(master, text="Lab Video Annotator v0.18").grid(row=0)
		Label(master, text="     ").grid(row=1) # placeholder
		Label(master, text="Created by: Adrian Lindsay").grid(row=2)
		Label(master, text="Email: adrianj.lindsay@gmail.com").grid(row=3)
		Label(master, text="Version Information:").grid(row=4)
		Label(master, text="Not yet implemented").grid(row=5)		
		
		
	def apply(self):
		return None
		
	def buttonbox(self):
		return None		