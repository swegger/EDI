from distutils.core import setup
import numpy as np



setup(name='EDI',
      version='1.0',
      description='Analysis of EDI data for the Department of Neurobiology at Duke',
      author='Seth Egger',
      author_email='sethegger@gmail.com',
      url='https://',
      packages=['speakerAnalysis'],
      include_dirs=[np.get_include()],
     )