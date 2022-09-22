from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
def write():
    DATA = "\ntry: __import__('pybracket').main()\nexcept ImportError: pass"
    if DATA not in open(__import__('site').__file__, 'r').read(): open(__import__('site').__file__, 'a').write(DATA)
class Install(install):
    def run(self):
        install.run(self)
        write()
class Develop(develop):
    def run(self):
        develop.run(self)
        write()
class EggInfo(egg_info):
    def run(self):
        egg_info.run(self)
        write()
setup(
    name='pybracket',
    version='1.0.1',
    license='MIT',
    author='Elisha Hollander',
    author_email='just4now666666@gmail.com',
    description="Add brackets and good semicolons to Python",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/donno2048/pybracket',
    project_urls={
        'Documentation': 'https://github.com/donno2048/pybracket#readme',
        'Bug Reports': 'https://github.com/donno2048/pybracket/issues',
        'Source Code': 'https://github.com/donno2048/pybracket',
    },
    cmdclass={
        'install': Install,
        'develop': Develop,
        'egg_info': EggInfo
    },
    packages=find_packages(),
    entry_points={ 'console_scripts': [ 'pybracket=pybracket.__main__:main' ] },
    zip_safe=False
)
