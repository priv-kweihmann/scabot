# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only

import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassRequest(TestBaseClass):

    @pytest.mark.parametrize('kwargs', [{
        "provider": "mock",
        "project": "1", 
        "requestnum": "1", 
        "inputfiles": [TestBaseClass.file_in_testdir('bad-po-1.0.dm')]
    }])
    def test_request_properties(self, kwargs):
        _args = self._create_args(**kwargs)
        _provider = self._create_provider(_args)
        _request = self._create_request(_args, _provider)
        assert(self.has_attribute(_request, "ValidInputFiles"))
        assert(self.has_attribute(_request, "SCAFindings"))
        assert(self.has_attribute(_request, "NewNotes"))
        assert(self.has_attribute(_request, "ResolveableNotes"))

        assert(self.has_method(_request, "Process"))

    @pytest.mark.parametrize('kwargs', [{
        "provider": "mock",
        "project": "1", 
        "requestnum": "1", 
        "inputfiles": [TestBaseClass.file_in_testdir('bad-po-1.0.dm')]
    }])
    def test_request_inputfile_properties(self, kwargs):
        _args = self._create_args(**kwargs)
        _provider = self._create_provider(_args)
        _request = self._create_request(_args, _provider)

        assert(any(_request.ValidInputFiles))

        _input = _request.ValidInputFiles[0]

        assert(self.has_attribute(_input, "File"))
        assert(self.has_attribute(_input, "Scope"))
        assert(self.has_attribute(_input, "BuildPath"))
        assert(self.has_attribute(_input, "Line"))
        assert(self.has_attribute(_input, "Column"))
        assert(self.has_attribute(_input, "Severity"))
        assert(self.has_attribute(_input, "Message"))
        assert(self.has_attribute(_input, "ID"))
        assert(self.has_attribute(_input, "PackageName"))
        assert(self.has_attribute(_input, "Tool"))
        assert(self.has_attribute(_input, "BBFiles"))

        assert(self.has_method(_input, "GetPlainID"))
        assert(self.has_method(_input, "GetFormattedMessage"))
        assert(self.has_method(_input, "GetFormattedID"))
        assert(self.has_method(_input, "GetPath"))
