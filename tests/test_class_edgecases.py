# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only

import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassEdgeCases(TestBaseClass):

    @pytest.mark.parametrize('kwargs', [{
        "provider": "mock",
        "project": "1", 
        "requestnum": "3", 
        "inputfiles": [TestBaseClass.file_in_testdir('bad-po-1.0.dm')]
    }])
    def test_patch_without_header(self, kwargs):
        _args = self._create_args(**kwargs)
        _provider = self._create_provider(_args)
        
        assert(any(_provider.GetChanges().Changes))

    @pytest.mark.parametrize('kwargs', [{
        "provider": "mock",
        "project": "1", 
        "requestnum": "2", 
        "inputfiles": ["/does/not/exist"]
    }])
    def test_scafile_not_exists(self, kwargs):
        _args = self._create_args(**kwargs)
        _provider = self._create_provider(_args)
        _request = self._create_request(_args, _provider)
        
        assert(not any(_request.ValidInputFiles))

    @pytest.mark.parametrize('kwargs', [{
        "provider": "mock",
        "project": "1", 
        "requestnum": "2", 
        "inputfiles": [TestBaseClass.file_in_testdir('corrupt.dm')]
    }])
    def test_scafile_corrupt(self, kwargs):
        _args = self._create_args(**kwargs)
        _provider = self._create_provider(_args)
        _request = self._create_request(_args, _provider)
        
        assert(not any(_request.ValidInputFiles))
    
    @pytest.mark.parametrize('kwargs', [{
        "provider": "mock",
        "project": "1", 
        "requestnum": "2", 
        "inputfiles": [TestBaseClass.file_in_testdir('corrupt.dm')]
    }])
    def test_provider_abstract(self, kwargs):
        from scabot.provider import Provider

        _args = self._create_args(**kwargs)

        with pytest.raises(TypeError):
            _provider = Provider(_args, 'foo', 'bar', 'baz')

        from scabot.provider.mock import MockProvider

        _provider = MockProvider(_args, 'foo', 'bar', TestBaseClass.TESTFILES_DIR, '1', '1')

        assert(_provider.Username == 'foo')
        assert(_provider.Token == 'bar')
        assert(_provider.ServerURL == TestBaseClass.TESTFILES_DIR)

    @pytest.mark.parametrize('kwargs', [{
        "provider": "mock",
        "project": "1", 
        "requestnum": "2", 
        "inputfiles": [TestBaseClass.file_in_testdir('corrupt.dm')]
    }])
    def test_provider_exceptions(self, kwargs):
        _args = self._create_args(**kwargs)

        from scabot.provider.mock import MockProvider
        from scabot.provider import SCABotProjectNotFoundError
        from scabot.provider import SCABotRequestNotFoundError

        with pytest.raises(SCABotProjectNotFoundError):
            _provider = MockProvider(_args, _args.botuser, _args.bottoken, _args.server, "3", "1")

        with pytest.raises(SCABotRequestNotFoundError):
            _provider = MockProvider(_args, _args.botuser, _args.bottoken, _args.server, "1", "4")
        