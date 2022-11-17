from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from setuptools import setup


setup(
    name='TLeague',
    version='1.3',
    description='Tencent Distributed League for StarCraft-II',
    keywords='League, SC2',
    packages=[
      'tleague',
    ],
    install_requires=[
      'gym',
      'joblib',
      'numpy',
      'scipy',
      'pyzmq',
      'paramiko',
      'libtmux',
      'absl-py',
      'xlrd',
      'pyyaml',
      'psutil',
      'namedlist',
      'protobuf==3.19.6',
      'opencv-contrib-python>=4.4.0.42',
      'opencv-python>=4.4.0.42',
      'diambra',
      'diambra-arena',
    ],
    scripts=['tleague/bin/tleague_horovodrun']
)
