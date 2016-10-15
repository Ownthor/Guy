import bge
import mathutils

def main(cont):
	own = cont.owner
	
	Mover = cont.sensors['MouseO']
	
	VIS = cont.actuators['VIS']
	Aempty = VIS.owner
	
	# if mouse pointer is over an object put a big ass arrow over the intersection of object and mouse pointer
	if Mover.positive:
		Aempty.worldPosition = Mover.hitPosition
		#Aempty.worldOrientation = Mover.hitNormal # Have the arrow oriented to the normal of the face your mouse touches
		VIS.visibility = True
	else:
		VIS.visibility = False
	cont.activate(VIS)
	