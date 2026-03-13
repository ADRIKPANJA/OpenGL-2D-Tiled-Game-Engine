# Import Libraries
import os
import moderngl as gl

# Shader class
class Shader():
    def __init__(self, file_path):
        self.path = file_path

    def _load(self):
        with open(os.path.join(self.path, "SHADER.vert"), "r") as f:
            _vert = f.read()
        with open(os.path.join(self.path, "SHADER.frag"), "r") as f:
            _frag = f.read()
        return _vert, _frag
    
    def compile(self, ctx: gl.Context):
        _v, _f = self._load()
        return ctx.program(_v, _f)