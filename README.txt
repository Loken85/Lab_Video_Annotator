README:

GUI for annotating Lab Rodent Video

By Adrian Lindsay and Daniel Leibovitz

 Author: Adrian Lindsay
 Email: adrianj.lindsay@gmail.com
 
Intent and Use:

This GUI was built in order to manually annotate video from rodent operant boxes. As configured, 
it takes as input frames from two cameras and allows a user to mark positions of 9 points from frame
to frame.  The GUI writes the annotations into a JSON file for easy retrieval and portability. It 
was built using the tkinter python GUI package, and will require a distribution of Python 2.7 to use.
 

This is a work in progress, with many rough edges and some incomplete functionality. If you have
questions regarding functionality, you can contact the author by email.  


Settings:

The GUI makes use of an external settings file. This file (config) can be manually edited, or changed 
from within the program by using the settings dialogue. This allows you to change the resolution,
number of cameras, FPS or framerate, or import external annotations. Also contains a setting for the
current OS: 0=Windows based, 1=Unix based

Sessions:

Sets of annotations are associated with a session. Session details can be changed through an in program
dialogue, including filepaths for input frames, experiment details, and output filename.  

Annotations:

The video frames can be navigated by hotkey, or manually by entering values in the current session boxes
on the top left. To annotate, first draw the current annotation (hotkey:"s") (this will draw either the
previous frame's annotation, or the default annotation). The 18 points, 9 for each camera, can then be
dragged to the correct position (click on the point you want to reposition, and drag to the desired
location). Then advance to the next frame, draw the annotation, and reposition as needed. Repeat until 
all frames are annotated (or you have succumbed to boredom or madness). 


Each row of annotations contains 18 points, 9 for each camera, each with a corresponding colour: 

Head/Nose	-White
Left Paw	-Blue
Right Paw	-Red
Shoulder Girdle	-Yellow
Pelvis	-Orange
Rear Left Paw	-Dark Blue
Rear Right Paw	-Dark Red
Tail Base	- Violet
Tail Midpoint	- Dark Violet


Hotkeys:

Forward 1 Frame: "d" or "right"
Backward 1 Frame: "a" or "left"
Draw current annotation: "s"
First Frame: "Home"
Last Frame: "End"

Date Explorer:

The data explorer is a standalone GUI for reformatting or exporting annotations. It reads in the JSON 
annotations, and is currently configured to export the data as 2D and 3D numpy arrays. This can be
reconfigured within the "processData" function.


