# Import libraries
import core.scene
import core.obj
import moderngl as gl
import main
import numpy as np
import core.shader
from SETTINGS import *
import pygame as pg
from pyrr import Matrix44

# Scene class
class UIScene(core.scene.Scene):
    def __init__(self, app: main.App):
        super().__init__(app, 0)
        self.app = app
        self.shader = core.shader.Shader(".\\shaders\\basic.shader")
        self.program = self.shader.compile(app.ctx)
        vbo = np.array([
            0, 0, 0, 0,
            0, SCREEN_Y, 0, 1,
            SCREEN_X, 0, 1, 0,
            SCREEN_X, 0, 1, 0,
            SCREEN_X, SCREEN_Y, 1, 1,
            0, SCREEN_Y, 0, 1
        ], dtype="f4")
        self.objs = [core.obj.Obj(self.program)]
        self.objs[0].add_remove_vbo_data(True, ["2f 2f", "in_pos", "in_uv"], self.app.ctx.buffer(vbo.tobytes()))
        self.objs[0].setup_render(app.ctx)
        self.textureMap = self.app.ctx.texture((1024, 1024), 4)
        self.textureMap.use(location=0)
        self.program["tex"] = 0
        
    def tick(self):
        m = Matrix44.identity(dtype="f4")
        v = Matrix44.identity(dtype="f4")
        p = Matrix44.orthogonal_projection(0, SCREEN_X, 0, SCREEN_Y, -1, 1, dtype="f4")
        fnt = pg.font.Font(None, 1000)
        tmp = fnt.render("Hello World", False, (1,1,1), None)
        tmp = tmp.convert_alpha(main.SCREEN)
        tmp = pg.transform.smoothscale(tmp, (1024, 1024))
        tmp = pg.image.tostring(tmp, "RGBA", True)
        self.textureMap.write(tmp)
        self.textureMap.use(location=0)
        for obj in self.objs:
            mvp = (p*v*m).astype("f4")
            mvp = mvp.tobytes()
            self.program["mvp"].write(mvp)
            obj.render()