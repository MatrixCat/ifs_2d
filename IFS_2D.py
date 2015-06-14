#!/usr/bin/python
"""
 Simple Symmetric IFS
"""
import pygame, math, random
from pygame.locals import *

class Simulation:
    def __init__(self, num_attractors=3, attractor_weight=0.5, scale=1.0):
        pygame.init()
        self.myfont = pygame.font.SysFont("monospace", 16)

        self.screen = pygame.display.set_mode((1280, 800))
        #self.screen = pygame.display.set_mode((1280, 800), pygame.FULLSCREEN)
        pygame.display.set_caption("Simple IFS in 2D")

        self.clock = pygame.time.Clock()
        self.num_attractors = num_attractors
        self.attractor_weight = attractor_weight
        self.current_scale = scale
        self.pointspeed = 1024
        self.pointcolour = pygame.Color(0,255,0,128)
        self.colourspeed = 256
        self.showinfo = 0
        self.showattractors = 1
        self.showhelp = 0
        self.reset()

    def reset(self):
        """ Clear screen and reset attractors."""
        self.screen.fill((0,0,0))
        self.xpos = 0
        self.ypos = 0
        self.newxpos = self.xpos
        self.newypos = self.ypos
        self.attractors = []
        # Generate a circle of attractors
        for count in range(self.num_attractors):
            # An attractor has x,y coordinates
            attractor = [math.sin(count*2*math.pi/self.num_attractors), -math.cos(count*2*math.pi/self.num_attractors)]
            self.attractors.append(attractor)
            if self.showattractors:
                screenx = self.screen.get_width()/2  + attractor[0] * self.current_scale*2
                screeny = self.screen.get_height()/2 + attractor[1] * self.current_scale*2
                self.screen.fill((0,0,128),(screenx-16,screeny-16,32,32))
         
    def render(self):
        """ Draw a set of points per frame """
        for n in range(self.pointspeed):
            chosen_one = random.randint(0, self.num_attractors-1)
            self.xpos = self.xpos * self.attractor_weight + self.attractors[chosen_one][0];
            self.ypos = self.ypos * self.attractor_weight + self.attractors[chosen_one][1];
            screenx = int((self.screen.get_width()/2  + self.xpos * self.current_scale)) % self.screen.get_width();
            screeny = int((self.screen.get_height()/2 + self.ypos * self.current_scale)) % self.screen.get_height();
            colour  = self.screen.get_at((screenx, screeny)).g + self.colourspeed;
            if colour > 255:
                colour = 255
            #colour = self.pointcolour
            self.screen.set_at((screenx, screeny), pygame.Color(0,colour,0));
            #self.screen.fill((0,255,0),(self.xpos-1,self.ypos-1,self.xpos+1,self.ypos+1))
        textx = 16
        texty = 16
        if self.showinfo:
            self.screen.fill((0,0,0),(16,16,320,256))
            text = self.myfont.render("Number of Attractors : "+str(self.num_attractors), 1, (255, 255, 0))
            self.screen.blit(text, (textx, texty))
            texty += 16
            text = self.myfont.render("Weight : "+str(self.attractor_weight), 1, (255, 255, 0))
            self.screen.blit(text, (textx, texty))
            texty += 16
            text = self.myfont.render("Colour increase per point : "+str(self.colourspeed), 1, (255, 255, 0))
            self.screen.blit(text, (textx, texty))
            texty += 16
            text = self.myfont.render("Points drawn per frame : "+str(self.pointspeed), 1, (255, 255, 0))
            self.screen.blit(text, (textx, texty))
            texty += 16
            text = self.myfont.render("Scale multiplier : "+str(self.current_scale), 1, (255, 255, 0))
            self.screen.blit(text, (textx, texty))
                
    def run(self):
        """ Main Loop """
        while 1:
            # Lock the framerate at 50 FPS.
            self.clock.tick(50)

            # Handle events.
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))
                    if event.key == K_r:
                        self.reset()
                    if event.key == K_c:
                        self.screen.fill((0,0,0))
                    if event.key == K_z:
                        self.num_attractors -= 1
                        if self.num_attractors<2:
                            self.num_attractors=2
                        #self.reset()
                    if event.key == K_x:
                        self.num_attractors += 1
                        self.reset()
                    if event.key == K_EQUALS:
                        self.current_scale *= 2
                    if event.key == K_MINUS:
                        self.current_scale /= 2
                    if event.key == K_COMMA:
                        self.attractor_weight -= 0.01
                    if event.key == K_PERIOD:
                        self.attractor_weight += 0.01
                    if event.key == K_LEFTBRACKET:
                        self.colourspeed /= 2
                        if self.colourspeed < 1:
                            self.colourspeed = 1
                    if event.key == K_RIGHTBRACKET:
                        self.colourspeed *= 2
                        if self.colourspeed > 256:
                            self.colourspeed = 256
                    if event.key == K_a:
                        self.showattractors = 1 - self.showattractors
                    if event.key == K_TAB:
                        self.showinfo = 1 - self.showinfo
                    if event.key == K_SLASH:
                        self.showhelp = 1 - self.showhelp
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            
            self.render()
            pygame.display.flip()

if __name__ == "__main__":
    Simulation(3, 0.5, 180).run()
