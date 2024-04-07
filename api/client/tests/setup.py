from distutils.core import setup, Extension

module = Extension('mouseBlock',
                    sources = ['mouse_blovk_test.cpp'])

setup(name='MouseBlockPackage',
      version='1.0',
      description='Mouse movement blocker',
      ext_modules=[module])
