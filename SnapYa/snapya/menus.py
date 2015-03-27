__author__ = 'randall'


import pygame
import kezmenu

from snapya import Game


class Menu(object):
    running = True

    def main(self, screen):
        pygame.mixer.init()
        bye_sound = pygame.mixer.Sound("../resources/PowerDown.wav")

        clock = pygame.time.Clock()
        background = pygame.image.load('../resources/snap-ya-background.jpg')
        menu = kezmenu.KezMenu(
            ['TAKE SNAP-YA', lambda: Game().main(screen)],
            ['QUIT', lambda:  setattr(self, 'running', False)],
        )
        menu.x = 300
        menu.y = 650

        while self.running:
            menu.update(pygame.event.get(), clock.tick(30)/1000)
            screen.blit(background, (240, 0))
            menu.draw(screen)
            pygame.display.flip()

        # wait for sound to play
        bye_sound.play()
        pygame.time.delay(1000)


if __name__ == '__main__':
    pygame.init()

    # would full screen be better for an event? pygame.RESIZABLE or pygame.FULLSCREEN
    screen = pygame.display.set_mode((1280, 960))
    pygame.display.set_caption("Snap-ya")
    Menu().main(screen)