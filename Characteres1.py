import pygame
from support import import_folder
from settings import *

class Walls(pygame.sprite.Sprite):
    def __init__(self,pos,groups,sprite_type,surface= pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groups)
        self.sprite_type=sprite_type
        self.image=surface
        self.rect= self.image.get_rect(topleft=pos)
        if sprite_type=="object":
            self.rect=self.image.get_rect(topleft=(pos[0],pos[1]-TILESIZE))
            self.hitbox= self.rect.inflate(-10,-50)
        elif sprite_type=="grass": 
            self.hitbox= self.rect.inflate(-10,-10)
        elif sprite_type=="boundary": 
            self.hitbox= self.rect.inflate(-30,50)
        else: 
            self.hitbox= self.rect.inflate(-10,0)


class Hero(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacles,create_attack):
        super().__init__(groups)
        self.image=pygame.transform.scale((pygame.image.load("./grafics/pj/0.png").convert_alpha()),(64,64))
        self.rect= self.image.get_rect(topleft=pos)
        self.hitbox=self.rect.inflate(-40,-60)
        self.obstacles=obstacles
        
        #grafics set up
        self.import_assets()
        self.status="down"

        #movement
        self.VEL=5
        self.direction= pygame.math.Vector2()
        self.attack_cooldown=400
        self.attacking=False
        self.attack_time=None
        self.frame_index=0
        self.animation_speed=0.15
        self.create_attack=create_attack
        
    def import_assets(self):
        character_path= "./grafics/player/"
        self.animations= {"down":[],"down_attack":[],"down_idle":[],"left":[],"left_attack":[],
        "left_idle":[],"right":[],"right_attack":[],"right_idle":[],"up":[],"up_attack":[],"up_idle":[]}
        for animation in self.animations.keys():
            full_path=character_path+animation
            self.animations[animation]=import_folder(full_path)
            

    def get_status(self):
        if self.direction.x==0 and self.direction.y==0:
            if not "idle" in self.status and not "attack" in self.status:
                self.status=self.status+"_idle"
        if self.attacking:
            self.direction.x=0
            self.direction.y=0
            if not "attack" in self.status:
                if "idle" in self.status:
                    self.status=self.status.replace("_idle","_attack")
                else:    
                    self.status=self.status+"_attack"
        else:
            if "attack" in self.status:
                self.status=self.status.replace("_attack","")
    def keyboard_inputs(self):
        if not self.attacking:
            keyboard = pygame.key.get_pressed()
            # movement input
            if keyboard[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keyboard[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keyboard[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keyboard[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0 
            # atack input
            if keyboard[pygame.K_SPACE]: 
                self.attacking=True
                self.attack_time=pygame.time.get_ticks()
                # self.create_attack()
            #magic input
            if keyboard[pygame.K_e]:
                self.attack_time=pygame.time.get_ticks()
                self.attacking=True
           
    def movement(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x +=self.direction.x*speed
        self.collisions("horizontal")
        self.hitbox.y +=self.direction.y*speed
        self.collisions("vertical")
        self.rect.center=self.hitbox.center
    def collisions(self,direction):
        if direction== "horizontal":
            for sprite in self.obstacles:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x>0:# moving right
                        self.hitbox.right=sprite.hitbox.left
                    if self.direction.x<0: # moving left
                        self.hitbox.left = sprite.hitbox.right


        if direction == "vertical":
            for sprite in self.obstacles:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y>0:# moving down
                        self.hitbox.bottom=sprite.hitbox.top
                    if self.direction.y<0: # moving up
                        self.hitbox.top = sprite.hitbox.bottom
    def cooldowns(self):
        current_time=pygame.time.get_ticks()
        if self.attacking:
            if current_time-self.attack_time>=self.attack_cooldown:
                self.attacking=False
    def animate(self):
        animation=self.animations[self.status]
        #loop over the frame index
        self.frame_index+=self.animation_speed
        if self.frame_index>=len(animation):
            self.frame_index=0

        #set the image
        self.image=animation[int(self.frame_index)]
        self.rect=self.image.get_rect(center=self.hitbox.center)


    def update(self):
        self.movement(self.VEL)
        self.keyboard_inputs()
        self.cooldowns()
        self.get_status()
        self.animate()

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        direction=player.status("_")[0]
        #graphics
        self.image= pygame.Surface((40,40))

    #placement
        if direction=="right":
            self.rect=self.image.get_rect(midleft=player.rect.midright+pygame.math.Vector2(0,16))
        else:
            self.rect=self.image.get_rect(cemter=player.rect.center)
