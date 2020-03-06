from setuptools import setup, find_packages
import subprocess
from setuptools.command.install import install
from distutils.command.build import build
from os import path
import os

# read the contents of our README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


version_path = os.path.join('pyganja', '_version.py')
exec(open(version_path).read())

class build_with_submodules(build):
    def run(self):
        if path.exists('.git'):
            subprocess.check_call(['git', 'submodule', 'init'])
            subprocess.check_call(['git', 'submodule', 'update'])
        build.run(self)

class install_with_submodules(install):
    def run(self):
        if path.exists('.git'):
            subprocess.check_call(['git', 'submodule', 'init'])
            subprocess.check_call(['git', 'submodule', 'update'])
        install.run(self)

setup(
    cmdclass={"build": build_with_submodules, "install": install_with_submodules},
    name='pyganja',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/hugohadfield/pyganja',
    license='MIT',
    author='Hugo Hadfield',
    author_email='hadfield.hugo@gmail.com',
    description='Python interface to ganja.js',
    include_package_data=True,
    install_requires = [
            'IPython'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
