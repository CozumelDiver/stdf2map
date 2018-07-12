import codecs
import os
import re
import sys
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

	
# VERSIONFILE="stdf_to_wafermap/_version.py"
# verstrline = open(VERSIONFILE, "rt").read()
# VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
# mo = re.search(VSRE, verstrline, re.M)
# if mo:
    # verstr = mo.group(1)
# else:
    # raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))
	
long_description = read('README.MD')
		
setup(name='stdf2map',
 #     version=verstr,
      version=find_version("stdf2map", "_version.py"),
      description='Generate Bin WaferMaps from STDF Files',
	  long_description=long_description,
      url='http://github.com/cozumeldiver/stdf_to_wafermap',
      keywords='stdf wafermap silicon wafer map semiconductor ATE',
      include_package_data=True,
      author='D. Fish',
      author_email='daffy@ninemoons.com',
      license='GPLv3',
      packages=['stdf2map'],
      install_requires=[
          'toml',
          'pillow'
      ],
	  entry_points={
        "console_scripts": [
            "stdf2map=stdf2map.stdf2map:main",
        ],
	  },
      classifiers=[
        "Development Status :: 4 - Beta"
	"Environment :: Console"
	"Topic :: Scientific/Engineering :: Information Analysis"
        "Intended Audience :: Science/Research"
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 2.7",
    ],
      zip_safe=False)
