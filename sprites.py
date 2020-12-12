import pygame
import os

##############################
#Robot
enemywalk=[pygame.image.load(os.path.join("sprites/Robot/Robot_walk",image)) for image in os.listdir(os.path.join("sprites/Robot","Robot_Walk"))]
enemyattackleft=[pygame.image.load(os.path.join("sprites/Robot/Robotattackleft",image)) for image in os.listdir(os.path.join("sprites/Robot","Robotattackleft"))]
enemyattackright=[pygame.image.load(os.path.join("sprites/Robot/Robotattackright",image)) for image in os.listdir(os.path.join("sprites/Robot","Robotattackright"))]


                      
############################################################################################################################################
#Shooter
shooterwalk=[pygame.image.load(os.path.join("sprites/Shooter/shooterwalk",image)) for image in os.listdir(os.path.join("sprites/Shooter","shooterwalk"))]
shootershootleft = [pygame.image.load(os.path.join("sprites/Shooter","shootershootleft.png")),pygame.image.load(os.path.join("sprites/Shooter","shootershootleft.png"))]
shootershootright= [pygame.image.load(os.path.join("sprites/Shooter","shootershootright.png")),pygame.image.load(os.path.join("sprites/Shooter","shootershootright.png"))]

############################################################################################################################################

#red
redwalking=[pygame.image.load(os.path.join("sprites/Redguy/Redwalk",image)) for image in os.listdir(os.path.join("sprites/Redguy","Redwalk"))]
redattackingright=[pygame.image.load(os.path.join("sprites/Redguy/Redattackingright",image)) for image in os.listdir(os.path.join("sprites/Redguy","Redattackingright"))]
redattackingleft =[pygame.image.load(os.path.join("sprites/Redguy/Redattackingleft",image)) for image in os.listdir(os.path.join("sprites/Redguy","Redattackingleft"))]

#Flyer
flyerwalking=[pygame.image.load(os.path.join("sprites/Flyer/flyerwalk",image)) for image in os.listdir(os.path.join("sprites/Flyer","flyerwalk"))]
flyerattackingleft=[pygame.image.load(os.path.join("sprites/Flyer/flyerattackleft",image)) for image in os.listdir(os.path.join("sprites/Flyer","flyerattackleft"))]
flyerattackingright = [pygame.image.load(os.path.join("sprites/Flyer/flyerattackright",image)) for image in os.listdir(os.path.join("sprites/Flyer","flyerattackright"))]


#User
character = pygame.image.load(os.path.join("sprites/User","char.png"))
healthlogo = pygame.image.load(os.path.join("sprites/User","healthlogo.png"))
charshootleft=[pygame.image.load(os.path.join("sprites/User/charshootleft",image)) for image in os.listdir(os.path.join("sprites/User","charshootleft"))]
charshootright=[pygame.image.load(os.path.join("sprites/User/charshootright",image)) for image in os.listdir(os.path.join("sprites/User","charshootright"))]
walkright =[pygame.image.load(os.path.join("sprites/User/walkright",image)) for image in os.listdir(os.path.join("sprites/User","walkright"))]
walkleft=[pygame.image.load(os.path.join("sprites/User/walkleft",image)) for image in os.listdir(os.path.join("sprites/User","walkleft"))]
############################################################################################################################################
#Extras
damage=pygame.image.load(os.path.join("sprites/Items","damage.png"))
ammo_pic=pygame.image.load(os.path.join("sprites/Items","bullet.png"))
health_pic=pygame.image.load(os.path.join("sprites/Items","healthitem.png"))

	
#######################################


bosswalk= [pygame.image.load(os.path.join("sprites/Trevor/Trevorwalk",image)) for image in os.listdir(os.path.join("sprites/Trevor","Trevorwalk"))]
bossfireleft = [pygame.image.load(os.path.join("sprites/Trevor/Trevorattackleft",image)) for image in os.listdir(os.path.join("sprites/Trevor","Trevorattackleft"))]
bossfireright = [pygame.image.load(os.path.join("sprites/Trevor/Trevorattackright",image)) for image in os.listdir(os.path.join("sprites/Trevor","Trevorattackright"))]
bossdeathleft=pygame.image.load(os.path.join("sprites/Trevor","bossdeathleft.png"))



#####
stevewalk = [pygame.image.load(os.path.join("sprites/Steve/stevewalk",image)) for image in os.listdir(os.path.join("sprites/Steve","Stevewalk"))]
steveattackleft = [pygame.image.load(os.path.join("sprites/Steve","steveattackleft.png")),pygame.image.load(os.path.join("sprites/Steve","steveattackleft.png"))]
steveattackright =[pygame.image.load(os.path.join("sprites/Steve","steveattackright.png")),pygame.image.load(os.path.join("sprites/Steve","steveattackright.png"))]
stevedeathleft=pygame.image.load(os.path.join("sprites/Steve","stevedeathleft.png"))


############
signuswalk = [pygame.image.load(os.path.join("sprites/Signus/Signuswalk",image)) for image in os.listdir(os.path.join("sprites/Signus","Signuswalk"))]
signusattackleft=[pygame.image.load(os.path.join("sprites/Signus/signusattackleft",image)) for image in os.listdir(os.path.join("sprites/Signus","signusattackleft"))]
signusattackright= [pygame.image.load(os.path.join("sprites/Signus/signusattackright",image)) for image in os.listdir(os.path.join("sprites/Signus","signusattackright"))]
signusdeathleft= pygame.image.load(os.path.join("sprites/Signus","signusdeath.png"))

area1=[pygame.image.load(os.path.join("sprites/Backgrounds/Level 1",image)) for image in os.listdir(os.path.join("sprites/Backgrounds","Level 1"))]
area2=[pygame.image.load(os.path.join("sprites/Backgrounds/Level 2",image)) for image in os.listdir(os.path.join("sprites/Backgrounds","Level 2"))]
area3=[pygame.image.load(os.path.join("sprites/Backgrounds/Level 3",image)) for image in os.listdir(os.path.join("sprites/Backgrounds","Level 3"))]


