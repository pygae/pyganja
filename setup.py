from setuptools import setup, find_packages
import subprocess
from distutils.command.install import install
from distutils.command.build import build
from os import path

class build_with_submodules(build):
    def run(self):
        if path.exists('.git'):
            subprocess.check_call(['git', 'submodule', 'init'])
            subprocess.check_call(['git', 'submodule', 'update'])
            subprocess.check_call(['git', 'submodule', 'foreach', 'git', 'pull', 'origin', 'master'])
        build.run(self)

class install_with_submodules(install):
    def run(self):
        if path.exists('.git'):
            subprocess.check_call(['git', 'submodule', 'init'])
            subprocess.check_call(['git', 'submodule', 'update'])
            subprocess.check_call(['git', 'submodule', 'foreach', 'git', 'pull', 'origin', 'master'])
        install.run(self)

setup(
    cmdclass={"build": build_with_submodules, "install": install_with_submodules},
    name='pyganja',
    version='0.0.2',
    packages=find_packages(),
    url='https://github.com/hugohadfield/pyganja',
    license='',
    author='Hugo Hadfield',
    author_email='hadfield.hugo@gmail.com',
    description='Python interface to ganja.js',
    include_package_data=True,
    install_requires = [
            'IPython'
    ],
)
