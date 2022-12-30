''' Author: Kjærsti Løkholm Bergli, klbergli@gmail.com'''
''' 
    Contains Flagship class and Wall class.
'''


import pygame
from pygame import Vector2 
from itertools import cycle
from pygame.constants import K_LEFT, K_RIGHT, K_UP, K_SPACE

class Flagship (pygame.sprite.Sprite):
    '''
        Flagship class.

        Contains init, handleInput and update functions.

    '''
    
    def __init__(self, pos):
        '''
            Sets flagship objects variables.
 
            Two imagevariables needed to redraw ship each frame.

            Input: position.

            Returns: nothing.
        '''
        super().__init__()
        self.originalImage = pygame.image.load("flag.png").convert_alpha()
        self.image = pygame.image.load("flag.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.direction = Vector2 (0,-1)#point upwards intially
        self.velocity = Vector2 (0,0)
        self.thrust = False
        self.previousShot = pygame.time.get_ticks()
        self.score = 0
        self.bulletsGroup = pygame.sprite.Group()
 
    def handleInput(self, keys):
        '''
            Moves ship according to keys pressed.

            Input: keys pressed.

            Returns: nothing.
        '''

        if keys[K_LEFT]:
            self.direction.rotate_ip(-5)
 
        if keys[K_RIGHT]:
            self.direction.rotate_ip(5)

        if keys[K_UP]:
            self.thrust= True
        else:
            self.thrust = False

        if keys[K_SPACE]:
            if self.previousShot + 100 < pygame.time.get_ticks():
                self.previousShot = pygame.time.get_ticks()
                bulletPos = self.pos + self.direction
                self.bulletsGroup.add(Bullet(bulletPos, self.direction))
        
    def update(self, screenWidth, screenHeight): 
        ''' 
            Updates the state of the flagships position.

            Ship is bounced back when it hits a wall.

            Gravity downwards added to the ship.

            Input: screenwidth and screenheight.

            Returns: nothing.
        '''
        if (self.pos.x > screenWidth):
            self.velocity.x = -abs(self.velocity.x)
        if (self.pos.x < 0):
            self.velocity.x = abs(self.velocity.x)
        if (self.pos.y > screenHeight):
            self.velocity.y = -abs(self.velocity.y)
        if (self.pos.y < 0):
            self.velocity.y = abs(self.velocity.y)
        
        if self.thrust:
            self.velocity += self.direction * 1/4
        else:
            self.velocity *= 0.95
        
        self.pos += self.velocity
        angle = self.direction.angle_to(Vector2(0, -1))
        self.image = pygame.transform.rotate(self.originalImage, angle)

        self.rect = self.image.get_rect(center=self.pos)
        
        self.pos += Vector2(0, 1)
  
class Bullet(pygame.sprite.Sprite):
    '''
        Bullet class.

        Contains inite and update functions. 

    '''
    bulletImages = cycle(["popcorn1.png", "popcorn2.png", "popcorn3.png"])

    def __init__(self, pos, direction):
        '''
            Sets bullet objects variables.
 
            Bullets are shot from ships tip.

            Three different bullet-images used. They are shot with some space between them.

            Input: position and direction.

            Returns: nothing.
        '''
        super().__init__()
        self.pos = Vector2(pos)
        angle = direction.angle_to(Vector2(0, -1))
        imagePath = next(self.bulletImages)
        self.image = pygame.transform.rotozoom(pygame.image.load(imagePath), angle, 0.2)
        self.rect = self.image.get_rect(center=self.pos)
        self.direction = Vector2(direction)
        

    def update(self):
        '''
            Moves bullets. 

            Input: nothing.

            Returns: nothing.
        '''
        self.pos += self.direction * 5
        self.rect = self.image.get_rect(center=self.pos)


class Wall (pygame.sprite.Sprite):
    '''
        Wall class.

        Contains init function.

    '''
    def __init__(self, pos):
        '''
            Sets wall objects variables.

            Input: position.

            Returns: nothing.
        '''
        super().__init__()
        self.image = pygame.image.load("tree.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)


class Band (pygame.sprite.Sprite):
    '''
        Marching band class.

        Contains init function.


    '''
    def __init__(self, pos):
        '''
            Sets marching band objects variables.

            Input: position.

            Returns: band object.
        '''
        super().__init__()
        self.image = pygame.image.load("band.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.numberOfHits = 0
        self.bandSound = pygame.mixer.Sound('band.wav')
        self.playingSound = False

    def gotHit(self):
        '''
            Checks if band is hit and plays band music and gives points to player.
            Removes band when hit 4 times. 

            Input: nothing.

            Returns: points generated when band is hit.
        '''
        hitScore = 1
        self.numberOfHits += 1

        if not self.playingSound:
            self.bandSound.play()
            self.playingSound = True
        
        if self.numberOfHits > 5:
            hitScore = 40
            self.bandSound.stop()
            self.kill()

        return hitScore