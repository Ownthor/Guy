import bge, math
from numpy import array, dot

# scale sets the speed of motion
scale = 0.0010 , 0.0010
# Tscale is for translations
Tscale = 9.0 , 9.0
# Rscale is for rotations
Rscale = 3.0 , 3.0

# Transform the mouse coordinates to see how far the mouse has moved. and reset position of mouse to center
def mousePos(mouse):
	x = (bge.render.getWindowWidth() / 2 - mouse.position[0]) * scale[0]
	y = (bge.render.getWindowHeight() / 2 - mouse.position[1]) * scale[1]
	# Centre the mouse
	bge.render.setMousePosition(int(bge.render.getWindowWidth() / 2), int(bge.render.getWindowHeight() / 2))
	x = min(0.1,max(-0.1,x))
	y = min(0.1,max(-0.1,y))
	return (x, y)

def rotateM(own, Mouse,parent):
	x, y = mousePos(Mouse)
	
	xtheta = x*Rscale[0]
	ytheta = y*Rscale[1]
	#c5 = math.cos((5theta)
	
	Rx = array([[1.0,0.0,0.0],[0.0,math.cos(ytheta),-math.sin(ytheta)],[0.0,math.sin(ytheta),math.cos(ytheta)]])
	#Ry = array([[math.cos(ytheta),0.0,math.sin(ytheta)],[0.0,1.0,0.0],[-math.sin(ytheta),0.0,math.cos(ytheta)]])
	Rz = array([[math.cos(xtheta),-math.sin(xtheta),0.0],[math.sin(xtheta),math.cos(xtheta),0.0],[0.0,0.0,1.0]])
	
	worldOri = array(parent.worldOrientation)
	parent.worldOrientation = dot(worldOri,Rz)
	#print(parent.worldOrientation)
	localOri = array(own.localOrientation)	
	own.localOrientation = dot(localOri,Rx)
	#print(own.localOrientation)
			
def translateM(Mouse,parent):
	x, y = mousePos(Mouse)
	
	xt = x*Tscale[0]*2
	yt = y*Tscale[1]*2
	
	pWo = parent.worldOrientation#	((pWo[0][0],pWo[0][1],pWo[0][2]),
								#	(pWo[1][0],pWo[1][1],pWo[1][2]),
								#	(pWo[2][0],pWo[2][1],pWo[2][2]))
	pWp = parent.localPosition
	parent.localPosition = (pWp[0]+yt*pWo[0][1]-xt*pWo[1][1],pWp[1]+yt*pWo[0][0]-xt*pWo[1][0],pWp[2])
	
def rotateK(own,z,parent):
	
	xtheta = z/10
			
	Rz = array([[math.cos(xtheta),-math.sin(xtheta),0.0],[math.sin(xtheta),math.cos(xtheta),0.0],[0.0,0.0,1.0]])
	
	worldOri = array(parent.worldOrientation)
	parent.worldOrientation = dot(worldOri,Rz)
		
def translateK(x,y,parent):
	
	xt = x
	yt = y
	
	pWo = parent.worldOrientation#	((pWo[0][0],pWo[0][1],pWo[0][2]),
								#	(pWo[1][0],pWo[1][1],pWo[1][2]),
								#	(pWo[2][0],pWo[2][1],pWo[2][2]))
	pWp = parent.localPosition
	parent.localPosition = (pWp[0]+yt*pWo[0][1]-xt*pWo[1][1],pWp[1]+yt*pWo[0][0]-xt*pWo[1][0],pWp[2])

   
def main(cont):
	cont = bge.logic.getCurrentController()
	own = cont.owner
	mouse = cont.sensors["Mouse"]
	MouseM = cont.sensors["MouseM"]
	MUp = cont.sensors["MouseU"]
	Mdown = cont.sensors["MouseD"]
	shift = cont.sensors["Shift"]
	WK = cont.sensors["WK"]
	AK = cont.sensors["AK"]
	SK = cont.sensors["SK"]
	DK = cont.sensors["DK"]
	
	ZoomA = cont.actuators['Zoom']
	
	parent = shift.owner
	
	
	if MUp.positive:
		if shift.positive:
			own['Zoom'] = min(106,own['Zoom']+5)
		else:
			own['Zoom'] = min(106,own['Zoom']+1)
		cont.activate(ZoomA)
	if Mdown.positive:
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
			if x != 0:
				rotateK(own,x,parent)
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