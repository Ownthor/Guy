import bge

# variables defined here will only be set once when the
# module is first imported. Set object specific vars
# inside the function if you intend to use the module
# with multiple objects.

Range_Mult = 1
AOE_Range_Mult = 1
Fire_Rate_Mult = 1

def main(cont):
	
	Damage = 1
	Range = 1
	AOE_Range = 1
	AOE = False
	Fire_Rate = 1
	
	Type = ["B1","Pistol"]
	
    own = cont.owner
	
	Enemey_Scanner = cont.sensors['Enemy Near']		# Near sensor that detects all enemies within range
	
    Targeter_Base = cont.actuators['Target_Base']	# Edit Object Actuator, (track to) Used to face the base at the targeted enemy
    Targeter_Gun = cont.actuators['Target_Gun']		# Edit Object Actuator, (track to) Used to face the gun at the targeted enemy
	
	
	
    sens = cont.sensors['mySensor']
    actu = cont.actuators['myActuator']

    if sens.positive:
        cont.activate(actu)
    else:
        cont.deactivate(actu)

# dont call main(bge.logic.getCurrentController()), the py controller will

def fire(Target, cont):
	#
#object is fired, if taget dies before impact... do stuff