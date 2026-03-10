# Import Libraries
import moderngl as gl
from . import console

# Obj class
class Obj():
    def __init__(self, program: gl.Program):
        self.program = program
        self.vbos = []
        self._vao = None
    
    def add_remove_vbo_data(self, add, vbo_struct, vbo):
        if add:
            self.vbos.append((vbo, vbo_struct))
        else:
            try:
                self.vbos.remove((vbo, vbo_struct))
            except Exception:
                console.write(f"{vbo} is not found on the list")

    def setup_render(self, ctx: gl.Context):
        self._vao = ctx.vertex_array(self.program, [
            (vbo, *struct) for vbo, struct in self.vbos
        ])

    def render(self, flags=gl.TRIANGLES):
        self._vao.render(flags)

    def update_vbo_and_rebind(self, updated_vbo, ctx, *vbo_struct):
        self.vbos = updated_vbo
        self.setup_render(ctx, *vbo_struct)