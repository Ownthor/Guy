import bge

def main(cont):
	gameover = cont.sensors['END']
	newgold = cont.sensors['ChangeG']
	newlives = cont.sensors['ChangeL']
	Ehit = cont.sensors['Collision']
	MSG = cont.sensors['Msg']
	Once = cont.sensors['Always']
	
	
	Overlay = cont.actuators['Scene']
	pause = cont.actuators['Pause'] 
	restart = cont.actuators['Restart']
	
	own = cont.owner
	
	bge.logic.globalDict['Gold'] = own['Gold']
	
	if MSG.positive:
		for msg in MSG.bodies:
			own['Gold'] += int(msg)
			bge.logic.globalDict['Gold'] = own['Gold']
	if newgold.positive or Once.positive:
		bge.logic.sendMessage("Goldset", str(own['Gold']),"", "")
	if newlives.positive or Once.positive:
		bge.logic.sendMessage("Livesset", str(own['Lives']),"", "")
	if Ehit.positive:
		Enemy = Ehit.hitObject
		if own['Lives'] > Enemy['Life']:
			own['Lives'] -= Enemy['Life']
			Enemy.endObject()
		else:
			Enemy.endObject()
			##cont.activate(Overlay)
			##cont.activate(pause)
			cont.activate(restart)