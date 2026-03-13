# Import libraries
import core.scene
import core.obj
import moderngl as gl
import main
import numpy as np
import pygame.freetype as font
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
            0, 100, 0, 1,
            100, 0, 1, 0,
            100, 0, 1, 0,
            100, 100, 1, 1,
            0, 100, 0, 1
        ], dtype="f4")
        self.objs = [core.obj.Obj(self.program)]
        self.vbo = self.app.ctx.buffer(vbo.tobytes(), dynamic=True)
        self.objs[0].add_remove_vbo_data(True, ["2f 2f", "in_pos", "in_uv"], self.vbo)
        self.objs[0].setup_render(app.ctx)
        self.textureMap = self.app.ctx.texture((1024, 1024), 4)
        self.textureMap.use(location=0)
        self.program["tex"] = 0
        
    def tick(self):
        m = Matrix44.identity(dtype="f4")
        v = Matrix44.identity(dtype="f4")
        p = Matrix44.orthogonal_projection(0, SCREEN_X, 0, SCREEN_Y, -1, 1, dtype="f4")
        fnt = font.Font(None, 50)
        inte = round(self.app.clock.get_fps())
        tmp = fnt.render(f"FPS {inte}", (255,255,255))[0]
        x, y = tmp.get_width(), tmp.get_height()
        vbo = np.array([
            0, 0, 0, 0,
            0, y, 0, 1,
            x, 0, 1, 0,
            x, 0, 1, 0,
            x, y, 1, 1,
            0, y, 0, 1
        ], dtype="f4")
        tmp = tmp.convert_alpha(main.SCREEN)
        tmp = pg.transform.smoothscale(tmp, (1024, 1024))
        tmp = pg.image.tostring(tmp, "RGBA", True)
        self.textureMap.write(tmp)
        self.textureMap.use(location=0)
        for obj in self.objs:
            mvp = (p*v*m).astype("f4")
            mvp = mvp.tobytes()
            self.program["mvp"].write(mvp)
            self.vbo.write(vbo.tobytes())
            obj.render()

class TileEngineScene(core.scene.Scene):
    def __init__(self, app: main.App, pics: list[pg.surface.Surface]):
        super().__init__(app, 0)
        self.app = app
        self.shader = core.shader.Shader(".\\shaders\\tile_engine.shader")
        self.program = self.shader.compile(app.ctx)
        vbo = np.array([
            0, 0,
            0, SCREEN_Y, 
            SCREEN_X, 0, 
            SCREEN_X, 0, 
            SCREEN_X, SCREEN_Y, 
            0, SCREEN_Y,
        ], dtype="f4")
        self.objs = [core.obj.Obj(self.program)]
        vbo = self.app.ctx.buffer(vbo.tobytes())
        self.objs[0].add_remove_vbo_data(True, ["2f", "in_pos"], vbo)
        self.objs[0].setup_render(app.ctx)
        tileMap = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
            [0, 0, 1],
            [0, 1, 0],
            [1, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ], dtype="i4")
        self.tileMap = self.app.ctx.texture(tileMap.shape[::-1], 1, np.flipud(tileMap).tobytes(), dtype="i4")
        self.tileMap.filter = (gl.NEAREST, gl.NEAREST)
        self.tileMap.use(location=0)
        self.program["tileMap"] = 0
        self.compiledAtlas = self.app.ctx.texture_array((256, 256, len(pics)), 4)
        # Create atlas
        for i, pic in enumerate(pics):
            pic = pg.transform.smoothscale(pic, (256, 256))
            data = pg.image.tostring(pic, "RGBA", True)
            self.compiledAtlas.write(
                data,
                viewport=(0, 0, i, 256, 256, 1)
            )
        self.compiledAtlas.use(location=1)
        self.program["tileAtlas"] = 1
        self.program["TILE_SIZE"] = 64.0

    def tick(self):
        v = (
            Matrix44.from_translation((SCREEN_X/2, SCREEN_Y/2, 0), dtype="f4") *
            Matrix44.from_scale((self.app.camZoom, self.app.camZoom, 1), dtype="f4") *
            Matrix44.from_z_rotation(np.radians(-self.app.camRot), dtype="f4") *
            Matrix44.from_translation((-self.app.camX, -self.app.camY, 0), dtype="f4") *
            Matrix44.from_translation((-SCREEN_X/2, -SCREEN_Y/2, 0), dtype="f4")
        )
        p = Matrix44.orthogonal_projection(0, SCREEN_X, 0, SCREEN_Y, -1, 1, dtype="f4")
        self.tileMap.use(location=0)
        self.program["p"].write(p.tobytes())
        self.program["invView"].write(np.linalg.inv(v).tobytes())
        self.tileMap.use(location=0)
        self.compiledAtlas.use(location=1)
        keys = pg.key.get_pressed()
        self.app.camX += (keys[pg.K_d] - keys[pg.K_a]) * 10
        self.app.camY += (keys[pg.K_w] - keys[pg.K_s]) * 10
        self.app.camRot += (keys[pg.K_UP] - keys[pg.K_DOWN]) * 5
        self.app.camZoom += (keys[pg.K_LEFT] - keys[pg.K_RIGHT]) * 0.1
        for obj in self.objs:
            obj.render()