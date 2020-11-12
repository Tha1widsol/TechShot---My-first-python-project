import pygame                    #
import random                    # 
from sprites import*             # These are modules that are imported in the program
import copy                      #
from keychanges import keychange #
from database import *
from ceasarcipher import cipher

pygame.init()       

pygame.display.set_caption("TechShot")    

Windowx=1000                        # These are global variables for the window size(1000 X 1000)
Windowy=1000

screen = pygame.display.set_mode((Windowx,Windowy)) # This creates the screen

Colours={"Red":(255,0,0),"Blue":(0,0,255),"Green":(0,255,0),"Grey":(128,128,128),"Black":(0,0,0),"Light Grey":(211,211,211),"White":(255,255,255),"Yellow":(255,255,0)}
# Dictionary for colours

class Character(): # This is the character class that makes a character 
    frame_count=0  #Class variable called frame_count
    def __init__(self,Vertical,health,speed,attackanimationleft,attackanimationright): 
        self.Horizontal=None
        self.Vertical=Vertical    
        self.health=health
        self.speed=speed   
        self.health_bar_height=5   # These are attributes of the character
        self.health_bar_length=50   
        self.alive=True   
        self.Faceleft=False    
        self.Faceright=False    
        self.damage_taken=0
        self.attackanimationleft=attackanimationleft    
        self.attackanimationright=attackanimationright    
    
    def animation(self,frames):  # This is the method that allows each character to have animations. These include walking and attacking
        screen.blit(frames[self.frame_count-len(frames)],(self.Horizontal,self.Vertical))   
        self.frame_count+=1   
        if self.frame_count>=len(frames):    
            self.frame_count=0    # This creates a loop
        
    def health_bar(self): # A method to draw a health bar for each character
        Text(str(self.health-self.damage_taken)+"/"+str(self.health),self.Horizontal+35,self.Vertical-30,25)
        pygame.draw.rect(screen,Colours["Green"],(self.Horizontal+35,self.Vertical-10, self.health_bar_length,self.health_bar_height))    
          
    def execute(self,player): # execute method that puts all the methods together. This is so that later on, the entire object could run with one method
        if not Pause.paused:
            if self.alive:    
                self.move(player)    
                self.health_bar()   
                player.check_if_hit(self,self.Horizontal+35,self.Vertical-10)   
    
            object_movement(self,player.speed)  # Moves the object towards the player 
      
      
class Enemy(Character): # This is the enemy class that makes an enemy. This inherits from the character class
    notice_range=Windowx   #This is the range the player has to be within in order for the enemy to notice the player.
    def __init__(self,Vertical,health,speed,enemy_damage,walkanimation,attackanimationleft,attackanimationright,attack_Range,y_calibrate): 
        super().__init__(Vertical,health,speed,attackanimationleft,attackanimationright) # All the attributes of the base class is drawn within this class
        self.walkanimation=walkanimation    
        self.path=player.Horizontal
        self.enemy_damage=enemy_damage  #These are atrributes of the enemy
        self.attack_Range=attack_Range    
        self.y_calibrate=y_calibrate # This attribute is used because some enemy sprites may appear bigger which needs to be calibrated so that the animation would make sense.
        self.damaged=False
        
    def damage_player(self):   # This method allows the enemy to damage the player depending on what kind of enemy it is. 
        if player.damage_taken!=player.health:    
                screen.blit(damage,(player.Horizontal-2,player.Vertical))    
                player.health-=self.enemy_damage
                
    def move(self,player):   # This method allows the enemy to move towards the player if it is in range.
        if self.Horizontal-self.notice_range<player.Horizontal:   
            if self.Horizontal>self.path+self.attack_Range:    
                self.Horizontal-=self.speed    
                self.Faceleft=True  
                self.Faceright=False  
                self.animation(self.walkanimation)  
                  
            elif self.Horizontal<self.path-self.attack_Range:    
                    self.Horizontal+=self.speed    
                    self.Faceright=True  
                    self.Faceleft=False  
                    self.animation(self.walkanimation)  
                      
            else: # If the enemy is close enough to the player, It will start attacking.
                self.attack(player)
                
     
        
    def attack(self,player): # This is the attack method that is used to attack the player. The animation has to face the right way.
        if self.Horizontal>=self.path and self.Vertical ==player.Vertical-self.y_calibrate:    
            self.animation(self.attackanimationleft)    
            self.damage_player()   
     
            
        elif self.Horizontal<=self.path and self.Vertical ==player.Vertical-self.y_calibrate:    
            self.animation(self.attackanimationright)    
            self.damage_player()
            
        else:  
            screen.blit(self.walkanimation[0],(self.Horizontal,self.Vertical))
            


class Shooter(Enemy): # Enemies can also be shooters, This class inherits from the enemy class 
    enemy_bullets=[]   
    def __init__(self,Vertical,health,speed,enemy_damage,walkanimation,attackanimationleft,attackanimationright,attack_Range,y_calibrate,bullet_speed,bullet_colour):    
        super().__init__(Vertical,health,speed,enemy_damage,walkanimation,attackanimationleft,attackanimationright,attack_Range,y_calibrate)    
        self.bullet_speed=bullet_speed
        self.bullet_colour=bullet_colour
        self.attackanimationleft=attackanimationleft # These are all the attributes of the class
        self.attackanimationright=attackanimationright
        self.bulletloop=0 # This variable is needed so that the bullets arent grouped together.
        
                
    def attack(self,player): # This method allows the enemy to shoot across the screen.
        if self.Faceleft:    
            self.animation(self.attackanimationleft)
        else: 
            self.animation(self.attackanimationright)
            
        if self.bulletloop==0:
            if len(self.enemy_bullets)<1: # This is so that the shooter shoots one bullet at a time.
                if self.Horizontal >player.Horizontal:     
                    self.Faceright=False    # Enemy has to be facing the right way.
                    self.Faceleft=True
                    facing=-1   
                    self.enemy_bullets.append(Bullets(round(self.Horizontal+45),round(self.Vertical+self.y_calibrate),self.bullet_speed,self.bullet_colour,4,facing)) #Bullets are pushed onto a stack   
                      
                elif self.Horizontal <player.Horizontal:       
                    self.Faceleft=False    
                    self.Faceright=True
                    facing=1    
                    self.enemy_bullets.append(Bullets(round(self.Horizontal+115),round(self.Vertical+self.y_calibrate),self.bullet_speed,self.bullet_colour,4,facing))
                    
            self.bulletloop+=1 # increment bullet loop
            
        Bullets.fix_bullets(self) # This method fixes the bullets
        Bullets.shoot(self.enemy_bullets) # Shoots bullets
        self.check_if_hit(player) # See if it hits player
            
    def check_if_hit(self,player): # This is the method to see if the bullets have collided with the player.
        for bullet in self.enemy_bullets:
            if bullet.Vertical>player.Vertical and bullet.Vertical<player.Vertical+100 :
                    if bullet.Horizontal> player.Horizontal and bullet.Horizontal<player.Horizontal+100:    
                            self.damage_player() 
                            self.enemy_bullets.pop(self.enemy_bullets.index(bullet))# If collided, then the bullets are popped from the top of the stack.
                                
      

              
class Boss(Shooter):
    def __init__(self,Vertical,health,speed,enemy_damage,walkanimation,attackanimationleft,attackanimationright,bossdeathleft,attack_Range,y_calibrate,bullet_speed,bullet_colour,name,jump_decision,increased_damage):
        super().__init__(Vertical,health,speed,enemy_damage,walkanimation,attackanimationleft,attackanimationright,attack_Range,y_calibrate,bullet_speed,bullet_colour)
        self.Horizontal=1000
        self.path=None
        self.health_bar_length=600
        self.health_bar_height=10
        self.staying_time=100 # This is the time that the boss is allowed to stay before moving
        self.JumpSpeed=10
        self.death_time=20     # This is the boss class that inherits from Shooter. It has more attributes and methods.
        self.healthbar_x=200
        self.healthbar_y=150
        self.name=name
        self.jump_decision=jump_decision # The amount of health in order for the boss to start jumping.
        self.bossdeathleft=bossdeathleft
        self.increased_damage = increased_damage# Increases damage
        self.minimum=200     #These 2 variables are the maximum and minimum x coordinates the boss can walk around in
        self.maximum=700
        self.standing=False
        self.isjumping=False
        
    def health_bar(self): #This method overrides the method from character since the health bar is at the middle of the screen and appears much larger.
        Text(self.name,self.healthbar_x+250,self.healthbar_y-45,40)
        Text(str(self.health-self.damage_taken)+"/"+str(self.health),self.Horizontal+35,self.Vertical-30,25)
        pygame.draw.rect(screen,Colours["Green"],(self.healthbar_x,self.healthbar_y,self.health_bar_length,self.health_bar_height))    
       
        
    def regenerate(self,lower,upper): # This method keeps regenerating chances for events to happen
       new_move=random.randint(lower,upper)
       return new_move
 
 
    def armour(self,reduced_damage): # Allows the boss to have armour
        return reduced_damage
    
    def jump_phase(self):
        jump=self.regenerate(0,100)
        if jump<=20: # 20% Chance for the boss to jump even though this method is being called constantly, so this has very little effect.
            if (self.health-self.damage_taken)<=self.jump_decision:
                self.isjumping=True
                if self.Horizontal+20>self.maximum:
                    Jump(self,1,-30)  # This decides when the boss can jump and not jump outside of the boss area.
                elif self.Horizontal-20 <self.minimum:
                    Jump(self,1,30)
                    

    def increase_damage_phase(self): # This increases the boss damage to the player.
        if (self.health - self.damage_taken) <=100:
            self.enemy_damage= self.increased_damage
        
    def help_player(self): # This method is called to help the player to defeat the boss when it's not jumping, The player will constantly gain health and ammo.
        if not(self.isjumping):
            health_drop = copy.copy(healthpack)
            ammo_drop = copy.copy(bullets)
            chance_to_help = self.regenerate(0,100)
            if chance_to_help <=2:
                chance_to_drop=self.regenerate(0,10)
                if chance_to_drop<=5:
                    health_drop.heal()
                else:
                    ammo_drop.add_ammo()
        
        
    def move(self,player): # This allows the boss to move
        self.path=self.regenerate(self.minimum,self.maximum)
        if self.Horizontal-30>self.path and self.standing==False:   
            self.Horizontal-=self.speed   
            self.animation(self.walkanimation)
            player.player_damage=self.armour(1)

        elif self.Horizontal+30<self.path and self.standing==False:
            self.animation(self.walkanimation)   
            self.Horizontal+=self.speed
            player.player_damage=self.armour(1) # The boss has armour when it's moving.
            
        else:
            self.standing=True
            self.staying_time-= 1
            player.player_damage=5
            self.attack(player)
    
            if self.staying_time<=0:
               self.standing=False
               
               self.staying_time=100

    def death(self):
        if self.death_time>0:
            screen.blit(self.bossdeathleft,(self.Horizontal,self.Vertical+40))
            self.death_time-=1 # This shows the boss dying
            
    def execute(self,player): # Executes the boss.
        if not Pause.paused:
            if self.alive:
                self.move(player)
                self.health_bar()
                self.jump_phase()
                self.help_player()
                self.increase_damage_phase()
                player.check_if_hit(self,self.healthbar_x,self.healthbar_y)
                if player.Horizontal==self.Horizontal+40 or player.Horizontal==self.Horizontal-10:
                    player.health-=2
                    
            else:    
                self.death()
            
            object_movement(self,player.speed)

        
def clone(obj,obj_list,obj_places): # Allows an object to be cloned given X coordinates.
    for X in obj_places:
        duplicates=copy.copy(obj)   
        duplicates.Horizontal=X 
        obj_list.append(duplicates)
        
def Text(words,x,y,size):    # This creates text on the screen.
    font = pygame.font.SysFont("comicans",size,True)    
    text=font.render(str(words),1,Colours["Black"])    
    screen.blit(text,[x,y])  

def object_movement(obj,speed): # This function moves all the objects towards the player. This makes it look like the player is actually moving.
    if not Pause.paused:
        if keys[player.keybindings["left"]] or keys[pygame.K_LEFT]:
                obj.Horizontal+=speed    

        elif keys[player.keybindings["right"]] or keys[pygame.K_RIGHT]:
                obj.Horizontal-=speed    
    
def Jump(obj,height,leap):  # Allow characters to jump
    if obj.JumpSpeed>=-10:    
                neg=height    
                if obj.JumpSpeed<0:    
                    neg=-height  
                
                obj.Vertical -= (obj.JumpSpeed **2 * 0.5 * neg)
                obj.JumpSpeed-=2
                obj.Horizontal+=leap  
                
    else:  
        obj.Jumped=False    
        obj.JumpSpeed=10          

   
            
class Bullets():# Bullet class 
    def __init__(self,Horizontal,Vertical,num,colour,radius,facing):    
        self.Horizontal = Horizontal-15    
        self.Vertical = Vertical+27    
        self.radius=radius     # Attributes for bullets
        self.colour=colour    
        self.facing=facing    
        self.num=num    
        self.Shootspeed=self.num* facing  
      
      
    def create(self):# draws bullets
        pygame.draw.circle(screen,self.colour,(self.Horizontal,self.Vertical),self.radius)  
              
    def shoot(bullet_list):  # Shoot bullets
        for projectile in bullet_list:    
            if projectile.Horizontal <Windowx and projectile.Horizontal >0:    
                    projectile.Horizontal+=projectile.Shootspeed
                    projectile.create()    
                   
            else:     
                bullet_list.pop(bullet_list.index(projectile))  

    
    def fix_bullets(char): # Fixes bullets
        if char.bulletloop>0:    
            char.bulletloop+=1    
        if char.bulletloop>3:    
            char.bulletloop=0
            
class User(Character): # Class to make the player, it inherits from character
    backgroundx=0
    def __init__(self,Horizontal,Vertical,health,speed,player_damage,ammo_capacity,magazine,walkleft,walkright,attackanimationleft,attackanimationright):    
        super().__init__(Vertical,health,speed,attackanimationleft,attackanimationright)
        self.Horizontal=Horizontal
        self.Jumped=False    
        self.JumpSpeed=10     
        self.health_height=15   
        self.player_damage=player_damage    
        self.walkleft=walkleft   
        self.walkright=walkright    # Attributes for the player
        self.projectiles=[]    
        self.ammo_capacity=ammo_capacity    
        self.magazine=magazine    
        self.reload_time=40    
        self.bulletloop=0
        self.death_time=20
        self.keybindings={"left":pygame.K_a,"right":pygame.K_d ,"jump":pygame.K_w,"shoot":pygame.K_SPACE,"pause":pygame.K_ESCAPE}# Dictionary for the keys.
        
    def check_if_hit(self,enemy,x,y):   # Check if bullets collide with the enemy
        damage_scale_factor=enemy.health/enemy.health_bar_length #Instead of increasing the length of the enemy's healthbar when the enemy has a lot of health, just decrease the player's damage to scale with the health
          
        for projectile in self.projectiles:  
                if projectile.Vertical>enemy.Vertical and projectile.Vertical<enemy.Vertical+100 :
                    if projectile.Horizontal> enemy.Horizontal and projectile.Horizontal<enemy.Horizontal+100:    
                        if enemy.damage_taken < enemy.health-5:    
                            enemy.damage_taken += self.player_damage    
                            screen.blit(damage,(enemy.Horizontal-2,enemy.Vertical))                       
                            enemy.damaged=True
                            self.projectiles.pop(self.projectiles.index(projectile))                                      
                        else:  
                            screen.blit(damage,(enemy.Horizontal-2,enemy.Vertical))   
                            enemy.alive=False    
              
                      
        if enemy.damaged:      
            pygame.draw.rect(screen,Colours["Red"],(x,y,enemy.damage_taken/damage_scale_factor,enemy.health_bar_height))                   
          
    def controls(self):  #This allows the user to control the player.
        if keys[self.keybindings["left"]] or keys[pygame.K_LEFT]:    
            self.backgroundx+=self.speed    
            self.Faceright = False    
            self.Faceleft=True
            self.animation(self.walkleft)   
                      
        elif keys[self.keybindings["right"]] or keys[pygame.K_RIGHT]:    
            self.backgroundx-=self.speed    
            self.Faceright = True    
            self.Faceleft=False
            self.animation(self.walkright)
            
        else:
            screen.blit(character,(self.Horizontal,self.Vertical))

       
        if keys[self.keybindings["shoot"]] and self.bulletloop==0:  # Allows the player to fire bullets. This is similar to the shooter class.
            if len(self.projectiles)<self.ammo_capacity:    
                if self.Faceleft:      
                    facing=-1    
                    self.projectiles.append(Bullets(round(self.Horizontal+75),round(self.Vertical+35 ),20,Colours["Blue"],4,facing))    
                    self.animation(self.attackanimationleft)    
                    self.ammo_capacity-=1    
                  
                elif self.Faceright:      
                    facing=1    
                    self.projectiles.append(Bullets(round(self.Horizontal+80),round(self.Vertical+35),20,Colours["Blue"],4,facing))    
                    self.animation(self.attackanimationright)    
                    self.ammo_capacity-=1
                   

            
            self.bulletloop+=1  
        
        Bullets.shoot(self.projectiles)  
        Bullets.fix_bullets(self)
        
        if self.ammo_capacity<=0 and self.magazine>0:  
              
            if self.reload_time>0:    
                self.reload_time-=1    
                Text("Reloading...",100,70,30)    
                  
            else:    
                self.ammo_capacity=12    
                self.magazine-=4
                self.reload_time+=40  

       
        if not(self.Jumped):    # Mechanic to allow the player to jump
            if keys[self.keybindings["jump"]] or keys[pygame.K_UP]:    
                self.Jumped=True    
                self.Faceright=False    
          
        else:    
            Jump(self,1,0)  

    def death(self): #Method to show up death screen and end the program.
        global execute
        pygame.draw.rect(screen,Colours["Light Grey"],(200,50,600,600),0)
        Text("You Died",380,300,60) 
        Pause.Paused=True
        self.speed=0
        if self.death_time>0:
            self.death_time-=1
            
        else:
            execute=False
     
            
    def health_bar(self): # Another overriden healthbar method because the healthbar appears at the top left hand corner and the healthbar loses health the opposite way from other characters.
        pygame.draw.rect(screen,Colours["Red"],(15,40,200,self.health_height))
        pygame.draw.rect(screen,Colours["Green"],(15,40,self.health,self.health_height))
        Text(str(self.health)+"/"+str(200),130,20,25)
    
       
    def GUI(self): # Creates the GUI on the screen.    
        Text("Health",60,20,25)    
        screen.blit(charshootright[0],(-45,-22))
        health_on_screen = pygame.image.load("healthitem.png")
        screen.blit(health_on_screen,(210,5))
        bullet_on_screen = pygame.image.load("bullet.png")
        screen.blit(bullet_on_screen,(710,15))
        Text("Ammo:"+ str(self.ammo_capacity)+"/"+str(self.magazine),800,30,40)
        
    def execute(self,Windowx): # Executes the player
        if not Pause.paused:
            self.controls()
            self.health_bar()
            self.GUI()
 
          
class Platform():    #Class for platform designs
    def __init__(self,Horizontal,Vertical,Length,Height,colour):    
        self.Horizontal=Horizontal    
        self.Vertical=Vertical    
        self.Height=Height    
        self.Length=Length
        self.colour=colour


            
    
    def make(self):    #Draws the platform
        pygame.draw.rect(screen,(self.colour),(self.Horizontal,self.Vertical,self.Length,self.Height))    
        object_movement(self,player.speed)

       

   

        
class Item(): #Item class that make items
    def __init__(self,Vertical,item_image):    
        self.Horizontal=None
        self.Vertical=Vertical  
        self.collected=False    
        self.item_image=item_image
        
    def make(self):    
        screen.blit(self.item_image,(self.Horizontal,self.Vertical))    
        object_movement(self,player.speed)   # Draws the image.
        
    def execute(self): #Executes the item
        if self.collected==False:    
            self.make()    
            self.collect()    
              
class Wall(Platform):# Wall class that makes walls
    def __init__(self,Horizontal,Vertical,Length,Height,colour):
        super().__init__(Horizontal,Vertical,Length,Height,colour)  
   
        
    def collision(self,ground,Items,characters,colliding_object,speed):#If the player collides with the wall,everything is moving the opposite way with the same player speed to stop player from moving.   
        if keys[pygame.K_a]:
            if self.Horizontal==colliding_object+100:
                player.backgroundx-=speed
                self.collision_movement(ground,Items,characters,-speed)
               
        elif keys[pygame.K_d]:
             if self.Horizontal==colliding_object+100:
                player.backgroundx+=speed
                self.collision_movement(ground,Items,characters,speed)
       
    def collision_movement(self,ground,Items,characters,speed):
        object_movement(self,-player.speed)
  
        for i in ground:   
            i.Horizontal+=speed    
        for n in Items:   
            n.Horizontal+=speed   
        for c in characters:
            c.Horizontal+=speed
            
   
    
     
                
class Ammo(Item): # Ammo class
    def __init__(self,Vertical,item_image,extra_ammo):
        super(). __init__(Vertical,item_image)
        self.extra_ammo=extra_ammo

    def collect(self):# Gives the player more ammo when collected
        if player.Horizontal==self.Horizontal:
              self.add_ammo()
              self.collected=True
               
    def add_ammo(self):
         player.magazine+=self.extra_ammo
      
    
class Health_Item(Item):#Health class
    def __init__(self,Vertical,item_image,heal_points):    
        super().__init__(Vertical,item_image)    
        self.heal_points=heal_points    
        
    def collect(self): # Gives the player more health when collected
        if player.Horizontal==self.Horizontal:    
           self.heal()
           self.collected=True

    def heal(self): #Heals the player
        max_player_health=200
        if player.health<max_player_health:    
            if player.health+self.heal_points>=max_player_health:    
                player.health=max_player_health   
            else:
                player.health+=self.heal_points    

        
class Map(): # This puts all the objects together
    def __init__(self,player,level,platform,char_list,items,Walls,boss,background_colour,boss_wall):    
        self.level=level
        self.platform=platform
        self.char_list=char_list
        self.items=items#  <-- positive/left     --> negative/right    
        self.Walls=Walls
        self.boss=boss
        self.background_colour = background_colour
        self.boss_wall=boss_wall
        self.done=False
        
    def execute(self,Windowx):
        screen.fill((self.background_colour))
    
        boss_zone=(Windowx*(len(self.level)-1) - Windowx /2)
       
        for placecount in range(len(self.level)):    
            screen.blit(self.level[placecount],((Windowx*placecount)+player.backgroundx,0))   
              
        for floor in self.platform:    
            floor.make()
         
        for char in self.char_list:   
            char.execute(player)
            char.running=True            #Iterates through all the arrays of objects and executes them

            if char.alive==False:
                 self.char_list.remove(char)
        
        
        for Wall in self.Walls:   
            Wall.make()   
            Wall.collision(self.platform,self.items,self.char_list,player.Horizontal,player.speed)
                      
        for item in self.items:    
            item.execute()
            
        if len(self.char_list)==0:
            if player.backgroundx<=-boss_zone and not Pause.paused:  #Checks if all the enemies are defeated. If so, the boss then executes.
                self.boss.execute(player)
                if player.backgroundx>=-boss_zone:
                    player.backgroundx-=player.speed
                    for floor in self.platform:
                        floor.Horizontal-=player.speed

                    
        
                elif player.backgroundx<=-boss_zone-Windowx:
                    player.backgroundx+=player.speed
                    for floor in self.platform:
                        floor.Horizontal+=player.speed
                 
                    
        else:       
            self.boss_wall.make() # wall to stop the player from approaching the boss stage.
            self.boss_wall.collision(self.platform,self.items,self.char_list,player.Horizontal,player.speed)

        if self.boss.alive==False:
            self.done=True # If the player completes the level,It displays this message and the next level is unlocked.
            Pause.win_screen("Well done! You beat the level. Next level is now unlocked",210,100,27)
         
        if keys[player.keybindings["pause"]]: # Pauses the game
            Pause.paused=True
          
      
                
        if Pause.paused:
            Pause.show_menu("",370,150,35) # Shows this menu if paused.
            
        
        if player.health>0: # Continue to run the game if the player is alive
            player.execute(Windowx)
            
        else:
            player.alive=False
            
          
        if player.alive==False:
            player.death()

        
            

class Button(): # Button class to make buttons
    def __init__(self,Horizontal,Vertical,width,height,colour,text=""):
        self.Horizontal=Horizontal
        self.Vertical=Vertical
        self.width=width
        self.height=height  # Button attributes
        self.colour=colour
        self.text=text
        self.action=None
        self.pressed=False

    def create(self,outline=None):# Creates button with text.
        if outline:
            pygame.draw.rect(screen,outline,(self.Horizontal,self.Vertical,self.width,self.height),0)

        pygame.draw.rect(screen,self.colour,(self.Horizontal,self.Vertical,self.width,self.height),0)
            
        if self.text != "":
            font = pygame.font.SysFont("comicans",30)
            text=font.render(self.text,1,(Colours["Black"]))

            screen.blit(text,(self.Horizontal +(self.width/2 - text.get_width()/2),self.Vertical + (self.height/2 - text.get_height()/2)))


    def is_hovering(self,position): # Checks to see if the mouse is hovering over the button
        if  not (self.pressed):
            if position[0] > self.Horizontal and position[0]< self.Horizontal + self.width:
                if position[1]> self.Vertical and position[1]< self.Vertical + self.height:
                    return True

            return False


    def execute(self): # Executes the button
        if self.pressed==False:
            self.create(Colours["Black"])  
              
            if event.type==pygame.MOUSEMOTION:
               if self.is_hovering(position):
                    self.colour=(Colours["Red"])
            
               else:
                    self.colour=(Colours["Green"])


class Menu(): # Menu class
    def __init__(self):
        self.menu_on=True
        self.accounts_page_on=False
        self.logged_in=False
        self.action="" 
        self.counter=0
        self.login_text=None
    
        
    def new_game(self):
        Level_1.done=False
        Level_2.done=False
        Level_3.done=False
        
    def play(self,Windowx): # Plays the game
        if self.action=="1":
            Level_1.execute(Windowx)
     
        elif self.action=="2":
            Level_2.execute(Windowx)

        elif self.action=="3":
            Level_3.execute(Windowx)
            
    def set_background_colour(self):# Sets background colour
        screen.fill(Colours["Light Grey"])
        
    def howtoplay(self):# How to play screen.
        self.set_background_colour()
        Text("Use asdw or arrow keys to move(You can change these keys in the settings page).",15,100,28)
        Text("Press space to shoot. Complete all levels to win.",15,150,28)
        Text("Each level Enemies include melee hitters,shooters and bosses. Kill all the enemies",15,200,28)
        Text("to unlock the boss area in the final stage of the level.",15,250,28)
        Text("Collect items to help you with the levels.",15,300,28)
        self.Return()
        
    def Return(self):# Return to the menu screen.
        self.display(back,"back")

        if self.action=="back":
            self.menu_on=True

    def settings(self): # Settings page
        self.set_background_colour()
        Text("Press a key to change the controls",200,200,40)
        Text("Press a key for moving left",320,300,30)
        Text("Press a key for moving right",320,450,30)
        Text("Press a key for jumping",350,590,30)
        Text("Press a key for shooting",350,720,30)
        self.display(reset_keys,"reset")
        
        self.Return()
        for box in text_boxes:
            box.execute()
            if click[0]==1 and box.is_hovering(position):
                if box.name=="left":
                    key_left.active=True
                    key_right.active=False
                    key_jump.active=False
                    key_shoot.active=False
            
                elif box.name=="right":
                    key_left.active=False
                    key_right.active=True
                    key_jump.active=False
                    key_shoot.active=False
                    
            
                elif box.name=="jump":
                    key_left.active=False
                    key_right.active=False
                    key_jump.active=True
                    key_shoot.active=False
                    
                elif box.name=="shoot":
                    key_left.active=False
                    key_right.active=False
                    key_jump.active=False
                    key_shoot.active=True
                    
            keychange(key_left,"left",player) # Allows the player to change the keys
            keychange(key_right,"right",player)
            keychange(key_shoot,"shoot",player)
            keychange(key_jump,"jump",player)

        if self.action=="reset": # Resets the buttons
            player.keybindings["left"]=pygame.K_a
            player.keybindings["right"]=pygame.K_d
            player.keybindings["jump"]=pygame.K_w
            player.keybindings["shoot"]=pygame.K_SPACE
            
            self.menu_on=True

        if self.menu_on:
            key_left.active=False
            key_right.active=False
            key_jump.active=False
            key_shoot.active=False
            
    def display(self,button,Action):# Displays and checks if the player clicks on the button.
        if click[0]==1 and button.is_hovering(position):
            self.action=Action
            self.menu_on=False
            
        else:
            button.execute()
                 
    def linear_search(self,login_text):   #Linear search to find account
        counter=0
        cursor.execute("""SELECT Username,Password,Email,Level FROM players""") # SQL statement to fetch data
        for row in cursor.fetchall():
             if (login_text==row[counter] or login_text==row[counter+2]) and cipher(loginpass.real_pass,50)==row[counter+1]:
                self.login_text=row[counter]    
        
                if row[3]=="2":
                    Level_1.done=True
					   #Fetches accounts’ current levels

                if row[3]=="3":
                    Level_1.done=True
                    Level_2.done=True

                return True
            
                if (login_text!=row[counter] or login_text!=row[counter+2]) and loginpass.real_pass!=row[counter+1]:
                    counter+=1
                    
                
                print("account index:",counter)

    def Login(self):
        self.accounts_page_on=True
        self.set_background_colour()
        self.Return()
        Text("Username or email",400,420,30) # Messages on the screen
        Text("Password",400,520,30)
        self.display(loginenter,"enter")
        
        for box in account_boxes["login"]:
            box.execute()
            if click[0]==1 and box.is_hovering(position):
                if box.name=="username":
                    loginuser.active=True
                    loginpass.active=False
                    
                elif box.name=="password":
                    loginuser.active=False
                    loginpass.active=True
      
        if self.action=="enter":
              if not self.logged_in:# Checks if user hasn't logged into an account already
                if len(loginuser.text)>0 and len(loginpass.text)>0:
                    if self.linear_search(loginuser.text) and self.login_text!=None:
                         print("Account logged in")
                         self.menu_on=True
                         self.logged_in=True
                         
                    else:
                        print("Account doesn't exist") # Error message if account doesn't exist
                        self.menu_on=True
        
                else:
                    print("Invalid login details, please try again")
                    self.menu_on=True
              else:              
                print("Please log out first")
                self.menu_on=True
                   
                        
        if self.menu_on:
           loginuser.active=False
           loginpass.active=False
         
    def reset_game(self):# Resets the game for each level. This might not be the most efficient way to do it but it gets the job done.
        if Level_1.done or Level_2.done or Level_3.done:
            player.backgroundx=0
            player.health=200
            player.ammo_capacity=12
            player.damage=5
            player.magazine=32
            wall.Horizontal=-30
            level_1_boss_wall.Horizontal=(Windowx * (len(area1) -1))
            level_2_boss_wall.Horizontal=(Windowx * (len(area2) -1))
            level_3_boss_wall.Horizontal=(Windowx * (len(area3) -1))
            metal_ground.Horizontal=0 
            black_ground.Horizontal=2000
            grass.Horizontal=-10
            green_wall.Horizontal=-40
            stone.Horizontal=0
            

    def register(self): # Allows the player to register
        self.set_background_colour()
        self.accounts_page_on=True
        
        self.Return()
        Text("Email",400,320,30)
        Text("Username",400,420,30) # Messages on the screen
        Text("Password",400,520,30)
        self.display(enter,"Enter")

        for box in account_boxes["register"]:
            box.execute() # runs the object
            if click[0]==1 and box.is_hovering(position):
                if box.name=="Email":
                    email.active=True
                    username.active=False
                    password.active=False
                    
                elif box.name=="username":
                    username.active=True
                    email.active=False
                    password.active=False
                    
                elif box.name=="password":
                    password.active=True
                    email.active=False
                    username.active=False
        
        if self.action=="Enter":
           if len(email.text)>0 and len(username.text)>0 and len(password.text)>0:
               if self.search():
                    print("Account with username already exists.")
                    self.menu_on=True
                    
               else:
                   add(username.text,email.text,cipher(password.real_pass,50),"1")
                   self.new_game()
                   self.logged_in=True
                   self.menu_on=True
                   self.login_text=username.text

           else:
               print("Invalid details, please try again.")
               self.menu_on=True
               
            
        if self.menu_on:
            email.active=False
            username.active=False
            password.active=False
          
          
       
    def execute(self,Windowx): # Executes the menu screen
        global execute
        self.set_background_colour()
        if self.menu_on:
            if self.logged_in:
                Text(self.login_text,35,20,40)
                self.display(logout,"logout")
                
            else:
                Text("Create an account or login to save your progress.",200,100,30)
                
            Text("TechShot",35,200,250)
            self.display(playbutton,"play")
            self.display(settings,"Settings")
            self.display(howtoplay,"howtoplay")
            self.display(Quit,"quit")
            self.display(Account,"account")
            self.display(login,"login")
            self.reset_game()
            player.Faceright=True
          
        else:
            if self.action=="play":
                self.Return()
                self.display(level1,"1")

               
                if Level_1.done:
                    cursor.execute(""" UPDATE players SET Level=="2" WHERE Level=="1" AND Username==(?) """,(username.text,)) #Updates current level
                    table.commit()
                        
                    self.display(level2,"2")

                if Level_2.done:
                  
                    cursor.execute(""" UPDATE players SET Level=="3" WHERE Level=="2" AND Username==(?) """,(username.text,)) #Updates current level
                    table.commit()
                       
                    self.display(level3,"3")

                if Level_3.done:
                    self.menu_on=True

            elif self.action=="account":
                self.register()
                
            elif self.action=="quit":
                execute=False
          
            elif self.action =="Settings":
                self.settings()
                
            elif self.action=="howtoplay":
                self.howtoplay()
           
            elif self.action=="login":
                self.Login()

            elif self.action=="logout":
                    self.logged_in=False
                    self.menu_on=True
                    self.new_game()
                    
            self.play(Windowx)
            


class Pause_menu(Menu): # Class for the pause menu
    def __init__(self):
        super().__init__()
        self.paused=False
        

    def win_screen(self,text,x,y,size):
        pygame.draw.rect(screen,Colours["Light Grey"],(200,50,600,600),0)
        Text(text,x,y,size)
        self.display(menubutton,"Return to menu")
        if self.action=="Return to menu":
           menu.menu_on=True
           self.action=""
        
         
    def show_menu(self,text,x,y,size):# Shows the ingame menu screen
        if self.paused:
            pygame.draw.rect(screen,Colours["Light Grey"],(200,50,600,600),0)
            self.display(Continue,"continue")
                
            Text(text,x,y,size)
            self.display(menubutton,"Return to menu")
            self.display(midgamesettings,"settings")
            if self.action=="settings":
                self.settings()
                
            elif self.action=="Return to menu":
               menu.menu_on=True
               self.action=""
               
            elif self.action=="continue":
                self.paused=False
                self.action=""
                
               
               
class Input(Button): # Class for the inputs
    def __init__(self,name,Horizontal,Vertical,width,height,colour=Colours["Light Grey"],text=""):
        super().__init__(Horizontal,Vertical,width,height,colour,text="")
        self.active=False
        self.image = pygame.Surface((width,height))
        self.name=name
        self.real_pass=""
        
    def add_text(self,key): # Allows the player to type in a character.
        words = list(self.text)
        asterisk=list(self.text)
        Pass=list(self.real_pass)
        if chr(key).isalpha() or chr(key).isdigit() and self.active:
            words.append(chr(key))
            if menu.accounts_page_on:
                self.text= "".join(words)
                if password.active or loginpass.active:
                    asterisk.append("*")
                    self.text= "".join(asterisk)
                    Pass.append(chr(key))
                    self.real_pass="".join(Pass)

            else:
                self.text= "".join(words)[0] # This is for the settings page
        
        elif key==8:
            words = list(self.text)
            Pass=list(self.real_pass)
            if len(words)>0:
                words.pop()
                self.text = "".join(words)
            if len(Pass)>0:
                Pass.pop()
                self.real_pass="".join(Pass)
                
# character objects
player = User(430,705,200,10,5,12,32,walkleft,walkright,charshootleft,charshootright)  
Robot=Enemy(680,50,7,1,enemywalk,enemyattackleft,enemyattackright,50,25)  
shooter=Shooter(685,75,8,2,shooterwalk,shootershootleft,shootershootright,300,40,20,Colours["Black"])
Redguy = Enemy(680,75,7,1,redwalking,redattackingleft,redattackingright,140,25)
Flyer = Shooter(665,50,4,5,flyerwalking,flyerattackingleft,flyerattackingright,400,30,20,Colours["Yellow"])
Trevor = Boss(685,400,5,5,bosswalk,bossfireleft,bossfireright,bossdeathleft,300,70,20,Colours["Light Grey"],"Trevor",200,8)
Steve = Boss(670,500,5,7,stevewalk,steveattackleft,steveattackright,stevedeathleft,500,70,30,Colours["Green"],"Steve",180,10)
Signus = Boss(680,800,5,10,signuswalk,signusattackleft,signusattackright,signusdeathleft,0,70,20,Colours["Red"],"Signus",150,12)

#Item objects
healthpack=Health_Item(705,pygame.image.load("healthitem.png"),50)
bullets = Ammo(705,pygame.image.load("bullet.png"),4)

#platforms

metal_ground = Platform(0,805,2000,40,Colours["Grey"])   
black_ground = Platform(2000,805,Windowx,40,Colours["Black"])   


wall = Wall(-40,10,30,800,Colours["Grey"])

#Level 1 #############################################################################################
platform=[metal_ground,black_ground]
area1=[pygame.image.load("training.png"),pygame.image.load("training2.png"),pygame.image.load("training3.png"),pygame.image.load("stage1boss.png")]    
level1={"chars":[],"items":[],"platforms":[metal_ground,black_ground],"area":area1,"walls":[wall]}

level_1_boss_wall=Wall(Windowx * (len(area1) -1),10,10,1000,Colours["Red"])
clone(shooter,level1["chars"],[2000,2500,2700,2300])   
clone(Robot,level1["chars"],[1000,1700,2500,2200,1400])
clone(bullets,level1["items"],[1700,2800])
clone(healthpack,level1["items"],[2000,3000])

#Level 2 #############################################################################################
area2=[pygame.image.load("level2area1.png"),pygame.image.load("level2area2.png"),pygame.image.load("level2area3.png"),pygame.image.load("level2area4.png")]
grass = Platform(0,805,Windowx*len(area2)+1000,1000,Colours["Green"])
green_wall =copy.copy(wall)
green_wall.colour=Colours["Green"]
level2={"chars":[],"items":[],"platforms":[grass],"area":area2,"walls":[green_wall]}
level_2_boss_wall=Wall(Windowx * (len(area2) -1),10,10,1000,Colours["Red"])

clone(Robot,level2["chars"],[1500,2000,2500])
clone(Redguy,level2["chars"],[2400,2600])
clone(shooter,level2["chars"],[1000,2200,1800])
clone(healthpack,level2["items"],[2500,1500,2000])
clone(bullets,level2["items"],[1000,2800,2300,1200])

#Level 3#################################################################################################
area3=[pygame.image.load("level3area1.png"),pygame.image.load("level3area2.png"),pygame.image.load("level3area3.png"),pygame.image.load("level3area4.png"),pygame.image.load("level3area5.png")]
level_3_boss_wall=Wall(Windowx * (len(area3) -1),10,10,1000,Colours["Red"])
stone=copy.copy(metal_ground)
stone.Length=(Windowx * len(area3)-1)+1000
level3={"chars":[],"items":[],"platforms":[stone],"area":area3,"walls":[wall]}
clone(Robot,level3["chars"],[2000,2500,3500])
clone(shooter,level3["chars"],[1000,2200,3000,3500])
clone(Flyer,level3["chars"],[2200,2670,4000])
clone(healthpack,level3["items"],[2000,1100,2300,3600,3600])
clone(bullets,level3["items"],[3500,3000,2700,1200,3700])

#Buttons##########################################################################
playbutton= Button(400,400,200,50,(Colours["Green"]),"Play")
settings= Button(400,800,200,50,(Colours["Green"]),"Settings")
Quit= Button(400,900,200,50,(Colours["Green"]),"Quit")
howtoplay = Button (400,700,200,50,(Colours["Green"]),"How to play")
Account = Button(400,600,200,50,(Colours["Green"]),"Register")
menubutton = Button(400,400,200,50,(Colours["Green"]),"Return to menu")
Continue = Button(400,200,200,50,(Colours["Green"]),"Continue")
midgamesettings=Button(400,300,200,50,(Colours["Green"]),"Settings")
enter=Button(400,650,200,50,(Colours["Green"]),"Enter")
controls = Button(400,300,200,50,(Colours["Green"]),"Controls")
back = Button (100,800,200,50,(Colours["Green"]),"Return to menu")
login=Button(400,500,200,50,(Colours["Green"]),"Login")
logout=Button(700,15,200,50,(Colours["Green"]),"Logout")
    
#### 3 levels
Level_1 = Map(player,level1["area"],level1["platforms"],level1["chars"],level1["items"],level1["walls"],Trevor,Colours["Grey"],level_1_boss_wall)
Level_2 = Map(player,level2["area"],level2["platforms"],level2["chars"],level2["items"],level2["walls"],Steve,Colours["Green"],level_2_boss_wall)                
Level_3 = Map(player,level3["area"],level3["platforms"],level3["chars"],level3["items"],level3["walls"],Signus,Colours["Grey"],level_3_boss_wall)
####

level1=Button(400,150,200,50,(Colours["Green"]),"Level 1")
level2=Button(400,250,200,50,(Colours["Green"]),"Level 2")
level3=Button(400,350,200,50,(Colours["Green"]),"Level 3")

key_left = Input("left",400,350,200,50)
key_right= Input("right",400,500,200,50)
key_jump = Input("jump",400,620,200,50)
key_shoot = Input("shoot",400,750,200,50)

email=Input("Email",400,350,200,50)
username=Input("username",400,450,200,50)
password =Input("password",400,550,200,50)

loginuser=copy.copy(username)
loginpass=copy.copy(password)
loginenter=copy.copy(enter)

account_boxes ={"register":[email,username,password],"login":[loginuser,loginpass]}
text_boxes =[key_left,key_right,key_jump,key_shoot]


reset_keys= Button(750,800,200,50,(Colours["Green"]),"Original keys")


menu=Menu()
Pause = Pause_menu()

execute = True

while execute:# This is the main loop that runs the entire program.
    for event in pygame.event.get():
        position = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
             execute=False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            for box in text_boxes:
                box.is_hovering(pygame.mouse.get_pos())
                
            for box in account_boxes["register"]:
                box.is_hovering(pygame.mouse.get_pos())
                
            for box in account_boxes["login"]:
                box.is_hovering(pygame.mouse.get_pos())
                
        if event.type ==pygame.KEYDOWN:
            for box in text_boxes:
                if box.active:
                    box.add_text(event.key)
                    
            for box in account_boxes["register"]:
                if box.active:
                    box.add_text(event.key)
                    
            for box in account_boxes["login"]:
                if box.active:
                    box.add_text(event.key)
                    
    keys = pygame.key.get_pressed()
    click = pygame.mouse.get_pressed()
   
    menu.execute(Windowx)# Runs menu

    pygame.display.update()

pygame.quit()    
               


