import bge, math
from numpy import array, dot

# scale sets the speed of motion
scale = 0.0010 , 0.0010
# Tscale is for translations
Tscale = 9.0 , 9.0
# Rscale is for rotations
Rscale = 3.0 , 3.0

# Transforms the mouse coordinates to see how far the mouse has moved. and reset position of mouse to center
def mousePos(mouse):
	# This translates the current position of the mouse relative to the center of the screen into a delta x
	x = (bge.render.getWindowWidth() / 2 - mouse.position[0]) * scale[0]
	# This translates the current position of the mouse relative to the center of the screen into a delta y
	y = (bge.render.getWindowHeight() / 2 - mouse.position[1]) * scale[1]
	# This moves the mouse cursor back to the center of the screen after seeing how much it has moved
	bge.render.setMousePosition(int(bge.render.getWindowWidth() / 2), int(bge.render.getWindowHeight() / 2))
	# this makes sure the x value is no greater then 0.1 and no less then -0.1
	x = min(0.1,max(-0.1,x))
	# this makes sure the y value is no greater then 0.1 and no less then -0.1
	y = min(0.1,max(-0.1,y))
	# this returns the x and y values to be used in by in function called this function
	return (x, y)

# This function rotates the camera a certain amount based two angles given
def rotateAny(own,ztheta,xtheta,parent):	

	# This makes a 2d array that is used to apply x rotation by dot multiplying this matrix to the current local orientation matrix
	Rx = array([[1.0,0.0,0.0],[0.0,math.cos(xtheta),-math.sin(xtheta)],[0.0,math.sin(xtheta),math.cos(xtheta)]])
	# This makes a 2d array that is used to apply z rotation by dot multiplying this matrix to the current global orientation matrix
	Rz = array([[math.cos(ztheta),-math.sin(ztheta),0.0],[math.sin(ztheta),math.cos(ztheta),0.0],[0.0,0.0,1.0]])
	
	# This gets ,in the form of an array, the current global orientaion matrix of the empty that the camera is parented to
	worldOri = array(parent.worldOrientation)
	# This sets the current world orientation to the dotProduct of the current world orientation and the z Rotaion array
	# This effectivly applies the rotation in the z direction (Turns the camera left or right)
	parent.worldOrientation = dot(worldOri,Rz)
		
	# This gets ,in the form of an array, the current local orientaion matrix of the empty that the camera is parented to
	localOri = array(own.localOrientation)	
	# This sets the current local orientation to the dotProduct of the current local orientation and the x Rotaion array
	# This effectivly applies the rotation in the x direction (Rotates the camera up or down)
	own.localOrientation = dot(localOri,Rx)
	
# Rotates the camera using mouse movements
def rotateM(own, Mouse,parent):
	# This gets the delta x and delta y of the mouse as the player moves it while holding the middle mouse button to be applied to rotating the camera
	x, y = mousePos(Mouse)
	
	# calls the general rotate function with correctly scaled inuts
	rotateAny(own,x*Rscale[0],y*Rscale[1],parent)
	
# Applies rotation from key inputs
def rotateK(own,x,y,parent):
	# calls the general rotate function with correctly scaled inuts
	rotateAny(own,x/10,y/10,parent)

# Moves the camera using given inputs
def translateAny(xt,yt,parent):
	
	# This gets the global orientation matrix of the cameras parent object in order to make sure the camera is moved in the correct direction
	pWo = parent.worldOrientation#	((pWo[0][0],pWo[0][1],pWo[0][2]),
								#	(pWo[1][0],pWo[1][1],pWo[1][2]),
								#	(pWo[2][0],pWo[2][1],pWo[2][2]))
	# This gets the position of the cameras parent object
	pWp = parent.localPosition
	
	# This applies the movement to the cameras parent objects location matrix by applying the movemens
	# in each axis based off the xt and xy and the direction the camera is facing
	parent.localPosition = (pWp[0]+yt*pWo[0][1]-xt*pWo[1][1],pWp[1]+yt*pWo[0][0]-xt*pWo[1][0],pWp[2])

# Moves the camera using mouse movements
def translateM(Mouse,parent):
	# This gets the delta x and delta y of the mouse as the player moves it while holding shift and the middle mouse button to be applied to moving the camera
	x, y = mousePos(Mouse)
	
	# This calles the general translate function with correctly scalled inputs
	translateAny(x*Tscale[0]*2,y*Tscale[1]*2,parent)

# Moves the camera using key inputs
def translateK(x,y,parent):
	
	# This calles the general translate function with correctly scalled inputs
	translateAny(x,y,parent)

   
def main(cont):
	#cont = bge.logic.getCurrentController() # not needed when being called as module blender automatically does this
	# cont is the controller that is calling this function
	own = cont.owner						# own is the object that owns the controller calling this function (the controller is part of the object)
	mouse = cont.sensors["Mouse"]			# mouse is a sensor that is positive when the mouse is moving
	MouseM = cont.sensors["MouseM"]			# MouseM is a sensor that is positive when the middle mouse button is pressed (mouse wheel click)
	MUp = cont.sensors["MouseU"]			# MUp is a sensor that is positive when the mouse wheel is scrolled up
	Mdown = cont.sensors["MouseD"]			# Mdown is a sensor that is positive when the mouse wheel is scrolled down
	shift = cont.sensors["Shift"]			# shift is a sensor that is positive when the left 'Shift' key is pressed (not when the right 'Shift' key is pressed)
	WK = cont.sensors["WK"]					# WK is a sensor that is positive when the 'W' key is pressed
	AK = cont.sensors["AK"]					# AK is a sensor that is positive when the 'A' key is pressed
	SK = cont.sensors["SK"]					# SK is a sensor that is positive when the 'S' key is pressed
	DK = cont.sensors["DK"]					# DK is a sensor that is positive when the 'D' key is pressed
	PlsK = cont.sensors["PLsK"]				# new key added # PlsK is a sensor that is positive when the '+' key is pressed
	MinK = cont.sensors["MinK"]				# new key added # MinK is a sensor that is positive when the '-' key is pressed
	
	# ZoomA is an Action actuator that is used to change the amount of zoom on the camera by changing the fram that the camera animation is at
	ZoomA = cont.actuators['Zoom']			# to long to fit here ^^^
	# If an object has a parent object then they are physically attached such that moving the parent moves the child, but moving the child does not effect the parent
	parent = shift.owner					# Parent is an empty object that the camera is parented to, the shift sensor belongs to the parent
	
	# Zoom in if scrolling up or if the '+' key is pressed
	if MUp.positive or PlsK.positive:
		if shift.positive: # Zoom in faster if shift is also pressed
			own['Zoom'] = min(106,own['Zoom']+5) # move 5 frames forward until at max zoom
		else:
			own['Zoom'] = min(106,own['Zoom']+1) # move 1 frame forward until at max zoom
		cont.activate(ZoomA)
		
	if Mdown.positive or MinK.positive:
		if shift.positive:
			own['Zoom'] = max(5,own['Zoom']-5)
		else:
			own['Zoom'] = max(5,own['Zoom']-1)
		cont.activate(ZoomA)

	if MouseM.positive and mouse.positive: #mouse camera rotation and translation
		if shift.positive:
			translateM(mouse,parent)
		else:
			rotateM(own,mouse,parent)
	# keys for camera translation and zoom ,globalz rotation		
	if WK.positive or AK.positive or SK.positive or DK.positive:	#
		x,y = 0,0
		if WK.positive:
			y += 0.3
		if SK.positive:
			y += -0.3
		if AK.positive:
			x += 0.3
		if DK.positive:
			x += -0.3
		
		if shift.positive:
			if x != 0 or y != 0:
				rotateK(own,x,y,parent)
			if y > 0:
				own['Zoom'] = min(106,own['Zoom']+1)
				cont.activate(ZoomA)
			elif y < 0:
				own['Zoom'] = max(5,own['Zoom']-1)
				cont.activate(ZoomA)
		elif x != 0 or y != 0:
			translateK(x,y,parent)
	
'''
# Set the amount of motion: X is applied in world coordinates...
wmotion.useLocalTorque = False
wmotion.torque = ((0.0, 0.0, pos[0]))

# ...Y is applied in local coordinates
lmotion.useLocalTorque = True
lmotion.torque = ((-pos[1], 0.0, 0.0))

# Activate both actuators
cont.activate(lmotion)
cont.activate(wmotion)

'''