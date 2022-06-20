import pygame
from settings import *

class Monster(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites=[] 
        self.current_sprite=0
        self.sprites.append(pygame.transform.scale(pygame.image.load("./grafics/monster/0.png").convert_alpha(),(45,45)))
        self.sprites.append(pygame.transform.scale(pygame.image.load("./grafics/monster/1.png").convert_alpha(),(45,45)))
        self.sprites.append(pygame.transform.scale(pygame.image.load("./grafics/monster/2.png").convert_alpha(),(45,45)))
        self.sprites.append(pygame.transform.scale(pygame.image.load("./grafics/monster/3.png").convert_alpha(),(45,45)))
        
        self.image= self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(center=(80,200))
        self.hitbox=self.rect.inflate(-10,-10)

       

    def update_sprite(self):
        self.current_sprite+=0.3
        if self.current_sprite>=len(self.sprites):
                self.current_sprite = 0
                # self.is_animating==False
        self.image=self.sprites[int(self.current_sprite)]
    def border_collisions(self):
        if self.rect.x <=0 : self.rect.x=0
        if self.rect.x >WIDTH-45 : self.rect.x=WIDTH-45
        if self.rect.y <=0 : self.rect.y=0
        if self.rect.y >HEIGHT-45 : self.rect.y=HEIGHT-45

  
       
    def update(self):
        self.border_collisions()
        self.update_sprite()
        
        
        
        
        
        
class Hero(pygame.sprite.Sprite):
    def __init__(self,pos,groop):
        super().__init__()
        self.is_animating=True 
        self.imagen= pygame.image.load("./grafics/monster/0.png").convert_alpha()
        self.image = pygame.transform.scale( self.imagen, (70, 70))
        self.rect = self.image.get_rect(center=pos)
        self.hitbox=self.rect.inflate(-10,-10)
        
        self.VEL=5
        self.direction = pygame.math.Vector2()
        self.atacking=False
        #Set up Grafics
        self.import_player_imagen()

    def import_player_imagen(self):
        hero_path= "./grafics/monster/"
        self.animation={"monster":[]}
        for file in self.animation.keys():
            print(file)

    def hero_keyboard_input(self):
             
        #movement
        keyboard=pygame.key.get_pressed()
        if keyboard[pygame.K_w]:
            self.direction.y =-1
            self.status="up"
        elif keyboard[pygame.K_s]:
            self.direction.y = 1  
            self.status = 'down'
        else: self.direction.y = 0 
        if keyboard[pygame.K_d]:
            self.direction.x = 1 
            self.status = 'right'
        elif keyboard[pygame.K_a]:
            self.direction.x =-1
            self.status = 'left'
        else: self.direction.x = 0 

        mouse=pygame.mouse.get_pos()
        mouse_click=pygame.mouse.get_pressed()
        

        
    def collisions(self):
             
       ##collisions with the borders
        if self.hitbox.x <=0 : self.hitbox.x=0
        if self.hitbox.x >WIDTH-45 : self.hitbox.x=WIDTH-45
        if self.hitbox.y <=0 : self.hitbox.y=0
        if self.hitbox.y >HEIGHT-45 : self.hitbox.y=HEIGHT-45 

    def coldowns(self):
        current_time=pygame.time.get_ticks()

    def update(self):
        self.hero_keyboard_input()
        self.collisions()
        self.movement(self.VEL)
    def animated(self):
        self.animated=False
     #atack
        mouse=pygame.mouse.get_pos()
        mouse_click=pygame.mouse.get_pressed()
        print(mouse_click)

        if mouse_click[pygame.BUTTON_LEFT]:
            self.atacking=True
            self.atack_time