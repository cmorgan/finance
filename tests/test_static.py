import subprocess
import os

import nose.tools as T

THIS_DIR = os.path.dirname(__file__)
MOD_DIR = os.path.join(THIS_DIR, '..')


def test_flake8():
    retcode = subprocess.call(['flake8',
                               '--ignore=E123,E125,E126,E128',
                               MOD_DIR])
    T.assert_equal(retcode, 0, 'Flake8 failed!')
