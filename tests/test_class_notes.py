# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only

import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassNotes(TestBaseClass):

    @pytest.mark.parametrize('kwargs', [{
        "provider": "mock",
        "project": "1", 
        "requestnum": "1", 
        "inputfiles": [TestBaseClass.file_in_testdir('bad-po-1.0.dm')]
    }])
    def test_notes_properties(self, kwargs):
        _args = self._create_args(**kwargs)
        _provider = self._create_provider(_args)
        _request = self._create_request(_args, _provider)
        assert(any(_provider.GetNotes()))
        assert(self.has_attribute(_provider.GetNotes()[0], "body"))
        assert(self.has_attribute(_provider.GetNotes()[0], "can_resolve"))
        assert(self.has_attribute(_provider.GetNotes()[0], "lines"))
        assert(self.has_attribute(_provider.GetNotes()[0], "path"))
        assert(self.has_attribute(_provider.GetNotes()[0], "resolved"))
        assert(self.has_attribute(_provider.GetNotes()[0], "user"))
        assert(self.has_attribute(_provider.GetNotes()[0], "reference"))

    @pytest.mark.parametrize('kwargs', [{
        "provider": "mock",
        "project": "1", 
        "requestnum": "1", 
        "inputfiles": [TestBaseClass.file_in_testdir('bad-po-1.0.dm')]
    }])
    def test_notes_properties_writebale(self, kwargs):
        _args = self._create_args(**kwargs)
        _provider = self._create_provider(_args)
        _request = self._create_request(_args, _provider)

        _provider.GetNotes()[0].path = 'foo'
        _provider.GetNotes()[0].body = 'foo'
        _provider.GetNotes()[0].resolved = True

    def test_notes_compare(self):
        from scabot.notes import Note

        a = Note("a", "a", "a", 1)
        b = Note("a", "a", "a", 1)
        c = Note("a", "a", "a", 4, 1)
        d = Note("b", "a", "a", 1)

        e = list()
        # test __eq__ function
        assert(a == b == c)
        # test __ne__ function
        assert(d != a)
        # test type safety
        assert(a != e)

    def test_notes_resolvable(self):
        from scabot.notes import Note

        a = Note("a", "a", "a", 1, can_resolve=False)
        a.resolved = True

        assert(not a.resolved)
