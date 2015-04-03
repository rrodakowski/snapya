__author__ = 'randall'

import pygame
import pygame.camera
import os
from services.images import AnimatedGifMaker
from pygame.locals import *


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


class Camera(object):

    def __init__(self, screen):
        pygame.camera.init()
        self.display = screen
        # self.size = (640,480)
        self.size = (960,720)
        # this is the same as what we saw before
        self.clist = pygame.camera.list_cameras()
        if not self.clist:
            raise ValueError("Sorry, no cameras detected.")
        self.cam = pygame.camera.Camera(self.clist[0], self.size)
        self.cam.start()

        # create a surface to capture to.  for performance purposes
        # bit depth is the same as that of the display surface.
        self.snapshot = pygame.surface.Surface(self.size, 0, self.display)

    def get_and_flip(self):
        # if you don't want to tie the framerate to the camera, you can check
        # if the camera has an image ready.  note that while this works
        # on most cameras, some will never return true.
        if self.cam.query_image():
            self.snapshot = self.cam.get_image(self.snapshot)

        # blit it to the display surface.  simple!
        self.display.blit(self.snapshot, (160, 120))
        pygame.display.flip()


class SnapyaImage(pygame.sprite.Sprite):

    def __init__(self, *groups):
        super(SnapyaImage, self).__init__(*groups)

        self.image = pygame.image.load('/home/randall/image.jpg')
        self.rect = pygame.rect.Rect((160, 120), self.image.get_size())

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= 10
        if key[pygame.K_RIGHT]:
            self.rect.x += 10
        if key[pygame.K_UP]:
            self.rect.y -= 10
        if key[pygame.K_DOWN]:
            self.rect.y += 10


class Game(object):

    def __init__(self):
        self.image = None
        self.snap_cam = None
        self.work_dir = "/app-data/queue"
        self.archive_dir = "/app-data/archive"
        ensure_dir(self.work_dir)
        ensure_dir(self.archive_dir)
        self.num_images = 1
        self.animator = AnimatedGifMaker()


    def main(self, screen):
        clock = pygame.time.Clock()  # slow the program down so it only runs say (30 times a second)
        self.snap_cam = Camera(screen)

        sprites = pygame.sprite.Group()

        pygame.mixer.init()
        waiting_sound = pygame.mixer.Sound("../resources/crickets.wav")
        shutter_sound = pygame.mixer.Sound("../resources/Shutter-01.wav")

        font = pygame.font.Font(None, 36)
        processing_text = font.render("Making Snap-ya", 1, (255, 255, 255))
        snap_text = font.render("Snap", 1, (255, 255, 255))
        textpos = processing_text.get_rect()
        textpos.centerx = screen.get_rect().centerx

        # event loop (a framework like piglet has this built in I believe)
        while 1:
            for event in pygame.event.get():
                clock.tick(30)  # 30 times a second (30 frames a second)

                if event.type == pygame.QUIT:
                    self.snap_cam.cam.stop()
                    screen.fill((0, 0, 0))
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.snap_cam.cam.stop()
                    screen.fill((0, 0, 0))
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    screen.blit(snap_text, textpos)
                    screen.fill((0, 0, 0))
                    pygame.display.flip()
                    print(self.work_dir+os.sep+'{}_snapya.jpg'.format(self.num_images))
                    pygame.image.save(self.snap_cam.snapshot, self.work_dir+os.sep+'{}_snapya.jpg'.format(self.num_images))
                    shutter_sound.play()
                    self.num_images += 1
                    #self.image = self.snap_cam.take_picture()
                    #SnapyaImage(sprites)
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3):
                    waiting_sound.play()
                    screen.blit(processing_text, textpos)
                    pygame.display.flip()
                    self.animator.main(self.work_dir, self.archive_dir, True )
                    self.snap_cam.cam.stop()
                    screen.fill((0, 0, 0))
                    waiting_sound.stop()
                    return

            screen.fill((0, 0, 0))
            self.snap_cam.get_and_flip()

            #sprites.update()
            #sprites.draw(screen)

            #if self.image != None:
            #    screen.blit(self.image, (100, 100))  # block image transfer
            #pygame.display.flip()  #toggle to the buffer to wich we just drew, previously displayed buffer becomes drawing buffer


if __name__ == '__main__':
    pygame.init()
    # create a display surface. standard pygame stuff
    #screen = pygame.display.set_mode((960, 720))
    #pygame.display.set_caption("Snap-ya")
    #Game().main(screen)

