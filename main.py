import pygame,sys
from settings import *
from Characteres1 import Hero,Walls,Weapon
from support import *
from random import choice



class Levels():
    def __init__(self):

        self.display_sur=pygame.display.get_surface()
        #sprite
        self.block_list = pygame.sprite.Group() # list of sprites for check the collisions
        self.all_sprites_list = Camera_MAN_Group()  # here go all the sprites to upload the imagens to the WINDOWS
        self.build_the_world()

    def build_the_world(self):
        layouts={
            "boundary": import_csv_layout("./grafics/map/level_0_bedrock.csv"),
            "grass"   : import_csv_layout("./grafics/map/level_0_grass.csv"),
            "objects"   : import_csv_layout("./grafics/map/level_0_objetos.csv")
        }
        grafics={
            "grass": import_folder("./grafics/grass"),
            "object": import_folder("./grafics/objects")
        }
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout): #this check the indice and give you the number of the row
                for col_index,col in enumerate(row): # this give you the colum indice and check each of the colums inside of the raw
                        if col != "-1": 
                            x= col_index* TILESIZE #this tell you the x when multiply the index for the tittle size that we choose
                            y=row_index * TILESIZE  # same with the y
                            if style == "boundary":
                                Walls((x,y+40),[self.block_list],"invisible")
                            if style == "grass":
                                random_grass = choice(grafics["grass"])
                                Walls((x,y+40),[self.all_sprites_list,self.block_list],"grass",random_grass)
                            if style == "objects":
                                surf=grafics["object"][int(col)]
                                Walls((x,y),[self.all_sprites_list,self.block_list],"object",surf)
       
        self.player = Hero((1900,2500),[self.all_sprites_list],self.block_list,self.create_attack)
    def create_attack(self):
        Weapon(self.player ,self.all_sprites_list)
    
    def main(self):
        self.all_sprites_list.update()
        self.all_sprites_list.custom_draw(self.player)
       
        
   
class Camera_MAN_Group(pygame.sprite.Group): # ysort ordenate the sprite for the Y
    def __init__(self):
       
        super().__init__()
        self.display_sur=pygame.display.get_surface()
        self.half_width=self.display_sur.get_size()[0]//2
        self.half_height=self.display_sur.get_size()[1]//2
        self.offset=pygame.math.Vector2()

        #floor
        self.floor_surf=pygame.image.load("./grafics/walls/map.png").convert()
        self.floor_rect=self.floor_surf.get_rect(topleft=(0,70))
        
    def custom_draw(self,player):
        #getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

                #drawing the floor
        floor_offset=self.floor_rect.topleft-self.offset
        self.display_sur.blit(self.floor_surf,floor_offset)

        for sprite in sorted(self.sprites(),key=lambda sprite: sprite.rect.centery):
            offset_position=sprite.rect.topleft - self.offset
            self.display_sur.blit(sprite.image,offset_position)


class Game():
    def __init__(self):
        
        pygame.init()
        self.WINDOWS = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('NEW GAME')
        self.clock = pygame.time.Clock()
        self.level = Levels()
	
    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.WINDOWS.fill("white")
            self.level.main()
            pygame.display.update()
            self.clock.tick(FPS)    
if __name__ == '__main__':
    game = Game()
    game.main()
     
  








 





