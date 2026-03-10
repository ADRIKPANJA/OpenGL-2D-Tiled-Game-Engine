# Import libraries
import moderngl as gl
import pygame as pg
import sys
from SETTINGS import *
from scenes import *

# Initialize Pygame
pg.init()

# Intitalize graphics API
pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

# Initialize Display
SCREEN = pg.display.set_mode((SCREEN_X, SCREEN_Y), pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE, vsync=1)

# App Class
class App():
    def __init__(self):
        self.clock = pg.time.Clock()
        self.ctx = gl.create_context()
        self.scenes = [TileEngineScene(self), UIScene(self)]
        self.camX = self.camY = 0
        self.camRot = 0
        self.camZoom = 1

    def _tick(self):
        for evt in pg.event.get():
            if evt.type == pg.QUIT:
                pg.quit()
                sys.exit()
        self.ctx.clear(0,0,0)
        if self.camZoom < 0.0001:
            self.camZoom = 0.0001
        for scene in self.scenes:
            scene.tick()
        pg.display.flip()
        self.clock.tick(FPS_LIMIT)

    def run(self):
        while True:
            self._tick()

if __name__ == "__main__":
    App().run()