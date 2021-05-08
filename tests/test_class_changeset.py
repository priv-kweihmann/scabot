# SPDX-FileCopyrightText: 2021 Konrad Weihmann
# SPDX-License-Identifier: GPL-3.0-only
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from base import TestBaseClass

class TestClassChangeset(TestBaseClass):

    @pytest.mark.parametrize('kwargs', [{
        "provider": "mock",
        "project": "1", 
        "requestnum": "1", 
        "inputfiles": [TestBaseClass.file_in_testdir('bad-po-1.0.dm')]
    }])
    def test_changeset_properties(self, kwargs):
        _args = self._create_args(**kwargs)
        _provider = self._create_provider(_args)
        _request = self._create_request(_args, _provider)
        assert(_provider.GetChanges() is not None)

        _changeset = _provider.GetChanges()

        assert(self.has_attribute(_changeset, "Changes"))
        assert(self.has_attribute(_changeset, "ChangedContent"))
        assert(self.has_method(_changeset, "AddChange"))

        assert(any(_changeset.Changes))

        _diff = _changeset.Changes[0]

        assert(self.has_attribute(_diff, "File"))
        assert(self.has_attribute(_diff, "NewFile"))
        assert(self.has_attribute(_diff, "Diff"))
        assert(self.has_attribute(_diff, "AffectedLines"))
        assert(self.has_attribute(_diff, "NewLines"))
