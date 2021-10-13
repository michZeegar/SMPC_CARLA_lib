from setuptools import setup

setup(
    name='mpc-CARLA',
    version='0.0.1',
    description='MPC controller for the CARLA vehicle simulator.',
    url="",
    author='Michael Seegerer',
    author_email='michael.seegerer@tum.de',
    license='I dont care',
    packages=['mpcCARLA'],
    install_requires=['numpy'],
    zip_safe=False
)