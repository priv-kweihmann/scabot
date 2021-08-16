# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only

from logging import log
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassFullScenarios(TestBaseClass):

    @pytest.mark.parametrize('kwargs', [{
        "provider": "mock",
        "project": "1", 
        "requestnum": "1", 
        "inputfiles": [TestBaseClass.file_in_testdir('bad-po-1.0.dm')]
    }])
    def test_scenario_nohit(self, kwargs):
        _args = self._create_args(**kwargs)
        _provider = self._create_provider(_args)
        _request = self._create_request(_args, _provider)
        assert(not any(_request.SCAFindings))

    @pytest.mark.parametrize('kwargs', [{
        "provider": "mock",
        "project": "1", 
        "requestnum": "2", 
        "inputfiles": [TestBaseClass.file_in_testdir('bad-po-1.0.dm')],
        "preargs": ["--comment_only_affected_lines"]
    }])
    def test_request_hit_only_affected(self, kwargs):
        _args = self._create_args(**kwargs)
        _provider = self._create_provider(_args)
        _request = self._create_request(_args, _provider)

        assert(any(_request.SCAFindings))

        _finding = next(iter(_request.SCAFindings))

        assert(_finding.Line == "45")
        assert(_finding.Column ==  "1")
        assert(_finding.Severity ==  "warning")
        assert(_finding.Message ==  "number of lines: 2 in string, 3 in translation")
        assert(_finding.ID ==  "lines")
        assert(_finding.PackageName ==  "bad-po")
        assert(_finding.Tool ==  "msgcheck")
        assert(_finding.Scope ==  "style")

    @pytest.mark.parametrize('kwargs', [{
        "provider": "mock",
        "project": "1", 
        "requestnum": "2", 
        "inputfiles": [TestBaseClass.file_in_testdir('bad-po-1.0.dm')],
        "preargs": ["--botuser=foo"]
    }])
    def test_request_hit_all(self, kwargs):
        _args = self._create_args(**kwargs)
        _provider = self._create_provider(_args)
        _request = self._create_request(_args, _provider)

        assert(any(_request.SCAFindings))
        assert(len(_request.SCAFindings) > 1)

        assert(len(_request.NewNotes) == 9)
        assert(len(_request.ResolveableNotes) == 1)

    @pytest.mark.parametrize('kwargs', [{
        "provider": "mock",
        "project": "1", 
        "requestnum": "2", 
        "inputfiles": [TestBaseClass.file_in_testdir('bad-po-1.0.dm')],
        "preargs": ["--botuser=foo"]
    }])
    def test_request_process(self, kwargs):
        from scabot.notes import Note

        _args = self._create_args(**kwargs)
        _provider = self._create_provider(_args)
        _request_one = self._create_request(_args, _provider)

        assert(any(_request_one.SCAFindings))

        assert(any(_request_one.NewNotes))
        assert(any(_request_one.ResolveableNotes))

        _request_one.Process()

        _resolvable_note = next(iter(_request_one.ResolveableNotes))

        assert(_resolvable_note.resolved)

        _result = _provider.GetCurrentStatus()
        _notes = _result['projects'][kwargs['project']]['requests'][kwargs['requestnum']]['notes']

        assert(any(Note(n) == _resolvable_note) for n in _notes)
        for note in _request_one.NewNotes:
            assert(any(Note(n) == note) for n in _notes)

    @pytest.mark.parametrize('kwargs', [{
        "provider": "mock",
        "project": "1", 
        "requestnum": "5", 
        "inputfiles": [TestBaseClass.file_in_testdir('bad-po-1.0.dm')],
        "preargs": ["--botuser=foo"]
    }])
    def test_request_no_process_draft(self, kwargs):
        from scabot.notes import Note

        _args = self._create_args(**kwargs)
        _provider = self._create_provider(_args)
        _request_one = self._create_request(_args, _provider)

        assert(any(_request_one.SCAFindings))
        assert(any(_request_one.NewNotes))

        _request_one.Process()

        _result = _provider.GetCurrentStatus()
        _notes = _result['projects'][kwargs['project']]['requests'][kwargs['requestnum']]['notes']

        assert(not any(_notes))

    @pytest.mark.parametrize('kwargs', [{
        "provider": "mock",
        "project": "1", 
        "requestnum": "5", 
        "inputfiles": [TestBaseClass.file_in_testdir('bad-po-1.0.dm')],
        "preargs": ["--botuser=foo", "--comment_drafts"]
    }])
    def test_request_process_draft(self, kwargs):
        from scabot.notes import Note

        _args = self._create_args(**kwargs)
        _provider = self._create_provider(_args)
        _request_one = self._create_request(_args, _provider)

        _request_one.Process()

        assert(any(_request_one.SCAFindings))
        assert(any(_request_one.NewNotes))

        _result = _provider.GetCurrentStatus()
        _notes = _result['projects'][kwargs['project']]['requests'][kwargs['requestnum']]['notes']

        assert(any(_notes))

    @pytest.mark.parametrize('kwargs', [{
        "provider": "mock",
        "project": "1", 
        "requestnum": "6", 
        "inputfiles": [TestBaseClass.file_in_testdir('bad-po-1.0.dm')],
        "preargs": ["--botuser=foo", "--comment_indirect"]
    }])
    def test_request_process_indirect(self, kwargs):
        from scabot.notes import Note

        _args = self._create_args(**kwargs)
        _provider = self._create_provider(_args)
        _request_one = self._create_request(_args, _provider)

        assert(any(_request_one.SCAFindings))
        assert(any(_request_one.NewNotes))

        _request_one.Process()

        _result = _provider.GetCurrentStatus()
        _notes = _result['projects'][kwargs['project']]['requests'][kwargs['requestnum']]['notes']

        assert(any(_notes))

    @pytest.mark.parametrize('kwargs', [{
        "provider": "mock",
        "project": "1", 
        "requestnum": "6", 
        "inputfiles": [TestBaseClass.file_in_testdir('bad-po-1.0.dm')],
        "preargs": ["--botuser=foo"]
    }])
    def test_request_process_indirect_off(self, kwargs):
        from scabot.notes import Note

        _args = self._create_args(**kwargs)
        _provider = self._create_provider(_args)
        _request_one = self._create_request(_args, _provider)

        assert(not any(_request_one.SCAFindings))
        assert(not any(_request_one.NewNotes))

        _request_one.Process()

        _result = _provider.GetCurrentStatus()
        _notes = _result['projects'][kwargs['project']]['requests'][kwargs['requestnum']]['notes']

        assert(not any(_notes))

    @pytest.mark.parametrize('kwargs', [{
        "provider": "mock",
        "project": "1", 
        "requestnum": "6", 
        "inputfiles": [TestBaseClass.file_in_testdir('bad-po-1.0.dm')],
        "preargs": ["--incomplete", "--comment_indirect"]
    }])
    def test_request_process_incomplete(self, kwargs):
        from scabot.notes import Note

        _args = self._create_args(**kwargs)
        _provider = self._create_provider(_args)
        _request_one = self._create_request(_args, _provider)

        assert(any(_request_one.SCAFindings))
        assert(any(_request_one.NewNotes))
        assert(not any(_request_one.ResolveableNotes))
