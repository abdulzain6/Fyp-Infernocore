from setuptools import setup, Extension
import distutils.cygwinccompiler
distutils.cygwinccompiler.get_msvcr = lambda: []
setup(
    name="processManagement",
    version="1",
    ext_modules=[Extension("processManagement",["_processManagement.cpp"]),]
)