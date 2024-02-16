from setuptools import setup, Extension
import distutils.cygwinccompiler
distutils.cygwinccompiler.get_msvcr = lambda: []
setup(
    name="mouseBlock",
    version="1",
    ext_modules=[Extension("mouseBlock",["mouseBlock.cpp"]),]
)