# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only

import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassMain(TestBaseClass):

    def test_import_main(self):
        import scabot.__main__
        with pytest.raises((SystemExit, NotImplementedError)):
            scabot.__main__.main() 
