import platform
import logging
import os
import sys
from glob import glob
from setuptools import setup
from distutils.command.build import build
from setuptools.command.easy_install import easy_install

assert sys.version_info[0:2] == (3,5)
assert platform.python_implementation() == 'CPython'
assert platform.system() == 'Linux'
assert platform.machine() == 'x86_64'

class BuildWithSO(build):
    def run(self):
        build.run(self)
        for path in glob(os.path.join(os.path.dirname(__file__),  '*.so')):
            dest = os.path.join(self.build_lib, os.path.basename(path))
            logging.info("Copying %s to %s." % (path, dest))
            self.copy_file(path, dest)

class EasyInstallWithSO(easy_install):
    def run(self):
        easy_install.run(self)
        for path in glob(os.path.join(os.path.dirname(__file__),  '*.so')):
            dest = os.path.join(self.install_dir, os.path.basename(path))
            logging.info("Copying %s to %s." % (path, dest))
            self.copy_file(path, dest)

setup(
    name = "PyV8",
    version = "8.1.0",
    py_modules=['PyV8'],
    zip_safe=False,
    include_package_data=True,
    package_data={'':['_PyV8.so']},
    cmdclass={
        'build': BuildWithSO,
        'easy_install': EasyInstallWithSO,
    }
)


