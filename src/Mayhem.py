#!/usr/local/bin/python3
''' Author: Kjærsti Løkholm Bergli, klbergli@gmail.com'''

'''
    Contains collision detection function and game function with main loop.
'''
import pygame
from pygame import Vector2
import random
from classes import Flagship, Wall, Band

scoreSum = 0 #score for the game

#sets screen and background image   
screenWidth = 1200
screenHeight = 750
BGFileName = "sky.png"
mainScreen = pygame.display.set_mode((screenWidth, screenHeight))
backGround = pygame.transform.scale(pygame.image.load(BGFileName), (screenWidth, screenHeight))

def collisionDetection(flagship, wallsGroup, bandsGroup):
    '''
        Checks if ship collides with any of the walls it turns 180 degrees.

        Cheks if bullet hits walls or bands.

        If ship hits wall - 1 point.
        If ship hits band - 10 points.
        If bullet hits band +1 point.
        If bullet kills band + 40 points.

        Input: flagship, walls and marching bands.

        Returns: nothing.
    '''
    
    if pygame.sprite.spritecollideany(flagship, wallsGroup):
        flagship.velocity.rotate_ip(180)
        flagship.score -= 1
    
    if pygame.sprite.spritecollideany(flagship, bandsGroup):
        flagship.velocity.rotate_ip(180)
        flagship.score -= 10
    
    pygame.sprite.groupcollide(wallsGroup, flagship.bulletsGroup, False, True)

    for band in bandsGroup:
        if pygame.sprite.spritecollideany(band, flagship.bulletsGroup):
            flagship.score += band.gotHit()
            for bullet in flagship.bulletsGroup:
                bullet.kill()

                
                    
    return flagship.score



def Mayhem():
    ''' 
        Main game function.
        
        Sets game window.
        Draws background.
        Executes mainloop.

        Input: nothing.
        Returns: nothing.
    '''
    print ("Lets play 17th of Mayhem!")
    pygame.display.set_caption("17th of Mayhem!")
    pygame.init()

    
    '''
        FLAGSHIP:
        Make flagship object as sprite.
    '''
    flagshipGroup = pygame.sprite.Group()
    flagshipPos = Vector2 (screenWidth/2, screenHeight-100)
    flagship = Flagship(Vector2 (flagshipPos))
    flagshipGroup.add(flagship)

    ''' 
        WALLS:
        Make wall objects as sprites.
    '''
    treePosArray = [Vector2(50,200), Vector2(screenWidth/2, 200),\
         Vector2(screenWidth-50, 200), Vector2(300,screenHeight-200),\
             Vector2(screenWidth-300,screenHeight-200)]
    wallsGroup = pygame.sprite.Group()
    
    for pos in treePosArray:
        wall = Wall(pos)
        wallsGroup.add(wall)

    ''' 
        BULLETS:
        Bullet sprites are made in Bullet class. 
        Bullet objects are made in Flagship class under handleInput when Space key is pressed.
    '''
        
    '''
        MARCHING BAND:
        Make marching band as sprites.
        Considers random position to not be inside walls or outside window.
    '''
    
    bandsGroup = pygame.sprite.Group()

    while len(bandsGroup) < 3:
        randomPos = Vector2(random.randrange(0, screenWidth), random.randrange(0, screenHeight))
        newBand = Band(randomPos)
        if not pygame.sprite.spritecollide(newBand, wallsGroup, False):
            bandsGroup.add(newBand)
  
            

     
    while True:
        ''' 
            Main program loop.
            
            Quits game if x in upper corner is clicked.
            
            Calls flagships 'handle_input()' to control flagship.
            Calls flagships 'update()' to move flagship.

        '''
        pygame.time.Clock().tick(60)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("You got", scoreSum, "points this round!")
                print("Thank you for playing!")
                exit()


        scoreSum = collisionDetection(flagship, wallsGroup, bandsGroup)

        keysPressed = pygame.key.get_pressed()
        flagship.handleInput(keysPressed)

        flagship.update(screenWidth, screenHeight)
        flagship.bulletsGroup.update()
       
        
        mainScreen.blit(backGround, (0,0))

        flagshipGroup.draw(mainScreen)
        flagship.bulletsGroup.draw(mainScreen)
        wallsGroup.draw(mainScreen)
        bandsGroup.draw(mainScreen)
        
        pygame.display.update()

if __name__ == '__main__':
    '''
        Run profiler function.
        Output results.
        
        Instantinate game object. 
    '''
    '''
    import cProfile
    cProfile.run("Mayhem()", "mayOutput.dat")

    import pstats
    from pstats import SortKey

    p = pstats.Stats('mayOutput.dat')
    p.sort_stats(SortKey.CUMULATIVE).print_stats(30)
    '''

    Mayhem()