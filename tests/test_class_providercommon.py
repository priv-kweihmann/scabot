# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only

import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassProdiverCommon(TestBaseClass):

    @pytest.mark.parametrize('kwargs', [{
        "provider": "mock",
        "project": "1", 
        "requestnum": "1", 
        "inputfiles": [TestBaseClass.file_in_testdir('bad-po-1.0.dm')]
    }])
    def test_prodiver_properties(self, kwargs):
        _args = self._create_args(**kwargs)
        _provider = self._create_provider(_args)
        assert(self.has_attribute(_provider, "Valid"))
        assert(self.has_attribute(_provider, "AllowDrafts"))

        assert(isinstance(_provider.Valid, bool))
        assert(isinstance(_provider.AllowDrafts, bool))
