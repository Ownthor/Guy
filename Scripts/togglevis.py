import bge

def main(cont):
	own = cont.owner
	Toggle = cont.sensors['Toggle_Key']
	
	if own.visible == False and own['Go'] == True:
		own.visible = True
		own['Go'] = False
	elif own.visible == True and own['Go'] == True:
		own.visible = False
		own['Go'] = False
	elif own['Go'] == False:
		own['Go'] = True