from setuptools import setup

setup(
    name='pyganja',
    version='0.0.1',
    packages=['pyganja'],
    url='https://github.com/hugohadfield/pyganja',
    license='',
    author='Hugo Hadfield',
    author_email='hadfield.hugo@gmail.com',
    description='Python interface to ganja.js',
    include_package_data=True,
    install_requires = [
            'Flask',
            'cefpython3',
            'IPython',
    ],
)
